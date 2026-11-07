#!/usr/bin/env python3
"""Compare two pp_resource_baseline.json blobs: list every leaf path that differs.
Usage: git show A:syn/ooc/pp_resource_baseline.json > a.json; ... ; python3 -I baseline_delta.py a.json b.json"""
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
def walk(x, y, p=""):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            walk(x.get(k, "<absent>"), y.get(k, "<absent>"), f"{p}/{k}")
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for i, (u, v) in enumerate(zip(x, y)):
            walk(u, v, f"{p}[{i}]")
    elif x != y:
        print(p)
walk(a, b)
