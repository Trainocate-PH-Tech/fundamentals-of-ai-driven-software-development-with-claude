# Optional extension — Feedback after Python edits

[Module overview](README.md) · [Core verification](01_VERIFICATION_AND_DEMO.md)

**Core:** instructor walkthrough (5 minutes). **Optional hands-on:** 20–30 minutes. Technique: hooks. Prerequisites: Python 3.9+ on the machine running Claude Code, the workshop root, and permission to configure local hooks.

This example parses backend Python after Claude's Edit/Write tools. It never imports, executes, or rewrites the checked file. Syntax feedback helps catch a broken edit early; it does not verify API behavior or replace tests.

## 1. Inspect and test the starter

Read [check_python_syntax.py](examples/hooks/check_python_syntax.py), [settings.fragment.json](examples/hooks/settings.fragment.json), and [fixture tests](examples/hooks/test_check_python_syntax.py).

From the workshop root, run:

```bash
python3 05-testing-debugging-and-demo/examples/hooks/test_check_python_syntax.py
```

**PowerShell 7.4+ (Windows):**

```powershell
py -3.14 05-testing-debugging-and-demo/examples/hooks/test_check_python_syntax.py
```

On native Windows, use the installed `python` executable instead of `python3` if appropriate. The script uses only the standard library. Fixtures are created in a temporary directory and cleaned up. Verify the tests actually ran; record a skipped symlink case as skipped.

## 2. Install without replacing existing settings

1. Copy the hook script from the course root. `-n` preserves any existing file:

   ```bash
   mkdir -p .claude/hooks
   cp -n 05-testing-debugging-and-demo/examples/hooks/check_python_syntax.py .claude/hooks/check_python_syntax.py
   ```

**PowerShell 7.4+ (Windows):**

```powershell
New-Item -ItemType Directory -Force -Path '.claude/hooks' | Out-Null
if (-not (Test-Path .claude/hooks/check_python_syntax.py)) { Copy-Item 05-testing-debugging-and-demo/examples/hooks/check_python_syntax.py .claude/hooks/check_python_syntax.py }
   
```
2. Open root `.claude/settings.local.json`, creating it if absent. Merge the fragment's `PostToolUse` entry into existing hooks; preserve all other events and permissions. Do not copy the example tests into active hook configuration.
3. The supplied fragment is for Linux/WSL with `python3`. On native Windows with the course's Git for Windows installation, hooks run in Git Bash. Use [settings.windows.fragment.json](examples/hooks/settings.windows.fragment.json), whose command invokes `py -3.14` and quotes `$CLAUDE_PROJECT_DIR` for paths with spaces. Merge its event into local settings rather than replacing existing settings. Verify `py -3.14 --version` in Git Bash before enabling it. If you configure a different hook shell, adapt and test the command for that shell explicitly.
4. Restart the session at the workshop root and inspect `/hooks` for the matcher and command. Resolve any configuration/organization restriction before continuing.

`PostToolUse` runs after a successful tool action; the script returns `additionalContext` feedback. An `Edit|Write` matcher does not see shell-based rewrites. It cannot reverse an edit. See [official hook input and output documentation](https://code.claude.com/docs/en/hooks).

## 3. Verify actual activation

Use only a new disposable file `issuetrackerapi/workshop_syntax_fixture.py`. If it already exists, choose another unused `.py` name and use it consistently. It must not be imported by the app.

Ask Claude:

```text
Using the Write tool, create only issuetrackerapi/workshop_syntax_fixture.py
with the text: value = 1
Do not run or import it. Report the syntax hook's visible feedback.
```

Check for PASS in the hook feedback. Then ask it to change that same disposable file, using Edit or Write, to the intentionally invalid `def broken(:` and stop without repairing it. Check for FAIL and a line number. Restore `value = 1` using the same tool and check for PASS again. These are deliberate fixture changes, not application changes.

For ignored-file behavior, use the isolated tests rather than editing real frontend files. If the hook does not fire, inspect the event/tool, command path, Python availability, settings scope, and hook diagnostics. A passing standalone test is not proof of a live hook invocation.

## 4. Review and cleanup

Record the installed command, fixture feedback, any failures, and whether the live check was actually performed. Delete only your disposable fixture. Retain the hook if useful, or remove its exact configuration entry and copied script; preserve pre-existing hooks/settings.

- [ ] Isolated tests run and outcomes recorded.
- [ ] Active hook is visible and valid/invalid fixture edits produce expected feedback.
- [ ] No file under test is executed or rewritten by the checker.
- [ ] Students can explain why syntax success is weaker than application-test success.
- [ ] Fixture removed and any retained configuration documented.
