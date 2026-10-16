#!/usr/bin/env python3
"""Box 3 edge containment when each console sample's placed time (its PHC read)
is moved back by the UART print time between the CSR reads and the PHC read
(milan_status_handler prints two lines, measured 271 bytes, before gettime_ns;
115200 baud 8N1 gives 23.5 ms, less a FIFO of up to 16 bytes, 1.4 ms).
Usage: check_skew.py <author-dir>"""
import json, os, sys
auth = sys.argv[1]
SKEWS = (0.0, 0.020, 0.022, 0.0235)
def edges(c):
    d = json.load(open(os.path.join(auth, 'bench', 'cycle%02d' % c, 'correlation.json')))
    E, W = d['edges'], d['wire']
    pick = lambda k, to, i: [x for x in E[k] if str(x['to']) == str(to)][i]
    ann = [a[0] for a in W['switch_announces_after_return']]
    gsw = pick('gm', '3cc0c6fffefe0210', -1)
    acc = [a for a in ann if a <= gsw['first_after']][-1]
    out = [('sync loss: last Sync + 0.375 s', pick('sync', 0, 0), W['switch_last_sync'] + 0.375),
           ('GM loss: last Announce + 3 s', pick('gm', '020000fffe000001', 0), W['switch_last_announce'] + 3.0),
           ('asCapable return: 2nd completed exchange', pick('asCapable', 1, -1), W['dut_completed_pdelay_after_return'][1]),
           ('GM return: accepted Announce', gsw, acc)]
    for x in d.get('crf_tu_vs_csr', []):
        if x['wire']['to'] == 1:
            out.append(('first tu=1 CRF PDU in CSR tu rise', x['csr'], x['wire']['first_after']))
    return out
print('skew (s) applied to every placed console sample:', SKEWS)
outside = {s: [] for s in SKEWS}
for c in range(1, 7):
    for name, e, cause in edges(c):
        row = []
        for s in SKEWS:
            lo, hi = e['last_before'] - s, e['first_after'] - s
            ok = lo <= cause <= hi
            row.append('%s(%+.1f/%+.1f ms)' % ('in ' if ok else 'OUT', (cause - lo) * 1e3, (hi - cause) * 1e3))
            if not ok: outside[s].append((c, name))
        print('cycle %d %-42s' % (c, name), ' '.join(row))
for s in SKEWS:
    print('skew %.4f s: edges outside their interval: %d %s' % (s, len(outside[s]), outside[s]))
