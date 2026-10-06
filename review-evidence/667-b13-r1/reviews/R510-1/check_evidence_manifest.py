#!/usr/bin/env python3
"""Verify the published evidence MANIFEST.json against the fetched bytes.

Usage: check_evidence_manifest.py <review-evidence/667-b13-r1 dir>
"""
import hashlib
import json
import os
import sys

root = sys.argv[1]
d = json.load(open(os.path.join(root, "MANIFEST.json")))
bad, changed = [], []
for e in d:
    p = os.path.join(root, e["file"])
    if not os.path.exists(p):
        bad.append(("missing", e["file"]))
        continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != e["published_sha256"]:
        bad.append(("hash", e["file"]))
    if e["original_sha256"] != e["published_sha256"]:
        changed.append((e["file"], e["path_redacted"]))
print(f"INFO entries {len(d)} mismatches {bad} redacted-for-publication {changed}")
print(f"CHECK {'PASS' if not bad else 'FAIL'} every published byte matches MANIFEST.json")
sys.exit(1 if bad else 0)
