# Module 5 — Prove completion and package the workflow

**Entry:** Module 4 integrated application. **Result:** reproducible checks,
regression evidence and a handoff another developer can use.

## 1. Plan final acceptance, then run the independent gates

Inside Claude:

```text
/workshop-plan final Plan verification of every specification criterion against the completed student application. Identify source, command and browser evidence needed. No new feature implementation.
```

Accept the plan, leave Plan Mode, and save it to
`workshop-output/milestones/final/plan.md` before final verification.


Keep API and frontend running in separate terminals. From the course root:

```bash
mkdir -p workshop-output/milestones/final/logs
set -o pipefail
workshop_run_id=$(date -u +%Y%m%dT%H%M%SZ)
./workshop test 2>&1 | tee "workshop-output/milestones/final/logs/${workshop_run_id}-backend.log"
./workshop build 2>&1 | tee "workshop-output/milestones/final/logs/${workshop_run_id}-build.log"
./workshop e2e 2>&1 | tee "workshop-output/milestones/final/logs/${workshop_run_id}-browser.log"
```

`pipefail` preserves a failed command when using tee. Never write “passed” just
because a log exists. Backend fixtures recreate tables in the dedicated `_test`
database; browser tests use the running local development app and create/delete
uniquely named demo records. Do not target real user data. Inspect the browser
trace if a test fails; a successful bundle does not prove the UI works.

**Claude guided exercise:**

```text
/workshop-verify final workshop-output/milestones/final/plan.md Compare the completed tracker with SOFTWARE_SPECIFICATIONS.md. Read the actual backend/build/browser logs in workshop-output/milestones/final/logs, inspect missing coverage, run required checks if stale, and record pass/fail/not-run per acceptance criterion. Do not claim live browser behavior from source inspection alone.
```

**Independent:** introduce a reversible defect in a branch (for example, omit
`exclude_unset=True` on issue PATCH). Run the assignment regression and observe
failure. Restore the correct behavior, rerun the focused check, and record the
cause. Never leave the deliberate defect in the working application.

## 2. Hooks are feedback, not a substitute for tests

A hook runs a configured command at a Claude lifecycle event. Our optional
PostToolUse hook checks Python syntax after Write/Edit. It does not undo the edit,
catch Bash-written files, validate business logic or replace permissions.
Follow [the hook lab](02_HOOKS_EXTENSION.md), including its isolated tests before
merging settings. Do not overwrite existing `.claude/settings.json`.

**Guided:** use the supplied malformed and valid Python fixtures in the hook test
suite. Verify failure feedback and success separately. **Independent:** add a test
for a path containing spaces and an edit outside the backend; explain why a syntax
checker cannot prove category integrity. Keep the hook fast and deterministic.

## 3. Independent review and task supervision

```text
Use workshop-reviewer to review SOFTWARE_SPECIFICATIONS.md against the completed
application and workshop-output/milestones/final/logs/*.log. Supply the exact source paths and
accepted plan. Ask for unmet criteria, missing evidence and risks, without edits.
Main session: save its report to workshop-output/milestones/final/review.md, classify each
finding, fix real defects, and rerun only the affected checks before final gates.
```

Watch the actual reviewer task and read its report. Ask it to distinguish an
unexecuted check from a failed check. **Independent:** give a reviewer a stale log
from before the latest edit and see whether it notices the missing evidence.
Record the code revision alongside future logs to make this check objective.

## 4. Repeatable delivery

The root `.github/workflows/workshop.yml` runs the instructor reference gates on
Linux with PostgreSQL and Chromium. For student repositories, adapt paths to your
layout and keep the same separation of test database and browser fixture data.
Never store Claude API keys in CI unless a separate, explicit AI job needs them;
these deterministic checks do not call Claude.

Create `workshop-output/milestones/final/handoff.md` with launch commands, ports, schema
revision, test results, known limitations and demo steps. Rehearse from a clean
checkpoint workspace, not a warm browser session alone.

**Independent capstone:** move the reusable kit into a small new project, replace
workflow/project.md with that project's real commands/constraints, create one
project-specific skill, and prove a read-only reviewer finds a seeded defect.
Explain what is generic and what must change. Do not carry Issue Tracker DB ports
or demo credentials into the new project by accident.

**Exit gate:** every specification criterion has executable evidence or an explicit
unmet status; all required gates pass; a peer can launch and demonstrate the app.
No production deployment is implied. Finish with the specification's browser demo.

Apply this workflow in the [diagnostic lab](DIAGNOSTIC_LAB.md).
