#!/usr/bin/env python3
"""Verify the published lane-B4 evidence (author, author-r2, author-r3) against MANIFEST.json.

usage: verify_evidence_packet.py <review-evidence/b4-r1 dir>
Checks each non-review entry's published_sha256, and lists the entries whose
published bytes differ from the original by design (redacted copies).
"""
import hashlib, json, os, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
n = bad = 0
missing, redacted = [], []
for e in m:
    f = e["file"]
    if f.startswith("reviews/"):
        continue
    p = os.path.join(root, f)
    if not os.path.exists(p):
        missing.append(f); continue
    n += 1
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != e["published_sha256"]:
        bad += 1; print("DIFFER", f)
    if e["original_sha256"] != e["published_sha256"]:
        redacted.append(f)
print(f"checked {n} differ {bad} missing {len(missing)}")
print("published differs from original by redaction:", ", ".join(redacted))
sys.exit(1 if bad or missing else 0)
