#!/usr/bin/env python3
"""Field-level diff of two capture receipts. Usage: receipt_field_diff.py OLD NEW"""
import json, sys
def flat(x, p=''):
    if isinstance(x, dict):
        for k, v in x.items(): yield from flat(v, f'{p}.{k}' if p else k)
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from flat(v, f'{p}[{i}]')
    else:
        yield p, x
a = dict(flat(json.load(open(sys.argv[1])))); b = dict(flat(json.load(open(sys.argv[2]))))
changed = [k for k in sorted(set(a) | set(b)) if a.get(k, '<absent>') != b.get(k, '<absent>')]
for k in changed:
    print(f'{k}\t{json.dumps(a.get(k, "<absent>"))[:90]}\t{json.dumps(b.get(k, "<absent>"))[:90]}')
print('changed fields:', len(changed))
