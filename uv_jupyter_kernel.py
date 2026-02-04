#!/usr/bin/env python3

import argparse
import os
import json
import re
import shutil
from pathlib import Path
import sys
from typing import Dict, Any


def validate_version(version: str) -> str:
    """
    Validates the version string to prevent path traversal attacks.

    Ensures that the version string contains only alphanumeric characters,
    dots, underscores, plus signs, or hyphens. This is crucial for security
    as this input is used in file paths.

    Args:
        version: The version string to validate.

    Returns:
        The validated version string.

    Raises:
        argparse.ArgumentTypeError: If the version string contains invalid characters.
    """
    if not re.match(r"^[a-zA-Z0-9._+-]+$", version):
        raise argparse.ArgumentTypeError(f"Invalid version: {version}")
    return version


def get_uv_path() -> str:
    """
    Locates the 'uv' executable in the system PATH.

    This function checks if 'uv' is available. If not found, it prints an
    error message to stderr and exits the program, as 'uv' is a core
    requirement for this tool.

    Returns:
        The absolute path to the 'uv' executable.
    """
    uv = shutil.which("uv")
    if uv is None:
        print("Error: 'uv' not found in PATH.", file=sys.stderr)
        sys.exit(1)
    return uv


def get_kernel_dir() -> Path:
    """
    Determines the appropriate Jupyter kernel directory for the user.

    The location varies by operating system:
    - macOS: ~/Library/Jupyter/kernels
    - Linux/Other: ~/.local/share/jupyter/kernels

    Returns:
        A Path object representing the user's Jupyter kernel directory.
    """
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Jupyter" / "kernels"
    return Path.home() / ".local" / "share" / "jupyter" / "kernels"


def create_kernel_config(uv_path: str, version: str) -> Dict[str, Any]:
    """
    Generates the configuration dictionary for the Jupyter kernel.

    This function constructs the kernel spec that Jupyter will use to launch
    the kernel. Key aspects include:
    - Adding the 'uv' directory to PATH.
    - Using 'uv run' to execute the kernel in an isolated environment.
    - Specifying '--no-project' to avoid looking for a project file.
    - Setting up debug support.

    Args:
        uv_path: The path to the 'uv' executable.
        version: The Python version for the kernel.

    Returns:
        A dictionary containing the kernel configuration (kernel.json structure).
    """
    uv_dir = str(Path(uv_path).parent)
    return {
        "env": {"PATH": os.pathsep.join(["${PATH}", uv_dir])},
        "argv": [
            uv_path,
            "run",
            "--python",
            version,
            "--with",
            "ipykernel",
            "--with",
            "pyzmq",
            "--no-project",
            "--isolated",
            "--refresh",
            "python",
            "-m",
            "ipykernel_launcher",
            "-f",
            "{connection_file}",
        ],
        "display_name": f"uv-{version}",
        "language": "python",
        "metadata": {"debugger": True},
    }


DEFAULT_VERSIONS = ["3.13", "3.12"]


def install_kernel(uv_path: str, version: str, kernel_base: Path) -> Path:
    """
    Installs a Jupyter kernel for a specific Python version using 'uv'.

    This function creates the kernel directory and writes the 'kernel.json'
    file. It ensures the directory exists and handles the file I/O.

    Args:
        uv_path: The path to the 'uv' executable.
        version: The Python version to install.
        kernel_base: The base directory for Jupyter kernels.

    Returns:
        The path to the created 'kernel.json' file.
    """
    kernel_file = kernel_base / f"uv-{version}" / "kernel.json"
    kernel_file.parent.mkdir(parents=True, exist_ok=True)

    kernel_config = create_kernel_config(uv_path, version)

    kernel_file.write_text(
        json.dumps(kernel_config, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return kernel_file


def main() -> None:
    """
    Main entry point for the script.

    Parses command-line arguments to get the requested Python versions,
    locates 'uv', determines the kernel directory, and installs the
    kernels for each requested version.
    """
    parser = argparse.ArgumentParser(description="Setup Jupyter kernels for uv")
    parser.add_argument(
        "--versions",
        nargs="+",
        default=DEFAULT_VERSIONS,
        type=validate_version,
        help=f"Python versions to configure (default: {' '.join(DEFAULT_VERSIONS)})",
    )

    args = parser.parse_args()

    uv_path = get_uv_path()
    kernel_base = get_kernel_dir()

    for version in args.versions:
        kernel_file = install_kernel(uv_path, version, kernel_base)
        print(f"Kernel configured for Python {version} at: {kernel_file}")


if __name__ == "__main__":
    main()
