#!/usr/bin/env python3
"""Copy receipts into the output directory: host paths replaced by placeholders, files over 200 KB not copied
(their SHA-256 and size go to not-copied.txt). usage: publish.py DEST SRC... (SRC is a file or a directory)"""
import hashlib, shutil, sys
from pathlib import Path

LIMIT = 200 * 1024
SUBST = [('<scratch>', '<scratch>'), ('<lanes>', '<lanes>'),
         ('<tools>', '<tools>'), ('<management>', '<management>'), ('<home>', '<home>')]
dest = Path(sys.argv[1])
dest.mkdir(parents=True, exist_ok=True)
skipped = []
for arg in sys.argv[2:]:
    src = Path(arg)
    files = [src] if src.is_file() else sorted(p for p in src.rglob('*') if p.is_file())
    for f in files:
        rel = f.name if src.is_file() else f.relative_to(src).as_posix()
        data = f.read_bytes()
        out = dest / rel
        if len(data) > LIMIT:
            skipped.append(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {rel}')
            continue
        try:
            text = data.decode()
            for a, b in SUBST:
                text = text.replace(a, b)
            data = text.encode()
        except UnicodeDecodeError:
            pass
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
if skipped:
    with (dest / 'not-copied.txt').open('a') as f:
        f.write('\n'.join(skipped) + '\n')
print(dest, 'skipped', len(skipped))
