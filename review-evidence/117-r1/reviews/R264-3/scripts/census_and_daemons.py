#!/usr/bin/env python3
"""A200 binding census before/after, the daemon check, and base-tree identifiers.

Usage: census_and_daemons.py PIN_ROOT CLONE BASE_REV
"""
import json, os, subprocess, sys

root, clone, base = sys.argv[1:4]


def acmp(p):
    return [json.loads(l) for l in open(p) if '"dmac"' in l]


a = acmp(os.path.join(root, "bench-a200/bench/census-start.jsonl"))
b = acmp(os.path.join(root, "bench-a200/bench/final/census-final.jsonl"))
key = lambda d: (d.get("query"), d.get("talker"), d.get("talker_uid"), d.get("listener"), d.get("listener_uid"))
A, B = {key(d): d for d in a}, {key(d): d for d in b}
ignore = {"t", "seq", "rtt_ms", "controller_eid", "controller", "argv"}
print(f"CENSUS states_before={len(A)} states_after={len(B)} same_keys={set(A) == set(B)} "
      f"conn_counts={sorted({d['conn_count'] for d in a + b})}")
for k in sorted(A, key=str):
    diff = {f: (A[k].get(f), B[k].get(f)) for f in set(A[k]) | set(B[k]) if f not in ignore and A[k].get(f) != B[k].get(f)}
    if diff:
        print(f"  DIFF {k} {diff}")
t = open(os.path.join(root, "bench-a200/bench/hosts-clock-and-daemons.txt"), encoding="utf-8").read()
print(f"DAEMONS hosts_checked={t.count('== ')} no_daemon_lines={t.count('no gPTP/AVB daemon process')}")
for ident in ("3cc0c6fffefe0210", "3cc0c6fffe010203", "3cc0c60102030000", "3cc0c6010203"):
    out = subprocess.run(["git", "-C", clone, "grep", "-il", ident, base], capture_output=True, text=True).stdout.split()
    print(f"BASE-TREE {ident} files={len(out)} {' '.join(sorted(o.split(':', 1)[1] for o in out))}")
