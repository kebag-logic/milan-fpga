#!/usr/bin/env python3
"""Verify selected public receipts, without reading handoffs or review reports."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root, packet = map(Path, sys.argv[1:])
commit = '2c1b14774f3429806ba8d2e51973f1225761ee0c'
prefix = 'review-evidence/fbshard-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])
manifest_bytes = git('show', commit + ':' + prefix + 'MANIFEST.json')
manifest = json.loads(manifest_bytes)
selected = [r for r in manifest if r['file'].startswith('author-r2/receipts/')]
assert len(selected) == 13
legacy = {'control-gate-union-proof.log', 'final-shard-0of3.log', 'final-shard-1of3.log',
          'final-shard-2of3.log', 'head-judge-3-shards.log', 'plant-dropped-capture.log',
          'plant-duplicated-capture.log'}
selected += [r for r in manifest if r['file'].startswith('author/receipts/') and Path(r['file']).name in legacy]
assert len(selected) == 20
rows = []
for entry in selected:
    data = git('show', commit + ':' + prefix + entry['file'])
    sha = hashlib.sha256(data).hexdigest()
    assert sha == entry['published_sha256'], entry['file']
    rows.append({'path': entry['file'], 'sha256': sha, 'bytes': len(data), 'verified': True})
    print('verified:', entry['file'], sha)
    if entry['file'].endswith('head-ci-and-docs-gates.log'):
        text = data.decode()
        assert text.splitlines()[0] == '5392adf989349b68cfbb54d91fd0413c5b745521'
        statuses = [line for line in text.splitlines() if line.startswith('== rc=')]
        assert len(statuses) == 28 and all(line.startswith('== rc=0 ') for line in statuses)
        assert '== overall status=0' in text
        print('28 published gate return codes verified at requested head')
    if entry['file'].endswith('head-ci_events-selftest.log'):
        text = data.decode()
        assert text.splitlines()[0] == '5392adf989349b68cfbb54d91fd0413c5b745521'
        print('contract selftest tail:', '\n'.join(text.splitlines()[-4:]))
    if entry['file'].endswith('delta-from-b7b35193.diff'):
        assert data == git('diff', 'b7b351935f65416c8632c21dd13e08fb2e9c1d9c..5392adf989349b68cfbb54d91fd0413c5b745521')
        print('published delta byte-equals local exact-head delta')
headers = git('cat-file', 'commit', commit).split(b'\n\n')[0]
paths = git('ls-tree', '-r', '--name-only', commit, prefix).decode().splitlines()
signatures = [p for p in paths if p.endswith(('.asc', '.sig', '.minisig'))]
summary = {'commit': commit, 'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(), 'verified_receipts': rows, 'commit_signature_present': b'\ngpgsig ' in headers, 'detached_signature_files': signatures, 'limit': 'Published SHA-256 integrity verified; no cryptographic signer authentication without a signature.'}
(packet / 'public-evidence.json').write_text(json.dumps(summary, indent=2) + '\n')
print('signature present:', summary['commit_signature_present'], '; detached signature files:', signatures)
