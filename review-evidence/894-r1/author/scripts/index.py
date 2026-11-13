#!/usr/bin/env python3
"""INDEX.md of an output directory, generated from the files present: each file's path, size and sha256. Exits 1 on a
file over 200 KB, or on a receipt (anything under receipts/) carrying a host path. usage: index.py OUTDIR"""
import hashlib
import sys
from pathlib import Path

out = Path(sys.argv[1]).resolve()
HOST = ('/data-2/', '$VALIDATION_STORAGE', '$WORKSPACE_HOME', '/tmp/')
rows, bad = [], []
for f in sorted(p for p in out.rglob('*') if p.is_file() and p.name != 'INDEX.md'):
    rel = f.relative_to(out).as_posix()
    data = f.read_bytes()
    if len(data) > 200 * 1024:
        bad.append(f'{rel}: {len(data)} B, over 200 KB')
    if rel.startswith('receipts/') and any(h.encode() in data for h in HOST):
        bad.append(f'{rel}: carries a host path')
    rows.append(f'| `{rel}` | {len(data):,} | `{hashlib.sha256(data).hexdigest()}` |')
text = ['# 894-a773 output index', '', f'Generated from the {len(rows)} files present (`index.py`).', '',
        '| File | Bytes | sha256 |', '|---|---:|---|', *rows, '']
(out / 'INDEX.md').write_text('\n'.join(text))
for line in bad:
    print('BAD', line)
print(f'{len(rows)} files indexed, {len(bad)} bad')
sys.exit(1 if bad else 0)
