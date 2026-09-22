"""Record one bounded correction command without filtering its output."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
CWD = Path('$CANDIDATE')


def git(*args):
    return subprocess.check_output(
        ['rtk', 'proxy', 'git', '--no-replace-objects', *args], cwd=CWD
    ).decode().strip()


def identity():
    changed = git('diff', '--name-only', 'HEAD').splitlines()
    return {
        'head': git('rev-parse', 'HEAD'),
        'head_tree': git('rev-parse', 'HEAD^{tree}'),
        'index_entries_sha256': hashlib.sha256(git('ls-files', '--stage').encode()).hexdigest(),
        'index_matches_head': not git('diff', '--cached', '--name-only'),
        'status': git('status', '--porcelain=v1'),
        'changed_worktree_sha256': {
            name: hashlib.sha256((CWD / name).read_bytes()).hexdigest()
            for name in changed
        },
    }


name, *argv = sys.argv[1:]
if not name or not argv or argv[0] != 'rtk':
    raise SystemExit('usage: record.py <unique-name> rtk <command...>')
out = ROOT / 'commands'
out.mkdir(exist_ok=True)
receipt = out / (name + '.json')
log = out / (name + '.log')
if receipt.exists() or log.exists():
    raise SystemExit('refusing to overwrite an existing receipt')
before = identity()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
start = time.monotonic()
with log.open('wb') as stream:
    result = subprocess.run(
        argv, cwd=CWD, stdout=stream, stderr=subprocess.STDOUT,
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), check=False,
    )
elapsed = time.monotonic() - start
record = {
    'name': name, 'argv': argv, 'command': shlex.join(argv), 'cwd': str(CWD),
    'env_delta': {'PYTHONDONTWRITEBYTECODE': '1'},
    'started_utc': started, 'elapsed_seconds': elapsed,
    'exit': result.returncode, 'before': before, 'after': identity(),
    'log': str(log.relative_to(ROOT)),
    'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest(),
}
receipt.write_text(json.dumps(record, indent=2) + '\n')
print(f'{name}: exit {result.returncode}; {elapsed:.3f}s; {receipt}')
print(log.read_text(errors='replace')[-3500:])
raise SystemExit(result.returncode)
