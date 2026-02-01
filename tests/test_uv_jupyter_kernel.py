import unittest
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from uv_jupyter_kernel import create_kernel_config
except ImportError:
    # If not found, try adding CWD explicitly if running from inside tests/
    sys.path.append(str(Path.cwd()))
    from uv_jupyter_kernel import create_kernel_config


class TestUvJupyterKernel(unittest.TestCase):
    def test_create_kernel_config(self):
        uv_path = "/usr/bin/uv"
        version = "3.12"
        config = create_kernel_config(uv_path, version)

        self.assertEqual(config["display_name"], "uv-3.12")
        self.assertEqual(config["language"], "python")
        # Check argv structure
        self.assertEqual(config["argv"][0], uv_path)
        self.assertEqual(config["argv"][1], "run")
        self.assertIn(version, config["argv"])
        self.assertIn("--isolated", config["argv"])
        self.assertIn("ipykernel", config["argv"])


if __name__ == "__main__":
    unittest.main()
