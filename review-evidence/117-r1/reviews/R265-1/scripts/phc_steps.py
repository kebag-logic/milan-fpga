#!/usr/bin/env python3
"""Observation 7 check: PHC step at each return vs the interval between
successive switch power-on commands (power-strip host clock).

Usage: phc_steps.py <bench-a202 dir>
Step = (TAI_NS jump between the two console samples bracketing the largest
discontinuity after the return) minus the console time between them.
The previous power-on for cycle 1 is attempt 1's guard "on" (first ON_RC).
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import condec, step3

base = sys.argv[1]
ons = {}
txt = open(os.path.join(base, "bench/attempt1-aborted/lock.txt")).read()
m = re.search(r"turning it back on now\n([0-9.]+)", txt)
ons[0] = float(m.group(1))
for n in range(1, 7):
    ons[n] = step3.powerstrip(os.path.join(base, "bench", f"cycle{n}"))["T_ON_CMD"]
for n in range(1, 7):
    cdir = os.path.join(base, "bench", f"cycle{n}")
    con = condec.parse(os.path.join(cdir, "console.txt"))
    S = [(r["t"], int(r["fields"]["TAI_NS"], 16)) for r in con if r["cmd"] == "milan_status" and "TAI_NS" in r.get("fields", {})]
    jumps = [((b[1] - a[1]) / 1e9 - (b[0] - a[0]), a[0], b[0]) for a, b in zip(S, S[1:])]
    big = min(jumps)
    pre = [x for x in S if x[0] < big[1] - 30]
    print(f"cycle {n}: largest negative PHC step {big[0]:.2f} s; on-to-on interval {ons[n] - ons[n - 1]:.2f} s; "
          f"difference {big[0] + (ons[n] - ons[n - 1]):+.3f} s; PHC before off ~{S[0][1] / 1e9:.1f} s")
