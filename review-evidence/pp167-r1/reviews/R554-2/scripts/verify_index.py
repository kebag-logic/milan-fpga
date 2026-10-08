#!/usr/bin/env python3
"""Check an evidence-index.json (list of {file, bytes, sha256}) against files in its directory.
usage: verify_index.py INDEX_JSON"""
import hashlib, json, os, sys
idx = sys.argv[1]; base = os.path.dirname(idx)
bad = 0
for e in json.load(open(idx)):
    p = os.path.join(base, e["file"])
    if not os.path.exists(p):
        print("MISSING ", e["file"]); bad += 1; continue
    b = open(p, "rb").read()
    ok = len(b) == e["bytes"] and hashlib.sha256(b).hexdigest() == e["sha256"]
    bad += not ok
    print("OK      " if ok else "MISMATCH", e["file"], e["bytes"], len(b), e["sha256"][:16], hashlib.sha256(b).hexdigest()[:16])
print("mismatches:", bad); sys.exit(1 if bad else 0)
