#!/usr/bin/env python3
"""index.py RECEIPTS: write RECEIPTS/INDEX.md from the files present: each directory's files with their size in bytes,
sha256 prefix and first line (none for a binary or compressed file)."""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = ['# Receipts index', '', 'Generated from the files present (index.py); size in bytes, sha256 prefix, first line.']
dirs = sorted({p.parent for p in root.rglob('*') if p.is_file() and p.name != 'INDEX.md'})
for d in dirs:
    out += ['', f'## {d.relative_to(root) if d != root else "."}', '', '| File | Bytes | sha256 | First line |',
            '|---|---:|---|---|']
    for f in sorted(p for p in d.iterdir() if p.is_file() and p.name != 'INDEX.md'):
        data = f.read_bytes()
        first = ''
        if not f.name.endswith('.gz'):
            try:
                first = data.decode().splitlines()[0] if data else ''
            except UnicodeDecodeError:
                first = ''
        first = first.replace('|', '\\|')[:110]
        out.append(f'| `{f.name}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` | {first} |')
(root / 'INDEX.md').write_text('\n'.join(out) + '\n')
print(f'{sum(1 for p in root.rglob("*") if p.is_file())} files indexed')
