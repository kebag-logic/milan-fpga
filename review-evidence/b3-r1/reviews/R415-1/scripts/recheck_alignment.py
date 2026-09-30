#!/usr/bin/env python3
"""Re-run attribute_dout.py's late-PDU matching for alignment multiples 0..12
from public data only: the cluster list in runs/dout-long/attribution.json
(first_ordinal_unwrapped, kind) and the talker's late-PDU log.
usage: recheck_alignment.py <packet-author-dir>"""
import json, os, sys
d = sys.argv[1]
cl = json.load(open(os.path.join(d, "runs/dout-long/attribution.json")))["clusters"]
under = [c for c in cl if c["kind"] != "beat"]
late = []
for line in open(os.path.join(d, "runs/dout-long/talker.jsonl")):
    if line.startswith("{"):
        o = json.loads(line)
        if o.get("kind") == "late-pdus":
            late += [(n * 6, lat) for n, _, lat in o["entries"]]
win = lambda n, lf: -60 <= n - lf <= 2880
print(f"underrun clusters {len(under)}, late PDUs logged {len(late)}")
for m in range(0, 13):
    off = m * 0x10000
    k = sum(1 for c in under if any(win(c["first_ordinal_unwrapped"] + off, lf) for lf, _ in late))
    print(f"multiple {m:2d}: underrun clusters matched {k}")
