#!/usr/bin/env python3
"""Compare the start and end effective-state snapshots independently.

Usage: check_restore.py <evidence author dir>
Ignores only per-request bookkeeping (sequence, request/response/observed times).
Binding readbacks report a numeric status, 0 meaning success.
"""
import json
import sys

ev = sys.argv[1]
VOL = {"sequence", "request_ns", "response_ns", "observed_ns"}


def load(name):
    rows = [json.loads(l) for l in open(f"{ev}/{name}")]
    return [{k: v for k, v in r.items() if k not in VOL} for r in rows]


a, b = load("restore-start.jsonl"), load("restore-end.jsonl")
fails = 0
ok = len(a) == len(b) and all(x == y for x, y in zip(a, b))
print(f"CHECK {'PASS' if ok else 'FAIL'} start == end over {len(a)} rows (volatile fields ignored)")
fails += not ok
succ = [r for r in b if r.get("status") in ("SUCCESS", 0)]
inv = [r for r in b if r.get("category") == "inventory"]
binds = [r for r in b if r.get("category") == "binding"]
zero = all(r["connections"] == 0 and r["status"] == 0 for r in binds)
print(f"CHECK {'PASS' if zero else 'FAIL'} every binding readback status 0 with 0 connections")
fails += not zero
print(f"INFO end snapshot: SUCCESS observations {len(succ)}, inventory rows {len(inv)}, binding rows {len(binds)}")
print(f"INFO binding row example: {json.dumps(binds[0])[:300]}")
by = {}
for r in succ:
    by[(r["role"], r.get("category"))] = by.get((r["role"], r.get("category")), 0) + 1
print(f"INFO SUCCESS by role/category: {by}")
ok = len(succ) == 42 and len(inv) == 2 and len(binds) == 18
print(f"CHECK {'PASS' if ok else 'FAIL'} 42 observations, 2 inventories, 18 binding readbacks")
fails += not ok
print(f"RESULT fails={fails}")
sys.exit(1 if fails else 0)
