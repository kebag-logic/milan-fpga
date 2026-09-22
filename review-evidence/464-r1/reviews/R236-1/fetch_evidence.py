import json,subprocess,hashlib,base64,concurrent.futures
from pathlib import Path
out=Path(__file__).parent
items=json.loads((out/'evidence-tree.json').read_text())
# Public factual receipts only. No reviewer packet or private author material.
selected=[t for t in items if t['type']=='blob' and ('/candidate1/' in t['path'] or '/author/' in t['path'] or t['path'].endswith('/MANIFEST.json') or t['path'].endswith('/native-superseded.json'))]
def get(t):
 p=out/'public'/t['path'];p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():
  raw=subprocess.check_output(['rtk','proxy','gh','api','repos/kebag-logic/milan-fpga/git/blobs/'+t['sha']])
  data=base64.b64decode(json.loads(raw)['content']);p.write_bytes(data)
 data=p.read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==t['sha']
 return {'path':t['path'],'git_blob':t['sha'],'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: result=list(pool.map(get,selected))
(out/'public-download-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print('Downloaded and git-blob verified',len(result),'public evidence files')
