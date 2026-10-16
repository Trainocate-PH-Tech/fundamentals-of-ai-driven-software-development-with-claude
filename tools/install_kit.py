"""Maintenance-only template copier; teaching material uses manual file creation."""
from pathlib import Path
import shutil
import sys
ROOT=Path(__file__).resolve().parents[1]
target=Path(sys.argv[1]).resolve()
conflicts=[]
for source in sorted((ROOT/'workflow-kit/template').rglob('*')):
    if not source.is_file(): continue
    relative=source.relative_to(ROOT/'workflow-kit/template')
    dest=target/relative
    if dest.exists():
        if dest.read_bytes()==source.read_bytes(): continue
        dest=target/'.workshop/proposed'/relative
        conflicts.append(str(relative))
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,dest)
for folder in ['milestones']:
    (target/'workshop-output'/folder).mkdir(parents=True,exist_ok=True)
if conflicts:
    print('Existing files preserved. Review candidates in .workshop/proposed:', ', '.join(conflicts))
else:
    print('Workflow kit installed; identical files left unchanged.')
