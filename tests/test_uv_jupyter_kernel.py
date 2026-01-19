import unittest
import argparse
import sys
import os

# Add root directory to sys.path to allow importing uv_jupyter_kernel
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from uv_jupyter_kernel import validate_version

class TestUVJupyterKernel(unittest.TestCase):
    def test_validate_version_valid(self):
        valid_versions = ["3.13", "3.12", "3.10.1", "pypy-3.9", "3.13-rc1", "3.13.0a1"]
        for v in valid_versions:
            self.assertEqual(validate_version(v), v)

    def test_validate_version_invalid(self):
        invalid_versions = [
            "3.13/../../../tmp",
            "../etc/passwd",
            "3.13; rm -rf /",
            "foo bar", # space
            "version/with/slashes",
            "back\\slash",
            "foo@bar",
            "$"
        ]
        for v in invalid_versions:
            with self.subTest(version=v):
                with self.assertRaises(argparse.ArgumentTypeError):
                    validate_version(v)

    def test_validate_version_double_dots(self):
        # Specific check for double dots if we want to disallow them explicitly
        # Our regex allows dots, so we manually check "..".
        invalid_double = ["..", "foo..bar", "..."]
        for v in invalid_double:
             with self.subTest(version=v):
                with self.assertRaises(argparse.ArgumentTypeError):
                    validate_version(v)

if __name__ == "__main__":
    unittest.main()
