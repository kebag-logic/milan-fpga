#!/usr/bin/env python3
"""Refetch the selected immutable evidence, checking each published Git blob."""
import base64
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
entries = json.loads((packet / 'download-list.json').read_text())
def one(row):
    result = json.loads(subprocess.check_output(['gh', 'api', 'repos/kebag-logic/milan-fpga/git/blobs/' + row['sha']]))
    data = base64.b64decode(result['content'])
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['sha']
    out = packet / 'evidence' / row['relative']
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    list(pool.map(one, entries))
print(f'{len(entries)} immutable evidence files fetched and matched to pinned Git blobs.')
