#!/usr/bin/env python3
"""For each plant re-anchored between main and head: the old->new line diff at main and at head, mark lines dropped."""
import difflib, json, subprocess, sys
repo, main, head = sys.argv[1:4]
load = lambda r: {p['name']: p for p in json.loads(subprocess.run(['git', '-C', repo, 'show', r + ':tests/mutations.json'], check=True, capture_output=True, text=True).stdout)}
M, H = load(main), load(head)
def delta(p):
    a = [l for l in p['old'].split('\n') if 'mark(a' not in l]
    b = [l for l in p['new'].split('\n') if 'mark(a' not in l]
    return [l for l in difflib.unified_diff(a, b, lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('---', '+++')]
for n in M:
    if M[n]['old'] != H[n]['old'] or M[n]['new'] != H[n]['new']:
        dm, dh = delta(M[n]), delta(H[n])
        print(('SAME ' if dm == dh else 'DIFF ') + n)
        if dm != dh:
            print('  main:', dm); print('  head:', dh)
