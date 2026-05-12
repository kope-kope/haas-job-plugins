#!/usr/bin/env python3
"""
Universal cross-platform dispatcher for the get-me-a-job plugin's Python helpers.

Usage:
    python run.py <script_name> [args...]

Examples:
    python run.py google_auth
    python run.py gdocs copy DOC_ID "New title" FOLDER_ID
    python run.py gmail send to@example.com "Subject" @body.txt

Picks the best available install method in this order:
  1. uv (if installed) — uses PEP 723 inline deps from each script. Zero install.
  2. Existing pip install — if deps are already importable, just runs.
  3. Auto pip install — installs requirements.txt once, then runs.

Works the same on macOS, Linux, and Windows.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parent
REPO_ROOT = LIB.parent
REQUIREMENTS = REPO_ROOT / "requirements.txt"

REQUIRED_IMPORTS = (
    "google_auth_oauthlib",
    "googleapiclient",
    "requests",
)


def have_uv() -> bool:
    return shutil.which("uv") is not None


def deps_importable() -> bool:
    for mod in REQUIRED_IMPORTS:
        try:
            __import__(mod)
        except ImportError:
            return False
    return True


def pip_install():
    print("Installing Python dependencies (one-time)...", file=sys.stderr)
    cmd = [sys.executable, "-m", "pip", "install", "-q", "-r", str(REQUIREMENTS)]
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(
            f"\nDependency install failed (exit {e.returncode}).\n"
            f"Try manually: {' '.join(cmd)}",
            file=sys.stderr,
        )
        sys.exit(e.returncode)


def exec_script(python_cmd: list[str], script: Path, args: list[str]):
    full = [*python_cmd, str(script), *args]
    if os.name == "nt":
        # execvp on Windows can lose signals; subprocess gives clean exit code.
        sys.exit(subprocess.call(full))
    else:
        os.execvp(full[0], full)


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    name = sys.argv[1]
    args = sys.argv[2:]
    script = LIB / f"{name}.py"

    if not script.exists():
        print(f"No such script: lib/{name}.py", file=sys.stderr)
        sys.exit(1)

    if have_uv():
        exec_script(["uv", "run", "--quiet"], script, args)
    elif deps_importable():
        exec_script([sys.executable], script, args)
    else:
        pip_install()
        exec_script([sys.executable], script, args)


if __name__ == "__main__":
    main()
