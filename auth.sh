#!/usr/bin/env bash
# One-shot Google OAuth for the get-me-a-job plugin.
#
# Cowork's tool sandbox can't open your local browser, so the OAuth flow
# has to happen in your real terminal — once. This script runs that flow.
# It's safe to re-run; it'll prompt before overwriting existing credentials.
#
# Usage (paste into Terminal / iTerm / your shell of choice):
#   bash <full-path-to-this-script>
#
# The /setup command in Cowork will print the full path for you.

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is not on your PATH."
  echo "Install Python 3.10+ from https://www.python.org/downloads/ and re-run."
  exit 1
fi

exec python3 "$SCRIPT_DIR/lib/run.py" google_auth "$@"
