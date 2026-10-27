#!/usr/bin/env python3
"""Compare r4_probe.py logs: per-case status and verdict, at the round-4 head and its parent against a new head.

Usage: python3 -I compare_r4_probe.py <log at 85da3e45> <log at 4d69e192> <log at the new head>

Prints, per group, the (old, new) status transitions against each earlier log; then every case whose
verdict changed against the round-4 head, with its DUT operations; then every case OK or INFO before
and DEVIATION now. Exit status 0.
"""
import collections
import json
import sys


def load(path: str) -> dict:
    out = {}
    for line in open(path, encoding="utf-8"):
        if line.startswith("SUMMARY"):
            continue
        name, status, rest = line.split(None, 2)
        out[name] = (status, json.loads(rest))
    return out


head, parent, new = (load(p) for p in sys.argv[1:4])
for label, old in (("round-4 head", head), ("its parent", parent)):
    moves = collections.Counter((k.split("-")[0], old[k][0], new[k][0]) for k in old)
    print(f"TRANSITIONS against {label}:")
    for key in sorted(moves):
        print("   ", key, moves[key])
print("VERDICT CHANGES against the round-4 head:")
for k in head:
    if head[k][1][0] != new[k][1][0]:
        ops = new[k][1][4] if k.startswith("R-") else k
        print("   ", k, head[k][1][0], "->", new[k][1][0], json.dumps(ops))
for label, old in (("round-4 head", head), ("its parent", parent)):
    worse = [k for k in old if old[k][0] in ("OK", "INFO") and new[k][0] == "DEVIATION"]
    print(f"DEVIATION now, OK or INFO at {label}:", worse)
    for k in worse:
        print("   ", k, json.dumps(new[k][1][:5])[:400])
