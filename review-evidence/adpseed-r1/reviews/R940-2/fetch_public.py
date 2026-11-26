#!/usr/bin/env python3
"""Fetch only pinned public evidence. Usage: fetch_public.py PACKET."""
import base64
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys

packet=Path(sys.argv[1]).resolve()
def api(path):
    return json.loads(subprocess.check_output(['gh','api',path]))
def file(ref,path):
    data=api(f'repos/kebag-logic/milan-fpga/contents/{path}?ref={ref}')
    return base64.b64decode(data['content'])
for round_,ref in [('r1','6682d3c02e80ae7d850b2bc6a169daf6c77f0e6e'),('r2','d33da1eae7d07dffb35d18317dcbdaef8dcd4fe9')]:
    root='review-evidence/adpseed-'+round_
    dest=packet/'scratch'/root
    dest.mkdir(parents=True,exist_ok=True)
    manifest=file(ref,root+'/MANIFEST.json')
    (dest/'MANIFEST.json').write_bytes(manifest)
    def fetch(row):
        relative=Path(row['file'])
        assert not relative.is_absolute() and '..' not in relative.parts
        target=dest/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(file(ref,root+'/'+row['file']))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(fetch,json.loads(manifest)))
    verification=api(f'repos/kebag-logic/milan-fpga/commits/{ref}')['commit']['verification']
    out=packet/'receipts'
    out.mkdir(exist_ok=True)
    (out/(round_+'-verification.json')).write_text(json.dumps(dict(commit=ref,verification=verification),indent=2)+'\n')
print('Pinned public evidence downloaded; no reviewer reports fetched.')
