---
name: workshop-implement
description: Implement an explicitly accepted milestone plan and verify its behavior.
disable-model-invocation: true
---

Task arguments: $ARGUMENTS

Arguments must start with a milestone ID followed by the accepted plan path.
Read AGENTS.md, workflow/project.md, app instructions and that plan. If inputs,
workspace or explicit acceptance are missing, clarify without application edits.
If still in Plan Mode, return the implementation steps and explain that execution
requires leaving Plan Mode; do not bypass it. Check the plan against current source.
Implement only the accepted scope using existing patterns. Add meaningful behavior
tests and reproduce the intended failure where practical; distinguish setup failures
from behavior failures. Run focused checks using the safe runner. Repair confirmed
failures within scope; stop and explain when a fix requires a material scope change.
Do not weaken assertions, skip tests, modify secrets, or commit/push automatically.
Write evidence.md and handoff.md under workshop-output/milestones/<milestone-id>/,
including active workspace, revisions/dirty state, changed files, commands, exit
codes, criteria satisfied, unresolved findings and next task. Never fabricate results.
