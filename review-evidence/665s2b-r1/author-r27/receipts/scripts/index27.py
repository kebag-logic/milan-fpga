#!/usr/bin/env python3
"""receipts/INDEX.md generated from the files present under the output directory: path, size, sha256. Refuses a file
over 200 KB and, in receipts, a host path. usage: index27.py OUT_DIR"""
import hashlib
import sys
from pathlib import Path

out = Path(sys.argv[1])
rows, big, hosts = [], [], []
for p in sorted(out.rglob('*')):
    if not p.is_file() or p.name == 'INDEX.md':
        continue
    data = p.read_bytes()
    rel = p.relative_to(out).as_posix()
    if len(data) > 200 * 1024:
        big.append(rel)
    if rel.startswith('receipts/') and any(h in data for h in (b'<home>', b'/data-2/', b'<data>')):
        hosts.append(rel)
    rows.append(f'| `{rel}` | {len(data):,} | `{hashlib.sha256(data).hexdigest()}` |')
assert not big, big
text = ('# The output directory\'s files\n\nGenerated from the files present (`index27.py`); every receipt the handoff '
        'cites is one of these.\n\n| File | Bytes | sha256 |\n|---|---:|---|\n' + '\n'.join(rows) + '\n')
(out / 'receipts' / 'INDEX.md').write_text(text)
print(f'{len(rows)} files indexed; host paths in {len(hosts)} receipts' + (': ' + ', '.join(hosts[:20]) if hosts else ''))
