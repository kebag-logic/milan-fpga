#!/usr/bin/env python3
"""Check an author packet's INDEX.md rows (path, bytes, sha256) against the files present. usage: verify_index.py DIR"""
import hashlib, pathlib, re, sys
d = pathlib.Path(sys.argv[1])
rows = re.findall(r'^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|', (d / 'INDEX.md').read_text(), re.M)
bad = []
for p, b, h in rows:
    data = (d / p).read_bytes()
    if hashlib.sha256(data).hexdigest() != h or len(data) != int(b.replace(',', '')):
        bad.append(f'{p}: indexed {b} B {h[:16]}..., present {len(data):,} B {hashlib.sha256(data).hexdigest()[:16]}...')
present = {str(x.relative_to(d)) for x in d.rglob('*') if x.is_file() and x.name != 'INDEX.md'}
unindexed = sorted(present - {r[0] for r in rows})
print(f'{len(rows)} rows, {len(present)} files, {len(bad)} mismatched, {len(unindexed)} unindexed')
for line in bad + [f'unindexed: {u}' for u in unindexed]:
    print(' ', line)
