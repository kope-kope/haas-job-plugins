# Security model

## The OAuth credential in `lib/credentials.b64`

`lib/credentials.b64` is the base64-encoded OAuth "installed app" client
configuration for the Google Cloud project that powers this plugin. It looks
like a secret. It mostly isn't. Here's why.

### What the file contains

A `client_id` and `client_secret` for an OAuth 2.0 "Desktop app" credential.
Per [Google's own documentation][gcp-oauth]:

> The process results in a client ID and, in some cases, a client secret,
> which you embed in the source code of your application. (In this context,
> the client secret is obviously not treated as a secret.)

This is standard practice for desktop OAuth apps. `gcloud`, `rclone`,
`google-drive-ocamlfuse`, the `gh` CLI, and dozens of others all ship
embedded client credentials.

### Why it's safe to distribute

The GCP project is configured as an **Internal** OAuth app inside the
Berkeley Google Workspace. Google enforces two things at the auth flow:

1. Only accounts within `berkeley.edu` can complete the OAuth handshake.
   A non-Berkeley user who grabs this file and tries to authenticate gets
   "Access blocked: this app is restricted to users within its organization."
2. The redirect URI is `http://localhost`. Even a malicious actor with the
   credential can't intercept tokens remotely — Google sends them to
   `localhost` on the victim's machine, which is only reachable if the
   attacker is already running code there.

The plugin additionally enforces an `@berkeley.edu` email-domain check in
`lib/google_auth.py` after the OAuth flow completes, as defense in depth.

### Why it's base64-encoded rather than committed as raw JSON

GitHub's secret scanner partners with Google's credential scanner. Both
trigger on the literal `client_secret.json` shape and email the project
owner with "your credential is leaked" warnings — even though, for
installed-app credentials, the leak is by design. Encoding to base64
sidesteps the false-positive scanner pipeline without changing the
underlying threat model.

`.gitignore` blocks `lib/client_secret.json` to prevent accidentally
committing the raw form during local testing.

[gcp-oauth]: https://developers.google.com/identity/protocols/oauth2

## What's actually sensitive

The user's own OAuth tokens — saved to
`~/.claude/get-me-a-job/credentials.json` after they sign in — *are* secret.
That file:

- Lives in the user's home directory, never inside the repo.
- Is generated locally during `/setup` and never leaves the user's machine.
- Can be revoked at any time from <https://myaccount.google.com/permissions>.

## Reporting

If you spot something that looks like a real vulnerability — a way to read
user tokens, exfiltrate Drive or Gmail content, or escalate from the
plugin's scopes — please email Tosin (`tosin.oladokun@berkeley.edu`) with
details before opening a public issue.
