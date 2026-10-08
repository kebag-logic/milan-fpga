#!/usr/bin/env python3
"""Compare two notify_mutants.py results.json files arm by arm.
usage: compare_campaign.py BASE_RESULTS HEAD_RESULTS"""
import json, sys
base = {r["mutant"]: r for r in json.load(open(sys.argv[1]))}
head = {r["mutant"]: r for r in json.load(open(sys.argv[2]))}
bad = 0
for name in sorted(set(base) | set(head)):
    b, h = base.get(name), head.get(name)
    bv = b["verdict"] if b else "-"
    hv = h["verdict"] if h else "-"
    same = b is not None and h is not None and b.get("failing_checks") == h.get("failing_checks")
    if hv not in ("PASS", "KILLED"):
        bad += 1
    print(f"{name:42s} base={bv:8s} head={hv:8s} "
          f"records={'identical' if same else ('head-only' if b is None else 'DIFFER')} "
          f"head_fails={len(h.get('failing_checks', [])) if h else '-'}")
print(f"arms at head: {sum(1 for n in head if not n.startswith('golden'))}, not PASS/KILLED: {bad}")
sys.exit(1 if bad else 0)
