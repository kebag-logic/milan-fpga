#!/usr/bin/env python3
"""Verify every published_sha256 in an evidence MANIFEST.json against the files beside it."""
import hashlib, json, os, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
bad = 0; listed = set()
for e in m:
    p = os.path.join(root, e["file"]); listed.add(e["file"])
    if not os.path.isfile(p):
        print("MISSING", e["file"]); bad += 1; continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != e["published_sha256"]:
        print("MISMATCH", e["file"]); bad += 1
present = set()
for d, _, fs in os.walk(root):
    for f in fs:
        rel = os.path.relpath(os.path.join(d, f), root)
        if rel != "MANIFEST.json": present.add(rel)
for x in sorted(present - listed): print("UNLISTED", x); bad += 1
print(f"entries={len(m)} present={len(present)} bad={bad}")
sys.exit(1 if bad else 0)
