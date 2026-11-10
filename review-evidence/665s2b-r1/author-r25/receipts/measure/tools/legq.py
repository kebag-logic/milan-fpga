#!/usr/bin/env python3
"""Run harness legs one after another: each queue line is CHECKOUT NAME POINT GROUPS [extra args...].
usage: legq.py QUEUE"""
import subprocess, sys, time
from pathlib import Path
L = Path('<scratch>/logs')
for line in Path(sys.argv[1]).read_text().splitlines():
    f = line.split()
    if not f or f[0].startswith('#'):
        continue
    with (L / 'legq.txt').open('a') as log:
        log.write(f'{time.strftime("%T")} start {f[1]}\n')
    subprocess.run(['bash', '<scratch>/scripts/leg.sh', *f])
    tail = (L / f'{f[1]}.log').read_text().splitlines()[-2:]
    with (L / 'legq.txt').open('a') as log:
        log.write(f'{time.strftime("%T")} end {f[1]} {" ".join(tail)}\n')
