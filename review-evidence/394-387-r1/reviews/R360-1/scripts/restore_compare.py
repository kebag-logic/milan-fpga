#!/usr/bin/env python3
"""Compare the packet's start and end censuses on response payloads (sequence
numbers and round-trip times removed).  Prints keys and differing field names
only, never identifier values.  usage: restore_compare.py <packet author dir>"""
import json, os, sys
pk = sys.argv[1]
load = lambda n: [json.loads(l) for l in open(os.path.join(pk, n)) if l.strip()]
key = lambda r: (r.get('role'), r.get('what'))
strip = lambda v: {a: b for a, b in v.items() if a not in ('seq', 'rtt_ms', 't')} if isinstance(v, dict) else v
S = {key(r): strip(r.get('response')) for r in load('census-start.jsonl')}
E = {key(r): strip(r.get('response')) for r in load('census-end.jsonl')}
print('entries start/end:', len(S), len(E))
for k in S:
    if S[k] != E.get(k):
        fields = sorted(f for f in set(S[k]) | set(E[k] or {}) if S[k].get(f) != (E[k] or {}).get(f))
        print('differs', k, 'fields', fields)
st = [k for k in S if k[1] and k[1].startswith('state-')]
print('stream states', len(st), '; conn_count>0 at start', [k for k in st if S[k].get('conn_count')],
      '; at end', [k for k in st if E[k].get('conn_count')])
print('DUT clock source index start/end:', S[('dut', 'clock')]['payload'][8:12], E[('dut', 'clock')]['payload'][8:12])
print('peer clock source index start/end:', S[('peer', 'clock')]['payload'][8:12], E[('peer', 'clock')]['payload'][8:12])
print('non-state, non-counter, non-avb payloads equal:', all(S[k] == E.get(k) for k in S if k[1] and not k[1].startswith(('state-', 'counter-', 'avb'))))
