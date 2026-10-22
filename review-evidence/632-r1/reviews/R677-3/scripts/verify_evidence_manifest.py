#!/usr/bin/env python3
"""Verify review-evidence/632-r1/MANIFEST.json against the files beside it.
usage: verify_evidence_manifest.py <review-evidence/632-r1 dir>"""
import hashlib, json, os, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
bad = miss = red = 0
for e in m:
    p = os.path.join(root, e["file"])
    red += bool(e.get("path_redacted"))
    if not os.path.exists(p):
        miss += 1; continue
    if hashlib.sha256(open(p, "rb").read()).hexdigest() != e["published_sha256"]:
        bad += 1; print("MISMATCH", e["file"])
listed = {e["file"] for e in m}
present = {os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs} - {"MANIFEST.json"}
print(f"entries {len(m)} mismatched {bad} missing {miss} path-redacted {red} unlisted {len(present - listed)}")
sys.exit(1 if bad or miss or present - listed else 0)
