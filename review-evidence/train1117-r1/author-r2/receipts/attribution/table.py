#!/usr/bin/env python3
"""table.py: decision 3's attribution table (markdown) from attr/out/<label>.json, one row per head in train order,
cycles and committed instructions, with each image's sha256 prefix (arm A's) and the rule's figure against the
statements the composition carries at 1x1/1if (round 1's STOP addendum: the long record 975 us, event.AECP 75 us,
event.MAAP 165 us in STATED_US, the datapath events 35 us)."""
import hashlib
import json
from pathlib import Path

T = Path('<scratch>/attr')
HEADS = [('base', 'cb96336d', 'dev-soft-core'), ('s1', '43b954e6', '1: #881'), ('s2', '877c99e4', '2: #914'),
         ('s3', '9c0e1974', '3: #918'), ('s4', '22a82038', '4: #935'), ('s5', '2078c438', '5: #933'),
         ('s6', '7c28f53f', '6: #938'), ('s7', '6a8126e4', '7: #931'), ('fix', '03c92617', 'THE STEP'),
         ('s8', 'eafe4a16', '8: #932'), ('931', 'd06ded5a', '#931 alone')]
STATED = {'record': 975, 'event.AECP': 75, 'event.MAAP': 165, 'AS_PATH_CHANGED': 35, 'AVB_INFO_CHANGED': 35}


def image(label: str) -> str:
    f = T / 'b' / label / 'none/image/ctrl_app.elf'
    return hashlib.sha256(f.read_bytes()).hexdigest()[:8] if f.is_file() else '-'


def cell(e: dict | None, stated: int) -> str:
    if not e:
        return 'pending'
    mark = '**' if e['us'] > stated else ''
    return f"{e['cycles']:,} / {e['instr']:,} ({mark}{e['us']}{mark})"


rows = ['| Head | Step | Image | Largest record: cycles / instr (us) | CPI | Its pass: rom refills / fetch wait | '
        'event.AECP | event.MAAP | AS_PATH_CHANGED | AVB_INFO_CHANGED |',
        '|---|---|---|---:|---:|---:|---:|---:|---:|---:|']
for label, sha, step in HEADS:
    p = T / 'out' / f'{label}.json'
    if not p.is_file():
        rows.append(f'| `{sha}` | {step} | - | pending | | | | | | |')
        continue
    d = json.loads(p.read_text())
    r = (d.get('record') or [None])[0]
    ev = d.get('events', {})
    rows.append(f"| `{sha}` | {step} | `{image(label)}` | {cell(r, STATED['record'])} | {r['cpi'] if r else '-'} | "
                f"{r.get('pass_refills', '-')} / {r.get('pass_fetch_wait', '-'):,} | "
                f"{cell(ev.get('event.AECP'), 75)} | {cell(ev.get('event.MAAP'), 165)} | "
                f"{cell(ev.get('AS_PATH_CHANGED'), 35)} | {cell(ev.get('AVB_INFO_CHANGED'), 35)} |")
where = {}
for label, _, _ in HEADS:
    p = T / 'out' / f'{label}.json'
    if p.is_file():
        for k, v in json.loads(p.read_text()).get('events', {}).items():
            where.setdefault(k, set()).add(v['where'])
print('\n'.join(rows))
print()
print('Where each event was dearest: ' + '; '.join(f"{k} {', '.join(sorted(v))}" for k, v in sorted(where.items())))
