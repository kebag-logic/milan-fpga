#!/usr/bin/env python3
"""The 32x32 service estimate (#640 D12, #665) from this round's legs: a derivation, never a measurement.

usage: estimate14.py CHECKOUT BUILDS OUT.md A1,B1 A8,B8 A81
The rows are each leg's worst over the four backlog windows (rows13.py's), the CPU on sys at 100 MHz.
U, the assigned derivation: four times the 8x8/2if measurement, the worse arm.
L, the measured growth: the line through 1x1/1if and 8x8/2if (the worse arm at each end), carried to 64 streams.
S, the streams' own growth: 8x8/2if (the worse arm) plus the slope from 1x1/1if to 8x8/1if, both arm A, which
holds the interfaces fixed: the scratch 8x8/1if point is arm A only, so the slope uses arm A at both ends.
Each row's bound is min(T_svc, its family's ceiling), FR_NFR.md 3.4.1.
"""
import json
import sys
from pathlib import Path

checkout, builds, out, a1, a8, a81 = sys.argv[1:7]
sys.path.insert(0, str(Path(checkout) / 'tb/verilator/ctrl_service_budget'))
sys.path.insert(0, str(Path(checkout) / 'sw/mailbox'))
sys.argv = [sys.argv[0], checkout, builds, '/dev/null']
sys.path.insert(0, str(Path(__file__).parent))
import rows14 as rows13  # noqa: E402

ROWS = ('ACMP record, first', 'ADP record, first', 'MAAP record, first', 'AECP record, first', 'SRP record, first',
        'ACMP record, last', 'ADP record, last', 'MAAP record, last', 'AECP record, last', 'SRP record, last',
        'an ACMP command behind a full acmp ring', 'an ENTITY_AVAILABLE behind a full adp ring',
        'an event behind 15 others')
load = lambda names: [rows13.load(Path(builds) / n) for n in names.split(',')]
p1, p8, p81 = load(a1), load(a8), load(a81)
ms = lambda res, row: rows13.worst(res, 'backlog')[row][0][1]
worst = lambda legs, row: max(ms(r, row) for r in legs)
longest = lambda legs: max(rows13.shares(r, 'backlog')[2] for r in legs)
fmt = lambda v: f'{v:.2f}'
over = lambda v, b: f'**{v:.1f}** (+{v - b:.1f})' if v > b else f'{v:.1f}'
lines = ['Measured with the CPU on sys at 100 MHz; the 32x32 columns are estimates, not measurements. ms; over the '
         'bound in bold, with the excess.', '',
         '| Row | Bound | 1x1/1if | 8x8/1if | 8x8/2if | Estimate U, 4 x 8x8/2if | Estimate L, the measured line | '
         'Estimate S, the streams alone |', '|---|---:|---:|---:|---:|---:|---:|---:|']
summary = {}
for row in ROWS:
    b = rows13.worst(p8[0], 'backlog')[row][2]
    t1, t8, t81 = worst(p1, row), worst(p8, row), ms(p81[0], row)
    u, l, s = 4 * t8, t8 + (t8 - t1) * 48 / 14, t8 + (t81 - ms(p1[0], row)) * 48 / 14
    summary[row] = dict(bound=b, u=u, l=l, s=s)
    lines.append(f'| {row} | {b:g} | {fmt(t1)} | {fmt(t81)} | {fmt(t8)} | {over(u, b)} | {over(l, b)} | {over(s, b)} |')
t1, t8, t81 = longest(p1), longest(p8), longest(p81)
u, l, s = 4 * t8, t8 + (t8 - t1) * 48 / 14, t8 + (t81 - rows13.shares(p1[0], 'backlog')[2]) * 48 / 14
summary['pass'] = dict(bound=2, u=u, l=l, s=s)
lines.append(f'| The longest work pass | 2 | {fmt(t1)} | {fmt(t81)} | {fmt(t8)} | {over(u, 2)} | {over(l, 2)} | {over(s, 2)} |')
lines.append('')
Path(out).write_text('\n'.join(lines) + '\n')
Path(out).with_suffix('.json').write_text(json.dumps(summary, indent=1) + '\n')
print('\n'.join(lines))
