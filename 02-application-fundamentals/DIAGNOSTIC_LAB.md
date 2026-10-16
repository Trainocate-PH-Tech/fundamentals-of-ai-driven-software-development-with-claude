# A 403 is not necessarily a bug

Complete the relevant [module prerequisites](README.md). Use student apps only.
This lab teaches symptom → reproduction → hypotheses → discriminating check →
minimal repair → regression. Evidence belongs to milestone `auth-investigation`.

## Guided scenario

The baseline /users endpoint rejects an authenticated ordinary user. Read the
existing auth tests and dependency before deciding whether a repair is appropriate.

**Inside Claude:**

```text
Use architecture-reviewer to trace GET /users in issuetrackerapi: route, auth dependency
and existing tests. Supply root/app instructions. Ask for source evidence explaining
an ordinary active user's 403. Main session: save the report under milestone
auth-investigation. Do not relax permissions or add endpoints during this task.
```

## Expected evidence and verification

Run `.venv/bin/python -m pytest spec/users/test_auth.py` from the API directory with `APP_ENV=test` and `DATABASE_URL=sqlite:///test.sqlite3` (PowerShell: `& ./.venv/Scripts/python.exe -m pytest spec/users/test_auth.py`) from the active project root and record its
actual output. Expected: identify intended admin-only behavior. The future safe
assignee selector is a separate target requirement, not an existing baseline fact.

Save inputs, observed facts, unsupported hypotheses, command/exit-code evidence
and remaining gaps under `workshop-output/milestones/auth-investigation/`. Read-only agents
return findings; the main session saves files, runs commands and owns repairs.

## Independent task

Compare missing authentication with insufficient authorization. State the expected response and test for each.

Debrief: what evidence ruled out a plausible cause, and which change was unnecessary?
