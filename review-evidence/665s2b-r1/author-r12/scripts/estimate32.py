#!/usr/bin/env python3
"""The 32x32 service estimate (#640 D12, #665): a derivation from this round's measured legs, never a measurement.

usage: estimate32.py BUILDS OUT.md A1,B1 A8,B8 A81 [none-A1 none-A8 soci-A1 soci-A8]
Each leg is a directory under BUILDS. Every leg must record its CPU on sys at 100 MHz.

U, the assigned derivation: four times the 8x8/2if measurement, every cycle taken to grow with the streams.
L, the measured growth: the line through 1x1/1if (2 streams) and 8x8/2if (16 streams), carried to 64 streams.
S, the streams' own growth: 8x8/2if plus the slope of 1x1/1if to 8x8/1if, which holds the interfaces fixed.
Each row's bound is min(T_svc, its family's ceiling), FR_NFR.md 3.4.1."""
import gzip
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, '$LANES/665-s2b-cycles/tb/verilator/ctrl_service_budget')
sys.path.insert(0, str(Path(__file__).parent))
import rows12  # noqa: E402
import grade  # noqa: E402

ROWS = ('ACMP record, first', 'ADP record, first', 'MAAP record, first', 'AECP record, first', 'SRP record, first',
        'ACMP record, last', 'ADP record, last', 'MAAP record, last', 'AECP record, last', 'SRP record, last',
        'an ACMP command behind a full acmp ring', 'an ENTITY_AVAILABLE behind a full adp ring',
        'an event behind 15 others')
GROUPS = rows12.GROUPS


def worst_ms(legs: list, row: str) -> float:
    return max(rows12.worst(res)[row][0][1] for res, _ in legs)


def longest(legs: list) -> float:
    return max(rows12.shares(res)[2] for res, _ in legs)


def idle_pass(res: dict) -> tuple[int, int]:
    groups = [g for g in res['results'] if g['group'] in GROUPS]
    return min(g['passes']['idle_min'] for g in groups), max(g['passes']['idle_max'] for g in groups)


def steady(build: Path) -> float:
    """Work-pass CPU cycles over the bus cycles from 'settled' to 'composed', in the backlog group's quiet stretch."""
    log = grade.parse((build / 'results/backlog.log').read_text(errors='replace'), 100_000_000, 100_000_000)
    marks = {n: c for c, n in log.marks}
    a, b = marks['settled'], marks['composed']
    return sum(p.cycles for p in log.passes if a <= p.start_sys < b) / (b - a)


def fmt(v: float) -> str:
    return f'{v:.2f}'


def over(v: float, b: float) -> str:
    return f'**{v:.1f}** (+{v - b:.1f})' if v > b else f'{v:.1f}'


def main() -> int:
    root, out, a1, a8, a81, *rest = sys.argv[1:]
    root = Path(root)
    load = lambda names: [rows12.load(root / n) for n in names.split(',')]
    p1, p8, p81 = load(a1), load(a8), load(a81)
    lines = ['Measured with the CPU on sys at 100 MHz; the 32x32 columns are estimates, not measurements. ms; '
             'over the bound in bold, with the excess.', '',
             '| Row | Bound | 1x1/1if | 8x8/1if | 8x8/2if | Estimate U, 4 x 8x8/2if | Estimate L, the measured line | '
             'Estimate S, the streams alone |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    for row in ROWS:
        b = rows12.worst(p8[0][0])[row][2]
        t1, t8, t81 = worst_ms(p1, row), worst_ms(p8, row), worst_ms(p81, row)
        u = 4 * t8
        l = t8 + (t8 - t1) * 48 / 14
        s = t8 + (t81 - t1) * 48 / 14
        lines.append(f'| {row} | {b:g} | {fmt(t1)} | {fmt(t81)} | {fmt(t8)} | {over(u, b)} | {over(l, b)} | {over(s, b)} |')
    t1, t8, t81 = longest(p1), longest(p8), longest(p81)
    u, l, s = 4 * t8, t8 + (t8 - t1) * 48 / 14, t8 + (t81 - t1) * 48 / 14
    lines.append(f'| The longest work pass | 2 | {fmt(t1)} | {fmt(t81)} | {fmt(t8)} | {over(u, 2)} | {over(l, 2)} | {over(s, 2)} |')
    lines.append('')
    for name, legs in (('1x1/1if', p1), ('8x8/1if', p81), ('8x8/2if', p8)):
        low, high = idle_pass(legs[0][0])
        lines.append(f'- {name}: an idle pass takes {low:,} to {high:,} CPU cycles.')
    lines.append('')
    sa = {n: steady(root / n) for n in (a1.split(',')[0], a81, a8.split(',')[0])}
    lines.append('Quiet work load, work-pass cycles over elapsed cycles from `settled` to `composed` (arm A): ' +
                 ', '.join(f'{k} {100 * v:.2f} %' for k, v in sa.items()) + '.')
    if rest:
        lines += ['', 'The one-CPU arms, 8x8 and 1x1, the same rows (arm A, ms):', '',
                  '| Row | Bound | Split CPU 1x1 | cacheless RV32IM 1x1 | cacheless RV32I 1x1 | Split CPU 8x8 | cacheless RV32IM 8x8 | cacheless RV32I 8x8 |',
                  '|---|---:|---:|---:|---:|---:|---:|---:|']
        none1, none8, soci1, soci8 = (rows12.load(root / n) for n in rest)
        for row in ROWS:
            b = rows12.worst(p8[0][0])[row][2]
            cells = [rows12.cell(rows12.worst(x[0]).get(row)) for x in (p1[0], none1, soci1, p8[0], none8, soci8)]
            lines.append(f'| {row} | {b:g} | ' + ' | '.join(cells) + ' |')
        cells = [f'{rows12.shares(x[0])[2]:.2f}' for x in (p1[0], none1, soci1, p8[0], none8, soci8)]
        lines.append('| The longest work pass | 2 | ' + ' | '.join(cells) + ' |')
        cells = [f'{rows12.shares(x[0])[0]} of {rows12.shares(x[0])[1]}' for x in (p1[0], none1, soci1, p8[0], none8, soci8)]
        lines.append('| Passes over the share | - | ' + ' | '.join(cells) + ' |')
    text = '\n'.join(lines) + '\n'
    Path(out).write_text(text)
    print(text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
