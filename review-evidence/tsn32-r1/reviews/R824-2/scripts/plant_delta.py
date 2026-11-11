#!/usr/bin/env python3
"""Plant-table delta between two revisions: added, removed, and changed fields per plant; order of the common plants.
usage: plant_delta.py REPO OLD NEW"""
import json, subprocess, sys
repo, a, b = sys.argv[1:4]
t = lambda r: json.loads(subprocess.run(['git', '-C', repo, 'show', r + ':tests/mutations.json'], check=True, capture_output=True, text=True).stdout)
A, B = t(a), t(b); ia = {m['name']: m for m in A}; ib = {m['name']: m for m in B}
print('counts', len(A), len(B))
print('added', [m['name'] for m in B if m['name'] not in ia])
print('removed', [m['name'] for m in A if m['name'] not in ib])
for n in ia:
    if n in ib and ia[n] != ib[n]:
        print('changed', n, 'fields', sorted(k for k in set(ia[n]) | set(ib[n]) if ia[n].get(k) != ib[n].get(k)))
print('common order kept', [m['name'] for m in A if m['name'] in ib] == [m['name'] for m in B if m['name'] in ia])
src = subprocess.run(['git', '-C', repo, 'show', b + ':src/acmp.c'], check=True, capture_output=True, text=True).stdout
for m in B:
    if m['name'] not in ia:
        print('new plant', m['name'], 'old-text occurrences in src/acmp.c:', src.count(m['old']))
