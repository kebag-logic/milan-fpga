"""Verify every file under a prefix of a published evidence tree against MANIFEST.json published_sha256, and list unlisted files."""
import hashlib, json, sys
from pathlib import Path
base = Path(sys.argv[1]); prefix = sys.argv[2].rstrip('/') + '/'
sel = {e['file']: e['published_sha256'] for e in json.load(open(base / 'MANIFEST.json')) if e['file'].startswith(prefix)}
bad = 0
for k, v in sorted(sel.items()):
    p = base / k
    h = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'MISSING'
    if h != v: bad += 1; print('MISMATCH', k, v, h)
present = {str(p.relative_to(base)) for p in (base / prefix).rglob('*') if p.is_file()}
unl = sorted(present - set(sel))
for k in unl: print('UNLISTED', k)
print(f'listed={len(sel)} present={len(present)} mismatches={bad} unlisted={len(unl)}')
