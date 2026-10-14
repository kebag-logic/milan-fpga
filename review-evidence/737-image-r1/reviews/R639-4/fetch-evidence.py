#!/usr/bin/env python3
"""Fetch only public author executable evidence; never another review report."""
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(parents=True, exist_ok=True)
tree_file = scratch / 'evidence-tree.json'
if not tree_file.exists():
    tree_file.write_bytes(subprocess.check_output(['gh', 'api',
        'repos/kebag-logic/milan-fpga/git/trees/42bb379cf9e8eca0161122b8a1919819455bc84c?recursive=1']))
tree = json.loads(tree_file.read_text())['tree']
prefix = 'review-evidence/737-image-r1/author-r4/'
selected = [x for x in tree if x['type'] == 'blob' and x['path'].startswith(prefix)
            and Path(x['path']).name.startswith(('round4-', 'builder-', 'cold-comparison',
                 'candidate-a-validation', 'candidate-b-validation', 'round3-buildx', 'runner-version',
                 'cpu-tree-proof', 'final-tree-check'))
            and not x['path'].endswith('.md')]

def fetch(row):
    dest = packet / 'scratch/public' / Path(row['path']).name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        raw = subprocess.check_output(['gh', 'api', 'repos/kebag-logic/milan-fpga/git/blobs/' + row['sha']])
        dest.write_bytes(base64.b64decode(json.loads(raw)['content']))
    data = dest.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert actual == row['sha'] and len(data) == row['size']
    return dict(path=row['path'], blob=actual, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))

with ThreadPoolExecutor(max_workers=8) as pool:
    records = list(pool.map(fetch, selected))
(packet / 'public-evidence-fetch.json').write_text(json.dumps(records, indent=2) + '\n')
print('Authenticated', len(records), 'public evidence blobs')
if not (scratch / 'hosted-docs.log').exists():
    (scratch / 'hosted-docs.log').write_bytes(subprocess.check_output(['gh','api','--allow-escape-sequences',
        'repos/kebag-logic/milan-fpga/actions/jobs/115923539474/logs']))
if not (scratch / 'runner-readme.md').exists():
    payload = subprocess.check_output(['gh','api',
        'repos/actions/runner-images/contents/images/ubuntu/Ubuntu2404-Readme.md?ref=ubuntu24/20261004.327'])
    (scratch / 'runner-readme.md').write_bytes(base64.b64decode(json.loads(payload)['content']))
