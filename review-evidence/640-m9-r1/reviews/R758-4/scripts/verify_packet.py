#!/usr/bin/env python3
"""Check the published author-r4 packet against the evidence manifest and its
own digest list. Usage: python3 -I verify_packet.py <evidence root>"""
import hashlib
import json
import os
import sys

root = sys.argv[1]
man = json.load(open(os.path.join(root, 'MANIFEST.json')))
entries = {e['file']: e for e in man if e['file'].startswith('author-r4/')}
pub_bad = [f for f, e in entries.items()
           if hashlib.sha256(open(os.path.join(root, f), 'rb').read()).hexdigest() != e['published_sha256']]
files = []
for d, _, fs in os.walk(os.path.join(root, 'author-r4')):
    files += [os.path.relpath(os.path.join(d, f), root) for f in fs]
unlisted = sorted(set(files) - set(entries))
print(f"manifest entries {len(entries)}; published-digest mismatches {len(pub_bad)}; unlisted files {len(unlisted)}")
sums = {}
for line in open(os.path.join(root, 'author-r4/evidence/SHA256SUMS')):
    h, f = line.split(None, 1)
    sums[f.strip().removeprefix('./')] = h
differs = []
absent = []
for k, h in sums.items():
    p = os.path.join(root, 'author-r4', k)
    if not os.path.exists(p):
        absent.append(k)
    elif hashlib.sha256(open(p, 'rb').read()).hexdigest() != h:
        differs.append(k)
red = {f[len('author-r4/'):] for f, e in entries.items() if e['path_redacted']}
print(f"digest list lines {len(sums)}; differ {len(differs)}; all differing are path-redacted: {set(differs) <= red}")
print(f"listed but not published: {absent}")
orig_bad = [k for k, h in sums.items() if 'author-r4/' + k in entries and entries['author-r4/' + k]['original_sha256'] != h]
print(f"digest list against the manifest's original digests: {len(orig_bad)} mismatches")
