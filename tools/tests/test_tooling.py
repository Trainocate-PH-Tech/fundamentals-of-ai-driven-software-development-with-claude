import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

class ToolingTests(unittest.TestCase):
    def test_installer_preserves_conflicts_and_is_repeatable(self):
        with tempfile.TemporaryDirectory(prefix='workshop space ') as tmp:
            path=Path(tmp)
            (path/'AGENTS.md').write_text('existing guidance')
            cmd=[sys.executable,str(ROOT/'tools/install_kit.py'),tmp]
            subprocess.run(cmd,check=True,capture_output=True)
            self.assertEqual((path/'AGENTS.md').read_text(),'existing guidance')
            self.assertTrue((path/'.workshop/proposed/AGENTS.md').exists())
            original=(path/'CLAUDE.md').read_bytes()
            subprocess.run(cmd,check=True,capture_output=True)
            self.assertEqual((path/'CLAUDE.md').read_bytes(),original)
            self.assertFalse((path/'.workshop/proposed/CLAUDE.md').exists())

    def test_expanded_kit_installs_roles_skills_and_preserves_conflicts(self):
        with tempfile.TemporaryDirectory(prefix='kit paths ') as tmp:
            root=Path(tmp)
            relative=Path('.claude/skills/workshop-implement/SKILL.md')
            existing=root/relative
            existing.parent.mkdir(parents=True)
            existing.write_text('student-owned procedure')
            subprocess.run([sys.executable,str(ROOT/'tools/install_kit.py'),tmp],check=True,capture_output=True)
            self.assertEqual(existing.read_text(),'student-owned procedure')
            self.assertIn('name: workshop-implement',(root/'.workshop/proposed'/relative).read_text())
            for role in ['workspace-scout','workshop-investigator','backend-reviewer','ui-reviewer']:
                content=(root/'.claude/agents'/f'{role}.md').read_text()
                self.assertIn('tools: Read, Glob, Grep',content)
            for skill in ['workshop-plan','workshop-verify']:
                self.assertTrue((root/'.claude/skills'/skill/'SKILL.md').exists())
            self.assertTrue((root/'workshop-output/milestones').is_dir())

    def test_recovery_refuses_existing_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=subprocess.run([str(ROOT/'workshop'),'recover','00-baseline',tmp],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('must not exist',result.stderr)
            self.assertEqual(list(Path(tmp).iterdir()),[])

    def test_unknown_checkpoint_and_command_fail(self):
        for args in [('recover','unknown','unused'),('destroy',)]:
            result=subprocess.run([str(ROOT/'workshop'),*args],capture_output=True)
            self.assertNotEqual(result.returncode,0)
