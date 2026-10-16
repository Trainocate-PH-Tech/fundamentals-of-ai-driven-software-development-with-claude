# Module 3 — Plan, create skills, and supervise reviewers

Windows users: follow [Windows setup](../WINDOWS_SETUP.md). Run commands from the active project root unless stated otherwise; choose Bash or PowerShell, not both. Prompts go inside Claude.

**Entry:** verified application map. **Result:** an accepted implementation plan
and a reusable workflow students can transfer to other projects.

## 1. Plan a bounded change

Start `claude` from the active project root. Use `/plan` if available in `/help`, or cycle
permission modes with Shift+Tab to Plan Mode. Planning cannot silently become
implementation. Paste inside Claude:

```text
Plan milestone 01-data using SQLite and direct commands. Add Category and Issue models, migrations and idempotent category seed only. Reuse User; preserve existing data. Use SOFTWARE_SPECIFICATIONS.md and workshop-output/milestones/exploration/map.md. Identify files, constraints and tests. No endpoints or frontend yet.
```

This is an ordinary request to the main Claude session, with no custom skill
dependency. Claude inspects the source and proposes a bounded plan.
In Plan Mode it returns the plan in the conversation; after accepting and leaving
Plan Mode, ask the main session to save it to `workshop-output/milestones/01-data/plan.md`.
Read every step before implementation. A plan must name validation commands and
expected behavior, not merely say “test it.”

## 2. Create your own skill

A skill is a folder containing SKILL.md with a name, a description explaining
when it applies, and the reusable procedure. Supporting scripts live beside it.
Create this from your selected terminal at the active project root:

```bash
mkdir -p .claude/skills/review-contract
cat > .claude/skills/review-contract/SKILL.md <<'SKILL'
---
name: review-contract
description: Compare a requested API change against the project contract and existing implementation.
disable-model-invocation: true
---
Read workflow/project.md and SOFTWARE_SPECIFICATIONS.md. Review $ARGUMENTS.
Inspect the relevant schemas, endpoints, operations and tests. Do not edit source.
Return a table: requirement, source path, test path, missing evidence, recommendation.
Do not claim a test passed unless its execution evidence was supplied.
SKILL
```

**PowerShell 7.4+ (Windows):**

```powershell
New-Item -ItemType Directory -Force -Path '.claude/skills/review-contract' | Out-Null
@'
---
name: review-contract
description: Compare a requested API change against the project contract and existing implementation.
disable-model-invocation: true
---
Read workflow/project.md and SOFTWARE_SPECIFICATIONS.md. Review $ARGUMENTS.
Inspect the relevant schemas, endpoints, operations and tests. Do not edit source.
Return a table: requirement, source path, test path, missing evidence, recommendation.
Do not claim a test passed unless its execution evidence was supplied.
'@ | Set-Content -Encoding utf8 .claude/skills/review-contract/SKILL.md
```

Restart Claude; use `/help` or type `/` to find the skill. Invoke **inside Claude**:

```text
/review-contract Category deletion when issues reference it
```

Expected before implementation: a gap report, not an invented endpoint. After
Module 4, invoke it again and compare the report with actual source and tests.
**Independent:** create `review-ui-state` for loading, error, empty, validation and
confirmation behavior. Run it before and after the issue form exists. Include a
negative case (missing error handling) and evaluate whether it finds the defect.
Use generic instructions and a project profile so the procedure transfers.

## 3. Subagent delegation with explicit inputs

Module 1 creates architecture-reviewer and acceptance-reviewer by writing their
files under .claude/agents. Additional role definitions are provided in
[the manual instruction examples](../workflow-kit/README.md). For the optional
backend-reviewer, ui-reviewer or bug-investigator exercises, open the matching file
under the course's workflow-kit/template/.claude/agents and copy its reviewed
contents into the same relative path in your active project. No installer runs.
Restart Claude before invoking a newly created role. The definitions restrict tools
to Read, Glob and Grep: reviewers return reports; the main session runs commands
and saves evidence. Give every agent explicit plan/spec/source paths.

```text
Use acceptance-reviewer to review workshop-output/milestones/01-data/plan.md against
SOFTWARE_SPECIFICATIONS.md and workshop-output/milestones/exploration/map.md. Give it the
backend path issuetrackerapi and the constraint that existing User data must survive.
Ask for verdict, severity, source paths and missing tests. Do not implement.
Main session: save the returned review to workshop-output/milestones/01-data/review.md.
```

**How to monitor:** verify the task was actually created with the named agent;
expand its tool activity in the session. For background tasks use `/tasks` when
shown in your installed `/help`; open the task and inspect status/output. Use the
UI's stop control for an out-of-scope task. Ask the main session to report task
name, assigned input files, status, findings and saved report path. A missing task
or missing output is “not run,” not “passed.” CLI versions change; do not assume
an undocumented keyboard shortcut is universal.

Subagents have separate context: supply the plan, source paths and acceptance
criteria every time. They do not inherit the whole parent conversation. Keep
implementation with one owner. Two reviewers may inspect separate backend and
frontend scopes; do not have multiple writers change the same files. Worktrees
provide isolation for separate writing tasks but do not isolate shared databases.

**Independent:** create ui-reviewer from the referenced example if absent, then inspect its definition from Bash:

```bash
cat .claude/agents/ui-reviewer.md
```

**PowerShell 7.4+ (Windows):**

```powershell
Get-Content .claude/agents/ui-reviewer.md
```

Extend `.claude/agents/ui-reviewer.md` with one additional evidence requirement
for accessible labels. Preserve its name and read-only tools. Restart, inspect `/agents`, then delegate a frontend-plan review.
Save the report and identify at least one missing acceptance test yourself.

## 4. Resume from evidence

Before `/compact` or ending a session, ask:

```text
Write workshop-output/milestones/01-data/handoff.md with completed changes, accepted plan,
actual commands and exit codes, remaining findings, and the next smallest task.
Do not include credentials. Separate tested facts from assumptions.
```

Start a fresh session and give it the handoff plus the current plan. Verify it
inspects source rather than trusting stale notes. **Independent:** resume the
category plan in a new session and identify one stale assumption deliberately
inserted in a copy of the handoff.

## 5. Efficient token usage

Complete the [token-efficiency lab](04_TOKEN_EFFICIENCY.md): inspect context/usage,
compare broad and targeted read-only prompts, keep logs outside the conversation,
write a concise handoff and evaluate whether a subagent adds useful independent
work. Preserve acceptance criteria and required tests. Record measurements rather
than claiming savings from shorter answers alone.

**Exit gate:** accepted plan, reviewer report and usable handoff. For the optional
skill lesson, also test the custom skill before/after implementation. Next: [Module 4](../04-issue-tracker-implementation/README.md).

Source references (checked 2026-10-15): [skills](https://code.claude.com/docs/en/skills),
[subagents](https://code.claude.com/docs/en/sub-agents),
[memory](https://code.claude.com/docs/en/memory),
[CLI options](https://code.claude.com/docs/en/cli-reference),
[permissions](https://code.claude.com/docs/en/permissions).
Use the installed CLI's help to resolve version-specific UI differences.

Apply this workflow in the [diagnostic lab](DIAGNOSTIC_LAB.md).
