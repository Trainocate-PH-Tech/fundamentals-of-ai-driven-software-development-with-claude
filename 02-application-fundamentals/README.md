# Module 2 — Build an evidence-based application map

Windows users: follow [Windows setup](../WINDOWS_SETUP.md). Run commands from the active project root unless stated otherwise; choose Bash or PowerShell, not both. Prompts go inside Claude.

**Entry:** Module 1 baseline checks pass. **Result:** a verified request/data flow
and contract map; no feature implementation yet.

## 1. Trace one existing request

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

Trace login → browser token → API auth dependency → controller → operation →
SQLAlchemy session → response → React state. Existing User IDs are strings;
`/users` is admin-only. The tracker needs a small authenticated `/assignees`
endpoint returning only ID/display name. SQLite is explicit in this course; development and tests use separate files. UI navigation uses hash URLs.

**Claude prompt — guided:**

```text
Read both application AGENTS.md files. Map the existing login and users request
flow with concrete paths. Identify User ID type, active-user auth, operation pattern,
list envelope, DB configuration precedence, migration chain, axios headers and
HashRouter routes. Do not edit application code or read .env. Save a concise map
to workshop-output/milestones/exploration/map.md, marking every unverified assumption.
```

**Independent:** trace an update request and explain why the tracker uses PATCH
while upstream users use PUT. Show the exact `exclude_unset` behavior you will need
for null versus omitted assignee, without changing existing users.

## 2. Scoped rules and context budget

Create `.claude/rules/api-contract.md` in your active project using the editor
(create its parent folder if needed). Paste this complete file:

```markdown
---
paths:
  - "issuetrackerapi/**/*.py"
---
Use existing authentication dependencies and database sessions. Validate at the API
boundary and enforce uniqueness and relationships in the database. Add a regression
test for each repaired defect. Preserve omitted PATCH fields; distinguish null.
```

The paths frontmatter scopes backend guidance. Rules are persistent constraints;
optional skills package procedures. Keep verified findings in a short map rather
than repeatedly attaching whole repositories. Restart and inspect the loaded rule.

**Guided:** read your newly created rule and add a line requiring a direct database
uniqueness test for category names. Ask Claude to plan duplicate-category handling
and explain which rule applied. **Independent:** create a frontend rule scoped to
`issuetrackerweb/src/**/*.js`, requiring labelled controls, loading/error/empty
states and existing auth headers. Probe it with an issue form planning request.

## 3. Subagent fact-check and monitoring

```text
Use architecture-reviewer to trace and fact-check workshop-output/milestones/exploration/map.md. Give it
SOFTWARE_SPECIFICATIONS.md, workflow/project.md and both application paths. Focus
on User identity, authentication, pagination and database configuration. Return
path-backed discrepancies only. Main session: save the report to
workshop-output/milestones/exploration/review.md and correct the map after reading sources.
```

Watch the task's tool calls and compare the actual files read to the requested
scope. If it cannot find an input, stop and supply the correct path. Do not treat
another agent's answer as independent execution evidence.

**Independent:** ask a fresh review of only the frontend map. Give a narrow task
and compare token/context usage with the broad review using `/context` and `/usage`
where available. Record usefulness and missing evidence, not just elapsed time.

**Exit gate:** the map names real paths, distinguishes admin users from assignees,
and explains SQLite/test isolation. Run `.venv/bin/python -m pytest spec` from the API directory with `APP_ENV=test` and `DATABASE_URL=sqlite:///test.sqlite3` (PowerShell: `& ./.venv/Scripts/python.exe -m pytest spec`) if you changed any
executable configuration; purely factual map edits do not need another full run.
Next: [Module 3](../03-ai-development-workflow/README.md).

Apply this workflow in the [diagnostic lab](DIAGNOSTIC_LAB.md).
