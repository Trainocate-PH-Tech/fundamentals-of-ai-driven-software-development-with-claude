# Setup failure: inspect before changing

Complete the relevant [module prerequisites](README.md). Use student apps only.
This lab teaches symptom → reproduction → hypotheses → discriminating check →
minimal repair → regression. Evidence belongs to milestone `setup-diagnosis`.

## Guided scenario

A learner reports `FileNotFoundError: alembic` after running a migration directly
from an unactivated shell. This is a supplied scenario, not a claim about the
current runner. Do not break your installation to reproduce it.

**Inside Claude:**

```text
Read tools/workshop.py and the backend CLI without editing. Given the supplied
missing-alembic error, compare wrong interpreter/PATH with a missing dependency.
Name a non-mutating check that distinguishes them. Explain how ./workshop db migrate
selects its environment. Do not reinstall packages or read .env. Save a diagnosis
under workshop-output/milestones/setup-diagnosis/.
```

## Expected evidence and verification

Expected: distinguish environment selection from dependency installation and cite
the runner's virtual-environment PATH. The main session can run `./workshop doctor`
and inspect installed tools without mutating application source. Only rerun an
actual migration after confirming its workspace and intended data target.

Save inputs, observed facts, unsupported hypotheses, command/exit-code evidence
and remaining gaps under `workshop-output/milestones/setup-diagnosis/`. Read-only agents
return findings; the main session saves files, runs commands and owns repairs.

## Independent task

Explain a wrong-working-directory error using source evidence and propose the next check.

Debrief: what evidence ruled out a plausible cause, and which change was unnecessary?
