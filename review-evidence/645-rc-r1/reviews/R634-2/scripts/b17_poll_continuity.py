#!/usr/bin/env python3
"""Which B17 later bursts a SLIP_LB read observed: within the cycle's own polls, or
only through the next cycle's first read (counter continuity, stream still bound),
or by no read in the summaries. usage: b17_poll_continuity.py <summary dir>"""
import glob, json, os, sys
TICK = 1e6 / 48000.0
cs = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(sys.argv[1], 'c[0-9][0-9].json')))]
for i, d in enumerate(cs):
    s = d['poll']['slips'][0]; lastp = d['poll']['last_poll_s']; lp = d['tap']['late_pdus']
    post = [p for p in lp if p['s'] > s['s_hi']]
    unobs = [p for p in post if p['s'] >= lastp]
    line = f"{d['cycle']}: last poll {lastp:.3f} s, SLIP_LB last {d['poll']['slip_lb_last']['dups']}; listed later PDUs after it: {len(unobs)}"
    if unobs:
        line += f" (peak {max(p['late_us'] for p in unobs):.3f} us, {unobs[0]['s']:.3f}..{unobs[-1]['s']:.3f} s)"
    if i + 1 < len(cs):
        n = cs[i + 1]
        nfirst = n['bind_local'] + n['poll']['first_poll_s'] - d['bind_local']
        nunbind = n['unbind_local'] - d['bind_local']
        cont = n['poll']['slip_lb_first'] == d['poll']['slip_lb_last']
        line += (f"; next first read {n['cycle']} at {nfirst:.3f} s from this bind, value {n['poll']['slip_lb_first']['dups']} "
                 f"({'continuous' if cont else 'CHANGED'}), next unbind at {nunbind:.3f} s; "
                 f"covers all listed PDUs: {all(p['s'] < nfirst for p in lp) and nfirst < nunbind}")
    else:
        line += '; no next cycle: unobserved by any summary read' if unobs else ''
    print(line)
