# Reusable engineering kit

Run `./workshop install-kit` at the course root. Missing files are installed,
identical files retained, and conflicts staged under `.workshop/proposed/` for
review. Existing student instructions and artifacts are never overwritten. Merge
intentional changes, restart Claude and inspect `/memory`, `/agents` and skill discovery.

The project profile separates verified baseline facts from target requirements.
It defaults to student apps; a reference or recovery task must explicitly select
its workspace. CLAUDE.md imports AGENTS.md and that profile.

Invoke skills **inside Claude**, not Bash:

```text
/workshop-plan 02-categories Implement authenticated category CRUD only.
```

Read and accept the returned plan. Leave Plan Mode, save it to
`workshop-output/milestones/02-categories/plan.md`, then explicitly authorize:

```text
I accept the scope in workshop-output/milestones/02-categories/plan.md.
```

Then send the skill invocation as its own message:

```text
/workshop-implement 02-categories workshop-output/milestones/02-categories/plan.md
```

A slash command should be submitted as its own message if the client does not
recognize it after other text. The acceptance sentence may be sent first.

```text
/workshop-verify 02-categories workshop-output/milestones/02-categories/plan.md Category CRUD and integrity
```

Each milestone stores plan.md, review.md, evidence.md, handoff.md and logs/.
Evidence includes workspace, app revisions, dirty state, commands, exit codes and
acceptance criteria. Preserve prior runs; add a dated run section or a new log name.
Never treat a saved plan as implicit approval. Missing required arguments prompt
clarification before application edits. Verification does not auto-repair failures.

Installed read-only roles: workspace-scout (request tracing), workshop-investigator
(one bug hypothesis), backend-reviewer (API/integrity), ui-reviewer (UI/integration),
and workshop-reviewer (general plan/acceptance review). All have Read/Glob/Grep only.
The main session owns commands, edits, report saving and independent reproduction.
See [use-case recipes](../CLAUDE_USE_CASES.md) for task selection and output examples.

For another project, copy template contents including `.claude/`, adapt the profile
and replace course runner commands with the project's actual commands. Review rules
and permissions. Test one bounded change before adopting the kit broadly.
