#!/usr/bin/env python3
import pathlib,json,subprocess,concurrent.futures,hashlib,re
p=pathlib.Path(__file__).resolve().parent
rows=json.loads((p/'receipts/public-evidence-tree.json').read_text())
prefix='review-evidence/pp185-r1/author/receipts/'
chosen=[]
for x in rows:
 if x['type']!='blob' or not x['path'].startswith(prefix): continue
 rel=x['path'][len(prefix):]
 if rel in ('INDEX.md','OVER-200KB.sha256') or rel.startswith(('r1c/base/gates/','r1c/head-final/','r1c/parent-base/','r1c/parent-head/','r1c/compare/')) or (rel.startswith('r1c/head/campaigns/') and any(t in rel for t in ('notify.','aecp_dispatch.','HEAD-'))):
  chosen.append((x,rel))
def fetch(pair):
 x,rel=pair
 target=p/'scratch/public-receipts'/rel; target.parent.mkdir(parents=True,exist_ok=True)
 if not target.exists():
  b=subprocess.check_output(['gh','api','-H','Accept: application/vnd.github.raw+json','repos/kebag-logic/milan-fpga/contents/'+x['path']+'?ref=baba38e7bb95a25eb63d6c7864ea0a1ca01eb013'])
  target.write_bytes(b)
 b=target.read_bytes()
 assert len(b)==x['size'] and hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==x['sha'], rel
 return rel
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: result=list(pool.map(fetch,chosen))
index=(p/'receipts/public-INDEX.md').read_text(); directory=''; indexed={}
for line in index.splitlines():
 if line.startswith('## '): directory=line[3:].strip().rstrip('/'); directory='' if directory=='.' else directory
 m=re.match(r'\| `([^`]+)` \| (\d+) \| `([a-f0-9]{64})` \|',line)
 if m: indexed[(directory+'/' if directory else '')+m[1]]=(int(m[2]),m[3])
known={x['path'][len(prefix):] for x in rows if x['type']=='blob' and x['path'].startswith(prefix)}
missing=[(k,v[0]) for k,v in indexed.items() if k not in known]
checked=[]
for rel in result:
 if rel not in indexed: continue
 b=(p/'scratch/public-receipts'/rel).read_bytes(); size,sha=indexed[rel]
 assert len(b)==size and hashlib.sha256(b).hexdigest()==sha,rel
 checked.append(rel)
summary={'published_commit':'baba38e7bb95a25eb63d6c7864ea0a1ca01eb013','downloaded_and_git_blob_verified':len(result),'index_sha256_verified':len(checked),'indexed_missing_files':missing,'checked':checked}
(p/'receipts/evidence-integrity.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Verified',len(checked),'selected redacted receipts; indexed missing:',missing)
