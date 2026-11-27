#!/usr/bin/env python3
"""Verify published census against its outer and inner integrity records."""
import hashlib, json, subprocess, sys
from pathlib import Path
repo, root = Path(sys.argv[1]), Path(sys.argv[2])
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
prefix = 'author-r8/receipts/census-extract/'
outer = json.loads((root / 'MANIFEST.json').read_text())
rows = [r for r in outer if r['file'].startswith(prefix)]
assert len(rows) == 762, len(rows)
for r in rows:
    assert r['original_sha256'] == r['published_sha256'] == sha(root / r['file']), r['file']
    assert not r['path_redacted'], r['file']
print(f'PASS outer: all {len(rows)} census files original == published == actual')
prior = json.loads(subprocess.check_output(['git', '-C', str(repo), 'show', '0cad829e^:review-evidence/artysplit-r1/MANIFEST.json']))
repaired = [r for r in prior if r['file'].startswith(prefix) and r['original_sha256'] != r['published_sha256']]
assert len(repaired) == 27, len(repaired)
print('PASS all 27 formerly transformed parts restored to original digest')
for r in repaired:
    print('RESTORED', r['file'], r['original_sha256'])
extract = root / prefix
inner = json.loads((extract / 'FILES.json').read_text())
for r in inner:
    assert sha(extract / r['path']) == r['sha256'], r['path']
print(f'PASS inner FILES: {len(inner)} case files')
census = json.loads((extract / 'census.json').read_text())
assert len(census['cases']) == 147
for r in census['cases']:
    assert sha(extract / r['manifest']) == r['sha256'], r['case']
print('PASS all 147 manifest hashes; source_head=' + census['source_head'])
print('QUALIFICATION SHA256', sha(extract / 'published-qualification.json'))
print('PASS receipt regrader must next verify assembled parts and complete grades')

receipts = root / 'author-r8/receipts'
record = json.loads((receipts / 'FILES.manifest.json').read_text())
data = b''
for part in record['parts']:
    path = receipts / part['file']
    assert path.stat().st_size == part['bytes'] and sha(path) == part['sha256']
    data += path.read_bytes()
assert len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256']
listed = data.decode().splitlines()[1:]
for line in listed:
    name, size, digest = line.split('\t')
    path = receipts / name
    assert path.stat().st_size == int(size) and sha(path) == digest, name
assert len(listed) == 814
print('PASS complete author FILES inventory: 814 listed files (INDEX.md outside inventory by design)')
