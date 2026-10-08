#!/usr/bin/env python3
"""Compare an author source inventory ({revision, files}) against an exported tree.
usage: verify_source_inventory.py INVENTORY_JSON TREE_DIR"""
import hashlib, json, os, sys
d = json.load(open(sys.argv[1])); tree = sys.argv[2]
files = d["files"]
entries = files.items() if isinstance(files, dict) else [(e.get("path") or e.get("file"), e) for e in files]
bad = n = 0
listed = set()
for path, e in entries:
    n += 1; listed.add(path)
    want = e if isinstance(e, str) else (e.get("sha256"))
    p = os.path.join(tree, path)
    got = hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None
    if got != want:
        bad += 1; print("MISMATCH", path)
on_disk = set()
for root, _, fs in os.walk(tree):
    for f in fs:
        on_disk.add(os.path.relpath(os.path.join(root, f), tree))
extra = sorted(on_disk - listed)
print(f"revision {d['revision']}: {n} listed, {bad} mismatches, {len(extra)} tree files not listed")
for x in extra[:10]: print("  unlisted:", x)
sys.exit(1 if bad else 0)
