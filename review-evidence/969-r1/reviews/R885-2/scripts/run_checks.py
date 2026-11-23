#!/usr/bin/env python3
"""Run small independent checks concurrently, with raw logs and return codes.
Usage: python3 -I run_checks.py CHECKOUT PACKET
"""
import concurrent.futures
from pathlib import Path
import subprocess
import sys

root, packet = (Path(p).resolve() for p in sys.argv[1:])
out = packet / 'receipts' / 'checks'
out.mkdir(parents=True, exist_ok=True)
budget = root / 'tb/verilator/ctrl_service_budget'
tasks = [('flip-1x1', [sys.executable, '-I', str(budget/'flip_grade.py'), '--check', '--point', '1x1/1if']),
         ('flip-8x8', [sys.executable, '-I', str(budget/'flip_grade.py'), '--check', '--point', '8x8/1if']),
         ('load-check', [sys.executable, '-I', str(budget/'load_grade.py'), '--check']),
         ('shape-check', [sys.executable, '-I', str(budget/'shape_costs.py'), '--check']),
         ('docs-check', [sys.executable, str(root/'scripts/docs_check.py')]),
         ('verilator-identity', ['$VALIDATION_TOOLS/pinned-verilator-5.050/verilator', '--version'])]
for shape in ('endstation_ax7101_8x8', 'endstation_ax7101_1x1_tdm8'):
    exe = packet/'scratch/arms/head-platsinks'/f'test_plat_sinks_{shape}'
    tasks.append((f'platsinks-{shape}', [str(exe)]))

def run(task):
    name, cmd = task
    with (out/f'{name}.log').open('w') as log:
        rc = subprocess.run(cmd, cwd=root, stdout=log, stderr=subprocess.STDOUT).returncode
    (out/f'{name}.rc').write_text(f'{rc}\n')
    print(f'{name}: rc={rc}', flush=True)
    return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    values = list(pool.map(run, tasks))
sys.exit(int(any(values)))
