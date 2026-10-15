#!/usr/bin/env python3
"""Recompute B17's first burst per cycle from B17's late-PDU lists with the rule the B18 page states:
PDUs more than 20 us late, grouped while less than 1 ms apart. Prints s and peak, and B17's largest burst.

usage: python3 -I b17_bursts.py <b17_summary_dir>
"""
import json, sys
from pathlib import Path

allpk = []
for p in sorted(Path(sys.argv[1]).glob("c[0-9][0-9].json")):
    s = json.load(open(p))
    late = [x for x in s["tap"]["late_pdus"] if x["late_us"] > 20 and x["s"] > 0]
    bursts = []
    for x in late:
        if bursts and x["s"] - bursts[-1][-1]["s"] < 0.001:
            bursts[-1].append(x)
        else:
            bursts.append([x])
    pk = [max(y["late_us"] for y in b) for b in bursts]
    allpk += pk
    b = bursts[0]
    print(p.stem, "first burst s %.2f peak %.1f" % (b[0]["s"], max(y["late_us"] for y in b)),
          "n_bursts", len(bursts), "max peak %.3f" % max(pk))
print("B17 largest burst peak over all cycles %.3f" % max(allpk))
