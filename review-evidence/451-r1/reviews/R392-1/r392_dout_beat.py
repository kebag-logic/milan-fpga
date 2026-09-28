#!/usr/bin/env python3
"""Reviewer probe: DOUT 70 s clusters, beat membership by 93,990-frame chaining.

A cluster is beat-class when some other cluster lies an integer number m>=1
of beat periods away (93,985..93,995 frames per period, m <= 3). Totals of
the beat class and of the remainder are printed for comparison with the page.
"""
import json, sys
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__file__))
from r392_decode import continuity
w = np.fromfile(sys.argv[1], dtype="<u4").reshape(-1, 8)
a = 2048
ordv = ((w[a:, 0] >> 8) & 0xFFFF)
cl = continuity(ordv)["clusters"]
fr = [c["first"] + a + 1 for c in cl]
beat = set()
for i, fi in enumerate(fr):
    for j, fj in enumerate(fr):
        if i == j:
            continue
        d = abs(fj - fi)
        for m in (1, 2, 3):
            if 93985 * m <= d <= 93995 * m:
                beat.add(i)
b = [cl[i] for i in sorted(beat)]
o = [c for i, c in enumerate(cl) if i not in beat]
sp = np.diff([fr[i] for i in sorted(beat)])
out = {
    "clusters": len(cl),
    "beat_class": {"n": len(b), "repeated": sum(c["repeated"] for c in b), "dropped": sum(c["dropped"] for c in b),
                   "net_hist": {str(k): v for k, v in zip(*np.unique([c["repeated"] - c["dropped"] for c in b], return_counts=True))} if b else {},
                   "adjacent_spacings": sorted(set(int(x) for x in sp))},
    "other": {"n": len(o), "repeated": sum(c["repeated"] for c in o), "dropped": sum(c["dropped"] for c in o)},
}
json.dump(out, sys.stdout, indent=1, default=int); print()
