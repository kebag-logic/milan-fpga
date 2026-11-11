#!/usr/bin/env python3
"""Status and kill words of the walk's plants and of the merge's plants. usage: plant_kills.py RESULTS.json MUTATIONS.json"""
import json, sys
by = {r['name']: r for r in json.load(open(sys.argv[1]))}
table = {m['name']: m for m in json.load(open(sys.argv[2]))}
names = [n for n in table if n.startswith('walk-')] + ['acmp-unbind-srp-after-response', 'acmp-first-owed-releases-every-change',
         'acmp-wide-release-loop-word-ignored', 'acmp-wide-release-loop-word-off-by-one',
         'acmp-timer-port-called-every-time', 'acmp-publish-stream-cache-stale']
print('results', len(by), 'statuses', sorted({r['status'] for r in by.values()}))
for n in names:
    print('%-42s %s' % (n, by[n]['status']))
    for k in table[n]['kills']:
        print('    %s [%s] "%s"' % (k['test'], k.get('arm', 'default arm'), k['needle']))
