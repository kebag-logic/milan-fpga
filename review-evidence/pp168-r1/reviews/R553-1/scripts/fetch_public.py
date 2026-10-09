#!/usr/bin/env python3
"""Fetch selected immutable public evidence and verify its published hash."""
import concurrent.futures,hashlib,json,subprocess,sys,urllib.request
from pathlib import Path
p=Path(sys.argv[1]).resolve()
m=json.loads((p/'public/author-manifest.json').read_text())
selected=[]
for x in m:
 f=x['file'];r=f.removeprefix('author/round2-recovery/')
 if f.startswith('author/round2-recovery/') and (
    ('/' not in r and (r.endswith('.json') or r.endswith('.rc') or r.endswith('.patch'))) or
    r.startswith(('comparison/','base-logs/','head-logs/')) or
    (r.startswith('area/') and r.endswith(('inputs.json','result.json','run.rc','util.rpt','util_hier.rpt'))) or
    (r.startswith(('base-campaigns/','head-campaigns/')) and r.endswith('results.json')) or
    (r.startswith(('parent-base/','parent-head/')) and r.endswith('.rc'))): selected.append(x)
def fetch(x):
 f=x['file'];target=p/'public'/f;target.parent.mkdir(parents=True,exist_ok=True)
 url='https://raw.githubusercontent.com/kebag-logic/milan-fpga/1570e00395c98ed4ea1c21e6abde28948346c82b/review-evidence/pp168-r1/'+f
 if target.exists():data=target.read_bytes()
 else:
  try:data=urllib.request.urlopen(url,timeout=60).read()
  except Exception:
   data=subprocess.check_output(['gh','api','-H','Accept: application/vnd.github.raw+json','repos/kebag-logic/milan-fpga/contents/review-evidence/pp168-r1/'+f+'?ref=1570e00395c98ed4ea1c21e6abde28948346c82b'])
 sha=hashlib.sha256(data).hexdigest()
 if sha!=x['published_sha256']:raise ValueError(f+' hash mismatch')
 target.write_bytes(data)
 return dict(file=f,sha256=sha,size=len(data),verified=True)
with concurrent.futures.ThreadPoolExecutor(4) as ex:results=list(ex.map(fetch,selected))
(p/'receipts/public-evidence-fetch.json').write_text(json.dumps(results,indent=2)+'\n')
print('Verified public evidence files:',len(results))
