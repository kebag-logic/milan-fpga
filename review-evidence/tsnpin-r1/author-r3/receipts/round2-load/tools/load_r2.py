#!/usr/bin/env python3
"""load_r2.py TREE COSTS_DIR: the long-window load with tsn-c-stack 715589c and the ACMP adapter's redelivery (#665,
the [A10] ruling on the round-2 STOP), from S2b's legs X1 and X8 on its head with this lane's firmware delta.

The column is built by S2b round 27's rule for its donor column (tables27.py, donor_column): a cost whose work runs the
ACMP core's walk (load_grade.WALK) the larger of this measurement and the committed STATED_US_DONOR; every other cost
the larger of this measurement, the committed pin column (load_grade.stated) and the committed donor column; a retained
retry at an SRP record's cost, an owed MRPDU at least a build of one's, THE STEP's pass the header's, an AECP probe at
a response's. 1x1/1if is held to 0.70 (load_grade.CEILING), 8x8/2if to the owner's 0.75 (#890). Prints both loads,
each against the committed columns, and every cost that moved.
"""
import json
import math
import sys
from pathlib import Path

tree, costs = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import load_grade  # noqa: E402
import poll_grade  # noqa: E402

stated = lambda cycles: int(math.ceil(cycles * 1.05 / 100 / 5 - 1e-9) * 5)
MEASURED = ['record.srp', 'record.aecp', 'record.acmp', 'record.adp', 'record.maap', 'event.ADP', 'event.ACMP',
            'event.MAAP', 'event.AECP', 'event.TICK', 'event.GM', 'centisecond', 'events_none']
POLLS = ['base', 'item.reclaim', 'item.retained', 'item.mrpdu', 'item.acmp', 'item.walk']
BUILDS = ['build', 'build_one', 'step']
KINDS = ['item.aecp.notice', 'item.aecp.response']
POINT = {'1': '1x1/1if', '8': '8x8/2if'}
CEIL = {'1x1/1if': 0.70, '8x8/2if': 0.75}
findings = []


def measured(name):
    c = json.loads((costs / name / 'costs.json').read_text())
    point = next(k for k in c if not k.startswith('_'))
    out = dict(c[point])
    out['_cycles'] = c['_most_cycles']
    k = json.loads((costs / name / 'aecp.json').read_text())
    for kind in ('notice', 'response'):
        if kind in k:
            out[f'item.aecp.{kind}'] = stated(k[kind]['most_cycles'])
    if 'probe' in k:
        findings.append(f'{name}: a probe was staged, {k["probe"]}')
    return out


def column(n):
    point, m = POINT[n], measured('X' + n)
    full = dict(load_grade.stated(tree, point, {point: load_grade.STATED_US[point]}))
    polls = poll_grade.stated_us(1 if n == '1' else 2)
    for key in POLLS:
        short = 'base' if key == 'base' else key[5:]
        if short != 'retained' and m['_cycles'].get(key, 0) > 100 * polls[short]:
            findings.append(f'{point}: measured {key} {m["_cycles"][key]} cycles over poll_grade.py\'s {polls[short]} us')
    out = {}
    for key in MEASURED + KINDS + POLLS + BUILDS:
        if key in ('item.retained', 'item.mrpdu', 'step'):
            continue
        committed = load_grade.STATED_US_DONOR[point].get(key)
        pool = (m.get(key), committed) if key in load_grade.WALK else (m.get(key), full.get(key), committed)
        out[key] = max(v for v in pool if v)
    out['item.retained'] = out['record.srp']
    out['item.mrpdu'] = max(out['build_one'], full['item.mrpdu'])
    out['step'] = full['step']
    out['item.aecp.probe'] = out['item.aecp.response']
    return point, out, m


rows, table = [], {}
for n in POINT:
    point, col, m = column(n)
    table[point] = col
    new = load_grade.load(tree, point, {point: col})
    graded = load_grade.load(tree, point, load_grade.STATED_US_DONOR)
    pin = load_grade.load(tree, point, load_grade.STATED_US)
    total = sum(new.values())
    ranked = ', '.join(f'{t} {v:.3f}' for t, v in sorted(new.items(), key=lambda t: -t[1])[:6])
    rows.append(f'| {point} | {sum(pin.values()):.3f} | {sum(graded.values()):.3f} | **{total:.3f}** | {CEIL[point]:.2f} | '
                f'{"within" if total <= CEIL[point] else "OVER"} | {ranked} |')
    moved = {k: (load_grade.STATED_US_DONOR[point].get(k), v) for k, v in col.items()
             if load_grade.STATED_US_DONOR[point].get(k) != v}
    rows.append(f'|  | costs moved against the committed donor column: '
                f'{", ".join(f"{k} {a} -> {b}" for k, (a, b) in sorted(moved.items())) or "none"} | | | | | |')
print('| Point | Load, committed pin column (70936b77) | Load, committed donor column (tsn-c-stack#32) | '
      'Load, 715589c with the redelivery (this measurement) | Ceiling | Verdict | Largest terms |')
print('|---|---:|---:|---:|---:|---|---|')
print('\n'.join(rows))
for f in findings:
    print('FINDING', f)
(costs / 'load_r2.json').write_text(json.dumps({'column': table, 'findings': findings}, indent=1) + '\n')
sys.exit(1 if any(sum(load_grade.load(tree, p, {p: table[p]}).values()) > CEIL[p] for p in table) else 0)
