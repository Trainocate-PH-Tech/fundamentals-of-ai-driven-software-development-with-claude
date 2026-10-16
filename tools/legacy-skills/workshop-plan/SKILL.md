---
name: workshop-plan
description: Plan a bounded milestone using source evidence.
disable-model-invocation: true
---

Task arguments: $ARGUMENTS

Read AGENTS.md, workflow/project.md and the specification. Arguments must start
with a milestone ID followed by a bounded task. If either is missing, ask for it;
do not edit application code. Inspect only the active workspace and relevant files.
Separate observed behavior, target requirements and proposed changes. Return paths,
acceptance criteria, ordered steps, risks and exact checks. In Plan Mode, return
the plan in conversation. Outside Plan Mode, save it under
workshop-output/milestones/<milestone-id>/plan.md. Do not implement. A saved plan
is not approval: wait for the user to explicitly accept its scope.
