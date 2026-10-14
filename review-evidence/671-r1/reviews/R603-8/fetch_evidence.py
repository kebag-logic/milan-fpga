#!/usr/bin/env python3
"""Fetch only author executable receipts from the public pinned evidence tree."""
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
(root / 'scratch').mkdir(exist_ok=True)
index = root / 'scratch/evidence-tree.json'
if not index.exists():
    index.write_bytes(subprocess.check_output(['gh','api',
        'repos/kebag-logic/milan-fpga/git/trees/10d91cdbd763f66c41fc87f3356d516a5610e746?recursive=1']))
tree = json.loads(index.read_text())['tree']
prefix = 'review-evidence/671-r1/author-r8/receipts/r8/'
names = {'GATE-TABLE-R8.md', 'GATES.json', 'CAPTURE-ARTIFACTS.json',
         'capture52-products.json', 'compare-products.log', 'assemble.log', 'refresh.log',
         'lane-input-identity.json', 'host-selftest.log', 'nvm-cosim-retry.log',
         'service-budget.log', 'firmware-size-final.log', 'term-census-retry.log',
         'term-matrix.log', 'term-views.log', 'full-control-comparison.json',
         'act-flat-selftest-final.log', 'act-selftest-final.log', 'ci-scope-final.log',
         'ci-events-final.log', 'final-gates-final.log', 'docs-replica-final.log',
         'builder-1-retry.log', 'builder-2.log', 'builder-3.log', 'builder-4.log',
         'builder-5.log', 'builder-6.log', 'capture52-driver-a.log', 'capture52-driver-b.log'}
selected = [x for x in tree if x['type']=='blob' and x['path'].startswith(prefix)
            and (x['path'][len(prefix):] in names or 'capture52-' in x['path']
                 or x['path'].endswith('.measurement.json'))]
(root / 'public').mkdir(exist_ok=True)

def fetch(item):
    data = json.loads(subprocess.check_output(['gh', 'api',
        'repos/kebag-logic/milan-fpga/git/blobs/' + item['sha']]))
    content = base64.b64decode(data['content'])
    blob = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
    assert blob == item['sha']
    dest = root / 'public' / item['path'].removeprefix(prefix)
    dest.write_bytes(content)
    return dict(path=item['path'], blob=blob, sha256=hashlib.sha256(content).hexdigest(),
                local=str(dest.relative_to(root)))

with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(fetch, selected))
(root / 'public-provenance.json').write_text(json.dumps(results, indent=2) + '\n')
print('Verified and fetched', len(results), 'public author executable receipts; no private material or reviewer reports.')
