#!/usr/bin/env python3
"""For each B17 cycle: when the largest post-slip listed PDU came, against the
SLIP_LB poll span, and the lower bound using only PDUs a later poll observed.
usage: b17_later_burst_observed.py <summary dir>
"""
import glob, json, os, sys
TICK = 1e6 / 48000.0
print('cycle max_later_us at_s last_poll_s observed? | max_later_observed_us at_s lo_observed | first/last tap s | unbind_s')
rows = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'c[0-9][0-9].json'))):
    d = json.load(open(f)); s = d['poll']['slips'][0]; lp = d['tap']['late_pdus']
    lastp = d['poll']['last_poll_s']
    post = [p for p in lp if p['s'] > s['s_hi']]
    m = max(post, key=lambda p: p['late_us'])
    obs = [p for p in post if p['s'] < lastp]
    mo = max(obs, key=lambda p: p['late_us'])
    rows.append((d['cycle'], mo['late_us'] - TICK))
    print('%s %.3f %.3f %.3f %s | %.3f %.3f %.3f | %.3f %.3f | %s' % (d['cycle'], m['late_us'], m['s'], lastp, m['s'] < lastp,
          mo['late_us'], mo['s'], mo['late_us'] - TICK, lp[0]['s'], lp[-1]['s'], d['poll'].get('unbind_s')))
lo = max(r[1] for r in rows)
print('observed-only lower bound %.3f us from %s' % (lo, [r[0] for r in rows if r[1] == lo]))
