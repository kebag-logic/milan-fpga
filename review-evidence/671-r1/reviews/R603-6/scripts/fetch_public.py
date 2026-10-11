#!/usr/bin/env python3
"""Fetch selected public blobs at a fixed evidence commit and verify identity."""
import base64
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys

packet = Path(sys.argv[1]).resolve()
ref = '4c4d44f8a9cc76d7a16945eb555c5b1b1777d084'
base = 'review-evidence/671-r1/author-r6/receipts/r6/'
names = ['MANIFEST.md', 'selftest_final.log', 'builder__driver.log', 'builder__part6.log',
         'equiv_1x1_arty.log', 'equiv_8x8.log', 'term_census.log', 'term_matrix.log',
         'term_views.log', 'r603_5_probe_comparison.log', 'final_gates__summary.log',
         'final_gates__capture.log']
tree_path = packet / 'scratch/evidence-tree.json'
if not tree_path.exists():
    tree_path.parent.mkdir(parents=True, exist_ok=True)
    tree_path.write_bytes(subprocess.check_output([
        'gh', 'api', 'repos/kebag-logic/milan-fpga/git/trees/'+ref+'?recursive=1']))
tree = json.loads(tree_path.read_text())['tree']
entries = {e['path']: e for e in tree}
dest = packet / 'receipts/public-author'
dest.mkdir(exist_ok=True)
def fetch(name):
    path = base + name
    if path not in entries:
        return {'path': path, 'result': 'absent'}
    e = entries[path]
    data = json.loads(subprocess.check_output(['gh', 'api', 'repos/kebag-logic/milan-fpga/git/blobs/'+e['sha']]))
    raw = base64.b64decode(data['content'])
    oid = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert oid == e['sha']
    (dest / name).write_bytes(raw)
    return {'path': path, 'blob': oid, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
            'url': 'https://github.com/kebag-logic/milan-fpga/blob/'+ref+'/'+path}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(fetch, names))
(packet / 'receipts/public-author-provenance.json').write_text(json.dumps(rows, indent=2)+'\n')
print(json.dumps(rows, indent=2))
