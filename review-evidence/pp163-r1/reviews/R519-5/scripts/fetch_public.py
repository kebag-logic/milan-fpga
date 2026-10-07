#!/usr/bin/env python3
"""Read selected public evidence; never fetch another review report."""
import base64
import concurrent.futures
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parents[1]
tree = json.loads(subprocess.check_output(['gh', 'api', 'repos/kebag-logic/milan-fpga/git/trees/350e06ae86bd5372f9f79b5fa5c95e0f3863b5d2?recursive=1']))
prefix = 'review-evidence/pp163-r1/'
def wanted(path):
    rel = path.removeprefix(prefix)
    return path.startswith(prefix) and (
        rel.startswith('author-r4/') or rel.startswith('author-r3/measurement-m3final/')
        or rel in ('MANIFEST.json', 'reviews/R518-2/scripts/reviewer_probes.py')
        or rel.startswith('author-r3/evidence/') and Path(rel).name in (
            'measurement-m3base.json', 'measurement-m3final.json', 'resource-reference-m3.json',
            'source-cones-m3.json', 'rtl-scope-m3final.json', 'cone-summary-m3final-all.txt',
            'final-measurement-tables-m3.md'))
def fetch(entry):
    raw = subprocess.check_output(['gh', 'api', 'repos/kebag-logic/milan-fpga/git/blobs/' + entry['sha']])
    data = base64.b64decode(json.loads(raw)['content'])
    out = packet / 'receipts/public' / entry['path'].removeprefix(prefix)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return {'path': str(out.relative_to(packet)), 'git_blob': entry['sha'], 'bytes': len(data)}
with concurrent.futures.ThreadPoolExecutor(8) as pool:
    rows = list(pool.map(fetch, [x for x in tree['tree'] if x['type'] == 'blob' and wanted(x['path'])]))
(packet / 'receipts/public-fetch.json').write_text(json.dumps(rows, indent=2) + '\n')
print('Fetched', len(rows), 'selected public artifacts; no review reports.')
