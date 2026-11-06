#!/usr/bin/env python3
"""Check an extracted evidence tree against its MANIFEST.json.

usage: manifest_check.py <evidence directory holding MANIFEST.json>
"""
import hashlib, json, os, sys
root = sys.argv[1]
entries = json.load(open(os.path.join(root, "MANIFEST.json")))
ok = bad = missing = 0
for entry in entries:
    path = os.path.join(root, entry["file"])
    if not os.path.exists(path):
        missing += 1
        continue
    digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
    ok, bad = (ok + 1, bad) if digest == entry["published_sha256"] else (ok, bad + 1)
listed = {entry["file"] for entry in entries} | {"MANIFEST.json"}
unlisted = [os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs]
unlisted = [p for p in unlisted if p not in listed]
print(f"entries {len(entries)} ok {ok} bad {bad} missing {missing} unlisted {len(unlisted)}")
print("sample unlisted:", sorted(unlisted)[:6])
