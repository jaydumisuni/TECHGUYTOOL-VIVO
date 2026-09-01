import hashlib
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from candidate_proof import ProofConfig, build_edl_command, require_baseline_match


class CandidateProofTests(unittest.TestCase):
    def test_build_edl_command_pins_candidate_and_serial_port(self):
        cfg = ProofConfig(
            python=r"D:\projects\TECHGUY TOOL VIVO\.venv\Scripts\python.exe",
            edl_py=r"D:\projects\my tool\for use\Android\edl-master\edl.py",
            loader=r"D:\projects\TECHGUY TOOL VIVO\loaders\V9_YOUTH_PD1730BF.mbn",
            port=r"\\.\COM10",
        )
        cmd = build_edl_command(cfg, "printgpt")
        self.assertEqual(cmd[:2], [cfg.python, cfg.edl_py])
        self.assertIn("printgpt", cmd)
        self.assertIn(f"--loader={cfg.loader}", cmd)
        self.assertIn(f"--portname={cfg.port}", cmd)
        self.assertIn("--serial", cmd)
        self.assertIn("--memory=emmc", cmd)

    def test_baseline_guard_accepts_exact_boot_hash(self):
        data = b"known boot content"
        expected = hashlib.sha256(data).hexdigest().upper()
        require_baseline_match(data, expected)

    def test_baseline_guard_rejects_any_hash_mismatch(self):
        with self.assertRaisesRegex(RuntimeError, "baseline SHA-256 mismatch"):
            require_baseline_match(b"different", "00" * 32)


if __name__ == "__main__":
    unittest.main()
