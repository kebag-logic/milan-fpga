#!/usr/bin/env python3
"""Audit published receipt hashes and job inventories without executing them."""
import hashlib
import json
from pathlib import Path
import sys
import yaml

root, archive = map(Path, sys.argv[1:3])
manifest = json.loads((archive / 'MANIFEST.json').read_text())
verified = 0
for item in manifest:
    if '/receipts/' not in item['file']:
        continue
    data = (archive / item['file']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == item['published_sha256'], item['file']
    verified += 1
print('published receipt hashes verified:', verified)
workflow = yaml.safe_load((root / '.github/workflows/docs.yml').read_text())
count = 0
for file in sorted((archive / 'author-r2/receipts/logs').glob('*/summary.json')):
    summary = json.loads(file.read_text())
    assert summary['head'] == 'ee5c6f922a5863e25cef5bbc5f37289acf4e4777'
    job = summary['job']
    assert summary['result'] == 'success'
    expected = [s['id'] for s in workflow['jobs'][job]['steps']]
    assert [r['id'] for r in summary['rows']] == expected, job
    runs = [r for r in summary['rows'] if r['action'] == 'run']
    for row in runs:
        assert row['rc'] == 0, (job, row)
        log = file.parent / row['log']
        if not log.exists():
            assert log.with_suffix(log.suffix + '.sha256').exists()
            print('raw log unavailable; published digest only:', job, row['id'])
    count += len(runs)
    print(job, 'head verified; workflow row inventory exact;', len(runs), 'run steps, all rc=0')
print('total run steps:', count)
assert count == 71
print('Hosted recording/upload, package resolution and collector union were not replayed.')
print('The second builder leg reports 16 NOT RUN cases; no elaboration or hardware proof is inferred.')
