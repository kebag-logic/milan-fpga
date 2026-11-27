"""Check a receipt packet's FILES.tsv inventory against the files on disk: every listed file present with its
bytes and SHA256, and no unlisted file. usage: python3 -I verify_inventory.py RECEIPTS_DIR"""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
rec = json.loads((root / 'FILES.manifest.json').read_text())
text = b''.join((root / p['file']).read_bytes() for p in rec['parts'])
assert hashlib.sha256(text).hexdigest() == rec['sha256'], 'inventory hash'
rows = [l.split('\t') for l in text.decode().splitlines()[1:] if l]
bad = 0
for path, size, digest in rows:
    f = root / path
    if not f.is_file():
        print('MISSING', path); bad += 1; continue
    h = hashlib.sha256()
    with f.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    if f.stat().st_size != int(size) or h.hexdigest() != digest:
        print('MISMATCH', path); bad += 1
listed = {r[0] for r in rows} | {'FILES.manifest.json'} | {p['file'] for p in rec['parts']}
extra = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and str(p.relative_to(root)) not in listed)
for e in extra:
    print('UNLISTED', e); bad += 1
print(f'RESULT: {"PASS" if not bad else "FAIL"} listed={len(rows)} bad={bad} total_bytes={sum(int(r[1]) for r in rows)}')
sys.exit(1 if bad else 0)
