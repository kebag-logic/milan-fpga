#!/usr/bin/env python3
"""Capture selected public executable evidence and verify its published digests."""
import base64
import concurrent.futures
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REV = '412c0f10e12755a47f79ec3f90e08ef5d2ecaa47'
ROOT = 'repos/kebag-logic/milan-fpga/contents/review-evidence/677-r1/'
FILES = ('author/evidence.json', 'author/nvm-campaign.json',
         'author/logs/coverage-check.log', 'author/logs/erased-end-asan.log',
         'author/logs/ctrl.log', 'author/logs/nvm-controls.log')
out = Path(sys.argv[1])
manifest = json.loads((out / 'evidence-manifest.json').read_text())
expected = {item['file']: item['published_sha256'] for item in manifest}
(out / 'public-evidence').mkdir(exist_ok=True)


def fetch(name):
    obj = json.loads(subprocess.check_output(['gh', 'api', ROOT + name + '?ref=' + REV]))
    data = base64.b64decode(obj['content'])
    digest = hashlib.sha256(data).hexdigest()
    assert digest == expected[name], name
    destination = out / 'public-evidence' / Path(name).name
    destination.write_bytes(data)
    return f'PASS {name}: {len(data)} bytes sha256={digest}'


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(fetch, FILES):
        print(result)
