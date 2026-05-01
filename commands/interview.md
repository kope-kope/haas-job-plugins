---
description: Prep for an upcoming interview
argument-hint: [company name and/or role]
---

Use the interview-prep skill to prepare the user for an interview at: $ARGUMENTS

If no company or role was specified, ask which company and role, and what stage of the interview (recruiter screen, hiring manager, panel, etc.).

Then:
1. Research the company (recent news, product, culture, interview format)
2. Generate 15-20 tailored interview questions with story guidance
3. Help craft the user's "tell me about yourself" for this specific role
4. Produce a dos and don'ts list for this company and role type

Always read `${CLAUDE_PLUGIN_ROOT}/skills/interview-prep/references/stories.md` first. If the file is missing or empty, offer to help the user build their stories now or tell them to run `/setup` to create them.
