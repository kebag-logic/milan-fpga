#!/usr/bin/env python3
"""Fetch selected public Git blobs and verify bytes against immutable trees."""
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent

def selected(name, row):
    path = row['path']
    if row['type'] != 'blob':
        return False
    if name == 'triage':
        return True
    suffix = path.split('review-evidence/520-r1/', 1)[1]
    if suffix.startswith('source/manager/'):
        s = suffix.removeprefix('source/manager/')
        return s.count('/') == 0 or s.startswith(('full-native/', 'manager-builder/', 'yosys-results/'))
    return suffix == 'MANIFEST.json' or suffix in (
        'author/FINAL-RECEIPT.json', 'author/final-source.json',
        'author/final-control-summary.json', 'author/audit_pp.py', 'author/real_pp_probe.py',
        'author/inventory-before.txt', 'author/inventory-final.txt',
    ) or suffix.startswith('author/final-pp/')

def fetch(item):
    name, row = item
    target = OUT / 'public-evidence' / row['path']
    if target.exists():
        data = target.read_bytes()
    else:
        p = subprocess.run(['rtk', 'proxy', 'gh', 'api',
            'repos/kebag-logic/milan-fpga/git/blobs/' + row['sha']], capture_output=True, check=True)
        data = base64.b64decode(json.loads(p.stdout)['content'])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert oid == row['sha'], str(target)
    return {'path': row['path'], 'blob': oid, 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(), 'source': name}

def main():
    items = []
    for name in ('public', 'triage'):
        rows = json.loads((OUT / (name + '-tree.json')).read_text())['entries']
        items += [(name, row) for row in rows if selected(name, row)]
    with ThreadPoolExecutor(max_workers=4) as pool:
        receipts = list(pool.map(fetch, items))
    (OUT / 'public-download-receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')
    print(f'Fetched and Git-blob verified {len(receipts)} immutable public files')

if __name__ == '__main__':
    main()
