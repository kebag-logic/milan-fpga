#!/usr/bin/env python3
"""Per cycle: every CLKV_STAT[3] (holdover) episode, with first-set/first-clear times and the GM at first set.

Usage: step3_holdover_episodes.py <evidence-root>
Times: seconds after the outlet-off command, build-box clock (see step3_rederive.py).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step3_rederive as s  # noqa: E402

root = sys.argv[1]
for c in range(1, 7):
    cdir = os.path.join(root, "bench-a202", "bench", f"cycle{c}")
    offs = s.offsets(cdir)
    off_pi = [v for h, v in offs.items() if h.endswith("pi")][0]
    t_off, t_on = s.strip_times(cdir)
    T0 = t_off - off_pi
    on = t_on - off_pi - T0
    con = [(ts - T0, f) for ts, f in s.console(cdir)]
    eps = []
    cur = None
    for t, f in con:
        h = int(f["CLKV_STAT"], 16) & 8
        if h and cur is None:
            cur = [t, 1, f["GPTP_GM"]]
        elif h:
            cur[1] += 1
        elif cur is not None:
            gm = "GM=self" if cur[2] == s.GM_SELF else ("GM=switch" if cur[2] == s.GM_SW else "GM=other")
            eps.append((cur[0], t, cur[1], gm))
            cur = None
    print(f"cycle {c}: holdover episodes")
    for a, b, n, gm in eps:
        print(f"   first set {a:6.2f}  first clear {b:6.2f}  samples {n}  span {b - a:.2f} s  {gm} at first set  {'before' if a < on else 'after'} the switch power-on")
