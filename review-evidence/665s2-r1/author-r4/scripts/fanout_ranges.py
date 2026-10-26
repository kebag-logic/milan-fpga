#!/usr/bin/env python3
"""Every measured fan-out (a probe with a fanout figure) per arm: its ms, recipients and
per-recipient CPU cycles, then the ranges per arm and point, so each stated range can be checked
against every cell. Usage: fanout_ranges.py RUNS (holding A1, A8, B1, B8 results.json)."""
import json
import sys
from pathlib import Path

runs = Path(sys.argv[1])
cells = {}
for arm in ('A1', 'A8', 'B1', 'B8'):
    results = json.loads((runs / arm / 'results.json').read_text())['results']
    rows = [r for g in results for r in g['probes'] if r.get('fanout') and r['status'] == 'measured'
            and r['fanout'].get('recipients', 0) > 1]
    cells[arm] = rows
    for r in rows:
        print(f"{arm} {r['probe']:45s} {r['ms']:9.5f} ms  recipients {r['fanout']['recipients']:2d}  "
              f"{r['fanout']['per_recipient_cpu_cycles']:6d} cycles a recipient  "
              f"{'fits' if r['within_t_svc'] else 'MISS'}{'' if r['within_ceiling'] else ' over ceiling'}")
print()
def span(rows, key):
    vals = [key(r) for r in rows]
    return (min(vals), max(vals)) if vals else None
for label, arms in (('A', ('A1', 'A8')), ('B', ('B1', 'B8')), ('A+B', ('A1', 'A8', 'B1', 'B8')),
                    ('1x1 A', ('A1',)), ('1x1 B', ('B1',)), ('1x1 A+B', ('A1', 'B1')),
                    ('8x8 A', ('A8',)), ('8x8 B', ('B8',)), ('8x8 A+B', ('A8', 'B8'))):
    rows = [r for a in arms for r in cells[a]]
    print(f"{label:8s} ms {span(rows, lambda r: r['ms'])}  cycles a recipient "
          f"{span(rows, lambda r: r['fanout']['per_recipient_cpu_cycles'])}  "
          f"recipients {sorted({r['fanout']['recipients'] for r in rows})}  n={len(rows)}")
for label, arms in (('A', ('A1', 'A8')), ('B', ('B1', 'B8')), ('A+B', ('A1', 'A8', 'B1', 'B8'))):
    rows = [r for a in arms for r in cells[a] if not r['probe'].startswith('aecp_fanout.set_name')]
    print(f"{label:8s} not SET_NAME: cycles a recipient {span(rows, lambda r: r['fanout']['per_recipient_cpu_cycles'])}")
    rows = [r for a in arms for r in cells[a] if r['probe'].startswith('aecp_fanout.set_name')]
    print(f"{label:8s} SET_NAME: cycles a recipient {span(rows, lambda r: r['fanout']['per_recipient_cpu_cycles'])}")
