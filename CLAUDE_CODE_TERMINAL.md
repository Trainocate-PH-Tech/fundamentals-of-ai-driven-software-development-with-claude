# Set up Claude Code in the terminal

For the full application toolchain and shell-specific exercises, follow [Windows setup](WINDOWS_SETUP.md). Claude installation alone does not install Python, Node, or Git.

[Workshop home](README.md) · [Project setup](01-project-setup/README.md) · [VS Code guide](CLAUDE_CODE_VSCODE_SETUP.md)

Documentation checked: 2026-10-15. The workshop provides Bash on Linux/WSL2 and PowerShell 7.4+ on native Windows. Installation is participant-run; see VALIDATION.md for the local CLI probe and application checks.

## 1. Install the CLI

Use a terminal on macOS, Linux, Windows, or WSL. Have Git available for the workshop. The native Claude Code installer does not require Node.js; the React application has its own runtime requirements.

macOS, Linux, or WSL:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Native Windows, in **PowerShell**:

```powershell
irm https://claude.ai/install.ps1 | iex
```

These commands download and run Anthropic's installer. On Windows, Git for Windows supplies Git Bash; in WSL, install and run Claude Code inside the Linux environment. Reopen your terminal after installation if needed, then check:

```text
claude --version
claude doctor
```

If `claude` is not found, follow the installer's PATH instructions for your shell. See [official installation documentation](https://code.claude.com/docs/en/setup) for supported systems and alternative installers.

## 2. Choose authentication

| Workshop access | What to configure |
|---|---|
| Eligible Claude subscription or organization-provided Claude access | Browser sign-in; no manually supplied API key needed |
| Direct Anthropic API access | Console API key in `ANTHROPIC_API_KEY` and enabled API billing |
| Organization-managed cloud provider or gateway | Follow your administrator's provider-specific configuration |

For account sign-in, run `claude` and follow the browser authorization. Use `/login` inside Claude Code when you need to sign in again. Do not copy browser cookies or session tokens. See [authentication options](https://code.claude.com/docs/en/authentication).

For subscription use, leave `ANTHROPIC_API_KEY` unset. An approved environment API key can take precedence over subscription authentication and incur separate API charges. Check `/status` inside Claude Code before starting the workshop. See [API-key precedence and billing](https://support.claude.com/en/articles/12304248-manage-api-key-environment-variables-in-claude-code).

## 3. Create an API key, if using API access

1. Sign in to the [Claude Console](https://platform.claude.com/) and select the intended organization/workspace. Confirm API billing or credits with the workshop administrator.
2. Open **Settings → API keys**, or the [API keys page](https://platform.claude.com/settings/keys).
3. Choose **Create key**, give it a recognizable name such as `issue-tracker-workshop`, and choose the appropriate account, workspace, and expiration. Prefer a personal key for individual development.
4. Copy the key to a password or secrets manager. The full value is shown only at creation. If key creation is unavailable, ask your organization administrator for access.

See the [official API-key guide](https://platform.claude.com/docs/en/get-api-key). A GitHub token or OpenAI API key cannot replace this credential.

## 4. Supply the API key to your terminal

Use one block matching your shell. Paste the key only at the hidden input prompt, not into a Claude conversation. These examples avoid placing the literal key in shell command history and keep it scoped to this shell and its child processes.

**Bash** — Linux, WSL, or a Bash session on macOS:

```bash
read -r -s -p 'Anthropic API key: ' ANTHROPIC_API_KEY
printf '\n'
export ANTHROPIC_API_KEY
```

**Zsh** — default shell on many Macs:

```zsh
read -r -s 'ANTHROPIC_API_KEY?Anthropic API key: '
printf '\n'
export ANTHROPIC_API_KEY
```

**PowerShell**:

```powershell
$workshopKey = Read-Host 'Anthropic API key' -AsSecureString
$env:ANTHROPIC_API_KEY = [System.Net.NetworkCredential]::new('', $workshopKey).Password
Remove-Variable workshopKey
```

The environment variable still contains the plaintext secret while in use. Do not print it, put it in a project `.env`, commit it, or add it to frontend configuration such as `VITE_*`. It authenticates the development tool; the Issue Tracker does not need it.

Run `claude` from this same terminal and accept the custom-key prompt if shown. Check `/status`, then send a small prompt to verify access. Environment-based keys are supported by [Claude Code authentication](https://code.claude.com/docs/en/authentication).

For this workshop, repeat the hidden-input step in each new shell rather than storing the key in a shell startup file. If persistent credential management is required, use your organization's approved secrets mechanism.

To remove the key from the current shell after exiting Claude Code:

```bash
# Bash or Zsh
unset ANTHROPIC_API_KEY
```

```powershell
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
```

Restart Claude Code after changing authentication. If you previously saved the variable persistently, remove that saved definition too. Revoke an exposed or no-longer-needed key in the Console.

## 5. Open the workshop and verify context

Change into your local workshop directory, replacing the example path:

```text
cd path/to/issue-tracker-manual
claude
```

Start from the workshop root so the lesson files and, once created, `issuetrackerapi/` and `issuetrackerweb/` are in scope. Ask:

```text
Read AGENTS.md, README.md, and SOFTWARE_SPECIFICATIONS.md.
Summarize the workshop structure and identify which application directories exist.
Do not edit files or install anything yet.
```

Claude Code uses `CLAUDE.md` for persistent project instructions; do not assume it automatically reads `AGENTS.md`. Explicitly request it as above. In the instructions lesson, a root `CLAUDE.md` can import the existing guidance with `@AGENTS.md`; inspect any existing file before adding imports. See [Claude Code project memory](https://code.claude.com/docs/en/memory).

## Troubleshooting and completion

- **Login or key rejected:** check `/status`, the selected organization, key validity, billing, and organization policy. Do not paste the key into a support prompt.
- **Quota or rate limit:** inspect the account's usage limits; a working installation does not guarantee available capacity.
- **Different behavior in Windows and WSL:** configure credentials in the environment where Claude actually runs.
- **Wrong files visible:** exit, change to the workshop root, and start again.

Complete when the CLI reports a version, the intended authentication method is active, and Claude can summarize the workshop files. For ordinary usage, see the [official quickstart](https://code.claude.com/docs/en/quickstart).
