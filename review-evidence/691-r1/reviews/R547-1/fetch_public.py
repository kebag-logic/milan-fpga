#!/usr/bin/env python3
"""Download only the immutable, public evidence packet used by this review."""
import base64
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess

packet=Path(__file__).resolve().parent
target=packet/'scratch/published'
target.mkdir(parents=True,exist_ok=True)
commit='8f502bd4d5a78ce590001f217ea60225643b8d17'
prefix='review-evidence/691-r1/'
def api(path):
    return json.loads(subprocess.check_output(['gh','api','repos/kebag-logic/milan-fpga/'+path]))
tree=api('git/trees/'+commit+'?recursive=1')
assert not tree.get('truncated',False)
def download(row):
    blob=api('git/blobs/'+row['sha'])
    data=base64.b64decode(blob['content'])
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['sha']
    path=target/row['path'][len(prefix):]
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data)
rows=[r for r in tree['tree'] if r['type']=='blob' and r['path'].startswith(prefix)]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    list(pool.map(download,rows))
print(f'PASS: {len(rows)} public files downloaded from {commit}; Git blob identities verified')
