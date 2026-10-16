# Shared engineering contract

Read workflow/project.md for paths and executable commands. Read the application
specification before design. Inspect existing patterns before introducing code.
Make a bounded plan, implement one slice, test, inspect the diff, then hand off.
Preserve existing authentication and user records. Never put credentials in
prompts, tracked files, logs, or browser code. Use environment configuration.
Do not perform destructive database operations against development data.
Tests use only the dedicated test database through the documented runner.
Instructions guide behavior; permissions, database constraints, and tests enforce it.
Report changed paths, actual commands and exit codes, evidence, and untested claims.
Do not claim an application is complete based on an agent's summary alone.

## Milestone evidence and Claude task selection

Separate observed baseline behavior from target requirements. Select the active
workspace explicitly; inspect reference/recovery source only when assigned.
Use milestone-specific plan, review, evidence and handoff files under
workshop-output/milestones/. Preserve earlier runs and record revision/dirty state.
Choose direct edits for trivial scoped work, planning for uncertain changes, and
bounded read-only delegation for independent questions. Main-session execution
and review findings are distinct evidence. See CLAUDE_USE_CASES.md in this course
for recipes; adapt that reference when transferring the kit to another project.
