# Module 1 — Establish a reproducible workspace

**Entry:** Bash, Git, Python 3.14, Node 24 and a working Docker daemon.
**Result:** two pinned application repos, PostgreSQL, explicit AI instructions.
Start at the course root (the directory containing `workshop`). Install Claude using
[terminal setup](../CLAUDE_CODE_TERMINAL.md) or [VS Code setup](../CLAUDE_CODE_VSCODE_SETUP.md).

## 1. Inspect and install

```bash
pwd
./workshop doctor
./workshop setup
./workshop db up
./workshop db migrate
./workshop install-kit
mkdir -p workshop-output/milestones/setup workshop-output/milestones/exploration workshop-output/milestones/01-data
```

Expected: Python 3.14 and Node 24, both PostgreSQL containers healthy, migration
`0002_add_role_to_users` applied in the student baseline. Setup uses exact commits
and lockfiles. It preserves `.env`; it does not pull latest template changes.
Do not use `db seed` yet: the category seed is built in Module 4.

The root already has course guidance in AGENTS.md. The installer **preserves** it
and stages its generic candidate at `.workshop/proposed/AGENTS.md`. Read both and
merge applicable shared rules; do not replace course instructions blindly. It
installs CLAUDE.md, which imports root AGENTS.md and workflow/project.md. Restart
Claude after installing project skills/agents.

```bash
cat CLAUDE.md
cat workflow/project.md
git -C issuetrackerapi status --short
git -C issuetrackerweb status --short
./workshop test
./workshop build
```

Expected: baseline tests/build pass. The changes already visible in Git are the
workshop's documented compatibility fixes, not student feature work. Review them,
then create a baseline commit separately in each repository. If Git identity is
missing, configure your own name/email before committing.

```bash
git -C issuetrackerapi add .
git -C issuetrackerapi commit -m "Establish tested workshop baseline"
git -C issuetrackerweb add .
git -C issuetrackerweb commit -m "Establish tested workshop baseline"
claude
```

## 2. Validate instructions, not just file existence

Follow [project structure](01_PROJECT_STRUCTURE.md), then
[modify and test Claude context](01_CLAUDE_SETUP.md). Inside Claude, use `/memory`
to inspect loaded files and `/agents` to confirm `workshop-reviewer` is available.

**Claude prompt — guided:**

```text
Read CLAUDE.md, AGENTS.md, workflow/project.md, and SOFTWARE_SPECIFICATIONS.md.
Analyze the workspace without editing application source or reading .env files.
Identify which instructions were imported, each app's purpose, where User lives,
and which database is safe for tests. Cite paths for every architectural claim.
Save the analysis to workshop-output/milestones/setup/map.md. Flag unknowns, don't guess.
```

**Independent exercise:** add a rule to root AGENTS.md requiring a migration review
before changing relationships. Add a Claude-specific instruction to CLAUDE.md to
return a short evidence table. Restart Claude and ask it to plan a category foreign
key change without implementing it. Check the actual answer mentions the migration
review and evidence table; file existence alone is not proof. Record misses and revise.

## 3. First supervised subagent

A subagent is a separate context with a bounded role. It does not automatically
know your conversation. Our reviewer has Read/Glob/Grep tools and cannot execute
commands or edit files. Give it explicit inputs:

```text
Use workshop-reviewer to inspect workshop-output/milestones/setup/map.md against
workflow/project.md and the two application repositories. Ask it to identify
unsupported claims, with paths. Do not implement fixes. Save its returned report
to workshop-output/milestones/setup/review.md in the main session.
```

Observe the named task in Claude's UI; expand it for tool activity. Check its report
exists and contains evidence. A confident summary is not proof of completion.
**Independent:** deliberately put an incorrect API port in a copy of the map and
ask the reviewer to find it. Correct the map, not the real configuration.

**Exit gate:** tests/build pass; root context imports are visible; map and reviewer
report agree on app paths, ports and test DB. If Docker is unavailable, fix the
daemon before continuing. If a port is occupied, stop the conflicting course
workspace with `./workshop db stop`; do not delete Docker volumes.

Next: [Module 2](../02-application-fundamentals/README.md).

Apply this workflow in the [diagnostic lab](DIAGNOSTIC_LAB.md).
