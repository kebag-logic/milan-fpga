#!/usr/bin/env python3
"""audit_index.py DIR: check each INDEX.md row (file, bytes, sha256 prefix) against DIR's files, and list
files present but not indexed. Prints a summary line; exit 1 on any mismatch or missing file."""
import hashlib, re, sys
from pathlib import Path
d = Path(sys.argv[1])
rows = re.findall(r'^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{16})` \|', (d / 'INDEX.md').read_text(), re.M)
bad = missing = 0
for name, size, pref in rows:
    p = d / name
    if not p.is_file():
        missing += 1; print('MISSING', name); continue
    b = p.read_bytes()
    if len(b) != int(size.replace(',', '')) or hashlib.sha256(b).hexdigest()[:16] != pref:
        bad += 1; print('DIFFER', name, len(b), hashlib.sha256(b).hexdigest()[:16], size, pref)
listed = {n for n, _, _ in rows}
extra = sorted(str(p.relative_to(d)) for p in d.rglob('*') if p.is_file() and str(p.relative_to(d)) not in listed
               and p.name != 'INDEX.md')
for e in extra: print('UNINDEXED', e)
print(f'{len(rows)} indexed, {len(rows)-bad-missing} match, {bad} differ, {missing} missing, {len(extra)} unindexed')
sys.exit(1 if bad or missing else 0)
