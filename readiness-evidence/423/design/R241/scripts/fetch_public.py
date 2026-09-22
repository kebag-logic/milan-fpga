import subprocess,json,pathlib,re,hashlib,base64
ROOT=pathlib.Path(__file__).resolve().parents[1]
PUB=ROOT/'public'
def api(endpoint):
 p=subprocess.run(['rtk','proxy','gh','api',endpoint],capture_output=True,text=True)
 with (ROOT/'logs/public-fetch.log').open('a') as f: f.write(f"GET {endpoint} exit={p.returncode}\n{p.stderr}")
 p.check_returncode(); return json.loads(p.stdout)
def save(name,data): (PUB/name).write_text(json.dumps(data,indent=2)+'\n')
def pages(endpoint):
 result=[]
 for page in range(1,100):
  data=api(f'{endpoint}?per_page=100&page={page}'); result.extend(data)
  if len(data)<100: return result
 raise RuntimeError('pagination limit')
repo='repos/kebag-logic/milan-fpga'
issue=api(repo+'/issues/423');save('issue423.json',issue)
comments=pages(repo+'/issues/423/comments')
allowed=[];excluded=[]
for c in comments:
 if c['id']>5776564663 and (re.search(r'\[R242(?:[-\] ])',c['body']) or ('R242' in c['body'] and re.search(r'report|verdict|DESIGN READY|NEEDS DECISION',c['body'],re.I))):
  excluded.append({k:c[k] for k in ('id','html_url','created_at')})
 else: allowed.append(c)
save('issue423-comments-filtered.json',allowed);save('excluded-comments-metadata.json',excluded)
print('ISSUE',issue['title'],'\n',issue['body'])
for c in allowed: print('\nCOMMENT',c['id'],c['created_at'],'\n',c['body'])
print('Excluded comment metadata:',excluded)
donor='repos/Mister-M-alt/FPGA-gPTP'
for name,endpoint in [('pr62',donor+'/pulls/62'),('pr62-commits',donor+'/pulls/62/commits'),('pr62-comments',donor+'/issues/62/comments'),('pr62-reviews',donor+'/pulls/62/reviews'),('pr62-review-comments',donor+'/pulls/62/comments')]:
 data=api(endpoint) if name=='pr62' else pages(endpoint);save(name+'.json',data)
 print(name,json.dumps(data if name!='pr62' else {k:data[k] for k in ('title','body','merge_commit_sha','merged_at','base','head')}))
sha='6181e900cd9f7ae618e1603e2ea867a5bb4d41a6'
tree=api(repo+'/git/trees/'+sha+'?recursive=1');save('prior-tree.json',tree)
assert not tree.get('truncated')
blobs=[e for e in tree['tree'] if e['path'].startswith('readiness-evidence/423/') and e['type']=='blob']
for e in blobs:
 obj=api(repo+'/git/blobs/'+e['sha']);raw=base64.b64decode(obj['content']);assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==e['sha']
 dest=PUB/e['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
 print('VERIFIED PUBLIC BLOB',e['path'],e['sha'],len(raw))
save('prior-blobs.json',blobs)
