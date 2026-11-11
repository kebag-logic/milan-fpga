# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The flip check (#665, issuecomment-6788828284, items 4 and 6): the long-window load at 8x8/2if, read at this
tree's TSN stack pin (load_grade.STATED_US, not the column graded with tsn-c-stack#32), held to the 0.70 ceiling
(#665 issuecomment-6751196896, item 4).

load_grade.py --check holds 1x1/1if for merge. 8x8/2if is held here instead, by a check separate from the merge gates:
the split placement's flip at 8x8/2if must pass it, and at this head it exits 1, its load over the ceiling. Its terms,
stated costs and rates are load_grade.py's own (load_grade.load), so the two checks read one table.

usage: python3 -I flip_grade.py [--check] [--selftest]
  --check     print the 8x8/2if row at the pin and exit 1 if its load is over the ceiling (the default)
  --selftest  plant each control and exit 1 unless every one is refused
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import load_grade  # noqa: E402

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


def report(root: Path) -> list[str]:
    """The held point's row at the pin: its load, its ceiling, the compute its load needs for it, its terms."""
    lines = ['| Point | Load at the pin | Flip ceiling | Compute for the ceiling | Terms by share (at the pin) |',
             '|---|---:|---:|---:|---|']
    for point, top in FLIP.items():
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
    # the held point and its ceiling (#665 issuecomment-6751196896, item 4), read at the pin (issuecomment-6788828284,
    # item 6), never on the graded column
    if FLIP != {'8x8/2if': 0.70}:
        escaped.append('the flip ceiling not 0.70 at 8x8/2if')
    if COLUMN is not load_grade.STATED_US:
        escaped.append('the graded column read, not the pin')
    return escaped


#: The planted defects controls() plants, in its order.
CONTROLS = ('an over-ceiling row', 'a row within its ceiling', 'a cost raised over the ceiling',
            'a stated cost missing', 'the flip ceiling not 0.70 at 8x8/2if', 'the graded column read, not the pin')


def flip_checks() -> list[tuple[str, bool, str]]:
    """The harness self-test's checks of the flip check: every planted defect refused."""
    escaped = controls(ROOT)
    return [(f'the flip check refuses {name}', name not in escaped, 'escaped' if name in escaped else 'refused')
            for name in CONTROLS]


def main() -> int:
    """Print the 8x8/2if row at the pin and refuse it over its ceiling, or plant each control and refuse an escape."""
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    rc = 0
    if args.selftest:
        escaped = controls(ROOT)
        for name in escaped:
            print(f'ESCAPED {name}')
        print(f'flip check: {len(CONTROLS) - len(escaped)} of {len(CONTROLS)} planted controls refused')
        rc |= bool(escaped)
    if args.check or not args.selftest:
        print('\n'.join(report(ROOT)))
        found = findings(ROOT)
        for line in found:
            print('OVER', line)
        print('RESULT: FAIL' if found else 'RESULT: PASS')
        rc |= bool(found)
    return rc


if __name__ == '__main__':
    sys.exit(main())
