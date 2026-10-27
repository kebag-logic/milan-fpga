#!/usr/bin/env python3
"""Compare the README's two 'path missing T_svc with the 4 KiB cache' tables with the archived regrade
tables: every row's worst ms (none and 4 KiB), its unbounded label and its CPU-cycles cell.
Usage: check_miss_rows.py <README.md> <arms dir with P1-none, P1-64x1, P8-none, P8-64x1/table.md>"""
import re, sys
from pathlib import Path
readme, arms = Path(sys.argv[1]).read_text().splitlines(), Path(sys.argv[2])

def summary(arm):
    """Path summary rows: (path, interface) -> [(ms text, verdict)], one per group that measures it."""
    out = {}
    for l in (arms / arm / 'table.md').read_text().splitlines():
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) >= 5 and re.fullmatch(r'\d+', c[1] or 'x') and '`' in c[2]:
            out.setdefault((c[0], c[1]), []).append((c[3], c[4]))
    return out

def worst_cycles(arm, path):
    """Largest cpu-cycles figure among the arm's instance rows for the path."""
    vals = []
    for l in (arms / arm / 'table.md').read_text().splitlines():
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) >= 6 and c[0] == path and '`' in c[1] and re.fullmatch(r'[\d,]+', c[2]):
            vals.append(int(c[2].replace(',', '')))
    return vals

bad = rows = 0
for point in ('1x1', '8x8'):
    none, cached = summary(f'P{point[0]}-none'), summary(f'P{point[0]}-64x1')
    inside = False
    for l in readme:
        if l.startswith(f'| {point}: path missing T_svc with the 4 KiB cache'):
            inside = True; continue
        if inside and not l.startswith('|'):
            break
        if not inside or l.startswith('|---'):
            continue
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        path, iface, ms_none, ms_c, cyc = c[0], c[1], c[2], c[3], c[4]
        rows += 1
        problems = []
        for label, cell, table in (('none', ms_none, none), ('4KiB', ms_c, cached)):
            got = table.get((path, iface))
            if not got:
                problems.append(f'{label}: no archived row'); continue
            num0 = float(re.search(r'[\d.]+', cell.replace(',', '')).group())
            ms, verdict = min(got, key=lambda g: abs(float(g[0].replace('at least', '').strip().split()[0]) - num0))
            unb = ms.startswith('at least')
            want = float(ms.replace('at least', '').strip().split()[0])
            num = float(re.search(r'[\d.]+', cell.replace(',', '')).group())
            if abs(num - want) > 0.006: problems.append(f'{label}: {num} vs archived {want}')
            if unb != cell.startswith('at least'): problems.append(f'{label}: lower-bound label {cell!r} vs {ms!r} {verdict}')
            if unb:
                word = 'never answered' if 'ANSWERED' in verdict else 'never released'
                if word not in cell: problems.append(f'{label}: {cell!r} lacks {word!r} ({verdict})')
        if ms_c.startswith('at least') != cyc.startswith('at least'):
            problems.append(f'cycles cell {cyc!r} not labelled like {ms_c!r}')
        print(f"{'BAD' if problems else 'OK '} {point} {path} if{iface}: {'; '.join(problems)}")
        bad += bool(problems)
print(f'{rows} rows, {bad} with problems')
sys.exit(1 if bad or not rows else 0)
