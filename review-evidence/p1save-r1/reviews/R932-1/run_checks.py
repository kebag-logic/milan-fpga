#!/usr/bin/env python3
"""Run the focused review checks; keep temporary outputs in packet/scratch."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
tasks = {
    'store': [sys.executable, '-B', 'sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py', '--require-rv32', '--self-test', '--jobs', '12'],
    'budget-selftest': [sys.executable, '-B', 'tb/verilator/ctrl_service_budget/selftest.py'],
    'memory': [sys.executable, '-B', 'sw/litex/test_ctrl_memory.py'],
}

def run(item):
    name, cmd = item
    with (packet / (name + '.log')).open('w') as log:
        log.write('COMMAND ' + ' '.join(cmd) + '\n')
        log.flush()
        result = subprocess.run(cmd, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=1800)
    (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
    return name, result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(run, item) for item in tasks.items()]
    for f in concurrent.futures.as_completed(futures):
        print(*f.result(), flush=True)
