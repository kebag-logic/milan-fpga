#!/usr/bin/env python3
"""Per-section check tallies of one milan_dp sim_nxn leg log.

usage: sections.py <leg.log>
A section opens at each '-- [TAG] ...' banner; every '[ok]'/'[FAIL]' line
counts toward the section open above it. Also counts lines labelled [762-DP]
and [MAPREC], and prints the leg's own 'checks:' line for comparison.
"""
import re
import sys

sec, order, tally = 'preamble', ['preamble'], {'preamble': [0, 0]}
lab = {'762-DP': [0, 0], 'MAPREC': [0, 0]}
leg = None
for line in open(sys.argv[1], errors='replace'):
    m = re.match(r'-- \[([^\]]+)\]', line)
    if m:
        sec = m.group(1)
        if sec not in tally:
            tally[sec] = [0, 0]
            order.append(sec)
        continue
    m = re.match(r'\s*\[(ok|FAIL)\]', line)
    if m:
        bad = m.group(1) == 'FAIL'
        tally[sec][0] += 1
        tally[sec][1] += bad
        for k in lab:
            if '[' + k + ']' in line:
                lab[k][0] += 1
                lab[k][1] += bad
    m = re.match(r'checks: (\d+)\s+failures: (\d+)', line)
    if m:
        leg = (int(m.group(1)), int(m.group(2)))
for s in order:
    print(f'section {s}: {tally[s][0]} checks, {tally[s][1]} failures')
for k, v in lab.items():
    print(f'labelled [{k}]: {v[0]} checks, {v[1]} failures')
print(f'sum: {sum(v[0] for v in tally.values())}; leg line: {leg}')
