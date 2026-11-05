#!/usr/bin/env python3
"""verify_evidence_manifest.py <pp212-r1 dir> <prefix>...: check every listed
file under the prefixes against MANIFEST.json's published_sha256."""
import hashlib, json, os, sys
root = sys.argv[1]; prefixes = tuple(sys.argv[2:])
m = json.load(open(os.path.join(root, "MANIFEST.json")))
ok = bad = miss = 0
for e in m:
    if not e["file"].startswith(prefixes):
        continue
    p = os.path.join(root, e["file"])
    if not os.path.exists(p):
        miss += 1; print("MISSING", e["file"]); continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h == e["published_sha256"]:
        ok += 1
    else:
        bad += 1; print("BAD", e["file"])
print(f"manifest entries checked: {ok + bad + miss}; ok {ok}; bad {bad}; missing {miss}")
