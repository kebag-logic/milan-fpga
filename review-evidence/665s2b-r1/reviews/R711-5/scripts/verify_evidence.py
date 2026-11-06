#!/usr/bin/env python3
"""Verify the published round 16 evidence against its MANIFEST.json (published_sha256), and list unlisted files.
usage: verify_evidence.py EVIDENCE_ROOT   (the review-evidence/665s2b-r1 directory of commit cd93800c)"""
import hashlib, json, os, sys
root = sys.argv[1]; os.chdir(root)
m = json.load(open('MANIFEST.json'))
r16 = [e for e in m if e['file'].startswith('author-r16/')]
bad = 0
for e in r16:
    p = e['file']
    if not os.path.exists(p) or hashlib.sha256(open(p, 'rb').read()).hexdigest() != e['published_sha256']:
        print('BAD', p); bad += 1
listed = {e['file'] for e in r16}
disk = {os.path.join(d, f) for d, _, fs in os.walk('author-r16') for f in fs}
print(f"listed {len(r16)} bad {bad} redacted-or-changed {sum(1 for e in r16 if e['path_redacted'] or e['original_sha256'] != e['published_sha256'])} on-disk {len(disk)} unlisted {len(disk - listed)}")
sys.exit(1 if bad or disk - listed else 0)
