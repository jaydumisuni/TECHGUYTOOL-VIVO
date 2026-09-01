from __future__ import annotations

import argparse
import hashlib
import pathlib
import urllib.request


CANDIDATES = {
    "v9-youth-pd1730bf": {
        "url": "https://raw.githubusercontent.com/Iqinix/Qualcomm-firehoses/main/Vivo/V9_YOUTH_PD1730BF.mbn",
        "size": 387361,
        "git_sha1": "6c1ae1dd5894d5f082f4c1c8dcd5c9194104e10f",
        "filename": "V9_YOUTH_PD1730BF.mbn",
    },
    "v9-youth-elf": {
        "url": "https://raw.githubusercontent.com/Iqinix/Qualcomm-firehoses/main/Vivo/V9_YOUTH.elf",
        "size": 406200,
        "git_sha1": "8fa768e4abb08defd77e1e73879c68a78b3eed3a",
        "filename": "V9_YOUTH.elf",
    },
}


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def verify_blob(data: bytes, *, expected_size: int, expected_git_sha1: str) -> None:
    if len(data) != expected_size:
        raise RuntimeError(f"size mismatch: expected {expected_size}, got {len(data)}")
    actual = git_blob_sha1(data)
    if actual.lower() != expected_git_sha1.lower():
        raise RuntimeError(
            f"Git blob SHA-1 mismatch: expected {expected_git_sha1.lower()}, got {actual.lower()}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage a pinned public Vivo Firehose candidate")
    parser.add_argument("candidate", choices=sorted(CANDIDATES))
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    meta = CANDIDATES[args.candidate]
    with urllib.request.urlopen(meta["url"], timeout=60) as response:
        data = response.read()
    verify_blob(data, expected_size=meta["size"], expected_git_sha1=meta["git_sha1"])

    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / meta["filename"]
    out.write_bytes(data)
    print(f"STAGED={out}")
    print(f"BYTES={len(data)}")
    print(f"GIT_BLOB_SHA1={git_blob_sha1(data)}")
    print(f"SHA256={hashlib.sha256(data).hexdigest().upper()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
