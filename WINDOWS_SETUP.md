# Windows setup and workshop delivery

Use **Windows 11 x64 and PowerShell 7.4+** for the native route, or **WSL2 Ubuntu**
for the Linux route. Both follow the same five modules, specification, and exit
gates. Windows ARM and Windows PowerShell 5.1 are not the initial validation target.
See [validation](VALIDATION.md) for actual checks; instructions and CI configuration
alone do not establish that a Windows classroom rehearsal passed.

## 1. Choose one workspace and shell

| Route | Project location | Terminal | Launcher from course root |
|---|---|---|---|
| Native Windows | A local folder such as `C:\Users\you\projects\issue-tracker-course` | PowerShell 7.4+ | `py -3.14 -m tools.workshop` |
| WSL2 | `~/projects/issue-tracker-course` inside Ubuntu | Ubuntu Bash | `./workshop` |

Use a local writable directory rather than a network share or synchronized folder.
Spaces in paths are supported; quote paths. Never share `.venv` or `node_modules`
between Windows and Linux. To change routes, use another clone and reinstall.
Docker Desktop uses Linux containers for PostgreSQL in **both** routes; the native
route runs Python, Node, Claude, and VS Code directly on Windows.

## 2. Native prerequisites

Run these in Windows Terminal's PowerShell tab. Windows may request elevation for
installers; run normal workshop work without administrator privileges.

```powershell
winget install --exact --id Microsoft.PowerShell
winget install --exact --id Python.Python.3.14
winget install --exact --id Git.Git
winget install --exact --id Microsoft.VisualStudioCode
winget install --exact --id Docker.DockerDesktop
```

