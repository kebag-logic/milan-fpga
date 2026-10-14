#!/usr/bin/env python3
"""Run independent compiler-free checks concurrently, waiting in foreground."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
scratch = out / 'scratch'
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
jobs = [('capture', ['scripts/check_nvm_capture.py'], 0),
        *[('capture-' + m, ['scripts/check_nvm_capture.py', '--mutation', m], 1)
          for m in ('bytes', 'records', 'clock', 'ignore-off-timing', 'receipt-opt-out')],
        ('ci-scope', ['scripts/ci_scope.py', '--selftest'], 0),
        ('ci-events', ['scripts/ci_events.py', '--check'], 0),
        ('delta-integrity', [str(out / 'audit_delta.py')], 0)]

def run(job):
    name, args, expected = job
    start = time.monotonic()
    with (out / (name + '.log')).open('w') as log:
        result = subprocess.run([sys.executable, *args], env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=550)
    (out / (name + '.rc')).write_text(str(result.returncode) + '\n')
    row = dict(name=name, command=['python3', *args], rc=result.returncode,
               expected=expected, seconds=round(time.monotonic()-start, 2))
    print(json.dumps(row), flush=True)
    return row

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, jobs))
(out / 'focused-results.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(any(r['rc'] != r['expected'] for r in results))
