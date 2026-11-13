#!/usr/bin/env python3
"""Run independent lightweight review checks concurrently, with foreground supervision."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
out = packet / 'checks'
out.mkdir(exist_ok=True)
base = 'tb/verilator/ctrl_service_budget/'
checks = {
    'flip': ['python3', '-B', base+'flip_grade.py', '--check', '--point', '1x1/1if'],
    'flip_controls': ['python3', '-B', base+'flip_grade.py', '--selftest'],
    'tier_controls': ['python3', '-B', base+'rows_tiers.py', '--selftest'],
    'load': ['python3', '-B', base+'load_grade.py', '--check'],
    'load_controls': ['python3', '-B', base+'load_grade.py', '--selftest'],
    'join_horizon': ['python3', '-B', str(packet/'probe_join.py'), str(root)],
}
def run(item):
    name, cmd = item
    with (out/(name+'.log')).open('w') as f:
        f.write('Command: '+' '.join(cmd)+'\n'); f.flush()
        result = subprocess.run(cmd, cwd=root, stdout=f, stderr=subprocess.STDOUT,
                                timeout=540, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    (out/(name+'.rc')).write_text(str(result.returncode)+'\n')
    return name, result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    for name, rc in pool.map(run, checks.items()):
        print(name, rc, flush=True)
