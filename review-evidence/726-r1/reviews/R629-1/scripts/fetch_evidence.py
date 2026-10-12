#!/usr/bin/env python3
"""Download only the designated public evidence subtree; verify Git blob identities."""
import concurrent.futures, hashlib, json, subprocess, sys, urllib.request
from pathlib import Path
p=Path(sys.argv[1]);dest=p/"scratch/public-evidence";dest.mkdir(exist_ok=True)
entries=json.loads((p/"receipts/public-evidence-tree.json").read_text())
def get(e):
    if e["type"]!="blob": return
    url="https://raw.githubusercontent.com/kebag-logic/milan-fpga/885f0527d9960b7594c6acc19ce4eb01230a5b53/"+e["path"]
    data=urllib.request.urlopen(url).read()
    assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==e["sha"]
    path=dest/Path(e["path"]).relative_to("review-evidence/726-r1");path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(get,entries))
print("Public evidence blobs downloaded and verified:",sum(e["type"]=="blob" for e in entries))
