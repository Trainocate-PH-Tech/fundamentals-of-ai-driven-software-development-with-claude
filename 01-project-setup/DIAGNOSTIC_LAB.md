# Setup failure: inspect before changing

Complete the relevant [module prerequisites](README.md). Use student apps only.
This lab teaches symptom → reproduction → hypotheses → discriminating check →
minimal repair → regression. Evidence belongs to milestone `setup-diagnosis`.

## Guided scenario

A learner reports `FileNotFoundError: alembic` after running a migration directly
from an unactivated shell. This is a supplied scenario, not a claim about the
current installation. Do not break your installation to reproduce it.

**Inside Claude:**

```text
Inspect the backend requirements, CLI and recorded interpreter path without
editing. Given the missing-alembic error, compare wrong interpreter/PATH with a
missing dependency. Propose a read-only check that distinguishes them. Explain how
invoking the venv Python with -m alembic chooses its installed package. Do not
reinstall packages or read .env. Save diagnosis under milestone setup-diagnosis.
```

## Expected evidence and verification

From issuetrackerapi, use `.venv/bin/python -m pip show alembic` and
`.venv/bin/python -m alembic --version`. PowerShell uses
`& ./.venv/Scripts/python.exe -m pip show alembic` and
`& ./.venv/Scripts/python.exe -m alembic --version`.
The version check must use the same interpreter intended for migration. Confirm
the API working directory and development SQLite target before running migration.

Save inputs, observed facts, unsupported hypotheses, command/exit-code evidence
and remaining gaps under `workshop-output/milestones/setup-diagnosis/`. Read-only agents
return findings; the main session saves files, runs commands and owns repairs.

## Independent task

Explain a wrong-working-directory error using source evidence and propose the next check.

Debrief: what evidence ruled out a plausible cause, and which change was unnecessary?
