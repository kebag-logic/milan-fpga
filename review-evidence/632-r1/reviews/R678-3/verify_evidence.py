#!/usr/bin/env python3
"""Verify public author receipts against their publication manifest."""
import hashlib
import json
import pathlib
import subprocess
import sys

REV = '7aa121b32be32be9d0ea45840bc9dc19e78e02f7'
PREFIX = 'review-evidence/632-r1/'
out = pathlib.Path(__file__).resolve().parent
repo = pathlib.Path(sys.argv[1]).resolve()
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
manifest = json.loads(git('show', REV + ':' + PREFIX + 'MANIFEST.json'))
records = [r for r in manifest if r['file'].startswith('author-r5/receipts/')]
results = []
for r in records:
    data = git('show', REV + ':' + PREFIX + r['file'])
    actual = hashlib.sha256(data).hexdigest()
    assert actual == r['published_sha256'], r['file']
    results.append({'file': r['file'], 'sha256': actual, 'bytes': len(data), 'path_redacted': r['path_redacted']})
    rel = r['file'].removeprefix('author-r5/receipts/')
    if rel.startswith(('round3/', 'round4/', 'round5/')) or rel == 'INDEX.md':
        path = out / 'scratch' / 'published' / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
(out / 'evidence-hashes.json').write_text(json.dumps(results, indent=2) + '\n')
print('Publication:', REV)
print('Author receipt hashes verified:', len(results))
print('Redacted receipts:', sum(r['path_redacted'] for r in results))
print('No reviewer report or private material read by this script.')
print('Publication commit signature status:', git('show', '-s', '--format=%G?', REV).decode().strip())
