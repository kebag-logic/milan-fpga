#!/usr/bin/env python3
"""Check a service-budget receipt's build_hashes against the tracked files of
a checkout (the tracked-source subset only), and compare its timing rows with
another receipt.

usage: receipt_hashes_vs_tree.py <checkout> <receipt.json> [<other.json>]
"""
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
rec = json.load(open(sys.argv[2]))
checked = diff = 0
for path, digest in sorted(rec["build_hashes"].items()):
    f = root / path
    if path.startswith(("build/", "external/")) or not f.is_file():
        continue
    checked += 1
    got = hashlib.sha256(f.read_bytes()).hexdigest()
    if got != digest:
        diff += 1
        print(f"DIFFERENT {path}")
print(f"tracked build inputs checked {checked}, different {diff}")
if len(sys.argv) > 3:
    other = json.load(open(sys.argv[3]))
    print("rows equal to other receipt:", rec["rows"] == other["rows"])
    print("heartbeat equal:", rec["heartbeat"] == other["heartbeat"])
    print("liveness equal:", rec["liveness"] == other["liveness"])
    print("budget_findings equal:", rec["budget_findings"] == other["budget_findings"])
    print("media slots equal:", rec["media"]["slots_sha256"] == other["media"]["slots_sha256"])
sys.exit(1 if diff else 0)
