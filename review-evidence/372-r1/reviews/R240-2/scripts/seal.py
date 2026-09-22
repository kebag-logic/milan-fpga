#!/usr/bin/env python3
"""Seal terminal review artifacts; excludes only the manifest itself."""
import hashlib
from pathlib import Path

out = Path(__file__).resolve().parents[1]
manifest = out/'MANIFEST.sha256'
rows=[]
for path in sorted(out.rglob('*')):
    if not path.is_file() or path == manifest:
        continue
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    rows.append(f'{digest}  {path.relative_to(out)}')
manifest.write_text('\n'.join(rows)+'\n')
for row in rows:
    digest,name=row.split('  ',1)
    assert hashlib.sha256((out/name).read_bytes()).hexdigest()==digest,name
print(f'MANIFEST PASS: {len(rows)} artifact files hash-verified')
print('REPORT sha256:',hashlib.sha256((out/'REPORT.md').read_bytes()).hexdigest())
