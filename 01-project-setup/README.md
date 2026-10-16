# Module 1 — Establish a reproducible workspace manually

**Entry:** Python 3.14, Node 24, Git, Claude Code, and Bash or PowerShell 7.4+.
**Result:** pinned application repositories, SQLite, explicit instructions and a
verified baseline. No Docker, installer or course launcher is required.

Install Claude using [terminal setup](../CLAUDE_CODE_TERMINAL.md) or
[VS Code setup](../CLAUDE_CODE_VSCODE_SETUP.md). Windows participants start with
[Windows setup](../WINDOWS_SETUP.md). The downloaded course is reference material;
your active project root is a new sibling folder containing both application repos.

## 1. Create the workspace, install, and test

Follow these steps in order. Each linked section includes exact file contents,
working directories and Bash/PowerShell alternatives. Run only your shell's block.

1. Inspect the [folder diagram](../GUIDE.md#m1-folder-diagram-and-ownership).
2. [Clone pinned templates and apply baseline source patches](../GUIDE.md#m2-clone-the-pinned-templates-explicitly) into a new destination. The patches supply compatibility fixes, not tracker features.
3. [Write AGENTS.md, CLAUDE.md and settings](../GUIDE.md#m3-write-the-root-instructions-yourself), and copy the supplied SQLite project profile as instructed. Preserve app-local instructions.
4. [Create SQLite storage](../GUIDE.md#m4-prepare-sqlite-storage), then [install locked dependencies and configure environments](../GUIDE.md#m5-install-dependencies-and-configure-the-applications).
5. [Migrate, seed the existing admin and start servers](../GUIDE.md#m6-migrate-seed-the-existing-login-and-start-both-servers).
6. [Run the isolated baseline tests/build and inspect a Git checkpoint](../GUIDE.md#m7-verify-the-baseline-directly-and-save-a-git-checkpoint). Record actual output and skips.

Expected: migration `0002_add_role_to_users`, existing users/authentication, and
passing baseline checks. Category/Issue are not implemented. The development file
is `issuetrackerapi/storage/development.sqlite3`; tests use `issuetrackerapi/test.sqlite3`.
Only the existing admin seed is available now. Add the tracker seed in Module 4.

## 2. Validate instructions, not just file existence

Read [project structure](01_PROJECT_STRUCTURE.md) and
[modify/test Claude context](01_CLAUDE_SETUP.md). Start `claude` from the active root.
Use `/memory` and inspect the actual file reads to verify loading.

**Guided prompt inside Claude:**

```text
Read CLAUDE.md, AGENTS.md, workflow/project.md, SOFTWARE_SPECIFICATIONS.md and both
application AGENTS.md files. Analyze this workspace without editing app source or
reading environment files. Identify the loaded instructions, app responsibilities,
User model/type, API/web ports and the exact SQLite test file. Cite paths. Save the
analysis to workshop-output/milestones/setup/map.md. Mark unknowns explicitly.
```

**Independent:** add a shared rule requiring migration review before relationship
changes and a Claude instruction requiring a short evidence table. Restart and ask
for a category foreign-key plan without implementation. Verify the response follows
both rules; record misses and revise rather than assuming a file was loaded.

## 3. Create and supervise a reviewer

Follow [manual subagent creation](../GUIDE.md#m8-create-and-invoke-subagents-yourself)
to create architecture-reviewer and acceptance-reviewer. Restart Claude, inspect
`/agents` or the installed client's help, then explicitly delegate:

```text
Use acceptance-reviewer to inspect workshop-output/milestones/setup/map.md against
workflow/project.md and both app instructions/source paths. Return unsupported
claims with file evidence; no edits or commands. Main session: save the returned
report to workshop-output/milestones/setup/review.md and check each finding.
```

Expand the named delegation row and inspect actual tools, inputs and output.
Missing task activity means delegation was not demonstrated. **Independent:** put
a wrong API port in a copy of the map and ask the reviewer to detect it; repair the
map, not the real application configuration.

**Exit gate:** baseline tests/build pass, context imports are observed, reviewer
activity is real, and the map names correct app paths, ports and SQLite test target.
Stop servers with Ctrl+C when needed; there is no database service to stop.
Next: [Module 2](../02-application-fundamentals/README.md).
Apply the workflow in the [diagnostic lab](DIAGNOSTIC_LAB.md).
