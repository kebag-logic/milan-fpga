#!/usr/bin/env python3
"""Recount the 06:22 and 08:23 inventory snapshots row by row, by category.

usage: inventory_rows.py <snapshot-prebind.jsonl> <snapshot-final.jsonl>
"""
import json
import sys
from collections import Counter


def rows(path):
    out = {}
    for line in open(path):
        d = json.loads(line)
        cat = d["category"]
        if cat == "inventory":
            key, val = (d["role"], cat), d["counts"]
        elif cat == "format":
            key, val = (d["role"], cat, d["descriptor_type"], d["descriptor_index"]), d["value"]
        elif cat == "binding":
            key, val = (d["role"], cat, d["descriptor_type"], d["descriptor_index"]), (d["status"], d["connections"])
        elif cat == "clock":
            key, val = (d["role"], cat), d["value"]
        elif cat == "map":
            key, val = (d["role"], cat, d["descriptor_type"]), (d["mapping_count"], d["effective_sha256"])
        else:
            raise SystemExit(f"unknown category {cat}")
        assert key not in out, key
        out[key] = val
    return out


a, b = rows(sys.argv[1]), rows(sys.argv[2])
assert a.keys() == b.keys()
eq = sum(a[k] == b[k] for k in a)
print(f"rows {len(a)} equal {eq}")
print("by category:", dict(Counter(k[1] for k in a)))
for k in a:
    if a[k] != b[k]:
        print("DIFFER", k, a[k], b[k])
