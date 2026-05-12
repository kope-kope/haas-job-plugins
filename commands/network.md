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
4. Show the draft to the user for approval
5. For email outreach: after the user approves, save it as a Gmail draft so they can review it in their inbox before it goes out:
   ```
   python ${CLAUDE_PLUGIN_ROOT}/lib/run.py gmail draft recipient@company.com "Subject line" @/tmp/outreach-body.txt
   ```
   Send only on explicit "send it" / "yes, send" from the user:
   ```
   python ${CLAUDE_PLUGIN_ROOT}/lib/run.py gmail send recipient@company.com "Subject line" @/tmp/outreach-body.txt
   ```
6. Suggest follow-up strategy

Always read `~/.claude/get-me-a-job/references/network-context.md` and `~/.claude/get-me-a-job/references/outreach-style-guide.md` first. If these files are missing or empty, tell the user to run `/setup` first.

**CRITICAL: Never call `gmail send` (or `gmail reply`) without showing the user the full draft first and getting their explicit approval in chat. "Yes" / "send it" in response to a shown draft is approval; nothing else is.**
