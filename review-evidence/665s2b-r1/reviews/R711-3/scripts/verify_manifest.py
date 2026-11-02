#!/usr/bin/env python3
"""Check every file of one directory of the published evidence packet against MANIFEST.json.

usage: verify_manifest.py <packet root containing MANIFEST.json> <prefix, e.g. author-r13/>
Prints one line per mismatch or missing file, then a summary; exit 1 on any mismatch.
"""
import hashlib
import json
import sys
from pathlib import Path

root, prefix = Path(sys.argv[1]), sys.argv[2]
manifest = json.loads((root / 'MANIFEST.json').read_text())
listed = {e['file']: e for e in manifest if e['file'].startswith(prefix)}
bad = 0
for name, e in sorted(listed.items()):
    p = root / name
    if not p.is_file():
        print('MISSING', name)
        bad += 1
        continue
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != e['published_sha256']:
        print('MISMATCH', name)
        bad += 1
on_disk = {str(p.relative_to(root)) for p in (root / prefix).rglob('*') if p.is_file()}
for extra in sorted(on_disk - set(listed)):
    print('UNLISTED', extra)
    bad += 1
redacted = sum(1 for e in listed.values() if e.get('path_redacted') or e['original_sha256'] != e['published_sha256'])
print(f'listed={len(listed)} on_disk={len(on_disk)} bad={bad} redacted_or_rewritten={redacted}')
sys.exit(1 if bad else 0)
