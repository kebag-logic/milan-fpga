#!/usr/bin/env python3
"""Independent recompute of B17 after-slip burst windows.
Usage: python3 -I recompute_bursts.py <author-packet-dir> <recompute-polls.jsonl>
Bursts: late_pdus (summary/cNN.json tap) with late_us > 20, grouped while successive
>20us PDUs are < 0.5 ms apart (4 PDU periods; a different gap than the tool's 1 ms,
to test sensitivity). Windows: last poll end (raw), 32.0 s hold, capture end."""
import json, sys, os
root, pr = sys.argv[1], sys.argv[2]
polls = {json.loads(l)['cycle']: json.loads(l) for l in open(pr)}
for gap in (0.5e-3, 1e-3, 5e-3):
  agg = {}
  for c in sorted(polls):
    P = polls[c]
    tap = json.load(open(os.path.join(root, 'summary', c + '.json')))['tap']
    L = tap['late_pdus']
    B = []
    for x in L:
        if x['late_us'] <= 20: continue
        if B and x['s'] - B[-1]['e'] < gap: B[-1]['e'] = x['s']; B[-1]['pk'] = max(B[-1]['pk'], x['late_us']); B[-1]['n'] += 1
        else: B.append(dict(s=x['s'], e=x['s'], pk=x['late_us'], n=1))
    lo, hi = P['changes'][0][3], P['changes'][0][4]
    last = P['last_t1']
    inside = [b for b in B if lo <= b['s'] <= hi]
    before10 = [x for x in L if x['s'] < lo and x['s'] > 0 and x['late_us'] > 10]
    r = dict(cycle=c, gap_ms=gap*1e3, min_late_listed=min(x['late_us'] for x in L),
             all_to_last=sum(b['s'] <= last for b in B), all_to_hold=sum(b['s'] <= 32.0 for b in B), all_cap=len(B),
             inside=len(inside), first_inside=bool(inside) and B[0] is inside[0], slip_peak=inside[0]['pk'] if inside else None,
             max_late_in_interval=max([x['late_us'] for x in L if lo <= x['s'] <= hi], default=None),
             before10=len(before10), pdus=(min(b['n'] for b in B), max(b['n'] for b in B)))
    for wn, end in (('last', last), ('hold', 32.0), ('cap', 1e9)):
        a = [b for b in B if hi < b['s'] <= end]
        r['after_' + wn] = (len(a), max((b['pk'] for b in a), default=None), any(b['pk'] > r['slip_peak'] for b in a))
    near = [round(b['s'] - t, 4) for b in B for t in (lo, hi, last, 32.0) if abs(b['s'] - t) < 0.05]
    r['near_boundary_50ms'] = near
    print(json.dumps(r))
    for k in ('all_to_last', 'all_cap', 'after_last', 'after_cap'):
        agg.setdefault(k, []).append(r[k][0] if isinstance(r[k], (list, tuple)) else r[k])
    for k in ('after_last', 'after_cap'):
        agg.setdefault(k + '_pk', []).append(r[k][1])
    agg.setdefault('slip_int_max', []).append(r['max_late_in_interval'])
    agg.setdefault('larger_last', []).append(r['after_last'][2])
    agg.setdefault('further', []).append(r['after_cap'][0] - r['after_last'][0])
    agg.setdefault('pdus', []).extend(r['pdus'])
  print('AGG gap_ms=%.1f' % (gap*1e3), json.dumps({k: (min(v), max(v)) if k != 'larger_last' else sum(v) for k, v in agg.items()}))
