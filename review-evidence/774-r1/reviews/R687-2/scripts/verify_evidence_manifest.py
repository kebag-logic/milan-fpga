#!/usr/bin/env python3
"""Verify a published review-evidence MANIFEST.json: every listed file's
sha256 equals its published_sha256, and list files present but unlisted."""
import hashlib, json, os, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
ok = bad = missing = 0
listed = set()
for e in m:
    f = e["file"]; listed.add(f)
    p = os.path.join(root, f)
    if not os.path.exists(p):
        missing += 1; print("MISSING", f); continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h == e["published_sha256"]: ok += 1
    else: bad += 1; print("MISMATCH", f)
unl = []
for d, _, fs in os.walk(root):
    for x in fs:
        r = os.path.relpath(os.path.join(d, x), root)
        if r != "MANIFEST.json" and r not in listed: unl.append(r)
for u in sorted(unl): print("UNLISTED", u)
print(f"entries={len(m)} ok={ok} mismatch={bad} missing={missing} unlisted={len(unl)}")
sys.exit(1 if bad or missing else 0)
