#!/usr/bin/env python3
"""Fetch immutable public round-8 evidence and verify published byte hashes."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys

COMMIT = 'c9d217d5fa998695e490d150e1da3ce6e3046234'
ROOT = Path(__file__).resolve().parent
PREFIX = 'author-r8/receipts/round8/'

def fetch(path):
    return subprocess.check_output(['gh', 'api',
        'repos/kebag-logic/milan-fpga/contents/review-evidence/632-r1/' + path + '?ref=' + COMMIT,
        '-H', 'Accept: application/vnd.github.raw+json'])

def one(entry):
    data = fetch(entry['file'])
    digest = hashlib.sha256(data).hexdigest()
    assert digest == entry['published_sha256'], entry['file']
    relative = entry['file'][len(PREFIX):]
    target = ROOT / 'public-round8' / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {'file': relative, 'bytes': len(data), 'sha256': digest,
            'matches_published_manifest': True, 'path_redacted': entry['path_redacted']}

def main():
    manifest = json.loads(fetch('MANIFEST.json'))
    selected = [e for e in manifest if e['file'].startswith(PREFIX)]
    (ROOT / 'public-round8-manifest.json').write_text(json.dumps(selected, indent=2) + '\n')
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(one, selected))
    (ROOT / 'receipt-hash-audit.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'PASS: {len(results)} round-8 files match immutable published SHA-256 values')

if __name__ == '__main__':
    main()
