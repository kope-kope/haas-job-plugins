#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Print a copy-paste command the user can run in their own terminal to do
the one-time Google OAuth.

Why this exists:
  Cowork installs each plugin into a per-session directory like
  `Application Support/Claude/local-agent-mode-sessions/<uuid>/<uuid>/rpm/
  plugin_<hash>/` — the path is unguessable. The agent in Cowork's chat
  knows the path (via $CLAUDE_PLUGIN_ROOT) but tends to substitute a
  conventional guess like `~/.claude/plugins/...` when telling the user
  what to type. This script bypasses the agent's guesswork: it resolves
  the path from Python (where __file__ never lies) and prints the literal
  command for the agent to relay verbatim.

Usage from the /setup skill:
  python3 "$CLAUDE_PLUGIN_ROOT/lib/print_setup_cmd.py"

The single line of stdout is the exact command the user should paste into
Terminal. The agent should show it verbatim — no modifications, no
"something like", no path substitutions.

Also tries to copy the command to the system clipboard (pbcopy on macOS,
xclip / xsel / wl-copy on Linux, clip.exe on Windows / WSL). Silent if
no clipboard tool is available.
"""

import shutil
import subprocess
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
AUTH_SH = PLUGIN_ROOT / "auth.sh"


def copy_to_clipboard(text: str) -> bool:
    candidates = [
        ("pbcopy", []),
        ("wl-copy", []),
        ("xclip", ["-selection", "clipboard"]),
        ("xsel", ["--clipboard", "--input"]),
        ("clip.exe", []),
    ]
    for binary, args in candidates:
        if shutil.which(binary):
            try:
                subprocess.run(
                    [binary, *args],
                    input=text.encode(),
                    check=True,
                    timeout=3,
                )
                return True
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                continue
    return False


def main():
    if not AUTH_SH.exists():
        print(f"ERROR: auth.sh missing from plugin install at {AUTH_SH}", file=sys.stderr)
        sys.exit(1)

    # Quote single quotes for bash safety even though plugin paths shouldn't contain them
    safe_path = str(AUTH_SH).replace("'", "'\\''")
    cmd = f"bash '{safe_path}'"

    clipboard_ok = copy_to_clipboard(cmd)

    print(cmd)
    if clipboard_ok:
        print("(copied to clipboard)", file=sys.stderr)


if __name__ == "__main__":
    main()
