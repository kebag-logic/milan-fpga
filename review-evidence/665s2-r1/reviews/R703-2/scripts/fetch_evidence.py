#!/usr/bin/env python3
"""Fetch the published review-evidence/665s2-r1 subtree at a commit, blob by blob, verifying each blob's git SHA-1.
Usage: fetch_evidence.py COMMIT PREFIX OUTDIR"""
import base64, hashlib, json, subprocess, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
commit, prefix, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
tree = json.loads(subprocess.run(['gh', 'api', f'repos/kebag-logic/milan-fpga/git/trees/{commit}?recursive=1'],
                                 capture_output=True, text=True, check=True).stdout)
assert not tree['truncated']
blobs = [t for t in tree['tree'] if t['type'] == 'blob' and t['path'].startswith(prefix)]
def get(t):
    d = json.loads(subprocess.run(['gh', 'api', f'repos/kebag-logic/milan-fpga/git/blobs/{t["sha"]}'],
                                  capture_output=True, text=True, check=True).stdout)
    data = base64.b64decode(d['content'])
    ok = hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest() == t['sha']
    p = out / t['path'][len(prefix):].lstrip('/')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    return ok
with ThreadPoolExecutor(8) as pool:
    oks = list(pool.map(get, blobs))
print(f'{len(blobs)} blobs fetched, {sum(oks)} git SHA-1 verified, {len(blobs) - sum(oks)} mismatched')
