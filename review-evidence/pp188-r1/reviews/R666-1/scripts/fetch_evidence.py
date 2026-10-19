#!/usr/bin/env python3
"""Download only the explicitly published evidence, validating its manifest."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import sys
import urllib.request

packet = Path(sys.argv[1])
dest = packet / 'scratch/public-evidence'
url = ('https://raw.githubusercontent.com/kebag-logic/milan-fpga/'
       '5baa360ef77eeae71b897a7e5ed7aee01673c6f0/review-evidence/pp188-r1/')
dest.mkdir(parents=True, exist_ok=True)
if not (dest / 'MANIFEST.json').exists():
    with urllib.request.urlopen(url + 'MANIFEST.json', timeout=60) as response:
        (dest / 'MANIFEST.json').write_bytes(response.read())
manifest = json.loads((dest / 'MANIFEST.json').read_text())

def fetch(row):
    path = dest / row['file']
    if not path.exists():
        with urllib.request.urlopen(url + row['file'], timeout=60) as r:
            data = r.read()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    assert sha == row['published_sha256'], row['file']
    return {'file': row['file'], 'bytes': len(data), 'sha256': sha,
            'redacted': row['path_redacted']}

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    rows = list(pool.map(fetch, manifest))
(packet / 'receipts/public-evidence-verified.json').write_text(json.dumps(rows, indent=2)+'\n')
print(f'PASS: {len(rows)} published files match publication manifest', flush=True)
