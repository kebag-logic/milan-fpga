#!/usr/bin/env python3
"""Reference-peer controller view per step 3 cycle, from the watcher logs.
usage: peer_view.py <archive-root>. Times: seconds after the outlet-off command, build-box clock."""
import json, os, re, sys
root = os.path.join(sys.argv[1], 'bench-a202', 'bench')
PEER = '3cc0c60102030000'; PEER_CLK = '3cc0c6fffe010203'; SW = '3cc0c6fffefe0210'
for n in range(1, 7):
    d = os.path.join(root, f'cycle{n}')
    off = {}
    for fn in ('clock-before.jsonl', 'clock-after.jsonl'):
        for ln in open(os.path.join(d, fn)):
            j = json.loads(ln); off.setdefault(j['host'].split('>')[-1], []).append(j['offset_s_median_best5'])
    off = {h: sum(v) / len(v) for h, v in off.items()}
    ps = {}
    for ln in open(os.path.join(d, 'powerstrip.txt')):
        m = re.match(r'(?:\w+=\d+ )?(T_\w+) ([0-9.]+)', ln.strip())
        if m: ps[m.group(1)] = float(m.group(2))
    T0 = ps['T_OFF_CMD'] - off['pi']
    W = [json.loads(l) for l in open(os.path.join(d, 'pw1-watch.jsonl'))]
    rel = lambda w: round(w['t'] - off['pw1'] - T0, 2)
    info = [(rel(w), w.get('status'), (w.get('decoded') or {}).get('gm'), (w.get('decoded') or {}).get('as_capable'))
            for w in W if w.get('what') == 'avb_info' and w.get('target') == PEER]
    after = [x for x in info if x[0] > 30 and x[1] == 'SUCCESS']
    first = after[0] if after else None
    names_sw = next((x[0] for x in after if x[2] == SW), None)
    adp = [(rel(w), w) for w in W if w.get('type') == 'adp' and (w.get('entity_id') or w.get('eid') or '').endswith(PEER[-6:])]
    adp_gm = [(t, w.get('gm') or w.get('gptp_gm') or w.get('gptp_grandmaster_id')) for t, w in adp]
    adp_self = [t for t, g in adp_gm if g == PEER_CLK and t > 30]
    adp_sw = next((t for t, g in adp_gm if g == SW and t > 30), None)
    cnt = [(rel(w), (w.get('decoded') or {}).get('c', {})) for w in W if w.get('what') == 'counters' and w.get('target') == PEER]
    cnt = [c for c in cnt if c[1]]
    gmc = (cnt[-1][1].get('5', 0) - cnt[0][1].get('5', 0)) if cnt else None
    avail = [(rel(w), w.get('available_index')) for w in W if w.get('type') == 'adp' and (w.get('entity_id') or w.get('eid') or '').endswith(PEER[-6:])]
    print(f'cycle {n}: first reachable peer poll {first}; names switch at {names_sw}; ADP self after return {adp_self[:3]}; ADP switch at {adp_sw}; GPTP_GM_CHANGED delta {gmc}; ADP avail {avail[0][1] if avail else None}->{avail[-1][1] if avail else None}')
