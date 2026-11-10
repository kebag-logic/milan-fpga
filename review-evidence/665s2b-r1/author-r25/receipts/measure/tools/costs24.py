#!/usr/bin/env python3
"""Round 24 (#665): each point's measured costs, from instrumented budget-harness legs, as the load gate's stated costs.

usage: python3 -I costs24.py OUT.json POINT N_IF PARTS.json EVENTS.json RESULTS_DIR...

PARTS.json is parts.py's (round 21's parser, unchanged) over the legs' logs, EVENTS.json eventcost.py's (round 20's,
unchanged); each RESULTS_DIR holds a leg's results.json, whose groups carry poll_grade.held's heaviest base and items
and whole_grade.held's heaviest build, build of one and aged step. Each stated cost is the most measured over every
instance plus 5 %, rounded up to 5 us (100 CPU cycles a microsecond at sys, 100 MHz). A timer slot's cost is its
module's heaviest slot (the composition's slot order: ADP's, ACMP's and MAAP's one an interface, then AECP's); AECP's
event is its heaviest of its timer slot and the face events it takes (COUNTERS_CHANGED, AVB_INFO_CHANGED,
AS_PATH_CHANGED, AMAP_LIVE_WRITE). Prints each cost, its most and where.
"""
import json
import math
import sys
from pathlib import Path

stated = lambda cycles: int(math.ceil(cycles * 1.05 / 100 / 5 - 1e-9) * 5)
SLOTS = {1: {'ADP': [0], 'ACMP': [1], 'MAAP': [2], 'AECP': [3]},
         2: {'ADP': [0, 1], 'ACMP': [2, 3], 'MAAP': [4, 5], 'AECP': [6]}}
FACE = ('COUNTERS_CHANGED', 'AVB_INFO_CHANGED', 'AS_PATH_CHANGED', 'AMAP_LIVE_WRITE')
POLL_KINDS = ('base', 'withdraw', 'rebuild', 'walk', 'reclaim', 'retained', 'mrpdu', 'acmp', 'aecp')


def main():
    out_path, point, n_if = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
    parts = json.loads(Path(sys.argv[4]).read_text())['parts']
    events = json.loads(Path(sys.argv[5]).read_text())
    most, where = {}, {}

    def note(key, cycles, at):
        if cycles > most.get(key, -1):
            most[key], where[key] = cycles, at

    for ch in ('srp', 'aecp', 'acmp', 'adp', 'maap'):
        p = parts.get(f'record.{ch}')
        if p:
            note(f'record.{ch}', p['most_cycles'], p['where'][0])
    for module, slots in SLOTS[n_if].items():
        for s in slots:
            e = events.get(f'TIMER#{s}')
            if e:
                note(f'event.{module}', e['most_cycles'], f'TIMER#{s}, {e["taken"]} taken')
    # an event's first word carries its interface above its type (mbx_contract.h, IF at bits 8 to 11), so the
    # parser names an event of interface 1 by its number, the type ORed with 0x100
    code = {'LINK': 2, 'GM': 3, 'TICK': 4, 'COUNTERS_CHANGED': 5, 'AVB_INFO_CHANGED': 6, 'AS_PATH_CHANGED': 7,
            'AMAP_LIVE_WRITE': 8}
    for kind in FACE:
        for name in (kind, str(code[kind] | 0x100)):
            e = events.get(name)
            if e:
                note('event.AECP', e['most_cycles'], f'{name}, {e["taken"]} taken')
    for kind, key in (('TICK', 'event.TICK'), ('GM', 'event.GM'), ('LINK', 'event.LINK')):
        for name in (kind, str(code[kind] | 0x100)):
            e = events.get(name)
            if e:
                note(key, e['most_cycles'], f'{name}, {e["taken"]} taken')
    for key, part in (('centisecond', 'centisecond_consumers'), ('events_none', 'events_none')):
        p = parts.get(part)
        if p:
            note(key, p['most_cycles'], p['where'][0])
    for d in sys.argv[6:]:
        r = json.loads((Path(d) / 'results.json').read_text())
        for g in r['results']:
            at = f'{Path(d).parent.name}/{g["group"]}'
            for k, v in g['passes']['polls']['heaviest'].items():
                note('base' if k == 'base' else f'item.{k}', v, at)
            for k, v in g['passes']['stated']['heaviest'].items():
                note({'build-one': 'build_one'}.get(k, k), v, at)
    out = {k: stated(v) for k, v in most.items() if v > 0}
    out_path.write_text(json.dumps({point: out, '_most_cycles': most, '_where': where}, indent=1) + '\n')
    for k in sorted(most):
        print(f'{point} {k:14} most {most[k]:>8,} CPU cycles, stated {stated(most[k]) if most[k] else 0:>5} us; '
              f'{where[k]}')


if __name__ == '__main__':
    main()
