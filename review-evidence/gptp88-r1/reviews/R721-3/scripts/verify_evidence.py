#!/usr/bin/env python3
"""Verify downloaded evidence files against the evidence MANIFEST.json.
Usage: verify_evidence.py EVROOT PREFIX...   (EVROOT holds MANIFEST.json and
the files at their manifest-relative paths)."""
import hashlib, json, os, sys
root, prefixes = sys.argv[1], sys.argv[2:]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
ok = bad = 0
for e in m:
    if not e["file"].startswith(tuple(prefixes)): continue
    p = os.path.join(root, e["file"])
    if not os.path.exists(p): continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    good = h == e["published_sha256"]
    ok += good; bad += not good
    print(("OK  " if good else "BAD ") + h + "  " + e["file"])
print(f"verified {ok}, mismatched {bad}")
sys.exit(1 if bad else 0)
