---
description: Tailor your resume to a job description
argument-hint: [paste job description or leave empty to be prompted]
---

Use the resume-tailor skill to tailor the user's resume to this job description:

$ARGUMENTS

If no job description was provided, ask the user to paste it now. Once you have it:
1. Deconstruct the JD (requirements, keywords, culture signals)
2. Map the user's experience to the JD
3. Rewrite bullets using the what/how/result/why framework
4. Produce a tailored resume as a Word document saved to the workspace
5. If Google Drive is configured in `~/.claude/get-me-a-job/config.json` (look for `master_resume_doc_id` and `job_search_folder_id`), also copy the master resume template and replace content
6. Write a gap report in the chat

Always read `~/.claude/get-me-a-job/references/resume.md` first. If the file is missing or empty, tell the user to run `/setup` first.
