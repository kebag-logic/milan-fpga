#!/usr/bin/env python3
"""Download only the public author evidence archive, never reviewer reports."""
import concurrent.futures, hashlib, json, pathlib, subprocess, sys, urllib.request
p=pathlib.Path(sys.argv[1]).resolve(); commit='c4a23f5a47804a521c54ada84a175b3c11df86d5'
t=json.loads(subprocess.check_output(['gh','api',f'repos/kebag-logic/milan-fpga/git/trees/{commit}?recursive=1']))
root='review-evidence/pp163-r1/author-r3/'
files=[x for x in t['tree'] if x['type']=='blob' and x['path'].startswith(root)]
def get(x):
    url=f'https://raw.githubusercontent.com/kebag-logic/milan-fpga/{commit}/{x["path"]}'
    data=urllib.request.urlopen(url).read()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['sha']
    out=p/'receipts/public-author-r3'/x['path'][len(root):];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
    return {'path':x['path'],'blob':x['sha'],'sha256':hashlib.sha256(data).hexdigest(),'url':url}
with concurrent.futures.ThreadPoolExecutor(8) as pool: records=list(pool.map(get,files))
(p/'receipts/public-downloads.json').write_text(json.dumps(records,indent=2)+'\n')
print('Verified public blobs:',len(records))
