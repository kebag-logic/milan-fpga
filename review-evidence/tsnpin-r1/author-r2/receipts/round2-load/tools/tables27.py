#!/usr/bin/env python3
"""Round 27 (#665, #882): the load gate's two stated-cost tables at 1x1/1if and 8x8/2if from this round's legs, and
poll_grade.py's two costs the cuts move.

usage: python3 -I tables26.py LANE COSTS_DIR

COSTS_DIR holds, per leg, <name>/costs.json (costs24.py's) and <name>/aecp.json (aecp_kinds.py's): G1 and G8, every
group of arm A and of the answering-every-port arm at this lane's head (the pin, the gate's own legs), and D1 and D8,
arm A's groups with tsn-c-stack#32 applied at the pin in a scratch build. Rules:
- the costs the round 26 ruling's cuts move (CUT: an SRP record, its retained retry, an AECP notice) are this round's
  measurement, at the pin and with the donor alike;
- every other cost of the pin's column the larger of this round's measurement and the committed table's; the polls and
  builds stay poll_grade.py's and ctrl_loop.h's, which the harness holds every pass to (a measurement over them is
  printed as a finding);
- the donor's column: a cost whose work runs the ACMP core's walk (WALK) the larger of its measurement with the donor
  and the committed donor column's; every other the larger of its measurement with the donor, the pin's column (CUT
  included: with the donor at least the pin's) and, but for CUT, the committed donor column's;
- an AECP probe is staged by no group: it is stated at a response's cost; a retained record's retry at an SRP record's;
- 32x32/2if is not re-measured: its rows stay the committed tables' (round 25's legs).
Prints both tables as Python literals, poll_grade.py's two new costs, and every finding.
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
CUT = set()   # round 27: no cut is committed, so every cost is the larger of this measurement and the committed table's
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
    point, m = POINT[n], measured('D' + n)
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
polls = {n: dict(retained=pin[POINT[n]]['record.srp'], aecp=pin[POINT[n]]['item.aecp.notice']) for n in POINT}
for name, table in (('STATED_US', pin), ('STATED_US_DONOR', donor)):
    print(f'{name} = {{')
    for point, row in table.items():
        print(f"    '{point}': {json.dumps(row)},")
    print('}')
print('poll_grade.STATED_US retained, aecp:', json.dumps(polls))
for f in findings:
    print('FINDING', f)
(costs / 'tables.json').write_text(json.dumps({'STATED_US': pin, 'STATED_US_DONOR': donor, 'poll_grade': polls,
                                               'findings': findings}, indent=1) + '\n')
# Round 27: each stated cost that differs from the committed tables'
for name, table, committed in (('STATED_US', pin, load_grade.STATED_US), ('STATED_US_DONOR', donor, load_grade.STATED_US_DONOR)):
    for point in ('1x1/1if', '8x8/2if'):
        moved = {k: (committed[point].get(k), v) for k, v in table[point].items() if committed[point].get(k) != v}
        print(f'{name} {point}:', ', '.join(f'{k} {a} -> {b}' for k, (a, b) in sorted(moved.items())) or 'unchanged')
