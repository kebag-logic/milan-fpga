#!/usr/bin/env python3
"""Compare the route-1x1 endpoint committed at the head with the record the published `record --write` receipt printed.
usage: cmp_record.py <pp_resource_baseline.json at the head> <record-write.txt> <pp_resource_baseline.json at the parent>"""
import json, sys
head = json.load(open(sys.argv[1])); parent = json.load(open(sys.argv[3]))
text = open(sys.argv[2]).read(); rec = json.loads(text[text.index('{'):text.rindex('}') + 1])
def endpoint(b):
    eps = b.get('endpoints', b)
    return eps['route-1x1'] if isinstance(eps, dict) else next(e for e in eps if e.get('name') == 'route-1x1')
h, p = endpoint(head), endpoint(parent)
fails = []
for k in rec:
    if h['record'].get(k) != rec[k]:
        fails.append(f'field {k}: head differs from the receipt')
changed = sorted(k for k in set(h) | set(p) if h.get(k) != p.get(k))
print('fields the commit changed in route-1x1:', changed)
print('figures at head:', h['record']['figures'])
print('record keys only in head:', sorted(set(h['record']) - set(rec)))
print('tolerance/floors unchanged:', {k: h[k] == p[k] for k in h if k not in ('record', 'measured')})
others = [k for k in (head.get('endpoints', head)) if k != 'route-1x1'] if isinstance(head.get('endpoints', head), dict) else []
same_others = all(head['endpoints'][k] == parent['endpoints'][k] for k in others) if others else None
print('other endpoints unchanged:', same_others, others)
top = sorted(k for k in set(head) | set(parent) if k != 'endpoints' and head.get(k) != parent.get(k))
print('top-level keys changed:', top)
print('receipt keys:', sorted(rec)); print('\n'.join(fails) or 'receipt record == committed record (every receipt field)')
