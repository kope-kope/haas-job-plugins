---
description: Set up your job search profile — resume, stories, targeting, outreach style, and network
argument-hint: (no arguments needed)
---

# /setup — Job Search Profile Setup

You are running the onboarding wizard for the get-me-a-job plugin. This is a career coaching session disguised as a setup flow. Your job is not just to collect data — it's to help the user build the best possible version of each reference file.

**Tone:** Conversational, warm, and helpful. You're a career coach who also happens to be configuring software. Never sound like a form. Never rush.

**Key rule:** At every step, if the user doesn't have something ready, offer to help them build it. If they want to skip, let them — but tell them what they'll miss and offer to come back later.

---

## Before You Start

Check which reference files already exist under `~/.claude/get-me-a-job/references/`:
- `resume.md`
- `stories.md`
- `profile.md`
- `outreach-style-guide.md`
- `network-context.md`

If some files already exist (from a previous partial setup), tell the user:
"Looks like you've already set up [X, Y]. Want to redo those, or just finish the ones you haven't done yet?"

Track completion as you go. At the end, report which steps are done and which are skipped.

---

## Step 0: Connect Google

**Goal:** Authenticate the user once for Google Drive, Docs, and Gmail. A single consent screen grants all three.

First, check whether credentials already exist:
```
python ${CLAUDE_PLUGIN_ROOT}/lib/run.py gdocs auth
```

If this prints `{"status": "authenticated", "email": "...@berkeley.edu", ...}`, skip the rest of this step and continue to Step 1.

If it returns "Not authenticated yet" or fails, tell the user:

"I need to connect to your Google account so I can save your resume to Drive, produce tailored docs, and send outreach from Gmail. This is a one-time sign-in. I'm opening your browser now — pick your **@berkeley.edu** account and click Allow."

Then run:
```
python ${CLAUDE_PLUGIN_ROOT}/lib/run.py google_auth
```

This opens the user's default browser to Google's sign-in page. After they sign in and click Allow:
- The script saves credentials to `~/.claude/get-me-a-job/credentials.json`
- It prints `Authenticated as: <email>`

**If the user signs in with the wrong account** (not @berkeley.edu), the script exits with a message saying the app is restricted to berkeley.edu. Tell them: "Looks like that was your personal Gmail. Let's try again — pick your @berkeley.edu account this time." Then re-run `google_auth`.

**If the script can't open a browser** (rare — e.g. SSH session), the Google library still prints the auth URL. Tell the user to copy that URL into a browser on a machine they control.

Only proceed to Step 1 once Google is connected.

---

## Step 1: Resume

**Goal:** Create `resume.md` — the master resume that all other skills read from.

Start by asking:

"First things first — I need your resume. You can:
- Upload it (PDF or Word doc)
- Paste the text right here
- Share a Google Doc link

Whatever's easiest."

Once you have it, parse it into a structured markdown format:

```markdown
# [Full Name] — Master Resume

## Contact
- Phone: [X]
- Email: [X]
- LinkedIn: [X]
- Website: [X] (if applicable)

## Education
### [School Name]
[Degree], [Graduation date]
[Notable activities, leadership roles, honors]

### [Previous school if applicable]
[Degree], [Graduation date]

## Experience

### [Company Name] — [Role Title]
[Date range]
- [Bullet 1]
- [Bullet 2]
- [Bullet 3]

[Repeat for each role]

## Skills
[Technical skills, certifications, languages]

## Narrative Summary
[2-3 sentences: who is this person, what's their thread, what makes them unusual]

## Target Roles
[What they're going after — filled in during Step 3, leave blank for now]
```

**After parsing, review the resume with the user:**

Look at each bullet critically. Flag any that are weak:
- Bullets that start with "Responsible for" or "Helped with" or "Assisted in"
- Bullets without metrics or results
- Bullets that are vague ("Improved processes" — which processes? by how much?)

If you find weak bullets, offer to help:
"I noticed a few bullets that could be stronger. For example, you wrote '[weak bullet]' — what was the actual result? Can you put a number on it? I can help you rewrite these before we save."

Coach them through strengthening bullets using the what/how/result/why framework:
- What: the task or accomplishment
- How: the skills or method used
- Result: the measurable impact
- Why: the context that makes it meaningful

Once the user is happy with the resume, save it to `~/.claude/get-me-a-job/references/resume.md`. All skills read from this single location.

### Step 1b: Set Up Google Drive Folder and Resume Template

**Goal:** Create a job search folder in the user's Google Drive, upload their formatted resume as the master template, and save the Doc ID so resume-tailor can copy from it every time (preserving their formatting perfectly).

Step 0 already authenticated the user, so Drive/Docs/Gmail are all available.

