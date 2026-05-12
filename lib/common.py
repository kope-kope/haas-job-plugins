"""
Shared paths and credential helpers for the get-me-a-job plugin's Python scripts.

All user data — OAuth tokens, plugin config, and parsed reference markdown —
lives under ~/.claude/get-me-a-job/. The plugin source tree under
CLAUDE_PLUGIN_ROOT only contains code; nothing the user edits.

Layout:
  ~/.claude/get-me-a-job/
    credentials.json          OAuth refresh token + client info
    config.json               Drive folder ID, master resume Doc ID, etc.
    references/
      resume.md
      stories.md
      profile.md
      outreach-style-guide.md
      network-context.md
"""

from __future__ import annotations

import json
import os
from pathlib import Path


USER_DIR = Path(os.environ.get("GET_ME_A_JOB_HOME") or (Path.home() / ".claude" / "get-me-a-job"))
CREDS_FILE = USER_DIR / "credentials.json"
CONFIG_FILE = USER_DIR / "config.json"
REFERENCES_DIR = USER_DIR / "references"


def ensure_user_dir() -> None:
    USER_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)


def load_creds_data() -> dict:
    if not CREDS_FILE.exists():
        raise SystemExit(
            f"Not authenticated yet. Run: python lib/run.py google_auth\n"
            f"(Expected credentials at {CREDS_FILE})"
        )
    with open(CREDS_FILE) as f:
        return json.load(f)


def save_creds_data(data: dict) -> None:
    ensure_user_dir()
    with open(CREDS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_config(data: dict) -> None:
    ensure_user_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def update_config(**kwargs) -> dict:
    cfg = load_config()
    cfg.update(kwargs)
    save_config(cfg)
    return cfg
