"""Historical PostgreSQL maintenance launcher; teaching uses direct SQLite commands."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import signal
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PINS = {
    'issuetrackerapi': ('https://github.com/cloudband-solutions/default_api_fast.git', '6afada28350e93d5a2cdff7dddcbe88c2036e299'),
    'issuetrackerweb': ('https://github.com/cloudband-solutions/admin-panel-web.git', '47578e05f4cca5c035ea51c0b5e92b55d0818928'),
}

def venv_python(api, platform=None):
    return api / '.venv' / ('Scripts/python.exe' if (platform or sys.platform) == 'win32' else 'bin/python')


def run(args, cwd, env=None):
    args = [str(a) for a in args]
    # Resolve npm.cmd explicitly on Windows; only fixed npm subcommands are used.
    if sys.platform == 'win32' and args[0] == 'npm':
        args[0] = shutil.which('npm.cmd') or 'npm.cmd'
    if sys.platform != 'win32':
        return subprocess.run(args, cwd=cwd, env=env, check=True)
    process = subprocess.Popen(args, cwd=cwd, env=env,
                               creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    try:
        code = process.wait()
    except KeyboardInterrupt:
        try:
            process.send_signal(signal.CTRL_BREAK_EVENT)
            process.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            process.wait()
        raise
    if code:
        raise subprocess.CalledProcessError(code, args)


def check_runtime():
    if sys.version_info[:2] != (3, 14):
        raise SystemExit('Use Python 3.14: py -3.14 -m tools.workshop on Windows; python3.14 -m tools.workshop on Linux.')


def doctor():
    check_runtime()
    for cmd in [[sys.executable, '--version'], ['node', '--version'], ['npm', '--version'],
                ['git', '--version'], ['docker', 'compose', 'version']]:
        run(cmd, ROOT)
    node = subprocess.check_output(['node', '--version'], text=True).strip()
    if node.split('.')[0] != 'v24':
        raise SystemExit('Node 24 is required; reopen the terminal after installation.')
    engine = subprocess.check_output(['docker', 'info', '--format', '{{.OSType}}'], text=True).strip()
    if engine != 'linux':
        raise SystemExit('Switch Docker Desktop to Linux containers, then rerun doctor.')
    print('Python 3.14, Node 24, Git and Docker Compose available; Linux container engine connected.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--reference', action='store_true')
    p.add_argument('--workspace', type=Path)
    p.add_argument('command', choices=['doctor','setup','db','start','test','build','e2e','recover','install-kit'])
    p.add_argument('args', nargs='*')
    a = p.parse_args()
    if a.reference and a.workspace:
        p.error('Choose --reference or --workspace')
    w = a.workspace.resolve() if a.workspace else ROOT / 'instructor-reference' if a.reference else ROOT
    api, web = w / 'issuetrackerapi', w / 'issuetrackerweb'
    offset = 2 if a.reference else 0
    devport, testport = 54329 + offset, 54330 + offset
    apiport, webport = (3001, 8001) if a.reference else (3000, 8000)
    env = os.environ.copy()
    env.update(DEV_DB_PORT=str(devport), TEST_DB_PORT=str(testport), API_BASE_URL=f'http://localhost:{apiport}', WEB_PORT=str(webport), API_VERSION='v1')
    dburl = f'postgresql+psycopg://workshop:workshop-local@127.0.0.1:{devport}/issuetracker'
    testurl = f'postgresql+psycopg://workshop:workshop-local@127.0.0.1:{testport}/issuetracker_test'
    py = venv_python(api)
    env['PATH'] = str(py.parent) + os.pathsep + env.get('PATH', '')
    compose = ['docker','compose','-f',ROOT/'compose.workshop.yml','-p','workshop-'+hashlib.sha256(str(w).encode()).hexdigest()[:10]]
    try:
        if a.command == 'doctor':
            doctor()
        elif a.command == 'recover':
            if len(a.args) != 2:
                p.error('recover CHECKPOINT NEW_DIRECTORY')
            stage, target = a.args[0], Path(a.args[1]).resolve()
            if stage not in [x.name for x in (ROOT/'checkpoints').iterdir() if x.is_dir()]:
                p.error('Unknown checkpoint')
            if target.exists():
                p.error('Recovery destination must not exist; existing work is never overwritten')
            target.mkdir(parents=True)
            for name, (url, pin) in PINS.items():
                run(['git','clone','--config','core.autocrlf=false',url,target/name], ROOT)
                run(['git','checkout','--detach',pin], target/name)
                patch = ROOT/'checkpoints'/stage/(name+'.patch')
                if patch.stat().st_size:
                    run(['git','apply','--check',patch], target/name)
                    run(['git','apply',patch], target/name)
            launcher = 'py -3.14 -m tools.workshop' if sys.platform == 'win32' else './workshop'
            print(f'Recovered source to {target}\nNext: {launcher} --workspace "{target}" setup')
        elif a.command == 'setup':
            check_runtime()
            for name,(url,pin) in PINS.items():
                path=w/name
                if not path.exists():
                    run(['git','clone','--config','core.autocrlf=false',url,path],ROOT)
                    run(['git','checkout','--detach',pin],path)
                    run(['git','apply',ROOT/'checkpoints/00-baseline'/f'{name}.patch'],path)
                if not (path/('requirements.lock.txt' if name.endswith('api') else 'package-lock.json')).exists():
                    p.error(f'{path} lacks workshop lockfile; use a fresh recovery workspace')
            if not py.exists():
                if (api/'.venv').exists():
                    p.error('Existing .venv is incomplete or belongs to another OS. Preserve it elsewhere or use a fresh workspace before setup.')
                run([sys.executable,'-m','venv',api/'.venv'],w)
            run([py,'-m','pip','install','-r','requirements.lock.txt'],api)
            run(['npm','ci'],web)
            for path,content in [(api/'.env',f'DATABASE_URL={dburl}\nSECRET_KEY={secrets.token_hex(32)}\n'),(web/'.env',f'API_BASE_URL=http://localhost:{apiport}\nTOKEN_BEARER=ISSUE_TRACKER_TOKEN\nCURRENT_USER=ISSUE_TRACKER_USER\n')]:
                if not path.exists():
                    path.write_text(content, encoding='utf-8')
                    if os.name != 'nt':
                        path.chmod(0o600)
            print('Installed locks; existing .env files preserved. Start databases with db up.')
        elif a.command == 'install-kit':
            run([sys.executable,ROOT/'tools/install_kit.py',w],ROOT)
        elif a.command == 'db':
            if a.args == ['up']:
                run(compose+['up','-d','--wait'],ROOT,env)
            elif a.args == ['stop']:
                run(compose+['stop'],ROOT,env)
            elif a.args in (['migrate'],['seed']):
                env.update(DATABASE_URL=dburl,APP_ENV='development')
                if a.args == ['migrate']:
                    run([py,'-m','app.cli','db:upgrade'],api,env)
                else:
                    run([py,'-m','app.cli','system:seed'],api,env)
                    run([py,'-m','app.seed_tracker'],api,env)
            else:
                p.error('db up|stop|migrate|seed (seed requires milestone 01-data)')
        elif a.command == 'start':
            if a.args == ['api']:
                env.update(DATABASE_URL=dburl,APP_ENV='development')
                run([py,'-m','uvicorn','app:create_app','--factory','--host','127.0.0.1','--port',str(apiport)],api,env)
            elif a.args == ['web']:
                run(['npm','start'],web,env)
            else:
                p.error('start api|web')
        elif a.command == 'test':
            env.update(DATABASE_URL=testurl, APP_ENV='test')
            run([py,'-m','pytest',*(a.args or ['spec'])],api,env)
        elif a.command == 'build':
            run(['npm','run','build'],web,env)
        elif a.command == 'e2e':
            env.update(E2E_BASE_URL=f'http://localhost:{webport}',E2E_API_URL=f'http://localhost:{apiport}')
            run(['npm','run','test:e2e'],web,env)
    except FileNotFoundError as e:
        p.exit(1, f'Missing executable or directory: {e.filename}. Check WINDOWS_SETUP.md or run doctor.\n')
    except KeyboardInterrupt:
        p.exit(130, 'Stopped.\n')
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

if __name__ == '__main__':
    main()
