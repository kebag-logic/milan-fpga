#!/usr/bin/env python3
"""Read the assigned public evidence; never fetch other review packets."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys

REF = '672394110780ae01de682b7ca8360d50dcdca633'
PREFIX = 'repos/kebag-logic/milan-fpga/'
def api(path, raw=False):
    args = ['gh', 'api', PREFIX + path]
    if raw:
        args += ['-H', 'Accept: application/vnd.github.raw+json']
    return subprocess.check_output(args)

dest = Path(sys.argv[1])
dest.mkdir(parents=True, exist_ok=True)
manifest = json.loads(api('contents/review-evidence/654-r1/MANIFEST.json?ref=' + REF, True))
def fetch(row):
    name = row['file']
    data = api('contents/review-evidence/654-r1/' + name + '?ref=' + REF, True)
    actual = hashlib.sha256(data).hexdigest()
    assert actual == row['published_sha256'], name
    path = dest / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {'file': name, 'sha256': actual, 'bytes': len(data)}
with ThreadPoolExecutor(max_workers=6) as pool:
    rows = list(pool.map(fetch, manifest))
print(json.dumps({'public_ref': REF, 'verified': rows}, indent=2))
