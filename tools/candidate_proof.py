from __future__ import annotations

import argparse
import hashlib
import pathlib
import subprocess
from dataclasses import dataclass


DEFAULT_BOOT_SHA256 = "14269D687B944965107E527A6E1AFEE8F24FB6D30EF17E1492530A36D1CDAAB0"


@dataclass(frozen=True)
class ProofConfig:
    python: str
    edl_py: str
    loader: str
    port: str
    memory: str = "emmc"


def build_edl_command(cfg: ProofConfig, operation: str, *args: str) -> list[str]:
    return [
        cfg.python,
        cfg.edl_py,
        operation,
        *args,
        f"--loader={cfg.loader}",
        f"--memory={cfg.memory}",
        f"--portname={cfg.port}",
        "--serial",
    ]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def require_baseline_match(data: bytes, expected_sha256: str) -> None:
    actual = sha256_bytes(data)
    if actual != expected_sha256.upper():
        raise RuntimeError(
            f"baseline SHA-256 mismatch: expected {expected_sha256.upper()}, got {actual}"
        )


def run(cmd: list[str]) -> None:
    print("+", subprocess.list2cmdline(cmd), flush=True)
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="TECHGUYTOOL-VIVO controlled Firehose candidate proof for PD1730BF_EX"
    )
    parser.add_argument("--python", required=True)
    parser.add_argument("--edl-py", required=True)
    parser.add_argument("--loader", required=True)
    parser.add_argument("--port", required=True, help=r"Windows serial path, e.g. \\.\COM10")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--expected-boot-sha256", default=DEFAULT_BOOT_SHA256)
    parser.add_argument(
        "--same-data-write-proof",
        action="store_true",
        help="After read/hash verification, write the exact dump back and re-read it.",
    )
    args = parser.parse_args()

    cfg = ProofConfig(args.python, args.edl_py, args.loader, args.port)
    workdir = pathlib.Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    before = workdir / "boot-proof-before.bin"
    after = workdir / "boot-proof-after.bin"

    # Read-only compatibility gate first.
    run(build_edl_command(cfg, "printgpt"))
    run(build_edl_command(cfg, "getstorageinfo"))
    run(build_edl_command(cfg, "r", "boot", str(before)))

    before_hash = sha256_file(before)
    print(f"BOOT_BEFORE_SHA256={before_hash}")
    if before_hash != args.expected_boot_sha256.upper():
        raise RuntimeError(
            "baseline SHA-256 mismatch: refusing any write; "
            f"expected {args.expected_boot_sha256.upper()}, got {before_hash}"
        )

    if not args.same_data_write_proof:
        print("READ_ONLY_PROOF=PASS")
        return 0

    # The only permitted write in this harness is byte-for-byte identical boot data.
    run(build_edl_command(cfg, "w", "boot", str(before)))
    run(build_edl_command(cfg, "r", "boot", str(after)))
    after_hash = sha256_file(after)
    print(f"BOOT_AFTER_SHA256={after_hash}")
    if after_hash != before_hash:
        raise RuntimeError(
            f"post-write SHA-256 mismatch: before {before_hash}, after {after_hash}"
        )

    print("SAME_DATA_WRITE_PROOF=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
