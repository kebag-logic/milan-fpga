#!/usr/bin/env python3
"""Verify published author receipts against the archive manifest; never read reviewer packets."""
import hashlib
import json
import pathlib
import subprocess
import sys

repo = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(__file__).resolve().parent
archive = '43bf7e3e6fe2065df264dbf23256381436f7eed6'
prefix = 'review-evidence/923-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
manifest = json.loads(git('show', archive + ':' + prefix + 'MANIFEST.json'))
rows = [r for r in manifest if r['file'].startswith(('author-r1/', 'author-r2/', 'author-r3/'))]
dest = out / 'scratch' / 'public-author'
dest.mkdir(parents=True, exist_ok=True)
for r in rows:
    data = git('show', archive + ':' + prefix + r['file'])
    actual = hashlib.sha256(data).hexdigest()
    assert actual == r['published_sha256'], r['file']
    path = dest / r['file']
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
print('Archive:', archive)
print('Manifest sha256:', hashlib.sha256(git('show', archive + ':' + prefix + 'MANIFEST.json')).hexdigest())
print('Author files verified:', len(rows))
print('Published files with path redaction:', sum(r['path_redacted'] for r in rows))
print('All published SHA-256 values match. No reviewer report was read.')
print('Commit signature headers:', 'present' if b'gpgsig ' in git('cat-file', 'commit', archive) else 'absent')
print('Content integrity is verified; no independent cryptographic signer authentication is claimed.')
