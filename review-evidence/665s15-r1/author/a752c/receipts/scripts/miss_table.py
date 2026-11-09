#!/usr/bin/env python3
"""Per group, the T_svc misses at each point (probe instances not within T_svc, of the group's probe instances), from
each leg's per-group results, and the totals; misses are recorded, not graded.

usage: python3 -I miss_table.py LABEL=RESULTS_DIR... > OUT.md
"""
import json
import sys
from pathlib import Path

legs = [a.split('=', 1) for a in sys.argv[1:]]
tables = {}
for label, d in legs:
    rows = {}
    for f in sorted(Path(d).glob('*.json')):
        if f.name == 'results.json':
            continue
        g = json.loads(f.read_text())
        probes = g.get('probes', [])
        rows[g['group']] = (sum(1 for p in probes if not p.get('within_t_svc')), len(probes))
    tables[label] = rows
groups = sorted({g for rows in tables.values() for g in rows})
print('| Group | ' + ' | '.join(f'{label} misses / instances' for label, _ in legs) + ' |')
print('|---|' + '---:|' * len(legs))
for g in groups:
    cells = [f'{tables[l][g][0]} / {tables[l][g][1]}' if g in tables[l] else 'not in this point\'s set'
             for l, _ in legs]
    print(f'| `{g}` | ' + ' | '.join(cells) + ' |')
tot = [f'**{sum(m for m, _ in tables[l].values())} / {sum(n for _, n in tables[l].values())}**' for l, _ in legs]
print('| all groups | ' + ' | '.join(tot) + ' |')
