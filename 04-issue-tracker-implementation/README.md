# Module 4 — Implement bounded, verified changes

Windows users: follow [Windows setup](../WINDOWS_SETUP.md). Run commands from the active project root unless stated otherwise; choose Bash or PowerShell, not both. Prompts go inside Claude.

**Entry:** verified application map and accepted data plan. **Result:** complete
Issue Tracker. Use the [specification](../SOFTWARE_SPECIFICATIONS.md) and
[workflow recipes](../CLAUDE_USE_CASES.md). Read each app's AGENTS.md. Student apps
are the active workspace; consult the instructor solution only after an attempt.

**Optional after the `01-data` gate:** [Subagent exercises](../SUBAGENT_EXERCISE.md) covers sequential delegation for mock-data seeding and GET /issues. Complete the remaining module gates as usual.

## Required cycle for every increment

1. Invoke the planning prompt below in Plan Mode. Inspect source paths, scope and checks.
2. Accept the plan, leave Plan Mode, and explicitly ask Claude to save it to the
   milestone's `plan.md` without implementing yet. Saving alone is not approval.
3. Send the listed implementation request. It requires that explicit acceptance.
4. Run the terminal gate yourself, then the verification prompt and a bounded review.
5. Repair confirmed failures within accepted scope; rerun affected checks and save
   evidence/handoff. Review the diff before committing in the affected app repo.

Every milestone directory is `workshop-output/milestones/<id>/`. Preserve earlier
plans/reviews/logs. Record workspace, app revisions, dirty state and actual outcomes.
The [use-case guide](../CLAUDE_USE_CASES.md) contains exact save, review and repair
patterns. The commands below are **inside Claude** unless marked Bash.

## 1. Data — 01-data

```text
Plan milestone 01-data using SQLite and direct commands. Inspect issuetrackerapi and plan only the persistence slice: Category and Issue, existing string UUID User references, case-insensitive uniqueness, category RESTRICT/user SET NULL, status/priority constraints, UTC timestamps, migration and idempotent category seed. Preserve users. Identify integrity and migration checks before implementation.
```

Accept/save to `workshop-output/milestones/01-data/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/01-data/plan.md. Implement only milestone 01-data using direct commands and the SQLite test environment. Record actual verification evidence.
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


After the applicable Bash/browser gate, verify inside Claude:

```text
Verify milestone 01-data against the accepted plan in workshop-output/milestones/01-data/plan.md using direct commands and the SQLite test environment. Verify the accepted increment and report criterion-level evidence.
```

## 2. Categories — 02-categories

```text
Plan milestone 02-categories using SQLite and direct commands. Inspect existing backend patterns and add authenticated category CRUD only. Trim/validate names, enforce case-insensitive uniqueness, paginate alphabetically and reject deletion of linked categories with 409. Add spec/tracker/test_categories.py. No issue endpoints or frontend changes.
```

Accept/save to `workshop-output/milestones/02-categories/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/02-categories/plan.md. Implement only milestone 02-categories using direct commands and the SQLite test environment. Record actual verification evidence.
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


After the applicable Bash/browser gate, verify inside Claude:

```text
Verify milestone 02-categories against the accepted plan in workshop-output/milestones/02-categories/plan.md using direct commands and the SQLite test environment. Verify the accepted increment and report criterion-level evidence.
```

## 3. Issues — 03-issues

```text
Plan milestone 03-issues using SQLite and direct commands. Inspect Category/User integration and add authenticated issue CRUD. Validate title/description/status/priority and references; default open/medium. Preserve omitted PATCH fields and allow null only for nullable fields. Return safe display data. Add spec/tracker/test_issues.py. No UI changes.
```

