#!/usr/bin/env python3
"""Run independent focused gates concurrently, waiting in this foreground process."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
cases = [('load-check', 'load_grade.py', '--check'),
         ('load-selftest', 'load_grade.py', '--selftest'),
         ('flip-1x1', 'flip_grade.py', '--check', '--point', '1x1/1if'),
         ('flip-8x8', 'flip_grade.py', '--check', '--point', '8x8/1if'),
         ('flip-selftest', 'flip_grade.py', '--selftest')]
def run(case):
    name, script, *args = case
    command = [sys.executable, '-B', str(root / 'tb/verilator/ctrl_service_budget' / script), *args]
    result = subprocess.run(command, cwd=root, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    (packet / (name + '.log')).write_bytes(result.stdout)
    (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
    return {'name': name, 'command': ['python3', '-B', 'tb/verilator/ctrl_service_budget/' + script, *args],
            'rc': result.returncode}
with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, cases))
print(json.dumps(results, indent=2))
assert all(r['rc'] == 0 for r in results)
