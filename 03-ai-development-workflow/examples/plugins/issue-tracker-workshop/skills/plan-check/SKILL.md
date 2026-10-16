---
name: plan-check
description: Review a supplied Issue Tracker plan for missing acceptance criteria before implementation.
disable-model-invocation: true
---

Review this plan or plan path: $ARGUMENTS

Read the workshop-root SOFTWARE_SPECIFICATIONS.md and relevant instructions. If no plan is provided, ask for it and stop. Inspect only files needed to verify the plan's claims.

Return a table of requirement, planned change, evidence, and Covered / Gap / Unclear. Identify missing verification and dependencies. Distinguish files that exist from proposed files. Do not edit, execute setup, or implement the plan. End with the highest-priority unresolved question, or state that no gap was found within the reviewed scope. A plan review is not a passing application test.
