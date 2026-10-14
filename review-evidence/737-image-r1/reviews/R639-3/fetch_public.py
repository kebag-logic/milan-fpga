#!/usr/bin/env python3
"""Fetch only selected public execution artifacts and verify Git blob identities."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request

packet=Path(__file__).resolve().parent
revision='d7f2e7f19fb1fbe66d81635ae09eb30c61aee89e'
tree_path=packet/'scratch/public-tree.json'
tree_path.parent.mkdir(parents=True,exist_ok=True)
if not tree_path.exists():
    with urllib.request.urlopen(f'https://api.github.com/repos/kebag-logic/milan-fpga/git/trees/{revision}?recursive=1',timeout=60) as stream:
        tree_path.write_bytes(stream.read())
tree=json.loads(tree_path.read_text())
assert not tree.get('truncated')
prefix='review-evidence/737-image-r1/author-r3/'
selected=[]
for item in tree['tree']:
    path=item['path']; name=Path(path).name
    if item['type']!='blob' or not path.startswith(prefix): continue
    if name.startswith(('round3-', 'builder-')) and name.endswith(('.json','.log','.py')):
        selected.append(item)
def fetch(item):
    url=f'https://raw.githubusercontent.com/kebag-logic/milan-fpga/{revision}/{item["path"]}'
    with urllib.request.urlopen(url, timeout=60) as stream: data=stream.read()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert actual==item['sha'],item['path']
    target=packet/'scratch/public'/Path(item['path']).name
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    return {'url':url,'blob':actual,'sha256':hashlib.sha256(data).hexdigest(),'size':len(data)}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    receipts=list(pool.map(fetch, selected))
(packet/'public-fetch.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(f'Authenticated {len(receipts)} public execution artifacts; no prose handoff or review report fetched.')
