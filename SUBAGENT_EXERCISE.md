# Subagent exercises: generate mock data and implement GET /issues

Create two Claude Code subagents and use them for sequential, bounded backend
changes. The first builds a repeatable way to populate the development system;
the second implements a real database-backed issue-list endpoint.

These are participant exercises, not completed application features. Create the
agent files below in your **active student workspace**, not automatically in the
course clone. No skill or MCP server is required. For those concepts, see
[Skills fundamentals](SKILLS_FUNDAMENTALS.md) and [MCP fundamentals](MCP_FUNDAMENTALS.md).

Here, “a given system” means the selected Issue Tracker application and its
configured database. The [specification](SOFTWARE_SPECIFICATIONS.md) defines no
System entity, tenant selector, or `system_id`. Do not invent one. If adapting
this exercise to a multi-system application, first establish its existing system
identity and authorization contract before changing the endpoint.

## 1. Entry gate and ownership

Complete the application map and **Module 4's `01-data` gate** first: Category
and Issue models, migrations, and the existing User model must be available.
Read the [Module 4 walkthrough](04-issue-tracker-implementation/README.md) and
specification. If the data layer is missing, finish that milestone first.

These exercises cover sample seeding and the read/list portion of issue work.
They do not replace the remaining CRUD, assignment, frontend, or demonstration
gates. If the endpoint already exists, inspect it and implement only verified
gaps rather than adding a second route.

The normal workshop workflow uses read-only reviewers. This optional exercise
explicitly delegates **bounded source-file edits** to one implementation subagent
at a time. The participant's implementation prompts below authorize that scoped
exception. The main session retains plan ownership, command execution, database
writes, review, and verification. Never run both writing agents concurrently or
let the main session edit their assigned files while they are working.

Use your editor to create `.claude/agents/` in the active root. Confirm the root
and shell first; replace the example path and run only your platform's block.

**Bash on Linux/WSL:**

```bash
cd /absolute/path/to/your/student-workspace
pwd
uname -s
printf '%s\n' "$SHELL"
claude --version
mkdir -p .claude/agents
```

**PowerShell 7.4+ on Windows:**

```powershell
Set-Location 'C:\absolute\path\to\your\student-workspace'
Get-Location
[System.Environment]::OSVersion
$PSVersionTable.PSVersion
claude --version
New-Item -ItemType Directory -Force -Path '.claude/agents' | Out-Null
```

Record the workspace, OS/shell, CLI version, and each app's Git revision/dirty
state. Keep earlier work intact. Use new run folders under:

- `workshop-output/milestones/subagent-mock-data/`
- `workshop-output/milestones/subagent-issues-list/`

Each run needs `plan.md`, the subagent's report, `review.md`, `evidence.md`, and
`handoff.md`. Replace `<RUN>` in prompts with your chosen unique folder name.

### Inspect before selecting commands

Paste inside Claude from the active root:

```text
Explore only. Read AGENTS.md, CLAUDE.md, workflow/project.md and
SOFTWARE_SPECIFICATIONS.md, then both application READMEs and local instructions.
Inspect the active issuetrackerapi and issuetrackerweb; do not inspect instructor
or recovery source. Report exact model/session/seed/test paths, User ID type,
authentication, route prefix, response envelope, pagination, and frontend API
client expectations. Confirm Category/Issue migrations exist and identify any
existing GET /issues implementation. Identify commands for isolated backend
tests, development seeding, API startup and frontend checks, including working
directory and OS-specific syntax. Distinguish observed facts from requirements.
Do not read environment files or expose credentials. Do not edit or run seeds.
```

Save the findings as the map for both exercises. Runtime commands must be derived
from that inspection; this page deliberately does not invent app module names.

## 2. Exercise A — mock-data-generator

**Result:** a small seed implementation that inserts 12 synthetic issues into
local development SQLite and can run twice without duplicating or overwriting
existing records. Mock data becomes persisted application data; it is not a
hard-coded replacement for endpoint responses.

### Create the agent

