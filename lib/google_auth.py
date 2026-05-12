#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "google-auth-oauthlib",
#   "google-auth-httplib2",
#   "google-api-python-client",
#   "requests",
# ]
# ///
"""
One-time Google OAuth setup for get-me-a-job plugin.

Run this once before using /setup. It opens your browser, you sign in with
your @berkeley.edu account, and your credentials are saved locally.

Usage:
  python lib/run.py google_auth
  # or directly with uv: uv run lib/google_auth.py
"""

import json
import sys
from pathlib import Path

import common

SCRIPT_DIR = Path(__file__).parent
CLIENT_SECRET_FILE = SCRIPT_DIR / "client_secret.json"

# Scopes needed for Google Docs, Drive, and Gmail operations
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/userinfo.email",
]

ALLOWED_EMAIL_DOMAINS = ("berkeley.edu",)


def main():
    if not CLIENT_SECRET_FILE.exists():
        print("Error: client_secret.json not found in lib/.")
        print("This file should ship with the plugin. Contact the plugin maintainer.")
        sys.exit(1)

    if common.CREDS_FILE.exists():
        print(f"Credentials already exist at {common.CREDS_FILE}")
        response = input("Overwrite? (y/N): ").strip().lower()
        if response != "y":
            print("Keeping existing credentials. Run 'python lib/run.py gdocs auth' to test them.")
            return

    from google_auth_oauthlib.flow import InstalledAppFlow
    import requests

    print("Opening browser for Google sign-in...")
    print("Sign in with your @berkeley.edu account.\n")

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRET_FILE),
        scopes=SCOPES,
    )
    creds = flow.run_local_server(port=0)

    r = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {creds.token}"},
    )
    email = r.json().get("email", "")

    if not any(email.lower().endswith("@" + d) for d in ALLOWED_EMAIL_DOMAINS):
        print(
            f"\nThis plugin is restricted to {', '.join(ALLOWED_EMAIL_DOMAINS)} accounts.\n"
            f"You signed in as: {email or '(unknown)'}\n"
            f"Re-run and choose your @berkeley.edu account."
        )
        sys.exit(2)

    with open(CLIENT_SECRET_FILE) as f:
        client_data = json.load(f)
    app_config = client_data.get("installed", client_data.get("web", {}))

    common.save_creds_data({
        "client_id": app_config["client_id"],
        "client_secret": app_config["client_secret"],
        "refresh_token": creds.refresh_token,
        "token_uri": "https://oauth2.googleapis.com/token",
        "scopes": SCOPES,
        "email": email,
    })

    print(f"\nAuthenticated as: {email}")
    print(f"Credentials saved to: {common.CREDS_FILE}")
    print("\nYou're all set. Open Cowork and run /setup to get started.")


if __name__ == "__main__":
    main()
