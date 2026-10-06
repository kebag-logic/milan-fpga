#!/usr/bin/env python3
"""Fetch only the public B13 evidence inputs used by this review.

Usage: python3 fetch_public.py SCRATCH_PUBLIC_DIRECTORY
"""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import sys
import urllib.request

dest = Path(sys.argv[1])
dest.mkdir(parents=True, exist_ok=True)
tree_url = 'https://api.github.com/repos/kebag-logic/milan-fpga/git/trees/06d2846c32ad1ba6f1043620623e8b4db09cbf24?recursive=1'
tree_path = dest / 'evidence-tree.json'
if not tree_path.exists():
    with urllib.request.urlopen(tree_url, timeout=30) as r:
        tree_path.write_bytes(r.read())
tree = json.loads(tree_path.read_text())
assert not tree['truncated']
assert tree['sha'] == '06d2846c32ad1ba6f1043620623e8b4db09cbf24'
excluded = {'HANDOFF.md', 'REVIEW-READY.md', 'TAKEN.md'}
files = [x for x in tree['tree'] if x['type'] == 'blob' and x['path'] not in excluded]
def fetch(x):
    name = Path(x['path'])
    assert not name.is_absolute() and '..' not in name.parts
    f = dest / 'author' / name
    f.parent.mkdir(parents=True, exist_ok=True)
    if not f.exists():
        url = 'https://raw.githubusercontent.com/kebag-logic/milan-fpga/b2bb3c89096c8fd4712a39677bae96e5987ccbbd/review-evidence/667-b13-r1/author/' + x['path']
        with urllib.request.urlopen(url, timeout=30) as r:
            f.write_bytes(r.read())
    b = f.read_bytes()
    assert len(b) == x['size']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == x['sha']
    return len(b)
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
    sizes = list(pool.map(fetch, files))
print('PASS:',len(sizes),'public inputs,',sum(sizes),'bytes, exact published Git blobs.')
