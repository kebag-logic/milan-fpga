#!/usr/bin/env python3
"""Compare two census JSONL receipts entry by entry, ignoring timing fields.

usage: census_compare.py <a.jsonl> <b.jsonl>
"""
import json, sys

IGN = {"t", "t_tx", "t_rx", "rtt_ms", "seq"}


def load(p):
    out = []
    for l in open(p):
        d = json.loads(l)
        if d.get("type") == "start":
            continue
        out.append({k: v for k, v in d.items() if k not in IGN})
    return out


a, b = load(sys.argv[1]), load(sys.argv[2])
print("entries", len(a), len(b))
print("what:", [x.get("what") for x in a])
same = 0
for x, y in zip(a, b):
    if x == y:
        same += 1
    else:
        print("DIFF", x.get("what"), x.get("payload", "")[:120], "|", y.get("payload", "")[:120])
print(f"same {same} of {min(len(a), len(b))}")
