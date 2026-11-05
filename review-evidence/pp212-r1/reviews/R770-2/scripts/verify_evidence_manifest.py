#!/usr/bin/env python3
"""verify_evidence_manifest.py <pp212-r1 dir> <prefix>: check every MANIFEST.json entry under
<prefix> against its published_sha256 and report unlisted files under that prefix."""
import hashlib, json, os, sys
root, prefix = sys.argv[1], sys.argv[2]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
ok = bad = miss = 0
for e in m:
    f = e["file"]
    if not f.startswith(prefix):
        continue
    p = os.path.join(root, f)
    if not os.path.exists(p):
        miss += 1; print("MISSING", f); continue
    if hashlib.sha256(open(p, "rb").read()).hexdigest() == e["published_sha256"]:
        ok += 1
    else:
        bad += 1; print("BAD", f)
listed = {e["file"] for e in m}
disk = {os.path.relpath(os.path.join(r, x), root) for r, _, fs in os.walk(os.path.join(root, prefix)) for x in fs}
print(f"entries {len(m)}; under {prefix}: ok {ok}, bad {bad}, missing {miss}, unlisted {len(disk - listed)}")
