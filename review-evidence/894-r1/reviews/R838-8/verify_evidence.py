#!/usr/bin/env python3
"""Verify published author receipts without opening other review reports."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

repo, output = map(Path, sys.argv[1:3])
rev = '9222da670fb7437ee6a0d5c939c44b2af40e2fbe'
prefix = 'review-evidence/894-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=__import__('os').environ | {'GIT_NO_REPLACE_OBJECTS': '1'})
def blob(path):
    return git('show', rev + ':' + prefix + path)
manifest = json.loads(blob('MANIFEST.json'))
entries = [e for e in manifest if e['file'].startswith('author-r13/')]
for e in entries:
    assert hashlib.sha256(blob(e['file'])).hexdigest() == e['published_sha256'], e['file']
print('Published manifest: verified', len(entries), 'author-r13 files')
index = blob('author-r13/INDEX.md').decode()
rows = re.findall(r'^\| `([^`]+)` \| ([0-9,]+) \| `([0-9a-f]{64})` \|$', index, re.M)
redacted = 0
for path, size, digest in rows:
    data = blob('author-r13/' + path)
    entry = next(e for e in entries if e['file'] == 'author-r13/' + path)
    if entry['path_redacted']:
        assert digest == entry['original_sha256'], path
        redacted += 1
        print('Publication redaction mapped to original index digest:', path)
    else:
        assert len(data) == int(size.replace(',', '')), path
        assert hashlib.sha256(data).hexdigest() == digest, path
print('Author index:', len(rows) - redacted, 'exact sizes/digests;', redacted, 'publication redactions mapped via manifest')
print('Evidence commit:', rev)
print('Git signature status:', git('log', '-1', '--format=%G?', rev).decode().strip(), '(N means unsigned; checksum verification is not signature verification)')
selected = [
 'model/flip-1x1-ed0df35b.txt', 'model/flip-8x8-ed0df35b.txt',
 'model/load-check-ed0df35b.txt', 'model/pace-slice-ed0df35b.txt',
 'model/tier-grid-1x1-ed0df35b.txt', 'model/rcs-ed0df35b.txt',
 'legs/joins.txt', 'classes/record-classes-ed0df35b.txt',
 'lane/lane-234bc149/summary.txt',
]
target = output / 'published'
target.mkdir(exist_ok=True)
for path in selected:
    dest = target / path.replace('/', '__')
    dest.write_bytes(blob('author-r13/receipts/' + path))
    print('Receipt:', path)
for local, remote in [('flip-check.txt', 'model/flip-1x1-ed0df35b.txt'), ('load-check.txt', 'model/load-check-ed0df35b.txt')]:
    data = blob('author-r13/receipts/' + remote)
    exact = (output / local).read_bytes()
    print(local + ':', 'byte-identical to published receipt' if exact == data else 'compare output with published wrapper')