Create `.claude/agents/mock-data-generator.md` with this complete content:

```markdown
---
name: mock-data-generator
description: Implement an accepted, bounded mock-data seed plan for the active Issue Tracker backend.
tools: Read, Glob, Grep, Write, Edit
model: inherit
---

Require explicit task inputs: active workspace, root/app instruction paths,
specification path, inspected application map, accepted plan path, and allowed
edit paths. Read those inputs. If the plan or scope is missing, report BLOCKED.

Implement only the approved seed and its focused tests. Reuse existing models,
DB session, validation and seed conventions. Create synthetic Category/Issue
records only; reuse existing users for optional assignment. Never create users,
reset passwords, alter authentication, add domain models or modify migrations.
Preserve foreign keys. Make reruns non-destructive and idempotent using the
collision/identity policy specified in the accepted plan. Do not add a package
when a small deterministic fixture suffices.

Do not read credentials, execute commands, connect to a database, or inspect
instructor/recovery workspaces. Only edit allowed source paths. Report missing
prerequisites instead of expanding scope. Return changed paths, dataset coverage,
identity strategy, proposed verification commands and known limitations.
Label tests as NOT RUN; the main session executes and verifies them.
```

Restart Claude after creating the agent. Confirm it is discoverable through the
installed `/agents` interface or help. These file-based roles use Claude's
[documented subagent configuration](https://code.claude.com/docs/en/sub-agents).
Tool access permits file edits, but grants no shell or database tool.

### Plan the dataset

Use this exercise-specific dataset contract alongside the specification:

| Property | Required coverage |
|---|---|
| Categories | Reuse or seed Bug, Feature Request, Task, Documentation; case-insensitive reuse |
| Issues | 12 identifiable synthetic records, with a reserved lab prefix in their titles |
| Status/priority | Cover every allowed value from the specification |
| Search | At least two titles containing “login” with different casing |
| Combined filters | At least two open/high Bug issues, plus distractors matching only some criteria |
| Assignment | Unassigned records; optionally assign some to a validated existing user supplied by the participant |
| Reruns | Stable identity; no duplicates and no updates to existing rows, even if a participant edited a seeded issue |

Plan a stable fixture identity compatible with the inspected primary-key type.
Do not rely only on a mutable title for identity. Reserve deterministic IDs when
supported, detect collisions with unrelated rows, and fail clearly rather than
overwrite them. Reuse category IDs actually found/created in the database.
No assumed user ID is valid. Without a supplied existing user, leave assignments
null; use existing test factories for assignment tests in the isolated test DB.

Paste in Plan Mode:

```text
Plan exercise subagent-mock-data using the inspected map and specification.
Design a 12-issue deterministic development seed meeting SUBAGENT_EXERCISE.md
Exercise A, with case-insensitive category reuse, stable issue identity, collision
handling, transaction rollback, and rerun preservation. Reuse seed conventions
without invoking any password-reset seed. Restrict execution to the configured
local development database; refuse unexpected environments/targets.
Name exact allowed seed/test paths and platform-specific commands. Test reruns,
preexisting categories, user preservation, invalid assignee and target refusal.
No edits or database writes yet. Report any prerequisite gaps.
```

If the guide is not copied into the student workspace, supply its absolute path
or paste the dataset contract into the prompt. Accept the concrete plan, leave
Plan Mode, and have the main session save it to the run's `plan.md`.

### Delegate the implementation

```text
I accept workshop-output/milestones/subagent-mock-data/<RUN>/plan.md.
For this exercise I authorize mock-data-generator to make the source edits in
that plan's allowed paths. This is a scoped exception to read-only delegation;
the main session retains commands, database execution and verification.
Delegate to mock-data-generator with the absolute active workspace, root/app
instructions, specification, inspected map, accepted plan and allowed edit paths.
Do not edit those files concurrently. Ask for its implementation report with
checks explicitly marked NOT RUN. Save the report unchanged in this run folder.
```

Expand the named delegation and inspect its file activity. A main-session answer
without a `mock-data-generator` task does not complete the delegation exercise.

### Verify and populate the system

Main session: review the diff first, then execute the accepted focused tests in
the isolated test environment. Run the new seed against development only after
its behavior is reviewed. Use these environment boundaries from the API directory:

| Operation | APP_ENV | DATABASE_URL |
|---|---|---|
| Development seed and API | `development` | `sqlite:///storage/development.sqlite3` |
| Automated tests | `test` | `sqlite:///test.sqlite3` |

The seed's development-target refusal tests should use the existing isolated test
fixtures; they must never insert into development. Keep foreign keys enabled.
Do not reuse virtual environments between Windows and WSL. Use direct Python
commands from the accepted plan, not course launchers.

```text
Main session: inspect the mock-data-generator diff against the accepted plan.
Run focused tests with the inspected test command and isolated SQLite test URL.
If they pass, run the reviewed seed twice against local development, recording
created/skipped counts and safe IDs. Verify all 12 fixture issues persist after
closing/reopening the session, the second run creates none, and existing users
and unrelated issues are unchanged. Test edited-row preservation and invalid
assignee rollback in the isolated test DB. Run required backend regression checks.
Record commands, working directories, environment names, exit codes, and actual
results in this run's evidence.md. Keep credentials and user secrets out of logs.
```

**Exit gate A:** fixture coverage confirmed, repeat runs preserve data, persistence
verified, user preservation and rollback tests pass, and review/evidence/handoff
saved. A generated JSON file alone does not establish that the system was seeded.

## 3. Exercise B — feature-implementation

**Result:** authenticated `GET /issues` returns persisted issues from this
application's database. `/issues` is the **logical route**; use the existing API
prefix discovered in section 1. Reuse the existing list/pagination envelope.

### Create the agent

Create `.claude/agents/feature-implementation.md`:

```markdown
---
name: feature-implementation
description: Implement an accepted issue-list endpoint plan in the active Issue Tracker backend.
tools: Read, Glob, Grep, Write, Edit
model: inherit
---

Require the active workspace, root/app instruction paths, specification,
inspected application map, accepted plan and allowed edit paths. Read them.
If inputs or persistence prerequisites are missing, report BLOCKED.

Implement only the approved GET /issues slice and its tests. Reuse routing,
authentication, ORM/session, serialization, pagination and error conventions.
Query persisted Issue data; never return a hard-coded fixture array. Follow the
specification's search, filters, ordering and safe response requirements.
Use parameterized ORM/query mechanisms. Preserve unrelated routes and behavior.
Do not add System/User models, schema migrations, write endpoints, frontend
features or dependencies outside the accepted scope.

Edit only allowed source paths. Do not read credentials, run commands, connect
to databases, or inspect instructor/recovery workspaces. Return changed paths,
resolved route and response shape, tests added, proposed verification commands,
and limitations. Mark execution NOT RUN; the main session verifies the changes.
```

Restart Claude and confirm the new named role is available.

### Plan the endpoint

Reference specification sections 4 (FR-03), 5.2, 5.4, 8, and 9 instead of copying
the full contract into the agent. The accepted plan must cover:

- Authentication and existing authorization behavior.
- Database-backed results, safe category/assignee data, and the established envelope.
- Case-insensitive title search; status, priority, category, and assignee filters;
  combined filters using AND.
- `updated_at` descending and a documented stable secondary ID order.
- Empty results, invalid query inputs, and pagination if the template has it.

Paste in Plan Mode:

```text
Plan exercise subagent-issues-list. Inspect the current GET /issues behavior
and the accepted data layer. Implement only missing behavior for the logical
GET /issues endpoint under the existing API prefix. Use SOFTWARE_SPECIFICATIONS.md
FR-03, sections 5.2/5.4/8/9 and the inspected application map. Do not add a System
entity or system_id; this endpoint lists issues of the active application.
Name exact allowed files, auth dependency, response envelope, queries and tests.
Include test fixtures independent of development seed state, null/existing
assignees, safe serialization, search, every filter, AND combinations, empty
results, invalid input, stable ordering and existing pagination conventions.
No edits yet. Do not reimplement a route that already meets the contract.
```

Accept/save the plan under `subagent-issues-list/<RUN>/plan.md`, then delegate:

```text
I accept workshop-output/milestones/subagent-issues-list/<RUN>/plan.md.
For this exercise I authorize feature-implementation to edit only that plan's
allowed source paths. This is a scoped exception to read-only delegation; the
main session retains commands and verification. Delegate with the absolute
workspace, root/app instructions, specification, inspected map and accepted plan.
Do not edit concurrently. Require the resolved route, response shape, changed
files, added tests and NOT RUN execution status in its returned report.
Save the report unchanged in this run folder.
```

### Verify the feature and its integration with the seed

Use the following as a checklist for actual test assertions, not a pass report:

| Scenario | Required observation |
|---|---|
| Authenticated list | 200; persisted issue IDs and fields in the existing envelope |
| Missing/invalid authentication | Rejected under existing auth rules |
| No issues / no matches | 200 with empty collection in the proper envelope |
| Case-insensitive search | Both seeded login variants match; unrelated titles do not |
| Individual filters | Only records matching each supplied criterion |
| Combined filters | All returned rows meet every supplied criterion |
| Updated time tie | Repeat calls use the documented secondary ID order |
| Invalid query values | Established validation error; never silently ignored |
| Safe serialization | Null assignee handled; no password/token/private User fields |
| Real persistence | A test-fixture DB change changes the next response; no fixture array |
| Pagination, if present | Correct page boundaries and metadata under existing conventions |

Main session prompt:

```text
Review feature-implementation's diff against its accepted plan. Run the smallest
relevant tests first, then the required backend suite with APP_ENV=test and
DATABASE_URL=sqlite:///test.sqlite3 from the API directory. Run the inspected
frontend checks required by repository guidance and record actual outcomes.
Start the API against local development using the inspected direct command.
Through the existing authenticated API client/docs UI, call the actual prefixed
GET /issues route and compare returned IDs with Exercise A's persisted fixture.
Account for pagination and unrelated existing data. Verify search and combined
filters without exposing credentials. Do not claim all CRUD or browser acceptance
passed from this list-endpoint check. Record commands, exit codes and limitations.
```

For manual requests, substitute the observed prefix and returned IDs. These
examples are request shapes, not verified URLs or executable shell commands:

```text
GET <API_PREFIX>/issues
GET <API_PREFIX>/issues?search=LOGIN
GET <API_PREFIX>/issues?status=open&priority=high&category_id=<REAL_BUG_CATEGORY_ID>
```

An empty prefix means `/issues`. Obtain credentials using the existing login
flow; do not paste tokens into prompts or evidence. The integration run should
find the known fixture IDs, but may also return unrelated issues. Do not assert
that the entire development database contains exactly 12 issues.

**Exit gate B:** named delegation observed, tests and required checks pass, live
endpoint returns persisted fixtures with correct filters, diff reviewed, and
report/evidence/handoff saved. Continue Module 4 for the remaining functionality.

## 4. Independent challenges and failure handling

- Mock-data agent: add two new fixtures while preserving the original 12 on rerun.
  Accept a revised plan and verify preservation before using development data.
- Feature agent: add a regression test with matching and nonmatching records that
  would catch an accidental OR instead of AND in combined filters.
- Both: invoke without an accepted plan and confirm BLOCKED with no source edits.
  Save the result separately from successful implementation runs.

If a test fails, the main session records the failure and delegates a bounded
repair to the same agent with the log and allowed paths. Rerun affected checks.
Do not rewrite the feature based only on an unverified reviewer hypothesis.
If required tools or inputs are unavailable, report that limitation rather than
claiming the exercise passed. A subagent without command tools cannot truthfully
report that it ran tests or seeded a database.

This guide supplies definitions and task prompts only. It does not install these
agents, seed a student database, or implement a student endpoint. Static document
checks do not establish that live Claude, backend, or Windows exercises passed.
