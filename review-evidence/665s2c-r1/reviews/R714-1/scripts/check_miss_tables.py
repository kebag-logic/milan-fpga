#!/usr/bin/env python3
"""Check the README's 'Paths that still miss T_svc' tables against regraded table.md files.

usage: check_miss_tables.py README REGRADE_DIR

Each README row (path, interface, cacheless cell, 4 KiB cell, 4 KiB CPU cycles)
must equal the worst-instance row of that path and interface in the regraded
P<n>-none and P<n>-64x1 tables: the ms, the bound, the verdict and the worst
instance's CPU cycles. It also checks that the README lists exactly the
paths the 4 KiB regrade reports missing.
"""
import re
import sys
from pathlib import Path

readme, regrade = Path(sys.argv[1]).read_text(), Path(sys.argv[2])
VERDICT = {'MISS T_svc': '**miss**', 'MISS ceiling': '**over ceiling**', 'STARVED: never released': '**over ceiling**',
           'NEVER ANSWERED': '**over ceiling**', 'fits': ''}


def worst(arm: str) -> dict:
    text = (regrade / arm / 'table.md').read_text()
    rows = {}
    for line in text.splitlines():
        m = re.match(r'\| (.+?) \| (\d+) \| `([^`]+)` \((\S+)\) \| (?:at least )?([\d.]+)(?: \(([\d.]+)\))? \| ([^|]+) \| .* \| (\d+) \| (\d+) \|$',
                     line)
        if m:
            rows[(m.group(1), int(m.group(2)))] = dict(probe=m.group(3), ms=m.group(5), bound=m.group(6),
                                                       verdict=m.group(7).strip(), misses=int(m.group(9)))
    cycles = {}
    for line in text.splitlines():
        m = re.match(r'\| [^|]+ \| `([^`]+)` \| ([\d,]+) \| ([\d.]+) \|', line)
        if m:
            cycles.setdefault((m.group(1), m.group(3)), m.group(2))
    return rows, cycles


def cell(r: dict) -> str:
    ms = r['ms']  # three places, as the table carries it
    bound = f" ({r['bound']})" if r['bound'] else ''
    v = VERDICT[r['verdict']]
    return f'{ms}{bound}' + (f' {v}' if v else '')


def close(a: str, b: str) -> bool:
    # The README rounds full-precision ms to two places; the table carries three. A cell agrees
    # when its words match and every number is within 0.005 ms (one rounding of a rounded value).
    na, nb = re.findall(r'[\d.]+', a), re.findall(r'[\d.]+', b)
    return (re.sub(r'[\d.]+', '#', a) == re.sub(r'[\d.]+', '#', b) and len(na) == len(nb)
            and all(abs(float(x) - float(y)) <= 0.0051 for x, y in zip(na, nb)))


bad = 0
for point, n in (('1x1', '1'), ('8x8', '8')):
    none, _ = worst(f'P{n}-none')
    cached, cyc = worst(f'P{n}-64x1')
    section = readme.split(f'| {point}: path missing T_svc with the 4 KiB cache |', 1)[1].split('\n\n', 1)[0]
    listed = set()
    for line in section.splitlines()[2:]:
        parts = [p.strip() for p in line.strip('|').split('|')]
        path, iface, c0, c4, cycles = parts[0], int(parts[1]), parts[2], parts[3], parts[4]
        listed.add((path, iface))
        a, b = none.get((path, iface)), cached.get((path, iface))
        if not a or not b:
            print(f'{point} {path} if{iface}: not in the regrade'); bad += 1; continue
        got = (cell(a), cell(b), cyc.get((b['probe'], b['ms']), '?'))
        if not (close(got[0], c0) and close(got[1], c4) and got[2] == cycles):
            print(f'{point} {path} if{iface}: README {(c0, c4, cycles)} regrade {got}'); bad += 1
    missing = {k for k, r in cached.items() if r['misses']}
    if missing != listed:
        print(f'{point}: README lists {len(listed)}, regrade misses {len(missing)}; '
              f'unlisted {sorted(missing - listed)}, extra {sorted(listed - missing)}'); bad += 1
    print(f'{point}: {len(listed)} README rows checked against P{n}-none and P{n}-64x1')
print('mismatches:', bad)
