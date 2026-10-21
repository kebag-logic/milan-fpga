#!/usr/bin/env python3
"""Check a published review-evidence packet against its MANIFEST.json.

usage: verify_evidence.py <packet dir> <prefix>
Every MANIFEST entry whose 'file' starts with <prefix> must exist and hash
to its 'published_sha256'; every file on disk under <prefix> must be listed.
"""
import hashlib, json, os, sys
root, prefix = sys.argv[1], sys.argv[2]
os.chdir(root)
m = json.load(open("MANIFEST.json"))
listed, bad, miss = set(), [], []
for e in m:
    p = e["file"]
    if not p.startswith(prefix):
        continue
    listed.add(p)
    if not os.path.exists(p):
        miss.append(p); continue
    if hashlib.sha256(open(p, "rb").read()).hexdigest() != e["published_sha256"]:
        bad.append(p)
disk = {os.path.join(r, f) for r, _, fs in os.walk(prefix.rstrip("/")) for f in fs}
print(f"MANIFEST.json sha256 {hashlib.sha256(open('MANIFEST.json','rb').read()).hexdigest()}")
print(f"prefix {prefix}: listed {len(listed)}, missing {len(miss)}, hash mismatches {len(bad)}, unlisted on disk {len(disk - listed)}")
for p in miss + bad + sorted(disk - listed):
    print("  ", p)
sys.exit(1 if (miss or bad or disk - listed) else 0)
