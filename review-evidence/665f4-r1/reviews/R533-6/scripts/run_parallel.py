#!/usr/bin/env python3
"""Join independent foreground checks, with separate logs and exit receipts."""
import argparse
import concurrent.futures
import json
import os
import subprocess
import time
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
a = p.parse_args()
repo = a.repo.resolve()
packet = Path(__file__).resolve().parents[1]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet / 'scratch'))
jobs = [(m, ['python3', str(packet / 'scripts/focused.py'), str(repo), '--mode', m, '--jobs', '4'])
        for m in ('suites', 'campaign', 'probes')]
jobs.append(('coverage', ['python3', str(repo / 'sw/firmware/gtest/fw_coverage.py'), '--check', '--jobs', '4',
                          '--keep', str(packet / 'scratch/coverage')]))
def run(job):
    name, argv = job
    start = time.monotonic()
    with (packet / 'receipts' / (name + '.log')).open('w') as log:
        r = subprocess.run(argv, cwd=repo, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=590)
    elapsed = time.monotonic() - start
    (packet / 'receipts' / (name + '.rc')).write_text(f'{r.returncode} {elapsed:.3f}\n')
    print(name, 'rc', r.returncode, 'seconds', round(elapsed, 3), flush=True)
    return {'name': name, 'argv': argv, 'rc': r.returncode, 'seconds': elapsed}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, jobs))
(packet / 'receipts/execution.json').write_text(json.dumps(results, indent=2) + '\n')
raise SystemExit(int(any(r['rc'] for r in results)))
