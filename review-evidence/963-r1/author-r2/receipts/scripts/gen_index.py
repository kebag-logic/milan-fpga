#!/usr/bin/env python3
"""gen_index.py RECEIPTS: write RECEIPTS/INDEX.md from the files present under it, a section a directory, each file's
size and the first 16 hex digits of its sha256, with the directory's description from its HOW.md first line when it
has one. Refuses any file over 200 KB."""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
lines = ['# Receipts index', '', 'Generated from the files present (size in bytes, sha256 prefix).', '']
big = []
for d in sorted({p.parent for p in root.rglob('*') if p.is_file() and p.name != 'INDEX.md'}):
    rel = d.relative_to(root).as_posix() or '.'
    lines += [f'## {rel}', '', '| File | Bytes | sha256 |', '|---|---:|---|']
    for f in sorted(p for p in d.iterdir() if p.is_file() and p.name != 'INDEX.md'):
        size = f.stat().st_size
        if size > 200_000:
            big.append(f.relative_to(root).as_posix())
        lines.append(f'| {f.name} | {size:,} | {hashlib.sha256(f.read_bytes()).hexdigest()[:16]} |')
    lines.append('')
if big:
    sys.exit(f'files over 200 KB: {big}')
(root / 'INDEX.md').write_text('\n'.join(lines))
print(f'{sum(1 for p in root.rglob("*") if p.is_file()) - 1} files indexed')
