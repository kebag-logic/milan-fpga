#!/usr/bin/env python3
"""INDEX.md of an output directory, generated from the files present after sanitize.py ran on them: each file's path,
size and sha256, then every row read back against its file. Exits 1 on a file over 200 KB, on a receipt (anything
under receipts/) carrying a host path, or on a row that does not match its file. usage: index.py OUTDIR"""
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
text = ['# 894-a773 round 12 output index', '',
        f'Generated from the {len(rows)} files present after sanitizing (`index.py`), each row read back.', '',
        '| File | Bytes | sha256 |', '|---|---:|---|', *rows, '']
(out / 'INDEX.md').write_text('\n'.join(text))
# every row's bytes and hash are the file's as it stands: sanitize first, then index, then this check
listed = {}
for line in (out / 'INDEX.md').read_text().splitlines():
    if line.startswith('| `'):
        name, size, digest = [c.strip().strip('`') for c in line.strip('|').split('|')]
        listed[name] = (int(size.replace(',', '')), digest)
present = sorted(p for p in out.rglob('*') if p.is_file() and p.name != 'INDEX.md')
for f in present:
    rel = f.relative_to(out).as_posix()
    data = f.read_bytes()
    if listed.get(rel) != (len(data), hashlib.sha256(data).hexdigest()):
        bad.append(f'{rel}: its INDEX row does not match the file')
if len(listed) != len(present):
    bad.append(f'INDEX lists {len(listed)} files, {len(present)} present')
for line in bad:
    print('BAD', line)
print(f'{len(rows)} files indexed, {len(bad)} bad')
sys.exit(1 if bad else 0)
