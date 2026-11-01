#!/usr/bin/env python3
"""Check an author packet directory against the evidence MANIFEST.json
(published_sha256 of every listed file, no unlisted file) and its
SHA256SUMS against the manifest's original_sha256.
Usage: python3 -I verify_packet.py <evidence-root> <packet-subdir>
"""
import hashlib, json, os, sys
root, sub = sys.argv[1], sys.argv[2]
m = {e['file']: e for e in json.load(open(os.path.join(root, 'MANIFEST.json')))}
mine = {k: e for k, e in m.items() if k.startswith(sub + '/')}
bad = [k for k, e in mine.items() if hashlib.sha256(open(os.path.join(root, k), 'rb').read()).hexdigest() != e['published_sha256']]
files = {os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(os.path.join(root, sub)) for f in fs}
red = sorted(k for k, e in mine.items() if e['path_redacted'])
sums = os.path.join(root, sub, 'evidence', 'SHA256SUMS')
n = sbad = 0
for line in open(sums):
    h, p = line.split(None, 1); p = sub + '/evidence/' + p.strip().lstrip('./'); n += 1
    sbad += m[p]['original_sha256'] != h
print(f"{sub}: {len(mine)} manifest entries, {len(bad)} published-hash mismatches, {len(files - set(mine))} unlisted files")
print(f"SHA256SUMS: {n} lines, {sbad} differ from the manifest's original_sha256")
print(f"path-redacted entries ({len(red)}); these alone differ from SHA256SUMS:")
for k in red: print("  " + k)
