# Windows setup — direct commands and SQLite

Use Windows 11 x64 with **PowerShell 7.4+**, or WSL2 Ubuntu with Bash. Both follow the
same five modules and SQLite acceptance gates. No Docker or database server is
needed. Windows ARM and Windows PowerShell 5.1 are outside the initial validation
target. See [validation](VALIDATION.md) for checks actually performed.

## Native Windows prerequisites

Install prerequisites from a Windows terminal; installers may request elevation.
Run ordinary project work without administrator privileges.

```powershell
winget install --exact --id Microsoft.PowerShell
winget install --exact --id Python.Python.3.14
winget install --exact --id Git.Git
winget install --exact --id Microsoft.VisualStudioCode
winget install --exact --id Anthropic.ClaudeCode
```

Install Node **24.x** from the [official downloads](https://nodejs.org/en/download).
Select that major version rather than assuming a package named LTS still means 24.
Open a new PowerShell 7 terminal (`pwsh`). In VS Code select the PowerShell terminal
profile. In each new workshop terminal, enable native command failure propagation:

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true
$PSVersionTable.PSVersion
py -3.14 --version
py -3.14 -c "import sqlite3; print(sqlite3.sqlite_version)"
node --version
npm.cmd --version
git --version
claude --version
claude doctor
```

Expected: PowerShell 7.4+, Python 3.14, Node 24 and working Git/Claude. SQLite is
included with Python. Use `npm.cmd` and `npx.cmd` to avoid blocked PowerShell shims;
there is no need to disable execution policy or activate a venv script.

## Authenticate Claude

Run `claude` and follow the supported account's browser sign-in. If using a Console
API key instead, enter it without placing it in command history:

```powershell
$env:ANTHROPIC_API_KEY = Read-Host 'Anthropic API key' -MaskInput
claude
```

Approve API-key use if Claude asks; API billing is separate from subscription use.
Never print the key, save it in an application `.env`, or include it in prompts/logs.
To return to account login, exit Claude and clear the process variable:

```powershell
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
claude
```

See [terminal authentication](CLAUDE_CODE_TERMINAL.md) and
[VS Code setup](CLAUDE_CODE_VSCODE_SETUP.md). Authentication belongs to the environment
where Claude runs; Windows credentials do not establish a WSL session's access.

## Create and operate the workspace

Start at the downloaded course root. Follow [Module 1](01-project-setup/README.md)
and its links to the guide's exact manual steps. Create a fresh sibling workspace
in a local writable folder, not a synchronized/network directory. Quote paths with
spaces. The active root contains issuetrackerapi and issuetrackerweb.

Use PowerShell blocks for file creation, dependencies, migrations, servers and tests.
From issuetrackerapi the interpreter is `& ./.venv/Scripts/python.exe`; from
issuetrackerweb use `npm.cmd`. No launcher or installation kit is required.
The API uses `sqlite:///storage/development.sqlite3`; isolated tests use exactly
`sqlite:///test.sqlite3` from the API directory. Always restore test environment
variables after a check using the guide's try/finally block.

Create agent files in `.claude/agents/` yourself as shown in the guide. Start Claude
at the active root and request a reviewer by name in an ordinary message. Observe
the actual delegation row, tools and output. Optional skills are student-authored
exercises; none is required to plan, implement or verify the application.

**Prompt inside Claude:**

```text
This workspace runs natively on Windows. Read CLAUDE.md and workflow/project.md.
Identify your active shell, working directory and Python interpreter before running
commands. Use direct Python, npm and Git commands with SQLite. In PowerShell use
Scripts/python.exe, npm.cmd and PowerShell environment syntax. Do not invoke WSL
or reuse Linux environments. Do not read environment files or print credentials.
```

Git for Windows supplies Git Bash, which Claude may use even when the human's
terminal is PowerShell. Check the tool's actual shell. A Git Bash tool call on
native Windows still uses the Windows venv (`.venv/Scripts/python.exe`), not
`.venv/bin/python`. If Claude cannot find Git Bash, follow its official
[Windows setup](https://code.claude.com/docs/en/setup) for the local path setting.

## WSL2 Ubuntu alternative

From an elevated Windows terminal:

```powershell
wsl --install -d Ubuntu
wsl --list --verbose
```

Confirm Ubuntu uses version 2. Install Linux Python 3.14, Node 24, Git and Claude
inside Ubuntu. Verify versions; the distribution's default Python may differ.
Keep the course and active workspace under `~/projects`, not `/mnt/c`. Install
VS Code's WSL extension and open the workspace using `code .` from Ubuntu.
Confirm the editor status bar indicates WSL, then follow Bash blocks throughout.
No Docker installation or integration is required for SQLite.
Never share `.venv`, `node_modules` or live database files across Windows and WSL.

## Troubleshooting and rehearsal

| Symptom | Action |
|---|---|
| `py` missing | Reopen the terminal and confirm Python 3.14's launcher installation. |
| `npm.ps1` blocked | Use npm.cmd/npx.cmd, not an execution-policy bypass. |
| Wrong venv interpreter | Select the current OS's interpreter; reinstall in a separate workspace when changing OS. |
| SQLite cannot open file | Check API working directory and create storage as shown in Module 1. |
| SQLite database locked | Stop competing writers; keep development/test files separate and use one browser worker. |
| Test isolation assertion fails | Use exactly sqlite:///test.sqlite3 from the API directory. |
| Patch fails | Use a new destination and the exact pinned commit; preserve source/patch line endings. |
| Hook fixture passes but no live feedback | Check active settings, actual hook shell and interpreter, then test a disposable edit. |

Before delivery, record OS/versions, commands and actual outcomes for fresh setup
in a path with spaces; baseline tests/build; completed migration/seed/browser flow;
Ctrl+C and restart; new-destination recovery; skill and subagent creation/discovery;
and standalone plus live hook checks. Preserve development data on shutdown.
CI configuration and Linux results are not proof of a completed Windows rehearsal.
