# Optional packaging: commands, plugins, and worktrees

Complete [Module 3](README.md) first. Skills are the main reusable procedure in this
course. Legacy `.claude/commands/name.md` custom commands are supported, but do not
create a second command with the same name as a skill.

## Local plugin

A plugin packages related skills/agents/hooks for sharing. Inspect the supplied
`examples/plugins/issue-tracker-workshop/` manifest and plan-check skill before loading it. From course root:

```bash
claude --plugin-dir ./03-ai-development-workflow/examples/plugins/issue-tracker-workshop
```

**PowerShell 7.4+ (Windows):**

```powershell
claude --plugin-dir ./03-ai-development-workflow/examples/plugins/issue-tracker-workshop
```

Inside Claude, invoke the namespaced command:

```text
/issue-tracker-workshop:plan-check workshop-output/milestones/01-data/plan.md
```

Use `/help` to confirm discovery. Supply the saved category plan. Expected: review findings, no implementation. **Independent:** copy
the example into a new local directory, rename the plugin, and package your custom
contract skill. Verify discovery and ensure it does not shadow the installed skill.
Do not publish a plugin or install third-party code as part of this exercise.

## Worktree isolation

Worktrees give separate writing tasks separate files and branches. They do not
give separate database ports or credentials. The core course uses one writer and
read-only reviewers, so worktrees are optional.

**Guided:** after committing a clean API checkpoint, run:

```bash
git -C issuetrackerapi worktree add ../api-review-lab -b workshop/review-lab
git -C issuetrackerapi worktree list
```

**PowerShell 7.4+ (Windows):**

```powershell
git -C issuetrackerapi worktree add ../api-review-lab -b workshop/review-lab
git -C issuetrackerapi worktree list
```

Inspect the new directory; do not start a second server against the same development
database. **Independent:** make a documentation-only change there, review the diff,
and explain how you would isolate application databases before parallel writers.
Remove the worktree only after saving/discarding its changes deliberately.
