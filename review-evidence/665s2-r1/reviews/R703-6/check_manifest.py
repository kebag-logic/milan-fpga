#!/usr/bin/env python3
"""Verify one prefix of a published evidence MANIFEST.json against the files beside it.

Usage: python3 -I check_manifest.py <evidence dir holding MANIFEST.json> <prefix, e.g. author-r6/>
Each entry's 'published_sha256' must equal the sha256 of '<dir>/<file>', and every file
on disk under the prefix must be listed. Exit 0 only when all match.
"""
import hashlib
import json
import os
import sys

root, prefix = sys.argv[1], sys.argv[2]
entries = [e for e in json.load(open(os.path.join(root, 'MANIFEST.json'))) if e['file'].startswith(prefix)]
listed = {e['file'] for e in entries}
bad = [e['file'] for e in entries
       if not os.path.isfile(os.path.join(root, e['file']))
       or hashlib.sha256(open(os.path.join(root, e['file']), 'rb').read()).hexdigest() != e['published_sha256']]
on_disk = {os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(os.path.join(root, prefix)) for f in fs}
unlisted = sorted(on_disk - listed)
redacted = sum(1 for e in entries if e.get('path_redacted') or e['original_sha256'] != e['published_sha256'])
print(f'{prefix}: {len(entries)} listed, {len(bad)} mismatched or missing, {len(unlisted)} unlisted on disk, '
      f'{redacted} redacted')
for name in bad + unlisted:
    print('  ', name)
sys.exit(1 if bad or unlisted else 0)
