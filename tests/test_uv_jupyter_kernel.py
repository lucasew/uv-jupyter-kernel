import unittest
from unittest.mock import patch
import sys
from pathlib import Path
import os
import argparse
import json

# Add root to sys.path to allow import
sys.path.append(os.getcwd())

import uv_jupyter_kernel


class TestUvJupyterKernel(unittest.TestCase):
    """
    Test suite for the uv-jupyter-kernel script.

    Validates the creation of kernel configuration, determination of correct
    kernel directories per platform, and the core validation logic for versions
    which prevents path traversal attacks.
    """

    def test_create_kernel_config(self):
        """
        Verifies the structure of the generated kernel configuration.

        Why: Ensures the crucial kernel.json dictionary conforms to Jupyter's
        expected spec, placing 'uv' in the environment PATH and explicitly
        running the ipykernel via 'uv run'.
        """
        config = uv_jupyter_kernel.create_kernel_config("mock/uv/bin", "3.12")
        self.assertEqual(config["display_name"], "uv-3.12")
        self.assertIn("mock/uv/bin", config["argv"])
        self.assertIn("3.12", config["argv"])
        self.assertEqual(config["language"], "python")

    @patch("sys.platform", "darwin")
    def test_get_kernel_dir_mac(self):
        """
        Verifies the kernel directory resolution on macOS.

        Nuance: macOS stores user kernels in ~/Library/Jupyter/kernels instead
        of the standard XDG path used by Linux.
        """
        expected = Path.home() / "Library" / "Jupyter" / "kernels"
        self.assertEqual(uv_jupyter_kernel.get_kernel_dir(), expected)

    @patch("sys.platform", "linux")
    def test_get_kernel_dir_linux(self):
        """
        Verifies the kernel directory resolution on Linux and other platforms.

        Why: Ensures non-macOS platforms fallback to the standard XDG data home
        for user-level Jupyter kernels.
        """
        expected = Path.home() / ".local" / "share" / "jupyter" / "kernels"
        self.assertEqual(uv_jupyter_kernel.get_kernel_dir(), expected)

    def test_validate_version_valid(self):
        """
        Verifies that benign version strings pass validation unmodified.

        Why: We need to allow standard semver and typical suffix variants (like
        rc.1, +build) without rejecting valid user input.
        """
        self.assertEqual(uv_jupyter_kernel.validate_version("3.12"), "3.12")
        self.assertEqual(uv_jupyter_kernel.validate_version("3.12.1"), "3.12.1")
        self.assertEqual(uv_jupyter_kernel.validate_version("env-name"), "env-name")

    def test_validate_version_invalid(self):
        """
        Verifies that potentially malicious version strings are rejected.

        Security: This is a critical check to prevent path traversal
        vulnerabilities, as the version string is directly concatenated into
        file paths when writing the kernel.json file. Input containing slashes
        or relative path components must trigger an ArgumentTypeError.
        """
        with self.assertRaises(argparse.ArgumentTypeError):
            uv_jupyter_kernel.validate_version("../etc/passwd")
        with self.assertRaises(argparse.ArgumentTypeError):
            uv_jupyter_kernel.validate_version("foo/bar")

    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.write_text")
    def test_install_kernel(self, mock_write, mock_mkdir):
        """
        Verifies the end-to-end installation side-effects.

        Why: Ensures the necessary directory structure is created safely
        (parents=True, exist_ok=True) and that the kernel config is correctly
        serialized and written to the kernel.json file within that directory.
        """
        kernel_base = Path("mock/tmp/kernels")
        uv_path = "mock/uv/bin"
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
