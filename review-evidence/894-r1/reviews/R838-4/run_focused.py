#!/usr/bin/env python3
"""Focused review checks. Run from the candidate repository; outputs beside this script."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
py = [sys.executable, '-B']
budget = 'tb/verilator/ctrl_service_budget/'
checks = {
    'flip-1x1': py + [budget+'flip_grade.py', '--check', '--point', '1x1/1if'],
    'flip-selftest': py + [budget+'flip_grade.py', '--selftest'],
    'load': py + [budget+'load_grade.py', '--check'],
    'map-core': py + ['sw/firmware/ctrl/test/aecp_arms.py', '--output', str(scratch/'map-core'), '--core', '--filter', 'Core.Map*:Core.Every*'],
    'map-keys': py + ['sw/firmware/ctrl/test/aecp_arms.py', '--output', str(scratch/'map-keys'), '--keys'],
}

def run(item):
    name, command = item
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    with (packet/(name+'.log')).open('w') as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, env=env)
    (packet/(name+'.rc')).write_text(str(result.returncode)+'\n')
    return name, result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for name, rc in pool.map(run, checks.items()):
        print(name, rc, flush=True)
