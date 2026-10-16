# Set up Claude Code in VS Code

For the full application toolchain and shell-specific exercises, follow [Windows setup](WINDOWS_SETUP.md). Claude installation alone does not install Python, Node, Git, or Docker.

[Workshop home](README.md) · [Project setup](01-project-setup/README.md) · [Terminal guide](CLAUDE_CODE_TERMINAL.md)

Documentation checked: 2026-10-15. The steps below are for participants; no extension installation or authenticated session was performed while writing this guide.

## 1. Install and open the extension

1. Install or update VS Code; Claude Code requires VS Code 1.94.0 or later.
2. Open Extensions with **Ctrl+Shift+X** on Windows/Linux or **Cmd+Shift+X** on macOS.
3. Search for **Claude Code** and install the official Anthropic extension.
4. Use **File → Open Folder** to open the main workshop directory containing `README.md` and `SOFTWARE_SPECIFICATIONS.md`.
5. Open the Command Palette, search for **Claude Code**, and choose **Open in New Tab**. If the extension is missing, use **Developer: Reload Window**.

The extension includes the CLI needed for its chat panel. Running `claude` yourself in the integrated terminal requires the separate installation in the [terminal guide](CLAUDE_CODE_TERMINAL.md). See [official VS Code setup](https://code.claude.com/docs/en/vs-code).

## 2. Choose account sign-in or an API key

**Account sign-in:** click **Sign in** in the Claude Code panel and complete browser authorization using your eligible Claude account or Console account. For subscription access, leave `ANTHROPIC_API_KEY` unset. See [supported authentication methods](https://code.claude.com/docs/en/authentication).

**API access:** create an Anthropic Console key using [terminal guide, section 3](CLAUDE_CODE_TERMINAL.md#3-create-an-api-key-if-using-api-access), then supply it through the launch environment below. API usage has its own billing; an approved environment key can override subscription access. See [API-key billing behavior](https://support.claude.com/en/articles/12304248-manage-api-key-environment-variables-in-claude-code).

## 3. Make the API key available to VS Code

A key set in VS Code's integrated terminal does not update the already-running extension's environment. Set it before launching VS Code. The official [VS Code authentication guidance](https://code.claude.com/docs/en/vs-code) recommends launching with `code .` to inherit shell variables.

1. Save your work and fully quit all VS Code windows and processes.
2. Open an external terminal in the same environment where you will run VS Code.
3. Use the matching hidden-input block in [terminal guide, section 4](CLAUDE_CODE_TERMINAL.md#4-supply-the-api-key-to-your-terminal): Bash, Zsh, or PowerShell. It sets `ANTHROPIC_API_KEY` without putting the literal secret in command history.
4. In that same terminal, change to the workshop directory and launch:

   ```text
   cd path/to/fundamentals-of-ai-driven-software-development-with-claude
   code .
   ```

5. Open Claude Code and acknowledge the API-key selection prompt if shown. Check `/status` in the panel to confirm the active authentication method, then send the verification prompt below.

If `code` is not available, configure the VS Code command-line launcher first. On macOS, use the Command Palette command **Shell Command: Install 'code' command in PATH**; on Windows/Linux, check your VS Code installation's PATH configuration and reopen the terminal.

Do not put a real key in `.vscode/settings.json`, tracked Claude settings, lesson files, the application's `.env`, or frontend variables. Use the temporary launch environment for this workshop. Do not share a screenshot of the key or paste it into chat.

For WSL, SSH, or a dev container, credentials must be available where the extension's Claude process runs. A local desktop variable may not reach that remote environment. If this is unclear, use the terminal guide inside the target environment to establish a working session before configuring remote VS Code access.

## 4. Verify workshop context

Use this first prompt in the Claude Code panel:

```text
Read @AGENTS.md, @README.md, and @SOFTWARE_SPECIFICATIONS.md.
Summarize the workshop goals and list the five lesson directories.
Check whether issuetrackerapi and issuetrackerweb exist.
Do not edit files or install anything yet.
```

The application folders are created during lesson 1, so their absence before that activity is expected. Keep the parent workshop folder open when working across both applications.

`AGENTS.md` is explicitly referenced here because Claude Code's persistent project instruction file is `CLAUDE.md`. During the instructions lesson, create or update a root `CLAUDE.md` to import shared guidance with `@AGENTS.md`, after checking existing instructions. See [project instruction loading](https://code.claude.com/docs/en/memory).

## 5. Troubleshooting and completion

| Symptom | Next step |
|---|---|
| Sign-in appears despite setting a key | Fully quit VS Code, set the key in an external terminal, and relaunch from that terminal. Check for remote execution or organization-enforced sign-in. |
| API authentication fails | Check the intended organization, key validity, and API access; never print the key to diagnose it. |
| Account signs in but requests fail | Check billing, credits, and usage limits for the active account. |
| `claude` is missing in the integrated terminal | Install the standalone CLI; extension installation alone does not add that shell command. |
| Switching back to subscription use | Quit VS Code, unset the key using the terminal guide, remove any persistent definition you previously added, and relaunch. |

Removing a variable from the launch shell does not remove it from an already-running VS Code process; quit that process when finishing API-key use. Revoke a leaked key in the Console and create a replacement.

- [ ] The official extension opens in the workshop folder.
- [ ] Authentication uses the intended account or API key.
- [ ] A prompt receives a response and Claude can read the workshop instructions.
- [ ] No credentials have been saved in project files.

Continue with [01 — Project setup](01-project-setup/README.md).
