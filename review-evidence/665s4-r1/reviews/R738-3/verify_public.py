#!/usr/bin/env python3
"""Verify the published author round-4 receipts against the evidence MANIFEST.json and summarise gate
receipts. Usage: verify_public.py <evidence-root review-evidence/665s4-r1> <exact head sha>."""
import hashlib, json, re, sys
from pathlib import Path

root, head = Path(sys.argv[1]), sys.argv[2]
man = json.loads((root / 'MANIFEST.json').read_text())
r4 = [e for e in man if e['file'].startswith('author-r4/')]
bad, missing = [], []
for e in r4:
    p = root / e['file']
    if not p.is_file():
        missing.append(e['file']); continue
    if hashlib.sha256(p.read_bytes()).hexdigest() != e['published_sha256']:
        bad.append(e['file'])
present = {str(p.relative_to(root)) for p in (root / 'author-r4').rglob('*') if p.is_file()}
unlisted = sorted(present - {e['file'] for e in r4})
print(f'author-r4 manifest entries: {len(r4)}; present files: {len(present)}; hash mismatches: {len(bad)}; '
      f'missing: {len(missing)}; unlisted: {len(unlisted)}')
for f in bad + missing + unlisted:
    print('  ', f)
for f in sorted(present):
    if f.endswith('HEAD.txt') or f.endswith('runs-head.txt'):
        t = (root / f).read_text()
        print(f'{f}: head recorded = {head in t}')
for summ in sorted(present):
    if summ.endswith('summary.md') or summ.endswith('summary.txt'):
        t = (root / summ).read_text()
        rcs = re.findall(r'\brc[ =:]*(-?\d+)', t)
        print(f'{summ}: rc tokens {len(rcs)}, nonzero {[r for r in rcs if r != "0"]}')
