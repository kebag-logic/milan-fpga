#!/usr/bin/env python3
"""Read public authorities, author receipts, and exact-head hosted metadata."""
import base64
import concurrent.futures
import hashlib
import json
import subprocess
from pathlib import Path

PACKET = Path(__file__).resolve().parent
EVIDENCE = '3e8c823acbb589151b5ccfd53f1399a89f4fa6ae'
HEAD = '49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c'

def api(endpoint):
    return json.loads(subprocess.check_output(['gh','api',endpoint], text=True))

def main():
    dst = PACKET/'public'
    dst.mkdir(exist_ok=True)
    root = f'repos/kebag-logic/milan-fpga/contents/review-evidence/g35-r1/'
    manifest = api(root+'MANIFEST.json?ref='+EVIDENCE)
    rows = json.loads(base64.b64decode(manifest['content']))
    lookup = {r['file']:r for r in rows}
    paths = ['author/evidence/equiv/summary.txt']
    prefix = 'author-r2/evidence/r2/'
    paths += [prefix+'gates-head/'+s for s in ['identity.txt','rc.txt','tb.log','docs.log','contract.log','lint.log']]
    paths += [prefix+'parent/'+side+'/'+s for side in ['base','head'] for s in [
        'identity.txt','pin.txt','rc.txt','flat.stat.txt','rom_bundle_digest.txt','rom_sha256.txt','top-KL_gptp_shadow.result']]
    paths += [prefix+'parent/module-compare-r1head-r2head.txt',prefix+'mutation/stale-mutant-named.txt',prefix+'mutation/planted-named.txt']
    def get(path):
        d=api(root+path+'?ref='+EVIDENCE)
        raw=base64.b64decode(d['content'])
        digest=hashlib.sha256(raw).hexdigest()
        assert digest == lookup[path]['published_sha256'], path
        f=dst/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
        return {'path':path,'published_sha256':digest,'url':'https://github.com/kebag-logic/milan-fpga/blob/'+EVIDENCE+'/review-evidence/g35-r1/'+path}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        got=list(pool.map(get,paths))
    (dst/'download-index.json').write_text(json.dumps(got,indent=2)+'\n')
    for endpoint,name in [
        (f'repos/Mister-M-alt/FPGA-gPTP/actions/runs?head_sha={HEAD}&per_page=100','hosted-runs'),
        (f'repos/Mister-M-alt/FPGA-gPTP/commits/{HEAD}/check-runs?per_page=100','check-runs'),
        (f'repos/Mister-M-alt/FPGA-gPTP/commits/{HEAD}/status','commit-status'),
    ]:
        data=api(endpoint)
        # Keep public technical metadata; no account/avatar fields.
        items=data.get('workflow_runs',data.get('check_runs',data.get('statuses',[])))
        keep=[{k:v for k,v in x.items() if k in ['id','name','status','conclusion','head_sha','head_branch','event','html_url','details_url','created_at','updated_at','started_at','completed_at','run_attempt','path','context','state','target_url','description']} for x in items]
        out={'head':HEAD,'total_count':data.get('total_count',len(items)),'state':data.get('state'),'items':keep}
        (dst/(name+'.json')).write_text(json.dumps(out,indent=2)+'\n')
        print(name,json.dumps(out))
    parent=api('repos/kebag-logic/milan-fpga/git/trees/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5?recursive=1')
    assert not parent['truncated']
    links=[{k:x[k] for k in ['path','mode','sha']} for x in parent['tree'] if x['mode']=='160000']
    (dst/'parent-gitlinks.json').write_text(json.dumps(links,indent=2)+'\n')
    print('parent gitlinks',json.dumps(links))
    print('Fetched and verified',len(got),'author receipt hashes; no review reports fetched')

if __name__=='__main__':
    main()
