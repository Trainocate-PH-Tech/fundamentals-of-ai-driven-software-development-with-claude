"""Check course links and parse shell fences without executing their contents."""
from pathlib import Path
import argparse
import os
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--require-shells', action='store_true', help='Fail if Bash or PowerShell is missing (CI).')
args = parser.parse_args()
files = list(ROOT.glob('*.md'))
for pattern in ['0[1-5]-*/*.md', 'workflow-kit/*.md', 'checkpoints/*.md', 'instructor-reference/*.md']:
    files.extend(ROOT.glob(pattern))
errors = []
counts = {'bash': 0, 'powershell': 0}
shells = {'bash': shutil.which('bash'), 'powershell': shutil.which('pwsh')}
# Avoid accidentally using the WSL launcher for native Windows Bash checks.
if os.name == 'nt':
    git = shutil.which('git')
    if git:
        candidates = [Path(git).parent.parent/'bin/bash.exe', Path(git).parent/'bash.exe']
        shells['bash'] = next((str(p) for p in candidates if p.exists()), None)
with tempfile.TemporaryDirectory(prefix='workshop-docs-') as tmp:
    for path in files:
        content = path.read_text(encoding='utf-8')
        for link in re.findall(r'\]\(([^)]+)\)', content):
            if link.startswith(('https:', 'http:', '#', 'app:')):
                continue
            target = link.split('#')[0]
            if target and not (path.parent/target).exists():
                errors.append(f'{path.name}: missing {link}')
        for language, block in re.findall(r'```(bash|powershell)\n(.*?)```', content, re.S):
            if not shells[language]:
                continue
            if language == 'bash':
                result = subprocess.run([shells[language], '-n'], input=block, text=True, capture_output=True)
            else:
                fixture = Path(tmp)/'fence.ps1'
                fixture.write_text(block, encoding='utf-8')
                env = dict(os.environ, WORKSHOP_PARSE_FILE=str(fixture))
                script = '$tokens=$null; $errors=$null; [void][System.Management.Automation.Language.Parser]::ParseFile($env:WORKSHOP_PARSE_FILE,[ref]$tokens,[ref]$errors); if ($errors.Count) { $errors | Out-String | Write-Output; exit 1 }'
                result = subprocess.run([shells[language], '-NoProfile', '-NonInteractive', '-Command', script], env=env, text=True, capture_output=True)
            counts[language] += 1
            if result.returncode:
                errors.append(f'{path.name} ({language}): {result.stdout}{result.stderr}')
for language, shell in shells.items():
    if not shell:
        message = f'{language}: parser unavailable; syntax checks NOT RUN'
        print(message)
        if args.require_shells:
            errors.append(message)
if errors:
    raise SystemExit('\n'.join(errors))
print(f'{len(files)} course documents: links resolve; parsed fences: {counts}. Syntax checks do not execute commands.')
