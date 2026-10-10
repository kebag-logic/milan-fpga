#!/usr/bin/env python3
"""R575-2: UTC of item 2's setup binds, first set, last poll and teardown unbinds (wall clock in the
records, mapped through the soak t0 1791613402.708542 = 06:23:22.708542).  Usage: <author dir>"""
import datetime, json, os, sys
a = sys.argv[1]
T0 = 1791613402.708542; base = datetime.datetime(2026, 10, 10, 6, 23, 22, 708542)
f = lambda t: (base + datetime.timedelta(seconds=t - T0)).strftime('%H:%M:%S.%f')[:-3]
J = lambda p: [json.loads(l) for l in open(os.path.join(a, p))]
ev = J('item2/cyc01/events.jsonl'); print('cyc01 first set-clock', f([e['t'] for e in ev if e['kind'] == 'set-clock'][0]))
print('setup2 binds', [(e['talker'], f(e['t'])) for e in J('item2/setup2/events.jsonl') if e['kind'] == 'bind'])
print('teardown unbinds', [(e['talker'], f(e['t'])) for e in J('item2/teardown/events.jsonl') if e['kind'] == 'unbind'])
print('cyc09 poll-end', f([e['t'] for e in J('item2/cyc09/events.jsonl') if e['kind'] == 'poll-end'][0]))
print('soak AAF bind', f([e['t'] for e in J('soak/bind-a-aaf.jsonl') if e['kind'] == 'bind'][0]), 'soak CRF bind', f([e['t'] for e in J('soak/bind-a-crf.jsonl') if e['kind'] == 'bind'][0]))
runs = ['cyc01', 'cyc03', 'cyc05', 'cyc07', 'cyc09']; E = {r: J(f'item2/{r}/events.jsonl') for r in runs}
t = lambda r, k, i: [e['t'] for e in E[r] if e['kind'] == k][i]
for x, y in zip(runs, runs[1:]): print(x, '->', y, 'last phase-end to first set-clock %.2f s' % (t(y, 'set-clock', 0) - t(x, 'phase-end', -1)))
