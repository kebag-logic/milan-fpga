#!/usr/bin/env python3
"""Run independent, lightweight checks concurrently; remain attached until all finish."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
BASE = 'tb/verilator/ctrl_service_budget/'
JOBS = {
    'load-check': ['python3', '-B', BASE + 'load_grade.py', '--check'],
    'load-selftest': ['python3', '-B', BASE + 'load_grade.py', '--selftest'],
    'deliveries-controls': ['python3', '-B', BASE + 'load_deliveries.py'],
    'flip-1x1': ['python3', '-B', BASE + 'flip_grade.py', '--check', '--point', '1x1/1if'],
    'flip-8x8': ['python3', '-B', BASE + 'flip_grade.py', '--check', '--point', '8x8/1if'],
    'flip-selftest': ['python3', '-B', BASE + 'flip_grade.py', '--selftest'],
    'diff-check': ['git', 'diff', '--check', 'origin/dev-soft-core..HEAD'],
}

def run(job):
    name, argv = job
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_NO_REPLACE_OBJECTS='1')
    result = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, timeout=300)
    (OUT / (name + '.log')).write_bytes(result.stdout)
    (OUT / (name + '.rc')).write_text(str(result.returncode) + '\n')
    return {'name': name, 'command': argv, 'rc': result.returncode}

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(run, JOBS.items()))
(OUT / 'checks.json').write_text(json.dumps(results, indent=2) + '\n')
for result in results:
    print(result['name'], result['rc'])
assert all(r['rc'] == 0 for r in results)
