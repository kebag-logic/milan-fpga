#!/usr/bin/env python3
"""Reviewer probe: can the floor test see a capture-path loss AT the real clusters?

usage: plant_probe.py <round1_author_dir> <read_record.u16>

For each cluster of 2-to-59-frame skips away from any stall, add the cluster's
skipped frames to the delivery deficit from the read before its first skip
(a loss inside the capture path after sampling), and recompute the floor step.
If the test could not see such a loss at these positions, the page's "no
capture-path loss of their size" would rest on nothing. Also reports the
3-frame band of the unplanted 'no step' clusters.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

FS, PER = 48000, 480


def step(D, a, b, R, w=10, gb=3, ga=2):
    lo, hi = a - gb - w, b + ga + w
    if lo < 0 or hi > R:
        return None
    return float(D[b + ga:hi + 1].min() - D[lo:a - gb + 1].min())


pkt, rec = Path(sys.argv[1]), sys.argv[2]
s = json.load(open(pkt / "summary/a-long/summary.json"))["continuity"]
c0 = s["window"][0]
gap = np.fromfile(rec, dtype="<u2").astype(np.int64)
R = len(gap)
D = np.concatenate(([0], np.cumsum(gap))) / 1e6 * FS - PER * np.arange(R + 1)
g = np.concatenate(([np.nan], gap / 1000.0))
multi = []
for row in csv.DictReader(open(pkt / "summary/a-long/continuity-events.csv")):
    if row["kind"] == "skip" and int(row["frames"]) >= 2:
        multi.append(dict(r=(int(row["frame"]) - c0) // PER + 1, n=int(row["frames"])))
multi.sort(key=lambda e: e["r"])
cl = []
for e in multi:
    if cl and e["r"] - cl[-1][-1]["r"] < 16:
        cl[-1].append(e)
    else:
        cl.append([e])
B = [c for c in cl if all(e["n"] < 60 for e in c)]
print(f"small-only clusters {len(B)}; any stall within: {sum(bool(np.any(g[max(1, c[0]['r'] - 2):c[-1]['r'] + 1] > 15)) for c in B)}")
det, err, base = 0, [], []
for c in B:
    a, b = c[0]["r"], c[-1]["r"]
    f = sum(e["n"] for e in c)
    s0 = step(D, a, b, R)
    base.append(s0)
    Dp = D.copy()
    Dp[a - 1:] += f
    s1 = step(Dp, a, b, R)
    err.append(s1 - s0 - f)
    det += abs(s1 - f) <= 4 or (abs(s1 - s0 - f) <= 4 and abs(s0) > 4)
base = np.array(base)
print(f"planted loss = cluster frames: step rises by the planted frames within 4 at "
      f"{sum(abs(x) <= 4 for x in err)} of {len(B)}; classified 'step = skip frames' (or step on step) at {det}")
nostep = base[np.abs(base) <= 4]
print(f"unplanted: |step| <= 4 at {len(nostep)}, max |step| among them {np.abs(nostep).max():.2f}")
