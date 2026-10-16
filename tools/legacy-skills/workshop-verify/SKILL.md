---
name: workshop-verify
description: Verify a milestone against its plan and report actual evidence.
disable-model-invocation: true
---

Task arguments: $ARGUMENTS

Arguments must start with a milestone ID followed by the plan path and scope.
If required inputs are missing, ask without editing application code. Read the
profile, plan, current source and supplied evidence. In Plan Mode return a check
plan only. Otherwise run focused checks and required broader gates through the
runner, using the active workspace and dedicated test DB. Browser checks require
ready services and implemented tests; report missing prerequisites as not run.
Do not repair code during this skill. Record workspace, app revisions and dirty
state, exact command, working directory, exit code, result and limitations in
workshop-output/milestones/<milestone-id>/evidence.md and logs/. Preserve prior
results when adding new runs. Return pass/fail/not-run per criterion, with a minimal
repair proposal for failures. A source review is not execution evidence.
