#!/usr/bin/env python3
"""Run independent scoped campaigns concurrently and join them in the foreground.

Usage: run_focused.py SOURCE PACKET SIMULATOR
All temporary copies stay in PACKET/scratch; no production file is changed.
"""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
import time

source, packet, simulator = map(Path, sys.argv[1:])
env = dict(os.environ, TMPDIR=str(packet / 'scratch'),
           PATH=str(packet / 'scratch/bin') + ':' + os.environ['PATH'],
           VERILATOR=str(simulator), PYTHONDONTWRITEBYTECODE='1')
jobs = {
    'srp-focused': ['python3', 'tb/srp_top/mutants.py', '--jobs', '2',
        '--output', str(packet / 'receipts/srp-focused'), '--only',
        'listener-rebind-abandons-leave,listener-declaration-not-held,listener-park-never-retires,listener-reprobe-abandons-leave,listener-reprobe-parks-own-stream,walk-ignores-leave-copy,lsid-ram-read-sink-0,lsid-flops-read-sink-0,lsid-ram-written-with-new-stream'],
    'acmp-focused': ['python3', 'tb/pp_top/acmp_mutants.py', '--jobs', '2',
        '--verilator', str(simulator), '--output', str(packet / 'receipts/acmp-focused'),
        '--only', 'rf_swap_unlatched', 'rf_swap_sticky', 'rebind_abandons_leave',
        'park_never_retires'],
    'docs': ['make', '-j16', 'check'],
}

def run(item):
    name, argv = item
    start = time.monotonic()
    with (packet / f'receipts/{name}.log').open('w') as f:
        f.write('COMMAND ' + repr(argv) + '\n'); f.flush()
        rc = subprocess.run(argv, cwd=source, env=env, stdout=f,
                            stderr=subprocess.STDOUT).returncode
    (packet / f'receipts/{name}.rc').write_text(str(rc) + '\n')
    print(f'{name}: rc={rc}, elapsed={time.monotonic()-start:.1f}s', flush=True)
    return rc

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    result = list(pool.map(run, jobs.items()))
sys.exit(any(result))
