#!/usr/bin/env python3
"""Reproduce the changed model statements and their small focused controls."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet / 'scratch'))
jobs = {
    'load-check': ['tb/verilator/ctrl_service_budget/load_grade.py', '--check'],
    'load-selftest': ['tb/verilator/ctrl_service_budget/load_grade.py', '--selftest'],
    'flip-1x1': ['tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point', '1x1/1if'],
    'flip-8x8': ['tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point', '8x8/1if'],
    'shape-check': ['tb/verilator/ctrl_service_budget/shape_costs.py', '--check'],
    'hot-check': ['sw/firmware/ctrl/test/ctrl_hot.py', '--check'],
}
def run(item):
    name, args = item
    result = subprocess.run([sys.executable, '-B', *args], cwd=root, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    (packet / f'{name}.log').write_text(result.stdout)
    (packet / f'{name}.rc').write_text(f'{result.returncode}\n')
    return name, result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, jobs.items()))
for name, rc in results:
    print(name, rc)
sys.exit(int(any(rc for _, rc in results)))
