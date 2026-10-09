#!/usr/bin/env python3
"""Fetch selected public executable receipts without reading review reports."""
import base64,concurrent.futures,hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]);tree=json.loads(subprocess.check_output(["gh","api","repos/kebag-logic/milan-fpga/git/trees/42e3d07b26bca054e18ec8f9d8e03ba8d114b9d6?recursive=1"]));dest=root/"receipts/public";dest.mkdir(parents=True,exist_ok=True)
selected=[]
for f in tree["tree"]:
 s=f["path"]
 if f['type']!='blob':continue
 if '/reviews/R474-5/receipts/' in s and ('trace-table-probe-inputs/' in s or 'shard0-suite-windows.txt' in s or ('/runs/T' in s and s.endswith(('.cmd','.time','.rc')))):
  selected.append(f)
 if '/author-r2f/resource-receipts/' in s and s.endswith(('check-route-1x1.log','resolved-measurement-inputs.json')):selected.append(f)
def fetch(f):
 data=json.loads(subprocess.check_output(['gh','api','repos/kebag-logic/milan-fpga/git/blobs/'+f['sha']]))
 raw=base64.b64decode(data['content']);out=dest/f['path'].split('/645-r1/')[1];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
 return dict(path=str(out.relative_to(root)),public_path=f['path'],blob=f['sha'],sha256=hashlib.sha256(raw).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(fetch,selected))
(root/'receipts/public-provenance.json').write_text(json.dumps(dict(tree=tree['sha'],files=results),indent=2)+'\n')
print('Downloaded',len(results),'public receipts')
