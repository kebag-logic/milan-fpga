"""Verify a packet's INDEX.md rows (| `path` | bytes | `sha256` |) against the files beside it.
Usage: python3 -I verify_index.py <packet-dir> [...]"""
import hashlib
import re
import sys
from pathlib import Path

ok = True
for d in map(Path, sys.argv[1:]):
    rows = re.findall(r'^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|', (d / 'INDEX.md').read_text(), re.M)
    bad = []
    for rel, size, digest in rows:
        f = d / rel
        if not f.is_file():
            bad.append(f'missing {rel}')
            continue
        b = f.read_bytes()
        if len(b) != int(size.replace(',', '')) or hashlib.sha256(b).hexdigest() != digest:
            bad.append(f'mismatch {rel}')
    listed = {r[0] for r in rows}
    extra = sorted(str(p.relative_to(d)) for p in d.rglob('*') if p.is_file() and p.name != 'INDEX.md'
                   and str(p.relative_to(d)) not in listed)
    print(f'{d.name}: {len(rows)} rows, {len(bad)} bad {bad}, unlisted {extra}')
    ok &= not bad
sys.exit(0 if ok else 1)
