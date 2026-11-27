#!/usr/bin/env python3
"""Run focused independent checks concurrently, waiting for every child."""
import concurrent.futures
import json
import os
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
base = 'tb/verilator/ctrl_service_budget/'
commands = {
    'load-check': [sys.executable, base + 'load_grade.py', '--check', '--selftest'],
    'flip-1if-check': [sys.executable, base + 'flip_grade.py', '--check', '--point', '8x8/1if', '--selftest'],
    'flip-small-check': [sys.executable, base + 'flip_grade.py', '--check', '--point', '1x1/1if'],
    'shape-check': [sys.executable, base + 'shape_costs.py', '--check', '--selftest'],
    'whitespace-current': ['git', 'diff', '--check', 'origin/dev-soft-core', 'HEAD'],
    'whitespace-before': ['git', 'diff', '--check', '71bad8c0', '9976b94f'],
}
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch))

def run(item):
    name, command = item
    with (packet / (name + '.log')).open('w') as out:
        result = subprocess.run(command, cwd=repo, env=env, stdout=out, stderr=subprocess.STDOUT, timeout=540)
    (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
    return {'name': name, 'command': command, 'returncode': result.returncode,
            'expected': 2 if name == 'whitespace-before' else 0}

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands.items()))
(packet / 'checks.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
sys.exit(any(r['returncode'] != r['expected'] for r in results))
