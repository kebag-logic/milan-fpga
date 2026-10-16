#!/usr/bin/env python3
"""Fetch only the public receipts listed in this packet; verify publication hashes and Git blob IDs.
Run: python3 fetch_receipts.py PACKET
Requires authenticated read access through gh when the repository requires it.
"""
import concurrent.futures,hashlib,json,subprocess,sys
from pathlib import Path
packet=Path(sys.argv[1]).resolve()
manifest=json.loads((packet/'evidence-verification.json').read_text())
def fetch(row):
    url='repos/kebag-logic/milan-fpga/contents/review-evidence/737-image-r1/'+row['file']+'?ref='+manifest['commit']
    data=subprocess.check_output(['gh','api','-H','Accept: application/vnd.github.raw+json',url])
    assert hashlib.sha256(data).hexdigest()==row['published_sha256'],row['file']
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob'],row['file']
    path=packet/'evidence'/row['file'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    return row['file']
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    files=list(pool.map(fetch,manifest['files']))
print('Verified',len(files),'published receipts at',manifest['commit'])
