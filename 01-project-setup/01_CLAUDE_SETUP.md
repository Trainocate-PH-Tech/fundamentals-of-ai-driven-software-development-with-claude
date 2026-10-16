# Modify and test Claude's project context

Complete Module 1 installation first. Root CLAUDE.md imports AGENTS.md and the
project profile. For an Issue Tracker change, edit the **shared** AGENTS.md rule:

```markdown
Issue assignments must reference the existing User model. Add only Category and
Issue as domain models. A missing PATCH field preserves its value; explicit null
clears assigned_user_id. Include regression evidence for both cases.
```

Add this **Claude-specific** instruction to CLAUDE.md:

```markdown
For an assignment change, use acceptance-reviewer after implementation. Give it the
accepted plan, relevant source paths and test evidence. The main session saves the
report and resolves findings; the reviewer must not edit or run commands.
```

Restart `claude` from the active project root. Inspect `/memory` and `/agents`, then paste:

```text
Read the root and app instruction files. Plan assigning an issue to an existing
user and later clearing that assignment. Do not edit application code. Name the
model, endpoint, omitted-versus-null behavior, tests, and review handoff. Cite the
instruction that requires each. If anything is absent, report it rather than invent it.
```

Expected: reuse User; safe read-only assignee endpoint because `/users` is admin-only;
PATCH preserve/clear tests; named read-only reviewer with explicit inputs. Save
observed output to `workshop-output/milestones/final/logs/context.md` and compare with these
expectations. Repeat in a new session after simplifying an ambiguous rule.

**Independent:** add category deletion integrity rules to AGENTS.md and a compact
review output format to CLAUDE.md. Test a plan to delete an in-use category. Passing
means it proposes 409 and a database constraint test, not deletion of linked issues.

These probes validate behavior only for the exercised prompts. Database constraints,
permission controls and executable tests remain the enforcement layers.
