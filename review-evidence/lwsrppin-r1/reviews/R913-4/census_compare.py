#!/usr/bin/env python3
"""Compare shard censuses (JSON list of shards, each a list of invocation identities) of a merge and its two parents.

Usage: python3 -I census_compare.py head.json first-parent.json second-parent.json
"""
import json, sys
load = lambda p: [i for s in json.load(open(p)) for i in s]
h, a, b = (load(p) for p in sys.argv[1:4])
H, A, B = set(h), set(a), set(b)
print(f"sizes head={len(h)} first={len(a)} second={len(b)} (unique {len(H)} {len(A)} {len(B)})")
print("head - second:", sorted(H - B))
print("second - head:", sorted(B - H))
print("first - head:", sorted(A - H))
print("first - second (pin-side or base-side differences):", len(A - B))
print("head - (first|second):", sorted(H - (A | B)))
