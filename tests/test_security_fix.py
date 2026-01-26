import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import uv_jupyter_kernel

class TestSecurityFix(unittest.TestCase):
    @patch("uv_jupyter_kernel.shutil.which")
    @patch("uv_jupyter_kernel.Path") # Patch Path to prevent real FS ops
    def test_malicious_input_rejected(self, mock_path_cls, mock_which):
        # Setup
        mock_which.return_value = "/fake/uv"

        # Mock Path instances
        mock_path_instance = MagicMock()
        mock_path_cls.return_value = mock_path_instance
        mock_path_cls.home.return_value = mock_path_instance
        # Allow division operator for Path (path / "str")
        mock_path_instance.__truediv__.return_value = mock_path_instance

        # Capture stderr
        captured_stderr = StringIO()
        with patch("sys.stderr", captured_stderr):
            with patch("sys.argv", ["script", "--versions", "../../../etc/passwd"]):
                uv_jupyter_kernel.main()

        output = captured_stderr.getvalue()
        self.assertIn("Error: Invalid version string", output)
        self.assertIn("../../../etc/passwd", output)

    @patch("uv_jupyter_kernel.shutil.which")
    @patch("uv_jupyter_kernel.Path")
    @patch("uv_jupyter_kernel.create_kernel_config")
    def test_valid_input_accepted(self, mock_create_config, mock_path_cls, mock_which):
        # Setup
        mock_which.return_value = "/fake/uv"
        mock_path_instance = MagicMock()
        mock_path_cls.return_value = mock_path_instance
        mock_path_cls.home.return_value = mock_path_instance
        mock_path_instance.__truediv__.return_value = mock_path_instance

        # Mock create_kernel_config to avoid real logic if needed,
        # but pure logic is fine if we mock Path
        mock_create_config.return_value = {}

        captured_stderr = StringIO()
        with patch("sys.stderr", captured_stderr):
            with patch("sys.argv", ["script", "--versions", "3.13"]):
                uv_jupyter_kernel.main()

        # Should NOT print error
        output = captured_stderr.getvalue()
        self.assertNotIn("Error: Invalid version string", output)

        # Verify write_text was called (simulating success)
        # kernel_file.write_text(...)
        # mock_path_instance is returned by div, so checking if write_text was called on it
        self.assertTrue(mock_path_instance.write_text.called)

if __name__ == "__main__":
    unittest.main()
