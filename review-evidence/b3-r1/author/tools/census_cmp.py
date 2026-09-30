#!/usr/bin/env python3
"""Compare two AVDECC census files (avdecc_rw.py census output), ignoring
per-exchange fields (timestamps, sequence ids, round-trip times).

usage: census_cmp.py <a.jsonl> <b.jsonl>
"""
import json
import sys

VOLATILE = {"t", "seq", "rtt_ms", "sequence_id"}


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in VOLATILE}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


def load(path):
    rows = []
    for line in open(path):
        try:
            rows.append(strip(json.loads(line)))
        except ValueError:
            continue
    return rows


a, b = load(sys.argv[1]), load(sys.argv[2])
print(json.dumps(dict(a_entries=len(a), b_entries=len(b))))
same = 0
for i, (x, y) in enumerate(zip(a, b)):
    if x == y:
        same += 1
    else:
        print(json.dumps(dict(index=i, a=x, b=y)))
print(json.dumps(dict(same=same, compared=min(len(a), len(b)))))
