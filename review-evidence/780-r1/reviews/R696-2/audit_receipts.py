#!/usr/bin/env python3
"""Verify public receipt bytes against the pinned evidence manifest."""
import hashlib
import json
import os
import subprocess

REV = '3e0d0e08ac6adcb2aa0f43316d800073f2492e6a'
PREFIX = 'review-evidence/780-r1/'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(*args):
    return subprocess.check_output(['git', *args], env=env)
manifest = json.loads(git('show', REV + ':' + PREFIX + 'MANIFEST.json'))
rows = [r for r in manifest if r['file'].startswith('author/receipts/')]
for row in rows:
    data = git('show', REV + ':' + PREFIX + row['file'])
    assert hashlib.sha256(data).hexdigest() == row['published_sha256'], row['file']
print(f'PASS: {len(rows)} public executable receipt files match published SHA-256 manifest')
commit = git('cat-file', 'commit', REV).split(b'\n\n', 1)[0]
print('Evidence commit has embedded signature:', b'\ngpgsig ' in commit)
print('Integrity claim: pinned Git object and published receipt hashes; no cryptographic signer authentication claimed')
for name in ['probe/probe-a032c6d6.log.p780-lines.txt', 'probe/probe-25f05752.log.p780-lines.txt',
             'probe/probe-a032c6d6.rc', 'probe/probe-25f05752.rc',
             'firmware/table.txt', 'milan_dp/summary.txt', 'rtl_fast/combined.txt',
             'sweep/suite-tally.out', 'vivado/route-1x1-check.log', 'vivado/ooc-1x1-check.log',
             'vivado/ooc-8x8-check.log']:
    print('\nARTIFACT: author/receipts/' + name)
    print(git('show', REV + ':' + PREFIX + 'author/receipts/' + name).decode())
