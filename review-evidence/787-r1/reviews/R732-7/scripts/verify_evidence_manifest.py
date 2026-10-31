#!/usr/bin/env python3
"""Check every published_sha256 in an evidence MANIFEST.json against the extracted files.
Usage: python3 -I verify_evidence_manifest.py <packet-root>"""
import hashlib, json, os, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
listed = {e["file"] for e in m}
bad = missing = 0
for e in m:
    p = os.path.join(root, e["file"])
    if not os.path.isfile(p):
        missing += 1; print("MISSING", e["file"]); continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != e["published_sha256"]:
        bad += 1; print("MISMATCH", e["file"])
extra = [os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs]
extra = [x for x in extra if x != "MANIFEST.json" and x not in listed]
for x in extra: print("UNLISTED", x)
print(f"entries={len(m)} mismatched={bad} missing={missing} unlisted={len(extra)}")
sys.exit(1 if bad or missing or extra else 0)
