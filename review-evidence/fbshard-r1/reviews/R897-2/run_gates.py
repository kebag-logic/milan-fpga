#!/usr/bin/env python3
"""Run focused independent checks concurrently, retaining each log and exit code."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet = map(lambda s: Path(s).resolve(), sys.argv[1:])
commands = [
    ['scripts/ci_gate_workflows.py', '--check'],
    ['scripts/ci_events.py', '--check'],
    ['scripts/ci_fail_fast_selftest.py'],
    ['scripts/ci_runtime_evidence_selftest.py'],
]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet / 'scratch'))
def run(args):
    name = Path(args[0]).stem
    start = time.monotonic()
    with (packet / (name + '.log')).open('w') as log:
        log.write('head 5392adf989349b68cfbb54d91fd0413c5b745521\n')
        log.flush()
        rc = subprocess.run([sys.executable, *args], cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=550).returncode
    (packet / (name + '.rc')).write_text(str(rc) + '\n')
    return {'command': ['python3', *args], 'rc': rc, 'seconds': round(time.monotonic() - start, 3)}
with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands))
(packet / 'gates.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
assert all(r['rc'] == 0 for r in results)
