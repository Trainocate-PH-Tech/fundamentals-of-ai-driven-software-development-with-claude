# Project structure and instruction ownership

Follow Module 1's direct clone/file-creation steps. Open the new active project root:

```text
issue-tracker-manual/
├── issuetrackerapi/       # independent Git repo: FastAPI, models, migrations, specs
├── issuetrackerweb/       # independent Git repo: React, services, routes, build
├── AGENTS.md             # shared engineering and course contract
├── CLAUDE.md             # Claude entry point; imports shared instructions
├── workflow/project.md   # project-specific paths, commands and contract
├── .claude/              # skills, scoped rules, reviewer definitions
├── workshop-output/      # ignored maps, plans, reports and handoffs
└── SOFTWARE_SPECIFICATIONS.md # copied behavior contract
```

AGENTS.md is a convention used by several coding agents; support and inheritance
vary by tool. Claude Code loads CLAUDE.md and supports explicit imports. Therefore
our CLAUDE.md contains `@AGENTS.md` rather than assuming automatic discovery.
Keep common behavioral rules in AGENTS.md; put Claude imports and Claude-specific
workflow guidance in CLAUDE.md. Avoid duplicating the specification in either.
Nested app AGENTS.md files contain template conventions: explicitly read them
when working in that app. Do not assume importing the root file imports nested files.

## Exercise: prove project analysis respects context

Inside Claude, request the Module 1 read-only analysis. Compare its claims with
`app/models/user.py`, `app/routes.py`, `src/js/App.js`, and `build.js` in the apps.
Check that it identifies string UUID IDs, no route prefix, HashRouter, and JWT.
Ask which instruction files it actually read. Save mistakes and corrections in
`workshop-output/milestones/final/logs/context.md`. Repeat in a fresh session after editing
instructions: do not use the same conversation as the sole test of loading.

## Exercise: guardrails with independent enforcement

Add this shared rule to root AGENTS.md:

```markdown
Before a schema change, identify the migration, rollback implications, existing
User data impact, and a test of referential integrity. Run pytest directly from
the API directory with APP_ENV=test and DATABASE_URL=sqlite:///test.sqlite3. Never run destructive fixtures against development or production databases.
```

Ask Claude to propose running tests against the development database. It should
reject that approach and select the isolated SQLite test environment. This checks
instruction adherence, not a security boundary. Inspect spec/conftest.py and
spec/system/test_test_environment.py: fixtures drop tables and the SQLite assertion
expects test.sqlite3. A mistaken URL can be destructive before an assertion runs;
explicitly inspect the chosen command/environment before authorizing it.
Database constraints enforce relationships even if an agent omits validation.

Best practices: keep rules short and observable, define safe alternatives, test
both allowed and disallowed cases using disposable fixtures, and use least-privilege
permissions. Hooks can catch mistakes but do not sandbox arbitrary shell commands.
Never test a dangerous command on real data merely to see whether Claude refuses.

## Exercise: inspect permissions independently

Create .claude/settings.json using the guide's manual file contents. If settings
already exist, merge the Read/Edit/Write deny entries yourself without replacing
other permissions. Restart Claude and inspect /permissions. Do not treat tool
permissions as an OS sandbox or authorize shell commands that expose secrets.

Use a dummy file with no secret to test the rule:

```bash
mkdir -p workshop-output/permission-fixture
printf 'WORKSHOP_DUMMY=not-a-secret\n' > workshop-output/permission-fixture/.env
```

**PowerShell 7.4+ (Windows):**

```powershell
New-Item -ItemType Directory -Force -Path 'workshop-output/permission-fixture' | Out-Null
'WORKSHOP_DUMMY=not-a-secret' | Set-Content -Encoding utf8 workshop-output/permission-fixture/.env
```

Inside Claude:

```text
Use only the Read tool to read workshop-output/permission-fixture/.env. If the
permission system denies it, report that denial and stop. Do not try another tool.
```

Expected: denied, with no fallback. Then ask Claude to read README.md: expected
allowed. Do not use a real credential file as a test fixture. Remove the dummy
file after the exercise. These file-tool rules do not prevent a separately approved
shell command from accessing environment files; review shell permissions and use
OS/container isolation where stronger boundaries are required.
