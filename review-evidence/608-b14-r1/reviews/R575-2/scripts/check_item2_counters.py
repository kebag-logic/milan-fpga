#!/usr/bin/env python3
"""R575-2: which GET_COUNTERS names moved in item 2's phases (switches.json).
Usage: check_item2_counters.py <author dir>"""
import ast, json, os, sys, collections
ph = json.load(open(os.path.join(sys.argv[1], 'item2/summary/switches.json')))
moved = collections.defaultdict(set)
for p in ph:
    for fld in ('counters_before_to_end', 'counters_locked_to_end'):
        v = p.get(fld)
        if v is None: continue
        d = ast.literal_eval(v) if isinstance(v, str) else v
        for desc, cs in d.items():
            for name, delta in cs.items():
                if delta: moved[(desc, name)].add(p['tag'].split('-')[1] + ':' + fld.split('_')[1])
for k in sorted(moved): print(k, sorted(moved[k]))
