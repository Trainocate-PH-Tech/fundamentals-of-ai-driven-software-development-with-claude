# Issue Tracker project profile

## Active workspace and observed baseline

Start Claude at the active project root: the parent of issuetrackerapi and
issuetrackerweb. It may be a separate manual workspace, not the downloaded course.
Read both app AGENTS.md files. The pinned baseline has User with string UUID IDs,
JWT login, admin-only /users, FastAPI/SQLAlchemy/Alembic, and React/Bootstrap/esbuild
with HashRouter. Python 3.14 and Node 24 are the course runtimes.

Do not inspect instructor-reference or another recovery/student workspace unless
explicitly assigned. Record the selected root and both app paths in every handoff.
Changing workspace means changing working directory, not passing a launcher flag.

## Target contract, not a completion claim

Read SOFTWARE_SPECIFICATIONS.md. Add only Category and Issue; reuse User/auth.
Build safe assignees, filtering and the UI. These are absent at baseline.
Omitted PATCH fields preserve values; explicit null clears a nullable assignee.
Expected errors include 422 validation, 404 missing references and 409 conflicts.
Inspect actual source before claiming a target behavior exists.

## Direct commands and SQLite

Use ordinary Claude requests, not course orchestration skills or launchers.
Run database/API commands from issuetrackerapi and frontend commands from
issuetrackerweb. Never read, print or rewrite environment files through AI tools.
The human configures the development environment; propose missing settings without
reading secrets. Confirm OS, shell, directory and interpreter before execution.

| Task | Bash/Linux or WSL | Native Windows PowerShell |
|---|---|---|
| Python executable in API | `.venv/bin/python` | `& ./.venv/Scripts/python.exe` |
| Migration in API | `.venv/bin/python -m alembic upgrade head` | `& ./.venv/Scripts/python.exe -m alembic upgrade head` |
| API server | `.venv/bin/python -m uvicorn app:create_app --factory --host 127.0.0.1 --port 3000` | `& ./.venv/Scripts/python.exe -m uvicorn app:create_app --factory --host 127.0.0.1 --port 3000` |
| Backend tests | `.venv/bin/python -m pytest spec` | `& ./.venv/Scripts/python.exe -m pytest spec` |
| Frontend | `npm start` | `npm.cmd start` |
| Build | `npm run build` | `npm.cmd run build` |
| Browser acceptance | `npm run test:e2e` | `npm.cmd run test:e2e` |

Before migrations/server/seed: APP_ENV=development and
DATABASE_URL=sqlite:///storage/development.sqlite3. Create storage before connecting.
Before pytest: APP_ENV=test and DATABASE_URL=sqlite:///test.sqlite3.
Use a subshell in Bash or save/restore both variables with try/finally in PowerShell.
Fixtures drop tables; never use the development file. Use the exact relative test
URL from the API directory to satisfy the existing isolation assertion.

After installing models/migrations, run the tracker seed with `-m app.seed_tracker`
twice to verify idempotence. Baseline only has `-m app.cli system:seed`; this resets
the local demo admin password. Never seed a real deployment.

Student API/web ports: 3000/8000. Instructor reference: 3001/8001, with frontend
API_BASE_URL and WEB_PORT adjusted by the human. Recovery uses its own SQLite files
and student ports; stop other servers before switching. SQLite has no daemon/DB port.
Never share .venv or node_modules between Windows and WSL.

## Evidence and ownership

Save plan.md, review.md, evidence.md, handoff.md and timestamped logs under
workshop-output/milestones/<milestone-id>/. Record app revisions, dirty state,
command, working directory, exit code and criterion-level outcome. Preserve prior runs.
Use setup/exploration, 01-data through 05-filters, 06a-categories-ui,
06b-issue-create-details, 06c-edit-assignment, 06d-filters-deletion and final.
Only the checkpoint catalog defines recovery names; evidence IDs need not be patches.

Reviewers use explicit input paths and return reports. The human or main session
runs commands, saves reports and verifies findings. A reviewer cannot claim tests
passed merely because test source exists. For another project, adapt this profile
before using its commands. Optional student-created skills are not prerequisites.
