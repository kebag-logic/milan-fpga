#!/usr/bin/env python3
"""Usage: focused_probe.py CHECKOUT PACKET LITEX_PYTHON

Runs the changed transaction gate with extra diagnostic assertions and the
timing/layout gate concurrently. All scratch files stay under PACKET/scratch.
No source files are changed. No hardware programmer is invoked.
"""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

root, packet = map(Path, sys.argv[1:3])
litex = sys.argv[3]
tmp = packet / 'scratch/tmp'
tmp.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(tmp), PYTHONDONTWRITEBYTECODE='1',
           MILAN_LITEX_PYTHON=litex)
transaction = r'''
import sys, subprocess
sys.path.insert(0, 'sw/builder')
import test_builder
original = subprocess.run
seen = {'layout': 0, 'die': 0, 'duplicate': 0}
def checked(*args, **kwargs):
    r = original(*args, **kwargs)
    if isinstance(r.stdout, str) and isinstance(r.stderr, str):
        output = r.stdout + r.stderr
        if '[deploy] REFUSED:' in output:
            for key, cause in [('layout', 'target layout names no flash device'),
                               ('die', 'JTAG-detected part xc7a200t does not match')]:
                if cause in output:
                    assert "the image set's layout or the FPGA on the cable fails the board check" in output, output
                    assert 'the FPGA on the cable is not the image set' not in output, output
                    seen[key] += 1
                    print('DIAGNOSTIC', key, 'rc', r.returncode)
            if "['xc7a100', 'xc7a100']" in output:
                seen['duplicate'] += 1
                print('DUPLICATE-DIE refusal rc', r.returncode)
    return r
subprocess.run = checked
test_builder.test_qspi_owner_transition_completed_write_prefixes()
assert all(n >= 3 for n in seen.values()), seen
print('PASS: transaction, real 200T map, all persistent refusal paths;', seen)
'''
jobs = [('transaction', [sys.executable, '-B', '-c', transaction]),
        ('timing-layout', [sys.executable, '-B', 'sw/builder/test_timing_grade.py', litex])]
def run(job):
    name, argv = job
    result = subprocess.run(argv, cwd=root, env=env, capture_output=True, text=True, timeout=580)
    output = result.stdout + result.stderr
    for a, b in [(str(root), '<checkout>'), (str(packet), '<packet>'), (litex, '<litex-python>')]:
        output = output.replace(a, b)
    (packet / (name + '.log')).write_text(output)
    (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(name, 'rc', result.returncode, flush=True)
    return result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, jobs))
raise SystemExit(int(any(results)))
