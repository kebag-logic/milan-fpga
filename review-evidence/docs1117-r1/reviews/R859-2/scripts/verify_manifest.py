#!/usr/bin/env python3
"""Check downloaded evidence files against the packet MANIFEST.json published_sha256.
Usage: verify_manifest.py <evidence_dir>  (dir holds MANIFEST.json and the files)"""
import hashlib, json, os, sys
d = sys.argv[1]
m = {e["file"]: e for e in json.load(open(os.path.join(d, "MANIFEST.json")))}
bad = 0
for root, _, fs in os.walk(d):
    for f in fs:
        p = os.path.relpath(os.path.join(root, f), d)
        if p == "MANIFEST.json": continue
        h = hashlib.sha256(open(os.path.join(d, p), "rb").read()).hexdigest()
        e = m.get(p)
        ok = e is not None and e["published_sha256"] == h
        bad += not ok
        print(("OK  " if ok else "BAD ") + p + " " + h + ("" if e else " (not in manifest)"))
print("author-r3 entries in manifest:", sum(1 for k in m if k.startswith("author-r3/")))
sys.exit(1 if bad else 0)
