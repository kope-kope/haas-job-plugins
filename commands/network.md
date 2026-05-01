---
description: Find contacts and draft outreach for a target company
argument-hint: [company name or person to reach out to]
---

Use the network-outreach skill to help the user reach out to contacts at: $ARGUMENTS

If no target was specified, ask which company or person they want to connect with.

Then:
1. Identify the best path to the target (warm intro, alumni, cold outreach)
2. Use Hunter tools to find email/contact info if available
3. Draft a personalized outreach message (LinkedIn or email)
4. Show the draft to the user for approval before any sending
5. Suggest follow-up strategy

Always read `${CLAUDE_PLUGIN_ROOT}/skills/network-outreach/references/network-context.md` and `${CLAUDE_PLUGIN_ROOT}/skills/network-outreach/references/outreach-style-guide.md` first. If these files are missing or empty, tell the user to run `/setup` first.

**CRITICAL: Never send any email without showing the user the full draft first and getting their explicit approval.**
