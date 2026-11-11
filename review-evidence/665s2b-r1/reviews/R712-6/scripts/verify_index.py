"""Verify every `| path | bytes | sha256 |` row of an INDEX.md against the files beside it, and list files the index
omits. Also verify MANIFEST.json entries under a prefix if given. Usage: python3 -I verify_index.py <dir> [manifest prefix]"""
import hashlib, json, re, sys
from pathlib import Path
d = Path(sys.argv[1])
rows = re.findall(r'^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|', (d / 'receipts/INDEX.md').read_text(), re.M)
bad = 0
for p, n, h in rows:
    f = d / p
    if not f.is_file():
        print('MISSING', p); bad += 1; continue
    b = f.read_bytes()
    if len(b) != int(n.replace(',', '')) or hashlib.sha256(b).hexdigest() != h:
        print('MISMATCH', p); bad += 1
listed = {p for p, _, _ in rows}
extra = [str(f.relative_to(d)) for f in d.rglob('*') if f.is_file() and str(f.relative_to(d)) not in listed]
print(f'index rows {len(rows)}, bad {bad}, files not in index {len(extra)}: {extra[:10]}')
if len(sys.argv) > 2:
    m = json.load(open(sys.argv[2])); pre = sys.argv[3]
    ent = [e for e in m if str(e.get('path', '')).startswith(pre)]
    mb = 0
    for e in ent:
        f = Path(sys.argv[2]).parent.parent.parent / e['path']
        if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != e.get('sha256'):
            mb += 1
    print(f'manifest entries under {pre}: {len(ent)}, bad {mb}; keys {sorted(ent[0]) if ent else None}')
