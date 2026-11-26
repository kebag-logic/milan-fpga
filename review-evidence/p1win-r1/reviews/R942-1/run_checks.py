#!/usr/bin/env python3
"""Run independent review checks concurrently; retain their output and exit codes."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
checks = {
    'store': [sys.executable, '-B', 'sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py', '--self-test', '--jobs', '12'],
    'budget_selftest': [sys.executable, '-B', 'tb/verilator/ctrl_service_budget/selftest.py'],
    'restore_selftest': [sys.executable, '-B', 'tb/verilator/nvm_split_target/run.py', '--self-test', '--jobs', '1'],
}

def run(item):
    name, argv = item
    start = time.monotonic()
    with (packet / (name + '.log')).open('w') as sink:
        sink.write('HEAD ' + subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip() + '\n')
        sink.write('COMMAND ' + ' '.join(argv) + '\n')
        sink.flush()
        result = subprocess.run(argv, cwd=root, env=env, stdout=sink, stderr=subprocess.STDOUT)
    (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(name, 'rc', result.returncode, 'seconds', round(time.monotonic() - start, 2), flush=True)
    return result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    codes = list(pool.map(run, checks.items()))
sys.exit(any(codes))
