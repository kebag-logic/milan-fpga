#!/usr/bin/env python3
"""Summarise the review's flood-preceded window probes from the harness's own per-group grades and logs.

For each <group>.json/<group>.log pair in the given directories: the composed window's open (MARK composed) and end
(MARK composed_end), the flood (FLOOD lines), every pass that carries the store's step (STEPPASS lines, and work passes
printed with step=1) from 40 ms before the window to its end, and the graded rows' last-record times.

usage: python3 -I window_probe.py <dir> [<dir> ...]
"""
import json
import re
import sys
from pathlib import Path

SYS_HZ = 100_000_000
ROWS = ('service.srp.last', 'service.aecp.last', 'service.acmp.last', 'adp_available')


def ms(cycles: int) -> float:
    return cycles * 1000 / SYS_HZ


for d in map(Path, sys.argv[1:]):
    print(f'== {d}')
    for js in sorted(d.glob('*.json')):
        if js.name == 'results.json':
            continue
        name = js.stem
        log = (d / f'{name}.log').read_text(errors='replace').splitlines()
        marks = {m.group(2): int(m.group(1)) for m in (re.match(r'MARK (\d+) (\S+)$', l) for l in log) if m}
        opened, ended = marks.get('composed'), marks.get('composed_end')
        floods = [l for l in log if l.startswith('FLOOD ')]
        steps = []
        for line in log:
            if line.startswith('STEPPASS '):
                f = line.split()
                steps.append((int(f[2]), int(f[4]), 'idle'))
            elif line.startswith('PASS ') and ' step=1 ' in line:
                f = line.split()
                steps.append((int(f[2]), int(f[4]), 'work'))
        near = [s for s in steps if opened - 40 * SYS_HZ // 1000 <= s[0] <= ended]
        inside = [s for s in near if opened <= s[0] <= ended]
        grade = json.load(open(js))
        rows = {key: next((p['ms'] for p in grade['probes'] if key in p['probe']), None) for key in ROWS}
        longest = max((p['cycles'] for p in grade.get('passes', []) if isinstance(p, dict) and 'cycles' in p),
                      default=None)
        print(f'{name}: flood {[" ".join(x.split()[1:4]) for x in floods]}; window {ms(ended - opened):.3f} ms; '
              f'step passes from 40 ms before: '
              + ', '.join(f'{ms(c - opened):+.2f} ms ({k}, {n} cycles)' for c, n, k in near)
              + f'; inside the window: {len(inside)}; rows ms: '
              + ', '.join(f'{k} {v}' for k, v in rows.items()))
