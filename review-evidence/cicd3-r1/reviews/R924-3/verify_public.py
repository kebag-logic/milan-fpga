#!/usr/bin/env python3
"""Usage: python3 verify_public.py CHECKOUT. Verify published objects without checking out reports."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
rev = '22b3d7ad1e8bca3a5b783af5c8bd2446edc2cc9a'
prefix = 'review-evidence/cicd3-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])
def read(path):
    return git('show', f'{rev}:{prefix}{path}')
manifest = json.loads(read('MANIFEST.json'))
rows = [r for r in manifest if r['file'].startswith('author-r8/')]
for row in rows:
    assert hashlib.sha256(read(row['file'])).hexdigest() == row['published_sha256'], row['file']
files = git('ls-tree', '-r', '--name-only', rev, prefix+'author-r8').decode().splitlines()
assert {prefix+r['file'] for r in rows} == set(files)
comparisons = []
for leg in (0, 1):
    old = json.loads(read(f'author-r8/receipts/local/fr-old/{leg}.json'))
    new = json.loads(read(f'author-r8/receipts/local/fr-fr/{leg}.json'))
    assert new['head'] == 'b0f2bc1a784d9f006204491c883ac2b1783e970a'
    assert new['tree'] == 'bb0c6d59a6e22c499de562a642978b73c998c653'
    assert old['head'] == '9c62539365fea8316dae2b9fd7c68defeff5cb31'
    assert old['results'] == new['results']
    assert old['inventory'] == new['inventory']
    comparisons += new['results']
    for side in ('fr-old', 'fr-fr'):
        print(f'{side} leg {leg}: '+read(f'author-r8/receipts/local/{side}/{leg}.time').decode().strip())
print(json.dumps({'publication_commit':rev, 'files_verified':len(rows),
                  'redacted_files':sum(r['path_redacted'] for r in rows),
                  'follow_ring_equal_results': comparisons,
                  'commit_signature_status':git('show','-s','--format=%G?',rev).decode().strip()}, indent=2))
print('PASS: every author-r8 publication hash matched; both follow_ring piece result tables identical')