Install **Node 24.x** using the Windows x64 installer from the
[official Node downloads](https://nodejs.org/en/download). Select the 24 release;
a package named “LTS” can advance to a different major version. Install standalone
[ripgrep](https://github.com/BurntSushi/ripgrep#installation) if using optional `rg`
commands; Claude's bundled search is not necessarily on your terminal PATH.

Restart if the Docker installer requests it. Start Docker Desktop and select
its WSL2 backend and **Linux containers**. Follow its supported Windows/virtualization
requirements; a Windows container engine cannot run this course's PostgreSQL image.
You do not need an Ubuntu development workspace for the native route.

Open a **new PowerShell 7** terminal (run `pwsh` if the tab is Windows PowerShell).
In VS Code, use **Terminal: Select Default Profile → PowerShell**, then open a new
terminal. Enable failure propagation for each workshop terminal:

```powershell
$PSVersionTable.PSVersion
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true
py -3.14 --version
node --version
npm.cmd --version
git --version
docker compose version
docker info --format '{{.OSType}}'
```

Expected: PowerShell 7.4 or newer, Python 3.14.x, Node v24.x, and Docker `linux`.
Use `npm.cmd`/`npx.cmd` in PowerShell to avoid blocked npm PowerShell shims. The
workshop launcher resolves npm automatically; no activation script or execution
policy bypass is needed. `doctor` verifies the required Python/Node major versions
and Docker engine. Diagnose a failed check before proceeding.

## 3. Claude Code and credentials

Install and reopen the terminal:

```powershell
winget install --exact --id Anthropic.ClaudeCode
```

```powershell
claude --version
claude doctor
claude
```

Use the browser sign-in flow for your supported subscription or Console account.
If your training uses a Console API key instead, load it into the **current process**
without putting the secret in command history, a prompt, or a repository file:

```powershell
$env:ANTHROPIC_API_KEY = Read-Host 'Anthropic API key' -MaskInput
claude
```

Approve the API-key authentication choice when Claude asks. API billing is separate
from subscription usage. To return to browser sign-in, exit Claude and remove the
variable before launching again:

```powershell
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
claude
```

Do not print environment variables to verify a secret. VS Code inherits environment
from its launching process; configure authentication in the environment where the
extension or CLI actually runs. See [terminal authentication](CLAUDE_CODE_TERMINAL.md)
and [VS Code setup](CLAUDE_CODE_VSCODE_SETUP.md).

The course installs Git for Windows, which gives Claude its Bash tool. The human
terminal can still be PowerShell. Tell Claude the actual execution shell; Bash tool
calls on native Windows must use Windows Python, not WSL Python. In Git Bash,
`python -m tools.workshop` works after verifying `python --version` is 3.14.
If Claude cannot find Git Bash, use the documented `CLAUDE_CODE_GIT_BASH_PATH`
setting with your actual Git installation path. Never copy a machine-specific
path into shared settings for the class.

**Prompt inside Claude:**

```text
This workspace runs natively on Windows. Read CLAUDE.md and workflow/project.md.
Identify your active shell before running commands. In PowerShell use
py -3.14 -m tools.workshop; in Git Bash verify Windows Python 3.14 and use
python -m tools.workshop. Do not invoke WSL, reuse Linux virtual environments,
or read .env files. Report the workspace and runtime you will use.
```

## 4. Complete the workshop in PowerShell

Open the downloaded/cloned course folder in VS Code. Its root contains `workshop`,
`tools`, and the five numbered module folders. Run all blocks from this root unless
explicitly told otherwise. Module pages provide Bash and PowerShell alternatives;
**run one alternative only**. Slash commands such as `/workshop-plan` go inside
Claude, never in the PowerShell terminal.

1. [Module 1](01-project-setup/README.md): run doctor, setup, databases, migrations,
   and kit installation. Test/build the baseline. Do not seed tracker categories yet.
2. [Module 2](02-application-fundamentals/README.md): use `Get-Content` to inspect the
   existing request flow; delegate a bounded read-only review of the map.
3. [Module 3](03-ai-development-workflow/README.md): create a skill using the supplied
   single-quoted PowerShell here-string. It preserves literal `$ARGUMENTS`.
   Create/adapt reviewers, restart Claude, inspect `/agents`, and monitor actual
   delegated tool calls as instructed. The instructor guide includes a full
   PowerShell subagent creation example.
4. [Module 4](04-issue-tracker-implementation/README.md): implement each slice and
   run its gate. Use separate terminals for API and frontend; Ctrl+C stops each.
5. [Module 5](05-testing-debugging-and-demo/README.md): capture test/build/browser
   logs with `Tee-Object`, verify hook activation, and perform the browser demo.

For HTTP diagnostics, avoid ambiguous `curl` aliases. A successful health check
uses this command once the student API is running:

```powershell
Invoke-RestMethod -Uri 'http://localhost:3000/health'
```

For JSON bodies, build a PowerShell object and pipe to `ConvertTo-Json`; do not put
live authentication tokens in copied examples or evidence logs.

To use the completed instructor solution, follow the PowerShell blocks in
[GUIDE.md](GUIDE.md). `--reference` uses separate ports. Recovery retains the same
interface and refuses to overwrite an existing destination:

```powershell
py -3.14 -m tools.workshop db stop
py -3.14 -m tools.workshop recover 06-frontend 'recovery/windows completed'
py -3.14 -m tools.workshop --workspace 'recovery/windows completed' setup
py -3.14 -m tools.workshop --workspace 'recovery/windows completed' db up
py -3.14 -m tools.workshop --workspace 'recovery/windows completed' db migrate
py -3.14 -m tools.workshop --workspace 'recovery/windows completed' db seed
py -3.14 -m tools.workshop --workspace 'recovery/windows completed' test
py -3.14 -m tools.workshop --workspace 'recovery/windows completed' build
```

Only run this recovery example when you need the completed milestone. Stop other
student/recovery servers first: recovered workspaces reuse student ports. Use the
same `--workspace` for both `start` commands, `e2e`, and `db stop` afterward.

## 5. WSL2 Ubuntu alternative

From an elevated Windows terminal, install Ubuntu and restart when requested:

```powershell
wsl --install -d Ubuntu
wsl --list --verbose
```

Confirm Ubuntu uses version 2. Enable Ubuntu under Docker Desktop's WSL integration.
Open Ubuntu, install Linux Git, Python 3.14 and Node 24 using their official Linux
instructions, and install Claude using the Bash instructions in
[terminal setup](CLAUDE_CODE_TERMINAL.md). Ubuntu's default Python may not be 3.14;
verify rather than assuming the distribution package meets the course version.

Clone the course under `~/projects` inside Ubuntu, not `/mnt/c`. Install the VS Code
WSL extension, run `code .` inside that clone, and confirm VS Code's status bar shows
WSL. All subsequent terminal commands use the Bash blocks. Docker Desktop itself
remains the Windows installation; do not install a second daemon inside Ubuntu.

```bash
python3 --version
node --version
docker compose version
./workshop doctor
```

Keep authentication in the Linux environment where Claude runs. A successful
native Windows sign-in or Python installation does not verify the WSL environment.

## 6. Troubleshooting and acceptance

| Symptom | Action |
|---|---|
| `py` not found | Reopen the terminal; verify the Python 3.14 installation includes the Windows launcher. |
| `.venv` belongs to another OS | Use another clone or move the old environment aside, then rerun setup; never overwrite source or `.env`. |
| `npm.ps1` blocked | Use `npm.cmd` or the workshop launcher; do not disable execution policy globally. |
| Docker connection or image failure | Start Docker Desktop; check Linux-container mode, virtualization, and Docker's diagnostics. |
| Database/API port in use | Stop the matching workspace's services and terminal processes before switching workspaces. |
| Patch application fails | Use a fresh recovery destination. Preserve LF source and byte-exact patch files; do not use whitespace-ignore options to conceal a mismatch. |
| Hook works in tests but not Claude | Check the actual hook shell, interpreter, matcher, active settings, and `/hooks`; restart and test a disposable file. |
| Commands continue after failure | Enable the PowerShell preferences in section 2 in each terminal; record `$LASTEXITCODE` when diagnosing native tools. |

Instructor Windows rehearsal checklist (record OS, versions, command, exit code,
and actual outcome in a fresh milestone evidence file):

- [ ] Fresh clone in a path with spaces: doctor, setup, migration, baseline tests/build.
- [ ] Repeat setup: existing `.env` contents and student instructions preserved.
- [ ] Completed reference: migration, seed twice, backend suite, frontend build.
- [ ] Start both servers; install Chromium and pass browser acceptance.
- [ ] Ctrl+C releases each server port; restart both successfully.
- [ ] Recover baseline and final checkpoint into new directories and install each.
- [ ] Create/invoke a skill and read-only subagent, inspect real task activity.
- [ ] Hook fixture tests and live valid/invalid edit feedback; record skips explicitly.
- [ ] Complete the specification's browser demonstration and save evidence.
- [ ] Stop servers and workspace databases.

Windows CI checks installation, tooling, process tests, hooks, documentation syntax,
build, and patch application. It does **not** exercise Docker Desktop or establish
Windows database/browser acceptance; complete the checklist on a Windows machine.

References: [Claude Windows setup](https://code.claude.com/docs/en/setup),
[Docker Windows requirements](https://docs.docker.com/desktop/setup/install/windows-install/),
[Docker WSL integration](https://docs.docker.com/desktop/features/wsl/),
[Microsoft WSL environment](https://learn.microsoft.com/en-us/windows/wsl/setup/environment).
