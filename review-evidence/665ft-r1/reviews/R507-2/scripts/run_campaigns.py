#!/usr/bin/env python3
"""Run the four independent focused campaigns concurrently, retaining raw receipts.

Usage: python3 scripts/run_campaigns.py CHECKOUT PACKET
The driver stays in the foreground and joins every child before returning.
Python 3.13+ CPU-count overrides bound drivers without a --jobs switch.
"""
import concurrent.futures
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
scratch = packet / 'scratch'
receipts = packet / 'receipts'
scratch.mkdir(exist_ok=True)
receipts.mkdir(exist_ok=True)
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
campaigns = [
    ('ctrl', 4, ['sw/firmware/ctrl/test/test_ctrl_firmware.py', '--require-rv32', '--self-test',
                 '--build-dir', str(scratch / 'ctrl')]),
    ('nvm', 6, ['sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py', '--require-rv32', '--self-test', '--jobs', '6']),
    ('coverage', 4, ['sw/firmware/gtest/fw_coverage.py', '--check', '--jobs', '4', '--keep', str(scratch / 'coverage')]),
    ('tally', 2, ['sw/firmware/gtest/tally_selftest.py', '--mutants']),
]

def run(task):
    name, jobs, args = task
    env = dict(os.environ, TMPDIR=str(scratch), PYTHON_CPU_COUNT=str(jobs), PYTHONDONTWRITEBYTECODE='1',
               PYTHONUNBUFFERED='1')
    command = [sys.executable, '-B', '-X', f'cpu_count={jobs}', *args]
    (receipts / f'{name}.command').write_text(' '.join(command).replace(str(root), '<checkout>')
        .replace(str(packet), '<packet>') + '\n', encoding='utf-8')
    start = time.monotonic()
    with (receipts / f'{name}.log').open('w') as log:
        result = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
    (receipts / f'{name}.rc').write_text(f'{result.returncode}\n')
    print(f'{name}: rc={result.returncode}, seconds={time.monotonic()-start:.1f}', flush=True)
    return result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, campaigns))
raise SystemExit(1 if any(results) else 0)
