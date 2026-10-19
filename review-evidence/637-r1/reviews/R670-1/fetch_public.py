#!/usr/bin/env python3
"""Retrieve only published receipts, checking their published manifest hashes."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
out = packet / 'scratch/public'
out.mkdir(parents=True, exist_ok=True)
base = 'repos/kebag-logic/milan-fpga/contents/review-evidence/637-r1/'
ref = '?ref=270c5c99c74e88be21806ec5319556981b0f188b'
def get(path):
    return subprocess.check_output(['gh', 'api', base + path + ref,
                                   '-H', 'Accept: application/vnd.github.raw+json'])
manifest = json.loads(get('MANIFEST.json'))
selected = [e for e in manifest if e['file'].startswith('author/receipts/')
            and ('/final/' in e['file'] or '/mutants/' in e['file']
                 or '/route-1x1/head2/' in e['file'] or '/ooc/' in e['file']
                 or e['file'].endswith(('sweep-final-63a187e1.log', 'INDEX.md',
                                        'dynmap-run10.log', 'yosys.log', 'xvlog.log')))]
def fetch(e):
    data = get(e['file'])
    sha = hashlib.sha256(data).hexdigest()
    assert sha == e['published_sha256'], e['file']
    dest = out / e['file']
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return sha + '  ' + e['file']
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    lines = list(pool.map(fetch, selected))
(packet / 'receipts/public-receipts-verified.log').write_text(
    'Published evidence commit 270c5c99c74e88be21806ec5319556981b0f188b\n'
    + '\n'.join(lines) + '\n')
print('Verified', len(lines), 'published receipt hashes')