Accept/save to `workshop-output/milestones/03-issues/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/03-issues/plan.md. Implement only milestone 03-issues using direct commands and the SQLite test environment. Record actual verification evidence.
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


After the applicable Bash/browser gate, verify inside Claude:

```text
Verify milestone 03-issues against the accepted plan in workshop-output/milestones/03-issues/plan.md using direct commands and the SQLite test environment. Verify the accepted increment and report criterion-level evidence.
```

## 4. Assignment — 04-assignment

```text
Plan milestone 04-assignment using SQLite and direct commands. Inspect current assignment behavior. Add authenticated read-only GET /assignees returning only ID/full_name for non-deleted existing users. Preserve admin-only /users. Test assign, omitted-field preservation, invalid reference, null clearing and ordinary-user access in spec/tracker/test_assignment.py.
```

Accept/save to `workshop-output/milestones/04-assignment/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/04-assignment/plan.md. Implement only milestone 04-assignment using direct commands and the SQLite test environment. Record actual verification evidence.
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
fields. Complete the [assignment diagnosis](03_DIAGNOSTIC_LAB.md). Recovery: `04-assignment`.


After the applicable Bash/browser gate, verify inside Claude:

```text
Verify milestone 04-assignment against the accepted plan in workshop-output/milestones/04-assignment/plan.md using direct commands and the SQLite test environment. Verify the accepted increment and report criterion-level evidence.
```

## 5. Filters — 05-filters

```text
Plan milestone 05-filters using SQLite and direct commands. Inspect issue listing and add literal case-insensitive title substring search plus AND-combined status, priority, category_id and assigned_user_id filters. Preserve pagination. Sort updated_at descending then ID. Test literal percent/underscore, no matches and equal-timestamp pagination in spec/tracker/test_filters.py.
```

