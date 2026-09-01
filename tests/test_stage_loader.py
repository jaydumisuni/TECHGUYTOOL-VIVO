import hashlib
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from stage_loader import git_blob_sha1, verify_blob


class StageLoaderTests(unittest.TestCase):
    def test_git_blob_sha1_matches_git_object_format(self):
        data = b"abc"
        expected = hashlib.sha1(b"blob 3\0abc").hexdigest()
        self.assertEqual(git_blob_sha1(data), expected)

    def test_verify_blob_rejects_wrong_size(self):
        with self.assertRaisesRegex(RuntimeError, "size mismatch"):
            verify_blob(b"abc", expected_size=4, expected_git_sha1=git_blob_sha1(b"abc"))

    def test_verify_blob_rejects_wrong_git_sha(self):
        with self.assertRaisesRegex(RuntimeError, "Git blob SHA-1 mismatch"):
            verify_blob(b"abc", expected_size=3, expected_git_sha1="0" * 40)


if __name__ == "__main__":
    unittest.main()
