#!/usr/bin/env python3
"""Pair ACMP state rows of two census files by (query, entity, index) and list differing fields.

Usage: census_acmp_diff.py <start.jsonl> <end.jsonl>
"""
import json
import sys


def rows(path):
    out = {}
    argv = None
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("type") == "start":
            argv = r.get("argv")
        elif r.get("type") == "acmp" and argv:
            key = tuple(argv[2:])
            out[key] = {k: v for k, v in r.items() if k not in ("t", "seq")}
    return out


a, b = rows(sys.argv[1]), rows(sys.argv[2])
print("ACMP states: start", len(a), "end", len(b), "common", len(set(a) & set(b)))
unbound = sum(1 for k, v in b.items() if v.get("conn_count") == 0)
print("end states with conn_count 0:", unbound)
for k in sorted(set(a) & set(b)):
    d = {f: (a[k].get(f), b[k].get(f)) for f in set(a[k]) | set(b[k]) if a[k].get(f) != b[k].get(f)}
    if d:
        print("  differs", k, d)
