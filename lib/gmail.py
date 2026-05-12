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
Gmail helper — draft, send, read, search, label.

Run via the dispatcher (recommended):
  python lib/run.py gmail <command> [args...]

Or directly with uv:
  uv run lib/gmail.py <command> [args...]

Commands:
  draft TO "Subject" "body text"
  draft TO "Subject" @path/to/body.txt
  send TO "Subject" "body text"
  send TO "Subject" @path/to/body.txt
  reply MESSAGE_ID "body text"
  reply MESSAGE_ID @path/to/body.txt
  list-unread [max]
  read MESSAGE_ID
  threads "search query" [max]
  label MESSAGE_ID "Label Name"

NEVER call `send` or `reply` without explicit user approval in the chat —
this is enforced by the skill prompts, not by the script itself.
"""

import base64
import json
import sys
from email.message import EmailMessage
from pathlib import Path

import common
from gdocs import get_service  # share the same token-refresh logic


def _read_body(arg: str) -> str:
    if arg.startswith("@"):
        return Path(arg[1:]).read_text()
    return arg


def _encode_message(msg: EmailMessage) -> str:
    return base64.urlsafe_b64encode(msg.as_bytes()).decode()


def _build_message(to: str, subject: str, body: str, thread_id: str | None = None,
                   in_reply_to: str | None = None) -> dict:
    msg = EmailMessage()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = "me"
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = in_reply_to
    msg.set_content(body)
    payload = {"raw": _encode_message(msg)}
    if thread_id:
        payload["threadId"] = thread_id
    return payload


def cmd_draft(to: str, subject: str, body_arg: str):
    service = get_service("gmail", "v1")
    body = _read_body(body_arg)
    message = _build_message(to, subject, body)
    draft = service.users().drafts().create(
        userId="me", body={"message": message}
    ).execute()
    draft_id = draft["id"]
    url = f"https://mail.google.com/mail/u/0/#drafts?compose={draft_id}"
    print(json.dumps({
        "status": "drafted", "draft_id": draft_id, "to": to,
        "subject": subject, "url": url,
    }))


def cmd_send(to: str, subject: str, body_arg: str):
    service = get_service("gmail", "v1")
    body = _read_body(body_arg)
    message = _build_message(to, subject, body)
    sent = service.users().messages().send(userId="me", body=message).execute()
    msg_id = sent["id"]
    thread_id = sent.get("threadId")
    print(json.dumps({
        "status": "sent", "message_id": msg_id, "thread_id": thread_id,
        "to": to, "subject": subject,
    }))


def cmd_reply(message_id: str, body_arg: str):
    service = get_service("gmail", "v1")
    body = _read_body(body_arg)
    original = service.users().messages().get(
        userId="me", id=message_id, format="metadata",
        metadataHeaders=["From", "Subject", "Message-ID"]
    ).execute()
    headers = {h["name"]: h["value"] for h in original.get("payload", {}).get("headers", [])}
    to = headers.get("From", "")
    subject = headers.get("Subject", "")
    if not subject.lower().startswith("re:"):
        subject = "Re: " + subject
    message = _build_message(
        to, subject, body,
        thread_id=original.get("threadId"),
        in_reply_to=headers.get("Message-ID"),
    )
    sent = service.users().messages().send(userId="me", body=message).execute()
    print(json.dumps({
        "status": "sent", "message_id": sent["id"],
        "thread_id": sent.get("threadId"), "to": to, "subject": subject,
    }))


def cmd_list_unread(max_results: int = 20):
    service = get_service("gmail", "v1")
    result = service.users().messages().list(
        userId="me", q="is:unread", maxResults=max_results
    ).execute()
    out = []
    for item in result.get("messages", []):
        full = service.users().messages().get(
            userId="me", id=item["id"], format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()
        headers = {h["name"]: h["value"] for h in full.get("payload", {}).get("headers", [])}
        out.append({
            "id": item["id"],
            "thread_id": full.get("threadId"),
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "date": headers.get("Date", ""),
            "snippet": full.get("snippet", "")[:140],
        })
    print(json.dumps(out, indent=2))


def _extract_body(payload: dict) -> str:
    if payload.get("mimeType", "").startswith("text/") and payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", "replace")
    for part in payload.get("parts", []) or []:
        text = _extract_body(part)
        if text:
            return text
    return ""


def cmd_read(message_id: str):
    service = get_service("gmail", "v1")
    msg = service.users().messages().get(
        userId="me", id=message_id, format="full"
    ).execute()
    headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
    body = _extract_body(msg.get("payload", {}))
    print(json.dumps({
        "id": msg["id"],
        "thread_id": msg.get("threadId"),
        "from": headers.get("From", ""),
        "to": headers.get("To", ""),
        "subject": headers.get("Subject", ""),
        "date": headers.get("Date", ""),
        "body": body,
    }, indent=2))


def cmd_threads(query: str, max_results: int = 10):
    service = get_service("gmail", "v1")
    result = service.users().threads().list(
        userId="me", q=query, maxResults=max_results
    ).execute()
    out = []
    for t in result.get("threads", []):
        out.append({
            "id": t["id"],
            "snippet": t.get("snippet", "")[:140],
            "history_id": t.get("historyId"),
        })
    print(json.dumps(out, indent=2))


def cmd_label(message_id: str, label_name: str):
    service = get_service("gmail", "v1")
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    label_id = next((l["id"] for l in labels if l["name"] == label_name), None)
    if not label_id:
        created = service.users().labels().create(
            userId="me", body={"name": label_name}
        ).execute()
        label_id = created["id"]
    service.users().messages().modify(
        userId="me", id=message_id, body={"addLabelIds": [label_id]}
    ).execute()
    print(json.dumps({
        "status": "labeled", "message_id": message_id,
        "label": label_name, "label_id": label_id,
    }))


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]

    handlers = {
        "draft": lambda: cmd_draft(args[0], args[1], args[2]),
        "send": lambda: cmd_send(args[0], args[1], args[2]),
        "reply": lambda: cmd_reply(args[0], args[1]),
        "list-unread": lambda: cmd_list_unread(int(args[0]) if args else 20),
        "read": lambda: cmd_read(args[0]),
        "threads": lambda: cmd_threads(args[0], int(args[1]) if len(args) > 1 else 10),
        "label": lambda: cmd_label(args[0], args[1]),
    }
    if cmd not in handlers:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
    try:
        handlers[cmd]()
    except (IndexError, TypeError) as e:
        print(f"Missing or wrong arguments for '{cmd}': {e}\n", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
