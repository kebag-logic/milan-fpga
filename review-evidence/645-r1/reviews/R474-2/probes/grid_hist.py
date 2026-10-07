#!/usr/bin/env python3
"""R474-2 probe P2: histogram of the aligner error (axis cycles) from a
follow_ring --grid-trace CSV (one sample per ms) over [a, b) seconds, with the
settle pending / recovery flags seen in that window."""
import csv, sys
from collections import Counter
path, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
h, pend, rec, eng, n = Counter(), 0, 0, 0, 0
with open(path) as f:
    for r in csv.DictReader(f):
        if None in r.values() or "" in r.values():
            continue
        t = float(r["t_s"])
        if not (a <= t < b):
            continue
        n += 1
        eng += int(r["mga_engaged"])
        if int(r["mga_engaged"]):
            h[int(r["mga_err_cyc"])] += 1
        pend += int(r["settle_pend"])
        rec += int(r["settle_recover"])
print(f"{path} [{a},{b}) samples {n} engaged {eng} settle_pend_samples {pend} settle_recover_samples {rec}")
print("  histogram", " ".join(f"{k}:{v}" for k, v in sorted(h.items())))
