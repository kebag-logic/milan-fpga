#!/usr/bin/env python3
"""Retrieve selected immutable public receipts and verify Git blob identities."""
import concurrent.futures, hashlib, json, pathlib, urllib.request
p=pathlib.Path(__file__).resolve().parent
commit='fca476ecbc2bc8ecf032500c08d6401dd0a01d1a'
prefix='review-evidence/pp192-r1/'
url='https://raw.githubusercontent.com/kebag-logic/milan-fpga/'+commit+'/'
tree=json.loads(urllib.request.urlopen('https://api.github.com/repos/kebag-logic/milan-fpga/git/trees/'+commit+'?recursive=1').read())['tree']
def select(q):
    if q in ['author/receipts/INDEX.md','author/parent-adoption-milan_dp-gsi-g9.patch']: return True
    if q.startswith('author/receipts/head/gates/'): return q.endswith(('.rc','HEAD.txt','run_suites.log','make_check.log'))
    if q.startswith('author/receipts/head/campaigns/') and q.count('/')==4: return q.endswith(('.rc','.log','.txt'))
    if q.startswith('author/receipts/head/campaigns/out/gsi/'): return q.endswith(('results.json','-run.log'))
    if any(q.startswith('author/receipts/'+part+'/') for part in ['parent-head','parent-head-adopt','parent-base']):
        return q.endswith(('.rc','submodule-HEAD.txt','parent-HEAD.txt','parent-log.txt','g15_milan_dp.log.excerpt.txt','gitlink.txt'))
    if q.startswith('author/receipts/head-42c6a5e/') and (q.endswith('HEAD-notify.txt') or q.endswith('notify.log') or q.endswith('notify.rc')): return True
    return False
def get(x):
    q=x['path']; data=urllib.request.urlopen(url+q).read()
    digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert digest==x['sha'],q
    target=p/'public'/q[len(prefix):]; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(data)
    return {'path':str(target.relative_to(p)),'url':url+q,'git_blob':digest,'sha256':hashlib.sha256(data).hexdigest()}
xs=[x for x in tree if x['type']=='blob' and x['path'].startswith(prefix) and select(x['path'][len(prefix):])]
with concurrent.futures.ThreadPoolExecutor(8) as pool: results=list(pool.map(get,xs))
(p/'public-receipts.json').write_text(json.dumps(results,indent=2)+'\n')
print('Verified',len(results),'public receipts')
