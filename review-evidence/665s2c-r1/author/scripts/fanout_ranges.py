#!/usr/bin/env python3
"""Every notification fan-out an arm measured, whole: the cost a recipient and the fan-out's time.

Reads every graded group JSON of each arm and takes each probe with a fan-out over more than one
recipient (S2 round 4's rule: every fan-out measured, on every interface, both SET_CONTROL
fan-outs included); nothing is measured.
usage: fanout_ranges.py REGRADE ARM..."""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
for arm in sys.argv[2:]:
    probes = []
    for path in sorted((root / arm).glob('*.json')):
        if path.name == 'results.json':
            continue
        probes += [p for p in json.loads(path.read_text()).get('probes', [])
                   if p.get('fanout') and p['fanout']['recipients'] > 1 and p.get('status') == 'measured']
    if not probes:
        print(f'{arm}: no fan-out')
        continue
    cost = [p['fanout']['per_recipient_cpu_cycles'] for p in probes]
    ms = [p['ms'] for p in probes]
    recipients = sorted({p['fanout']['recipients'] for p in probes})
    misses = sorted(f"{p['row']} if{p['interface']} {p['ms']:.2f}{'' if p['within_ceiling'] else ' over ceiling'}"
                    for p in probes if not p['within_t_svc'])
    print(f'{arm}: {len(probes)} fan-outs, recipients {recipients}; a recipient {min(cost):,} to {max(cost):,} CPU cycles; '
          f'{min(ms):.2f} to {max(ms):.2f} ms; over T_svc: {misses or "none"}')
    for p in sorted(probes, key=lambda p: (p['row'], p['interface'], p['probe'])):
        print(f"  {p['probe']} ({p['row']}, if{p['interface']}): {p['fanout']['per_recipient_cpu_cycles']:,} a recipient, "
              f"{p['ms']:.2f} ms")
