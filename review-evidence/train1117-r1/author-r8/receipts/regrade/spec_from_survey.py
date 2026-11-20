#!/usr/bin/env python3
"""spec_from_survey.py OUTDIR SPEC.json: commit_restate.py's spec from a head's survey (r4meas/out/<rev>): every
statement the survey reports exceeded (OVER, or OVER-raw past its statement by the rule), restated by the unchanged rule,
and each AECP class record_classes.py refuses, into the table that states it. A statement a header constant mirrors is
left out and listed apart: 8x8/1if's record.srp, which load_grade's srp_unit holds to ctrl_loop.h's
CTRL_LOOP_SRP_UNIT_US (#665's ruling of 2026-11-18, item 2: a restatement moves no header constant)."""
import json
import re
import sys
from pathlib import Path

out, spec_path = Path(sys.argv[1]), Path(sys.argv[2])
PT = {'1x1': '1x1/1if', '8x8-1if': '8x8/1if', '8x8': '8x8/2if'}
POLL = {'1x1/1if': 'one', '8x8/1if': 'e1', '8x8/2if': 'two'}
STATED = {'1x1/1if': 's1', '8x8/1if': 'own81', '8x8/2if': 's2'}
HEADER_TIED = {('8x8/1if', 'record.srp')}
POLL_FED = {'base', *(f'item.{k}' for k in ('reclaim', 'retained', 'mrpdu', 'acmp', 'walk', 'acmp_declined'))}
ROW = re.compile(r'^(\S+)\s+([\d,]+)\s+[\d.]+\s+(\d+)\s+(\d+)\s+(OVER(?:-raw)?)\s+(.*?); (\S+?)(?:\s|$)')
spec, held = {}, []
for p, point in PT.items():
    f = out / f'survey-{p}/compare-ordinary.txt'
    for line in f.read_text().splitlines() if f.is_file() else []:
        m = ROW.match(line)
        if not m:
            continue
        key, cycles, rule, stated, verdict, table, where = m.groups()
        cycles, rule, stated = int(cycles.replace(',', '')), int(rule), int(stated)
        if rule <= stated:
            continue  # OVER-raw within its statement by the rule: nothing to restate
        if point == '8x8/1if' and table.startswith('load_grade') and key in POLL_FED:
            continue  # at a NEAREST point load_grade.stated takes the base and these items from poll_grade (EIGHT_ONE)
        if table.startswith('poll_grade'):
            name = key.split('.', 1)[1] if key.startswith('item.') else key
            name = {'record': 'retained'}.get(name, name)
            t = POLL[point]
        else:
            name, t = key, STATED[point]
        if (point, key) in HEADER_TIED:
            held.append(f'{point} {key} {cycles:,} cycles, {rule} us by the rule, stated {stated} us ({where}): '
                        'its header constant CTRL_LOOP_SRP_UNIT_US mirrors it, not restated')
            continue
        e = spec.get((t, point, name))
        if e is None or cycles > e['cycles']:
            spec[(t, point, name)] = dict(table=t, point=point, key=name, us=rule, cycles=cycles,
                                          where=where.rstrip(';').split('/', 1)[-1])
    rc = out / f'record-classes-{p}.txt'
    for line in rc.read_text().splitlines() if rc.is_file() else []:
        m = re.match(r'REFUSED (\S+) \S+ (\S+): a record of ([\d,]+) CPU cycles, (\d+) us by the rule, over the paced '
                     r"record's (\d+) us \((.*?), paced\)", line)
        if m:
            kind = 'an accepted SET_CONFIGURATION' if 'SET_CONFIGURATION' in m[6] else 'a one-row edit'
            cycles = int(m[3].replace(',', ''))
            spec[('paced', m[1], kind)] = dict(table='paced', point=m[1], key=kind, us=int(m[4]), cycles=cycles,
                                               where=f'answering-ports {m[2]}, {m[6]}')
spec_path.write_text(json.dumps(sorted(spec.values(), key=lambda e: (e['point'], e['table'], e['key'])), indent=1))
for e in sorted(spec.values(), key=lambda e: (e['point'], e['table'], e['key'])):
    print(f"restate {e['point']} {e['table']}.{e['key']} {e['us']} us ({e['cycles']:,} cycles, {e['where']})")
for h in sorted(set(held)):
    print('HELD', h)
