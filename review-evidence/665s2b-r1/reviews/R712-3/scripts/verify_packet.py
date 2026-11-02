#!/usr/bin/env python3
"""Verify the round 13 author packet against the evidence MANIFEST.json and receipts/INDEX.md.

Usage: verify_packet.py <extracted review-evidence/665s2b-r1 dir>
Prints, for author-r13: files hashed, mismatches against MANIFEST.json's published_sha256,
files present but not in the manifest, manifest entries absent from the tree, and INDEX.md rows
whose file is absent (each with its recorded sha256).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
man = {e['file']: e for e in json.loads((root / 'MANIFEST.json').read_text())}
sub = 'author-r13/'
present = {str(p.relative_to(root)): p for p in (root / 'author-r13').rglob('*') if p.is_file()}
bad, unlisted = [], []
for rel, p in sorted(present.items()):
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    e = man.get(rel)
    if e is None:
        unlisted.append(rel)
    elif e['published_sha256'] != h:
        bad.append((rel, h, e['published_sha256']))
absent = [f for f in man if f.startswith(sub) and f not in present]
print(f'author-r13 files: {len(present)}; manifest entries: {sum(f.startswith(sub) for f in man)}')
print(f'sha256 mismatches: {len(bad)}')
for b in bad:
    print('  MISMATCH', *b)
print(f'present, not in manifest: {len(unlisted)}', *unlisted[:20], sep='\n  ')
print(f'in manifest, absent: {len(absent)}', *absent[:40], sep='\n  ')
idx = (root / 'author-r13/receipts/INDEX.md').read_text()
rows = re.findall(r'^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|$', idx, re.M)
miss, imis = [], []
for f, size, h in rows:
    p = root / 'author-r13/receipts' / f
    if not p.exists():
        miss.append((f, size, h))
    elif hashlib.sha256(p.read_bytes()).hexdigest() != h:
        imis.append(f)
print(f'INDEX rows: {len(rows)}; hash mismatches: {len(imis)}', *imis, sep='\n  ')
print(f'INDEX rows absent from the tree (hash recorded only): {len(miss)}')
for m in miss:
    print('  ABSENT', *m)
