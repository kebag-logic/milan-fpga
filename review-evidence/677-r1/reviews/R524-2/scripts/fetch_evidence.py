#!/usr/bin/env python3
"""Read selected public executable evidence and verify its published hashes."""
import argparse
import base64
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess

REF = '412c0f10e12755a47f79ec3f90e08ef5d2ecaa47'
PREFIX = 'review-evidence/677-r1/'
FILES = ('author/evidence.json', 'author/logs/coverage-check.log',
         'author/logs/erased-end-asan.log', 'author/logs/ctrl.log',
         'author/logs/nvm-controls.log', 'author/nvm-campaign.json')
ap = argparse.ArgumentParser()
ap.add_argument('packet', type=Path)
args = ap.parse_args()
receipts = args.packet / 'receipts'
manifest = json.loads((receipts / 'source-evidence-manifest.json').read_text())
expected = {item['file']: item['published_sha256'] for item in manifest}
out = receipts / 'source-evidence'
out.mkdir(exist_ok=True)

def fetch(path):
    endpoint = f'repos/kebag-logic/milan-fpga/contents/{PREFIX}{path}?ref={REF}'
    obj = json.loads(subprocess.check_output(['rtk', 'proxy', 'gh', 'api', endpoint]))
    raw = base64.b64decode(obj['content'])
    sha = hashlib.sha256(raw).hexdigest()
    assert sha == expected[path]
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == obj['sha']
    (out / Path(path).name).write_bytes(raw)
    return {'path': PREFIX + path, 'ref': REF, 'git_blob': obj['sha'],
            'sha256': sha, 'manifest_match': True, 'bytes': len(raw)}

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fetch, FILES))
print(json.dumps({'result': 'PASS', 'verified': results}, indent=2))
