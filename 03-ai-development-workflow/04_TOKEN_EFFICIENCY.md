# Efficient token usage without weakening verification

Use this lab after planning and skill creation in [Module 3](README.md). The goal
is useful, verified progress per session. A shorter prompt that omits critical
requirements can cost more through incorrect changes and repeated repairs.

## 1. Know what you are measuring

Context occupancy, cumulative token usage, API cost and subscription limits are
different measurements. Inspect `/context` for context composition and `/usage`
for the usage information available to your account. Check `/help` for the commands
supported by your installed version. API cost estimates are not subscription bills;
use your provider's billing records for authoritative charges. A small answer alone
does not establish low total usage. See [Claude usage guidance](https://code.claude.com/docs/en/costs).

Before a lab, record the model, client version, active workspace and starting usage.
Afterward, record usage again and whether the result met the acceptance criteria.
Do not invent unavailable measurements or compare unlike displays as equivalent.

## 2. Make the next question smaller

For this course, use these habits:

| Instead of | Ask for |
|---|---|
| “Understand the entire repository” for every change | One request path or feature and its relevant dependencies |
| Pasting complete files and logs repeatedly | File paths, a failing assertion and the relevant log excerpt |
| “Fix all problems” | A reproduced failure and bounded repair criteria |
| Rewriting the same explanation each turn | A milestone plan and concise evidence/handoff files |
| Repeatedly printing a successful full test run | Command, outcome, summary and saved log path |
| A long speculative diagnosis | Competing hypotheses and one discriminating check |
| Several agents reviewing identical scope | One reviewer assigned a specific independent question |

Example of an underspecified request:

```text
Read everything and fix assignment.
```

Better **inside Claude**, after the assignment slice exists:

```text
Work only in issuetrackerapi on title-only PATCH preserving the existing assignee.
Start with spec/tracker/test_assignment.py, app/schemas/tracker.py and
app/controllers/issues_controller.py. Follow the operation import only if needed.
Do not inspect frontend, reference, recovery or dependency directories.
First explain current behavior with file/symbol evidence in at most six bullets.
Do not edit or run tests yet. If these paths differ in my implementation, locate
only their equivalents before proceeding.
```

The file list is a starting scope, not permission to ignore a relevant dependency.
If more context is necessary, Claude should explain the missing evidence and read
that dependency. Do not force an answer from insufficient input.

## 3. Search first; keep full evidence outside the conversation

From Bash at the course root, after student setup:

```bash
rg -n 'exclude_unset|assigned_user_id' issuetrackerapi/app/controllers issuetrackerapi/app/schemas
```

If ripgrep is unavailable, use editor search. Exclude generated dependencies and
other workspaces from the search. A matching line is a navigation aid, not enough
context to implement a fix: inspect the containing function before changing it.

**Inside Claude:**

```text
Investigate the assignment failure using the relevant test and the failing traceback.
Save full command output in this milestone's logs directory with a new run name.
In conversation, report the command, exit code, failing assertion and the smallest
relevant excerpt. Read surrounding log lines if the excerpt is insufficient.
Do not discard warnings or earlier errors that could explain the failure.
```

Run focused checks during diagnosis and the required broader gates before declaring
completion. Repeating the full suite without new edits or an unresolved question
usually adds little evidence. Skipping required checks is not a token optimization.

## 4. Keep persistent guidance short and procedures reusable

Use AGENTS.md and CLAUDE.md for stable constraints, the profile for project facts,
and skills for repeatable procedures. Do not paste the whole course guide into
always-loaded instructions. Keep observed facts separate from target requirements.
A reusable skill saves repeated instruction-writing; its execution still consumes
model/tool context. Use it when the procedure is relevant, not as an extra ritual.

**Independent audit prompt:**

```text
Review CLAUDE.md, AGENTS.md and workflow/project.md without editing. Identify
repeated instructions, facts likely to become stale and long procedures that could
move into an existing skill. Preserve security, data integrity and test requirements.
Return at most five proposed changes with reasons; do not rewrite the specification.
```

## 5. Manage long sessions deliberately

Claude supports context compaction and fresh sessions. Save a durable handoff before
switching tasks or relying on a compacted history; then verify it against source.
Specific context, verification criteria and deliberate session management are
recommended in the [official best practices](https://code.claude.com/docs/en/best-practices).

**Inside Claude, before ending the assignment session:**

```text
Update workshop-output/milestones/04-assignment/handoff.md in at most 300 words.
Include active workspace, accepted scope, app revisions/dirty state, completed
changes, actual checks and evidence paths, unresolved issue and next smallest task.
Link the plan and logs rather than copying them. Preserve important uncertainties.
```

To continue the same task with less conversational history, use the installed
client's `/compact` command after saving the handoff. For a different task, start
a fresh session instead of carrying all prior debugging attempts into it. Neither
choice refunds tokens already used; reloading context also has a cost.

**Fresh-session prompt:**

```text
Read workshop-output/milestones/04-assignment/handoff.md and its linked plan.
Verify the active source state before trusting the summary. Read only the files
needed for the recorded next task. Identify stale claims, then propose the next
check. Do not re-explore the whole application or assume previous tests cover edits
made after the recorded run.
```

## 6. Use agents and model choices selectively

Subagents can keep verbose investigation out of the main conversation, but their
work adds usage. Delegation does not guarantee lower total cost. Prefer one bounded
investigation with a concise result over duplicate whole-repository reviews.
These tradeoffs and model selection are covered in [cost guidance](https://code.claude.com/docs/en/costs).

```text
Use workshop-investigator for one question: can omitted PATCH fields reach the
update operation as null? Supply the assignment failure log and relevant schema,
handler and operation paths. Ask for at most five findings, each with a path and
evidence, and one proposed check. No edits, commands or further delegation.
Main session: evaluate the findings rather than repeating the entire investigation.
```

For routine source lookup or summarization, try an available lower-cost model only
if it meets the same evidence criteria. Use more capable reasoning when ambiguity
or change risk requires it. Keep the model fixed during comparison exercises; do
not use hard-coded pricing or assume the cheapest request minimizes total repair
cost. Any model or account-policy change remains the learner's explicit choice.

## 7. Guided comparison exercise

Use the same completed assignment source in two fresh sessions or paired learners.
Keep model, workspace, task and acceptance criteria constant. Do not change source.
Both prompts must inspect at most six relevant source/test files and return at most
six bullets. This bounds the classroom experiment instead of intentionally wasting
usage on an unrestricted repository scan.

**Session A:**

```text
In issuetrackerapi, explain whether a title-only issue PATCH preserves its assignee.
Locate and inspect at most six relevant source/test files. Return at most six bullets
with file evidence and one exact verification command. No edits, commands or delegation.
```

**Session B:** use the targeted prompt in section 2, adding: “Inspect at most six
relevant files; include one exact verification command in your six-bullet answer.”
Both sessions must receive the same applicable project instructions.

Record results in `workshop-output/milestones/token-efficiency/evidence.md`:

| Measurement | Session A | Session B |
|---|---|---|
| Client/model and workspace revision/dirty state | | |
| Starting and ending usage, as actually displayed | | |
| Files read/tool calls observed | | |
| Context occupancy, where available | | |
| Correctly distinguishes omitted from null | | |
| Cites relevant implementation and regression evidence | | |
| Gives the correct test-workspace command | | |
| Corrections needed before result is usable | | |

Do not claim savings from word count alone. Cache state, automatic context,
provider/account differences and model variation can affect results. Report this
as an observed classroom comparison, not a guaranteed percentage reduction.
If usage data is unavailable, report qualitative findings and mark token savings
unmeasured. Students may skip the second paid run and compare prompt design instead,
but must label that as an unexecuted comparison.

**Independent:** narrow a frontend network-error diagnosis using the same method.
Keep the requirement to distinguish network failure from an empty successful result.

**Exit gate:** the learner can show a correctly scoped prompt, concise source-backed
output, a safe handoff and honest measurements. A cheaper incorrect answer does
not pass. No application tests need rerunning for this read-only comparison alone.
