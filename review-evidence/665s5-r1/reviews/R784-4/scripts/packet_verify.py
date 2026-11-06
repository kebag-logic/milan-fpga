#!/usr/bin/env python3
"""Every author-r4 blob of the evidence tree against MANIFEST.json's published digest. usage: packet_verify.py <tree_r4.txt> <blob dir> <manifest>"""
import hashlib, json, subprocess, sys, concurrent.futures as cf
from pathlib import Path
lines = [l.split(None, 2) for l in Path(sys.argv[1]).read_text().splitlines()]
out = Path(sys.argv[2]); out.mkdir(exist_ok=True)
m = {e['file']: e for e in json.loads(Path(sys.argv[3]).read_text())}
def get(l):
    sha, size, path = l
    rel = path.removeprefix('review-evidence/665s5-r1/')
    if rel == 'MANIFEST.json':
        return None
    d = subprocess.run(['gh', 'api', f'repos/kebag-logic/milan-fpga/git/blobs/{sha}', '-H', 'Accept: application/vnd.github.raw'], capture_output=True).stdout
    return rel, hashlib.sha256(d).hexdigest() == m.get(rel, {}).get('published_sha256'), m.get(rel, {}).get('original_sha256') == m.get(rel, {}).get('published_sha256')
with cf.ThreadPoolExecutor(8) as ex:
    r = [x for x in ex.map(get, lines) if x]
print('author-r4 blobs', len(r), 'digest match', sum(x[1] for x in r), 'unredacted (original == published)', sum(x[2] for x in r))
print('mismatch', [x[0] for x in r if not x[1]])
