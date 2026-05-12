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

SCRIPT_DIR = Path(__file__).parent
CLIENT_SECRET_FILE = SCRIPT_DIR / "client_secret.json"
CREDS_DIR = SCRIPT_DIR / ".credentials"
CREDS_FILE = CREDS_DIR / "google_credentials.json"

# Scopes needed for Google Docs, Drive, and Sheets operations
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/userinfo.email",
]


def main():
    if not CLIENT_SECRET_FILE.exists():
        print("Error: client_secret.json not found.")
        print("This file should ship with the plugin. Contact the plugin maintainer.")
        sys.exit(1)

    if CREDS_FILE.exists():
        print(f"Credentials already exist at {CREDS_FILE}")
        response = input("Overwrite? (y/N): ").strip().lower()
        if response != "y":
            print("Keeping existing credentials. Run 'python gdocs.py auth' to test them.")
            return

    from google_auth_oauthlib.flow import InstalledAppFlow

    print("Opening browser for Google sign-in...")
    print("Sign in with your @berkeley.edu account.\n")

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRET_FILE),
        scopes=SCOPES,
    )
    creds = flow.run_local_server(port=0)

    # Get the user's email to confirm which account was used
    import requests
    r = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {creds.token}"},
    )
    email = r.json().get("email", "unknown")

    # Read client_id and client_secret from the client_secret file
    with open(CLIENT_SECRET_FILE) as f:
        client_data = json.load(f)
    # Handle both "installed" and "web" key formats
    app_config = client_data.get("installed", client_data.get("web", {}))

    # Save credentials
    CREDS_DIR.mkdir(exist_ok=True)
    creds_data = {
        "client_id": app_config["client_id"],
        "client_secret": app_config["client_secret"],
        "refresh_token": creds.refresh_token,
        "token_uri": "https://oauth2.googleapis.com/token",
        "scopes": SCOPES,
    }
    with open(CREDS_FILE, "w") as f:
        json.dump(creds_data, f, indent=2)

    print(f"\nAuthenticated as: {email}")
    print(f"Credentials saved to: {CREDS_FILE}")
    print("\nYou're all set. Open Cowork and run /setup to get started.")


if __name__ == "__main__":
    main()
