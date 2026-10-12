#!/usr/bin/env python3
"""Fetch explicit paths from the pinned public evidence tree, proving blob identity.

Usage: python3 fetch_public.py PACKET PATH [PATH ...]
Paths are relative to review-evidence/726-r1; output remains scratch-only.
"""
import base64
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys

packet = Path(sys.argv[1])
prefix = 'review-evidence/726-r1/'
revision = '727f29284f7f6a15d6529df6884bd2ef028320d0'
tree_path = packet / 'scratch/evidence-tree.json'
if not tree_path.exists():
    tree_path.parent.mkdir(parents=True, exist_ok=True)
    tree_path.write_bytes(subprocess.check_output([
        'gh', 'api', 'repos/kebag-logic/milan-fpga/git/trees/' + revision + '?recursive=1']))
tree = json.loads(tree_path.read_text())
assert not tree.get('truncated'), 'Evidence tree response is truncated'
entries = {entry['path']: entry for entry in tree['tree']}

def fetch(rel):
    """Download one immutable blob and validate its Git object hash."""
    entry = entries[prefix + rel]
    response = subprocess.check_output(['gh', 'api',
               'repos/kebag-logic/milan-fpga/git/blobs/' + entry['sha']])
    data = base64.b64decode(json.loads(response)['content'])
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert blob == entry['sha']
    dest = packet / 'scratch/public' / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dict(path=prefix+rel, commit=revision, blob=blob,
                sha256=hashlib.sha256(data).hexdigest(), size=len(data))

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fetch, sys.argv[2:]))
out = packet / 'receipts/public-provenance.json'
out.parent.mkdir(parents=True, exist_ok=True)
previous = json.loads(out.read_text()) if out.exists() else []
out.write_text(json.dumps(previous + results, indent=2) + '\n')
print('Verified public blobs:', len(results))
