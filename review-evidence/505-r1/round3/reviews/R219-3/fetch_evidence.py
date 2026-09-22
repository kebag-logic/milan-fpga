#!/usr/bin/env python3
"""Download selected public receipts at an immutable evidence commit."""
import base64
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
REV = 'ffdfe935dfcc1a8773fa10ca3b0064f377e52ca0'
tree = json.loads((OUT / f'archive-tree-{REV}.json').read_text())
prefix = 'review-evidence/505-r1/'
selected = []
for entry in tree['tree']:
    name = entry['path'].removeprefix(prefix)
    if entry['type'] == 'blob' and entry['path'].startswith(prefix) and (
        name.startswith(('round3/manager/', 'ac5/', 'ac5-act/'))
        or name == 'act-draft-fast/01.log'
    ):
        selected.append(entry)

def fetch(entry):
    args = ['rtk', 'proxy', 'gh', 'api',
            f"repos/kebag-logic/milan-fpga/git/blobs/{entry['sha']}"]
    dest = OUT / 'public-evidence' / entry['path'].removeprefix(prefix)
    if dest.exists():
        data = dest.read_bytes()
    else:
        process = subprocess.run(args, capture_output=True, check=True)
        data = base64.b64decode(json.loads(process.stdout)['content'])
    digest = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
    assert digest == entry['sha']
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return {'path': str(dest.relative_to(OUT)), 'sha': digest, 'size': len(data),
            'argv': args, 'exit': 0, 'archive': REV}

with ThreadPoolExecutor(max_workers=5) as pool:
    receipts = list(pool.map(fetch, selected))
(OUT / 'public-evidence-downloads.json').write_text(json.dumps(
    {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'files': receipts}, indent=2) + '\n')
print(f'Downloaded and Git-blob-verified {len(receipts)} public artifacts at {REV}')
