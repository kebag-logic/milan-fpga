#!/usr/bin/env python3
"""Check the page's capture-path claims against grade.json skip_clusters. Usage: capclaims.py <packet-author-dir>"""
import json, sys
ROOT = sys.argv[1]
small = []
out = {}
for c in ["a0", "a1", "a2", "b0", "bcrf", "baaf"]:
    g = json.load(open(f"{ROOT}/summary/{c}/grade.json"))
    ks = g["skip_clusters"]
    bases = sorted(set(k["basis"] for k in ks))
    mism = [k["cluster"] for k in ks if abs(k["read_rise_ms"] - k["lost_ms"]) > 1 + 0.02 * k["lost_ms"]]
    steps = [s for k in ks for s in k["steps"]]
    under98 = [k for k in ks if k["lost_frames"] < 98]
    small += [(c, k["cluster"], k["lost_frames"], k["read_rise_ms"], k["recent_read_gap_ms"]) for k in under98]
    out[c] = dict(clusters=len(ks), bases=bases, rise_mismatch=mism, not_capture=[k["cluster"] for k in ks if not k["capture_path"]],
                  smallest_cluster_loss=min(k["lost_frames"] for k in ks), smallest_positive_step=min(s for s in steps if s > 0),
                  steps_2_to_48=[s for s in steps if 2 <= abs(s) <= 48], negative_steps=[s for s in steps if s < 0],
                  under98=len(under98), loops_added=[(k["cluster"], k["whole_loops_added"]) for k in ks if k["whole_loops_added"]])
    print(c, json.dumps(out[c]))
print("clusters under 98 frames:", len(small), "rise range", min(x[3] for x in small), max(x[3] for x in small),
      "min gap", min(x[4] for x in small), "sizes", sorted(set(x[2] for x in small)))
