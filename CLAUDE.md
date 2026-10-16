# Claude project entry point

@AGENTS.md
@workflow/project.md

Read the current task's acceptance criteria before editing. Use Plan Mode for
cross-cutting changes. Reviewers inspect files and return evidence; the main
session owns edits, commands, and verification. Do not assume a subagent shares
the conversation: supply the task, paths, plan, and acceptance criteria explicitly.

Use the active workspace and milestone from the task/profile. Keep observed baseline
facts separate from target requirements. Preserve milestone-specific artifacts;
do not use a generic current.md as the sole source of progress. For implementation,
require the explicitly accepted plan and use the bounded workshop-implement procedure.
For a trivial, clearly scoped edit, a direct edit plus focused check is sufficient.
