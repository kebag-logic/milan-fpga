#!/usr/bin/env python3
"""Verify a published author evidence subtree against MANIFEST.json (published_sha256)
and receipts/INDEX.md rows (bytes, sha256). usage: verify_evidence.py <665s1-r1 dir> <subdir>"""
import hashlib, json, re, sys
from pathlib import Path
base, sub = Path(sys.argv[1]), sys.argv[2]
man = {e['file']: e for e in json.loads((base / 'MANIFEST.json').read_text())}
files = sorted(p.relative_to(base).as_posix() for p in (base / sub).rglob('*') if p.is_file())
bad = [f for f in files if f not in man or hashlib.sha256((base / f).read_bytes()).hexdigest() != man[f]['published_sha256']]
listed = [k for k in man if k.startswith(sub + '/')]
missing = [k for k in listed if not (base / k).is_file()]
print(f'{sub}: {len(files)} files present, {len(listed)} manifest rows, mismatched/unlisted {len(bad)}, missing {len(missing)}, '
      f'path-redacted {sum(man[k]["path_redacted"] for k in listed)}')
for f in bad + missing: print('  BAD', f)
idx = base / sub / 'receipts/INDEX.md'
rows = ok = 0
for line in idx.read_text().splitlines():
    m = re.match(r'\|\s*`?([^`|]+?)`?\s*\|\s*([\d,]+)\s*\|\s*`?([0-9a-f]{64})`?\s*\|', line)
    if not m: continue
    rows += 1; p = base / sub / 'receipts' / m[1].strip()
    if p.is_file() and p.stat().st_size == int(m[2].replace(',', '')) and hashlib.sha256(p.read_bytes()).hexdigest() == m[3]: ok += 1
    else: print('  INDEX-BAD', m[1])
print(f'INDEX.md rows parsed {rows}, matching {ok}')
