#!/usr/bin/env python3
"""Read published workflow receipts; make no remote changes."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import zipfile
packet=Path(sys.argv[1]).resolve()
out=packet/'receipts/hosted';out.mkdir(parents=True,exist_ok=True)
scratch=packet/'scratch/hosted';scratch.mkdir(parents=True,exist_ok=True)
base='repos/kebag-logic/tsn-c-stack'
def api(path):return subprocess.check_output(['gh','api',base+path])
summary=[]
for run_id in (37889963458,37889967433):
    run=json.loads(api('/actions/runs/'+str(run_id)))
    assert run['head_sha']=='ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3'
    jobs=json.loads(api('/actions/runs/'+str(run_id)+'/jobs'))['jobs']
    item={k:run[k] for k in ('id','event','head_sha','status','conclusion','html_url')}
    item['jobs']=[{**{k:j[k] for k in ('id','name','head_sha','status','conclusion','html_url')},'steps':j['steps']} for j in jobs]
    artifacts=json.loads(api('/actions/runs/'+str(run_id)+'/artifacts'))['artifacts']
    item['artifacts']=[]
    for artifact in artifacts:
        data=api('/actions/artifacts/'+str(artifact['id'])+'/zip')
        (scratch/(str(artifact['id'])+'.zip')).write_bytes(data)
        row={'id':artifact['id'],'name':artifact['name'],'zip_sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for name in z.namelist():
                if name.endswith('gates.json'):
                    gates=json.loads(z.read(name))
                    row['gates']=gates
                    assert len(gates)==20 and all(x['rc']==0 for x in gates)
                elif name.endswith('mutations/results.json'):
                    plants=json.loads(z.read(name))
                    row['plants']=[{'name':m['name'],'status':m['status']} for m in plants]
                    assert len(plants)==311 and all(m['status']=='CAUGHT' for m in plants)
                elif name.endswith('results.json'):
                    rv=json.loads(z.read(name))
                    row['rv32']=rv
                    assert len(rv)==2 and all(m['rc']==0 and m['unresolved_final']==[] for m in rv)
                elif name.endswith(('.rc','coverage.log','gcc-test.log','clang-sanitizers-test.log')):
                    target=out/(str(run_id)+'-'+Path(name).name)
                    text=z.read(name).decode()
                    text=text.replace('<home-path>/work/tsn-c-stack/tsn-c-stack','<REPO>')
                    target.write_text(text)
        item['artifacts'].append(row)
    assert {j['name'] for j in jobs}=={'quality','bare-metal'}
    assert all(j['conclusion']=='success' for j in jobs)
    summary.append(item)
    print(run_id,run['event'],run['conclusion'],[(x['name'],x['conclusion']) for x in jobs],flush=True)
(out/'executed-evidence.json').write_text(json.dumps(summary,indent=2)+'\n')
