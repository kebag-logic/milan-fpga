#!/usr/bin/env python3
"""The failing tests and their messages for chosen plants in a campaign's results.json. usage: plant_failures.py RESULTS.json NAME..."""
import json, sys
by = {r['name']: r for r in json.load(open(sys.argv[1]))}
for n in sys.argv[2:]:
    r = by[n]
    print(n, r['status'], 'rc', r['rc'])
    print('   failures:', json.dumps(r['failures'])[:900])
    print('   tests:', json.dumps(r['tests'])[:600])
