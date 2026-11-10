#!/usr/bin/env python3
"""Usage: verify_manifest.py <packet-dir>
Hashes every file a published packet's MANIFEST.json lists against its
published_sha256, and names any file present but unlisted."""
import hashlib, json, os, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
bad = 0
listed = set()
for e in m:
    listed.add(e["file"])
    p = os.path.join(root, e["file"])
    if not os.path.isfile(p):
        print("MISSING", e["file"]); bad += 1; continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != e["published_sha256"]:
        print("MISMATCH", e["file"]); bad += 1
present = set()
for d, _, fs in os.walk(root):
    for f in fs:
        present.add(os.path.relpath(os.path.join(d, f), root))
extra = sorted(present - listed - {"MANIFEST.json"})
for x in extra: print("UNLISTED", x)
red = sum(1 for e in m if e.get("path_redacted"))
print(f"{len(m)} listed, {bad} missing or mismatched, {len(extra)} unlisted, {red} path-redacted")
sys.exit(1 if bad or extra else 0)
