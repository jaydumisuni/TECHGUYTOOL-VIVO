from __future__ import annotations

import importlib.util
import pathlib

import pytest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "tools" / "direct_sahara_upload.py"


def load_module():
    spec = importlib.util.spec_from_file_location("direct_sahara_upload", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeData:
    version = 2


class FakeSahara:
    def __init__(self, upload_result: str = "firehose"):
        self.programmer = ""
        self.upload_result = upload_result
        self.upload_versions: list[int] = []

    def upload_loader(self, *, version: int) -> str:
        self.upload_versions.append(version)
        return self.upload_result


def test_explicit_upload_requires_initial_sahara():
    module = load_module()
    sahara = FakeSahara()
    with pytest.raises(RuntimeError, match="initial mode must be sahara"):
        module.upload_explicit_loader(sahara, "candidate.mbn", {"mode": "firehose"})
    assert sahara.upload_versions == []


def test_explicit_upload_skips_cmd_info_and_requires_firehose_result():
    module = load_module()
    sahara = FakeSahara()
    result = module.upload_explicit_loader(
        sahara,
        "candidate.mbn",
        {"mode": "sahara", "data": FakeData()},
    )
    assert result == "firehose"
    assert sahara.programmer == "candidate.mbn"
    assert sahara.upload_versions == [2]


def test_default_serial_timeout_is_bounded_seconds():
    module = load_module()
    assert module.DEFAULT_SERIAL_TIMEOUT_SECONDS == 5.0


def test_apply_serial_timeout_overrides_legacy_value():
    module = load_module()

    class FakeCdc:
        timeout = 1500

    cdc = FakeCdc()
    module.apply_serial_timeout(cdc)
    assert cdc.timeout == 5.0
