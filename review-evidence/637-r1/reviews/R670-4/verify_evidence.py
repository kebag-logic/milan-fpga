#!/usr/bin/env python3
"""Verify immutable public receipt bytes; extract current composition receipts only."""
import hashlib
import json
import pathlib
import subprocess
import sys

repo = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]).resolve()
commit = '1980192f9c93b1bcdeea1aa40daa64171f4ddaac'
prefix = 'review-evidence/637-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
manifest_bytes = git('show', commit + ':' + prefix + 'MANIFEST.json')
manifest = json.loads(manifest_bytes)
rows = [r for r in manifest if r['file'].startswith('author-r3c/')]
assert rows
print('Evidence commit', commit)
print('Manifest SHA256', hashlib.sha256(manifest_bytes).hexdigest())
count = 0
redacted = 0
for row in rows:
    name = row['file']
    data = git('show', commit + ':' + prefix + name)
    digest = hashlib.sha256(data).hexdigest()
    assert digest == row['published_sha256'], name
    count += 1
    redacted += bool(row['path_redacted'])
    if name.startswith('author-r3c/receipts/round3c/'):
        dst = out / 'published' / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
print('PASS published SHA256 entries', count, 'path-redacted entries', redacted)
header = git('cat-file', 'commit', commit).split(b'\n\n', 1)[0]
print('Commit signature present:', b'\ngpgsig ' in header)
print('Hash consistency verifies published bytes, not execution provenance or a signature.')
