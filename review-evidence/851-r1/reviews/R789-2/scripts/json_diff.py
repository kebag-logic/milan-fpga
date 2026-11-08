#!/usr/bin/env python3
"""json_diff.py A B: list every leaf path whose value differs between two JSON files."""
import json, sys
def walk(a, b, p=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a: print(f"ADDED   {p}/{k}")
            elif k not in b: print(f"REMOVED {p}/{k}")
            else: walk(a[k], b[k], f"{p}/{k}")
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)): walk(x, y, f"{p}[{i}]")
    elif a != b:
        s = lambda v: (json.dumps(v)[:70])
        print(f"CHANGED {p}: {s(a)} -> {s(b)}")
walk(json.load(open(sys.argv[1])), json.load(open(sys.argv[2])))
