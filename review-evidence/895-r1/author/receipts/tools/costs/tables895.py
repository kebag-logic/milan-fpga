#!/usr/bin/env python3
"""#895 (from #665 round 28's tables28.py): the load gate's two stated-cost tables at 1x1/1if and 8x8/2if from this
lane's legs, at the pin 715589c, which carries tsn-c-stack#32.

usage: python3 -I tables895.py LANE COSTS_DIR

COSTS_DIR holds G1 and G8, each <name>/costs.json (costs24.py's) and <name>/aecp.json (aecp_kinds.py's), over every
leg of the point at the lane's head: arm A's groups, the answering-every-port arm's, the valid-destinations arm's (the
Talker declarations and withdrawals) and arm B's aecp group. Rules (SPLIT_CONTROL_MEMORY section 13's, unchanged):
- the pin's column: every measured cost the larger of this measurement and the committed table's; the polls and builds
  stay poll_grade.py's and ctrl_loop.h's, which the harness holds every pass to (a measurement over them is printed as
  a finding, and a run fails it as STATED);
- the column with tsn-c-stack#32: the pin carries it, so it is measured on the same legs: a cost whose work runs the
  ACMP core's walk (WALK) the larger of the measurement and the committed donor column's; every other the larger of
  the measurement, the pin's column and the committed donor column's;
- an AECP probe is staged by no group: it is stated at a response's cost; a retained record's retry at an SRP record's;
- 32x32/2if is not re-measured: its rows stay the committed tables'.
Prints both tables as Python literals and every finding; poll_grade.py's costs are not moved.
"""
import json
import math
import sys
from pathlib import Path

lane, costs = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(lane / 'tb/verilator/ctrl_service_budget'))
import load_grade  # noqa: E402
import poll_grade  # noqa: E402

stated = lambda cycles: int(math.ceil(cycles * 1.05 / 100 / 5 - 1e-9) * 5)
WALK = {'record.acmp', 'record.adp', 'event.ACMP', 'item.acmp', 'base'}
CUT = set()   # round 28: no cut, so every cost is the larger of this measurement and the committed table's
MEASURED = ['record.srp', 'record.aecp', 'record.acmp', 'record.adp', 'record.maap', 'event.ADP', 'event.ACMP',
            'event.MAAP', 'event.AECP', 'event.TICK', 'event.GM', 'centisecond', 'events_none']
POLLS = ['base', 'item.reclaim', 'item.retained', 'item.mrpdu', 'item.acmp', 'item.walk']
BUILDS = ['build', 'build_one', 'step']
KINDS = ['item.aecp.notice', 'item.aecp.response', 'item.aecp.probe']
POINT = {'1': '1x1/1if', '8': '8x8/2if'}
findings = []


def measured(name):
    c = json.loads((costs / name / 'costs.json').read_text())
    point = next(k for k in c if not k.startswith('_'))
    out = dict(c[point])
    out['_cycles'] = c['_most_cycles']
    k = json.loads((costs / name / 'aecp.json').read_text())
    if 'notice' in k:
        out['item.aecp.notice'] = stated(k['notice']['most_cycles'])
    if 'response' in k:
        out['item.aecp.response'] = stated(k['response']['most_cycles'])
    if 'probe' in k:
        findings.append(f'{name}: a probe was staged, {k["probe"]}')
    out['_aecp'] = k
    return out


def pin_column(n):
    point, m = POINT[n], measured('G' + n)
    old = load_grade.STATED_US[point]
    out = {}
    for key in MEASURED + KINDS[:2]:
        if key in CUT:
            out[key] = m[key]
        else:
            out[key] = max(v for v in (m.get(key), old.get(key)) if v)
    out['item.retained'] = out['record.srp']
    polls = poll_grade.stated_us(1 if n == '1' else 2)
    for key in POLLS:
        short = 'base' if key == 'base' else key[5:]
        if short == 'retained':
            continue
        if m['_cycles'].get(key, 0) > 100 * polls[short]:
            findings.append(f'{point}: measured {key} {m["_cycles"][key]} cycles over poll_grade.py\'s {polls[short]} us')
    out['item.aecp.probe'] = out['item.aecp.response']
    return out


def donor_column(n, pin):
    point = POINT[n]
    m = measured('G' + n)
    full = dict(load_grade.stated(lane, point, {point: pin}))
    out = {}
    for key in MEASURED + KINDS[:2] + POLLS + BUILDS:
        if key in ('item.retained', 'item.mrpdu', 'step'):
            continue
        committed = None if key in CUT else load_grade.STATED_US_DONOR[point].get(key)
        if key in WALK:
            out[key] = max(v for v in (m.get(key), committed) if v)
        else:
            out[key] = max(v for v in (m.get(key), full.get(key), committed) if v)
    out['item.retained'] = out['record.srp']
    out['item.mrpdu'] = max(out['build_one'], full['item.mrpdu'])
    out['step'] = full['step']
    out['item.aecp.probe'] = out['item.aecp.response']
    return out


pin = {POINT[n]: pin_column(n) for n in POINT}
donor = {POINT[n]: donor_column(n, pin[POINT[n]]) for n in POINT}
pin['32x32/2if'] = load_grade.STATED_US['32x32/2if']
donor['32x32/2if'] = load_grade.STATED_US_DONOR['32x32/2if']
polls = {}
for name, table in (('STATED_US', pin), ('STATED_US_DONOR', donor)):
    print(f'{name} = {{')
    for point, row in table.items():
        print(f"    '{point}': {json.dumps(row)},")
    print('}')
for f in findings:
    print('FINDING', f)
(costs / 'tables.json').write_text(json.dumps({'STATED_US': pin, 'STATED_US_DONOR': donor, 'poll_grade': polls,
                                               'findings': findings}, indent=1) + '\n')
# each stated cost that differs from the committed tables'
for name, table, committed in (('STATED_US', pin, load_grade.STATED_US), ('STATED_US_DONOR', donor, load_grade.STATED_US_DONOR)):
    for point in ('1x1/1if', '8x8/2if'):
        moved = {k: (committed[point].get(k), v) for k, v in table[point].items() if committed[point].get(k) != v}
        print(f'{name} {point}:', ', '.join(f'{k} {a} -> {b}' for k, (a, b) in sorted(moved.items())) or 'unchanged')
