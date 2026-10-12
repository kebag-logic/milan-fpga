#!/usr/bin/env python3
"""Bind a published author round directory to the evidence MANIFEST.json and its own MANIFEST.sha256.

usage: verify_publication.py <review-evidence/629-b16-r1 dir> <author-rN> <out.json>
"""
import hashlib, json, sys
from pathlib import Path

base, rnd, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
d = base / rnd
man = {e['file']: e for e in json.loads((base / 'MANIFEST.json').read_text())}
own = {}
for line in (d / 'MANIFEST.sha256').read_text().splitlines():
    h, p = line.split(None, 1)
    own[p.lstrip('*').removeprefix('./')] = h
res = {'round': rnd, 'files': 0, 'redacted': 0, 'problems': []}
for f in sorted(p for p in d.rglob('*') if p.is_file()):
    rel = f.relative_to(d).as_posix()
    if rel == 'MANIFEST.sha256':
        continue
    res['files'] += 1
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    e = man.get(f'{rnd}/{rel}')
    if e is None:
        res['problems'].append([rel, 'not in MANIFEST.json']); continue
    if e['published_sha256'] != h:
        res['problems'].append([rel, 'published hash differs'])
    if own.get(rel) != e['original_sha256']:
        res['problems'].append([rel, 'own manifest differs from original_sha256'])
    if (e['original_sha256'] != e['published_sha256']) != e['path_redacted']:
        res['problems'].append([rel, 'redaction flag inconsistent'])
    res['redacted'] += e['path_redacted']
listed = set(own)
present = {p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()} - {'MANIFEST.sha256'}
res['listed_not_present'] = sorted(listed - present)
res['present_not_listed'] = sorted(present - listed)
res['manifest_entries'] = len(man)
res['manifest_sha256'] = hashlib.sha256((base / 'MANIFEST.json').read_bytes()).hexdigest()
out.write_text(json.dumps(res, indent=1) + '\n')
print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in res.items()}))
sys.exit(1 if res['problems'] or res['listed_not_present'] or res['present_not_listed'] else 0)
