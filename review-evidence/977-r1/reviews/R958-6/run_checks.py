#!/usr/bin/env python3
"""Run independent lightweight gates concurrently; wait in the foreground."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
HARNESS = 'tb/verilator/ctrl_service_budget/'
CHECKS = {
    'load-check': ['load_grade.py', '--check'],
    'load-selftest': ['load_grade.py', '--selftest'],
    'delivery-controls': ['load_deliveries.py'],
    'flip-1x1': ['flip_grade.py', '--check', '--point', '1x1/1if'],
    'flip-8x8': ['flip_grade.py', '--check', '--point', '8x8/1if'],
    'flip-selftest': ['flip_grade.py', '--selftest'],
}
def run(item):
    name, args = item
    command = [sys.executable, '-B', HARNESS + args[0], *args[1:]]
    with (OUT / (name + '.log')).open('w') as log:
        p = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, timeout=540)
    (OUT / (name + '.rc')).write_text(str(p.returncode) + '\n')
    return {'name': name, 'command': ['python3', '-B', HARNESS + args[0], *args[1:]], 'rc': p.returncode}
with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, CHECKS.items()))
(OUT / 'checks.json').write_text(json.dumps(results, indent=2) + '\n')
for result in results:
    print(result['name'], 'rc=' + str(result['rc']))
assert all(x['rc'] == 0 for x in results)
