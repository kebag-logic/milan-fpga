#!/usr/bin/env python3
"""Check a published evidence tree against its publication MANIFEST.json.
Every file must hash to published_sha256; files whose path_redacted is False
must also equal original_sha256. Usage: verify_publication.py EVIDENCE_DIR"""
import hashlib, json, os, sys
root = sys.argv[1]
ents = json.load(open(os.path.join(root, "MANIFEST.json")))
ok = bad = miss = red = 0
listed = set()
for e in ents:
    listed.add(e["file"])
    p = os.path.join(root, e["file"])
    if not os.path.exists(p):
        miss += 1; print("MISSING", e["file"]); continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    exp = e["published_sha256"]
    if not e["path_redacted"] and exp != e["original_sha256"]:
        print("INCONSISTENT", e["file"]); bad += 1; continue
    red += e["path_redacted"]
    if h == exp: ok += 1
    else: bad += 1; print("BAD", e["file"])
on_disk = {os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs} - {"MANIFEST.json"}
for f in sorted(on_disk - listed): print("UNLISTED", f)
print(f"entries={len(ents)} ok={ok} bad={bad} missing={miss} path_redacted={red} unlisted={len(on_disk-listed)}")
