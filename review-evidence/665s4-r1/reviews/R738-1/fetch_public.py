#!/usr/bin/env python3
"""Read immutable public evidence into scratch and verify its published hashes.

Requires an authenticated read-only GitHub CLI session if the repository is private.
This script makes GET requests only.
"""
import hashlib
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
root = packet / 'scratch/public'
commit = '970c3e41d037c8e0ce58af7241a05078218c28ac'
for row in json.loads((packet / 'public-inputs.json').read_text()):
    dest = root / row['file']
    if not dest.exists():
        endpoint = ('repos/kebag-logic/milan-fpga/contents/review-evidence/665s4-r1/'
                    + row['file'] + '?ref=' + commit)
        data = subprocess.check_output(['gh', 'api', '-H', 'Accept: application/vnd.github.raw+json', endpoint])
        assert hashlib.sha256(data).hexdigest() == row['published_sha256'], row['file']
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    assert hashlib.sha256(dest.read_bytes()).hexdigest() == row['published_sha256'], row['file']
    print('PASS', row['file'], row['published_sha256'])
