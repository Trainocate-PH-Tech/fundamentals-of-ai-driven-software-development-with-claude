"""Capture cumulative patches against the pinned upstreams, excluding runtime files."""
import pathlib, subprocess, sys
root = pathlib.Path(__file__).resolve().parents[1]
name = sys.argv[1]
for app in ['issuetrackerapi', 'issuetrackerweb']:
    path = root / 'instructor-reference' / app
    git = ['git', '--git-dir', str(root/'.workshop/upstream-git'/app), '--work-tree', str(path)] if not (path/'.git').exists() else ['git']
    subprocess.run(git+['add','-N','.'],cwd=path,check=True)
    patch = subprocess.check_output(git+['diff','--binary','HEAD'],cwd=path)
    out = root/'checkpoints'/name
    out.mkdir(parents=True,exist_ok=True)
    (out/f'{app}.patch').write_bytes(patch)
