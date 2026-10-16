"""Verify every cumulative patch independently against the pinned upstream."""
from pathlib import Path
import subprocess
import tempfile
from tools.workshop import PINS, ROOT

def run(*args,cwd=None):
    return subprocess.run(args,cwd=cwd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

with tempfile.TemporaryDirectory(prefix='workshop-checkpoints-') as tmp:
    for stage in sorted((ROOT/'checkpoints').iterdir()):
        if not stage.is_dir(): continue
        for app,(_,pin) in PINS.items():
            source=ROOT/'instructor-reference'/app
            if not (source/'.git').exists():
                source=ROOT/'.workshop/upstream-git'/app
            if not source.exists():
                source=PINS[app][0]
            dest=Path(tmp)/f'{stage.name}-{app}'
            run('git','clone','--shared',str(source),str(dest))
            run('git','checkout','--detach',pin,cwd=dest)
            patch=stage/(app+'.patch')
            if patch.stat().st_size:
                run('git','apply','--check',str(patch),cwd=dest)
                run('git','apply',str(patch),cwd=dest)
            print(stage.name,app,'applies cleanly')
