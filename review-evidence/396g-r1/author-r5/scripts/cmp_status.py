#!/usr/bin/env python3
"""Compare per-case status between two probe logs: <parent> <head>; prints regressions/improvements."""
import sys, collections
def load(p):
    out = {}
    for l in open(p):
        parts = l.split(None, 2)
        if len(parts) >= 2 and not l.startswith("SUMMARY"):
            out[parts[0]] = parts[1]
    return out
a, b = load(sys.argv[1]), load(sys.argv[2])
reg = [k for k in a if k in b and a[k] == "OK" and b[k] != "OK"]
imp = [k for k in a if k in b and a[k] != "OK" and b[k] == "OK"]
both = [k for k in a if k in b and a[k] != "OK" and b[k] != "OK"]
print("cases", len(a), "regressed", len(reg), "improved", len(imp), "deviating at both", len(both))
for k in reg[: int(sys.argv[3]) if len(sys.argv) > 3 else 60]:
    print("REGRESSED", k, a[k], "->", b[k])
