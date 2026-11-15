#!/usr/bin/env python3
"""INDEX.md of an output directory, generated from the files present after sanitize.py ran on them: each file's path,
size and sha256, then every row read back against its file. Exits 1 on a file over 200 KB, on any file carrying one of
the host prefixes given (receipts, scripts and notes alike, so the archive has nothing to redact), or on a row that
does not match its file. usage: index.py OUTDIR TITLE HOST_PREFIX..."""
import hashlib
import sys
from pathlib import Path

out, title, host = Path(sys.argv[1]).resolve(), sys.argv[2], tuple(sys.argv[3:])
assert host, 'name at least one host prefix'
rows, bad = [], []
files = sorted(p for p in out.rglob('*') if p.is_file() and p.name != 'INDEX.md')
for f in files:
    rel = f.relative_to(out).as_posix()
    data = f.read_bytes()
    if len(data) > 200 * 1024:
        bad.append(f'{rel}: {len(data)} B, over 200 KB')
    if any(h.encode() in data for h in host):
        bad.append(f'{rel}: carries a host path')
    rows.append(f'| `{rel}` | {len(data):,} | `{hashlib.sha256(data).hexdigest()}` |')
text = [f'# {title}', '',
        f'Generated from the {len(rows)} files present after sanitizing (`scripts/index.py`), each row read back.',
        'No file here carries a host path, scripts included, so each row is the hash of the bytes as published. '
        'For an earlier packet whose scripts the archive redacted, the archive\'s outer `MANIFEST.json` is '
        'authoritative for those scripts: its `original_sha256` is the INDEX row, `path_redacted` marks the file.',
        '', '| File | Bytes | sha256 |', '|---|---:|---|', *rows, '']
(out / 'INDEX.md').write_text('\n'.join(text))
listed = {}
for line in (out / 'INDEX.md').read_text().splitlines():
    if line.startswith('| `'):
        name, size, digest = [c.strip().strip('`') for c in line.strip('|').split('|')]
        listed[name] = (int(size.replace(',', '')), digest)
for f in files:
    rel = f.relative_to(out).as_posix()
    data = f.read_bytes()
    if listed.get(rel) != (len(data), hashlib.sha256(data).hexdigest()):
        bad.append(f'{rel}: its INDEX row does not match the file')
if len(listed) != len(files):
    bad.append(f'INDEX lists {len(listed)} files, {len(files)} present')
for line in bad:
    print('BAD', line)
print(f'{len(rows)} files indexed, {len(bad)} bad')
sys.exit(1 if bad else 0)
