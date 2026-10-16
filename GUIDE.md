# Instructor guide: delivering the Claude Code engineering workshop with SQLite

This guide uses **SQLite and direct commands** on Linux/WSL or Windows PowerShell
7.4+. Docker and a database server are not required. Use the Python, Node, Git and
Claude prerequisites in [Windows setup](WINDOWS_SETUP.md). Choose the block for your shell and the stated working directory.

SQLite is the teaching default in the specification, modules and project profile.
Use ordinary Claude requests and direct development commands. Historical maintenance
tooling is not part of the classroom workflow.

This is the facilitator's companion to the [student course](README.md). It explains
what to prepare, demonstrate, say, ask students to do, and verify. Students follow
the five module READMEs; use this guide to orchestrate those lessons rather than
introducing a competing sequence. For delivery without the provided tooling, use
the [manual track](#manual-track-build-and-operate-the-workspace-without-workshop-tools):
it supplies the folder layout, direct commands, and plain Claude/subagent prompts.

The outcome is a working Issue Tracker backed by SQLite, with a FastAPI API,
React interface, automated checks, and a reusable Claude Code engineering workflow.
The [software specification](SOFTWARE_SPECIFICATIONS.md) is the behavior contract.
The [validation record](VALIDATION.md) describes earlier executed checks and their
limits; rerun the relevant checks before your own delivery.

## Contents

1. [Delivery approach and preparation](#1-delivery-approach-and-preparation)
   - [Manual track: setup, direct commands, and your own subagents](#manual-track-build-and-operate-the-workspace-without-workshop-tools)
2. [Instructor rehearsal and opening demonstration](#2-instructor-rehearsal-and-opening-demonstration)
3. [Module 1: project setup and trustworthy context](#3-module-1-project-setup-and-trustworthy-context)
4. [Module 2: understand the application](#4-module-2-understand-the-application)
5. [Module 3: reusable skills and supervised subagents](#5-module-3-reusable-skills-and-supervised-subagents)
6. [Module 4: build verified increments](#6-module-4-build-verified-increments)
7. [Module 5: verification, debugging, and handoff](#7-module-5-verification-debugging-and-handoff)
8. [Recovery and classroom troubleshooting](#8-recovery-and-classroom-troubleshooting)
9. [Assessment and closing](#9-assessment-and-closing)
10. [Preparing the course for GitHub](#10-preparing-the-course-for-github)
11. [Instructor reference map](#11-instructor-reference-map)

## 1. Delivery approach and preparation

### Audience and prerequisites

Learners should be able to navigate folders, edit a file, run a terminal command,
and explain a basic HTTP request. They do not need prior Claude Code experience.
For learners unfamiliar with Git, Python environments, React, or relational
constraints, schedule a prerequisite lab. Do not spend the implementation sessions
trying to install missing system software on every machine.

Delivery environments: Bash on Linux/WSL2 or PowerShell 7.4+ on Windows, Python 3.14, Node 24, Git,
and a browser. Claude Code requires the learner's supported
account or API billing. Windows and macOS require their own full classroom
rehearsals; consult VALIDATION.md for executed checks and remaining platform gates.

Send these materials before class:

- [Terminal Claude setup](CLAUDE_CODE_TERMINAL.md) and [VS Code setup](CLAUDE_CODE_VSCODE_SETUP.md).
- [Module 1 prerequisites](01-project-setup/README.md).
- The course repository URL once published, and instructions to open its root folder.
- A request to verify Python SQLite support and Claude authentication before class.

Keep authentication off the shared screen. Claude's account/API credentials are
separate from the Issue Tracker's local demo account. The app does not need an
Anthropic API key. Use the setup guides' hidden-input procedure for API access;
do not ask learners to paste tokens into chat or instructor notes.

### Suggested pacing

These are planning ranges, not time limits or measured completion guarantees.
Advance by exit gates. Split Module 4 across sessions when necessary.

| Segment | Suggested time | Evidence before moving on |
|---|---:|---|
| Pre-class setup | 60–90 minutes | Python, Node, Git and Claude available |
| Opening demonstration | 20–30 minutes | Learners can describe the target workflow |
| Module 1 | 90–120 minutes | Baseline checks and instruction probes |
| Module 2 | 60–90 minutes | Source-backed application map |
| Module 3 | 120–150 minutes | Accepted plan, custom skill and reviewer report |
| Module 4 | 4–6 hours | Six implemented slices and real browser integration |
| Module 5 | 120–150 minutes | Verification evidence, regression repair and handoff |
| Demonstrations and assessment | 45–60 minutes | Complete browser demo and explanation |

For a shorter event, assign setup beforehand and continue implementation later.
Do not claim the full engineering outcome after only demonstrating prompts.

### Teaching rhythm

For each exercise, explain the requirement, demonstrate one bounded task, let
students repeat it, then give a different independent task. Ask students to show
source and execution evidence before accepting completion. Pairing works well:
one learner operates Claude while the other checks scope, diffs, and results;
switch roles at each slice.

**Instructor says:**

> Our workflow is explore, plan, implement, and verify. Claude can propose and write
> changes, but we remain responsible for scope, permissions, data, and proof that
> the system works. A review report and a passing test answer different questions.

### Establish terminal conventions

Terminal blocks run from the active project root unless explicitly stated.
Open the manual workspace in the editor; its root contains both app directories,
AGENTS.md and CLAUDE.md. References to course files mean the separate course clone. A `text` block is a prompt to paste inside Claude, not a shell command.
Each command block is a checkpoint: inspect failures before continuing.

Use three named terminals once servers are needed:

| Terminal | Purpose |
|---|---|
| A — API | Foreground API process; leave running |
| B — Web | Foreground frontend process; leave running |
| C — Checks | Setup, tests, builds, Git inspection, and Claude sessions |

| Workspace | API | Web | Database files relative to its API directory |
|---|---:|---:|---|
| Student manual root | 3000 | 8000 | `storage/development.sqlite3`, `test.sqlite3` |
| Instructor reference | 3001 | 8001 | `storage/development.sqlite3`, `test.sqlite3` |
| Recovered workspace | 3000 | 8000 | Its own files at the same relative paths |

The reference can coexist with student work because its ports and source directory
are distinct. Stop student servers before starting recovery on the same ports.
SQLite has no database host port or background service. The test file is at the
API root to match the template's existing isolation assertion. Keep it separate
from development; do not place it under `storage_test/`, which fixtures delete.

## Manual track: build and operate the workspace without workshop tools

Use this track when students should see and execute every underlying command.
It replaces the launcher-based setup and verification steps; it does not change the
five modules' learning objectives or the software specification. Do not run both
setup tracks against the same directories. No provided launcher, installer or
custom orchestration skill is needed in the new workspace. Claude receives ordinary
prompts, and students create and invoke their own subagents.

**Starting point:** the course repository is downloaded, Python 3.14, Node 24,
Git and Claude are installed. Python includes the SQLite driver; no separate
SQLite CLI or database service is required.
Use [Windows setup](WINDOWS_SETUP.md) for prerequisites and
[terminal authentication](CLAUDE_CODE_TERMINAL.md) for sign-in. API credentials
belong to Claude's environment, not either application's environment files.

Every terminal block names its working directory. Stop on a failed command; do
not paste the entire chapter as one script. In each new PowerShell terminal set
`$ErrorActionPreference = 'Stop'` and
`$PSNativeCommandUseErrorActionPreference = $true` before multi-command blocks.

### M1. Folder diagram and ownership

Create a **new sibling directory**, `issue-tracker-manual`, beside the course.
Start Claude at that new root so it can see both apps and the shared instructions.
This tree shows the desired layout after setup; `(later)` entries are built during
Modules 3–5, not supplied by the baseline.

```text
projects/
├── fundamentals-of-ai-driven-software-development-with-claude/  # course reference
│   ├── GUIDE.md
│   ├── SOFTWARE_SPECIFICATIONS.md
│   └── checkpoints/00-baseline/                               # reviewed compatibility patches
└── issue-tracker-manual/                                      # open this folder in VS Code
    ├── AGENTS.md                                             # shared engineering rules
    ├── CLAUDE.md                                             # imports AGENTS.md for Claude
    ├── workflow/project.md                                   # direct commands and SQLite targets
    ├── SOFTWARE_SPECIFICATIONS.md                            # copied behavior contract
    ├── .gitignore
    ├── .claude/
    │   ├── settings.json                                     # secret-file permissions
    │   └── agents/
    │       ├── architecture-reviewer.md
    │       └── acceptance-reviewer.md
    ├── workshop-output/                                      # local evidence, ignored by Git
    │   └── milestones/
    │       ├── setup/
    │       ├── exploration/
    │       └── 01-data/                                      # more milestone folders later
    ├── issuetrackerapi/                                      # independent Git repository
    │   ├── .git/
    │   ├── AGENTS.md                                         # preserve template instructions
    │   ├── .env                                              # local, never committed
    │   ├── .venv/                                            # generated for this OS
    │   ├── storage/
    │   │   └── development.sqlite3                            # local app data, generated
    │   ├── test.sqlite3                                       # disposable tests, generated
    │   ├── requirements.lock.txt
    │   ├── app/{models,schemas,controllers,operations}/
    │   ├── alembic/versions/
    │   └── spec/                                             # tracker tests added later
    └── issuetrackerweb/                                      # independent Git repository
        ├── .git/
        ├── AGENTS.md                                         # preserve template instructions
        ├── .env                                              # local build configuration
        ├── package.json
        ├── package-lock.json
        ├── node_modules/                                    # generated, never committed
        ├── src/js/{services,commons}/
        ├── playwright.config.js                             # later
        └── e2e/                                             # later
```

`AGENTS.md` is shared guidance for tools that read it. Claude loads `CLAUDE.md`,
which explicitly imports that shared file; do not assume it discovers AGENTS.md
automatically. Nested application instructions still apply when editing those
apps. Instructions guide behavior; permissions and tests provide separate checks.
See [Claude memory/imports](https://code.claude.com/docs/en/memory).

### M2. Clone the pinned templates explicitly

**Working directory: the existing course root.** The destination must not exist.
These commands keep the course path available only for copying the specification
and applying the baseline compatibility files.

```bash
course_source=$(pwd)
manual_root="$(dirname "$course_source")/issue-tracker-manual"
if [ -e "$manual_root" ]; then
  echo 'Choose a new destination; existing work must be preserved.'
else
  mkdir "$manual_root"
fi
```

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true
$course_source = (Get-Location).Path
$manual_root = Join-Path (Split-Path $course_source -Parent) 'issue-tracker-manual'
if (Test-Path $manual_root) { throw 'Choose a new destination; existing work must be preserved.' }
New-Item -ItemType Directory -Path $manual_root | Out-Null
```

If the destination existed, stop and choose a different name before continuing.
**Working directory changes to the new manual root:**

```bash
cd "$manual_root"
cp "$course_source/SOFTWARE_SPECIFICATIONS.md" SOFTWARE_SPECIFICATIONS.md
git clone --config core.autocrlf=false https://github.com/cloudband-solutions/default_api_fast.git issuetrackerapi
git -C issuetrackerapi checkout -b workshop/manual 6afada28350e93d5a2cdff7dddcbe88c2036e299
git clone --config core.autocrlf=false https://github.com/cloudband-solutions/admin-panel-web.git issuetrackerweb
git -C issuetrackerweb checkout -b workshop/manual 47578e05f4cca5c035ea51c0b5e92b55d0818928
```

```powershell
Set-Location $manual_root
Copy-Item (Join-Path $course_source 'SOFTWARE_SPECIFICATIONS.md') SOFTWARE_SPECIFICATIONS.md
git clone --config core.autocrlf=false https://github.com/cloudband-solutions/default_api_fast.git issuetrackerapi
git -C issuetrackerapi checkout -b workshop/manual 6afada28350e93d5a2cdff7dddcbe88c2036e299
git clone --config core.autocrlf=false https://github.com/cloudband-solutions/admin-panel-web.git issuetrackerweb
git -C issuetrackerweb checkout -b workshop/manual 47578e05f4cca5c035ea51c0b5e92b55d0818928
```

**Why use patches in a manual track?** These are visible source changes, not an
execution wrapper or completed capstone. The pinned upstream templates need the
course's lockfiles, platform fixes, database test fixes, and frontend baseline
fixes. Inspect/apply **only `00-baseline`**, not the final solution. Omitting the
patches creates a different, unverified starting point. This track removes tooling
dependence; it still uses the course's reviewed starting source.

```bash
git -C issuetrackerapi apply --stat "$course_source/checkpoints/00-baseline/issuetrackerapi.patch"
git -C issuetrackerapi apply --check "$course_source/checkpoints/00-baseline/issuetrackerapi.patch"
git -C issuetrackerapi apply "$course_source/checkpoints/00-baseline/issuetrackerapi.patch"
git -C issuetrackerweb apply --stat "$course_source/checkpoints/00-baseline/issuetrackerweb.patch"
git -C issuetrackerweb apply --check "$course_source/checkpoints/00-baseline/issuetrackerweb.patch"
git -C issuetrackerweb apply "$course_source/checkpoints/00-baseline/issuetrackerweb.patch"
mkdir -p workflow .claude/agents workshop-output/milestones/setup workshop-output/milestones/exploration workshop-output/milestones/01-data
cp "$course_source/workflow/project.md" workflow/project.md
```

```powershell
git -C issuetrackerapi apply --stat "$course_source/checkpoints/00-baseline/issuetrackerapi.patch"
git -C issuetrackerapi apply --check "$course_source/checkpoints/00-baseline/issuetrackerapi.patch"
git -C issuetrackerapi apply "$course_source/checkpoints/00-baseline/issuetrackerapi.patch"
git -C issuetrackerweb apply --stat "$course_source/checkpoints/00-baseline/issuetrackerweb.patch"
git -C issuetrackerweb apply --check "$course_source/checkpoints/00-baseline/issuetrackerweb.patch"
git -C issuetrackerweb apply "$course_source/checkpoints/00-baseline/issuetrackerweb.patch"
New-Item -ItemType Directory -Force -Path 'workflow', '.claude/agents', 'workshop-output/milestones/setup', 'workshop-output/milestones/exploration', 'workshop-output/milestones/01-data' | Out-Null
Copy-Item (Join-Path $course_source 'workflow/project.md') workflow/project.md
```

### M3. Write the root instructions yourself

Create these files in the editor at the **manual root**, using the exact contents
below. These blocks are file contents, not shell commands. Copy the supplied SQLite profile in M2 before creating these imports. Preserve
any existing project-specific guidance instead of replacing it blindly.

**`AGENTS.md`:**

```markdown
# Issue Tracker engineering rules

Read SOFTWARE_SPECIFICATIONS.md before planning feature work.
Inspect both apps' AGENTS.md files and follow their local conventions.
Only Category and Issue are new domain models; reuse User and authentication.
Explore, plan, implement a bounded change, then verify it.
Preserve existing data, unrelated files, instructions, and Git checkpoints.
Use SQLite, following the project profile and software specification.
Keep functional acceptance criteria from SOFTWARE_SPECIFICATIONS.md.
Use direct Python, npm and Git commands from the correct app directory.
Confirm OS and shell before selecting paths; never share .venv between OSes.
Development uses sqlite:///storage/development.sqlite3.
Tests use sqlite:///test.sqlite3, never development data.
Run database commands from issuetrackerapi so relative SQLite paths resolve correctly.
The template expects the test URL sqlite:///test.sqlite3; preserve that exact target.
Preserve SQLite foreign-key enforcement on every application connection.
Do not read, print, edit, or commit .env files or credentials through AI tools.
Human operators configure environments. Report missing configuration without
trying to read secret files or dumping environment variables.
Reviewers return findings; the main session owns edits and test execution.
Save plans, reports, evidence and handoffs under workshop-output/milestones/.
Record actual commands, exit codes, revision and dirty state. Unrun means unverified.
```

**`CLAUDE.md`:**

```markdown
# Claude entry point

@AGENTS.md
@workflow/project.md

Start here at the parent of issuetrackerapi and issuetrackerweb.
Use SOFTWARE_SPECIFICATIONS.md as the behavior contract. Read each app's
AGENTS.md before changing its files. No workshop launcher or custom skill is
installed; use ordinary requests and direct commands.
For uncertain work, plan first and wait for explicit acceptance before editing.
Supply each subagent its task, paths, constraints and expected output.
Do not treat reviewer findings as evidence that tests ran.
```

**`.claude/settings.json`:**

```json
{
  "permissions": {
    "deny": [
      "Read(./**/.env)",
      "Read(./**/.env.*)",
      "Edit(./**/.env)",
      "Edit(./**/.env.*)",
      "Write(./**/.env)",
      "Write(./**/.env.*)"
    ]
  }
}
```

These tool permissions complement the instructions. They are not an OS sandbox
and must not be treated as protection against every shell command; never authorize
secret-printing commands. Give reviewers only read tools and no shell tool.

**Root `.gitignore`:**

```gitignore
.env
.env.*
!.env.example
.venv/
node_modules/
*.sqlite
*.sqlite3
*.sqlite3-*
workshop-output/
.claude/settings.local.json
CLAUDE.local.md
# Application repositories have their own history and commits.
/issuetrackerapi/
/issuetrackerweb/
```

Preserve each application's own `.gitignore`. The root ignore rules apply if you
later initialize a parent repository; they do not prevent secrets being staged
inside either app. Review `git -C <app> diff --cached` before committing.

### M4. Prepare SQLite storage

SQLite is an embedded database. Alembic creates tables inside a local file; there
is no Docker container, database account, port, or database daemon to start.
Create the parent directory before connecting. **Working directory: manual root.**

```bash
mkdir -p issuetrackerapi/storage
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
```

```powershell
New-Item -ItemType Directory -Force issuetrackerapi/storage | Out-Null
py -3.14 -c "import sqlite3; print(sqlite3.sqlite_version)"
```

Use `sqlite:///storage/development.sqlite3` for application data and
`sqlite:///test.sqlite3` for tests. These are **relative file URLs**:
run Alembic, pytest and Uvicorn from the API directory. The three slashes are
intentional and work on both supported platforms. Never point destructive tests
at the development file. Confirm app-local Git ignore rules cover database files;
the root ignore file does not protect files staged inside a nested repository.

The template's app/db.py enables SQLite foreign keys using a connection event.
Preserve that behavior; see [SQLite foreign-key enforcement](https://www.sqlite.org/foreignkeys.html).
SQLite does not enforce declared VARCHAR lengths, so retain the specification's
schema validation and explicit integrity constraints; see
[SQLite type affinity](https://www.sqlite.org/datatype3.html). Use one API process and one browser-test worker for this local workshop.
Concurrent writes can produce `database is locked`; stop competing runs rather than
weakening constraints or treating SQLite as a high-concurrency production setup.

### M5. Install dependencies and configure the applications

**Working directory: manual root.** No virtual-environment activation is required.

```bash
python3 --version
node --version
python3 -m venv issuetrackerapi/.venv
issuetrackerapi/.venv/bin/python -m pip install -r issuetrackerapi/requirements.lock.txt
(cd issuetrackerweb && npm ci)
```

```powershell
py -3.14 --version
node --version
py -3.14 -m venv issuetrackerapi/.venv
& ./issuetrackerapi/.venv/Scripts/python.exe -m pip install -r issuetrackerapi/requirements.lock.txt
Push-Location issuetrackerweb
try { npm.cmd ci } finally { Pop-Location }
```

Stop if Python is not 3.14 or Node is not 24. On Linux/WSL, use `python3.14`
instead of `python3` if needed. Do not replace the lock-based install with an
unbounded requirements install.

Create the backend `.env` with an exclusive-write command. It generates a random
application signing secret without printing it and fails if the file already exists.
**Working directory: manual root; run only your OS's block:**

```bash
issuetrackerapi/.venv/bin/python -c "import secrets; from pathlib import Path; p=Path('issuetrackerapi/.env'); f=p.open('x', encoding='utf-8'); f.write('APP_ENV=development\nDATABASE_URL=sqlite:///storage/development.sqlite3\nSECRET_KEY='+secrets.token_hex(32)+'\n'); f.close(); p.chmod(0o600)"
```

```powershell
& ./issuetrackerapi/.venv/Scripts/python.exe -c "import secrets; from pathlib import Path; p=Path('issuetrackerapi/.env'); f=p.open('x', encoding='utf-8'); f.write('APP_ENV=development\nDATABASE_URL=sqlite:///storage/development.sqlite3\nSECRET_KEY='+secrets.token_hex(32)+'\n'); f.close()"
```

In your editor create **`issuetrackerweb/.env`**:

```dotenv
API_BASE_URL=http://localhost:3000
API_VERSION=v1
WEB_PORT=8000
TOKEN_BEARER=ISSUE_TRACKER_TOKEN
CURRENT_USER=ISSUE_TRACKER_USER
```

`TOKEN_BEARER` and `CURRENT_USER` are browser-storage key names, not credentials.
`API_VERSION` is required by the build. These are build-time values: restart the
frontend after changing them. Existing process environment variables override the
backend dotenv values; use dedicated course terminals with the environment shown
below, not a terminal previously targeting a different database.

### M6. Migrate, seed the existing login, and start both servers

**Terminal A: begin at manual root and enter the API directory.** Keep it there.

```bash
cd issuetrackerapi
unset DATABASE_URL
export APP_ENV=development
.venv/bin/python -m alembic upgrade head
.venv/bin/python -m app.cli system:seed
.venv/bin/python -m uvicorn app:create_app --factory --host 127.0.0.1 --port 3000
```

```powershell
Set-Location issuetrackerapi
Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
$env:APP_ENV = 'development'
& ./.venv/Scripts/python.exe -m alembic upgrade head
& ./.venv/Scripts/python.exe -m app.cli system:seed
& ./.venv/Scripts/python.exe -m uvicorn app:create_app --factory --host 127.0.0.1 --port 3000
```

At baseline, migration head is `0002_add_role_to_users`. `system:seed` creates or
updates the existing local admin (`admin@example.com` / `password`); rerunning it
resets that demo login. **Do not run `app.seed_tracker` yet:** students create it
in the data milestone. At that milestone, rerun Alembic then run
`.venv/bin/python -m app.seed_tracker` (Windows:
`& ./.venv/Scripts/python.exe -m app.seed_tracker`) twice to check idempotence.

**Terminal B: new terminal at manual root; enter the frontend directory.**

```bash
cd issuetrackerweb
npm start
```

```powershell
Set-Location issuetrackerweb
npm.cmd start
```

Open `http://localhost:3000/docs` and `http://localhost:8000/#/login`.
Log in with the local demo account. The baseline has existing users/authentication;
Category and Issue screens do not exist yet. Ctrl+C stops a foreground server.

### M7. Verify the baseline directly and save a Git checkpoint

**Terminal C: start at manual root.** Backend fixtures drop tables; explicitly
select the separate test database. These blocks restore the caller's environment
after testing. On PowerShell enable the failure preferences from M2 in each new
terminal so a failed native command stops the block.

```bash
(
  cd issuetrackerapi
  export APP_ENV=test
  export DATABASE_URL=sqlite:///test.sqlite3
  .venv/bin/python -m pytest spec
)
(cd issuetrackerweb && npm run build)
```

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true
$previous_app_env = $env:APP_ENV
$previous_db_url = $env:DATABASE_URL
Push-Location issuetrackerapi
try {
    $env:APP_ENV = 'test'
    $env:DATABASE_URL = 'sqlite:///test.sqlite3'
    & ./.venv/Scripts/python.exe -m pytest spec
} finally {
    $env:APP_ENV = $previous_app_env
    $env:DATABASE_URL = $previous_db_url
    Pop-Location
}
Push-Location issuetrackerweb
try { npm.cmd run build } finally { Pop-Location }
```

Inspect the result of **each** command; a successful build cannot erase a failed
test result. Save actual outcomes to `workshop-output/milestones/setup/evidence.md`,
including OS, shell, versions, commands, exit codes and skips. Do not claim the
full application is implemented just because the baseline passes.

Once both gates pass, run these Git commands from the manual root in either shell:

```bash
git -C issuetrackerapi status --short
git -C issuetrackerweb status --short
git -C issuetrackerapi add .
git -C issuetrackerapi diff --cached --stat
git -C issuetrackerapi diff --cached
git -C issuetrackerweb add .
git -C issuetrackerweb diff --cached --stat
git -C issuetrackerweb diff --cached
```

Review staged content for credentials, generated files and unexpected changes.
Only after that review, commit in each repository:

```bash
git -C issuetrackerapi commit -m "Establish manually verified workshop baseline"
git -C issuetrackerweb commit -m "Establish manually verified workshop baseline"
```

These Git blocks are identical in PowerShell. Configure your own Git name/email
if prompted. Keep the two application histories; parent-folder commits do not
include them automatically.

### M7a. Verify SQLite migration preservation after the data milestone

The inherited PostgreSQL migration test deliberately skips on SQLite. Keep that
skip visible. Once `0003_tracker` exists, add the following independent check as
**`issuetrackerapi/spec/tracker/test_migrations_sqlite.py`**. It uses a temporary file,
not the development or shared test database, and preserves an existing user across
upgrade, downgrade and re-upgrade. It also exercises actual SQLite foreign keys.

```python
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.exc import IntegrityError


def test_sqlite_tracker_migration_preserves_users(tmp_path, monkeypatch):
    uri = f"sqlite:///{tmp_path / 'migration.sqlite3'}"
    monkeypatch.setattr('config.Config.SQLALCHEMY_DATABASE_URI', uri)
    cfg = Config('alembic.ini')
    engine = create_engine(uri)

    @event.listens_for(engine, 'connect')
    def enable_foreign_keys(connection, _record):
        connection.execute('PRAGMA foreign_keys=ON')

    try:
        command.upgrade(cfg, '0002_add_role_to_users')
        with engine.begin() as connection:
            connection.execute(text("""
                INSERT INTO users
                (id, email, password_hash, first_name, last_name, status, role,
                 created_at, updated_at)
                VALUES ('existing', 'keep@example.com', 'unused', 'Keep', 'Me',
                        'active', 'user', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """))
        command.upgrade(cfg, 'head')
        assert {'users', 'categories', 'issues'} <= set(inspect(engine).get_table_names())
        with engine.begin() as connection:
            assert connection.scalar(text('PRAGMA foreign_keys')) == 1
            assert connection.scalar(text("SELECT email FROM users WHERE id='existing'")) == 'keep@example.com'
            connection.execute(text("""
                INSERT INTO categories (id, name, created_at, updated_at)
                VALUES ('category', 'Bug', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """))
            connection.execute(text("""
                INSERT INTO issues (id, title, status, priority, category_id,
                                    created_at, updated_at)
                VALUES ('issue', 'Keep this reference', 'open', 'medium', 'category',
                        CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """))
        with pytest.raises(IntegrityError):
            with engine.begin() as connection:
                connection.execute(text("DELETE FROM categories WHERE id='category'"))
        command.downgrade(cfg, '0002_add_role_to_users')
        assert 'issues' not in inspect(engine).get_table_names()
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM users WHERE id='existing'")) == 1
        command.upgrade(cfg, 'head')
        assert 'issues' in inspect(engine).get_table_names()
    finally:
        engine.dispose()
```

Run M7's isolated test block, replacing `spec` with
`spec/tracker/test_migrations_sqlite.py`. Use the same OS-specific interpreter.
If your accepted migration has a different revision identifier, inspect its actual
chain and substitute that identifier; do not guess. The existing user's row must
survive; tracker rows are intentionally removed by the downgrade in this disposable
file. **Independent:** extend this test to prove duplicate names differing only in
case fail and deleting a separately created assignee clears `assigned_user_id` while
retaining the original user. Do not execute downgrade drills against development data.

### M8. Create and invoke subagents yourself

Create **`.claude/agents/architecture-reviewer.md`** in the manual root with:

```markdown
---
name: architecture-reviewer
description: Trace a bounded Issue Tracker request flow and check a supplied architecture map.
tools: Read, Glob, Grep
---
Read AGENTS.md and the supplied specification, map and application instructions.
Inspect only the requested source paths. Do not edit files or run commands.
Trace authentication, controller, operation, persistence and frontend API use.
Return facts with paths, uncertainties, contradictions and proposed checks.
Do not infer that a target feature exists or that a test passed.
If an input is absent, report it instead of widening the search to other projects.
```

Create **`.claude/agents/acceptance-reviewer.md`** with:

```markdown
---
name: acceptance-reviewer
description: Review one accepted Issue Tracker milestone against its contract and execution evidence.
tools: Read, Glob, Grep
---
Read AGENTS.md, the supplied accepted plan, specification and evidence.
Inspect the named application's AGENTS.md and only the supplied feature scope.
Return a verdict, severity-ranked findings with paths, missing test cases,
and unsupported completion claims. Do not edit files or execute commands.
Distinguish source inspection from supplied execution evidence.
Never report tests as passed because test code exists. If the plan or evidence
is missing, return insufficient evidence and identify the missing input.
```

The files define the roles; no installer or Python wrapper registers them.
Their tools permit source inspection but not edits or test execution. Start or
restart Claude **at the manual root**, then use `/agents` or the installed client's
help to inspect discovery. In newer clients `/agents` may provide instructions
rather than an interactive wizard. See the
[official subagent documentation](https://code.claude.com/docs/en/sub-agents).

**Terminal, manual root (both shells):**

```bash
claude
```

**Inside Claude — validate context and delegate a real task:**

```text
Read CLAUDE.md, AGENTS.md, SOFTWARE_SPECIFICATIONS.md and both application AGENTS.md
files. Do not read environment files. Report the active workspace and instruction
sources. Then use the architecture-reviewer subagent to trace the existing login
and users request flow in issuetrackerapi/app and issuetrackerweb/src/js. Supply
it the specification and both app instruction files. Ask for path-backed findings
on User identity, auth, request/response shapes and frontend token use. No edits
or commands by the reviewer. Main session: save its returned report to
workshop-output/milestones/exploration/architecture-review.md and label unverified
claims explicitly. Do not implement Category or Issue yet.
```

A subagent is requested by name in an ordinary message; `/architecture-reviewer`
is **not** a skill command. The CLI starts the parent session, and that session
creates the delegated task. You do not launch a separate terminal process for
each reviewer in this exercise.

**Monitor it yourself:** expand the named delegation/tool row and inspect its
inputs, tool calls, status and returned output. Confirm a real task was created;
a main-session answer pretending to be the reviewer is not delegation evidence.
Use `/tasks` if present in your client's `/help` for background work and its stop
control when necessary. No task/output means “not run.” Stop a reviewer that
requests writes or shell execution; inspect its definition and restart before
retrying. The main session must save and assess the returned report.

**Independent exercise:** create `frontend-state-reviewer.md` with the same
read-only tools and a description focused on labelled controls, empty/loading/error
states, filter reset and assignment clearing. Invoke it against an actual frontend
plan. Demonstrate its task row, cite one source-backed finding, and explain one
claim that still requires a browser test. Do not run extra agents solely to make
the transcript look more sophisticated.

### M9. Build each milestone using ordinary Claude requests

Follow the same sequence as Module 4: data → categories → issues → assignment →
filters → category UI → issue create/details → editing/assignment → filters/deletion.
Create a new evidence directory for each step and preserve previous runs.

**Inside Claude — planning example (use Plan Mode):**

```text
Plan milestone 01-data only. Read SOFTWARE_SPECIFICATIONS.md, both app instructions,
and workshop-output/milestones/exploration/architecture-review.md. Inspect actual
models, migrations and test fixtures. Propose Category and Issue models, migration,
and an idempotent app.seed_tracker module. Reuse User and preserve existing data.
Name files, acceptance criteria, tests and direct commands with working directories
and OS-specific interpreter paths. Do not implement or invoke workshop tools/skills.
Return the plan for my review.
```

After accepting the plan and leaving Plan Mode, have the main session save it to
`workshop-output/milestones/01-data/plan.md`. Then send:

```text
I accept workshop-output/milestones/01-data/plan.md. Implement only that scope.
Follow the backend's test-first instructions and use direct commands. Do not read
or change .env files. Tests must use the separate test.sqlite3 file.
Record actual commands, exit codes, skips, changed files and remaining gaps in
workshop-output/milestones/01-data/evidence.md. Do not claim success without execution.
```

**After direct verification, request an independent review:**

```text
Use acceptance-reviewer to review milestone 01-data. Supply AGENTS.md,
SOFTWARE_SPECIFICATIONS.md, workshop-output/milestones/01-data/plan.md,
workshop-output/milestones/01-data/evidence.md, issuetrackerapi/AGENTS.md and the
changed model, migration, seed and spec paths identified in the evidence.
Ask it to check existing User preservation, integrity rules, seed idempotence and
whether the evidence supports completion. Main session: save the result to
workshop-output/milestones/01-data/review.md. Do not fix findings until I review them.
```

Use the same plain-message sequence for each later milestone, substituting its ID,
requirements and scope. Human operators can execute all commands themselves and
supply the resulting evidence instead of authorizing the main session to execute.
Either way, reviewers inspect evidence; they do not manufacture it.

| Milestone gate | Direct command, working directory `issuetrackerapi` unless noted |
|---|---|
| New migration | `.venv/bin/python -m alembic upgrade head` with development environment |
| Data seed | `.venv/bin/python -m app.seed_tracker`, twice, only after implementation |
| Categories | `.venv/bin/python -m pytest spec/tracker/test_categories.py` with test environment |
| Issues | `.venv/bin/python -m pytest spec/tracker/test_issues.py` with test environment |
| Assignment | `.venv/bin/python -m pytest spec/tracker/test_assignment.py` with test environment |
| Filters | `.venv/bin/python -m pytest spec/tracker/test_filters.py` with test environment |
| Frontend slices | `npm run build`, working directory `issuetrackerweb` |
| Final backend | `.venv/bin/python -m pytest spec` with test environment |

Use M7's isolated test block, replacing the pytest target for a focused check.
PowerShell uses `& ./.venv/Scripts/python.exe` and `npm.cmd`. Do not run these test
commands in the development terminal without setting the test database first.
The named tracker test files are target deliverables, not baseline files.

### M10. Browser acceptance and shutdown without helper scripts

After implementing the frontend and its acceptance tests, install the browser test
dependency directly. **Working directory: `issuetrackerweb`.**

```bash
npm install --save-dev --save-exact @playwright/test@1.64.1
npm pkg set 'scripts.test:e2e=playwright test'
npx playwright install chromium
```

```powershell
npm.cmd install --save-dev --save-exact @playwright/test@1.64.1
npm.cmd pkg set 'scripts.test:e2e=playwright test'
npx.cmd playwright install chromium
```

If Linux reports missing browser system libraries, follow Playwright's diagnostic
and use `npx playwright install --with-deps chromium` on an appropriate machine.
Review and commit the resulting package/lock changes as part of the test milestone.

Create **`issuetrackerweb/playwright.config.js`**:

```javascript
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './e2e',
  workers: 1,
  use: {
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:8000',
    trace: 'retain-on-failure',
  },
  reporter: 'list',
});
```

This config does not start servers or create tests. Use this **Claude prompt**:

```text
Implement browser acceptance tests under issuetrackerweb/e2e against the running
local API and SQLite, not mocked API responses. Read the specification's browser
demonstration. Cover login, category/issue creation, assignment and clearing, edits,
reload persistence, combined filters and reset, deletion conflict/confirmation,
empty results and network-error feedback. Use unique test data and clean up only
records created by the tests. Read E2E_API_URL with localhost:3000 as its default.
Do not modify environment files or claim tests ran until executed. Keep the
Playwright worker count at one. Provide direct commands and evidence.
```

Run the API and frontend as in M6; seed the implemented categories first if needed.
Check `http://localhost:3000/docs` and the browser login manually rather than using
a readiness wrapper. E2E exercises the **local development** database because that
is what the running API uses; never point it at shared or production data.

**Working directory: `issuetrackerweb`, verification terminal:**

```bash
E2E_BASE_URL=http://localhost:8000 E2E_API_URL=http://localhost:3000 npm run test:e2e
```

```powershell
$env:E2E_BASE_URL = 'http://localhost:8000'
$env:E2E_API_URL = 'http://localhost:3000'
npm.cmd run test:e2e
```

Ask `acceptance-reviewer` to inspect the final evidence and gaps, then perform the
specification's browser demonstration yourself. Save a final handoff with both
Git revisions/dirty states and outcomes. Review traces before sharing: they can
contain application session data.

Stop API/frontend with Ctrl+C in their terminals. There is no database service
to stop. Preserve `storage/development.sqlite3` to retain data across sessions;
never delete it as routine cleanup. To reset a test run, first stop all users of
the disposable test file and confirm its exact path before deleting only that file.
At the end, students should be able to explain each direct command and reproduce
this layout without the workshop launcher or installer.

**Instructor gate:** baseline startup/test/build, real subagent invocation and
review, each implementation gate, final browser acceptance, and saved evidence.
See VALIDATION.md for which parts of this manual route have actually been rehearsed.


## 2. Instructor rehearsal and opening demonstration

### Rehearse the completed reference before class

The completed source is in `instructor-reference/`. Open that directory as the
active project root for this rehearsal. Follow M4–M7 with these deliberate changes:

- The two app directories already exist: do not clone or apply baseline patches.
- Install their lockfiles as in M5. Preserve any existing `.venv` for the correct OS.
- If `.env` already exists, do not run the exclusive-create command. A human should
  set its database URL to `sqlite:///storage/development.sqlite3`, preserving its
  other settings and signing key. A SQLite file starts independently of PostgreSQL;
  changing the URL does not migrate existing server data.
- Set frontend `.env` to `API_BASE_URL=http://localhost:3001`, `API_VERSION=v1`,
  `WEB_PORT=8001`, and the same browser-storage keys shown in M5.
- Start the API with M6's Uvicorn command using `--port 3001`.
- After Alembic, run both `app.cli system:seed` and `app.seed_tracker` because this
  source already includes the completed tracker. Seed categories twice.
- Run M7 with the explicit SQLite test URL, then M10 with E2E URLs on 8001/3001.
  Playwright and its configuration/tests already exist here; install Chromium,
  but do not overwrite these files or regenerate the tests.

Use the complete backend suite, build and browser demo as rehearsal gates. The
PostgreSQL-only migration test skips on SQLite; record the skip and perform the
SQLite migration-preservation exercise below rather than counting a skip as a pass.
Historical results appear in [VALIDATION.md](VALIDATION.md); rerun the chosen backend
before class. Live Claude/hook checks remain separate from application checks.

### Opening browser script

Open `http://localhost:8001/#/login` and sign in with the local demo account
`admin@example.com` / `password`. Keep the API docs at `http://localhost:3001/docs`
for later discussion.

1. Open Categories and create `Instructor demo`.
2. Open Issues and create `Login error during instructor demo`, with that category.
3. Assign the existing demo user and save.
4. Edit status to `in_progress` and priority to `high`; reload to demonstrate persistence.
5. Search by the title and apply both filters. Reset the filters afterward.
6. Try deleting the category while the issue uses it. Show the conflict message.
7. Open the issue, clear its assignment, save, and reload.
8. Start deleting the issue and cancel once; then confirm deletion.
9. Delete the now-unused demo category.

**Instructor says:**

> Every visible behavior crosses several boundaries: browser state, authenticated
> HTTP requests, validation, persistence, and database constraints. We will build
> these boundaries in small slices and prove them separately.

Ask learners which behaviors require server-side enforcement. Expected answers
include category uniqueness, foreign keys, allowed values and protected deletion.
A disabled frontend button alone cannot enforce those rules.

### Rehearse Claude separately

Open Claude at the active project root, inspect `/help`, `/memory`, and `/agents`, and
rehearse the named skill and reviewer prompts below. UI commands may vary by
installed version. Verify actual discovery and tool activity; do not promise a
specific shortcut without checking your installed CLI.

Record any live exercises you did not rehearse. The earlier validation did not
establish live VS Code behavior, custom subagent execution, plugin execution or
PostToolUse activation on every instructor machine.

## 3. Module 1: project setup and trustworthy context

Student route: [Module 1](01-project-setup/README.md).
Supporting lessons: [project structure](01-project-setup/01_PROJECT_STRUCTURE.md)
and [Claude context setup](01-project-setup/01_CLAUDE_SETUP.md).

### Teach the workspace boundary

Display root `AGENTS.md`, `CLAUDE.md`, and `AGENTS.md`. Explain that the
student apps are independent repositories generated at the root. The completed
reference lives elsewhere and is not the student's working implementation.

**Instructor says:**

> AGENTS.md holds shared engineering guidance. CLAUDE.md is our Claude entry point
> and explicitly imports that shared guidance. We verify which instructions were
> loaded rather than assuming a filename is enough. The root instructions contain
> this project's SQLite paths and commands; custom skills can package procedures.

### Guided setup — terminal in the student workspace

Walk through M1–M8 in a fresh manual workspace. Students create the separate SQLite
file paths, instructions and reviewers themselves. Expected: pinned templates,
baseline migration, direct tests/build, and a real reviewer task. Seed the existing
admin at baseline; add the tracker category seed only in the data milestone.
No kit installer is needed. Keep the existing per-app instructions and review
baseline compatibility changes before committing.

After inspecting both diffs, make baseline commits in the independent app repos:

```bash
git -C issuetrackerapi diff
git -C issuetrackerweb diff
git -C issuetrackerapi add .
git -C issuetrackerapi diff --cached --stat
git -C issuetrackerapi commit -m "Establish workshop baseline"
git -C issuetrackerweb add .
git -C issuetrackerweb diff --cached --stat
git -C issuetrackerweb commit -m "Establish workshop baseline"
claude
```

**PowerShell 7.4+ (Windows):**

```powershell
git -C issuetrackerapi diff
git -C issuetrackerweb diff
git -C issuetrackerapi add .
git -C issuetrackerapi diff --cached --stat
git -C issuetrackerapi commit -m "Establish workshop baseline"
git -C issuetrackerweb add .
git -C issuetrackerweb diff --cached --stat
git -C issuetrackerweb commit -m "Establish workshop baseline"
claude
```

If Git requests identity, have learners configure their own name and email. Never
supply the instructor's identity for the whole class. A repeated commit may report
nothing to commit; inspect status rather than manufacturing a change.

### Guided context probe — inside Claude

```text
Read CLAUDE.md, AGENTS.md, and SOFTWARE_SPECIFICATIONS.md.
Read the instruction files in each application repository. Analyze the student
workspace without editing application source or reading environment/credential files.
Identify the purpose of each application, the existing User model and its ID type,
the API and web ports, and the SQLite file selected by the M7 test commands. Cite paths.
Save your analysis to workshop-output/milestones/setup/map.md. Mark unknowns explicitly.
```

Inspect the resulting file with students. It should identify the student apps,
string UUID IDs, existing authentication, and the dedicated test database. If it
analyzes the reference instead, correct the task scope before accepting its answer.

### Guided rule change and probe

Have students add this rule to root AGENTS.md using their editor:

```markdown
Before changing relationships, identify the migration, existing User data impact,
rollback implications, and a referential-integrity test. Run pytest directly from
issuetrackerapi with APP_ENV=test and DATABASE_URL=sqlite:///test.sqlite3.
Never point destructive fixtures at development data.
```

Restart Claude, inspect loaded instructions, and paste:

```text
Plan adding a required category relationship to an issue. Do not implement it.
Identify the instruction that governs schema changes, how existing User records
are preserved, and the exact safe test command. Explain what evidence is needed
before the change can be called complete.
```

Expected: migration review, user preservation and test isolation. A rule only
appearing in the file is not evidence that the model followed it.

### Permissions demonstration

Follow the [permissions fixture exercise](01-project-setup/01_PROJECT_STRUCTURE.md).
Inspect the shared settings and use a dummy `.env` containing no real credentials.
Ask Claude to use only Read; observe the permission denial without trying another
tool. Contrast it with an allowed AGENTS.md read. Explain that these file-tool rules
are not an operating-system sandbox and do not cover every approved shell action.

### Independent exercise and debrief

Students add assignment rules to AGENTS.md and an evidence-table instruction to
CLAUDE.md, then test a fresh-session plan for assigning and clearing a user.
Use [the context lesson](01-project-setup/01_CLAUDE_SETUP.md) for the exact changes.

Ask: “What is guided by instructions, and what is enforced independently?”
Expected distinction: instructions shape behavior; permissions restrict tools;
database constraints and executable tests enforce application expectations.

**Exit gate:** baseline checks pass, the map cites real paths, loaded instructions
are observed, and students can explain the test/development database boundary.

## 4. Module 2: understand the application

Student route: [Module 2](02-application-fundamentals/README.md).

### Walk one request through the existing system

In terminal C:

```bash
sed -n '1,180p' issuetrackerapi/app/routes.py
sed -n '1,180p' issuetrackerapi/app/models/user.py
sed -n '1,180p' issuetrackerweb/src/js/services/UserService.js
sed -n '1,160p' issuetrackerweb/src/js/helpers/AppHelper.js
```

**PowerShell 7.4+ (Windows):**

```powershell
Get-Content issuetrackerapi/app/routes.py | Select-Object -First 180
Get-Content issuetrackerapi/app/models/user.py | Select-Object -First 180
Get-Content issuetrackerweb/src/js/services/UserService.js | Select-Object -First 180
Get-Content issuetrackerweb/src/js/helpers/AppHelper.js | Select-Object -First 160
```

Ask students to trace login → token/header → protected route → operation/session →
response → React state. Use file evidence when someone proposes a convention.
Do not teach a new architecture before examining the template's existing one.

**Inside Claude:**

```text
Map the existing login and users request flow in the student apps. Read their
AGENTS.md files. Identify actual paths for authentication, User identity, operations,
SQLAlchemy sessions, migrations, list response envelopes, axios headers and routing.
Explain why the tracker cannot simply expose the admin-only /users list to everyone.
Do not edit source or read .env. Save workshop-output/milestones/exploration/map.md with
source-backed facts and a separate list of unresolved assumptions.
```

Expected: `/users` remains admin-only; the tracker needs safe authenticated assignee
selection. The course uses separate SQLite development and test files. The frontend uses HashRouter, esbuild and the existing header helper.

### Fact-check with a bounded reviewer

```text
Use acceptance-reviewer to fact-check workshop-output/milestones/exploration/map.md against
SOFTWARE_SPECIFICATIONS.md, AGENTS.md, issuetrackerapi and issuetrackerweb.
Give it those paths explicitly. Focus on User ID type, authentication, pagination
and database configuration. Request discrepancies with source evidence, without
edits or command execution. Main session: save its returned report to
workshop-output/milestones/exploration/review.md and identify which claims need correction.
```

Show the named task and file reads. If the reviewer was not actually invoked,
record that and fix discovery; do not accept a main-session answer impersonating
a delegated review. The main session saves the report because this reviewer is
read-only. Detailed supervision is taught in Module 3.

### Independent exercise

Have students map a user update, then describe the Issue PATCH behavior they will
need: omitted fields are preserved; explicit null clears a nullable assignee.
They should also add a frontend scoped rule requiring labels, loading/error/empty
states and existing authentication headers, following the module walkthrough.

Debrief with “Which fact surprised you, and which proposed change did it prevent?”
Look for examples grounded in source rather than preference.

**Exit gate:** a verified application map and reviewer corrections, with no invented
endpoint conventions, duplicate User model, or undocumented authentication rewrite.

## 5. Module 3: reusable skills and supervised subagents

Student route: [Module 3](03-ai-development-workflow/README.md).
Optional reference: [manual instruction examples](workflow-kit/README.md). M3/M8
show how to create and test the instructions and reviewers yourself.

### Explain the division of responsibilities

| Mechanism | Teaching purpose | Evidence of correct use |
|---|---|---|
| Project instructions | Stable constraints and context | Fresh-session behavior probe |
| Scoped rules | Guidance for matching files | Relevant rule applied to a bounded task |
| Plan Mode | Inspect and propose before implementation | Accepted plan naming files and checks |
| Skill | Repeated procedure with task arguments | Discovered invocation and useful output |
| Subagent | Separate, bounded review context | Named task, inspected inputs and findings |
| Hook | Deterministic event feedback | Isolated tests plus observed live activation |
| CI | Repeatable automated gates | Actual job results for the relevant revision |

### Demonstrate planning

Enter Plan Mode using the installed CLI's supported controls. Inside Claude:

```text
Plan milestone 01-data using SQLite and direct commands. Add Category and Issue models, migrations and an idempotent category seed only. Use SOFTWARE_SPECIFICATIONS.md and workshop-output/milestones/exploration/map.md. Reuse the existing User model. Identify concrete source paths, integrity constraints, migration risks and test commands. Do not implement endpoints or frontend code.
```

Discuss the plan before leaving Plan Mode. Check that it addresses case-insensitive
category uniqueness, category deletion protection, nullable user assignment,
existing user preservation, and verification. After accepting it and leaving Plan
Mode, paste:

```text
Save the accepted data-only plan to workshop-output/milestones/01-data/plan.md. Do not
implement it yet. Preserve the acceptance criteria and exact verification commands.
```

### Create and invoke a skill — terminal

Use an unused skill directory for the classroom exercise. If this example already
exists from a rehearsal, inspect it instead of overwriting student work.

```bash
mkdir -p .claude/skills/review-contract
cat > .claude/skills/review-contract/SKILL.md <<'SKILL'
---
name: review-contract
description: Compare a requested API change with the project contract and existing source.
disable-model-invocation: true
---
Read AGENTS.md and SOFTWARE_SPECIFICATIONS.md. Review $ARGUMENTS.
Inspect relevant schemas, controllers, operations and tests. Do not edit source.
Return a table: requirement, implementation path, test path, missing evidence,
and recommendation. Do not claim tests passed without supplied execution evidence.
SKILL
```

**PowerShell 7.4+ (Windows):**

```powershell
New-Item -ItemType Directory -Force -Path '.claude/skills/review-contract' | Out-Null
@'
---
name: review-contract
description: Compare a requested API change with the project contract and existing source.
disable-model-invocation: true
---
Read AGENTS.md and SOFTWARE_SPECIFICATIONS.md. Review $ARGUMENTS.
Inspect relevant schemas, controllers, operations and tests. Do not edit source.
Return a table: requirement, implementation path, test path, missing evidence,
and recommendation. Do not claim tests passed without supplied execution evidence.
'@ | Set-Content -Encoding utf8 .claude/skills/review-contract/SKILL.md
```

Explain the quoted heredoc: Bash preserves `$ARGUMENTS` for Claude to substitute
later. Restart Claude and inspect skill discovery. Inside Claude:

```text
/review-contract Category deletion when issues reference it
```

Before implementation, expect a gap report. Repeat after Module 4 and compare it
with the actual source and tests. A skill produces model-guided work; it is not
itself a deterministic test program.

**Independent:** students create `review-ui-state`, invoke it on the issue-form
plan, and later repeat it against the implementation. Require one deliberately
incomplete example to check whether it finds missing evidence.

### Create a specialized reviewer — terminal

Display the acceptance-reviewer definition created in M8. To demonstrate another
role, create this accessibility-focused reviewer under a new name:

```bash
mkdir -p .claude/agents
cat > .claude/agents/ui-accessibility-reviewer.md <<'AGENT'
---
name: ui-accessibility-reviewer
description: Read-only review of Issue Tracker accessible UI states.
tools: Read, Glob, Grep
---
Read AGENTS.md, the supplied plan and frontend paths.
Check visible labels, loading/error/empty states, authenticated API calls,
assignment clearing, filter reset, persistence and delete confirmation.
Do not edit files or run commands. Report verdict, findings with paths, missing
execution evidence and suggested tests. If input files are missing, say so.
AGENT
```

**PowerShell 7.4+ (Windows):**

```powershell
New-Item -ItemType Directory -Force -Path '.claude/agents' | Out-Null
@'
---
name: ui-accessibility-reviewer
description: Read-only review of Issue Tracker accessible UI states.
tools: Read, Glob, Grep
---
Read AGENTS.md, the supplied plan and frontend paths.
Check visible labels, loading/error/empty states, authenticated API calls,
assignment clearing, filter reset, persistence and delete confirmation.
Do not edit files or run commands. Report verdict, findings with paths, missing
execution evidence and suggested tests. If input files are missing, say so.
'@ | Set-Content -Encoding utf8 .claude/agents/ui-accessibility-reviewer.md
```

Restart and check `/agents`. Explain that omitting Bash/Edit/Write is intentional:
the reviewer inspects evidence while the main session owns execution and changes.

**Inside Claude — review the data plan:**

```text
Use acceptance-reviewer to review workshop-output/milestones/01-data/plan.md. Supply
SOFTWARE_SPECIFICATIONS.md, workshop-output/milestones/exploration/map.md and issuetrackerapi
as explicit inputs. Ask for verdict, severity, source paths, integrity risks and
missing tests. Do not implement. Main session: save the returned review to
workshop-output/milestones/01-data/review.md and list decisions I need to resolve.
```

### How to supervise the actual task

1. Confirm a task for the named agent was created.
2. Expand its tool activity. Check whether it reads the assigned inputs.
3. For background tasks, inspect `/tasks` if supported in the installed CLI.
4. Use the UI stop control if the task leaves scope; give a corrected, narrower task.
5. Read the returned findings before accepting the verdict.
6. Have the main session save the report and reproduce actionable findings.

Use this status prompt when students cannot explain what their agent is doing:

```text
Report the actual delegated task name and status, input paths supplied, work
observed so far, output location, and any missing information. Distinguish running,
completed, failed and not invoked. Do not infer completion from a partial summary.
```

A separate context needs explicit inputs. Do not assume the reviewer knows every
conversation decision. Start with one writer and one reviewer; optional parallel
reviews can inspect separate scopes, but multiple writers need deliberate file
and database isolation.

**Independent:** give the reviewer a copy of a map with an incorrect port or an
unsupported pagination claim. Ask students whether it detects the error and what
source proves the correction. Do not corrupt real configuration for this exercise.

### Demonstrate a handoff

```text
Write workshop-output/milestones/01-data/handoff.md with the accepted plan, completed work,
actual commands and exit codes, remaining findings, and the next smallest task.
Separate tested facts from assumptions and omit credentials. Do not implement more.
```

Start a fresh Claude session and paste:

```text
Read workshop-output/milestones/01-data/handoff.md and workshop-output/milestones/01-data/plan.md.
Check their claims against the current source. Summarize the current state and
next bounded task; report stale assumptions before making changes.
```

**Exit gate:** accepted plan, saved review and a handoff; if taking the optional
skill lesson, also demonstrate the student-created skill
that another session can use. Optional packaging/worktree exercises are in
[Module 3 extensions](03-ai-development-workflow/03_FEATURE_LABS.md).

### Token-efficiency demonstration — 20–30 minutes

Use the [canonical token-efficiency lab](03-ai-development-workflow/04_TOKEN_EFFICIENCY.md)
after students understand skills and handoffs. Instructor says: “We want verified
progress per session. Removing requirements or skipping tests can make a short
interaction more expensive to repair.”

1. Show `/context` and `/usage` where supported; distinguish context occupancy from
   accumulated usage and billing. Avoid projecting private account information.
2. Compare the lab's broad and targeted assignment prompts on the same source/model.
   Use read-only sessions; no deliberate unrestricted repository scan is needed.
3. Inspect file reads, evidence quality, corrections and actual usage differences.
4. Demonstrate saving a concise milestone handoff before compaction or a fresh session.
5. Discuss why a subagent may reduce main-session clutter while adding total usage.
6. Assign the frontend diagnosis variation and collect the lab's evidence table.

The lab contains the exact prompts. Do not announce a fixed savings percentage;
record cache/model/account differences and unavailable measurements. This is an
optional measured comparison, not permission to alter billing or model settings.
Assessment: the answer stays correct, scope is justified and required verification
is retained. The classroom comparison has not been executed merely by adding these
instructions to the guide.

## 6. Module 4: build verified increments

Use the following cycle for each increment. Instructor: demonstrate one bounded
change, assign the independent variation, then debrief using the acceptable and
inadequate outputs in [the recipes](CLAUDE_USE_CASES.md). This mirrors the
[student sequence](04-issue-tracker-implementation/README.md).

**Entry:** verified application map and accepted data plan. **Result:** complete
Issue Tracker. Use the [specification](SOFTWARE_SPECIFICATIONS.md) and
[workflow recipes](CLAUDE_USE_CASES.md). Read each app's AGENTS.md. Student apps
are the active workspace; consult the instructor solution only after an attempt.

### Required cycle for every increment

1. Invoke the planning prompt below in Plan Mode. Inspect source paths, scope and checks.
2. Accept the plan, leave Plan Mode, and explicitly ask Claude to save it to the
   milestone's `plan.md` without implementing yet. Saving alone is not approval.
3. Send the listed implementation request. It requires that explicit acceptance.
4. Run the terminal gate yourself, then the verification prompt and a bounded review.
5. Repair confirmed failures within accepted scope; rerun affected checks and save
   evidence/handoff. Review the diff before committing in the affected app repo.

Every milestone directory is `workshop-output/milestones/<id>/`. Preserve earlier
plans/reviews/logs. Record workspace, app revisions, dirty state and actual outcomes.
The [use-case guide](CLAUDE_USE_CASES.md) contains exact save, review and repair
patterns. The commands below are **inside Claude** unless marked Bash or PowerShell.

### 1. Data — 01-data

```text
Plan milestone 01-data using SQLite and direct commands. Inspect issuetrackerapi and plan only the persistence slice: Category and Issue, existing string UUID User references, case-insensitive uniqueness, category RESTRICT/user SET NULL, status/priority constraints, UTC timestamps, migration and idempotent category seed. Preserve users. Identify integrity and migration checks before implementation.
```

Accept/save to `workshop-output/milestones/01-data/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/01-data/plan.md. Implement only milestone 01-data using SQLite and direct commands, and record actual verification evidence.
```

**Bash:**

```bash
(cd issuetrackerapi && APP_ENV=development DATABASE_URL=sqlite:///storage/development.sqlite3 .venv/bin/python -m alembic upgrade head)
(cd issuetrackerapi && APP_ENV=development DATABASE_URL=sqlite:///storage/development.sqlite3 .venv/bin/python -m app.seed_tracker)
(cd issuetrackerapi && APP_ENV=development DATABASE_URL=sqlite:///storage/development.sqlite3 .venv/bin/python -m app.seed_tracker)
(cd issuetrackerapi && APP_ENV=test DATABASE_URL=sqlite:///test.sqlite3 .venv/bin/python -m pytest spec)
```

**PowerShell 7.4+ (Windows):**

```powershell
& {
    Push-Location issuetrackerapi
    $prior_app_env = $env:APP_ENV
    $prior_database_url = $env:DATABASE_URL
    try {
        $env:APP_ENV = 'development'
        $env:DATABASE_URL = 'sqlite:///storage/development.sqlite3'
        & ./.venv/Scripts/python.exe -m alembic upgrade head
    } finally {
        $env:APP_ENV = $prior_app_env
        $env:DATABASE_URL = $prior_database_url
        Pop-Location
    }
}
& {
    Push-Location issuetrackerapi
    $prior_app_env = $env:APP_ENV
    $prior_database_url = $env:DATABASE_URL
    try {
        $env:APP_ENV = 'development'
        $env:DATABASE_URL = 'sqlite:///storage/development.sqlite3'
        & ./.venv/Scripts/python.exe -m app.seed_tracker
    } finally {
        $env:APP_ENV = $prior_app_env
        $env:DATABASE_URL = $prior_database_url
        Pop-Location
    }
}
& {
    Push-Location issuetrackerapi
    $prior_app_env = $env:APP_ENV
    $prior_database_url = $env:DATABASE_URL
    try {
        $env:APP_ENV = 'development'
        $env:DATABASE_URL = 'sqlite:///storage/development.sqlite3'
        & ./.venv/Scripts/python.exe -m app.seed_tracker
    } finally {
        $env:APP_ENV = $prior_app_env
        $env:DATABASE_URL = $prior_database_url
        Pop-Location
    }
}
& {
    Push-Location issuetrackerapi
    $prior_app_env = $env:APP_ENV
    $prior_database_url = $env:DATABASE_URL
    try {
        $env:APP_ENV = 'test'
        $env:DATABASE_URL = 'sqlite:///test.sqlite3'
        & ./.venv/Scripts/python.exe -m pytest spec
    } finally {
        $env:APP_ENV = $prior_app_env
        $env:DATABASE_URL = $prior_database_url
        Pop-Location
    }
}
```

Expected: existing users preserved; repeated category seed does not duplicate the
four sample categories. The local demo seed updates `admin@example.com` / `password`;
never target a real deployment. Independent: prove database uniqueness and user
preservation during migration. Recovery checkpoint: `01-data`.


After the applicable terminal/browser gate, verify inside Claude:

```text
Verify milestone 01-data against the accepted plan in workshop-output/milestones/01-data/plan.md using the SQLite test environment and direct commands. Verify the accepted increment and report criterion-level evidence.
```

### 2. Categories — 02-categories

```text
Plan milestone 02-categories using SQLite and direct commands. Inspect existing backend patterns and add authenticated category CRUD only. Trim/validate names, enforce case-insensitive uniqueness, paginate alphabetically and reject deletion of linked categories with 409. Add spec/tracker/test_categories.py. No issue endpoints or frontend changes.
```

Accept/save to `workshop-output/milestones/02-categories/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/02-categories/plan.md. Implement only milestone 02-categories using SQLite and direct commands, and record actual verification evidence.
```

**Bash:**

```bash
(cd issuetrackerapi && APP_ENV=test DATABASE_URL=sqlite:///test.sqlite3 .venv/bin/python -m pytest spec/tracker/test_categories.py)
```

**PowerShell 7.4+ (Windows):**

```powershell
& {
    Push-Location issuetrackerapi
    $prior_app_env = $env:APP_ENV
    $prior_database_url = $env:DATABASE_URL
    try {
        $env:APP_ENV = 'test'
        $env:DATABASE_URL = 'sqlite:///test.sqlite3'
        & ./.venv/Scripts/python.exe -m pytest spec/tracker/test_categories.py
    } finally {
        $env:APP_ENV = $prior_app_env
        $env:DATABASE_URL = $prior_database_url
        Pop-Location
    }
}
```

Expected: 201 create, 409 duplicate/protected deletion, 422 invalid input, 404 missing,
204 empty successful delete. Independent: duplicate rename and association preservation.
Recovery checkpoint: `02-categories`.


After the applicable terminal/browser gate, verify inside Claude:

```text
Verify milestone 02-categories against the accepted plan in workshop-output/milestones/02-categories/plan.md using the SQLite test environment and direct commands. Verify the accepted increment and report criterion-level evidence.
```

### 3. Issues — 03-issues

```text
Plan milestone 03-issues using SQLite and direct commands. Inspect Category/User integration and add authenticated issue CRUD. Validate title/description/status/priority and references; default open/medium. Preserve omitted PATCH fields and allow null only for nullable fields. Return safe display data. Add spec/tracker/test_issues.py. No UI changes.
```

Accept/save to `workshop-output/milestones/03-issues/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/03-issues/plan.md. Implement only milestone 03-issues using SQLite and direct commands, and record actual verification evidence.
```

**Bash:**

```bash
(cd issuetrackerapi && APP_ENV=test DATABASE_URL=sqlite:///test.sqlite3 .venv/bin/python -m pytest spec/tracker/test_issues.py)
```

**PowerShell 7.4+ (Windows):**

```powershell
& {
    Push-Location issuetrackerapi
    $prior_app_env = $env:APP_ENV
    $prior_database_url = $env:DATABASE_URL
    try {
        $env:APP_ENV = 'test'
        $env:DATABASE_URL = 'sqlite:///test.sqlite3'
        & ./.venv/Scripts/python.exe -m pytest spec/tracker/test_issues.py
    } finally {
        $env:APP_ENV = $prior_app_env
        $env:DATABASE_URL = $prior_database_url
        Pop-Location
    }
}
```

Independent: boundary lengths, whitespace-only title and unauthenticated writes.
Recovery checkpoint: `03-issues`.


After the applicable terminal/browser gate, verify inside Claude:

```text
Verify milestone 03-issues against the accepted plan in workshop-output/milestones/03-issues/plan.md using the SQLite test environment and direct commands. Verify the accepted increment and report criterion-level evidence.
```

### 4. Assignment — 04-assignment

```text
Plan milestone 04-assignment using SQLite and direct commands. Inspect current assignment behavior. Add authenticated read-only GET /assignees returning only ID/full_name for non-deleted existing users. Preserve admin-only /users. Test assign, omitted-field preservation, invalid reference, null clearing and ordinary-user access in spec/tracker/test_assignment.py.
```

Accept/save to `workshop-output/milestones/04-assignment/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/04-assignment/plan.md. Implement only milestone 04-assignment using SQLite and direct commands, and record actual verification evidence.
```

**Bash:**

```bash
(cd issuetrackerapi && APP_ENV=test DATABASE_URL=sqlite:///test.sqlite3 .venv/bin/python -m pytest spec/tracker/test_assignment.py)
```

**PowerShell 7.4+ (Windows):**

```powershell
& {
    Push-Location issuetrackerapi
    $prior_app_env = $env:APP_ENV
    $prior_database_url = $env:DATABASE_URL
    try {
        $env:APP_ENV = 'test'
        $env:DATABASE_URL = 'sqlite:///test.sqlite3'
        & ./.venv/Scripts/python.exe -m pytest spec/tracker/test_assignment.py
    } finally {
        $env:APP_ENV = $prior_app_env
        $env:DATABASE_URL = $prior_database_url
        Pop-Location
    }
}
```

Independent: verify ordinary-user assignee access without exposing /users or sensitive
fields. Complete the [assignment diagnosis](04-issue-tracker-implementation/03_DIAGNOSTIC_LAB.md). Recovery: `04-assignment`.


After the applicable terminal/browser gate, verify inside Claude:

```text
Verify milestone 04-assignment against the accepted plan in workshop-output/milestones/04-assignment/plan.md using the SQLite test environment and direct commands. Verify the accepted increment and report criterion-level evidence.
```

### 5. Filters — 05-filters

```text
Plan milestone 05-filters using SQLite and direct commands. Inspect issue listing and add literal case-insensitive title substring search plus AND-combined status, priority, category_id and assigned_user_id filters. Preserve pagination. Sort updated_at descending then ID. Test literal percent/underscore, no matches and equal-timestamp pagination in spec/tracker/test_filters.py.
```

Accept/save to `workshop-output/milestones/05-filters/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/05-filters/plan.md. Implement only milestone 05-filters using SQLite and direct commands, and record actual verification evidence.
```

**Bash:**

```bash
(cd issuetrackerapi && APP_ENV=test DATABASE_URL=sqlite:///test.sqlite3 .venv/bin/python -m pytest spec/tracker/test_filters.py)
```

**PowerShell 7.4+ (Windows):**

```powershell
& {
    Push-Location issuetrackerapi
    $prior_app_env = $env:APP_ENV
    $prior_database_url = $env:DATABASE_URL
    try {
        $env:APP_ENV = 'test'
        $env:DATABASE_URL = 'sqlite:///test.sqlite3'
        & ./.venv/Scripts/python.exe -m pytest spec/tracker/test_filters.py
    } finally {
        $env:APP_ENV = $prior_app_env
        $env:DATABASE_URL = $prior_database_url
        Pop-Location
    }
}
```

Independent: equal-timestamp paging without repetition or omission. Recovery: `05-filters`.

### 6. Frontend — four teaching increments

These four IDs organize evidence, **not recovery snapshots**. The existing
`06-frontend` checkpoint restores the completed UI only. Each prompt must produce
an accepted plan before the corresponding implementation invocation.


After the applicable terminal/browser gate, verify inside Claude:

```text
Verify milestone 05-filters against the accepted plan in workshop-output/milestones/05-filters/plan.md using the SQLite test environment and direct commands. Verify the accepted increment and report criterion-level evidence.
```

#### 06a-categories-ui: category management

```text
Plan milestone 06a-categories-ui using SQLite and direct commands. Inspect the existing React layout, routing and services. Add category navigation/list/create/edit/delete using real API calls and existing auth headers. Include labels, loading/error/empty states and protected-deletion feedback. Add exact Playwright dev dependency, configuration, test:e2e script and a focused category browser test. Do not build issue screens yet.
```

Accept/save to `workshop-output/milestones/06a-categories-ui/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/06a-categories-ui/plan.md. Implement only milestone 06a-categories-ui using SQLite and direct commands, and record actual verification evidence.
```

Observe create/edit/delete and validation feedback in the browser. Independent:
verify an API error is visible rather than rendered as an empty successful list.


After the applicable terminal/browser gate, verify inside Claude:

```text
Verify milestone 06a-categories-ui against the accepted plan in workshop-output/milestones/06a-categories-ui/plan.md using the SQLite test environment and direct commands. Verify the accepted increment and report criterion-level evidence.
```

#### 06b-issue-create-details: creation and persistence

```text
Plan milestone 06b-issue-create-details using SQLite and direct commands. Inspect the completed category UI. Add issue listing, creation and details using real endpoints. Fetch all category option pages and safe assignees. Include required labels, validation, loading/error/empty states. Extend browser tests to create an issue and verify details after reload. No editing/filtering/deletion yet.
```

Accept/save to `workshop-output/milestones/06b-issue-create-details/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/06b-issue-create-details/plan.md. Implement only milestone 06b-issue-create-details using SQLite and direct commands, and record actual verification evidence.
```

Observe creation through the form and persisted details after reload. Independent:
no categories available must produce useful guidance rather than an unusable save.


After the applicable terminal/browser gate, verify inside Claude:

```text
Verify milestone 06b-issue-create-details against the accepted plan in workshop-output/milestones/06b-issue-create-details/plan.md using the SQLite test environment and direct commands. Verify the accepted increment and report criterion-level evidence.
```

#### 06c-edit-assignment: updates and clearing

```text
Plan milestone 06c-edit-assignment using SQLite and direct commands. Add issue editing through existing services. Persist category, status, priority and assignee changes. Distinguish omitted fields from null clearing. Extend browser tests to edit/reload and unassign/reload. Keep authentication and existing pages intact.
```

Accept/save to `workshop-output/milestones/06c-edit-assignment/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/06c-edit-assignment/plan.md. Implement only milestone 06c-edit-assignment using SQLite and direct commands, and record actual verification evidence.
```

Observe changed fields after reload and an unassigned issue after explicit clearing.
Independent: reproduce a rejected API update and verify the UI explains it.


After the applicable terminal/browser gate, verify inside Claude:

```text
Verify milestone 06c-edit-assignment against the accepted plan in workshop-output/milestones/06c-edit-assignment/plan.md using the SQLite test environment and direct commands. Verify the accepted increment and report criterion-level evidence.
```

#### 06d-filters-deletion: discovery and confirmed removal

```text
Plan milestone 06d-filters-deletion using SQLite and direct commands. Add issue search, combined filters/reset, pagination and delete confirmation. Extend browser tests for matching/nonmatching results, reset, cancel and confirm deletion and category conflict feedback. Preserve existing issue/category behaviors and complete the specification's browser lifecycle.
```

Accept/save to `workshop-output/milestones/06d-filters-deletion/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/06d-filters-deletion/plan.md. Implement only milestone 06d-filters-deletion using SQLite and direct commands, and record actual verification evidence.
```

Observe filtered matches, reset, cancellation preserving an issue, and confirmed
removal. Independent: no matches and network error must remain distinct UI states.


After the applicable terminal/browser gate, verify inside Claude:

```text
Verify milestone 06d-filters-deletion against the accepted plan in workshop-output/milestones/06d-filters-deletion/plan.md using the SQLite test environment and direct commands. Verify the accepted increment and report criterion-level evidence.
```

#### Browser gates for each increment

Run the block for your shell after implementation:

```bash
(cd issuetrackerweb && npm run build)
(cd issuetrackerweb && npx playwright install chromium)
```

**PowerShell 7.4+ (Windows):**

```powershell
& { Push-Location issuetrackerweb; try { npm.cmd run build } finally { Pop-Location } }
Push-Location issuetrackerweb
try { npx.cmd playwright install chromium } finally { Pop-Location }
```

Start API and web in separate root terminals and keep them running:

```bash
(cd issuetrackerapi && APP_ENV=development DATABASE_URL=sqlite:///storage/development.sqlite3 .venv/bin/python -m uvicorn app:create_app --factory --host 127.0.0.1 --port 3000)
```

**PowerShell 7.4+ (Windows):**

```powershell
& {
    Push-Location issuetrackerapi
    $prior_app_env = $env:APP_ENV
    $prior_database_url = $env:DATABASE_URL
    try {
        $env:APP_ENV = 'development'
        $env:DATABASE_URL = 'sqlite:///storage/development.sqlite3'
        & ./.venv/Scripts/python.exe -m uvicorn app:create_app --factory --host 127.0.0.1 --port 3000
    } finally {
        $env:APP_ENV = $prior_app_env
        $env:DATABASE_URL = $prior_database_url
        Pop-Location
    }
}
```

```bash
(cd issuetrackerweb && npm start)
```

**PowerShell 7.4+ (Windows):**

```powershell
& { Push-Location issuetrackerweb; try { npm.cmd start } finally { Pop-Location } }
```

In a third terminal:

```bash
(cd issuetrackerweb && npm run test:e2e)
```

**PowerShell 7.4+ (Windows):**

```powershell
& { Push-Location issuetrackerweb; try { npm.cmd run test:e2e } finally { Pop-Location } }
```

Use `http://localhost:8000/#/login` with the local demo account. Each increment adds
tests for implemented behavior only; do not run tests for future screens as a passing
gate. For missing Linux browser libraries, follow Playwright's system-dependency setup.
At the completed frontend milestone, run the M7 SQLite backend check and the full browser suite.

### Verification, review and repair example

For categories, invoke:

```text
Verify milestone 02-categories against the accepted plan in workshop-output/milestones/02-categories/plan.md using the SQLite test environment and direct commands. Category CRUD and integrity
```

Use the same pattern with the exact milestone ID/plan for every increment.

```text
Use acceptance-reviewer for milestone 02-categories. Supply its plan, specification,
issuetrackerapi and milestone evidence/logs. Request path-backed contract/auth/
integrity findings without edits or commands. Main session: save review.md in that
milestone, reproduce findings and classify each as confirmed, rejected with evidence
or needing more evidence. Do not inspect instructor-reference.
```

Use ui-accessibility-reviewer for frontend increments after creating it above. Monitor actual tasks and file reads; a
reviewer's verdict cannot replace terminal/browser results. For a confirmed defect,
use the bounded repair prompt in the [recipes](CLAUDE_USE_CASES.md). Preserve
failed-run evidence and append the repaired run. Review diffs and commit in the
affected app repository once the gate passes.

**Exit:** the complete real browser lifecycle works. Continue to
[Module 5](05-testing-debugging-and-demo/README.md).

Apply this workflow in the [diagnostic lab](04-issue-tracker-implementation/03_DIAGNOSTIC_LAB.md).

## 7. Module 5: verification, debugging, and handoff

Student route: [Module 5](05-testing-debugging-and-demo/README.md).

### Establish the final acceptance plan

Inside Claude, use `Plan milestone final using SQLite and direct commands. Verify the complete specification against
the active student application; plan checks only, with no new feature work.` Review
and accept that plan, leave Plan Mode, and save it to
`workshop-output/milestones/final/plan.md` before invoking final verification.

### Capture real evidence

With both student servers running, use terminal C:

```bash
mkdir -p workshop-output/milestones/final/logs
set -o pipefail
workshop_run_id=$(date -u +%Y%m%dT%H%M%SZ)
(cd issuetrackerapi && APP_ENV=test DATABASE_URL=sqlite:///test.sqlite3 .venv/bin/python -m pytest spec) 2>&1 | tee "workshop-output/milestones/final/logs/${workshop_run_id}-backend.log"
(cd issuetrackerweb && npm run build) 2>&1 | tee "workshop-output/milestones/final/logs/${workshop_run_id}-build.log"
(cd issuetrackerweb && npm run test:e2e) 2>&1 | tee "workshop-output/milestones/final/logs/${workshop_run_id}-browser.log"
git -C issuetrackerapi rev-parse HEAD
git -C issuetrackerweb rev-parse HEAD
git -C issuetrackerapi status --short
git -C issuetrackerweb status --short
```

**PowerShell 7.4+ (Windows):**

```powershell
New-Item -ItemType Directory -Force -Path 'workshop-output/milestones/final/logs' | Out-Null
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true
$workshop_run_id = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssfffffffZ")
& {
    Push-Location issuetrackerapi
    $prior_app_env = $env:APP_ENV
    $prior_database_url = $env:DATABASE_URL
    try {
        $env:APP_ENV = 'test'
        $env:DATABASE_URL = 'sqlite:///test.sqlite3'
        & ./.venv/Scripts/python.exe -m pytest spec
    } finally {
        $env:APP_ENV = $prior_app_env
        $env:DATABASE_URL = $prior_database_url
        Pop-Location
    }
} 2>&1 | Tee-Object -FilePath "workshop-output/milestones/final/logs/${workshop_run_id}-backend.log"
& { Push-Location issuetrackerweb; try { npm.cmd run build } finally { Pop-Location } } 2>&1 | Tee-Object -FilePath "workshop-output/milestones/final/logs/${workshop_run_id}-build.log"
& { Push-Location issuetrackerweb; try { npm.cmd run test:e2e } finally { Pop-Location } } 2>&1 | Tee-Object -FilePath "workshop-output/milestones/final/logs/${workshop_run_id}-browser.log"
git -C issuetrackerapi rev-parse HEAD
git -C issuetrackerweb rev-parse HEAD
git -C issuetrackerapi status --short
git -C issuetrackerweb status --short
```

Explain `pipefail`: a log file can exist even when the command failed. Record each
command's outcome before proceeding. Record both revision and dirty state; a commit
ID alone does not identify uncommitted code used by the test.

**Inside Claude:**

```text
Verify milestone final against the accepted plan in workshop-output/milestones/final/plan.md using the SQLite test environment and direct commands. Compare the completed student tracker against SOFTWARE_SPECIFICATIONS.md. Inspect the latest timestamped backend/build/browser logs in workshop-output/milestones/final/logs and the current source. Run required checks if evidence is stale. Produce a pass/fail/not-run table per acceptance criterion with paths and actual execution evidence. Identify gaps without claiming source inspection proves browser behavior.
```

### Teach regression debugging

Have students create a Git branch from a passing state. Using a small reversible
edit, remove omitted-field preservation from Issue PATCH. Run the assignment test
and observe a failure. Restore the implementation and rerun the focused check.
Use the [assignment reference](instructor-reference/issuetrackerapi/spec/tracker/test_assignment.py)
to discuss what the failing assertion means; do not simply copy the solution.

**Inside Claude:**

```text
Investigate the failing assignment regression. Read the test, implementation and
failure output. Explain the expected versus observed behavior and the smallest
plausible cause. Propose a minimal repair and verification command before editing.
Do not weaken assertions, skip the test or change the API contract to obtain a pass.
```

**Independent:** students reproduce a different defect, document its cause, and
show a regression that fails before the repair and passes afterward. Keep the
intentional defect out of the final working application.

### Demonstrate a hook with observable activation

Follow [the full hook lab](05-testing-debugging-and-demo/02_HOOKS_EXTENSION.md).
First run isolated fixtures:

Before running the hook commands, open a fresh terminal at the **downloaded course
root** and select the active workspace. These paths follow M2's default sibling
layout; substitute your actual active directory if you chose another name.

```bash
course_source=$(pwd)
cd ../issue-tracker-manual
```

```powershell
$course_source = (Get-Location).Path
Set-Location ../issue-tracker-manual
```

```bash
python3 "$course_source/05-testing-debugging-and-demo/examples/hooks/test_check_python_syntax.py"
mkdir -p .claude/hooks
cp -n "$course_source/05-testing-debugging-and-demo/examples/hooks/check_python_syntax.py" .claude/hooks/check_python_syntax.py
```

**PowerShell 7.4+ (Windows):**

```powershell
py -3.14 "$course_source/05-testing-debugging-and-demo/examples/hooks/test_check_python_syntax.py"
New-Item -ItemType Directory -Force -Path '.claude/hooks' | Out-Null
if (-not (Test-Path .claude/hooks/check_python_syntax.py)) { Copy-Item "$course_source/05-testing-debugging-and-demo/examples/hooks/check_python_syntax.py" .claude/hooks/check_python_syntax.py }
```

Open the [settings fragment](05-testing-debugging-and-demo/examples/hooks/settings.fragment.json).
Merge its PostToolUse entry into `.claude/settings.local.json` without replacing
other hooks or permissions. Restart Claude and inspect `/hooks`.

Choose an unused fixture filename; then paste inside Claude:

```text
Using only Write, create issuetrackerapi/workshop_syntax_fixture.py containing
value = 1. Do not import or execute it. Report the syntax hook's observed feedback.
```

Then:

```text
Using Edit or Write, change only issuetrackerapi/workshop_syntax_fixture.py to the
intentionally invalid Python text: def broken(:
Stop without repairing it. Report the hook's actual feedback and line number.
```

Then:

```text
Using Edit or Write, restore only issuetrackerapi/workshop_syntax_fixture.py to
value = 1. Report the observed hook feedback. Do not modify application files.
```

Expected: success, syntax failure, success. If the hook does not fire, diagnose
configuration instead of accepting the model's guess. Remove only the disposable
fixture afterward. Explain that PostToolUse happens after the edit; it neither
undoes the edit nor proves business behavior. Shell-based edits are not covered
by this particular Edit/Write matcher.

### Final reviewer and handoff

```text
Use acceptance-reviewer to compare the specification, accepted plan, completed source
and current verification logs. Ask for unmet criteria, stale evidence and remaining
risks. Do not edit. Save the report to workshop-output/milestones/final/review.md in the main
session. After findings are resolved, write workshop-output/milestones/final/handoff.md with
launch commands, ports, migration state, revisions/dirty state, actual check results,
known limitations and a reproducible browser demonstration. Omit credentials.
```

Show the [GitHub Actions workflow](.github/workflows/workshop.yml). It runs direct
SQLite setup, tests, build and browser checks without a Claude API key or classroom
launcher. A workflow file is not evidence of a successful remote run; inspect
GitHub's results for the relevant revision. Maintenance checks run separately.

**Optional extensions:** [headless review](05-testing-debugging-and-demo/03_FEATURE_LABS.md),
[plugins/worktrees](03-ai-development-workflow/03_FEATURE_LABS.md), and
[MCP/parallel review](04-issue-tracker-implementation/02_FEATURE_LABS.md).
They do not replace required application gates.

## 8. Recovery and classroom troubleshooting

### Recover without overwriting student work

Use recovery when a learner understands the failure but needs a known state to
continue. Require a short explanation of the recovered change and rerun its gate.
Never use `git reset --hard`, delete a student's folders, or apply cumulative
patches on top of one another as a classroom shortcut.

Stop student servers first. Repeat M2 in a **different, new sibling directory**
(e.g. `issue-tracker-recovery`) using the same pinned template commits. In the patch
commands replace `checkpoints/00-baseline/` with `checkpoints/06-frontend/` to recover
the completed source. Apply only that cumulative patch to each clean template;
never apply it on top of 00-baseline. Other checkpoint names are listed in the
[checkpoint table](checkpoints/README.md); use its names, not its launcher commands.

Repeat M3–M7 with fresh SQLite environment files/storage inside the new workspace.
For 01-data or later, run `app.seed_tracker` after migration; baseline has only
`system:seed`. Complete the direct test/build gates and M10's browser check if the
recovered milestone includes browser tests. Keep student data/source untouched.

Start Claude at the new recovery root and state:

```text
This recovery workspace is now active. Read its CLAUDE.md and app instructions.
Use SQLite development at issuetrackerapi/storage/development.sqlite3 and tests at
issuetrackerapi/test.sqlite3 in this workspace.
Use direct Python/npm commands with explicit working directories. Do not inspect
or edit the former student workspace. Compare the current source to the supplied
handoff and identify remaining acceptance gaps; do not assume recovery means passed.
```

### Troubleshooting table

| Symptom | First inspection | Instructor action |
|---|---|---|
| Wrong working directory | `pwd` / `Get-Location` | Start at the active root; enter the API directory for SQLite commands |
| SQLite cannot open database | API working directory and storage folder | Create storage as in M4; check directory permissions |
| Python/Node version mismatch | Interpreter `--version` and `node --version` | Use Python 3.14 and Node 24 |
| Database is locked | Competing API/test writers | Stop competing runs; use separate development/test files and one browser worker |
| Port already occupied | Running student/reference/recovery terminals | Stop the conflicting workspace; do not delete volumes |
| Setup preserves an old `.env` | File presence and intended workspace | Review locally without exposing values; setup intentionally does not overwrite |
| Migration/seed missing | Current checkpoint and command selector | Apply migration first; seed only after data slice exists |
| Login fails | Correct port and seeded workspace | Check local seed and API connectivity; Claude credentials are unrelated |
| Skill not discovered | File location, name, restart, `/help` | Verify project root and SKILL.md frontmatter |
| Reviewer never invoked | `/agents` and actual task activity | Restart after definition changes and delegate with explicit inputs |
| Reviewer says “passed” without logs | Its allowed tools and supplied evidence | Require missing checks to be marked not run |
| Unexpected database in tests | `APP_ENV`, selected URL and working directory | Use the isolated M7 block; never development.sqlite3 |
| Test isolation assertion fails | Selected workspace, URL and working directory | Use exactly sqlite:///test.sqlite3 from the API directory; do not weaken the assertion |
| Browser cannot launch | Chromium install and missing OS libraries | Complete browser installation before diagnosing UI code |
| Browser test fails after saving | Trace, API response, awaited navigation | Diagnose the actual behavior; do not add arbitrary sleeps as the first fix |
| Build passes but UI fails | Browser console and real API/network behavior | Run the browser gate; a bundle alone is insufficient |
| Hook fixture tests pass but no live feedback | Matcher, settings scope, restart | Observe real Write/Edit activation before calling it installed |
| Context becomes stale | Current plan, handoff and source | Save evidence and start a fresh session with explicit paths |

When a failure affects the whole class, pause the shared demo and reproduce it in
the reference. When it affects one learner, inspect their workspace and evidence
before modifying the common course instructions.

## 9. Assessment and closing

### Acceptance demonstration

Have each learner demonstrate the specification's workflow on their own application:
login, category creation, issue creation, assignment, status/priority edits,
combined filtering, persistence after reload, unassignment, deletion cancellation,
confirmed issue deletion, and category deletion protection. Require visible error
handling and at least one empty state.

### Suggested assessment rubric

Score each area 0 (missing), 1 (partially demonstrated) or 2 (demonstrated with evidence).
The scoring organizes feedback; it does not excuse a failed required application gate.

| Area | Full-credit evidence |
|---|---|
| Reproducibility | Another person can follow the setup and handoff |
| Context and planning | Correct imported guidance, bounded plan, source-backed map |
| Data/API correctness | Constraints, validation, authentication and regressions |
| UI integration | Real endpoints, persistence and required UI states |
| Claude engineering | Working custom skill, actual bounded reviewer and inspected findings |
| Verification | Current backend/build/browser results with honest limitations |
| Transferability | Generic kit adapted to a different project's real commands |

Do not pass a broken integration because its prompts are well written. Conversely,
ask learners with a working application to explain the evidence and workflow rather
than assessing only the final screenshot.

### Transfer exercise

```text
Review our workflow kit for reuse in another project. Identify which instructions
are generic and which facts belong in AGENTS.md. Propose replacements
for paths, runtime commands, test isolation, acceptance criteria and review scopes.
Do not copy Issue Tracker credentials or ports into the new project. Give a small
behavior probe and deterministic check to validate the adapted workflow.
```

Debrief: “What would you keep, change, and test first in your next project?”
Look for thoughtful adaptation rather than copying every setting unchanged.

### Shutdown

Stop API and frontend with Ctrl+C in their terminals. SQLite has no separate
service to stop. Preserve application source, handoffs and the development database.
Keep database files and journals out of commits; back up a development file only
after its writer is stopped (or use SQLite's backup API).

## 10. Preparing the course for GitHub

The top-level [.gitignore](.gitignore) separates distributable course material
from local work. Root-only `/issuetrackerapi/` and `/issuetrackerweb/` rules exclude
the generated student repositories while retaining identically named directories
under `instructor-reference/`. Removing the leading slash would hide the reference.

| Include in the course repository | Keep out of the course repository |
|---|---|
| Module docs, GUIDE, specification and original PDF | Local workshop logs, maps, plans and handoffs |
| Reference source and dependency lockfiles | Dependencies, virtual environments and caches |
| Checkpoint patches and launcher/tooling | Recovery copies and local template Git metadata |
| Shared `.claude` rules, agents, skills and settings | Machine-local Claude settings and CLAUDE.local.md |
| Workflow templates and CI configuration | Runtime `.env` files, databases and browser reports |

Reviewed `.env.example`, `.env.sample` and `.env.dist` templates remain eligible.
The explicit reference `.env.test` exception preserves the supplied non-production
test fixture. Do not put real credentials into these tracked examples. Ignore rules
do not inspect file contents and do not remove files already tracked by Git.

The instructor reference is ordinary source, not nested Git submodules. Student
application repositories are independent: their commits are not included by
committing the course repository. Publish those separately only if you intend to.

### Review before your own commit

The following are instructions for the person publishing the course; they are not
part of the student implementation lab. If the course directory is not yet a Git
repository, initialize it once:

```bash
git init
```

**PowerShell 7.4+ (Windows):**

```powershell
git init
```

Inspect status, ignore rules and documentation before staging:

```bash
git status --short --untracked-files=normal
python3 tools/check_docs.py
git check-ignore -v --no-index issuetrackerapi/.env instructor-reference/issuetrackerapi/.env
```

**PowerShell 7.4+ (Windows):**

```powershell
git status --short --untracked-files=normal
py -3.14 tools/check_docs.py
git check-ignore -v --no-index issuetrackerapi/.env instructor-reference/issuetrackerapi/.env
```

Expected: both runtime paths are ignored. Check the opposite case:

```bash
git check-ignore -v --no-index instructor-reference/issuetrackerapi/app/models/tracker.py instructor-reference/issuetrackerweb/package-lock.json
```

**PowerShell 7.4+ (Windows):**

```powershell
& {
    $PSNativeCommandUseErrorActionPreference = $false
    git check-ignore -v --no-index instructor-reference/issuetrackerapi/app/models/tracker.py instructor-reference/issuetrackerweb/package-lock.json
    if ($LASTEXITCODE -ne 1) { throw 'Expected source files to be eligible for tracking (exit 1).' }
}
```

Expected: no matching ignore rule and exit status 1 for these eligible source files.
For this Git command, that status is the intended result, not a failed application test.

After reviewing the files, stage and inspect locally:

```bash
git add --dry-run .
git add .
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git ls-files --stage | awk '$1 == "160000" { print }'
```

**PowerShell 7.4+ (Windows):**

```powershell
git add --dry-run .
git add .
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git ls-files --stage | Select-String '^160000 '
```

The final command should not list the instructor apps as Git links. If it does,
inspect nested repository metadata before proceeding; do not blindly delete it.
Review staged content as well as names for credentials or private notes. Verify
reference source, locks, shared Claude files, CI, checkpoints and the PDF are present.
Do not use `git add -f` to bypass exclusions as a shortcut.

When satisfied, make your own commit and configure the intended GitHub remote.
This guide does not prescribe an account or repository URL. After pushing, inspect
GitHub Actions results and rehearse from a fresh clone; local success does not prove
that every necessary file was committed or that remote CI passed.

## 11. Instructor reference map

| Need | Repository reference |
|---|---|
| Student entry point | [README](README.md) |
| Application acceptance criteria | [Specification](SOFTWARE_SPECIFICATIONS.md) |
| Shared repository guidance | [AGENTS](AGENTS.md), [Claude entry](CLAUDE.md), the SQLite project instructions in M3 |
| Account/VS Code preparation | [Terminal guide](CLAUDE_CODE_TERMINAL.md), [VS Code guide](CLAUDE_CODE_VSCODE_SETUP.md) |
| Required teaching sequence | [Module 1](01-project-setup/README.md), [Module 2](02-application-fundamentals/README.md), [Module 3](03-ai-development-workflow/README.md), [Module 4](04-issue-tracker-implementation/README.md), [Module 5](05-testing-debugging-and-demo/README.md) |
| Reusable configuration | [Manual instruction examples](workflow-kit/README.md), optional student-created skills in Module 3 |
| Completed application | [Reference launch guide](instructor-reference/README.md) |
| Known-state recovery | [Checkpoint guide](checkpoints/README.md) |
| SQLite commands | Manual track M4–M10 in this guide; historical maintenance tooling is not used for teaching |
| Hook implementation and fixtures | [Hook lab](05-testing-debugging-and-demo/02_HOOKS_EXTENSION.md) |
| Automation | [CI](.github/workflows/workshop.yml), [documentation checker](tools/check_docs.py) |
| Evidence and course design rationale | [Validation](VALIDATION.md), [review findings](WORKSHOP_REVIEW.md) |

For version-specific Claude behavior, use the official documentation linked from
the setup guides and Module 3, then verify the behavior in the installed client.
Keep instructor notes about changed behavior separate from untested assumptions.

## Diagnostic facilitation supplements

Choose the workflow using [the use-case table](CLAUDE_USE_CASES.md). Run a guided
scenario, inspect its expected output, then assign the independent variation:

- Module 1: [setup diagnosis](01-project-setup/DIAGNOSTIC_LAB.md).
- Module 2: [authorization investigation](02-application-fundamentals/DIAGNOSTIC_LAB.md).
- Module 3: [contradictions and failed delegation](03-ai-development-workflow/DIAGNOSTIC_LAB.md).
- Module 4: [assignment and UI diagnosis](04-issue-tracker-implementation/03_DIAGNOSTIC_LAB.md).
- Module 5: [browser evidence diagnosis](05-testing-debugging-and-demo/DIAGNOSTIC_LAB.md).

A correct no-change diagnosis is valuable: intended authorization behavior and a
stopped service do not require source repairs. For delegated tasks, inspect actual
agent identity, input paths, tool activity and report, then have the main session
reproduce findings. Require students to distinguish proposed tests from executed tests.
