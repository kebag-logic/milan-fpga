#!/usr/bin/env python3
"""Verify review-evidence/b2-r1/MANIFEST.json at the archive head against the
extracted tree: every listed file's published_sha256 and every extracted file
listed. Usage: archive_manifest_r2.py <extracted b2-r1 dir> [skip-prefix ...]"""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1]); skip = tuple(sys.argv[2:])
man = json.load(open(root / 'MANIFEST.json'))
ent = man if isinstance(man, list) else man.get('files', man)
ok = bad = skipped = redacted = 0
listed = set()
for e in ent:
    f = e['file']; listed.add(f)
    if f.startswith(skip):
        skipped += 1; continue
    p = root / f
    h = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
    if h == e['published_sha256']:
        ok += 1
        if e.get('original_sha256') and e['original_sha256'] != h:
            redacted += 1
    else:
        bad += 1; print('MISMATCH', f)
extra = [p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()
         and p.name != 'MANIFEST.json' and p.relative_to(root).as_posix() not in listed]
print(f'entries {len(ent)}: verified {ok} (of which redacted copies {redacted}), mismatched {bad}, skipped {skipped} {skip}')
print('extracted files not listed:', len(extra), extra[:5])
