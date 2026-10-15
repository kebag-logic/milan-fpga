#!/usr/bin/env python3
"""Summarise follow_ring bind-sweep run logs: per-bind phase, primed margin, window, slips.

Usage: python3 -I summ_bind_sweep.py <sweep dir>
"""
import glob, os, re, sys
pat = re.compile(r"RESULT-645-BIND: B17 cycle (\d+) phase ([\d.]+) at INTERNAL: .*?primed margin ([\d.]+)\.\.([\d.]+) us "
                 r"\((\w+) .*?arms (\d+) .*?settle recentres (\d+) .*?render recentres (\d+), SLIP_LB \+(\d+) dups \+(\d+) skips, "
                 r"slipped frames (\d+) before the ring acts and (\d+) after")
runs = binds = 0; rcs = {}; inside = []; slipped = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], "bind_j*_p*.log"))):
    name = os.path.basename(f)[:-4]; runs += 1
    rc = open(f[:-4] + ".rc").read().strip() if os.path.exists(f[:-4] + ".rc") else "none"
    rcs[rc] = rcs.get(rc, 0) + 1
    for m in pat.finditer(open(f).read()):
        binds += 1
        c, ph, lo, hi, win, arms, st, rr, d, s, pre, post = m.groups()
        row = (name, int(c), float(ph), float(lo), float(hi), win, int(arms), int(st), int(rr), int(d), int(s), int(pre), int(post))
        if win == "inside": inside.append(row)
        if int(d) + int(s) > 0: slipped.append(row)
print(f"runs {runs} rc {rcs} binds {binds} inside {len(inside)} binds_with_SLIP_LB_change {len(slipped)}")
print("one arm/settle/render each:", sum(1 for f in [0]) and None)
for r in slipped:
    print("SLIP", r)
print("INSIDE-SLIPPED", [r[:2] for r in slipped if r[5] == "inside"])
print("POST-ACT-SLIPS", sum(r[12] for r in slipped))
