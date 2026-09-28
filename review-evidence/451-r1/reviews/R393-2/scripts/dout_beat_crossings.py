#!/usr/bin/env python3
"""Count INTERNAL-source beat crossings in the DOUT capture and locate the ones
that are not in the "beat" class of the archived cluster attribution.

Fits the beat phase and period to the attributed "beat" clusters by least
squares on (index, first_frame), enumerates every expected crossing inside the
capture, and reports which cluster (if any) contains each expected crossing
within +/-600 frames, with that cluster's class. Also re-sums every class row (dropped = skips plus,
for each ordinal step of size s listed under "other", s - 1 frames).
Usage: dout_beat_crossings.py <attribution.json>
"""
import json
import sys

import numpy as np

d = json.load(open(sys.argv[1]))
cl = d["clusters"]
n = d["summary"]["frames"]
beats = [c for c in cl if c["kind"] == "beat"]
f0 = beats[0]["first_frame"]
P0 = 93990.6
k = np.array([round((c["first_frame"] - f0) / P0) for c in beats])
f = np.array([c["first_frame"] for c in beats])
P, A = np.polyfit(k, f, 1)
exp = [A + i * P for i in range(-1, int(n / P) + 2) if 0 <= A + i * P < n]
hits = []
for e in exp:
    cont = [c for c in cl if c["first_frame"] - 600 <= e <= c["last_frame"] + 600]
    hits.append({"expected_frame": int(round(e)),
                 "clusters": [[c["first_frame"], c["last_frame"], c["kind"]] for c in cont]})
rows = {}
for c in cl:
    r = rows.setdefault(c["kind"], [0, 0, 0])
    r[0] += 1
    r[1] += c["repeats"]
    r[2] += c["skips"] + sum(o - 1 for o in c["other"])
print(json.dumps({
    "fitted_period_frames": round(float(P), 2), "fitted_phase_frame": round(float(A), 1),
    "expected_crossings_in_capture": len(exp),
    "crossings_in_beat_clusters": sum(1 for h in hits if any(x[2] == "beat" for x in h["clusters"])),
    "crossings_not_in_beat_class": [h for h in hits if not any(x[2] == "beat" for x in h["clusters"])],
    "beat_spacing_min_max": [int(np.diff(f).min()), int(np.diff(f)[np.diff(k) == 1].max())],
    "class_rows_count_repeated_dropped": rows,
    "summary": d["summary"],
}, indent=1))
