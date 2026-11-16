#!/usr/bin/env python3
"""Extract only public author receipts and verify their published digests."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
archive = '887dbc6444faac5c0fe736ab8caae37701dc91a5'
prefix = 'review-evidence/917-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
manifest = json.loads(git('show', archive + ':' + prefix + 'MANIFEST.json'))
selected = [r for r in manifest if r['file'].startswith(('author-r1/receipts/', 'author-r2/receipts/', 'author-r3/receipts/')) or r['file'] in ('author-r2/INDEX.md', 'author-r3/INDEX.md')]
for row in selected:
    data = git('show', archive + ':' + prefix + row['file'])
    assert hashlib.sha256(data).hexdigest() == row['published_sha256'], row['file']
    dest = out / 'scratch/evidence' / row['file']
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
print(f'Archive {archive}: {len(selected)} public receipt/index files match MANIFEST.json published_sha256')
print(f'Publication redactions recorded for {sum(r["path_redacted"] for r in selected)} selected files')
print('No independent reviewer reports extracted or read.')
for ref in ('8f73ade5', 'HEAD'):
    for path in ('hdl', 'sw/firmware', 'configs', 'sw/mailbox/mailbox.yaml', 'docs/reference/MAILBOX_CONTRACT.md'):
        print(ref, path, git('rev-parse', f'{ref}:{path}').decode().strip())
print(git('show', '-s', '--format=commit %H%ntree %T%nsignature-status %G?', archive).decode())
