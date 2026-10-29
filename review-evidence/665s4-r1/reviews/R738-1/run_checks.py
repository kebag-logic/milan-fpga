#!/usr/bin/env python3
"""Run independent focused checks concurrently, keeping raw output and exit status."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
checks = {
    'flash-map-selftest': ['python3', '-B', 'sw/firmware/ctrl_nvm/plat/gen_flash_port.py', '--self-test'],
    'target-selftest': ['python3', '-B', 'tb/verilator/nvm_split_target/run.py', '--self-test'],
    'budget-selftest': ['python3', '-B', 'tb/verilator/ctrl_service_budget/run.py', '--self-test'],
    'current-capture-gate': ['python3', '-B', 'scripts/check_nvm_capture.py'],
    'record-space': ['python3', '-B', 'scripts/check_nvm_record_space.py'],
}

def run(item):
    name, argv = item
    with (packet / (name + '.log')).open('w') as log:
        log.write('COMMAND ' + ' '.join(argv) + '\n')
        log.flush()
        rc = subprocess.run(argv, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, check=False).returncode
    (packet / (name + '.rc')).write_text(str(rc) + '\n')
    return name, rc

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    results = dict(pool.map(run, checks.items()))
print(json.dumps(results, indent=2))
sys.exit(int(any(results.values())))
