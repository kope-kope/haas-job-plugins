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
Google Docs / Drive helper.

Run via the dispatcher (recommended):
  python lib/run.py gdocs <command> [args...]

Or directly with uv:
  uv run lib/gdocs.py <command> [args...]

Commands:
  auth
  create "Doc Title" [FOLDER_ID]
  copy SOURCE_DOC_ID "New Title" [FOLDER_ID]
  read DOC_ID
  write DOC_ID "Text to append"
  write DOC_ID @/path/to/file.txt
  replace DOC_ID "old text" "new text"
  clear DOC_ID
  move DOC_ID FOLDER_ID
  create-folder "Folder Name"
  upload /path/to/file.docx [FOLDER_ID]
"""

import sys
import json
import os
from pathlib import Path

# Locate credentials relative to this script
SCRIPT_DIR = Path(__file__).parent
CREDS_FILE = SCRIPT_DIR / ".credentials" / "google_credentials.json"

def get_access_token():
    """Get a fresh access token using curl (forces IPv4, avoids httplib2 IPv6 issue)."""
    import subprocess
    with open(CREDS_FILE) as f:
        creds_data = json.load(f)
    result = subprocess.run([
        'curl', '-4', '-s', '-X', 'POST', 'https://oauth2.googleapis.com/token',
        '-d', f'client_id={creds_data["client_id"]}&client_secret={creds_data["client_secret"]}&refresh_token={creds_data["refresh_token"]}&grant_type=refresh_token'
    ], capture_output=True, text=True, timeout=15)
    data = json.loads(result.stdout)
    return data['access_token']


def get_service(api, version):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    with open(CREDS_FILE) as f:
        creds_data = json.load(f)

    # Use curl-based token refresh to avoid httplib2 IPv6 timeout issue
    access_token = get_access_token()
    creds = Credentials(
        token=access_token,
        refresh_token=creds_data["refresh_token"],
        client_id=creds_data["client_id"],
        client_secret=creds_data["client_secret"],
        token_uri=creds_data["token_uri"],
        scopes=creds_data["scopes"]
    )
    return build(api, version, credentials=creds)


def cmd_auth():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    import requests as req

    with open(CREDS_FILE) as f:
        creds_data = json.load(f)

    creds = Credentials(
        token=None,
        refresh_token=creds_data["refresh_token"],
        client_id=creds_data["client_id"],
        client_secret=creds_data["client_secret"],
        token_uri=creds_data["token_uri"],
        scopes=creds_data["scopes"]
    )
    creds.refresh(Request())

    # Get email
    r = req.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {creds.token}"}
    )
    email = r.json().get("email", "unknown")
    print(json.dumps({"status": "authenticated", "email": email, "token_ok": True}))


def cmd_move(doc_id, folder_id):
    """Move a file into a Drive folder."""
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    with open(CREDS_FILE) as f:
        creds_data = json.load(f)

    creds = Credentials(
        token=None,
        refresh_token=creds_data["refresh_token"],
        client_id=creds_data["client_id"],
        client_secret=creds_data["client_secret"],
        token_uri=creds_data["token_uri"],
        scopes=creds_data["scopes"]
    )
    drive = build("drive", "v3", credentials=creds)

    # Get current parents
    file_meta = drive.files().get(fileId=doc_id, fields="parents").execute()
    current_parents = ",".join(file_meta.get("parents", []))

    # Move to new folder
    drive.files().update(
        fileId=doc_id,
        addParents=folder_id,
        removeParents=current_parents,
        fields="id, parents"
    ).execute()

    url = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(json.dumps({"status": "moved", "doc_id": doc_id, "folder_id": folder_id, "url": url}))


def cmd_copy(source_doc_id, title, folder_id=None):
    """Copy an existing Google Doc (preserves all formatting)."""
    drive = get_service("drive", "v3")
    body = {"name": title}
    if folder_id:
        body["parents"] = [folder_id]
    copied = drive.files().copy(fileId=source_doc_id, body=body).execute()
    new_id = copied["id"]
    url = f"https://docs.google.com/document/d/{new_id}/edit"
    print(json.dumps({"doc_id": new_id, "url": url, "title": title, "source": source_doc_id}))


def cmd_create(title, folder_id=None):
    service = get_service("docs", "v1")
    doc = service.documents().create(body={"title": title}).execute()
    doc_id = doc["documentId"]
    url = f"https://docs.google.com/document/d/{doc_id}/edit"
    if folder_id:
        cmd_move(doc_id, folder_id)
    print(json.dumps({"doc_id": doc_id, "url": url, "title": title}))


def cmd_create_folder(name):
    """Create a folder in Google Drive."""
    drive = get_service("drive", "v3")
    body = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    folder = drive.files().create(body=body, fields="id").execute()
    folder_id = folder["id"]
    url = f"https://drive.google.com/drive/folders/{folder_id}"
    print(json.dumps({"folder_id": folder_id, "url": url, "name": name}))


def cmd_upload(file_path, folder_id=None):
    """Upload a file to Google Drive (e.g. .docx resume template)."""
    from googleapiclient.http import MediaFileUpload
    drive = get_service("drive", "v3")

    file_name = Path(file_path).name
    body = {"name": file_name}
    if folder_id:
        body["parents"] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)
    uploaded = drive.files().create(body=body, media_body=media, fields="id").execute()
    file_id = uploaded["id"]

    # If it's a .docx, get the Google Docs URL (Drive auto-converts)
    if file_name.endswith(".docx"):
        url = f"https://docs.google.com/document/d/{file_id}/edit"
    else:
        url = f"https://drive.google.com/file/d/{file_id}/view"

    print(json.dumps({"file_id": file_id, "url": url, "name": file_name}))


def cmd_read(doc_id):
    service = get_service("docs", "v1")
    doc = service.documents().get(documentId=doc_id).execute()
    content = doc.get("body", {}).get("content", [])
    text_parts = []
    for block in content:
        para = block.get("paragraph")
        if para:
            for elem in para.get("elements", []):
                tr = elem.get("textRun")
                if tr:
                    text_parts.append(tr.get("content", ""))
    full_text = "".join(text_parts)
    print(json.dumps({"doc_id": doc_id, "title": doc.get("title", ""), "text": full_text}))


def cmd_write(doc_id, text):
    """Append text to end of doc."""
    service = get_service("docs", "v1")

    # Load file content if text starts with @
    if text.startswith("@"):
        filepath = text[1:]
        with open(filepath) as f:
            text = f.read()

    # Get current end index
    doc = service.documents().get(documentId=doc_id).execute()
    content = doc.get("body", {}).get("content", [])
    end_index = content[-1].get("endIndex", 1) - 1 if content else 1

    requests = [
        {
            "insertText": {
                "location": {"index": end_index},
                "text": text
            }
        }
    ]
    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": requests}
    ).execute()
    print(json.dumps({"status": "written", "doc_id": doc_id, "chars_written": len(text)}))


def cmd_replace(doc_id, old_text, new_text):
    service = get_service("docs", "v1")
    requests = [
        {
            "replaceAllText": {
                "containsText": {"text": old_text, "matchCase": True},
                "replaceText": new_text
            }
        }
    ]
    result = service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": requests}
    ).execute()
    print(json.dumps({"status": "replaced", "doc_id": doc_id}))


def cmd_clear(doc_id):
    """Clear all content from a doc."""
    service = get_service("docs", "v1")
    doc = service.documents().get(documentId=doc_id).execute()
    content = doc.get("body", {}).get("content", [])
    end_index = content[-1].get("endIndex", 2) - 1 if content else 2

    if end_index > 1:
        requests = [
            {
                "deleteContentRange": {
                    "range": {"startIndex": 1, "endIndex": end_index}
                }
            }
        ]
        service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": requests}
        ).execute()
    print(json.dumps({"status": "cleared", "doc_id": doc_id}))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "auth":
        cmd_auth()
    elif cmd == "create":
        folder_id = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_create(sys.argv[2], folder_id)
    elif cmd == "copy":
        folder_id = sys.argv[4] if len(sys.argv) > 4 else None
        cmd_copy(sys.argv[2], sys.argv[3], folder_id)
    elif cmd == "move":
        cmd_move(sys.argv[2], sys.argv[3])
    elif cmd == "read":
        cmd_read(sys.argv[2])
    elif cmd == "write":
        cmd_write(sys.argv[2], sys.argv[3])
    elif cmd == "replace":
        cmd_replace(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "clear":
        cmd_clear(sys.argv[2])
    elif cmd == "create-folder":
        cmd_create_folder(sys.argv[2])
    elif cmd == "upload":
        folder_id = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_upload(sys.argv[2], folder_id)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
