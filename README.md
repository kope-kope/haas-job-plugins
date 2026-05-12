# get-me-a-job

An AI-powered job search pipeline built by a Berkeley Haas MBA student who used it to land a job. Now packaged for classmates.

GO BEARS.

> Restricted to `@berkeley.edu` accounts. The Google OAuth app is configured as Internal to the Berkeley Workspace.

---

## What it does

Six skills that work together to run your entire job search from Cowork:

- **Resume Tailor** — Paste a JD, get a tailored resume with rewritten bullets and a gap analysis
- **Cover Letter** — Writes cover letters that sound human, not like a robot summarizing your resume
- **Interview Prep** — Company research, 15-20 tailored questions, story mapping, practice mode
- **Network Outreach** — Finds contacts, drafts value-first outreach messages, sends via your Gmail after you approve
- **Company Research** — Deep research briefs with fit analysis against your profile
- **Humanizer** — Strips AI-sounding patterns from any text (mandatory pass on all outputs)

Three shortcut commands:

- `/tailor` — paste a JD, get a tailored resume
- `/interview` — name a company, get a full prep doc
- `/network` — name a company, get contacts and outreach drafts

And a one-time onboarding wizard:

- `/setup` — authenticates Google, then walks you through resume, stories, profile, outreach style, and network context

---

## Getting started

### 1. Install the plugin

In Cowork:

```
/plugin marketplace add kope-kope/haas-job-plugins
/plugin install get-me-a-job@haas-job-plugins
```

### 2. Run `/setup`

That's it. `/setup` handles everything else:

1. **Connect Google** — opens your browser, you sign in with `@berkeley.edu`, click Allow once. Drive, Docs, and Gmail are all granted in a single consent screen.
2. **Resume** — upload your formatted resume (`.docx` or Google Doc link). `/setup` parses it for the skills to use, creates a `Job Search` folder in your Drive, and saves your formatted doc as the master template.
3. **Behavioral stories** — build 3–5 STAR stories conversationally, or upload existing ones.
4. **Job search profile** — target roles, industries, geographies, seniority, strengths.
5. **Outreach style** — how you want your messages to sound.
6. **Network context** — communities, alumni networks, former colleagues.
7. **Connector check** — verifies Drive/Docs/Gmail are working.
8. **Smoke test** — tailors a real JD end-to-end to confirm everything's wired up.

You can stop at any step and resume later — `/setup` is idempotent.

### 3. (Optional) Connect Hunter.io for email finding

Free tier: 25 searches/month. Add your Hunter API key as a connector in Cowork. Without it, outreach falls back to LinkedIn and email pattern guessing — still works fine.

---

## How it works

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

Your data lives in your home directory, not inside the plugin install. Updating or reinstalling the plugin doesn't touch any of it.

The Python helpers in `lib/` (`gdocs.py`, `gmail.py`, `google_auth.py`) are invoked through `lib/run.py`, which picks the best Python install path automatically:

1. `uv` if available — uses [PEP 723](https://peps.python.org/pep-0723/) inline deps, zero install
2. Existing pip install — just runs
3. Auto pip install — installs `requirements.txt` once on first use, then runs

Works the same on macOS, Linux, and Windows.

---

## Safety rules

- **No emails sent without your approval.** Outreach is drafted first, you see it in chat and (after Gmail-draft) in your inbox, and only an explicit "send it" triggers delivery.
- **No fabricated metrics.** If a resume bullet needs a number, the plugin asks you for the real one instead of inventing one.
- **Humanizer pass on everything.** Cover letters, outreach messages, and interview prep docs all go through the humanizer before you see them. Recruiters spot AI writing instantly.

---

## Examples

The `examples/` folder shows what your reference files will look like after `/setup`:

- `example-resume.md` — finished master resume
- `example-stories.md` — structured STAR stories
- `example-profile.md` — job search profile
- `example-network-context.md` — network map
- `example-outreach-style-guide.md` — outreach style guide

---

## Requirements

- Cowork (Claude desktop app)
- Python 3.10+ (the dispatcher will install dependencies on first use)
- A `@berkeley.edu` Google account (the OAuth app is restricted to Berkeley Workspace)
- A Berkeley Haas MBA and the will to get a job

---

## Security

The OAuth client config in `lib/credentials.b64` is intentionally distributed with the plugin. The Internal-app restriction means a leaked credential is useless outside the Berkeley Workspace. Details and threat model in [SECURITY.md](SECURITY.md).

---

## Built by

Tosin Oladokun — Berkeley Haas MBA '26

This plugin got me a job. Now it's your turn.
