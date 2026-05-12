# get-me-a-job

An AI-powered job search pipeline built by a Berkeley Haas MBA student who used it to land a job. Now packaged for classmates.

GO BEARS.

---

## What It Does

Six skills that work together to run your entire job search from Cowork:

- **Resume Tailor** — Paste a JD, get a tailored resume with rewritten bullets and a gap analysis
- **Cover Letter** — Writes cover letters that sound human, not like a robot summarizing your resume
- **Interview Prep** — Company research, 15-20 tailored questions, story mapping, practice mode
- **Network Outreach** — Finds contacts, drafts value-first outreach messages. 
- **Company Research** — Deep research briefs with fit analysis against your profile
- **Humanizer** — Strips AI-sounding patterns from any text (mandatory pass on all outputs)

Three shortcut commands:

- `/tailor` — paste a JD, get a tailored resume
- `/interview` — name a company, get a full prep doc
- `/network` — name a company, get contacts and outreach drafts

And a one-time onboarding wizard:

- `/setup` — walks you through creating your resume, stories, profile, outreach style, and network context

---

## Getting Started

### Step 1: Install the Plugin

1. Clone the plugin repo: `git clone https://github.com/kope-kope/haas-job-plugins.git`
2. In Cowork, go to Settings → Plugins → Install from folder
3. Select the `get-me-a-job` folder from the cloned repo

### Step 2: Connect Google Drive & Docs

You need this for resume storage, cover letter creation, and tailored resume output. This uses the Google APIs directly (not a Cowork connector).

1. Install Python dependencies: `pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client requests`
2. `cd` into the `get-me-a-job` plugin folder
3. Run: `python lib/run.py google_auth`
4. Your browser will open — sign in with your @berkeley.edu Google account and grant permissions
5. Done. Credentials are saved locally and everything else happens automatically during `/setup`.

To verify it worked: `python lib/run.py gdocs auth` — should print your email and "authenticated".

### Step 3: Connect your Berkeley Gmail (Optional but Recommended)

For sending outreach emails directly from Cowork.

1. Clone the Gmail MCP server: `git clone https://github.com/kope-kope/berkeley-gmail-mcp.git`
2. Download `client_creds.json` from the shared Berkeley Google Drive folder and place it in the cloned repo
3. Run the setup script (`uv run setup.py`) — it will open a browser for you to OAuth with your @berkeley.edu account
4. The MCP server runs locally on your machine

### Step 4: Connect Hunter.io (Optional)

For finding email addresses during outreach. Free tier gives you 25 searches/month.

1. Sign up at hunter.io
2. Add your API key as a connector in Cowork

Without Hunter, outreach falls back to LinkedIn and email pattern guessing. Totally fine.

### Step 5: Run /setup

This is where the magic happens. Say `/setup` in Cowork and the plugin will walk you through:

1. **Resume** — Upload your resume (PDF, Word, or Google Doc link). The plugin parses it, flags weak bullets, and helps you strengthen them before saving.
2. **Google Drive** — Creates a "Job Search" folder in your Drive and saves your formatted resume as a template. Every tailored resume copies this template so your formatting stays perfect.
3. **Behavioral Stories** — Build 3-5 STAR stories for interviews. You can upload existing stories, build them conversationally with the AI, or skip and come back later.
4. **Job Search Profile** — Target roles, industries, geographies, seniority, strengths. If you're unsure, the plugin helps you reason through it based on your resume.
5. **Outreach Style** — How you want your outreach to sound. Teaches you the value-first approach and lets you set your own rules.
6. **Network Context** — Maps your communities, alumni networks, and former colleagues for warm intros.
7. **Connector Check** — Tests that Google, Gmail, and Hunter are working.
8. **Smoke Test** — Tailors a real JD to make sure everything works end-to-end.

---

## How It Works

Every skill reads from personal reference files that `/setup` creates under your home directory:

```
~/.claude/get-me-a-job/
├── credentials.json                ← OAuth tokens (from Google sign-in)
├── config.json                     ← Drive folder ID, master resume Doc ID
└── references/
    ├── resume.md                   ← your master resume
    ├── stories.md                  ← your STAR stories
    ├── profile.md                  ← your job search targeting
    ├── outreach-style-guide.md     ← your outreach preferences
    └── network-context.md          ← your network map
```

Your data lives in your home directory, not inside the plugin install. Updating or reinstalling the plugin won't touch any of it.

---

## Safety Rules

- **No emails sent without your approval.** Every outreach draft is shown to you first. You say "send it" before anything goes out.
- **No fabricated metrics.** If a resume bullet needs a number, the plugin asks you for the real one instead of making one up.
- **Humanizer pass on everything.** Every cover letter, outreach message, and interview prep doc goes through the humanizer before you see it. Recruiters can spot AI writing instantly.

---

## Examples

The `examples/` folder contains anonymized versions of what your reference files will look like after `/setup`:

- `example-resume.md` — what a finished master resume looks like
- `example-stories.md` — what structured STAR stories look like
- `example-profile.md` — what a job search profile looks like
- `example-network-context.md` — what a network map looks like
- `example-outreach-style-guide.md` — what an outreach style guide looks like

---

## Requirements

- Cowork (Claude desktop app)
- Python 3.8+ (for Google Drive auth and API scripts)
- Google Drive & Docs (required — set up via `python lib/run.py google_auth`)
- Gmail MCP server (recommended)
- Hunter.io API key (optional)
- A Berkeley Haas MBA and the will to get a job

---

## Built By

Tosin Oladokun — Berkeley Haas MBA '26

This plugin got me a job. Now it's your turn.
