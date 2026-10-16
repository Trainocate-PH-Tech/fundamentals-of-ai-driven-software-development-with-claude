"""Process lifecycle tests without a database or application fixtures."""
import sys
from unittest.mock import Mock
from app import cli


def test_command_preserves_exit_code():
    assert cli._run_command([sys.executable, '-c', 'raise SystemExit(7)']) == 7


def test_windows_interrupt_uses_process_group(monkeypatch):
    process = Mock()
    process.wait.side_effect = [KeyboardInterrupt, 0]
    popen = Mock(return_value=process)
    monkeypatch.setattr(cli.sys, 'platform', 'win32')
    monkeypatch.setattr(cli.subprocess, 'CREATE_NEW_PROCESS_GROUP', 512, raising=False)
    monkeypatch.setattr(cli.signal, 'CTRL_BREAK_EVENT', 1, raising=False)
    monkeypatch.setattr(cli.subprocess, 'Popen', popen)
    assert cli._run_command(['example']) == 130
    assert popen.call_args.kwargs['creationflags'] == 512
    process.send_signal.assert_called_once_with(1)
