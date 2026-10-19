#!/usr/bin/env python3
"""Run the bounded source checks in a disposable copy; no remote writes."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

packet = Path(__file__).resolve().parent
source = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else packet / 'scratch/source'
receipts = packet / 'receipts'
receipts.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(packet / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
compiler = env.get('REVIEW_VERILATOR', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')

def run(name, command):
    with (receipts / (name + '.log')).open('w') as log:
        rc = subprocess.run(command, cwd=source, env=env, stdout=log,
                            stderr=subprocess.STDOUT, check=False).returncode
    (receipts / (name + '.rc')).write_text(str(rc) + '\n')
    print(name, rc, flush=True)
    return rc

jobs = [
    ('dynmap-baseline', ['make', '-j16', '-C', 'tb/verilator/milan_dp', 'dynmap',
                         'VERILATOR=' + compiler, 'VERILATOR_JOBS=12']),
    ('record-space', ['python3', 'scripts/check_nvm_record_space.py', '--self-test']),
    ('capture', ['python3', 'scripts/check_nvm_capture.py']),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(lambda job: run(*job), jobs))
sys.exit(any(results))
