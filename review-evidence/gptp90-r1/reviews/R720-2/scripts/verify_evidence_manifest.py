#!/usr/bin/env python3
"""Verify the public evidence packet MANIFEST.json (list of {file, published_sha256}) against files on disk."""
import hashlib, json, os, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
listed = set(); bad = missing = 0
for e in m:
    p = e["file"]; listed.add(p); fp = os.path.join(root, p)
    if not os.path.exists(fp):
        missing += 1; print("MISSING", p); continue
    if hashlib.sha256(open(fp, "rb").read()).hexdigest() != e["published_sha256"]:
        bad += 1; print("BAD", p)
ondisk = {os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs} - {"MANIFEST.json"}
unlisted = sorted(ondisk - listed)
for u in unlisted: print("UNLISTED", u)
red = sum(1 for e in m if e.get("path_redacted"))
print(f"entries={len(m)} bad={bad} missing={missing} unlisted={len(unlisted)} redacted={red}")
sys.exit(1 if bad or missing or unlisted else 0)
