# Choosing a Claude workflow for an engineering task

Use this alongside the five module READMEs. Each recipe should identify the active
workspace, inputs, mode, scope, output and check. Default to the root student apps;
do not read instructor-reference or recovery unless the task explicitly selects them.

| Situation | Workflow | Concrete outcome |
|---|---|---|
| Understand unfamiliar behavior | Read-only exploration; scout for an isolated trace | File-backed request map |
| Resolve cross-file uncertainty | Plan Mode | Accepted scope and verification criteria |
| Make a small, obvious correction | Direct bounded edit | Reviewed diff and focused check |
| Repeat a proven process | Named skill | Milestone artifacts and actual results |
| Investigate competing explanations | Read-only investigator | Evidence and a discriminating next check |
| Review an API/UI change | Specialized reviewer | Reproducible findings and evidence gaps |
| Catch predictable syntax mistakes | Tested hook | Observed event feedback |
| Prove delivery readiness | Tests, build, browser checks and CI | Recorded pass/fail results |

Do not add a planning ceremony to every typo fix. Do use a plan when scope, data
impact or dependencies are uncertain. Subagents help isolate questions; keep one
implementation owner until file and database isolation are deliberately designed.

## Standard task and evidence contract

Every core task supplies: milestone ID, active app paths, observed problem or target
behavior, relevant inputs, allowed changes, expected output and verification command.
Skills use the ID to write under `workshop-output/milestones/<id>/`:

- `plan.md`: observed implementation, requirements, proposed changes and acceptance checks.
- `review.md`: reviewer/task identity, supplied paths, findings and main-session dispositions.
- `evidence.md`: workspace, timestamp, app commit IDs, dirty state, command, working directory,
  exit code, criterion, result and limitations. Logs go in `logs/` with distinct run names.
- `handoff.md`: current milestone, completed work, evidence paths, unresolved findings and next task.

Create missing artifact directories before saving. Never overwrite earlier milestones.
A Git revision alone does not identify uncommitted code. Previously existing local
`current.md` files are historical inputs; copy useful material deliberately, label
its provenance and recheck stale claims. No automated artifact migration is required.

## Recipe: implement an accepted change

In Plan Mode:

```text
/workshop-plan 02-categories Implement category CRUD in issuetrackerapi only. Read the existing controller/operation conventions and specification. Name source and test paths, errors, integrity constraints and checks. Do not implement or inspect the instructor solution.
```

After inspecting and accepting the plan, leave Plan Mode and send:

```text
I accept this category plan. Save it to workshop-output/milestones/02-categories/plan.md without changing its scope. Do not implement yet.
```

Then invoke:

```text
/workshop-implement 02-categories workshop-output/milestones/02-categories/plan.md
```

And:

```text
/workshop-verify 02-categories workshop-output/milestones/02-categories/plan.md Category CRUD and protected deletion
```

If verification fails, inspect the evidence and authorize a bounded repair:

```text
Read workshop-output/milestones/02-categories/evidence.md. Reproduce the confirmed
failure using the documented test target. Repair only the behavior covered by the
accepted plan, without weakening assertions. Rerun the failing test and affected
regressions. Append results and update the handoff; ask before expanding scope.
```

## Recipe: diagnostic loop

Use symptom → reproduction → competing hypotheses → discriminating check → minimal
repair → regression. Do not reinstall everything, relax auth, or disable tests as
a first response to an unexplained failure.

```text
In issuetrackerapi, an issue loses its assignee when PATCH changes only its title.
Read the supplied failing output and assignment tests, schema, handler and operation.
Do not read instructor-reference. First reproduce with ./workshop test using the
dedicated test DB. Compare request parsing, update logic and persistence as causes.
Show the evidence distinguishing them. Propose the smallest repair before editing.
After my acceptance, fix it, run assignment and issue regressions, and record the
cause, changed files, commands and results under milestone assignment-diagnosis.
```

Expected output names the failing assertion and the responsible data transformation.
“Probably a database bug; rebuild the containers” is inadequate without evidence.
If reproduction passes, report that result and investigate input/environment
mismatch rather than deliberately breaking correct application code.

## Recipe: delegate investigation without delegating ownership

```text
Use workshop-investigator to inspect one hypothesis: omitted PATCH fields are
being converted to null. Supply the active backend path, assignment failure log,
request schema and issue handler/operation paths. Ask it to cite evidence for and
against this hypothesis and propose one discriminating check. No edits or commands.
Main session: save its report under milestone assignment-diagnosis, run the proposed
check if appropriate, and classify the hypothesis using actual output.
```

Monitor the actual named task and its file reads. An agent with no Bash tool cannot
claim it ran pytest. Main-session execution and read-only review are separate evidence.

## Output calibration examples

These are illustrative output shapes, not records of newly executed checks.

| Output | Acceptable | Inadequate |
|---|---|---|
| Plan | Names observed files, target behavior, bounded edits and tests | “Build the backend and test it” |
| Review | Identifies handler/schema path, omitted-field risk and reproducing request | “Looks good” without inspected scope |
| Diagnosis | Failing title-only PATCH test plus evidence fields were included as null | Unsupported speculation or unrelated refactor |
| Verification | Exact command, exit code, revision/dirty state and criterion covered | “All tests pass” without execution evidence |
| Handoff | Active workspace and next task linked to current source/evidence | Old summary copied into a new session unchanged |

## Recipe: course-correct a stalled session

```text
Stop adding changes. Summarize the active workspace, accepted scope, edits so far,
checks actually run and the unresolved hypothesis. Identify the smallest next
check. Do not repeat the same failed repair or expand scope without evidence.
Save a handoff under this milestone so a fresh session can continue.
```

Start the next session with that handoff and plan, then ask it to verify source state
before proceeding. If task input is incomplete, a clarification is the correct result.

## Recipe: efficient token usage

Use the [Module 3 token-efficiency lab](03-ai-development-workflow/04_TOKEN_EFFICIENCY.md)
for copy-paste prompts and a measured comparison. Start with the smallest relevant
question and source paths; expand when evidence requires it. Save full logs and
return concise results. Before changing tasks, preserve a milestone handoff.
Measure usefulness and required corrections alongside usage; keep all verification
gates. Delegating the same work repeatedly is not an efficiency strategy.
