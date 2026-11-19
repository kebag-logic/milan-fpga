#!/usr/bin/env python3
"""Run bounded independent read-only probes concurrently and retain each exit code."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

out = Path(sys.argv[1]).resolve()
python = sys.argv[2]
env = dict(os.environ, TMPDIR=str(out / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
tasks = {
    'ledger-probe': [python, '-B', str(out / 'probe_ledger.py')],
    'flip-check': [python, '-B', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--check'],
    'flip-selftest': [python, '-B', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--selftest'],
    'load-check': [python, '-B', 'tb/verilator/ctrl_service_budget/load_grade.py', '--check'],
    'load-selftest': [python, '-B', 'tb/verilator/ctrl_service_budget/load_grade.py', '--selftest'],
    'docs-check': [python, '-B', 'scripts/docs_check.py'],
    'diff-check': ['git', 'diff', '--check', 'cb96336d', 'HEAD'],
}
def run(item):
    label, command = item
    with (out / (label + '.log')).open('w') as log:
        rc = subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=500).returncode
    (out / (label + '.rc')).write_text(str(rc)+'\n')
    print(label, 'rc='+str(rc), flush=True)
    return rc == (1 if label == 'flip-check' else 0)
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
    results = list(pool.map(run, tasks.items()))
raise SystemExit(not all(results))
