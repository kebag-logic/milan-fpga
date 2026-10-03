#!/usr/bin/env python3
"""Field-by-field comparison of syn/ooc/pp_resource_baseline.json between two revisions.
Usage: compare_baseline.py OLD_REV NEW_REV  (run inside the repository)"""
import json, subprocess, sys
def load(rev):
    return json.loads(subprocess.check_output(['git', 'show', f'{rev}:syn/ooc/pp_resource_baseline.json']))
old, new = load(sys.argv[1]), load(sys.argv[2])
def walk(a, b, path=''):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a: print(f'ADDED   {path}/{k} = {json.dumps(b[k])[:160]}')
            elif k not in b: print(f'REMOVED {path}/{k}')
            else: walk(a[k], b[k], f'{path}/{k}')
    elif a != b:
        print(f'CHANGED {path}: {json.dumps(a)[:300]} -> {json.dumps(b)[:300]}')
print('top-level keys', list(old), list(new))
for ep in new['endpoints']:
    print('== endpoint', ep, 'keys', list(new['endpoints'][ep]))
    o, n = old['endpoints'][ep], new['endpoints'][ep]
    for k in sorted(set(o) | set(n)):
        if k in ('figures', 'scopes'):
            continue
        walk(o.get(k), n.get(k), f'{ep}/{k}')
    fo, fn = o.get('figures', {}), n.get('figures', {})
    print(f'  figures: ' + ', '.join(f'{k} {fo.get(k)}->{fn.get(k)} ({(fn.get(k) or 0)-(fo.get(k) or 0):+g})' for k in fn))
    so, sn = o.get('scopes', {}), n.get('scopes', {})
    print(f'  scopes: {len(so)} -> {len(sn)}; added {sorted(set(sn)-set(so))} removed {sorted(set(so)-set(sn))}')
