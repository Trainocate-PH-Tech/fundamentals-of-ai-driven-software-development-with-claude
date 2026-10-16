---
name: verify-feature
description: Compare one accepted feature with source and actual execution evidence.
disable-model-invocation: true
---
For $ARGUMENTS, request the accepted plan, source paths and recent execution evidence
if missing. Inspect only that scope. Identify direct checks with working directories
and the isolated SQLite test environment. Run only authorized checks or ask the
human to supply their output. Report pass/fail/not-run by criterion with commands,
exit codes and gaps. Do not repair code or infer passing tests from source alone.
