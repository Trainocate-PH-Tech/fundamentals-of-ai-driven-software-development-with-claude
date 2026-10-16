# Reusable instruction examples — manual adoption

These files are reference material, not a required installation. Core exercises use
ordinary Claude messages and direct Python, npm, Git and Playwright commands.
The SQLite project profile records working directories, environment selection and
verification targets; replace those facts when transferring to another application.

## Adopt selected files yourself

Read template/AGENTS.md, template/CLAUDE.md and template/workflow/project.md in your
editor. Create corresponding files in a new project's root, preserving existing
instructions and merging deliberately. Copy only needed `.claude/agents/`, rules
and settings after review. Do not overwrite existing permissions or unrelated hooks.
The course [manual setup](../GUIDE.md#m3-write-the-root-instructions-yourself)
provides exact initial contents and shell instructions.

Restart Claude. Inspect `/memory` and actual file reads. Create/invoke the read-only
reviewers as shown in [the subagent exercise](../GUIDE.md#m8-create-and-invoke-subagents-yourself).
Additional definitions in template/.claude/agents are optional examples; create or
copy the chosen file before requesting its role by name. Subagents return reports;
the human or main session runs commands, owns changes and saves the evidence.

## Use ordinary requests

```text
Plan category CRUD in issuetrackerapi only. Read the project instructions,
specification and existing patterns. Name source/test paths, validation, integrity
constraints, risks and direct verification commands. Do not implement yet.
```

Review the plan, leave Plan Mode, save it, then explicitly accept its scope:

```text
I accept workshop-output/milestones/02-categories/plan.md. Implement only that scope.
Use direct commands and the documented isolated SQLite test environment. Preserve
unrelated work. Record actual commands, exit codes, skips and acceptance evidence.
```

After verification, ask a named reviewer for independent source-based findings.
Maintain plan.md, review.md, evidence.md, handoff.md and distinct logs per milestone.
A saved plan is not approval and a review is not test execution.

Optional skill lessons teach how students create their own procedures. They do not
provide a mandatory orchestration layer. Historical launcher/installer code remains
for maintenance only and is not part of the teaching path.
