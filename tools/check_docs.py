"""Check local links and Bash code-fence syntax in course Markdown."""
from pathlib import Path
import re
import subprocess
ROOT=Path(__file__).resolve().parents[1]
files=list(ROOT.glob('*.md'))
for pattern in ['0[1-5]-*/*.md','workflow-kit/*.md','checkpoints/*.md','instructor-reference/*.md']:
    files.extend(ROOT.glob(pattern))
errors=[]
blocks=0
for path in files:
    content=path.read_text()
    for link in re.findall(r'\]\(([^)]+)\)',content):
        if link.startswith(('https:','http:','#','app:')): continue
        target=link.split('#')[0]
        if target and not (path.parent/target).exists(): errors.append(f'{path.name}: missing {link}')
    for block in re.findall(r'```bash\n(.*?)```',content,re.S):
        blocks+=1
        result=subprocess.run(['bash','-n'],input=block,text=True,capture_output=True)
        if result.returncode: errors.append(f'{path.name}: {result.stderr}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'{len(files)} course documents: links resolve; {blocks} Bash blocks parse. Syntax checks do not execute commands.')
