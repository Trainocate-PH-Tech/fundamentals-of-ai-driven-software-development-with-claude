# MCP fundamentals: give a Claude subagent a live tool

This optional extension follows [Module 3, section 3](03-ai-development-workflow/README.md#3-subagent-delegation-with-explicit-inputs).
You will host a small MCP server, create a restricted Claude Code subagent, and
prove that it called the running server. Allow about 30 minutes. This standalone
lab does not require the Issue Tracker API or database.

## 1. Understand the pieces

**Model Context Protocol (MCP)** lets an AI application discover and call tools
provided by another process. A server can also expose resources (readable data)
and prompts (reusable messages); this lab exposes only tools. The validation
prompt below is a user request, not an MCP prompt endpoint.

```text
Your validation prompt
  → Claude Code main session delegates to mcp-validator
    → Claude Code's MCP client calls a tool over HTTP
      → test_mcp.py executes Python and returns structured data
    ← subagent checks the actual response
  ← main session presents and saves the report
```

The subagent supplies a focused role and tool permissions. The MCP server supplies
executable capabilities. Neither replaces the other. Here, “hosted” means a
process listening at `http://127.0.0.1:8765/mcp` on your own machine, not a public
cloud deployment. Run Claude and Python in the same OS environment (both WSL,
or both native Windows). This unauthenticated teaching server binds to loopback;
keep it local.

## 2. Select the workspace and prerequisites

Use Python 3.14, Git, and an authenticated Claude Code installation from
[Module 1](01-project-setup/README.md). Use Bash on Linux/WSL or PowerShell 7.4+
on Windows. Choose one platform; never reuse virtual environments across them.

Choose your active student workspace, normally a sibling of this course clone.
Copy these reviewed course files into the **same relative paths** there using
your editor/file manager:

- [test_mcp.py](test_mcp.py): the server, despite its `test_` filename.
- [requirements-mcp.txt](requirements-mcp.txt): isolated lab dependency.
- [tools/verify_mcp.py](tools/verify_mcp.py): independent protocol check.

Sections 4 and 5 teach you to create the two configuration files. Completed
examples are also supplied as [.mcp.json](.mcp.json) and
[.claude/agents/mcp-validator.md](.claude/agents/mcp-validator.md). If you choose
to run directly in this course clone, those files already exist: inspect them
and skip their creation. Do not overwrite existing MCP configurations.

In **each terminal**, first change to your selected root. Replace the example
path with your actual directory. These are alternative commands:

```bash
cd /absolute/path/to/your/student-workspace
pwd
uname -s
printf '%s\n' "$SHELL"
python3 --version
claude --version
```

```powershell
Set-Location 'C:\absolute\path\to\your\student-workspace'
Get-Location
[System.Environment]::OSVersion
$PSVersionTable.PSVersion
py -3.14 --version
claude --version
```

Record the workspace, OS/shell, versions, `git rev-parse HEAD`, and
`git status --short` in a new run folder under
`workshop-output/milestones/mcp-fundamentals/`. Preserve earlier runs. If the
workspace is not a Git repository, record that explicitly. The main session
owns plan, evidence and handoff files; subagent output is separate evidence.

## 3. Create and host the server

Open `test_mcp.py`. It uses the official Python SDK pinned to `mcp==1.26.0` for
this exercise. `FastMCP` handles protocol initialization, tool discovery, input
schemas, and responses. The `@mcp.tool()` decorators expose two Python functions:

| Tool | Input | Observable result |
|---|---|---|
| `ping` | A nonblank `challenge` string | `pong`, the exact challenge, and a server instance UUID |
| `add` | Integer `a` and `b` | A `sum` field |

The instance UUID changes when the process restarts. A blank challenge produces
an MCP tool error. Nothing reads application files or writes to a database.
`mcp.run(transport="streamable-http")` serves the protocol at `/mcp`.

In terminal A, create a separate lab environment and start the server:

```bash
python3 -m venv .venv-mcp
.venv-mcp/bin/python -m pip install -r requirements-mcp.txt
.venv-mcp/bin/python test_mcp.py
```

```powershell
py -3.14 -m venv .venv-mcp
& ./.venv-mcp/Scripts/python.exe -m pip install -r requirements-mcp.txt
& ./.venv-mcp/Scripts/python.exe test_mcp.py
```

Add `.venv-mcp/` to the active workspace's `.gitignore`. Leave terminal A running.
This is a server program, so do not run `pytest test_mcp.py`.

In terminal B, from the same workspace, check the actual protocol:

```bash
.venv-mcp/bin/python tools/verify_mcp.py
```

```powershell
& ./.venv-mcp/Scripts/python.exe tools/verify_mcp.py
```

Expected: `PASS: initialize, discovery, ping, add, blank challenge, missing argument`,
followed by the live instance and challenge. This checks the server independently
of Claude. An HTTP response in a browser alone does not prove MCP works.

## 4. Connect Claude Code to the hosted MCP

If the `workshop` entry is absent, run this from the active root in either shell:

```bash
claude mcp add --transport http --scope project workshop http://127.0.0.1:8765/mcp
```

This creates or updates `.mcp.json`. Its `mcpServers` object should contain:

```json
{
  "mcpServers": {
    "workshop": {
      "type": "http",
      "url": "http://127.0.0.1:8765/mcp"
    }
  }
}
```

Keep any other server entries. Inspect with `claude mcp get workshop`. Start
`claude` from this same root, review the project-server trust prompt if shown,
and open `/mcp` to inspect connectivity. The server must remain running.
Project registration and HTTP transport follow the
[Claude MCP documentation](https://code.claude.com/docs/en/mcp).

## 5. Create the subagent

In your editor, create `.claude/agents/mcp-validator.md`. Copy the entire
[provided definition](.claude/agents/mcp-validator.md), including both `---`
frontmatter markers. Read its instructions before running it.

Its key configuration is:

```yaml
name: mcp-validator
description: Validate the local workshop MCP server when explicitly asked to run the MCP fundamentals lab.
tools: mcp__workshop__ping, mcp__workshop__add
model: inherit
```

The exact names combine `mcp__`, the registered server name `workshop`, and the
Python tool name. The allowlist restricts this agent to these two tools; it has
no shell or file-editing tools. The project-level MCP connection supplies the
server. You do not need a second server definition inside the agent.

The Markdown body tells it what to call, what to compare, and when to report
BLOCKED. Restart Claude after creating the file, then use `/agents` or ask it
to identify `mcp-validator`. Interface details vary by CLI version. File-based
roles and tool restrictions are described in the
[Claude subagent documentation](https://code.claude.com/docs/en/sub-agents).

## 6. Validate through the subagent

Choose a new non-secret challenge for every run, such as your initials plus the
current time. Replace `REPLACE-WITH-FRESH-CHALLENGE` below. Paste this **inside
Claude Code**, not your terminal:

```text
Run the MCP fundamentals validation in this active workspace. Delegate explicitly
to mcp-validator. Supply this exact challenge: REPLACE-WITH-FRESH-CHALLENGE.
Ask it to call workshop ping with that challenge, add with a=19 and b=23,
and ping with an empty challenge. Expected: pong with an exact echo and a
nonempty server_instance; sum=42; then an error saying "challenge must not be blank".
Require a table of actual tool names, arguments, responses and PASS/FAIL.
No simulated calls or source-based answers. If connectivity or permissions prevent
calls, report BLOCKED. Do not modify code or start a substitute server.
Main session: show the named delegation and returned report. Save the report and
actual execution evidence in a new run folder under
workshop-output/milestones/mcp-fundamentals/. Include workspace, OS/shell,
revision/dirty state and any checks not run. Keep the subagent report separate
from the main-session evidence.
```

Expand the named delegation's tool activity. Require all three tool calls;
`42` alone is not evidence. Compare its instance UUID with the independent check
while the same server process is running. Record a verdict yourself.

**Negative exercise:** stop terminal A with Ctrl+C. In a fresh Claude session,
repeat with another fresh challenge. It must report BLOCKED (connection failure
or unavailable tools), never a cached PASS. Restart the server, run the independent
check again, and rerun the prompt; the new instance UUID should differ.

**Independent extension:** add a `multiply(a: int, b: int)` tool, update the
agent allowlist and instructions, and validate `6 × 7 = 42` using an actual call.
Restart the server and Claude to refresh tool discovery. Explain why writing a
function without registering it does not expose a tool.

## 7. Exit gate and troubleshooting

Complete this lab only when the protocol check passes, the named subagent makes
all three calls, and the stopped-server exercise cannot report success. Save a
handoff with observed results and any missing evidence. This gate is separate
from the required Issue Tracker acceptance gates.

| Symptom | Check |
|---|---|
| `No module named mcp` | Use the lab environment's Python and install its requirements. |
| Connection refused | Keep terminal A running; check the same OS environment and port 8765. |
| Address already in use | Stop your previous lab server; do not terminate an unknown process. |
| HTTP 404 / protocol failure | Use `/mcp`, with HTTP transport, not the root URL or `/sse`. |
| Agent missing | Confirm the active root and file path, then restart Claude. |
| Tools missing or denied | Inspect `/mcp`, trust/permission prompts, and exact allowlist names. |
| Success without tool activity | Reject the result; repeat with explicit delegation and a fresh challenge. |

Stop the server with Ctrl+C when finished. To disable the optional integration,
remove only the `workshop` entry with `claude mcp remove --scope project workshop`,
and remove the lab agent if desired. Keep your evidence.

## Maintainer verification boundary

See the current implementation checks in the change report. Python/HTTP checks
and CLI configuration inspection do not establish that a live Claude delegation
passed. Participants must perform section 6 themselves. Windows commands are
provided for rehearsal; Linux results do not establish Windows success.

SDK reference: [official Python SDK v1.26.0](https://github.com/modelcontextprotocol/python-sdk/tree/v1.26.0).
The SDK version is intentionally pinned; this lab is not a claim about the latest
SDK API. No capstone feature or application-template runtime is changed.
