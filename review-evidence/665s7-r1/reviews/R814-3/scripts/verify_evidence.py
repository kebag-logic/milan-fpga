#!/usr/bin/env python3
"""verify_evidence.py DIR - check every MANIFEST.json entry's published_sha256 under DIR, and that no file is unlisted."""
import hashlib, json, os, sys
root = sys.argv[1]
d = json.load(open(os.path.join(root, "MANIFEST.json")))
listed, bad, miss = set(), 0, 0
for e in d:
    p = e["file"]; listed.add(p)
    f = os.path.join(root, p)
    if not os.path.exists(f):
        miss += 1; print("MISSING", p); continue
    if hashlib.sha256(open(f, "rb").read()).hexdigest() != e["published_sha256"]:
        bad += 1; print("BAD", p)
present = {os.path.relpath(os.path.join(r, n), root) for r, _, fs in os.walk(root) for n in fs} - {"MANIFEST.json"}
r3 = sum(1 for p in listed if p.startswith("author-r3/"))
print(f"entries {len(d)}, author-r3 {r3}, bad {bad}, missing {miss}, unlisted {len(present - listed)}")
sys.exit(1 if bad or miss or present - listed else 0)