**1. Create the job search folder:**
Run:
```
python ${CLAUDE_PLUGIN_ROOT}/lib/run.py gdocs create-folder "Job Search — [Name]"
```
This returns a JSON with `folder_id` and `url`. Save both.

**2. Get the master resume:**
Ask the user:
"I've created a 'Job Search — [Name]' folder in your Google Drive. Now I need your formatted resume as a template. This is the doc I'll copy every time I tailor your resume, so the formatting stays perfect.

You can:
- **Upload a .docx file** — I'll upload it to your Google Drive folder
- **Share a Google Doc link** — I'll copy it into the folder

Whichever you use, make sure the formatting looks how you want it — bold company names, italic titles, clean spacing. This is your template."

**3. Process the resume:**

If they upload a .docx:
- Upload it to the Job Search folder:
  ```
  python ${CLAUDE_PLUGIN_ROOT}/lib/run.py gdocs upload /path/to/resume.docx FOLDER_ID
  ```
- This returns a JSON with `file_id` — that's the Doc ID (Google Drive auto-converts .docx to Google Docs format)

If they share a Google Doc link:
- Extract the Doc ID from the URL (it's the long string between `/d/` and `/edit`)
- Copy it into the Job Search folder:
  ```
  python ${CLAUDE_PLUGIN_ROOT}/lib/run.py gdocs copy DOC_ID "Master Resume" FOLDER_ID
  ```
- The returned JSON has the new Doc ID

**4. Save configuration:**
Save the IDs and URLs to `~/.claude/get-me-a-job/config.json` (merge into the existing JSON; don't overwrite other keys):

```json
{
  "job_search_folder_id": "FOLDER_ID",
  "job_search_folder_url": "URL",
  "master_resume_doc_id": "DOC_ID",
  "master_resume_url": "URL"
}
```

All skills read these IDs from `~/.claude/get-me-a-job/config.json`.

Tell the user: "Your template is saved. Every time you run `/tailor`, I'll copy this doc and swap in the tailored content — your formatting stays perfect every time. Here's the folder: [folder URL]"

---

## Step 2: Behavioral Stories

**Goal:** Create `stories.md` — structured STAR stories for interviews.

Ask the user which path they want:

"Next up: your interview stories. These are the 3-5 accomplishments you'll draw on for every behavioral question. You can:
- **Upload a doc** if you already have stories written down — I'll structure them into STAR format
- **Build them with me now** — I'll interview you and we'll craft them together
- **Skip for now** — but heads up, this is the single most important part of interview prep. Without structured stories, your answers will be vague and forgettable."

### Option A: They upload a doc
Read the doc. For each story, check if it has all four STAR components:
- **Situation**: Clear context (2 sentences max)
- **Task**: What was the user's specific responsibility
- **Action**: What the user specifically did (not "we" — "I")
- **Result**: Measurable outcome with a number or observable change

If any component is missing, flag it:
"Your [story name] story has a great action but no clear result. What actually changed? Did revenue go up? Did churn drop? Did the team ship faster?"

Restructure all stories into clean STAR format and show the user: "Here's how I'd structure this for an interview. Sound right?"

### Option B: Build stories together
Interview them conversationally. For each story:

1. "Tell me about an accomplishment you're proud of. Doesn't have to be fancy — just something where you made a real difference."
2. "What was going on at the time? What was the problem or opportunity?" (establishing Situation)
3. "What was YOUR specific role? Not what the team did — what were YOU responsible for?" (establishing Task — push past "we")
4. "Walk me through what you actually did. What decisions did you make? What was hard about it?" (establishing Action)
5. "What happened? Can you put a number on it? Revenue, users, time saved, anything measurable." (establishing Result — push for metrics)
6. "What did you take away from this?" (for the "what did you learn" follow-up)

After each story, show them the structured version:
"Here's how I'd tell this story in an interview: [structured version]. Does that capture it? Anything you'd change?"

After 3-5 stories, check for theme coverage:
- Leadership / influence without authority
- Failure / learning from mistakes
- Conflict / disagreement with a colleague or stakeholder
- Data-driven decision making
- Ambiguity / making decisions without perfect information
- Cross-functional collaboration
- Going above and beyond / initiative

If they're missing a theme: "You've got great stories for [X] and [Y], but you don't have a clear failure story. Interviewers almost always ask 'tell me about a time you failed.' Got one?"

### Option C: Skip
Save a placeholder:
```markdown
# Interview Stories

Stories not yet configured. Run `/setup` or say "help me build my stories" to create them.

This is the most important part of interview prep — without structured stories, behavioral answers will be vague and forgettable.
```

Tell the user: "No worries. When you're ready, just say 'help me build my stories' and we'll work on it together. This is the thing that'll make the biggest difference in your interviews."

Save to: `~/.claude/get-me-a-job/references/stories.md`

---

## Step 3: Job Search Profile

**Goal:** Create `profile.md` — targeting preferences for company research and fit analysis.

"Now let's figure out what you're actually going after."

Ask these questions (use AskUserQuestion for structured choices where it makes sense):

1. **Target roles**: "What kind of roles are you targeting? PM, consulting, banking, ops, engineering, VC, something else?"

2. **Industries**: "What industries do you care about? And more importantly — why? The 'why' helps me write better cover letters later."

3. **Geographies**: "Where are you willing to work? Are you flexible or locked to a specific city?"

4. **Seniority**: "What level feels right? Entry, mid, senior? Are you open to founding/first-hire roles at startups?"

5. **Core strengths**: "What are you genuinely better at than most people? Don't be humble — this is for targeting, not for a cover letter."

6. **Adjacent strengths**: "What could you make a strong case for, even if it's not your main thing?"

7. **Technical skills**: "Any technical skills? Languages, tools, certifications?"

**If they're unsure about targeting:**
Don't just ask them to pick. Help them reason through it based on their resume:
"Based on your resume, you've got strong experience in [X] and [Y]. That maps well to roles like [A] and [B]. Does that feel right, or are you trying to pivot into something new?"

Help them articulate their narrative — why the roles they want make sense given where they've been.

Save as structured markdown:

```markdown
# Job Search Profile

## Target Roles (in order of priority)
1. [Role type 1]
2. [Role type 2]
3. [Role type 3]

## Core Strengths
- [Strength 1]
- [Strength 2]
- [Strength 3]

## Adjacent Strengths
- [Adjacent 1]
- [Adjacent 2]

## Technical Skills
- [Skill 1, Skill 2, Skill 3]

## Industries (ranked by fit)
1. [Industry 1] — [why]
2. [Industry 2] — [why]
3. [Industry 3] — [why]

## Geographies
- Preferred: [X]
- Open to: [X]
- Not targeting: [X]

## Seniority Range
- Sweet spot: [X]
- Also open to: [X]
- Too senior: [X]
- Too junior: [X]
```

Save to: `~/.claude/get-me-a-job/references/profile.md`

Also update the "Target Roles" section of `~/.claude/get-me-a-job/references/resume.md` with this info.

---

## Step 4: Outreach Style

**Goal:** Create `outreach-style-guide.md` — how the user wants their outreach to sound.

"How do you want to come across when you reach out to people at companies you're interested in?"

**If they don't know what good outreach looks like, teach them:**

"Let me show you two approaches. Here's a generic message most people send:

> Hi [Name], I'm a [School] MBA student and I came across your profile. I'd love to connect and learn more about your experience at [Company]. Would you be open to a quick chat?

And here's what actually gets responses:

> Hey [Name], I was poking around [Company]'s product and noticed [specific thing]. I ran into a similar problem at [previous company] — we ended up [specific solution] and it moved [metric]. Curious if that's the same dynamic you're dealing with or if I'm reading it wrong. Would love 15 min to compare notes.

The second one works because you're giving them something useful, not just asking for their time. It's called the value-first approach."

Then ask:
1. **Tone preference**: "Do you want to come across as direct, warm, curious, or something else?"
2. **Personal rules**: "Any rules? Like 'keep it under 100 words' or 'never sound salesy' or 'always mention [school]'?"
3. **Confirm the default style rules**: No em dashes, use contractions, vary sentence length, no "I hope this message finds you well"

Save as:

```markdown
# Outreach Style Guide

## Approach
Primary: Value-first product insight (find a real problem, connect to your experience, propose a fix)
Fallback: Curiosity bridge (frame a genuine question connecting your experience to their work)

## Tone
[User's preference — e.g., "Direct but warm. Peer-to-peer, not junior-asking-senior."]

## Personal Rules
- [Any user-specific rules]

## Anti-AI Rules (always apply)
- No em dashes — use commas, periods, or restructure
- Use contractions: "I've" not "I have", "I'm" not "I am"
- Vary sentence length — short punchy sentences mixed with longer ones
- End casually: "Thanks so much" beats "Best regards"
- Never use: "I hope this message finds you well", "I'd love to connect", "I came across your profile"

## Subject Line Rule
Subject lines should create curiosity, not describe credentials.
- Wrong: "MBA student interested in PM role"
- Right: "Quick question about [specific thing they're building]"

## Length Limits
- LinkedIn: under 150 words
- Email: under 200 words
```

Save to: `~/.claude/get-me-a-job/references/outreach-style-guide.md`

---

## Step 5: Network Context

**Goal:** Create `network-context.md` — who the user knows and how to find warm paths.

"Last data question: what communities or networks are you plugged into? This helps me find warm paths to people at companies you're targeting."

Ask:
1. **School**: "Where did you go to school? Any strong alumni networks?"
2. **Professional communities**: "Part of any fellowships, accelerators, industry groups, Slack communities?"
3. **Previous employers**: "Where have you worked? Former colleagues are often the best intro path."
4. **Existing contacts**: "Do you already know anyone at companies you're targeting?"
5. **Strongest intro angle**: "When you reach out to someone, what's your strongest opening? School connection, mutual friend, shared industry, cold?"

**If they feel like they don't have a network:**
"You have more than you think. Let's map it out."
- Walk through their previous employers — even one former colleague at a target company is a warm intro
- Their school alumni network — search LinkedIn for [school] + [target company]
- Any professional communities, even informal ones
- "Even one alumni at a target company is enough to get a conversation. You don't need a huge network — you need one good path."

Save as:

```markdown
# Network Context

## Who [Name] Is
[1-2 sentences: school, background, what they're looking for — for use as context in outreach]

## Network Communities
- **School**: [School name, graduation year, any clubs or leadership roles]
- **Professional**: [Fellowships, accelerators, industry groups]
- **Previous employers**: [Company list — former colleagues are warm paths]
- **Other**: [Any other relevant communities]

## Target Company Contacts
[Any existing contacts at target companies, or "None yet"]

## Strongest Intro Angles
1. [Strongest angle — e.g., "Haas alumni connection"]
2. [Second angle — e.g., "Former colleague at same company"]
3. [Third angle — e.g., "Cold outreach with product insight"]

## Warm Path Search Strategy
When looking for contacts at a target company, search in this order:
1. [School] alumni at the company
2. Former colleagues from [previous employers]
3. [Professional community] members
4. Mutual LinkedIn connections
5. Cold outreach (last resort)
```

Save to: `~/.claude/get-me-a-job/references/network-context.md`

---

## Step 6: Connector Verification

"Alright, the personal stuff is done. Let me make sure your tools are working."

**Test Google (Drive + Docs + Gmail — one auth, all three):**
```
python ${CLAUDE_PLUGIN_ROOT}/lib/run.py gdocs auth
python ${CLAUDE_PLUGIN_ROOT}/lib/run.py gmail list-unread 1
```
The first call confirms the credentials and prints the user's email. The second confirms the Gmail scope was granted (just count the result; don't show contents). If either fails:
- Does `~/.claude/get-me-a-job/credentials.json` exist?
- Did they sign in with their @berkeley.edu account?
- If the credential file is corrupt, re-run `python ${CLAUDE_PLUGIN_ROOT}/lib/run.py google_auth` to refresh it.

**Test Hunter (optional):**
If a Hunter MCP connector is configured in Cowork, try a test domain search on a well-known company. If not configured, tell them: "No email finder connected — that's fine. Network outreach will use LinkedIn and email pattern guessing instead. Hunter.io has a free tier (25 searches/month) if you want it later."

Report status:
```
Connector Status:
✓ Google Drive / Docs — connected
✓ Gmail — connected
○ Hunter — not connected (optional)
```

If Google fails, don't move to Step 7. Help them fix it before continuing.

---

## Step 7: Smoke Test

"Everything's set up. Let's test it with a real job. Paste a JD you're interested in — or I can find one for you."

Once they paste a JD:
1. Run the resume-tailor skill on it
2. Verify the tailored resume is produced (Word doc and/or Google Doc)
3. Show them the result: "Here's your tailored resume. See how I moved [X] to the top because the JD emphasizes [Y]?"
4. Show the gap report

Then wrap up:
"You're all set. Here's what you can do now:
- `/tailor` — paste a JD, get a tailored resume
- `/interview` — name a company, get a full interview prep doc
- `/network` — name a company, get contacts and outreach drafts

And you can always just talk to me naturally — 'help me apply to this role', 'I have an interview at Stripe', 'who should I reach out to at Notion' — I'll figure out which skill to use."

---

## Behavioral Rules

- **Be conversational, not form-like.** This is a career coaching session, not a bureaucratic intake form.
- **If the user gets tired, let them stop.** "We can pick this up anytime. Just say 'let's finish setup.'"
- **Always offer to help BUILD, not just collect.** If their resume bullets are weak, help rewrite them. If they don't have stories, interview them. If they don't know their target roles, reason through it with them.
- **Track completion.** At the end (or whenever they stop), report which steps are done and which are pending.
- **Use AskUserQuestion** for structured choices (role types, industries, tone preferences) but keep the conversation flowing naturally around it.
- **Run the humanizer** on any content you generate during setup (rewritten bullets, structured stories, outreach examples) before saving.
