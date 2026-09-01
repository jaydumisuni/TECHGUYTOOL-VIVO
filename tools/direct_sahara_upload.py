from __future__ import annotations

import argparse
import logging
import pathlib
import sys
from typing import Any


DEFAULT_SERIAL_TIMEOUT_SECONDS = 5.0


def apply_serial_timeout(cdc: Any, timeout_seconds: float = DEFAULT_SERIAL_TIMEOUT_SECONDS) -> None:
    if timeout_seconds <= 0:
        raise ValueError("serial timeout must be greater than zero")
    cdc.timeout = float(timeout_seconds)


def upload_explicit_loader(sahara_obj: Any, loader: str, initial_response: dict[str, Any]) -> str:
    mode = initial_response.get("mode")
    if mode != "sahara":
        raise RuntimeError(f"initial mode must be sahara, got {mode!r}")

    data = initial_response.get("data")
    version = getattr(data, "version", 2)
    sahara_obj.programmer = loader
    result = sahara_obj.upload_loader(version=version)
    if result != "firehose":
        raise RuntimeError(f"explicit loader did not reach firehose, got {result!r}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Upload one explicit Qualcomm programmer directly from a proven Sahara hello"
    )
    parser.add_argument("--edl-root", required=True)
    parser.add_argument("--loader", required=True)
    parser.add_argument("--port", required=True)
    args = parser.parse_args()

    edl_root = pathlib.Path(args.edl_root).resolve()
    loader = pathlib.Path(args.loader).resolve()
    if not (edl_root / "edlclient").is_dir():
        raise RuntimeError(f"invalid edl root: {edl_root}")
    if not loader.is_file():
        raise RuntimeError(f"loader not found: {loader}")

    sys.path.insert(0, str(edl_root))
    from edlclient.Config.usb_ids import default_ids
    from edlclient.Library.Connection.seriallib import serial_class
    from edlclient.Library.sahara import sahara

    cdc = serial_class(loglevel=logging.INFO, portconfig=default_ids)
    apply_serial_timeout(cdc)
    if not cdc.connect(portname=args.port):
        raise RuntimeError(f"unable to open {args.port}")

    try:
        client = sahara(cdc, loglevel=logging.INFO)
        initial = client.connect()
        print(f"INITIAL_MODE={initial.get('mode')}", flush=True)
        data = initial.get("data")
        if data is not None and hasattr(data, "version"):
            print(f"SAHARA_VERSION={data.version}", flush=True)
        result = upload_explicit_loader(client, str(loader), initial)
        print(f"UPLOAD_MODE={result}", flush=True)
        print("DIRECT_SAHARA_UPLOAD=PASS", flush=True)
        return 0
    finally:
        cdc.close()


if __name__ == "__main__":
    raise SystemExit(main())
