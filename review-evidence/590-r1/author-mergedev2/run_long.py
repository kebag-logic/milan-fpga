"""Run one gate command at the new head and write its receipt.

Usage: run_long.py NAME [--env K=V ...] -- COMMAND...

The log goes to the scratch directory and is copied here only when it is
200 KB or smaller; the receipt always binds its size and SHA-256. The
worktree must be clean and at the same HEAD before and after.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = Path('$LANES/590-592-599-firmware')
OUT = Path(__file__).parent
SCRATCH = Path('$VALIDATION_STORAGE/590-a430/logs')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


name = sys.argv[1]
split = sys.argv.index('--')
extra = dict(item.split('=', 1) for item in sys.argv[2:split] if item != '--env')
argv = sys.argv[split + 1:]
assert Path.cwd() == ROOT
head = git('rev-parse', 'HEAD')
assert not git('status', '--porcelain'), 'dirty before ' + name
environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0', **extra)
log = SCRATCH / (name + '.log')
started = time.monotonic()
wall = time.strftime('%Y-%m-%dT%H:%M:%S%z')
with log.open('w') as stream:
    rc = subprocess.run(argv, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, env=environment).returncode
seconds = round(time.monotonic() - started, 3)
raw = log.read_bytes()
kept = None
if len(raw) <= 200000:
    (OUT / 'logs').mkdir(exist_ok=True)
    shutil.copyfile(log, OUT / 'logs' / log.name)
    kept = 'logs/' + log.name
receipt = dict(name=name, head=head, started=wall, command=argv, env=extra, rc=rc, seconds=seconds,
               log=str(log), log_size=len(raw), log_sha256=hashlib.sha256(raw).hexdigest(), kept=kept,
               head_after=git('rev-parse', 'HEAD'), clean_after=not git('status', '--porcelain'))
(OUT / 'receipts').mkdir(exist_ok=True)
(OUT / 'receipts' / (name + '.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print(name, 'rc', rc, 'seconds', seconds, 'clean', receipt['clean_after'], flush=True)
sys.exit(rc if receipt['clean_after'] and receipt['head_after'] == head else 99)
