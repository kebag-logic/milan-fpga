#!/usr/bin/env python3
"""R713-1-F1's verification: every row of the README's two "Paths that still miss T_svc" tables
against the archived head-regrade tables of P1-none, P1-64x1, P8-none and P8-64x1.

A path whose worst instance was never answered or never released must read
"at least X, **never answered**" (or "never released") in its ms column and,
for the cached arm, "at least N, **...**" in its cycles column; every other
cell must start with the measured figure, unlabelled. Usage: check_miss_cells.py README ARMS_DIR
"""
import re
import sys
from pathlib import Path

readme = Path(sys.argv[1]).read_text()
arms = Path(sys.argv[2])
UNBOUNDED = {'NEVER ANSWERED': 'never answered', 'STARVED: never released': 'never released'}


def arm(name: str) -> tuple[dict, dict]:
    """The arm's path table, (row, interface) -> (probe, ms text, verdict), and its probe cycles."""
    paths, cycles = {}, {}
    for line in (arms / name / 'table.md').read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        m = len(cells) == 8 and re.fullmatch(r'`([^`]+)` \(([^)]+)\)', cells[2])
        if m and cells[1].isdigit():
            paths[(cells[0], int(cells[1]))] = (m.group(1), cells[3], cells[4])
        elif len(cells) == 10 and cells[1].startswith('`') and cells[2].replace(',', '').isdigit():
            cycles[cells[1].strip('`')] = cells[2]
    return paths, cycles


def matches(cell: str, ms_text: str, verdict: str) -> bool:
    """The README cell gives this path's figure, rounded to 0.01 ms from the table's 0.001 ms, with its
    label: "at least X, **never answered**" or "never released" where the path is unbounded."""
    figure = float(ms_text.removeprefix('at least ').split()[0])
    m = re.match(r'(at least )?(\d+\.\d\d)(, \*\*(never answered|never released)\*\*)?', cell)
    label = UNBOUNDED.get(verdict)
    return bool(m) and abs(float(m.group(2)) - figure) <= 0.0055 and bool(m.group(1)) == bool(label) \
        and m.group(4) == label


bad = rows = 0
for point in ('1x1', '8x8'):
    n = point[0]
    none, _ = arm(f'P{n}-none')
    cached, cycles = arm(f'P{n}-64x1')
    start = readme.index(f'| {point}: path missing T_svc with the 4 KiB cache |')
    for line in readme[start:].splitlines()[2:]:
        if not line.startswith('|'):
            break
        row, iface, none_cell, cached_cell, cycles_cell = (c.strip() for c in line.strip('|').split(' | '))
        key = (row, int(iface))
        rows += 1
        probe, ms_text, verdict = cached[key]
        want_cycles = cycles[probe]
        if verdict in UNBOUNDED:
            want_cycles = f'at least {want_cycles}, **{UNBOUNDED[verdict]}**'
        ok = matches(none_cell, *none[key][1:]) and matches(cached_cell, ms_text, verdict) \
            and cycles_cell == want_cycles
        unbounded = none[key][2] in UNBOUNDED or verdict in UNBOUNDED
        bad += not ok
        if unbounded or not ok:
            print(f"{'ok ' if ok else 'BAD'} {point} {row} if{iface}: none {none[key][1]} {none[key][2]} -> "
                  f"'{none_cell}'; 4 KiB {ms_text} {verdict} -> '{cached_cell}'; cycles -> '{cycles_cell}'")
print(f'{rows} rows checked, {bad} mismatches')
raise SystemExit(1 if bad else 0)
