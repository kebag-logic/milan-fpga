#!/usr/bin/env python3
"""Verify the published evidence MANIFEST.json sha256 for one subtree.
Usage: python3 -I evidence_manifest_check.py <review-evidence/637-r1 dir> <prefix, e.g. author-r3c/>"""
import hashlib, json, os, sys
root, pre = sys.argv[1], sys.argv[2]
m = [e for e in json.load(open(os.path.join(root, "MANIFEST.json"))) if e["file"].startswith(pre)]
bad = miss = 0
for e in m:
    p = os.path.join(root, e["file"])
    if not os.path.exists(p): miss += 1; print("MISSING", e["file"]); continue
    if hashlib.sha256(open(p, "rb").read()).hexdigest() != e["published_sha256"]: bad += 1; print("MISMATCH", e["file"])
onfs = {os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(os.path.join(root, pre)) for f in fs}
extra = onfs - {e["file"] for e in m}
print(f"{pre}: {len(m)} entries, {bad} mismatches, {miss} missing, {len(extra)} unlisted files")
sys.exit(1 if bad or miss or extra else 0)
