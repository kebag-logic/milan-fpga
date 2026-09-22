#!/usr/bin/env python3
"""Capture raw argv, combined output, exit and source identity without a shell."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('$CANDIDATE')
label, *argv = sys.argv[1:]
assert argv[0] == 'rtk'
receipt = ROOT / 'raw' / (label + '.json')
log = ROOT / 'raw' / (label + '.log')
assert not receipt.exists() and not log.exists(), label

def git(*args):
    return subprocess.check_output(['rtk', 'proxy', 'git', *args], cwd=SOURCE, text=True).strip()

start = time.monotonic()
record = dict(argv=argv, cwd=str(SOURCE), head=git('rev-parse', 'HEAD'),
              tree=git('rev-parse', 'HEAD^{tree}'),
              worktree_status=git('status', '--porcelain=v1'),
              checker_sha256=hashlib.sha256((SOURCE/'scripts/check_baremetal_only.py').read_bytes()).hexdigest(),
              started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', VERILATOR_JOBS='8', MAKEFLAGS='-j8')
record['environment_overrides'] = {k: env[k] for k in ('PYTHONDONTWRITEBYTECODE', 'VERILATOR_JOBS', 'MAKEFLAGS')}
with log.open('wb') as stream:
    result = subprocess.run(argv, cwd=SOURCE, env=env, stdout=stream, stderr=subprocess.STDOUT, check=False)
record.update(exit=result.returncode, elapsed_seconds=time.monotonic()-start,
              finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
receipt.write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record))
print(log.read_text(errors='replace'))
sys.exit(result.returncode)
