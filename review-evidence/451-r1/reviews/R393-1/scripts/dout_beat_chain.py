#!/usr/bin/env python3
"""Split decode_dout.py clusters into the INTERNAL beat chain and the rest.
A cluster is on the chain if its start lies within 60 frames of
anchor + k*period for the best anchor, period 93,990.5 frames (10.64 ppm).
Usage: dout_beat_chain.py <decode_dout.json> [talker.jsonl]"""
import json, sys
d = json.load(open(sys.argv[1])); cl = d["cluster_list"]; P = 93990.6
best = None
for a in cl:
    on = [c for c in cl if abs(((c["start"] - a["start"]) / P) - round((c["start"] - a["start"]) / P)) * P < 60]
    if best is None or len(on) > len(best[1]): best = (a, on)
on = best[1]; off = [c for c in cl if c not in on]
sp = [b["start"] - a["start"] for a, b in zip(on, on[1:])]
def s(x, k): return sum(c[k] for c in x)
print(json.dumps({"clusters": len(cl), "beat_chain": len(on), "beat_repeated": s(on, "repeated"), "beat_dropped": s(on, "dropped"),
                  "beat_net_histogram": {str(n): sum(1 for c in on if c["net"] == n) for n in sorted(set(c["net"] for c in on))},
                  "beat_spacing_min": min(sp), "beat_spacing_max": max(sp),
                  "other_clusters": len(off), "other_repeated": s(off, "repeated"), "other_dropped": s(off, "dropped"),
                  "other_list": off}, indent=1))
