#!/usr/bin/env python3
"""Check an extracted evidence packet directory against its MANIFEST.json published hashes.

usage: python3 -I verify_packet.py <review-evidence/665s2b-r1 dir> <prefix, e.g. author-r14/>
Prints listed, present, bad, missing, unlisted counts and exits 0 only when all listed files match and none is unlisted.
"""
import hashlib
import json
import os
import sys

root, prefix = sys.argv[1], sys.argv[2]
entries = [e for e in json.load(open(os.path.join(root, 'MANIFEST.json'))) if e['file'].startswith(prefix)]
bad, missing, seen = [], [], set()
for e in entries:
    path = os.path.join(root, e['file'])
    if not os.path.isfile(path):
        missing.append(e['file'])
        continue
    seen.add(e['file'])
    if hashlib.sha256(open(path, 'rb').read()).hexdigest() != e['published_sha256']:
        bad.append(e['file'])
on_disk = set()
for d, _, files in os.walk(os.path.join(root, prefix)):
    for f in files:
        on_disk.add(os.path.relpath(os.path.join(d, f), root))
unlisted = sorted(on_disk - seen)
print(f'listed {len(entries)} present {len(seen)} bad {len(bad)} missing {len(missing)} unlisted {len(unlisted)} '
      f'path_redacted {sum(1 for e in entries if e["path_redacted"])}')
for name in bad + missing + unlisted:
    print('PROBLEM', name)
sys.exit(0 if not (bad or missing or unlisted) else 1)
