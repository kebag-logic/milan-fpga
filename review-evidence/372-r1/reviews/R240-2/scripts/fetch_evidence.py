#!/usr/bin/env python3
"""Fetch only public corrected-source manager evidence, never private material."""
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

out = Path(__file__).resolve().parents[1]
prefix = 'review-evidence/372-r1/corrected-source2/manager/'
tree = json.loads((out / 'raw/evidence-tree.log').read_text())
assert not tree['truncated']
selected = []
for entry in tree['tree']:
    name = entry['path']
    if entry['type'] != 'blob' or not name.startswith(prefix):
        continue
    relative = name.removeprefix(prefix)
    if (relative.endswith('.json') or relative.startswith(('full-native/', 'manager-builder/'))
            or relative in ['full-suite-logs/ptp_ts.log', 'full-suite-logs/tsn_fuzz.log']):
        selected.append(entry)

def fetch(entry):
    command = ['rtk', 'proxy', 'gh', 'api',
               'repos/kebag-logic/milan-fpga/git/blobs/' + entry['sha']]
    response = json.loads(subprocess.check_output(command))
    content = base64.b64decode(response['content'])
    oid = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
    assert oid == entry['sha'], entry['path']
    target = out / 'public-manager' / entry['path'].removeprefix(prefix)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    return dict(path=entry['path'], blob=oid, bytes=len(content),
                sha256=hashlib.sha256(content).hexdigest(), command=command)

with ThreadPoolExecutor(max_workers=4) as pool:
    receipts = list(pool.map(fetch, selected))
(out / 'raw/public-evidence-manifest.json').write_text(json.dumps(receipts, indent=2) + '\n')
print('Fetched and Git-blob verified', len(receipts), 'public manager artifacts')
