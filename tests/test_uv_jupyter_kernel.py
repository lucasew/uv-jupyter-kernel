import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
import os
import argparse
import json

# Add root to sys.path to allow import
sys.path.append(os.getcwd())

import uv_jupyter_kernel

class TestUvJupyterKernel(unittest.TestCase):
    def test_create_kernel_config(self):
        config = uv_jupyter_kernel.create_kernel_config("/usr/bin/uv", "3.12")
        self.assertEqual(config["display_name"], "uv-3.12")
        self.assertIn("/usr/bin/uv", config["argv"])
        self.assertIn("3.12", config["argv"])
        self.assertEqual(config["language"], "python")

    @patch("sys.platform", "darwin")
    def test_get_kernel_dir_mac(self):
        expected = Path.home() / "Library" / "Jupyter" / "kernels"
        self.assertEqual(uv_jupyter_kernel.get_kernel_dir(), expected)

    @patch("sys.platform", "linux")
    def test_get_kernel_dir_linux(self):
        expected = Path.home() / ".local" / "share" / "jupyter" / "kernels"
        self.assertEqual(uv_jupyter_kernel.get_kernel_dir(), expected)

    def test_validate_version_valid(self):
        self.assertEqual(uv_jupyter_kernel.validate_version("3.12"), "3.12")
        self.assertEqual(uv_jupyter_kernel.validate_version("3.12.1"), "3.12.1")
        self.assertEqual(uv_jupyter_kernel.validate_version("env-name"), "env-name")

    def test_validate_version_invalid(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            uv_jupyter_kernel.validate_version("../etc/passwd")
        with self.assertRaises(argparse.ArgumentTypeError):
            uv_jupyter_kernel.validate_version("foo/bar")

    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.write_text")
    def test_install_kernel(self, mock_write, mock_mkdir):
        kernel_base = Path("/tmp/kernels")
        uv_path = "/usr/bin/uv"
        version = "3.12"

        result = uv_jupyter_kernel.install_kernel(uv_path, version, kernel_base)

        expected_path = kernel_base / "uv-3.12" / "kernel.json"
        self.assertEqual(result, expected_path)
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_write.assert_called_once()
        # Verify content
        args, _ = mock_write.call_args
        content = json.loads(args[0])
        self.assertEqual(content["display_name"], "uv-3.12")

if __name__ == "__main__":
    unittest.main()
