#!/usr/bin/env python3
"""Run small independent checks concurrently, with a foreground join and receipts.

Usage: python3 scripts/run-focused.py SOURCE PACKET
Prerequisites: PACKET/scratch/python has wavedrom==2.0.3.post3; mmdc is on PATH;
PACKET/scratch/suites is a detached copy of SOURCE. VERILATOR_BIN may override
the scoped simulator binary. Three builds use four compilation workers each.
"""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
import time

source, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
receipts = packet / 'receipts'
scratch = packet / 'scratch'
env = os.environ.copy()
env['PATH'] = str(scratch / 'python/bin') + os.pathsep + env['PATH']
env['TMPDIR'] = str(scratch)
env['PYTHONDONTWRITEBYTECODE'] = '1'
sim = env.get('VERILATOR_BIN', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
wrapper = scratch / 'sim-four.py'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\n'
                   'for i in range(len(a)-1):\n'
                   ' if a[i]=="-j": a[i+1]="4"\n'
                   'os.execv(' + repr(sim) + ',[' + repr(sim) + ']+a)\n')
wrapper.chmod(0o755)
tasks = [('make-check', source, ['make', '-j16', 'check']),
         ('make-ids', source, ['make', '-j16', 'ids'])]
tasks += [(s, scratch / 'suites/tb' / s,
           ['make', '-j16', 'VERILATOR=' + str(wrapper)])
          for s in ('rx_validator', 'tx_arbiter', 'side_port')]

def run(task):
    name, cwd, argv = task
    start = time.monotonic()
    with (receipts / (name + '.log')).open('w') as f:
        f.write('command: ' + repr(argv) + '\ncwd: ' + str(cwd) + '\n')
        f.flush()
        proc = subprocess.run(argv, cwd=cwd, env=env, stdout=f,
                              stderr=subprocess.STDOUT, timeout=540)
        f.write(f'\nexit={proc.returncode} elapsed={time.monotonic()-start:.3f}s\n')
    (receipts / (name + '.rc')).write_text(str(proc.returncode) + '\n')
    print(name, 'rc', proc.returncode, flush=True)
    return proc.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(run, tasks))
sys.exit(1 if any(results) else 0)
