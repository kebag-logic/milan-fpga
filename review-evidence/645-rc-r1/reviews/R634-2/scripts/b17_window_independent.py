#!/usr/bin/env python3
"""Independent derivation of the primed-margin window from B17's cNN.json.

Upper bound per cycle: the slip record's own tap_lateness_max_us over the slip
interval (no burst grouping). Lower bound per cycle: the maximum late_us of any
listed PDU after the slip interval, minus one 48 kHz tick. Also reports listed
PDUs before the slip interval and the number of distinct bursts (5 ms and
50 ms grouping) inside the slip interval, and the bounds' sensitivity.
usage: b17_window_independent.py <summary dir>
"""
import glob, json, os, sys
TICK = 1e6 / 48000.0
rows = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'c[0-9][0-9].json'))):
    d = json.load(open(f))
    s = d['poll']['slips']
    assert len(s) == 1, (f, len(s))
    s = s[0]
    lp = d['tap']['late_pdus']
    pre = [p for p in lp if p['s'] < s['s_lo']]
    inn = [p for p in lp if s['s_lo'] <= p['s'] <= s['s_hi']]
    post = [p for p in lp if p['s'] > s['s_hi']]
    def nb(ps, gap):
        n, last = 0, None
        for p in ps:
            if last is None or p['s'] - last >= gap: n += 1
            last = p['s']
        return n
    hi_tap = s['tap_lateness_max_us']
    hi_list = max(p['late_us'] for p in inn)
    lo = max(p['late_us'] for p in post) - TICK
    rows.append((d['cycle'], s['dups'], s['skips'], len(pre), nb(inn, .005), nb(inn, .05), hi_tap, hi_list, lo,
                 max(p['s'] for p in post), d['poll']['last_poll_s']))
print('cycle dups skips pre_listed bursts_in_slip(5ms,50ms) hi_tap hi_list lo(later-1tick) last_later_s last_poll_s')
for r in rows:
    print('%s %d %d %d %d %d %.3f %.3f %.3f %.3f %.3f' % r)
lo = max(r[8] for r in rows); hi = min(r[6] for r in rows)
print('tick %.6f us; window %.3f .. %.3f us' % (TICK, lo, hi))
print('lo from', [r[0] for r in rows if r[8] == lo], 'hi from', [r[0] for r in rows if r[6] == hi])
oth = [r for r in rows if r[0] != 'c05']
print('others lo %.3f..%.3f hi %.3f..%.3f' % (min(r[8] for r in oth), max(r[8] for r in oth), min(r[6] for r in oth), max(r[6] for r in oth)))
print('all contain window:', all(r[8] <= lo and r[6] >= hi for r in rows))
