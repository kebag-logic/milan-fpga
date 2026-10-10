#!/usr/bin/env python3
"""Print selected soak counter deltas from soak/summary.json.

Usage: soak_counters.py <packet-author-dir>
"""
import json, sys
from pathlib import Path

s = json.load(open(Path(sys.argv[1]) / "soak" / "summary.json"))
print("top-level keys:", sorted(s))
for key, d in s["counter_deltas_first_to_last_poll"].items():
    c = d.get("counters", {})
    sel = {n: (v.get("at_first_poll"), v.get("delta")) for n, v in c.items()
           if n.startswith("FRAMES") or n in ("STREAM_START", "STREAM_STOP", "TIMESTAMP_VALID")}
    print(key, d.get("valid_mask"), d.get("status"), sel)
