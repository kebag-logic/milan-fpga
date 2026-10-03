#!/usr/bin/env python3
"""How plausible is the strict reading of the five off-signature capture clusters?

usage: attribution_bound.py <path to review-evidence/629-b7-r1/author>

Under the strict reading each frame a cluster is short of 48 n + 12 is one listener repeat
merged with the capture loss. The listener's event rate is then bounded by the same window's
visible audio, which holds no listener event. With a flat prior on a Poisson rate and 0
events in V seconds, the posterior predictive chance of at least k events in an interval of
L seconds is (L / (V + L)) ** k. The product over a case's clusters bounds the strict reading.
A0's off-signature cluster is the control: there the listener events are measured, so the
expected number inside the cluster follows from their rate; it shows the capture path alone
departs from the signature. Read-only.
"""
import json, sys
root = sys.argv[1]
out = {}
for c in ("a0", "a2", "baaf"):
    g = json.load(open(f"{root}/summary/{c}/grade.json"))
    V = g["window"]["seconds"]
    rows, p = [], 1.0
    for x in g["skip_clusters"]:
        nsk = max(1, sum(1 for s in x["steps"] if s > 0))
        r = (x["lost_frames"] - 12 * nsk) % 48
        if r:
            short = 48 - r
            L = x["lost_ms"] / 1000.0
            pk = (L / (V + L)) ** short if not g["attribution"].get("listener", {}).get("events", 0) else None
            p *= pk if pk is not None else 1.0
            rows.append(dict(cluster=x["cluster"], lost_frames=x["lost_frames"], lost_s=round(L, 4), short_by=short,
                             p_at_least_short_by_events=pk))
    lst = g["attribution"].get("listener", {}).get("events", 0)
    out[c] = dict(visible_s=V, listener_events_visible=lst, off_signature=rows,
                  strict_reading_joint_bound=p if lst == 0 else None,
                  expected_listener_events_in_cluster=[round(lst / V * r["lost_s"], 4) for r in rows] if lst else None)
print(json.dumps(out, indent=1))
