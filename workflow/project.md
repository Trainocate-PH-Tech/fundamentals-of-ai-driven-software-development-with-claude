# Issue Tracker project profile

## Verified baseline and workspace

Start Claude at the course root. Student apps are issuetrackerapi/ and
issuetrackerweb/. Read their AGENTS.md files before editing. The baseline has User,
string UUID IDs, JWT login, admin-only /users, FastAPI/SQLAlchemy/Alembic and
React/Bootstrap/esbuild with HashRouter. The course runner selects PostgreSQL.
Python 3.14 and Node 24 are the course runtimes.

## Target contract — not a claim of current implementation

Students add Category and Issue, category/issue endpoints, safe authenticated
/assignees selection, filtering and the tracker UI. These are absent at baseline.
Read SOFTWARE_SPECIFICATIONS.md for requirements. Intended PATCH behavior is
omitted = preserve; explicit null clears assignee. Target errors include 422 for
invalid fields, 404 for missing references and 409 for duplicate/protected categories.
Inspect actual source before claiming any target behavior exists.

## Active workspace and progress

Default: root student apps. Do not inspect instructor-reference/ or recovery/ unless
the task explicitly requests them. A recovery handoff must name both app paths and
the matching --workspace argument. --reference selects the completed solution.
The milestone handoff records progress; do not infer completion from this profile.

## Commands from course root

- ./workshop doctor
- ./workshop setup
- ./workshop db up
- ./workshop db migrate
- ./workshop db seed (requires completed data slice; resets local demo admin password)
- ./workshop start api (foreground terminal A)
- ./workshop start web (foreground terminal B)
- ./workshop test (dedicated test DB; destructive fixtures, never development data)
- ./workshop build
- ./workshop e2e (requires completed browser tests and both servers)

Student ports: 3000/8000, dev/test DB 54329/54330. Reference ports:
3001/8001, DB 54331/54332. Recovered workspaces reuse student host ports.

## Evidence

Use workshop-output/milestones/<milestone-id>/ with plan.md, review.md,
evidence.md, handoff.md and logs/. Record workspace, app revisions, dirty state,
commands, exit codes, outcomes and acceptance criteria. Preserve earlier milestones.
Use setup and exploration for Modules 1–2, 01-data through 05-filters for backend,
06a-categories-ui, 06b-issue-create-details, 06c-edit-assignment,
06d-filters-deletion for frontend, and final for acceptance. These artifact IDs
are not all recovery checkpoints. Only the checkpoints README defines recovery names.
For another project, replace this profile's paths, contracts and commands first.

## Host and shell selection

Before executing commands, identify the OS, active shell, workspace, and Python.
On native Windows PowerShell use `py -3.14 -m tools.workshop` in place of
`./workshop`. Inside Git Bash on Windows use `python -m tools.workshop` after
confirming `python --version` is 3.14; this still uses Windows dependencies.
Linux/WSL uses `./workshop`. Do not mix Windows and WSL virtual environments or
node_modules. The launcher selects Scripts/python.exe versus bin/python.
Use PowerShell file/environment syntax in PowerShell, Bash syntax in Bash.
Keep tokens in environment configuration, never in source or evidence logs.
