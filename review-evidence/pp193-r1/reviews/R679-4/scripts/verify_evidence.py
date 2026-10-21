#!/usr/bin/env python3
"""Check every author-r4 file of the published pp193-r1 evidence against MANIFEST.json.
usage: verify_evidence.py <checkout>/review-evidence/pp193-r1"""
import hashlib, json, os, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
listed = {e["file"]: e for e in m if e["file"].startswith("author-r4/")}
ok = bad = miss = 0
for f, e in sorted(listed.items()):
    p = os.path.join(root, f)
    if not os.path.exists(p):
        miss += 1; print("MISSING", f); continue
    if hashlib.sha256(open(p, "rb").read()).hexdigest() == e["published_sha256"]:
        ok += 1
    else:
        bad += 1; print("BAD", f)
ondisk = {os.path.relpath(os.path.join(r, x), root) for r, _, fs in os.walk(os.path.join(root, "author-r4")) for x in fs}
print(f"author-r4 listed {len(listed)} ok {ok} bad {bad} missing {miss}; on disk {len(ondisk)}, unlisted {len(ondisk - set(listed))}")
