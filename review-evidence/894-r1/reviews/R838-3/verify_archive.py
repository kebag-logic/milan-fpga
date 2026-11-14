#!/usr/bin/env python3
"""Verify the published author packet against its archive manifest."""
import hashlib
import json
from pathlib import Path

base = Path(__file__).resolve().parent / 'scratch/review-evidence/894-r1'
rows = json.loads((base / 'MANIFEST.json').read_text())
selected = [r for r in rows if r['file'].startswith('author-r8/')]
bad = []
for r in selected:
    p = base / r['file']
    actual = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else 'MISSING'
    if actual != r['published_sha256']:
        bad.append((r['file'], actual, r['published_sha256']))
print('Archive: 183cd03d60e9d51dd8e251bbd38ffe5b3c01ee66')
print(f'Checked {len(selected)} author-r8 files against published_sha256; mismatches: {len(bad)}')
for b in bad:
    print(b)
print('Manifest provides content integrity; the archive commit has no cryptographic signature.')
raise SystemExit(bool(bad))
