#!/usr/bin/env python3

import argparse
import os
import re
import json
import shutil
from pathlib import Path
import sys
from typing import Dict, Any


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Setup Jupyter kernels for uv")
    parser.add_argument(
        "--versions",
        nargs="+",
        default=["3.13", "3.12"],
        help="Python versions to configure (default: 3.13 3.12)",
    )

    args = parser.parse_args()

    uv_path = get_uv_path()
    kernel_base = get_kernel_dir()

    for version in args.versions:
        if not re.match(r"^[a-zA-Z0-9._+-]+$", version):
            print(f"Error: Invalid version string '{version}'. Must contain only alphanumeric characters, dots, underscores, plus, or minus.", file=sys.stderr)
            continue

        kernel_file = kernel_base / f"uv-{version}" / "kernel.json"
        kernel_file.parent.mkdir(parents=True, exist_ok=True)

        kernel_config = create_kernel_config(uv_path, version)

        kernel_file.write_text(
            json.dumps(kernel_config, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        print(f"Kernel configured for Python {version} at: {kernel_file}")


if __name__ == "__main__":
    main()
