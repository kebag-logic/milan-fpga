#!/usr/bin/env python3
"""Recheck the reported required-gate failures without invoking any full bank."""
import concurrent.futures
import os
from pathlib import Path
import subprocess

p = Path(__file__).resolve().parent
src = p / 'scratch/source'
env = dict(os.environ, TMPDIR=str(p / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
def run(item):
    name, command = item
    with (p / 'receipts' / (name + '.log')).open('w') as f:
        rc = subprocess.run(command, cwd=src, env=env, stdout=f,
                            stderr=subprocess.STDOUT, check=False).returncode
    (p / 'receipts' / (name + '.rc')).write_text(str(rc) + '\n')
    print(name, rc, flush=True)
jobs = [
    ('port-contracts', ['python3', 'scripts/check_port_contracts.py']),
    ('cpp-idiom', ['python3', 'scripts/check_cpp_idiom.py']),
    ('test-evidence', ['python3', 'scripts/measure_test_evidence.py', '--check']),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(run, jobs))
