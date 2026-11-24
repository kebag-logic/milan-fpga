"""Recompute an author packet's receipts/INDEX.md sha256 prefixes and byte counts, and check MANIFEST.json entries.

usage: python3 -I -B verify_evidence.py <extracted review-evidence/train1123-r1 dir> <manifest.json> <packet name>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

root, manifest, name = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()), sys.argv[3]
rec = root / name / 'receipts'
bad = 0
for m in re.finditer(r'^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]+)` \|', (rec / 'INDEX.md').read_text(), re.M):
    path, size, pre = m.group(1), int(m.group(2).replace(',', '')), m.group(3)
    data = (rec / path).read_bytes()
    ok = hashlib.sha256(data).hexdigest().startswith(pre) and len(data) == size
    bad += not ok
    print('ok ' if ok else 'BAD', pre, path)
entries = [e for e in manifest if isinstance(e, dict) and str(e.get('file', '')).startswith(f'{name}/')]
print(f'# MANIFEST.json entries under {name}/: {len(entries)}; keys {sorted(entries[0]) if entries else None}')
for e in entries:
    f = root / e['file']
    h = hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None
    want = e.get('published_sha256')
    ok = h is not None and (want is None or h == want)
    bad += not ok
    if not ok:
        print('BAD manifest', e)
print(f'mismatches: {bad}')
