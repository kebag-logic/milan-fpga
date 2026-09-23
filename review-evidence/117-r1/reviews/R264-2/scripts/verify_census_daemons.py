#!/usr/bin/env python3
"""Bench-state claims: the 18 ACMP states before and after each packet's runs,
and which bench hosts the daemon check covered (host names printed as roles).

usage: verify_census_daemons.py EVIDENCE_ROOT
"""
import sys, os, json, re
root = sys.argv[1]


def acmp(p):
    out = {}
    for l in open(p):
        o = json.loads(l)
        if o.get('type') == 'acmp':
            tx = o['query'] == 'get_tx_state'
            k = (o['query'], o['talker'] if tx else o['listener'], o['talker_uid'] if tx else o['listener_uid'])
            out[k] = {x: y for x, y in o.items() if x not in ('t', 'controller')}
    return out


for a, b in (('bench-a200/bench/census-start.jsonl', 'bench-a200/bench/final/census-final.jsonl'),
             ('bench-a202/bench/census-start.jsonl', 'bench-a202/bench/final/census-end.jsonl')):
    A, B = acmp(os.path.join(root, a)), acmp(os.path.join(root, b))
    print(a.split('/')[0], 'ACMP states start/end', len(A), len(B), 'same set', set(A) == set(B),
          'conn_count values', sorted(set(v['conn_count'] for v in A.values()) | set(v['conn_count'] for v in B.values())))
    for k in sorted(A):
        if A[k] != B.get(k):
            print('   differs', k, {x: (A[k].get(x), B[k].get(x)) for x in A[k] if A[k].get(x) != B[k].get(x)})


def role(h):
    h = h.split('>')[-1]
    return 'power-strip host' if h.endswith('pi') else ('controller host' if h.endswith('pw1') else 'capture server')


txt = open(os.path.join(root, 'bench-a200/bench/hosts-clock-and-daemons.txt')).read()
hosts = re.findall(r'^== (\S+)\n(.*?)(?=^== |\Z)', txt, flags=re.M | re.S)
print('daemon check covered %d hosts:' % len(hosts))
for h, body in hosts:
    print('  ', role(h), '|', ' '.join(body.split()))
for h, off, rtt in re.findall(r'^(\S+) remote-minus-local_s=([0-9.-]+) rtt_s=([0-9.]+)', txt, flags=re.M):
    print('   build box behind the %s by %s s (rtt %s s)' % (role(h), off, rtt))