Accept/save to `workshop-output/milestones/05-filters/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/05-filters/plan.md. Implement only milestone 05-filters using direct commands and the SQLite test environment. Record actual verification evidence.
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

## 6. Frontend — four teaching increments

These four IDs organize evidence, **not recovery snapshots**. The existing
`06-frontend` checkpoint restores the completed UI only. Each prompt must produce
an accepted plan before the corresponding implementation invocation.


After the applicable Bash/browser gate, verify inside Claude:

```text
Verify milestone 05-filters against the accepted plan in workshop-output/milestones/05-filters/plan.md using direct commands and the SQLite test environment. Verify the accepted increment and report criterion-level evidence.
```

### 06a-categories-ui: category management

```text
Plan milestone 06a-categories-ui using SQLite and direct commands. Inspect the existing React layout, routing and services. Add category navigation/list/create/edit/delete using real API calls and existing auth headers. Include labels, loading/error/empty states and protected-deletion feedback. Add exact Playwright dev dependency, configuration, test:e2e script and a focused category browser test. Do not build issue screens yet.
```

Accept/save to `workshop-output/milestones/06a-categories-ui/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/06a-categories-ui/plan.md. Implement only milestone 06a-categories-ui using direct commands and the SQLite test environment. Record actual verification evidence.
```

Observe create/edit/delete and validation feedback in the browser. Independent:
verify an API error is visible rather than rendered as an empty successful list.


After the applicable Bash/browser gate, verify inside Claude:

```text
Verify milestone 06a-categories-ui against the accepted plan in workshop-output/milestones/06a-categories-ui/plan.md using direct commands and the SQLite test environment. Verify the accepted increment and report criterion-level evidence.
```

### 06b-issue-create-details: creation and persistence

```text
Plan milestone 06b-issue-create-details using SQLite and direct commands. Inspect the completed category UI. Add issue listing, creation and details using real endpoints. Fetch all category option pages and safe assignees. Include required labels, validation, loading/error/empty states. Extend browser tests to create an issue and verify details after reload. No editing/filtering/deletion yet.
```

Accept/save to `workshop-output/milestones/06b-issue-create-details/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/06b-issue-create-details/plan.md. Implement only milestone 06b-issue-create-details using direct commands and the SQLite test environment. Record actual verification evidence.
```

Observe creation through the form and persisted details after reload. Independent:
no categories available must produce useful guidance rather than an unusable save.


After the applicable Bash/browser gate, verify inside Claude:

```text
Verify milestone 06b-issue-create-details against the accepted plan in workshop-output/milestones/06b-issue-create-details/plan.md using direct commands and the SQLite test environment. Verify the accepted increment and report criterion-level evidence.
```

### 06c-edit-assignment: updates and clearing

```text
Plan milestone 06c-edit-assignment using SQLite and direct commands. Add issue editing through existing services. Persist category, status, priority and assignee changes. Distinguish omitted fields from null clearing. Extend browser tests to edit/reload and unassign/reload. Keep authentication and existing pages intact.
```

Accept/save to `workshop-output/milestones/06c-edit-assignment/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/06c-edit-assignment/plan.md. Implement only milestone 06c-edit-assignment using direct commands and the SQLite test environment. Record actual verification evidence.
```

Observe changed fields after reload and an unassigned issue after explicit clearing.
Independent: reproduce a rejected API update and verify the UI explains it.


After the applicable Bash/browser gate, verify inside Claude:

```text
Verify milestone 06c-edit-assignment against the accepted plan in workshop-output/milestones/06c-edit-assignment/plan.md using direct commands and the SQLite test environment. Verify the accepted increment and report criterion-level evidence.
```

### 06d-filters-deletion: discovery and confirmed removal

```text
Plan milestone 06d-filters-deletion using SQLite and direct commands. Add issue search, combined filters/reset, pagination and delete confirmation. Extend browser tests for matching/nonmatching results, reset, cancel and confirm deletion and category conflict feedback. Preserve existing issue/category behaviors and complete the specification's browser lifecycle.
```

Accept/save to `workshop-output/milestones/06d-filters-deletion/plan.md`, then:

```text
I accept the plan in workshop-output/milestones/06d-filters-deletion/plan.md. Implement only milestone 06d-filters-deletion using direct commands and the SQLite test environment. Record actual verification evidence.
```

Observe filtered matches, reset, cancellation preserving an issue, and confirmed
removal. Independent: no matches and network error must remain distinct UI states.


After the applicable Bash/browser gate, verify inside Claude:

```text
Verify milestone 06d-filters-deletion against the accepted plan in workshop-output/milestones/06d-filters-deletion/plan.md using direct commands and the SQLite test environment. Verify the accepted increment and report criterion-level evidence.
```

### Browser gates for each increment

Run **Bash** after implementation:

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
At the completed frontend milestone, run `.venv/bin/python -m pytest spec` from the API directory with `APP_ENV=test` and `DATABASE_URL=sqlite:///test.sqlite3` (PowerShell: `& ./.venv/Scripts/python.exe -m pytest spec`) and the full browser suite.

## Verification, review and repair example

For categories, invoke:

```text
Verify milestone 02-categories against the accepted plan in workshop-output/milestones/02-categories/plan.md using direct commands and the SQLite test environment. Category CRUD and integrity
```

Use the same pattern with the exact milestone ID/plan for every increment.

```text
Use backend-reviewer for milestone 02-categories. Supply its plan, specification,
issuetrackerapi and milestone evidence/logs. Request path-backed contract/auth/
integrity findings without edits or commands. Main session: save review.md in that
milestone, reproduce findings and classify each as confirmed, rejected with evidence
or needing more evidence. Do not inspect instructor-reference.
```

Use ui-reviewer for frontend increments. Monitor actual tasks and file reads; a
reviewer's verdict cannot replace Bash/browser results. For a confirmed defect,
use the bounded repair prompt in the [recipes](../CLAUDE_USE_CASES.md). Preserve
failed-run evidence and append the repaired run. Review diffs and commit in the
affected app repository once the gate passes.

**Exit:** the complete real browser lifecycle works. Continue to
[Module 5](../05-testing-debugging-and-demo/README.md).

Apply this workflow in the [diagnostic lab](03_DIAGNOSTIC_LAB.md).
