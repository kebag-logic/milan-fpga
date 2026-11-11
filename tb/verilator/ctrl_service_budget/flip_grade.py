# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The flip check (#665, #890): the long-window load at 8x8/2if, read at this
tree's TSN stack pin (load_grade.STATED_US, not the column graded with tsn-c-stack#32), held to the 0.70 ceiling
(#665: the 0.70 long-window ceiling, option D).

load_grade.py --check holds 1x1/1if for merge. 8x8/2if is held here instead, by a check separate from the merge gates:
the split placement's flip at 8x8/2if must pass it, and at this head it exits 1, its load over the ceiling. Its terms,
stated costs and rates are load_grade.py's own (load_grade.load), so the two checks read one table.

Each point's flip is held as well to decision D's tier bounds, the rows by every source (rows_grade.py: R4 at tier 1's
20 ms, R5 and R6 at SRP's 90 ms, the first queued notice at 20 ms and the last at 125 ms), at 1x1/1if and at 8x8/2if:
those bind each point's flip, not the merge (#665). The flip at 1x1/1if must pass --check --point 1x1/1if; 8x8/2if's
waits on #890.

usage: python3 -I flip_grade.py [--check] [--point POINT] [--selftest]
  --check     print the 8x8/2if row at the pin and the rows by every source, and exit 1 if a load is over its ceiling
              or a row over its bound (the default)
  --point     hold only that point (1x1/1if or 8x8/2if): its rows, and its load where FLIP holds one
  --selftest  plant each control and exit 1 unless every one is refused
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import load_grade  # noqa: E402
import rows_grade  # noqa: E402

ROOT = load_grade.ROOT
#: The point the flip check holds, and its ceiling.
FLIP = {'8x8/2if': 0.70}
#: The column it reads: the stated costs at this tree's pin.
COLUMN = load_grade.STATED_US


def findings(root: Path, table: dict | None = None, ceiling: dict | None = None) -> list[str]:
    """Each held point whose load at the pin is over its ceiling, whose table lacks a cost the load needs, or whose
    load counts a term without a source."""
    out = []
    for point, top in (ceiling or FLIP).items():
        try:
            terms = load_grade.load(root, point, table or COLUMN)
        except KeyError as missing:
            out.append(f'{point}: no stated cost {missing}')
            continue
        out += [f'{point}: the term {term} has no source in the term list' for term in load_grade.unsourced(terms)]
        total = sum(terms.values())
        if total > top:
            out.append(f'{point}: the load {total:.3f} at the pin is over the flip ceiling {top:.2f}')
    return out


def report(root: Path, points: tuple[str, ...] = rows_grade.POINTS) -> list[str]:
    """The held point's row at the pin: its load, its ceiling, the compute its load needs for it, its terms."""
    lines = ['| Point | Load at the pin | Flip ceiling | Compute for the ceiling | Terms by share (at the pin) |',
             '|---|---:|---:|---:|---|']
    for point, top in FLIP.items():
        if point not in points:
            continue
        terms = load_grade.load(root, point, COLUMN)
        total = sum(terms.values())
        ranked = ', '.join(f'{t} {v:.3f}' for t, v in sorted(terms.items(), key=lambda t: -t[1]))
        lines.append(f'| {point} | {total:.3f} | {top:.2f} | {max(1.0, total / top):.2f}x | {ranked} |')
    return lines


def controls(root: Path) -> list[str]:
    """Each planted defect the flip check must refuse: the planted names that escaped."""
    escaped = []
    point = next(iter(FLIP))
    total = sum(load_grade.load(root, point, COLUMN).values())
    # an over-ceiling row: the row's own load against a ceiling a thousandth under it, and over it
    if not any(f'{point}: the load' in f for f in findings(root, COLUMN, {point: total - 0.001})):
        escaped.append('an over-ceiling row')
    if any(f'{point}: the load' in f for f in findings(root, COLUMN, {point: total + 0.001})):
        escaped.append('a row within its ceiling')
    # a raised cost: the load passes the ceiling
    raised = {p: dict(v) for p, v in COLUMN.items()}
    raised[point]['record.acmp'] = 100_000
    if not any(f'{point}: the load' in f for f in findings(root, raised, {point: 10.0})):
        escaped.append('a cost raised over the ceiling')
    # a cost the load needs, missing
    dropped = {p: dict(v) for p, v in COLUMN.items()}
    dropped[point].pop('event.ACMP')
    if not any("no stated cost 'event.ACMP'" in f for f in findings(root, dropped, {point: 10.0})):
        escaped.append('a stated cost missing')
    # the held point and its ceiling (#665: the 0.70 long-window ceiling, option D), read at the pin (#665, #890:
    # item 6), never on the graded column
    if FLIP != {'8x8/2if': 0.70}:
        escaped.append('the flip ceiling not 0.70 at 8x8/2if')
    if COLUMN is not load_grade.STATED_US:
        escaped.append('the graded column read, not the pin')
    return escaped + row_controls(root)


def row_controls(root: Path) -> list[str]:
    """Each planted defect of the rows by every source the flip check must refuse: the planted names that escaped."""
    escaped = []
    for point in rows_grade.POINTS:
        inputs = rows_grade.point_inputs(root, point)
        held = rows_grade.rows(root, point, inputs=inputs)
        for row, (w, _) in held.items():
            # the row's own W against a bound a hundredth of a millisecond under it, and over it
            under = dict(rows_grade.BOUNDS, **{row: (w or 2000) - 0.01})
            over = dict(rows_grade.BOUNDS, **{row: (w or 2000) + 0.01})
            name = f'{point} {row}:'
            if not any(f.startswith(name) for f in rows_grade.findings(root, (point,), bounds=under)):
                escaped.append(f'{point} {row} over its bound')
            if w is not None and any(f.startswith(name) for f in rows_grade.findings(root, (point,), bounds=over)):
                escaped.append(f'{point} {row} within its bound')
        # each source the method counts lengthens a row's window: one left out must shorten it
        for row in rows_grade.SOLVED:
            w, terms = held[row]
            for term in (k for k, v in terms.items() if v > 0):
                if w is not None and not rows_grade.rows(root, point, dropped=term, inputs=inputs)[row][0] < w:
                    escaped.append(f'{point} {row}: the source {term} not counted')
    # a stated cost raised: the rows read the pin's column, so an SRP record's cost raised there lengthens R5
    raised = {p: dict(v) for p, v in load_grade.STATED_US.items()}
    raised['1x1/1if']['record.srp'] *= 4
    if not rows_grade.rows(root, '1x1/1if', raised)['R5'][0] > rows_grade.rows(root, '1x1/1if')['R5'][0]:
        escaped.append('a stated cost not read')
    # the rows read this tree's pin, as the flip's load does, never the column graded with tsn-c-stack#32
    pin = load_grade.stated(root, '8x8/2if', load_grade.STATED_US)
    if any(rows_grade.costs(root, '8x8/2if')[k] != pin[k] for k in pin):
        escaped.append('the rows read on the column graded with tsn-c-stack#32')
    # the queued notices are the tree's derived bounds: a derivation past its bound is refused
    path = load_grade.ROW_HEADERS[2]
    text = (root / path).read_text()
    old = '#define AECP_QUEUED_PASSES (MBX_N_IF == 1u ? 7u : 27u)'
    planted = {path: text.replace(old, '#define AECP_QUEUED_PASSES (MBX_N_IF == 1u ? 70u : 27u)')}
    if text.count(old) != 1 or not any(f.startswith('1x1/1if last:') for f in
                                       rows_grade.findings(root, ('1x1/1if',), texts=planted)):
        escaped.append('the last queued notice past its bound')
    # every source the method's docstring names is counted in every solved row, and every term it counts has one
    if rows_grade.unsourced(root):
        escaped.append('a source the rows do not count')
    # the tier bounds themselves (#665, decision D)
    if rows_grade.BOUNDS != {'R4': 20, 'R5': 90, 'R6': 90, 'first': 20, 'last': 125} or \
            rows_grade.POINTS != ('1x1/1if', '8x8/2if'):
        escaped.append('the tier bounds or the points not decision D\'s')
    return escaped


#: The planted defects controls() plants, in its order: the load's, then the rows'.
CONTROLS = ('an over-ceiling row', 'a row within its ceiling', 'a cost raised over the ceiling',
            'a stated cost missing', 'the flip ceiling not 0.70 at 8x8/2if', 'the graded column read, not the pin')


def row_control_names(root: Path) -> tuple[str, ...]:
    """The rows' controls row_controls() plants, in its order."""
    names = []
    for point in rows_grade.POINTS:
        held = rows_grade.rows(root, point)
        for row, (w, _) in held.items():
            names.append(f'{point} {row} over its bound')
            if w is not None:
                names.append(f'{point} {row} within its bound')
        for row in rows_grade.SOLVED:
            w, terms = held[row]
            names += [f'{point} {row}: the source {term} not counted' for term, v in terms.items()
                      if v > 0 and w is not None]
    return (*names, 'a stated cost not read', 'the rows read on the column graded with tsn-c-stack#32',
            'the last queued notice past its bound',
            'a source the rows do not count', "the tier bounds or the points not decision D's")


def flip_checks() -> list[tuple[str, bool, str]]:
    """The harness self-test's checks of the flip check: every planted defect refused."""
    escaped = controls(ROOT)
    return [(f'the flip check refuses {name}', name not in escaped, 'escaped' if name in escaped else 'refused')
            for name in (*CONTROLS, *row_control_names(ROOT))]


def main() -> int:
    """Print the 8x8/2if row at the pin and refuse it over its ceiling, or plant each control and refuse an escape."""
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--point', choices=rows_grade.POINTS)
    args = ap.parse_args()
    points = (args.point,) if args.point else rows_grade.POINTS
    rc = 0
    if args.selftest:
        escaped = controls(ROOT)
        for name in escaped:
            print(f'ESCAPED {name}')
        total = len(CONTROLS) + len(row_control_names(ROOT))
        print(f'flip check: {total - len(escaped)} of {total} planted controls refused')
        rc |= bool(escaped)
    if args.check or not args.selftest:
        load = {p: c for p, c in FLIP.items() if p in points}
        print('\n'.join((report(ROOT, points) + [''] if load else []) + rows_grade.report(ROOT, points)))
        found = (findings(ROOT, ceiling=load) if load else []) + rows_grade.findings(ROOT, points)
        for line in found:
            print('OVER', line)
        print('RESULT: FAIL' if found else 'RESULT: PASS')
        rc |= bool(found)
    return rc


if __name__ == '__main__':
    sys.exit(main())
