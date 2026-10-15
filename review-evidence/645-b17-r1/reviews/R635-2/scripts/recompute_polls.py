#!/usr/bin/env python3
"""Independent recompute of B17 poll figures from raw cycles/cNN/{poll,events}.jsonl.
Usage: python3 -I recompute_polls.py <author-packet-dir>
Bind instant = events 'bind-time'.t_bind_local. Times relative to it, raw (unrounded)."""
import json, sys, os
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
root = sys.argv[1]
def ld(p): return [json.loads(l) for l in open(p)]
def w(p, k): return int(p['words'][k], 16)
prev_last = None
for c in range(1, 11):
    d = os.path.join(root, 'cycles', 'c%02d' % c)
    P = ld(os.path.join(d, 'poll.jsonl')); E = ld(os.path.join(d, 'events.jsonl'))
    tb = [e for e in E if e['kind'] == 'bind-time'][0]['t_bind_local']
    tu = [e for e in E if e['kind'] == 'unbind'][0]['t_cmd_local']
    slip = [w(p, '0x8d4') & 0xffff for p in P]
    skip = [w(p, '0x8d4') >> 16 for p in P]
    tdm = {w(p, '0x8d8') for p in P}
    ch = [i for i in range(1, len(P)) if slip[i] != slip[i-1]]
    r = {'cycle': 'c%02d' % c, 'polls': len(P),
         'first_t0': P[0]['t0'] - tb, 'last_t1': P[-1]['t1'] - tb, 'last_t0': P[-1]['t0'] - tb,
         'slip_first': slip[0], 'slip_last': slip[-1], 'skips': sorted(set(skip)), 'tdm': sorted(tdm),
         'changes': [(i, slip[i-1], slip[i], P[i-1]['t0'] - tb, P[i]['t1'] - tb) for i in ch],
         'continuity_ok': prev_last is None or slip[0] == prev_last}
    if ch:
        i = ch[-1]; r['left_after_slip'] = P[-1]['t1'] - P[i]['t1']
    # RENDER_STAT
    rs = [w(p, '0x8dc') for p in P]
    post = [i for i in range(len(P)) if P[i]['t0'] >= tb]
    i0 = post[0]
    ipf = next(i for i in post if not (rs[i] >> 8) & 1)
    icv = next(i for i in post if (rs[i] >> 9) & 1 and not (rs[i] >> 8) & 1)
    r['prefill0_poll_end'] = P[ipf]['t1'] - tb; r['prefill0_is_first_post'] = ipf == i0
    r['conv_poll_end'] = P[icv]['t1'] - tb; r['conv_lag_polls'] = icv - ipf
    r['fill_range_after'] = (min(rs[i] & 0xff for i in range(ipf, len(P))), max(rs[i] & 0xff for i in range(ipf, len(P))))
    r['held_to_last'] = all(not (rs[i] >> 8) & 1 and (rs[i] >> 9) & 1 for i in range(icv, len(P)))
    r['rails'] = sorted({x >> 16 for x in rs})
    r['servo_states'] = sorted({p['servo_state'] for p in P}); r['aafm'] = sorted({w(p, '0x8e0') for p in P})
    dur = sorted(((P[i]['t1'] - P[i]['t0']), i) for i in range(len(P)))
    r['long_polls'] = [(round(dd, 3), round(P[i]['t0'] - tu, 3), round(P[i]['t0'] - tb, 3)) for dd, i in dur[-2:]]
    r['max_other_dur'] = dur[-3][0]
    prev_last = slip[-1]
    print(json.dumps(r))
