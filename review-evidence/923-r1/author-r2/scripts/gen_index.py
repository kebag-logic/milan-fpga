#!/usr/bin/env python3
"""gen_index.py <receipts dir>: INDEX.md listing every file present under the directory, its size and sha256 prefix,
and refusing a file over 200 KB or one that names a host path."""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
rows, bad = [], []
for p in sorted(q for q in root.rglob('*') if q.is_file() and q.name != 'INDEX.md'):
    data = p.read_bytes()
    rel = p.relative_to(root).as_posix()
    if len(data) > 200_000:
        bad.append(f'{rel}: {len(data)} B, over 200 KB')
    if b'/data-2/' in data or b'$WORKSPACE_HOME' in data or b'$VALIDATION_STORAGE' in data:
        bad.append(f'{rel}: names a host path')
    rows.append(f'| `{rel}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` |')
(root / 'INDEX.md').write_text('# Receipts index (generated from the files present)\n\n| File | Bytes | sha256 |\n'
                               '|---|---:|---|\n' + '\n'.join(rows) + '\n')
print(f'{len(rows)} files indexed')
for b in bad:
    print('REFUSED', b)
sys.exit(1 if bad else 0)
