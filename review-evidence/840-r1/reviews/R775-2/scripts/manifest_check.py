#!/usr/bin/env python3
"""Check every author-r2 and author-r3 file against the evidence MANIFEST.json.

Usage: manifest_check.py <extracted review-evidence/840-r1 directory>
"""
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
entries = json.loads((root / 'MANIFEST.json').read_text())
counts = dict(listed=0, ok=0, bad=0, missing=0)
listed = set()
for entry in entries:
    name = entry['file']
    if not name.startswith(('author-r2/', 'author-r3/')):
        continue
    counts['listed'] += 1
    listed.add(name)
    path = root / name
    if not path.exists():
        counts['missing'] += 1
    elif hashlib.sha256(path.read_bytes()).hexdigest() == entry['published_sha256']:
        counts['ok'] += 1
    else:
        counts['bad'] += 1
        print('BAD', name)
on_disk = {str(p.relative_to(root)) for d in ('author-r2', 'author-r3') for p in (root / d).rglob('*') if p.is_file()}
print(counts, 'unlisted on disk:', len(on_disk - listed), sorted(on_disk - listed)[:5])
