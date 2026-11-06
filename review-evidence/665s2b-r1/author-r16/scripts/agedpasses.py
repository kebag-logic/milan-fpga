#!/usr/bin/env python3
"""The passes given whole to an aged step (THE STEP) at this head, per leg (#665): a STEPPASS line with aged=1 wrote
nothing to the mailbox; a PASS line with step=1 aged=1 did, as THE RETRY's round after the step does when it re-arms
AECP's timer. For each kind: how many, the longest pass in CPU cycles and ms, and for the work kind the longest of the
pass less the store's own cycles (the round, the loop's clock read and its call).

usage: agedpasses.py BUILDS LEG ...
"""
import re
import sys
from pathlib import Path

CPU_HZ = 100_000_000
builds, legs = Path(sys.argv[1]), sys.argv[2:]
for leg in legs:
    idle, work = [], []
    for log in sorted((builds / leg / 'results').glob('*.log')):
        for line in log.read_text(errors='replace').splitlines():
            if line.startswith('STEPPASS ') and line.endswith('aged=1'):
                k = line.split()
                idle.append((int(k[4]), int(k[5].partition('=')[2]), log.stem))
            elif line.startswith('PASS ') and ' step=1 ' in line and ' aged=1 ' in line:
                k = line.split(' W ')[0].split()
                store = int(re.search(r' store=(\d+)', line).group(1))
                work.append((int(k[4]), store, log.stem))
    for name, rows in (('STEPPASS aged=1 (no mailbox write)', idle), ('PASS step=1 aged=1 (a retry round after the step)', work)):
        if not rows:
            print(f'{leg} {name}: 0')
            continue
        top = max(rows)
        rest = max((c - s, g) for c, s, g in rows)
        print(f'{leg} {name}: {len(rows)}, the longest {top[0]:,} cycles ({top[0] / CPU_HZ * 1000:.3f} ms, {top[2]}); '
              f'less the store\'s own, the longest {rest[0]:,} cycles ({rest[1]})')
