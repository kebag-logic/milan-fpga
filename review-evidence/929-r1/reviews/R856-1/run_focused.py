#!/usr/bin/env python3
"""Foreground supervisor; joins independent checks and records every rc.
Usage: run_focused.py CHECKOUT PACKET VERILATOR
"""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

root, packet, verilator = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
env = dict(os.environ, TMPDIR=str(packet / 'scratch'), PYTHONDONTWRITEBYTECODE='1')

def run(name, cmd):
    with (packet / (name + '.log')).open('w') as f:
        f.write('COMMAND ' + repr(cmd) + '\n'); f.flush()
        result = subprocess.run(cmd, cwd=root, env=env, stdout=f, stderr=subprocess.STDOUT)
    (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(f'{name}: rc {result.returncode}', flush=True)
    return result.returncode

make = ['make', '-j16', '-C', 'tb/verilator/milan_dp', 'VERILATOR=' + verilator,
        'VERILATOR_JOBS=4', 'TWIN_FW_ARGS=--jobs 4']
def twin():
    first = run('twin', make + ['twin'])
    return first or run('twin-plants', make + ['twin-plants'])

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(twin), pool.submit(run, 'srp-focused',
               [sys.executable, '-B', str(packet / 'focused_srp.py'), str(root), str(packet), '--jobs', '4'])]
    results = [f.result() for f in futures]
sys.exit(any(results))
