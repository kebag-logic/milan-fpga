#!/usr/bin/env python3
"""Run focused review checks concurrently, joined by this foreground process.
Usage: python3 run_checks.py REPOSITORY OUTPUT
"""
import concurrent.futures
import pathlib
import subprocess
import sys

root, out = map(pathlib.Path, sys.argv[1:])
out.mkdir(parents=True, exist_ok=True)
budget = 'tb/verilator/ctrl_service_budget/'
checks = {
    'flip-check': [budget+'flip_grade.py', '--check', '--point', '1x1/1if'],
    'flip-selftest': [budget+'flip_grade.py', '--selftest'],
    'load-check': [budget+'load_grade.py', '--check'],
    'load-selftest': [budget+'load_grade.py', '--selftest'],
    'rows-selftest': [budget+'rows_tiers.py', '--selftest'],
    'record-selftest': [budget+'record_classes.py', '--selftest'],
    'grid': [budget+'tier_grid.py', '--point', '1x1/1if'],
}
def run(item):
    name, args = item
    cmd = [sys.executable, '-B', *args]
    with (out/(name+'.log')).open('w') as log:
        log.write('COMMAND: '+' '.join(['python3', '-B', *args])+'\n')
        log.flush()
        rc = subprocess.run(cmd, cwd=root, stdout=log, stderr=subprocess.STDOUT).returncode
    (out/(name+'.rc')).write_text(str(rc)+'\n')
    print(name, rc, flush=True)
    return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, checks.items()))
sys.exit(any(results))
