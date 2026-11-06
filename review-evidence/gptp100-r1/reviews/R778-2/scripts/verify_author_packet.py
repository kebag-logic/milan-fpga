#!/usr/bin/env python3
"""Check the author's round 2 receipts against the evidence MANIFEST.json.

usage: python3 -I verify_author_packet.py <downloaded review-evidence/gptp100-r1 dir>

Every MANIFEST entry under author-r2/ must exist and match its
published_sha256; every file under author-r2/ must be listed.
"""
import hashlib
import json
import os
import sys

root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
entries = {x["file"]: x for x in m if x["file"].startswith("author-r2/")}
bad = 0
for f, x in sorted(entries.items()):
    p = os.path.join(root, f)
    if not os.path.exists(p):
        print("MISSING", f)
        bad += 1
        continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    ok = h == x["published_sha256"]
    bad += not ok
    print("OK " if ok else "BAD", h, f, "(redacted copy)" if x["original_sha256"] != x["published_sha256"] else "")
for d, _, fs in os.walk(os.path.join(root, "author-r2")):
    for n in fs:
        rel = os.path.relpath(os.path.join(d, n), root)
        if rel not in entries:
            print("UNLISTED", rel)
            bad += 1
print(f"{len(entries)} listed author-r2 files, {bad} problems")
sys.exit(1 if bad else 0)
