#!/usr/bin/env python3
"""Compare the source campaign's core mutants with the exported table.

Usage: compare_mutants.py SOURCE_MUTANTS.json EXPORT_MUTATIONS.json
A source mutant is core when its path is one of the exported production files.
Reports core mutants missing from the export, plant text changes, killer changes,
and exported mutants with no source counterpart.
"""
import json, sys, collections
MAP = {'sw/firmware/ctrl/adp/adp.c': 'src/adp.c', 'sw/firmware/ctrl/adp/adp.h': 'include/adp.h',
       'sw/firmware/ctrl/acmp/acmp.c': 'src/acmp.c', 'sw/firmware/ctrl/acmp/acmp.h': 'include/acmp.h',
       'sw/firmware/ctrl/maap/maap.c': 'src/maap.c', 'sw/firmware/ctrl/maap/maap.h': 'include/maap.h',
       'sw/firmware/ctrl/wire/wire.h': 'include/wire.h'}
src = json.load(open(sys.argv[1])); exp = json.load(open(sys.argv[2]))
def norm(p):
    for k, v in MAP.items():
        if p.endswith(k) or p == k.split('sw/firmware/ctrl/')[1]:
            return v
    return None
paths = collections.Counter(m['path'] for m in src)
print('source paths:', dict(paths))
core = [m for m in src if norm(m['path'])]
print('source mutants', len(src), 'core-path mutants', len(core), 'exported', len(exp))
E = {m['name']: m for m in exp}
missing = changed_plant = changed_kill = 0
for m in core:
    e = E.get(m['name'])
    if e is None:
        # try matching by plant text
        cands = [x for x in exp if x['old'] == m['old'] and x['new'] == m['new']]
        print('MISSING-BY-NAME', m['name'], m['path'], 'plant-match:', [c['name'] for c in cands])
        missing += 1
        continue
    if e['path'] != norm(m['path']) or e['old'] != m['old'] or e['new'] != m['new']:
        print('PLANT-CHANGED', m['name']); changed_plant += 1
    sk = sorted((k[1], k[2]) for k in m['kills'])
    ek = sorted((k['test'], k['needle']) for k in e['kills'])
    if sk != ek:
        print('KILLERS-CHANGED', m['name'], '\n   src:', sk, '\n   exp:', ek); changed_kill += 1
srcnames = {m['name'] for m in core}
extra = [m['name'] for m in exp if m['name'] not in srcnames]
print('EXPORT-ONLY', len(extra), extra)
print('summary missing', missing, 'plant-changed', changed_plant, 'killers-changed', changed_kill)
