"""Isolated tests for the teaching hook; no application or Claude login required."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("check_python_syntax.py")


class SyntaxHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.backend = self.root / "issuetrackerapi"
        self.backend.mkdir()

    def invoke(self, path=None, *, raw=None, event_name="PostToolUse", tool="Write", root=True):
        payload = raw if raw is not None else json.dumps({
            "hook_event_name": event_name,
            "tool_name": tool,
            "tool_input": {"file_path": str(path)},
        })
        env = dict(os.environ)
        env.pop("CLAUDE_PROJECT_DIR", None)
        if root:
            env["CLAUDE_PROJECT_DIR"] = str(self.root)
        result = subprocess.run([sys.executable, str(SCRIPT)], input=payload, text=True,
                                capture_output=True, env=env, check=True)
        self.assertEqual(result.stderr, "")
        if not result.stdout:
            return None
        output = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "PostToolUse")
        return output["additionalContext"]

    def test_valid_code_is_not_executed_or_rewritten(self):
        target = self.backend / "example.py"
        original = b'raise RuntimeError("must not execute")\n'
        target.write_bytes(original)
        before = set(self.root.rglob("*"))
        self.assertIn("PASS", self.invoke(target))
        self.assertEqual(target.read_bytes(), original)
        self.assertEqual(set(self.root.rglob("*")), before)

    def test_invalid_code_reports_line_without_repair(self):
        target = self.backend / "example.py"
        target.write_text("def broken(:\n")
        message = self.invoke(target, tool="Edit")
        self.assertIn("FAIL", message)
        self.assertIn("line 1", message)
        self.assertEqual(target.read_text(), "def broken(:\n")

    def test_outside_backend_and_non_python_are_ignored(self):
        for target in [self.root / "outside.py", self.backend / "notes.txt",
                       self.root / "issuetrackerapi-other" / "example.py"]:
            self.assertIsNone(self.invoke(target))

    def test_parent_traversal_is_ignored(self):
        self.assertIsNone(self.invoke(self.backend / ".." / "outside.py"))

    def test_symlink_escape_is_ignored(self):
        outside = self.root / "outside.py"
        outside.write_text("invalid python !")
        link = self.backend / "link.py"
        try:
            link.symlink_to(outside)
        except OSError:
            self.skipTest("symlinks unavailable")
        self.assertIsNone(self.invoke(link))

    def test_other_tool_or_event_is_ignored(self):
        self.assertIsNone(self.invoke(self.backend / "file.py", tool="Bash"))
        self.assertIsNone(self.invoke(self.backend / "file.py", event_name="PreToolUse"))

    def test_malformed_or_incomplete_input_is_reported(self):
        for raw in ["not json", "[]", '{"hook_event_name":"PostToolUse","tool_name":"Edit"}']:
            self.assertIn("no check performed", self.invoke(raw=raw))

    def test_missing_file_and_relative_path(self):
        self.assertIn("unavailable", self.invoke(self.backend / "missing.py"))
        self.assertIn("absolute", self.invoke("relative.py"))

    def test_missing_project_root(self):
        self.assertIn("CLAUDE_PROJECT_DIR missing", self.invoke(self.backend / "file.py", root=False))


if __name__ == "__main__":
    unittest.main()
