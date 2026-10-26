#!/usr/bin/env python3
"""Compare a reviewer results.json with the author's published one, probe by probe and pass figure by figure.
Usage: compare_results.py MINE THEIRS"""
import json, sys
mine, theirs = (json.load(open(p)) for p in sys.argv[1:3])
def index(r):
    return {g['group']: g for g in r['results']}
a, b = index(mine), index(theirs)
diffs = 0
print('groups mine', len(a), 'theirs', len(b), 'only mine', sorted(set(a) - set(b)), 'only theirs', sorted(set(b) - set(a)))
for name in sorted(set(a) & set(b)):
    ga, gb = a[name], b[name]
    pa = {p['probe']: p for p in ga['probes']}; pb = {p['probe']: p for p in gb['probes']}
    for k in sorted(set(pa) | set(pb)):
        if pa.get(k) != pb.get(k):
            diffs += 1
            print('PROBE DIFF', name, k)
    if ga['passes'] != gb['passes'] or ga['summary'] != gb['summary'] or ga['code'] != gb['code']:
        diffs += 1
        print('PASS/SUMMARY DIFF', name)
print('misses mine', len(mine['misses']), 'theirs', len(theirs['misses']), 'same' if mine['misses'] == theirs['misses'] else 'DIFFER')
print('refusals mine', len(mine['refusals']), 'theirs', len(theirs['refusals']))
print('differences:', diffs)
