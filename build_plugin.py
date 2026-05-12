#!/usr/bin/env python3
"""Build get-me-a-job.plugin (zip) from the current repo for Cowork distribution.

Run: python3 build_plugin.py
Output: get-me-a-job.plugin in the repo root.

The .plugin file is what Cowork users upload via the plugin browser. It
should NOT be committed to the repo — attach it to a GitHub release instead.
"""

import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent
OUTPUT = REPO / "get-me-a-job.plugin"

EXCLUDE_DIR_NAMES = {".git", "__pycache__", ".venv", ".credentials"}
EXCLUDE_EXTS = {".pyc", ".pyo"}
EXCLUDE_FILES = {".DS_Store", "get-me-a-job.plugin", "build_plugin.py"}


def should_skip(path: Path) -> bool:
    if path.name in EXCLUDE_FILES:
        return True
    if path.suffix in EXCLUDE_EXTS:
        return True
    if any(part in EXCLUDE_DIR_NAMES for part in path.parts):
        return True
    return False


def main():
    if OUTPUT.exists():
        OUTPUT.unlink()

    count = 0
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(REPO.rglob("*")):
            if path.is_dir() or should_skip(path):
                continue
            arcname = path.relative_to(REPO)
            z.write(path, arcname)
            count += 1

    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Wrote {OUTPUT.name} ({size_kb:.1f} KB, {count} files)")


if __name__ == "__main__":
    main()
