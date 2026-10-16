"""PostToolUse teaching hook: parse backend Python without running or writing it."""

import ast
import json
import os
from pathlib import Path
import sys


def feedback(message):
    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": message,
        }
    }


def inspect_event(event, project_root):
    if not isinstance(event, dict):
        return feedback("Workshop syntax hook: invalid event object; no check performed.")
    if event.get("hook_event_name") != "PostToolUse" or event.get("tool_name") not in {"Edit", "Write"}:
        return None
    tool_input = event.get("tool_input")
    if not isinstance(tool_input, dict) or not isinstance(tool_input.get("file_path"), str):
        return feedback("Workshop syntax hook: missing file_path; no check performed.")
    if not project_root:
        return feedback("Workshop syntax hook: CLAUDE_PROJECT_DIR missing; no check performed.")
    try:
        backend = (Path(project_root).resolve() / "issuetrackerapi").resolve()
        target = Path(tool_input["file_path"])
        if not target.is_absolute():
            return feedback("Workshop syntax hook: expected an absolute file_path; no check performed.")
        target = target.resolve()
        if not target.is_relative_to(backend) or target.suffix != ".py":
            return None
        relative = target.relative_to(backend)
        # ast.parse accepts bytes and honors Python source encoding declarations.
        # It does not execute code, import the application, or produce bytecode.
        ast.parse(target.read_bytes(), filename=str(relative))
    except SyntaxError as error:
        return feedback(
            f"Workshop syntax hook: FAIL {relative}, line {error.lineno}: {error.msg}. "
            "The edit already happened. Fix the syntax, then rerun relevant checks."
        )
    except (OSError, ValueError, RuntimeError) as error:
        return feedback(f"Workshop syntax hook: check unavailable ({type(error).__name__}); inspect the file/path.")
    return feedback(f"Workshop syntax hook: PASS {relative}. Syntax only; application tests were not run.")


def main():
    try:
        event = json.load(sys.stdin)
    except (ValueError, UnicodeError):
        result = feedback("Workshop syntax hook: malformed JSON input; no check performed.")
    else:
        result = inspect_event(event, os.environ.get("CLAUDE_PROJECT_DIR"))
    if result:
        print(json.dumps(result))
    # This is advisory feedback, not a veto or a test-suite gate.
    return 0


if __name__ == "__main__":
    sys.exit(main())
