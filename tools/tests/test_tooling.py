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
            self.assertEqual((path/'AGENTS.md').read_text(encoding='utf-8'),'existing guidance')
            self.assertTrue((path/'.workshop/proposed/AGENTS.md').exists())
            original=(path/'CLAUDE.md').read_bytes()
            subprocess.run(cmd,check=True,capture_output=True)
            self.assertEqual((path/'CLAUDE.md').read_bytes(),original)
            self.assertFalse((path/'.workshop/proposed/CLAUDE.md').exists())

    def test_manual_templates_preserve_roles_without_orchestration_skills(self):
        with tempfile.TemporaryDirectory(prefix='kit paths ') as tmp:
            root=Path(tmp)
            relative=Path('.claude/agents/acceptance-reviewer.md')
            existing=root/relative
            existing.parent.mkdir(parents=True)
            existing.write_text('student-owned reviewer', encoding='utf-8')
            subprocess.run([sys.executable,str(ROOT/'tools/install_kit.py'),tmp],check=True,capture_output=True)
            self.assertEqual(existing.read_text(encoding='utf-8'),'student-owned reviewer')
            self.assertIn('name: acceptance-reviewer',(root/'.workshop/proposed'/relative).read_text(encoding='utf-8'))
            for role in ['architecture-reviewer','bug-investigator','backend-reviewer','ui-reviewer']:
                content=(root/'.claude/agents'/f'{role}.md').read_text(encoding='utf-8')
                self.assertIn('tools: Read, Glob, Grep',content)
            for skill in ['workshop-plan','workshop-implement','workshop-verify']:
                self.assertFalse((root/'.claude/skills'/skill/'SKILL.md').exists())
            profile=(root/'workflow/project.md').read_text(encoding='utf-8')
            self.assertIn('sqlite:///test.sqlite3', profile)
            self.assertNotIn('./workshop', profile)
            self.assertTrue((root/'workshop-output/milestones').is_dir())

    def test_recovery_refuses_existing_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=subprocess.run([sys.executable,str(ROOT/'workshop'),'recover','00-baseline',tmp],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('must not exist',result.stderr)
            self.assertEqual(list(Path(tmp).iterdir()),[])

    def test_unknown_checkpoint_and_command_fail(self):
        for args in [('recover','unknown','unused'),('destroy',)]:
            result=subprocess.run([sys.executable,str(ROOT/'workshop'),*args],capture_output=True)
            self.assertNotEqual(result.returncode,0)

    def test_platform_venv_paths(self):
        from tools.workshop import venv_python
        root = Path('project with spaces')
        self.assertEqual(venv_python(root, 'win32'), root/'.venv/Scripts/python.exe')
        self.assertEqual(venv_python(root, 'linux'), root/'.venv/bin/python')

    def test_child_failure_is_propagated(self):
        from tools.workshop import run
        with self.assertRaises(subprocess.CalledProcessError) as error:
            run([sys.executable, '-c', 'raise SystemExit(7)'], ROOT)
        self.assertEqual(error.exception.returncode, 7)

    def test_setup_preserves_existing_environment_files(self):
        from unittest.mock import patch
        from tools import workshop
        with tempfile.TemporaryDirectory(prefix='workshop setup space ') as tmp:
            root = Path(tmp)
            api, web = root/'issuetrackerapi', root/'issuetrackerweb'
            api.mkdir(); web.mkdir()
            (api/'requirements.lock.txt').write_text('', encoding='utf-8')
            (web/'package-lock.json').write_text('{}', encoding='utf-8')
            py = workshop.venv_python(api)
            py.parent.mkdir(parents=True)
            py.touch()
            for path in [api/'.env', web/'.env']:
                path.write_text('EXISTING=preserve-me\n', encoding='utf-8')
            with patch.object(sys, 'argv', ['workshop', '--workspace', tmp, 'setup']), \
                 patch.object(workshop, 'run'), patch.object(workshop, 'check_runtime'):
                workshop.main()
                workshop.main()
            for path in [api/'.env', web/'.env']:
                self.assertEqual(path.read_text(encoding='utf-8'), 'EXISTING=preserve-me\n')

    def test_windows_interrupt_targets_child_group(self):
        from unittest.mock import Mock, patch
        from tools import workshop
        process = Mock()
        process.wait.side_effect = [KeyboardInterrupt, 0]
        with patch.object(workshop.sys, 'platform', 'win32'), \
             patch.object(workshop.subprocess, 'CREATE_NEW_PROCESS_GROUP', 512, create=True), \
             patch.object(workshop.signal, 'CTRL_BREAK_EVENT', 1, create=True), \
             patch.object(workshop.subprocess, 'Popen', return_value=process) as popen:
            with self.assertRaises(KeyboardInterrupt):
                workshop.run(['example'], ROOT)
        self.assertEqual(popen.call_args.kwargs['creationflags'], 512)
        process.send_signal.assert_called_once_with(1)
