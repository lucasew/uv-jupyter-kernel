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
    if not re.match(r"^[a-zA-Z0-9._+-]+$", version):
        raise argparse.ArgumentTypeError(f"Invalid version: {version}")
    return version


def get_uv_path() -> str:
    uv = shutil.which("uv")
    if uv is None:
        print("Error: 'uv' not found in PATH.", file=sys.stderr)
        sys.exit(1)
    return uv


def get_kernel_dir() -> Path:
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Jupyter" / "kernels"
    return Path.home() / ".local" / "share" / "jupyter" / "kernels"


def create_kernel_config(uv_path: str, version: str) -> Dict[str, Any]:
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
    kernel_file = kernel_base / f"uv-{version}" / "kernel.json"
    kernel_file.parent.mkdir(parents=True, exist_ok=True)

    kernel_config = create_kernel_config(uv_path, version)

    kernel_file.write_text(
        json.dumps(kernel_config, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return kernel_file


def main() -> None:
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
