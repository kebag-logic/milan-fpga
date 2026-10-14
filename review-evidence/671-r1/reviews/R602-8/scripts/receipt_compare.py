"""Compare two capture receipts: list top-level keys that differ and verify arms/rows.

Usage: python3 -I receipt_compare.py <old.json> <new.json>
"""
import json
import sys

old = json.load(open(sys.argv[1]))
new = json.load(open(sys.argv[2]))
print('changed keys:', sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k)))
arms = new['measurements']
print('arms:', len(arms), 'captures:', sum(len(a['rows']) for a in arms))
print('rows identical to old:', [a['rows'] for a in old['measurements']] == [a['rows'] for a in arms])
print('arms identical to old:', old['measurements'] == arms)
for a in arms:
    print(' ', a['shape'], a['cpu_hz'], a['traffic'], 'n=%d' % len(a['rows']),
          'max_cycles=%d' % max(r['sys_cycles'] for r in a['rows']))
print('maxima:', json.dumps(new['maxima']))
for k in ('simulator', 'verilator', 'simulator_version'):
    if k in new:
        print(k, new[k])
print('top-level keys:', sorted(new))
