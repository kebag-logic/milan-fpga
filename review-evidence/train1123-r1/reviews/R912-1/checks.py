#!/usr/bin/env python3
"""Run focused review checks, synchronously; all temporary files stay in packet scratch."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
(packet / 'scratch' / 'tmp').mkdir(parents=True, exist_ok=True)
(packet / 'receipts').mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0',
           TMPDIR=str(packet / 'scratch' / 'tmp'))
py = sys.executable
budget = 'tb/verilator/ctrl_service_budget/'
checks = {
    'kept-selftest': [py, '-B', budget + 'kept_grade.py', '--selftest'],
    'load-check': [py, '-B', budget + 'load_grade.py', '--check'],
    'flip-one': [py, '-B', budget + 'flip_grade.py', '--check', '--point', '1x1/1if'],
    'flip-eight': [py, '-B', budget + 'flip_grade.py', '--check', '--point', '8x8/1if'],
    'shape-check': [py, '-B', budget + 'shape_costs.py', '--check'],
    'memory-check': [py, '-B', 'sw/litex/test_ctrl_memory.py'],
    'harness-selftest': [py, '-B', budget + 'run.py', '--self-test'],
}

def run(item):
    name, command = item
    started = time.monotonic()
    with (packet / 'receipts' / (name + '.log')).open('w') as log:
        log.write('COMMAND ' + ' '.join(['python3', *command[1:]]) + '\n')
        log.flush()
        try:
            rc = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT,
                                timeout=550).returncode
        except subprocess.TimeoutExpired:
            rc = 124
            log.write('\nINCOMPLETE: review time limit of 550 seconds reached.\n')
        log.write(f'\nEXIT {rc}\n')
    (packet / 'receipts' / (name + '.rc')).write_text(str(rc) + '\n')
    return dict(check=name, rc=rc, seconds=round(time.monotonic() - started, 2))

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(run, checks.items()))
print(json.dumps(rows, indent=2))
(packet / 'receipts' / 'checks.json').write_text(json.dumps(rows, indent=2) + '\n')
raise SystemExit(any(row['rc'] for row in rows))
