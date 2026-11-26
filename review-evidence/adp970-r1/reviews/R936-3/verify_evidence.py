#!/usr/bin/env python3
"""Verify public author receipts at immutable evidence commits; no reviewer files are read."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

repo, packet = map(Path, sys.argv[1:3])
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

records = []
for commit, directory in [
    ('40ce56ee579d00874e4c9db98893f0742498aee3', 'adp970-r1'),
    ('af092a85bcda1d60fab649ca42e2b013996ee21e', 'adp970-r2'),
]:
    prefix = 'review-evidence/' + directory + '/'
    manifest = json.loads(git('show', commit + ':' + prefix + 'MANIFEST.json'))
    signed = b'\ngpgsig ' in git('cat-file', 'commit', commit)
    print(f'Evidence commit {commit}: embedded signature present={signed}')
    for entry in manifest:
        name = entry['file']
        if not name.startswith('author/'):
            continue
        data = git('show', commit + ':' + prefix + name)
        digest = hashlib.sha256(data).hexdigest()
        assert digest == entry['published_sha256'], name
        dest = packet / 'scratch' / 'public' / directory / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        records.append(dict(commit=commit, path=prefix + name, sha256=digest, verified=True))
        print(f'PASS {digest}  {prefix}{name}')
print(f'Verified {len(records)} author files. Digest integrity only; no detached signature supplied.')
(packet / 'evidence-integrity.json').write_text(json.dumps(records, indent=2) + '\n')
