#!/usr/bin/env python3
"""Reproduce the departure-capacity boundary, with a smaller positive control.

Exit 0 means the counterexample reproduced (control 0, boundary 1).
The boundary executable itself returns 1 for the no-loss violation.
"""
import argparse
import os
from pathlib import Path
import subprocess
import time

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
a = ap.parse_args()
root, packet = a.repo.resolve(), a.packet.resolve()
exe = packet / 'scratch/queue-capacity'
cmd = [os.environ.get('CC', 'cc'), '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
       '-I' + str(root / 'sw/firmware/ctrl/adp'), '-I' + str(root / 'sw/firmware/ctrl/wire'),
       str(root / 'sw/firmware/ctrl/adp/adp.c'), str(packet / 'scripts/queue_capacity_probe.c'), '-o', str(exe)]
subprocess.run(cmd, check=True)
for name, count, expected in [('queue-capacity-control', 10000000, 0), ('queue-capacity', 4294967296, 1)]:
    start = time.monotonic()
    r = subprocess.run([str(exe), str(count)], capture_output=True, text=True, timeout=540)
    output = r.stdout + r.stderr + f'elapsed_seconds={time.monotonic()-start:.2f}\n'
    (packet / 'receipts' / (name + '.log')).write_text(output)
    (packet / 'receipts' / (name + '.rc')).write_text(str(r.returncode) + '\n')
    print(output, end='', flush=True)
    assert r.returncode == expected, (name, r.returncode, expected)
print('Counterexample reproduced with the unchanged source and public API calls.')
