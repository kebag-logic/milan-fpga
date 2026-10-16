#!/usr/bin/env python3
"""Re-hash every raw listed in RAW-ARTIFACTS.json at a raw root (read-only).
Usage: verify_raws.py RAW-ARTIFACTS.json RAW_ROOT"""
import hashlib, json, os, sys
manifest, root = sys.argv[1], sys.argv[2]
files = json.load(open(manifest))["files"]
prefix = "/tmp/a624/raw/"
eq = diff = miss = 0
for f in files:
    rel = f["path"][len(prefix):] if f["path"].startswith(prefix) else f["path"]
    p = os.path.join(root, rel)
    if not os.path.exists(p):
        miss += 1; print("MISSING", rel); continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h == f["sha256"] and os.path.getsize(p) == f["bytes"]:
        eq += 1
    else:
        diff += 1; print("DIFF", rel)
print(f"listed={len(files)} equal={eq} differ={diff} missing={miss}")
