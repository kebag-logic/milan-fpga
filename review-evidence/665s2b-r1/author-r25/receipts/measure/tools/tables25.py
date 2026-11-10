#!/usr/bin/env python3
"""Round 25 (#665): the load gate's two stated-cost tables from this round's traced legs (costs25.sh outputs).

usage: python3 -I tables25.py LANE COSTS_DIR

COSTS_DIR holds, per leg set, <name>/costs.json (costs24.py's) and <name>/aecp.json (aecp_kinds.py's): C1, C8, C32 at
this lane's head (the pin), D1, D8, D32 with tsn-c-stack#32 applied at the pin in a scratch build. Rules:
- the pin's column at 1x1/1if and 8x8/2if: each record, event, centisecond and AECP kind the larger of this round's
  measurement and the committed table's (round 24's, at its image); the polls and builds stay poll_grade.py's and
  ctrl_loop.h's, which the harness holds every pass to (a measurement over them is printed as a finding);
- the pin's column at 32x32/2if: each cost the larger of this round's measurement and the committed table's;
- the donor's column: a cost whose work runs the ACMP core's completion walk (WALK) its measurement with the donor;
  every other cost the larger of its measurement with the donor and the pin's column;
- an AECP probe is staged by no group: it is stated at a response's cost; a retained record's retry at an SRP
  record's, an owed MRPDU at a build of one's, THE STEP at ctrl_loop.h's two-interface pass at 32x32/2if.
Prints both tables as Python literals and every finding.
"""
import json
import math
import re
import sys
from pathlib import Path

lane, costs = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(lane / 'tb/verilator/ctrl_service_budget'))
import load_grade  # noqa: E402
import poll_grade  # noqa: E402

stated = lambda cycles: int(math.ceil(cycles * 1.05 / 100 / 5 - 1e-9) * 5)
WALK = {'record.acmp', 'record.adp', 'event.ACMP', 'item.acmp', 'base'}
MEASURED = ['record.srp', 'record.aecp', 'record.acmp', 'record.adp', 'record.maap', 'event.ADP', 'event.ACMP',
            'event.MAAP', 'event.AECP', 'event.TICK', 'event.GM', 'centisecond', 'events_none']
POLLS = ['base', 'item.reclaim', 'item.retained', 'item.mrpdu', 'item.acmp', 'item.walk']
BUILDS = ['build', 'build_one', 'step']
KINDS = ['item.aecp.notice', 'item.aecp.response', 'item.aecp.probe']
POINT = {'1': '1x1/1if', '8': '8x8/2if', '32': '32x32/2if'}
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
    return out


def pin_column(n):
    point, m = POINT[n], measured('C' + n)
    old = load_grade.STATED_US[point]
    out = {}
    keys = MEASURED + KINDS[:2] + (POLLS + BUILDS if n == '32' else [])
    for key in keys:
        if key in ('item.retained', 'item.mrpdu', 'step') and n == '32':
            continue
        vals = [v for v in (m.get(key), old.get(key)) if v]
        out[key] = max(vals)
    if n == '32':
        out['item.retained'] = max(out['record.srp'], old['item.retained'])
        out['item.mrpdu'] = max(out['build_one'], old['item.mrpdu'])
        out['step'] = old['step']
    else:
        polls = poll_grade.stated_us(1 if n == '1' else 2)
        for key in POLLS:
            short = 'base' if key == 'base' else key[5:]
            if m['_cycles'].get(key, 0) > 100 * polls[short]:
                findings.append(f'{point}: measured {key} {m["_cycles"][key]} cycles over poll_grade.py\'s '
                                f'{polls[short]} us')
    out['item.aecp.probe'] = out['item.aecp.response']
    return out


def donor_column(n, pin):
    point, m = POINT[n], measured('D' + n)
    full = dict(load_grade.stated(lane, point, {point: pin}))
    out = {}
    for key in MEASURED + KINDS[:2] + POLLS + BUILDS:
        if key in ('item.retained', 'item.mrpdu', 'step'):
            continue
        if key in WALK:
            out[key] = m[key]
        else:
            out[key] = max(v for v in (m.get(key), full.get(key)) if v)
    out['item.retained'] = max(out['record.srp'], full['item.retained'])
    out['item.mrpdu'] = max(out['build_one'], full['item.mrpdu'])
    out['step'] = full['step']
    out['item.aecp.probe'] = out['item.aecp.response']
    return out


have = [n for n in ('1', '8', '32') if (costs / ('C' + n) / 'costs.json').exists()
        and (costs / ('D' + n) / 'costs.json').exists()]
pin = {POINT[n]: pin_column(n) for n in have}
donor = {POINT[n]: donor_column(n, pin[POINT[n]]) for n in have}
for name, table in (('STATED_US', pin), ('STATED_US_DONOR', donor)):
    print(f'{name} = {{')
    for point, row in table.items():
        print(f"    '{point}': {json.dumps(row)},")
    print('}')
for f in findings:
    print('FINDING', f)
(costs / 'tables.json').write_text(json.dumps({'STATED_US': pin, 'STATED_US_DONOR': donor, 'findings': findings},
                                              indent=1) + '\n')
