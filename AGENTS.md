# Workshop repository guidance

## Purpose and layout

This repository teaches AI-assisted full-stack development with Claude through an Issue Tracker capstone. Keep material accessible to new developers in a completion-first, multi-session workshop. Advance by verified exit gates.

- `01-project-setup/`: tools, template setup, and connectivity.
- `02-application-fundamentals/`: request flow, APIs, databases, and Docker.
- `03-ai-development-workflow/`: exploration, planning, instructions, and reusable skills.
- `04-issue-tracker-implementation/`: database, backend, and frontend feature work.
- `05-testing-debugging-and-demo/`: verification, debugging, and demonstration.
- `issuetrackerapi/` and `issuetrackerweb/`: intended backend and frontend locations at the repository root. Participants create these from the templates during lesson 1; they are not included in the initial workshop scaffold.

Each lesson README is the canonical sequential walkthrough with prerequisites, guided and independent exercises, and executable exit gates. Keep the root README's lesson index and layout consistent with these folders.

## Sources of truth

Read `SOFTWARE_SPECIFICATIONS.md` before planning or implementing capstone features. It defines functional behavior and acceptance criteria; reference it instead of duplicating its full contract. Preserve the source course-outline PDF.

Inspect both application templates and their local instructions before selecting paths, runtime versions, installation commands, environment variables, ports, API prefixes, migrations, or test commands. Record verified commands in the relevant lesson when developing detailed exercises. Do not present illustrative commands or unperformed checks as verified facts.

## Development constraints

- Extend existing template patterns, UI components, configuration, and authentication.
- Add only Category and Issue as new domain models. Reuse the existing User model for assignment.
- Follow the specification's validation, integrity, search/filtering, and error-handling requirements.
- Keep changes focused; avoid unrelated refactors or unnecessary dependencies.
- Keep secrets out of documentation, prompts, logs, and commits. Use environment configuration.
- Distinguish lesson outlines from implemented features and completed exercises.
- Keep application repositories' own instructions and Git checkpoints when they are cloned independently. Ensure the agent can read the root specification and guidance; do not assume every tool automatically loads `AGENTS.md`.

## Workflow and verification

Explore → plan → implement → verify. Explain assumptions and make small, reviewable changes.

For documentation changes, check lesson coverage, relative links, directory names, and consistency with the specification. For application changes, discover and run the smallest relevant checks first, then the required backend tests and frontend checks. Use the specification's browser demonstration for end-to-end acceptance.

Report what changed, what checks actually ran, and any remaining limitations. Never claim a test, build, or browser walkthrough passed without running it.

## Milestone evidence and Claude task selection

Separate observed baseline behavior from target requirements. Select the active
workspace explicitly; inspect reference/recovery source only when assigned.
Use milestone-specific plan, review, evidence and handoff files under
workshop-output/milestones/. Preserve earlier runs and record revision/dirty state.
Choose direct edits for trivial scoped work, planning for uncertain changes, and
bounded read-only delegation for independent questions. Main-session execution
and review findings are distinct evidence. See CLAUDE_USE_CASES.md in this course
for recipes; adapt that reference when transferring the kit to another project.
