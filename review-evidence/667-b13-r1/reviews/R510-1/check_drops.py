#!/usr/bin/env python3
"""Count capture receipts by their kernel-drop statement.

Usage: check_drops.py <evidence author dir>
"""
import collections
import glob
import json
import os
import re
import sys

ev = sys.argv[1]
for kind in ("soak", "start"):
    c = collections.Counter()
    missing = []
    for f in sorted(glob.glob(f"{ev}/667-b13-{kind}-*-*.pcap.json")):
        lines = json.load(open(f))["summary"]
        m = [re.match(r"^(\d+) packets dropped by kernel$", l) for l in lines]
        m = [x for x in m if x]
        if not m:
            missing.append(os.path.basename(f))
            c["no drop statement"] += 1
        else:
            c[f"dropped={m[0].group(1)}"] += 1
    print(f"INFO {kind}: {dict(c)} missing={missing}")
