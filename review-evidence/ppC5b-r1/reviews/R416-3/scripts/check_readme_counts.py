#!/usr/bin/env python3
"""Compare the AECP dispatch mutation table of tb/pp_top/README.md with one or
more campaign results.json files, and count table rows whose cell count
differs from their header (code spans with '|' are not split).

Usage: check_readme_counts.py README.md results.json [results.json ...]
Exit 0 when every arm has exactly one row, every row's last cell equals the
measured failure count, every measured arm is KILLED, and no row of the table
is off its header."""
import json, re, sys

def cells(line):
    out, cur, code = [], '', False
    for ch in line.strip().strip('|'):
        if ch == '`': code = not code
        if ch == '|' and not code:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    return [c.strip() for c in out]

lines = open(sys.argv[1]).read().split('\n')
start = next(i for i, l in enumerate(lines) if l.startswith('### AECP dispatch and response negative controls'))
hdr = next(i for i in range(start, len(lines)) if lines[i].startswith('| Arm |'))
ncol = len(cells(lines[hdr]))
rows = {}
off = 0
for l in lines[hdr + 2:]:
    if not l.startswith('|'):
        break
    c = cells(l)
    if len(c) != ncol:
        off += 1
        print('OFF-HEADER ROW:', len(c), 'cells:', l[:100])
    arm = c[0].strip('`')
    if arm in rows:
        print('DUPLICATE ROW', arm)
        off += 1
    rows[arm] = c[-1]
measured = {}
for f in sys.argv[2:]:
    for r in json.load(open(f)):
        if 'patch' in r:
            measured[r['arm']] = r
bad = off
for arm, r in measured.items():
    cell = rows.get(arm)
    ok = cell == str(r['failures']) and r['verdict'] == 'KILLED'
    print(f"{'OK ' if ok else 'BAD'} {arm}: README {cell!r} measured {r['failures']} {r['verdict']}")
    bad += not ok
for arm in rows:
    if arm not in measured:
        print('ROW WITHOUT MEASUREMENT', arm); bad += 1
print(f'{len(rows)} rows, {len(measured)} measured arms, header {ncol} columns, {off} rows off header, {bad} problems')
sys.exit(1 if bad else 0)
