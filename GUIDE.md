# Instructor guide: delivering the Claude Code engineering workshop

This is the facilitator's companion to the [student course](README.md). It explains
what to prepare, demonstrate, say, ask students to do, and verify. Students follow
the five module READMEs; use this guide to orchestrate those lessons rather than
introducing a competing sequence.

The outcome is a working Issue Tracker backed by PostgreSQL, with a FastAPI API,
React interface, automated checks, and a reusable Claude Code engineering workflow.
The [software specification](SOFTWARE_SPECIFICATIONS.md) is the behavior contract.
The [validation record](VALIDATION.md) describes earlier executed checks and their
limits; rerun the relevant checks before your own delivery.

## Contents

1. [Delivery approach and preparation](#1-delivery-approach-and-preparation)
2. [Instructor rehearsal and opening demonstration](#2-instructor-rehearsal-and-opening-demonstration)
3. [Module 1: project setup and trustworthy context](#3-module-1-project-setup-and-trustworthy-context)
4. [Module 2: understand the application](#4-module-2-understand-the-application)
5. [Module 3: reusable skills and supervised subagents](#5-module-3-reusable-skills-and-supervised-subagents)
6. [Module 4: build verified increments](#6-module-4-build-verified-increments)
7. [Module 5: verification, debugging, and handoff](#7-module-5-verification-debugging-and-handoff)
8. [Recovery and classroom troubleshooting](#8-recovery-and-classroom-troubleshooting)
9. [Assessment and closing](#9-assessment-and-closing)
10. [Preparing the course for GitHub](#10-preparing-the-course-for-github)
11. [Instructor reference map](#11-instructor-reference-map)

## 1. Delivery approach and preparation

### Audience and prerequisites

Learners should be able to navigate folders, edit a file, run a terminal command,
and explain a basic HTTP request. They do not need prior Claude Code experience.
For learners unfamiliar with Git, Python environments, React, or relational
constraints, schedule a prerequisite lab. Do not spend the implementation sessions
trying to install missing system software on every machine.

Primary delivery environment: Bash on Linux or WSL2, Python 3.14, Node 24, Git,
Docker with Compose, and a browser. Claude Code requires the learner's supported
account or API billing. macOS requires its own rehearsal; native PowerShell is not
the course's tested application-command path.

Send these materials before class:

- [Terminal Claude setup](CLAUDE_CODE_TERMINAL.md) and [VS Code setup](CLAUDE_CODE_VSCODE_SETUP.md).
- [Module 1 prerequisites](01-project-setup/README.md).
- The course repository URL once published, and instructions to open its root folder.
- A request to verify Docker access and Claude authentication before class.

Keep authentication off the shared screen. Claude's account/API credentials are
separate from the Issue Tracker's local demo account. The app does not need an
Anthropic API key. Use the setup guides' hidden-input procedure for API access;
do not ask learners to paste tokens into chat or instructor notes.

### Suggested pacing

These are planning ranges, not time limits or measured completion guarantees.
Advance by exit gates. Split Module 4 across sessions when necessary.

| Segment | Suggested time | Evidence before moving on |
|---|---:|---|
| Pre-class setup | 60–90 minutes | Tools, Docker and Claude available |
| Opening demonstration | 20–30 minutes | Learners can describe the target workflow |
| Module 1 | 90–120 minutes | Baseline checks and instruction probes |
| Module 2 | 60–90 minutes | Source-backed application map |
| Module 3 | 120–150 minutes | Accepted plan, custom skill and reviewer report |
| Module 4 | 4–6 hours | Six implemented slices and real browser integration |
| Module 5 | 120–150 minutes | Verification evidence, regression repair and handoff |
| Demonstrations and assessment | 45–60 minutes | Complete browser demo and explanation |

For a shorter event, assign setup beforehand and continue implementation later.
Do not claim the full engineering outcome after only demonstrating prompts.

### Teaching rhythm

For each exercise, explain the requirement, demonstrate one bounded task, let
students repeat it, then give a different independent task. Ask students to show
source and execution evidence before accepting completion. Pairing works well:
one learner operates Claude while the other checks scope, diffs, and results;
switch roles at each slice.

**Instructor says:**

> Our workflow is explore, plan, implement, and verify. Claude can propose and write
> changes, but we remain responsible for scope, permissions, data, and proof that
> the system works. A review report and a passing test answer different questions.

### Establish terminal conventions

All Bash blocks in this guide run from the course root unless explicitly stated.
Open that directory in the editor; it contains `workshop`, `AGENTS.md`, and this
file. A `text` block is a prompt to paste inside Claude, not a shell command.
Each command block is a checkpoint: inspect failures before continuing.

Use three named terminals once servers are needed:

| Terminal | Purpose |
|---|---|
| A — API | Foreground API process; leave running |
| B — Web | Foreground frontend process; leave running |
| C — Checks | Setup, tests, builds, Git inspection, and Claude sessions |

| Workspace | API | Web | Development DB | Test DB |
|---|---:|---:|---:|---:|
| Student root | 3000 | 8000 | 54329 | 54330 |
| Instructor reference | 3001 | 8001 | 54331 | 54332 |
| Recovered workspace | 3000 | 8000 | 54329 | 54330 |

The reference can coexist with student work. A recovered workspace conflicts with
the student's host ports even though it has a separate Compose project and volume.
Always use the same workspace selector throughout a demonstration.

## 2. Instructor rehearsal and opening demonstration

### Rehearse the completed reference before class

Read [reference instructions](instructor-reference/README.md). In terminal C:

```bash
pwd
./workshop --reference doctor
claude --version
./workshop --reference setup
./workshop --reference db up
./workshop --reference db migrate
./workshop --reference db seed
./workshop --reference test
./workshop --reference build
(cd instructor-reference/issuetrackerweb && npx playwright install chromium)
```

`doctor` displays versions and checks Docker access; inspect the versions yourself.
Setup installs lockfiles and preserves existing `.env` files. Migration should
reach the tracker migration. The seed creates/updates the local demo admin and
seeds categories. It resets that demo account's password and is only for local
workshop data. It must not be pointed at a real deployment.

Start terminal A:

```bash
./workshop --reference start api
```

Start terminal B:

```bash
./workshop --reference start web
```

Then, in terminal C:

```bash
python3 tools/wait_servers.py http://localhost:3001/docs http://localhost:8001
./workshop --reference e2e
python3 tools/check_docs.py
python3 -m unittest discover -s tools/tests
python3 05-testing-debugging-and-demo/examples/hooks/test_check_python_syntax.py
```

On Linux, missing Chromium system libraries may require the documented Playwright
`install --with-deps chromium` procedure with administrator access. Resolve this
before class rather than replacing the browser test with a mock.

Historical results are recorded in [VALIDATION.md](VALIDATION.md), including skipped
upstream tests and warnings. Check your actual output. Do not use a historical
count as proof that a current run passed, and do not describe the standalone hook
tests as a live Claude hook demonstration.

### Opening browser script

Open `http://localhost:8001/#/login` and sign in with the local demo account
`admin@example.com` / `password`. Keep the API docs at `http://localhost:3001/docs`
for later discussion.

1. Open Categories and create `Instructor demo`.
2. Open Issues and create `Login error during instructor demo`, with that category.
3. Assign the existing demo user and save.
4. Edit status to `in_progress` and priority to `high`; reload to demonstrate persistence.
5. Search by the title and apply both filters. Reset the filters afterward.
6. Try deleting the category while the issue uses it. Show the conflict message.
7. Open the issue, clear its assignment, save, and reload.
8. Start deleting the issue and cancel once; then confirm deletion.
9. Delete the now-unused demo category.

**Instructor says:**

> Every visible behavior crosses several boundaries: browser state, authenticated
> HTTP requests, validation, persistence, and database constraints. We will build
> these boundaries in small slices and prove them separately.

Ask learners which behaviors require server-side enforcement. Expected answers
include category uniqueness, foreign keys, allowed values and protected deletion.
A disabled frontend button alone cannot enforce those rules.

### Rehearse Claude separately

Open Claude at the course root, inspect `/help`, `/memory`, and `/agents`, and
rehearse the named skill and reviewer prompts below. UI commands may vary by
installed version. Verify actual discovery and tool activity; do not promise a
specific shortcut without checking your installed CLI.

Record any live exercises you did not rehearse. The earlier validation did not
establish live VS Code behavior, custom subagent execution, plugin execution or
PostToolUse activation on every instructor machine.

## 3. Module 1: project setup and trustworthy context

Student route: [Module 1](01-project-setup/README.md).
Supporting lessons: [project structure](01-project-setup/01_PROJECT_STRUCTURE.md)
and [Claude context setup](01-project-setup/01_CLAUDE_SETUP.md).

### Teach the workspace boundary

Display root `AGENTS.md`, `CLAUDE.md`, and `workflow/project.md`. Explain that the
student apps are independent repositories generated at the root. The completed
reference lives elsewhere and is not the student's working implementation.

**Instructor says:**

> AGENTS.md holds shared engineering guidance. CLAUDE.md is our Claude entry point
> and explicitly imports that shared guidance. We verify which instructions were
> loaded rather than assuming a filename is enough. The project profile contains
> this project's paths and commands; the reusable skills contain procedures.

### Guided setup — Bash in the student workspace

Use a fresh course copy for the student-path demonstration if your root already
contains student work. Do not delete existing work to make the demo look clean.

```bash
./workshop doctor
./workshop setup
./workshop db up
./workshop db migrate
./workshop install-kit
mkdir -p workshop-output/milestones/setup workshop-output/milestones/exploration workshop-output/milestones/01-data
./workshop test
./workshop build
git -C issuetrackerapi status --short
git -C issuetrackerweb status --short
```

Expected: pinned templates installed, both databases healthy, baseline migration
applied, tests/build successful. Do not run `db seed` until the category seed is
implemented in Module 4. Baseline source changes are compatibility fixes supplied
by the course, not student feature work.

The kit installer preserves existing files. Conflicting candidates go under
`.workshop/proposed/`. Inspect and merge intended differences rather than blindly
copying over guidance. The generic AGENTS candidate does not replace course policy.

After inspecting both diffs, make baseline commits in the independent app repos:

```bash
git -C issuetrackerapi diff
git -C issuetrackerweb diff
git -C issuetrackerapi add .
git -C issuetrackerapi diff --cached --stat
git -C issuetrackerapi commit -m "Establish workshop baseline"
git -C issuetrackerweb add .
git -C issuetrackerweb diff --cached --stat
git -C issuetrackerweb commit -m "Establish workshop baseline"
claude
```

If Git requests identity, have learners configure their own name and email. Never
supply the instructor's identity for the whole class. A repeated commit may report
nothing to commit; inspect status rather than manufacturing a change.

### Guided context probe — inside Claude

```text
Read CLAUDE.md, AGENTS.md, workflow/project.md, and SOFTWARE_SPECIFICATIONS.md.
Read the instruction files in each application repository. Analyze the student
workspace without editing application source or reading environment/credential files.
Identify the purpose of each application, the existing User model and its ID type,
the API and web ports, and the database selected by ./workshop test. Cite paths.
Save your analysis to workshop-output/milestones/setup/map.md. Mark unknowns explicitly.
```

Inspect the resulting file with students. It should identify the student apps,
string UUID IDs, existing authentication, and the dedicated test database. If it
analyzes the reference instead, correct the task scope before accepting its answer.

### Guided rule change and probe

Have students add this rule to root AGENTS.md using their editor:

```markdown
Before changing relationships, identify the migration, existing User data impact,
rollback implications, and a referential-integrity test. Use ./workshop test for
backend checks; never point destructive fixtures at development data.
```

Restart Claude, inspect loaded instructions, and paste:

```text
Plan adding a required category relationship to an issue. Do not implement it.
Identify the instruction that governs schema changes, how existing User records
are preserved, and the exact safe test command. Explain what evidence is needed
before the change can be called complete.
```

Expected: migration review, user preservation and test isolation. A rule only
appearing in the file is not evidence that the model followed it.

### Permissions demonstration

Follow the [permissions fixture exercise](01-project-setup/01_PROJECT_STRUCTURE.md).
Inspect the shared settings and use a dummy `.env` containing no real credentials.
Ask Claude to use only Read; observe the permission denial without trying another
tool. Contrast it with an allowed README read. Explain that these file-tool rules
are not an operating-system sandbox and do not cover every approved shell action.

### Independent exercise and debrief

Students add assignment rules to AGENTS.md and an evidence-table instruction to
CLAUDE.md, then test a fresh-session plan for assigning and clearing a user.
Use [the context lesson](01-project-setup/01_CLAUDE_SETUP.md) for the exact changes.

Ask: “What is guided by instructions, and what is enforced independently?”
Expected distinction: instructions shape behavior; permissions restrict tools;
database constraints and executable tests enforce application expectations.

**Exit gate:** baseline checks pass, the map cites real paths, loaded instructions
are observed, and students can explain the test/development database boundary.

## 4. Module 2: understand the application

Student route: [Module 2](02-application-fundamentals/README.md).

### Walk one request through the existing system

In terminal C:

```bash
sed -n '1,180p' issuetrackerapi/app/routes.py
sed -n '1,180p' issuetrackerapi/app/models/user.py
sed -n '1,180p' issuetrackerweb/src/js/services/UserService.js
sed -n '1,160p' issuetrackerweb/src/js/helpers/AppHelper.js
```

Ask students to trace login → token/header → protected route → operation/session →
response → React state. Use file evidence when someone proposes a convention.
Do not teach a new architecture before examining the template's existing one.

**Inside Claude:**

```text
Map the existing login and users request flow in the student apps. Read their
AGENTS.md files. Identify actual paths for authentication, User identity, operations,
SQLAlchemy sessions, migrations, list response envelopes, axios headers and routing.
Explain why the tracker cannot simply expose the admin-only /users list to everyone.
Do not edit source or read .env. Save workshop-output/milestones/exploration/map.md with
source-backed facts and a separate list of unresolved assumptions.
```

Expected: `/users` remains admin-only; the tracker needs safe authenticated assignee
selection. The course uses PostgreSQL explicitly although upstream defaults include
SQLite. The frontend uses HashRouter, esbuild and the existing header helper.

### Fact-check with a bounded reviewer

```text
Use workshop-reviewer to fact-check workshop-output/milestones/exploration/map.md against
SOFTWARE_SPECIFICATIONS.md, workflow/project.md, issuetrackerapi and issuetrackerweb.
Give it those paths explicitly. Focus on User ID type, authentication, pagination
and database configuration. Request discrepancies with source evidence, without
edits or command execution. Main session: save its returned report to
workshop-output/milestones/exploration/review.md and identify which claims need correction.
```

Show the named task and file reads. If the reviewer was not actually invoked,
record that and fix discovery; do not accept a main-session answer impersonating
a delegated review. The main session saves the report because this reviewer is
read-only. Detailed supervision is taught in Module 3.

### Independent exercise

Have students map a user update, then describe the Issue PATCH behavior they will
need: omitted fields are preserved; explicit null clears a nullable assignee.
They should also add a frontend scoped rule requiring labels, loading/error/empty
states and existing authentication headers, following the module walkthrough.

Debrief with “Which fact surprised you, and which proposed change did it prevent?”
Look for examples grounded in source rather than preference.

**Exit gate:** a verified application map and reviewer corrections, with no invented
endpoint conventions, duplicate User model, or undocumented authentication rewrite.

## 5. Module 3: reusable skills and supervised subagents

Student route: [Module 3](03-ai-development-workflow/README.md).
Reusable material: [workflow kit](workflow-kit/README.md).

### Explain the division of responsibilities

| Mechanism | Teaching purpose | Evidence of correct use |
|---|---|---|
| Project instructions | Stable constraints and context | Fresh-session behavior probe |
| Scoped rules | Guidance for matching files | Relevant rule applied to a bounded task |
| Plan Mode | Inspect and propose before implementation | Accepted plan naming files and checks |
| Skill | Repeated procedure with task arguments | Discovered invocation and useful output |
| Subagent | Separate, bounded review context | Named task, inspected inputs and findings |
| Hook | Deterministic event feedback | Isolated tests plus observed live activation |
| CI | Repeatable automated gates | Actual job results for the relevant revision |

### Demonstrate planning

Enter Plan Mode using the installed CLI's supported controls. Inside Claude:

```text
/workshop-plan 01-data Add Category and Issue models, migrations and an idempotent category seed only. Use SOFTWARE_SPECIFICATIONS.md and workshop-output/milestones/exploration/map.md. Reuse the existing User model. Identify concrete source paths, integrity constraints, migration risks and test commands. Do not implement endpoints or frontend code.
```

Discuss the plan before leaving Plan Mode. Check that it addresses case-insensitive
category uniqueness, category deletion protection, nullable user assignment,
existing user preservation, and verification. After accepting it and leaving Plan
Mode, paste:

```text
Save the accepted data-only plan to workshop-output/milestones/01-data/plan.md. Do not
implement it yet. Preserve the acceptance criteria and exact verification commands.
```

### Create and invoke a skill — Bash

Use an unused skill directory for the classroom exercise. If this example already
exists from a rehearsal, inspect it instead of overwriting student work.

```bash
mkdir -p .claude/skills/review-contract
cat > .claude/skills/review-contract/SKILL.md <<'SKILL'
---
name: review-contract
description: Compare a requested API change with the project contract and existing source.
disable-model-invocation: true
---
Read workflow/project.md and SOFTWARE_SPECIFICATIONS.md. Review $ARGUMENTS.
Inspect relevant schemas, controllers, operations and tests. Do not edit source.
Return a table: requirement, implementation path, test path, missing evidence,
and recommendation. Do not claim tests passed without supplied execution evidence.
SKILL
```

Explain the quoted heredoc: Bash preserves `$ARGUMENTS` for Claude to substitute
later. Restart Claude and inspect skill discovery. Inside Claude:

```text
/review-contract Category deletion when issues reference it
```

Before implementation, expect a gap report. Repeat after Module 4 and compare it
with the actual source and tests. A skill produces model-guided work; it is not
itself a deterministic test program.

**Independent:** students create `review-ui-state`, invoke it on the issue-form
plan, and later repeat it against the implementation. Require one deliberately
incomplete example to check whether it finds missing evidence.

### Create a specialized reviewer — Bash

Display the [installed reviewer template](workflow-kit/template/.claude/agents/workshop-reviewer.md).
The kit already installs ui-reviewer. To demonstrate creation, use this separate
accessibility-focused name only if it is not already in use:

```bash
mkdir -p .claude/agents
cat > .claude/agents/ui-accessibility-reviewer.md <<'AGENT'
---
name: ui-accessibility-reviewer
description: Read-only review of Issue Tracker accessible UI states.
tools: Read, Glob, Grep
---
Read AGENTS.md, workflow/project.md, the supplied plan and frontend paths.
Check visible labels, loading/error/empty states, authenticated API calls,
assignment clearing, filter reset, persistence and delete confirmation.
Do not edit files or run commands. Report verdict, findings with paths, missing
execution evidence and suggested tests. If input files are missing, say so.
AGENT
```

Restart and check `/agents`. Explain that omitting Bash/Edit/Write is intentional:
the reviewer inspects evidence while the main session owns execution and changes.

**Inside Claude — review the data plan:**

```text
Use workshop-reviewer to review workshop-output/milestones/01-data/plan.md. Supply
SOFTWARE_SPECIFICATIONS.md, workshop-output/milestones/exploration/map.md and issuetrackerapi
as explicit inputs. Ask for verdict, severity, source paths, integrity risks and
missing tests. Do not implement. Main session: save the returned review to
workshop-output/milestones/01-data/review.md and list decisions I need to resolve.
```

### How to supervise the actual task

1. Confirm a task for the named agent was created.
2. Expand its tool activity. Check whether it reads the assigned inputs.
3. For background tasks, inspect `/tasks` if supported in the installed CLI.
4. Use the UI stop control if the task leaves scope; give a corrected, narrower task.
5. Read the returned findings before accepting the verdict.
6. Have the main session save the report and reproduce actionable findings.

Use this status prompt when students cannot explain what their agent is doing:

```text
Report the actual delegated task name and status, input paths supplied, work
observed so far, output location, and any missing information. Distinguish running,
completed, failed and not invoked. Do not infer completion from a partial summary.
```

A separate context needs explicit inputs. Do not assume the reviewer knows every
conversation decision. Start with one writer and one reviewer; optional parallel
reviews can inspect separate scopes, but multiple writers need deliberate file
and database isolation.

**Independent:** give the reviewer a copy of a map with an incorrect port or an
unsupported pagination claim. Ask students whether it detects the error and what
source proves the correction. Do not corrupt real configuration for this exercise.

### Demonstrate a handoff

```text
Write workshop-output/milestones/01-data/handoff.md with the accepted plan, completed work,
actual commands and exit codes, remaining findings, and the next smallest task.
Separate tested facts from assumptions and omit credentials. Do not implement more.
```

Start a fresh Claude session and paste:

```text
Read workshop-output/milestones/01-data/handoff.md and workshop-output/milestones/01-data/plan.md.
Check their claims against the current source. Summarize the current state and
next bounded task; report stale assumptions before making changes.
```

**Exit gate:** accepted plan, saved review, custom skill invocation, and a handoff
that another session can use. Optional packaging/worktree exercises are in
[Module 3 extensions](03-ai-development-workflow/03_FEATURE_LABS.md).

## 6. Module 4: build verified increments

Use the following cycle for each increment. Instructor: demonstrate one bounded
change, assign the independent variation, then debrief using the acceptable and
inadequate outputs in [the recipes](CLAUDE_USE_CASES.md). This mirrors the
[student sequence](04-issue-tracker-implementation/README.md).

**Entry:** verified application map and accepted data plan. **Result:** complete
Issue Tracker. Use the [specification](SOFTWARE_SPECIFICATIONS.md) and
[workflow recipes](CLAUDE_USE_CASES.md). Read each app's AGENTS.md. Student apps
are the active workspace; consult the instructor solution only after an attempt.

### Required cycle for every increment

1. Invoke the planning prompt below in Plan Mode. Inspect source paths, scope and checks.
2. Accept the plan, leave Plan Mode, and explicitly ask Claude to save it to the
   milestone's `plan.md` without implementing yet. Saving alone is not approval.
3. Invoke the listed implementation command. It requires that explicit acceptance.
4. Run the Bash gate yourself, then the verification skill and a bounded review.
5. Repair confirmed failures within accepted scope; rerun affected checks and save
   evidence/handoff. Review the diff before committing in the affected app repo.

Every milestone directory is `workshop-output/milestones/<id>/`. Preserve earlier
plans/reviews/logs. Record workspace, app revisions, dirty state and actual outcomes.
The [use-case guide](CLAUDE_USE_CASES.md) contains exact save, review and repair
patterns. The commands below are **inside Claude** unless marked Bash.

### 1. Data — 01-data

```text
/workshop-plan 01-data Inspect issuetrackerapi and plan only the persistence slice: Category and Issue, existing string UUID User references, case-insensitive uniqueness, category RESTRICT/user SET NULL, status/priority constraints, UTC timestamps, migration and idempotent category seed. Preserve users. Identify integrity and migration checks before implementation.
```

Accept/save to `workshop-output/milestones/01-data/plan.md`, then:

```text
/workshop-implement 01-data workshop-output/milestones/01-data/plan.md
```

**Bash:**

```bash
./workshop db migrate
./workshop db seed
./workshop db seed
./workshop test
```

Expected: existing users preserved; repeated category seed does not duplicate the
four sample categories. The local demo seed updates `admin@example.com` / `password`;
never target a real deployment. Independent: prove database uniqueness and user
preservation during migration. Recovery checkpoint: `01-data`.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 01-data workshop-output/milestones/01-data/plan.md Verify the accepted increment and report criterion-level evidence.
```

### 2. Categories — 02-categories

```text
/workshop-plan 02-categories Inspect existing backend patterns and add authenticated category CRUD only. Trim/validate names, enforce case-insensitive uniqueness, paginate alphabetically and reject deletion of linked categories with 409. Add spec/tracker/test_categories.py. No issue endpoints or frontend changes.
```

Accept/save to `workshop-output/milestones/02-categories/plan.md`, then:

```text
/workshop-implement 02-categories workshop-output/milestones/02-categories/plan.md
```

**Bash:**

```bash
./workshop test spec/tracker/test_categories.py
```

Expected: 201 create, 409 duplicate/protected deletion, 422 invalid input, 404 missing,
204 empty successful delete. Independent: duplicate rename and association preservation.
Recovery checkpoint: `02-categories`.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 02-categories workshop-output/milestones/02-categories/plan.md Verify the accepted increment and report criterion-level evidence.
```

### 3. Issues — 03-issues

```text
/workshop-plan 03-issues Inspect Category/User integration and add authenticated issue CRUD. Validate title/description/status/priority and references; default open/medium. Preserve omitted PATCH fields and allow null only for nullable fields. Return safe display data. Add spec/tracker/test_issues.py. No UI changes.
```

Accept/save to `workshop-output/milestones/03-issues/plan.md`, then:

```text
/workshop-implement 03-issues workshop-output/milestones/03-issues/plan.md
```

**Bash:**

```bash
./workshop test spec/tracker/test_issues.py
```

Independent: boundary lengths, whitespace-only title and unauthenticated writes.
Recovery checkpoint: `03-issues`.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 03-issues workshop-output/milestones/03-issues/plan.md Verify the accepted increment and report criterion-level evidence.
```

### 4. Assignment — 04-assignment

```text
/workshop-plan 04-assignment Inspect current assignment behavior. Add authenticated read-only GET /assignees returning only ID/full_name for non-deleted existing users. Preserve admin-only /users. Test assign, omitted-field preservation, invalid reference, null clearing and ordinary-user access in spec/tracker/test_assignment.py.
```

Accept/save to `workshop-output/milestones/04-assignment/plan.md`, then:

```text
/workshop-implement 04-assignment workshop-output/milestones/04-assignment/plan.md
```

**Bash:**

```bash
./workshop test spec/tracker/test_assignment.py
```

Independent: verify ordinary-user assignee access without exposing /users or sensitive
fields. Complete the [assignment diagnosis](04-issue-tracker-implementation/03_DIAGNOSTIC_LAB.md). Recovery: `04-assignment`.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 04-assignment workshop-output/milestones/04-assignment/plan.md Verify the accepted increment and report criterion-level evidence.
```

### 5. Filters — 05-filters

```text
/workshop-plan 05-filters Inspect issue listing and add literal case-insensitive title substring search plus AND-combined status, priority, category_id and assigned_user_id filters. Preserve pagination. Sort updated_at descending then ID. Test literal percent/underscore, no matches and equal-timestamp pagination in spec/tracker/test_filters.py.
```

Accept/save to `workshop-output/milestones/05-filters/plan.md`, then:

```text
/workshop-implement 05-filters workshop-output/milestones/05-filters/plan.md
```

**Bash:**

```bash
./workshop test spec/tracker/test_filters.py
```

Independent: equal-timestamp paging without repetition or omission. Recovery: `05-filters`.

### 6. Frontend — four teaching increments

These four IDs organize evidence, **not recovery snapshots**. The existing
`06-frontend` checkpoint restores the completed UI only. Each prompt must produce
an accepted plan before the corresponding implementation invocation.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 05-filters workshop-output/milestones/05-filters/plan.md Verify the accepted increment and report criterion-level evidence.
```

#### 06a-categories-ui: category management

```text
/workshop-plan 06a-categories-ui Inspect the existing React layout, routing and services. Add category navigation/list/create/edit/delete using real API calls and existing auth headers. Include labels, loading/error/empty states and protected-deletion feedback. Add exact Playwright dev dependency, configuration, test:e2e script and a focused category browser test. Do not build issue screens yet.
```

Accept/save to `workshop-output/milestones/06a-categories-ui/plan.md`, then:

```text
/workshop-implement 06a-categories-ui workshop-output/milestones/06a-categories-ui/plan.md
```

Observe create/edit/delete and validation feedback in the browser. Independent:
verify an API error is visible rather than rendered as an empty successful list.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 06a-categories-ui workshop-output/milestones/06a-categories-ui/plan.md Verify the accepted increment and report criterion-level evidence.
```

#### 06b-issue-create-details: creation and persistence

```text
/workshop-plan 06b-issue-create-details Inspect the completed category UI. Add issue listing, creation and details using real endpoints. Fetch all category option pages and safe assignees. Include required labels, validation, loading/error/empty states. Extend browser tests to create an issue and verify details after reload. No editing/filtering/deletion yet.
```

Accept/save to `workshop-output/milestones/06b-issue-create-details/plan.md`, then:

```text
/workshop-implement 06b-issue-create-details workshop-output/milestones/06b-issue-create-details/plan.md
```

Observe creation through the form and persisted details after reload. Independent:
no categories available must produce useful guidance rather than an unusable save.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 06b-issue-create-details workshop-output/milestones/06b-issue-create-details/plan.md Verify the accepted increment and report criterion-level evidence.
```

#### 06c-edit-assignment: updates and clearing

```text
/workshop-plan 06c-edit-assignment Add issue editing through existing services. Persist category, status, priority and assignee changes. Distinguish omitted fields from null clearing. Extend browser tests to edit/reload and unassign/reload. Keep authentication and existing pages intact.
```

Accept/save to `workshop-output/milestones/06c-edit-assignment/plan.md`, then:

```text
/workshop-implement 06c-edit-assignment workshop-output/milestones/06c-edit-assignment/plan.md
```

Observe changed fields after reload and an unassigned issue after explicit clearing.
Independent: reproduce a rejected API update and verify the UI explains it.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 06c-edit-assignment workshop-output/milestones/06c-edit-assignment/plan.md Verify the accepted increment and report criterion-level evidence.
```

#### 06d-filters-deletion: discovery and confirmed removal

```text
/workshop-plan 06d-filters-deletion Add issue search, combined filters/reset, pagination and delete confirmation. Extend browser tests for matching/nonmatching results, reset, cancel and confirm deletion and category conflict feedback. Preserve existing issue/category behaviors and complete the specification's browser lifecycle.
```

Accept/save to `workshop-output/milestones/06d-filters-deletion/plan.md`, then:

```text
/workshop-implement 06d-filters-deletion workshop-output/milestones/06d-filters-deletion/plan.md
```

Observe filtered matches, reset, cancellation preserving an issue, and confirmed
removal. Independent: no matches and network error must remain distinct UI states.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 06d-filters-deletion workshop-output/milestones/06d-filters-deletion/plan.md Verify the accepted increment and report criterion-level evidence.
```

#### Browser gates for each increment

Run **Bash** after implementation:

```bash
./workshop build
(cd issuetrackerweb && npx playwright install chromium)
```

Start API and web in separate root terminals and keep them running:

```bash
./workshop start api
```

```bash
./workshop start web
```

In a third terminal:

```bash
./workshop e2e
```

Use `http://localhost:8000/#/login` with the local demo account. Each increment adds
tests for implemented behavior only; do not run tests for future screens as a passing
gate. For missing Linux browser libraries, follow Playwright's system-dependency setup.
At the completed frontend milestone, run `./workshop test` and the full browser suite.

### Verification, review and repair example

For categories, invoke:

```text
/workshop-verify 02-categories workshop-output/milestones/02-categories/plan.md Category CRUD and integrity
```

Use the same pattern with the exact milestone ID/plan for every increment.

```text
Use backend-reviewer for milestone 02-categories. Supply its plan, specification,
issuetrackerapi and milestone evidence/logs. Request path-backed contract/auth/
integrity findings without edits or commands. Main session: save review.md in that
milestone, reproduce findings and classify each as confirmed, rejected with evidence
or needing more evidence. Do not inspect instructor-reference.
```

Use ui-reviewer for frontend increments. Monitor actual tasks and file reads; a
reviewer's verdict cannot replace Bash/browser results. For a confirmed defect,
use the bounded repair prompt in the [recipes](CLAUDE_USE_CASES.md). Preserve
failed-run evidence and append the repaired run. Review diffs and commit in the
affected app repository once the gate passes.

**Exit:** the complete real browser lifecycle works. Continue to
[Module 5](05-testing-debugging-and-demo/README.md).

Apply this workflow in the [diagnostic lab](04-issue-tracker-implementation/03_DIAGNOSTIC_LAB.md).

## 7. Module 5: verification, debugging, and handoff

Student route: [Module 5](05-testing-debugging-and-demo/README.md).

### Establish the final acceptance plan

Inside Claude, use `/workshop-plan final Verify the complete specification against
the active student application; plan checks only, with no new feature work.` Review
and accept that plan, leave Plan Mode, and save it to
`workshop-output/milestones/final/plan.md` before invoking final verification.

### Capture real evidence

With both student servers running, use terminal C:

```bash
mkdir -p workshop-output/milestones/final/logs
set -o pipefail
workshop_run_id=$(date -u +%Y%m%dT%H%M%SZ)
./workshop test 2>&1 | tee "workshop-output/milestones/final/logs/${workshop_run_id}-backend.log"
./workshop build 2>&1 | tee "workshop-output/milestones/final/logs/${workshop_run_id}-build.log"
./workshop e2e 2>&1 | tee "workshop-output/milestones/final/logs/${workshop_run_id}-browser.log"
git -C issuetrackerapi rev-parse HEAD
git -C issuetrackerweb rev-parse HEAD
git -C issuetrackerapi status --short
git -C issuetrackerweb status --short
```

Explain `pipefail`: a log file can exist even when the command failed. Record each
command's outcome before proceeding. Record both revision and dirty state; a commit
ID alone does not identify uncommitted code used by the test.

**Inside Claude:**

```text
/workshop-verify final workshop-output/milestones/final/plan.md Compare the completed student tracker against SOFTWARE_SPECIFICATIONS.md. Inspect the latest timestamped backend/build/browser logs in workshop-output/milestones/final/logs and the current source. Run required checks if evidence is stale. Produce a pass/fail/not-run table per acceptance criterion with paths and actual execution evidence. Identify gaps without claiming source inspection proves browser behavior.
```

### Teach regression debugging

Have students create a Git branch from a passing state. Using a small reversible
edit, remove omitted-field preservation from Issue PATCH. Run the assignment test
and observe a failure. Restore the implementation and rerun the focused check.
Use the [assignment reference](instructor-reference/issuetrackerapi/spec/tracker/test_assignment.py)
to discuss what the failing assertion means; do not simply copy the solution.

**Inside Claude:**

```text
Investigate the failing assignment regression. Read the test, implementation and
failure output. Explain the expected versus observed behavior and the smallest
plausible cause. Propose a minimal repair and verification command before editing.
Do not weaken assertions, skip the test or change the API contract to obtain a pass.
```

**Independent:** students reproduce a different defect, document its cause, and
show a regression that fails before the repair and passes afterward. Keep the
intentional defect out of the final working application.

### Demonstrate a hook with observable activation

Follow [the full hook lab](05-testing-debugging-and-demo/02_HOOKS_EXTENSION.md).
First run isolated fixtures:

```bash
python3 05-testing-debugging-and-demo/examples/hooks/test_check_python_syntax.py
mkdir -p .claude/hooks
cp -n 05-testing-debugging-and-demo/examples/hooks/check_python_syntax.py .claude/hooks/check_python_syntax.py
```

Open the [settings fragment](05-testing-debugging-and-demo/examples/hooks/settings.fragment.json).
Merge its PostToolUse entry into `.claude/settings.local.json` without replacing
other hooks or permissions. Restart Claude and inspect `/hooks`.

Choose an unused fixture filename; then paste inside Claude:

```text
Using only Write, create issuetrackerapi/workshop_syntax_fixture.py containing
value = 1. Do not import or execute it. Report the syntax hook's observed feedback.
```

Then:

```text
Using Edit or Write, change only issuetrackerapi/workshop_syntax_fixture.py to the
intentionally invalid Python text: def broken(:
Stop without repairing it. Report the hook's actual feedback and line number.
```

Then:

```text
Using Edit or Write, restore only issuetrackerapi/workshop_syntax_fixture.py to
value = 1. Report the observed hook feedback. Do not modify application files.
```

Expected: success, syntax failure, success. If the hook does not fire, diagnose
configuration instead of accepting the model's guess. Remove only the disposable
fixture afterward. Explain that PostToolUse happens after the edit; it neither
undoes the edit nor proves business behavior. Shell-based edits are not covered
by this particular Edit/Write matcher.

### Final reviewer and handoff

```text
Use workshop-reviewer to compare the specification, accepted plan, completed source
and current verification logs. Ask for unmet criteria, stale evidence and remaining
risks. Do not edit. Save the report to workshop-output/milestones/final/review.md in the main
session. After findings are resolved, write workshop-output/milestones/final/handoff.md with
launch commands, ports, migration state, revisions/dirty state, actual check results,
known limitations and a reproducible browser demonstration. Omit credentials.
```

Show the [GitHub Actions workflow](.github/workflows/workshop.yml). Explain that it
runs deterministic reference checks and does not need a Claude API key. A workflow
file existing is not evidence that a remote job passed; inspect actual GitHub runs
once the repository is published.

**Optional extensions:** [headless review](05-testing-debugging-and-demo/03_FEATURE_LABS.md),
[plugins/worktrees](03-ai-development-workflow/03_FEATURE_LABS.md), and
[MCP/parallel review](04-issue-tracker-implementation/02_FEATURE_LABS.md).
They do not replace required application gates.

## 8. Recovery and classroom troubleshooting

### Recover without overwriting student work

Use recovery when a learner understands the failure but needs a known state to
continue. Require a short explanation of the recovered change and rerun its gate.
Never use `git reset --hard`, delete a student's folders, or apply cumulative
patches on top of one another as a classroom shortcut.

First stop the student's API/web with Ctrl+C in their respective terminals. Then:

```bash
./workshop db stop
./workshop recover 06-frontend recovery/classroom-completed
./workshop --workspace recovery/classroom-completed setup
./workshop --workspace recovery/classroom-completed db up
./workshop --workspace recovery/classroom-completed db migrate
./workshop --workspace recovery/classroom-completed db seed
./workshop --workspace recovery/classroom-completed test
./workshop --workspace recovery/classroom-completed build
```

The destination must not exist. On a repeat exercise, choose a new directory name;
do not delete the earlier recovery just to rerun this block. For an earlier slice,
choose its milestone from the [checkpoint table](checkpoints/README.md). `00-baseline`
does not yet have the category seed, so omit `db seed` at that milestone.

Run recovered servers in separate terminals:

```bash
./workshop --workspace recovery/classroom-completed start api
```

```bash
./workshop --workspace recovery/classroom-completed start web
```

Install Chromium in the recovered web directory if needed, then use the same
workspace selector for `e2e`. Keep Claude at the course root and explicitly redirect it:

```text
For this exercise the active applications are
recovery/classroom-completed/issuetrackerapi and
recovery/classroom-completed/issuetrackerweb. Use the course runner with
--workspace recovery/classroom-completed for every command. Do not edit or run the
root student apps or instructor reference. Read the current handoff and compare
this recovered implementation with the accepted plan before continuing.
```

### Troubleshooting table

| Symptom | First inspection | Instructor action |
|---|---|---|
| `./workshop` not found | `pwd`, course root contents | Return to the course root; do not invent another setup command |
| Permission denied on launcher | Executable mode on `workshop` | Restore executable permission in the course checkout |
| Python/Node version mismatch | `./workshop doctor` output | Use the documented versions; rerun setup afterward |
| Docker inaccessible | Docker daemon and user access | Resolve host setup before the database lab |
| Port already occupied | Running student/reference/recovery terminals | Stop the conflicting workspace; do not delete volumes |
| Setup preserves an old `.env` | File presence and intended workspace | Review locally without exposing values; setup intentionally does not overwrite |
| Migration/seed missing | Current checkpoint and command selector | Apply migration first; seed only after data slice exists |
| Login fails | Correct port and seeded workspace | Check local seed and API connectivity; Claude credentials are unrelated |
| Skill not discovered | File location, name, restart, `/help` | Verify project root and SKILL.md frontmatter |
| Reviewer never invoked | `/agents` and actual task activity | Restart after definition changes and delegate with explicit inputs |
| Reviewer says “passed” without logs | Its allowed tools and supplied evidence | Require missing checks to be marked not run |
| Pytest flags rejected by launcher | Argument separator | Use `./workshop test -- -q spec/tracker/test_assignment.py` |
| Test DB guard refuses execution | Selected workspace and runner environment | Use the dedicated test target; do not remove the guard |
| Browser cannot launch | Chromium install and missing OS libraries | Complete browser installation before diagnosing UI code |
| Browser test fails after saving | Trace, API response, awaited navigation | Diagnose the actual behavior; do not add arbitrary sleeps as the first fix |
| Build passes but UI fails | Browser console and real API/network behavior | Run the browser gate; a bundle alone is insufficient |
| Hook fixture tests pass but no live feedback | Matcher, settings scope, restart | Observe real Write/Edit activation before calling it installed |
| Context becomes stale | Current plan, handoff and source | Save evidence and start a fresh session with explicit paths |

When a failure affects the whole class, pause the shared demo and reproduce it in
the reference. When it affects one learner, inspect their workspace and evidence
before modifying the common course instructions.

## 9. Assessment and closing

### Acceptance demonstration

Have each learner demonstrate the specification's workflow on their own application:
login, category creation, issue creation, assignment, status/priority edits,
combined filtering, persistence after reload, unassignment, deletion cancellation,
confirmed issue deletion, and category deletion protection. Require visible error
handling and at least one empty state.

### Suggested assessment rubric

Score each area 0 (missing), 1 (partially demonstrated) or 2 (demonstrated with evidence).
The scoring organizes feedback; it does not excuse a failed required application gate.

| Area | Full-credit evidence |
|---|---|
| Reproducibility | Another person can follow the setup and handoff |
| Context and planning | Correct imported guidance, bounded plan, source-backed map |
| Data/API correctness | Constraints, validation, authentication and regressions |
| UI integration | Real endpoints, persistence and required UI states |
| Claude engineering | Working custom skill, actual bounded reviewer and inspected findings |
| Verification | Current backend/build/browser results with honest limitations |
| Transferability | Generic kit adapted to a different project's real commands |

Do not pass a broken integration because its prompts are well written. Conversely,
ask learners with a working application to explain the evidence and workflow rather
than assessing only the final screenshot.

### Transfer exercise

```text
Review our workflow kit for reuse in another project. Identify which instructions
are generic and which facts belong in workflow/project.md. Propose replacements
for paths, runtime commands, test isolation, acceptance criteria and review scopes.
Do not copy Issue Tracker credentials or ports into the new project. Give a small
behavior probe and deterministic check to validate the adapted workflow.
```

Debrief: “What would you keep, change, and test first in your next project?”
Look for thoughtful adaptation rather than copying every setting unchanged.

### Shutdown

Stop foreground API/web processes with Ctrl+C. Stop only the databases you used:

```bash
./workshop db stop
./workshop --reference db stop
```

If you used the recovery example, stop that workspace too:

```bash
./workshop --workspace recovery/classroom-completed db stop
```

Development volumes persist. Preserve student source and handoffs. Do not run
volume deletion commands as a routine class cleanup step.

## 10. Preparing the course for GitHub

The top-level [.gitignore](.gitignore) separates distributable course material
from local work. Root-only `/issuetrackerapi/` and `/issuetrackerweb/` rules exclude
the generated student repositories while retaining identically named directories
under `instructor-reference/`. Removing the leading slash would hide the reference.

| Include in the course repository | Keep out of the course repository |
|---|---|
| Module docs, GUIDE, specification and original PDF | Local workshop logs, maps, plans and handoffs |
| Reference source and dependency lockfiles | Dependencies, virtual environments and caches |
| Checkpoint patches and launcher/tooling | Recovery copies and local template Git metadata |
| Shared `.claude` rules, agents, skills and settings | Machine-local Claude settings and CLAUDE.local.md |
| Workflow templates and CI configuration | Runtime `.env` files, databases and browser reports |

Reviewed `.env.example`, `.env.sample` and `.env.dist` templates remain eligible.
The explicit reference `.env.test` exception preserves the supplied non-production
test fixture. Do not put real credentials into these tracked examples. Ignore rules
do not inspect file contents and do not remove files already tracked by Git.

The instructor reference is ordinary source, not nested Git submodules. Student
application repositories are independent: their commits are not included by
committing the course repository. Publish those separately only if you intend to.

### Review before your own commit

The following are instructions for the person publishing the course; they are not
part of the student implementation lab. If the course directory is not yet a Git
repository, initialize it once:

```bash
git init
```

Inspect status, ignore rules and documentation before staging:

```bash
git status --short --untracked-files=normal
python3 tools/check_docs.py
git check-ignore -v --no-index issuetrackerapi/.env instructor-reference/issuetrackerapi/.env
```

Expected: both runtime paths are ignored. Check the opposite case:

```bash
git check-ignore -v --no-index instructor-reference/issuetrackerapi/app/models/tracker.py instructor-reference/issuetrackerweb/package-lock.json
```

Expected: no matching ignore rule and exit status 1 for these eligible source files.
For this Git command, that status is the intended result, not a failed application test.

After reviewing the files, stage and inspect locally:

```bash
git add --dry-run .
git add .
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git ls-files --stage | awk '$1 == "160000" { print }'
```

The final command should not list the instructor apps as Git links. If it does,
inspect nested repository metadata before proceeding; do not blindly delete it.
Review staged content as well as names for credentials or private notes. Verify
reference source, locks, shared Claude files, CI, checkpoints and the PDF are present.
Do not use `git add -f` to bypass exclusions as a shortcut.

When satisfied, make your own commit and configure the intended GitHub remote.
This guide does not prescribe an account or repository URL. After pushing, inspect
GitHub Actions results and rehearse from a fresh clone; local success does not prove
that every necessary file was committed or that remote CI passed.

## 11. Instructor reference map

| Need | Repository reference |
|---|---|
| Student entry point | [README](README.md) |
| Application acceptance criteria | [Specification](SOFTWARE_SPECIFICATIONS.md) |
| Shared repository guidance | [AGENTS](AGENTS.md), [Claude entry](CLAUDE.md), [project profile](workflow/project.md) |
| Account/VS Code preparation | [Terminal guide](CLAUDE_CODE_TERMINAL.md), [VS Code guide](CLAUDE_CODE_VSCODE_SETUP.md) |
| Required teaching sequence | [Module 1](01-project-setup/README.md), [Module 2](02-application-fundamentals/README.md), [Module 3](03-ai-development-workflow/README.md), [Module 4](04-issue-tracker-implementation/README.md), [Module 5](05-testing-debugging-and-demo/README.md) |
| Reusable configuration | [Kit](workflow-kit/README.md), [plan skill](workflow-kit/template/.claude/skills/workshop-plan/SKILL.md), [verification skill](workflow-kit/template/.claude/skills/workshop-verify/SKILL.md) |
| Completed application | [Reference launch guide](instructor-reference/README.md) |
| Known-state recovery | [Checkpoint guide](checkpoints/README.md) |
| Command implementation | [Launcher](workshop), [runner](tools/workshop.py), [Compose](compose.workshop.yml) |
| Hook implementation and fixtures | [Hook lab](05-testing-debugging-and-demo/02_HOOKS_EXTENSION.md) |
| Automation | [CI](.github/workflows/workshop.yml), [documentation checker](tools/check_docs.py) |
| Evidence and course design rationale | [Validation](VALIDATION.md), [review findings](WORKSHOP_REVIEW.md) |

For version-specific Claude behavior, use the official documentation linked from
the setup guides and Module 3, then verify the behavior in the installed client.
Keep instructor notes about changed behavior separate from untested assumptions.

## Diagnostic facilitation supplements

Choose the workflow using [the use-case table](CLAUDE_USE_CASES.md). Run a guided
scenario, inspect its expected output, then assign the independent variation:

- Module 1: [setup diagnosis](01-project-setup/DIAGNOSTIC_LAB.md).
- Module 2: [authorization investigation](02-application-fundamentals/DIAGNOSTIC_LAB.md).
- Module 3: [contradictions and failed delegation](03-ai-development-workflow/DIAGNOSTIC_LAB.md).
- Module 4: [assignment and UI diagnosis](04-issue-tracker-implementation/03_DIAGNOSTIC_LAB.md).
- Module 5: [browser evidence diagnosis](05-testing-debugging-and-demo/DIAGNOSTIC_LAB.md).

A correct no-change diagnosis is valuable: intended authorization behavior and a
stopped service do not require source repairs. For delegated tasks, inspect actual
agent identity, input paths, tool activity and report, then have the main session
reproduce findings. Require students to distinguish proposed tests from executed tests.
