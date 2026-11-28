"""The larger of each measurement over consecutive censuses at one point and clock (round 9's merged-census practice):
each cost's cycles, and each retry round's, from whichever census measured more. usage: merge4.py OUT A.json B.json"""
import json, sys
out, a, b = sys.argv[1], json.load(open(sys.argv[2])), json.load(open(sys.argv[3]))
assert a['cpu_hz'] == b['cpu_hz'] and a['shape'] == b['shape']
mhz = a['cpu_hz'] // 1_000_000
rule = lambda c: -(-c * 105 // (mhz * 100 * 5)) * 5  # noqa: E731
costs, sources = {}, {}
for k in sorted(set(a['costs']) | set(b['costs'])):
    x, y = a['costs'].get(k), b['costs'].get(k)
    pick, src = (x, sys.argv[2]) if y is None or (x is not None and x['cycles'] >= y['cycles']) else (y, sys.argv[3])
    costs[k] = dict(pick, rule_us=rule(pick['cycles']), us=pick['cycles'] / mhz)
    sources[k] = src
rounds = {}
for k in sorted(set(a['rounds']) | set(b['rounds'])):
    x, y = a['rounds'].get(k), b['rounds'].get(k)
    rounds[k] = x if y is None or (x is not None and x['cycles'] >= y['cycles']) else y
json.dump(dict(status='MERGED MAXIMA of two censuses at one point and clock', cpu_hz=a['cpu_hz'], shape=a['shape'],
               groups=a['groups'], costs=costs, rounds=rounds, sources=sources,
               owed_969=a.get('owed_969', []) + b.get('owed_969', [])), open(out, 'w'), indent=1)
print('merged', len(costs), 'costs;', sum(1 for v in sources.values() if v == sys.argv[3]), 'from the second')
