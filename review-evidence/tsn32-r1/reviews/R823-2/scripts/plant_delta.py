#!/usr/bin/env python3
"""List plants present at main whose definition differs at head, and show whether only the anchor text moved."""
import json, subprocess, sys
repo, main, head = sys.argv[1:4]
load = lambda r: {p['name']: p for p in json.loads(subprocess.run(['git', '-C', repo, 'show', r + ':tests/mutations.json'], check=True, capture_output=True, text=True).stdout)}
M, H = load(main), load(head)
strip = lambda s: '\n'.join(l for l in s.split('\n') if 'mark(a' not in l and '!= 0u) {' not in l)
for n, p in M.items():
    q = H[n]
    if p != q:
        keys = [k for k in p if p[k] != q.get(k)]
        print(n, 'differs in', keys)
        if p['kills'] != q['kills']:
            print('   kills main:', [(k['test'], k['needle']) for k in p['kills']])
            print('   kills head:', [(k['test'], k['needle']) for k in q['kills']])
