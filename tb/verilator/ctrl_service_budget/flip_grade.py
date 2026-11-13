# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The flip check (#665, #890): the long-window load at 8x8/2if, read at this
tree's TSN stack pin (load_grade.STATED_US, not the column graded with tsn-c-stack#32), held to the 0.70 ceiling
(#665: the 0.70 long-window ceiling, option D).

load_grade.py --check holds 1x1/1if for merge. 8x8/2if is held here instead, by a check separate from the merge gates:
the split placement's flip at 8x8/2if must pass it, and at this head it exits 1, its load over the ceiling. Its terms,
stated costs and rates are load_grade.py's own (load_grade.load), so the two checks read one table.

Each point's flip is held as well to decision D's tier bounds, the rows by every source (R4 at tier 1's 20 ms, R5 and
R6 at SRP's 90 ms, the first queued notice at 20 ms and the last at 125 ms), at 1x1/1if and at 8x8/2if: those bind
each point's flip, not the merge (#665). The rows are the built design's by default (rows_tiers.py, rows_tiers.BUILT:
THE TIERS as ctrl_loop.h builds them, #894), or THE DRAIN before them (rows_grade.py, `--design as-built`), kept for
comparison. The built design's rows also hold each tier-1 channel's last record of its burst (#894's ruling of
2026-11-13, item 2: AECP's with its largest legal notice at tier 1's 20 ms, ACMP's, ADP's and MAAP's at 30 ms by the
owner's decision of 2026-11-13, option A, FR_NFR.md 3.4.1)
and THE TRANSMIT's MRPDU at the MRP timer budget's bound (item 1: CTRL_LOOP_TX_BOUND_MS, 40 ms), by its stated notice
and with every AECP notice the largest legal one (txL, #894's slice ruling of 2026-11-13), and the check fails
when a channel the loop serves has no row (rows_tiers.unrowed, the channels read from the firmware's bindings) or
when ctrl_loop.h states THE TRANSMIT's figure under its row. The flip at 1x1/1if must pass --check --point 1x1/1if;
8x8/2if's rows by every source are reported, not held (#894, the owner's decision of 2026-11-12, owed to #872).

usage: python3 -I flip_grade.py [--check] [--point POINT] [--design DESIGN] [--selftest]
  --check     print the 8x8/2if row at the pin and the rows by every source, and exit 1 if a load is over its ceiling
              or a row over its bound (the default)
  --point     hold only that point (1x1/1if or 8x8/2if): its rows, and its load where FLIP holds one
  --design    built (the default: the tier model of the built design) or as-built (rows_grade.py)
  --selftest  plant each control and exit 1 unless every one is refused
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import load_grade  # noqa: E402
import rows_grade  # noqa: E402
import paced_rows  # noqa: E402
import rows_tiers  # noqa: E402

ROOT = load_grade.ROOT
#: The point the flip check holds, and its ceiling.
FLIP = {'8x8/2if': 0.70}
#: The column it reads: the stated costs at this tree's pin.
COLUMN = load_grade.STATED_US
#: The designs the rows are held by: the built design's tier model first, the default; THE DRAIN before the tiers.
DESIGNS = ('built', 'as-built')


def row_findings(root: Path, points: tuple[str, ...], design: str = DESIGNS[0]) -> list[str]:
    """Each row over its bound by every source at each point, by the design's model."""
    if design == 'as-built':
        return rows_grade.findings(root, points)
    return rows_tiers.findings(root, rows_tiers.BUILT, points) + rows_tiers.unrowed(root, rows_tiers.BUILT, points) + \
        rows_tiers.tx_statements(root, points)


def row_report(root: Path, points: tuple[str, ...], design: str = DESIGNS[0]) -> list[str]:
    """Each row at each point by the design's model, with its largest terms."""
    if design == 'as-built':
        return rows_grade.report(root, points)
    return rows_tiers.report(root, rows_tiers.BUILT, points)


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
    return escaped + row_controls(root) + built_controls(root)


def built_controls(root: Path) -> list[str]:
    """Each planted defect of the built design's rows the flip check must refuse: each row's bound a hundredth under its
    W and over it, each source left out, which must shorten W, the model breaking its own rules, and the default design
    not the built one."""
    escaped = []
    model = rows_tiers.BUILT
    for point in rows_grade.POINTS:
        i = rows_tiers.point_inputs(root, point)
        for row, (w, terms) in rows_tiers.rows(root, point, model, i).items():
            name = f'{point} {row}:'
            under = dict(rows_tiers.bounds_at(i), **{row: (w or 2000) - 0.01})
            over = dict(rows_tiers.bounds_at(i), **{row: (w or 2000) + 0.01})
            if not any(f.startswith(name) for f in rows_tiers.findings(root, model, (point,), under)):
                escaped.append(f'built {point} {row} over its bound')
            if w is not None and any(f.startswith(name) for f in rows_tiers.findings(root, model, (point,), over)):
                escaped.append(f'built {point} {row} within its bound')
            for term in (k for k, v in terms.items() if v > 0 and w is not None):
                if not rows_tiers.solve(row, i, model, dropped=term)[0] < w:
                    escaped.append(f'built {point} {row}: the source {term} not counted')
    if rows_tiers.broken(root, model):
        escaped.append('the built design breaks its own rules')
    if DESIGNS[0] != 'built':
        escaped.append('the flip check not held by the built design')
    return escaped + channel_controls(root)


#: The channel rows' and THE TRANSMIT's planted defects, in channel_controls' order.
CHANNEL_CONTROLS = ('a channel the loop serves without its rows', "THE TRANSMIT's stated figure under its row",
                    "a channel row's or THE TRANSMIT's bound not the ruling's",
                    "the owed-notice slot under the largest legal notice")


def channel_controls(root: Path) -> list[str]:
    """Each planted defect of the rows the ruling of 2026-11-13 adds that the flip check must refuse: a served
    channel's rows dropped, ctrl_loop.h stating THE TRANSMIT's figure under its row, the added bounds moved, and
    aecp.h's slot under the largest legal notice, which R4L's notices must then wait in the response buffer for."""
    from unittest import mock
    escaped = []
    one = ('1x1/1if',)
    with mock.patch.dict(rows_tiers.CHANNEL_ROWS, {'acmp': ()}):
        if not any('the channel acmp the loop serves has no row' in f for f in row_findings(root, one)):
            escaped.append(CHANNEL_CONTROLS[0])
    loop = 'sw/firmware/ctrl/loop/ctrl_loop.h'
    text = (root / loop).read_text()
    figure = '#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 30u : 98u)'
    under = {loop: text.replace(figure, '#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 29u : 98u)')}
    with mock.patch.object(rows_tiers, 'tx_statements', lambda r, p, texts=None, f=rows_tiers.tx_statements:
                           f(r, p, under)):
        if text.count(figure) != 1 or not any('CTRL_LOOP_TX_MS states 29 ms' in f for f in row_findings(root, one)):
            escaped.append(CHANNEL_CONTROLS[1])
    if rows_tiers.CHANNEL_BOUNDS != {'R4L': 20, 'ACMP': 30, 'ADP': 30, 'MAAP': 30} or rows_tiers.TX_BUDGET_MS != 40 or \
            paced_rows.PACED_BOUNDS != {'R4L': 240}:
        escaped.append(CHANNEL_CONTROLS[2])
    aecp = 'sw/firmware/ctrl/aecp/aecp.h'
    text, slot = (root / aecp).read_text(), '#define AECP_OWED_BYTES 552u'
    narrow = {aecp: text.replace(slot, '#define AECP_OWED_BYTES 548u')}

    def unpaced(texts: dict[str, str] | None) -> float:
        """R4L at 1x1/1if with no pace, its notices waiting where the slot puts them (THE PACE makes R4L's burst one
        command at a time, which no slot slows)."""
        i = rows_tiers.point_inputs(root, '1x1/1if', texts)._replace(pace_ms=0)
        return rows_tiers.solve('R4L', i, rows_tiers.BUILT)[0] or 2000.0
    if text.count(slot) != 1 or not unpaced(narrow) > unpaced(None):
        escaped.append(CHANNEL_CONTROLS[3])
    return escaped


def built_control_names(root: Path) -> tuple[str, ...]:
    """The built design's controls built_controls() plants, in its order."""
    names = []
    for point in rows_grade.POINTS:
        for row, (w, terms) in rows_tiers.rows(root, point, rows_tiers.BUILT).items():
            names.append(f'built {point} {row} over its bound')
            if w is not None:
                names.append(f'built {point} {row} within its bound')
                names += [f'built {point} {row}: the source {term} not counted' for term, v in terms.items() if v > 0]
    return (*names, 'the built design breaks its own rules', 'the flip check not held by the built design',
            *CHANNEL_CONTROLS)


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
    # the queued notices are the tree's stated bounds: a statement past its bound is refused
    path = load_grade.ROW_HEADERS[2]
    text = (root / path).read_text()
    old = '#define AECP_QUEUED_MS (MBX_N_IF == 1u ? 125u : 62u)'
    planted = {path: text.replace(old, '#define AECP_QUEUED_MS (MBX_N_IF == 1u ? 1250u : 62u)')}
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
    return escaped + rule_controls(root)


def planted_rule(name: str, value: object) -> object:
    """Set rows_grade's `name` to a planted `value`, returning what it was."""
    held = getattr(rows_grade, name)
    setattr(rows_grade, name, value)
    return held


def rule_controls(root: Path) -> list[str]:
    """Each earlier or wrong arrival rule planted in the rows, which the check must refuse by name and which must move
    1x1/1if's R4 the way the defect does: the planted names that escaped."""
    escaped = []
    # the head's own rows hold every rule: no rule finding at this tree
    if rows_grade.rule_findings(root):
        escaped.append('the arrival rules not held at this head')
    held = rows_grade.rows(root, '1x1/1if')['R4'][0]
    burst = rows_grade.contract(root)[0]['aecp'][0]
    # the earlier rules (#665): a retained record retried once a pass, and SRP's arrivals counted over the window
    # less AECP's whole burst; the first lengthens R4, the second shortens it; and SRP's arrivals counted over the
    # window less two records of AECP, an error of one record, which moves no row at this head (None) and which only a
    # window off SRP's refill grid sees (rows_grade.rule_windows)
    for name, attr, value, longer, words in (
            ('the retained retry counted once a pass', 'retained_retries', lambda w, passes, tick: passes, True,
             "retained retries in"),
            ("SRP's arrivals cut by AECP's whole burst", 'srp_window',
             lambda w, inputs: max(0.0, w - burst * inputs.c['record.aecp'] / 1000), False, 'SRP records ahead'),
            ("SRP's arrivals cut by two records of AECP", 'srp_window',
             lambda w, inputs: max(0.0, w - 2 * inputs.c['record.aecp'] / 1000), None, 'SRP records ahead')):
        saved = planted_rule(attr, value)
        try:
            w = rows_grade.rows(root, '1x1/1if')['R4'][0]
            refused = any(words in f for f in rows_grade.rule_findings(root, ('1x1/1if',)))
        finally:
            planted_rule(attr, saved)
        moved = longer is None or (w is not None and held is not None and (w > held if longer else w < held))
        if not refused or not moved:
            escaped.append(name)
    # a retained record's retry counted in SRP's own rows, which are solved with no record refused for storage
    saved = planted_rule('RETAINED_ROWS', ('R4', 'R5', 'R6'))
    try:
        refused = any('retry counted in an SRP row' in f for f in rows_grade.rule_findings(root, ('1x1/1if',)))
    finally:
        planted_rule('RETAINED_ROWS', saved)
    if not refused:
        escaped.append('a retained retry in an SRP row')
    # the tree's retry rule itself: a poll that retries every pass a change allows states no centisecond's rule
    path = load_grade.RETRY_RULE["a centisecond's retry"][0]
    text = (root / path).read_text()
    old = '                m->retry_spent = true;\n'
    if text.count(old) != 1 or not any("rule not the tree's" in f for f in rows_grade.rule_findings(
            root, ('1x1/1if',), texts={path: text.replace(old, '')})):
        escaped.append('a retry rule the tree does not state')
    # an event type of the contract neither counted nor excluded: one dropped from the excluded list
    saved = planted_rule('EXCLUDED', rows_grade.EXCLUDED[1:])
    try:
        refused = any('neither counted nor excluded' in f for f in rows_grade.rule_findings(root, ('1x1/1if',)))
    finally:
        planted_rule('EXCLUDED', saved)
    if not refused:
        escaped.append('a datapath event neither counted nor excluded')
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
            'a source the rows do not count', "the tier bounds or the points not decision D's", *RULE_CONTROLS)


#: The arrival rules' controls rule_controls() plants, in its order.
RULE_CONTROLS = ('the arrival rules not held at this head', 'the retained retry counted once a pass',
                 "SRP's arrivals cut by AECP's whole burst", "SRP's arrivals cut by two records of AECP",
                 'a retained retry in an SRP row', 'a retry rule the tree does not state',
                 'a datapath event neither counted nor excluded')


def flip_checks() -> list[tuple[str, bool, str]]:
    """The harness self-test's checks of the flip check: every planted defect refused."""
    escaped = controls(ROOT)
    return [(f'the flip check refuses {name}', name not in escaped, 'escaped' if name in escaped else 'refused')
            for name in (*CONTROLS, *row_control_names(ROOT), *built_control_names(ROOT))]


def main() -> int:
    """Print the 8x8/2if row at the pin and refuse it over its ceiling, or plant each control and refuse an escape."""
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--point', choices=rows_grade.POINTS)
    ap.add_argument('--design', choices=DESIGNS, default=DESIGNS[0])
    args = ap.parse_args()
    points = (args.point,) if args.point else rows_grade.POINTS
    rc = 0
    if args.selftest:
        escaped = controls(ROOT)
        for name in escaped:
            print(f'ESCAPED {name}')
        total = len(CONTROLS) + len(row_control_names(ROOT)) + len(built_control_names(ROOT))
        print(f'flip check: {total - len(escaped)} of {total} planted controls refused')
        rc |= bool(escaped)
    if args.check or not args.selftest:
        load = {p: c for p, c in FLIP.items() if p in points}
        print('\n'.join((report(ROOT, points) + [''] if load else []) + row_report(ROOT, points, args.design)))
        found = (findings(ROOT, ceiling=load) if load else []) + row_findings(ROOT, points, args.design) + \
            rows_grade.rule_findings(ROOT, points)
        for line in found:
            print('OVER', line)
        print('RESULT: FAIL' if found else 'RESULT: PASS')
        rc |= bool(found)
    return rc


if __name__ == '__main__':
    sys.exit(main())
