#!/usr/bin/env python3
"""usage: audit_manifest.py <evidence-root>  - check every downloaded file named
in <root>/MANIFEST.json against its published_sha256; print the tally."""
import hashlib, json, os, sys
root = sys.argv[1]
ok = bad = absent = 0
for e in json.load(open(os.path.join(root, "MANIFEST.json"))):
    p = os.path.join(root, e["file"])
    if not os.path.exists(p):
        absent += 1
        continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h == e.get("published_sha256", e.get("sha256")):
        ok += 1
    else:
        bad += 1
        print("MISMATCH", e["file"])
print(f"manifest entries checked: {ok} match, {bad} mismatch, {absent} not downloaded")
