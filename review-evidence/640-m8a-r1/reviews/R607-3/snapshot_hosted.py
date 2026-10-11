#!/usr/bin/env python3
"""Read exact-head workflow/job evidence without publishing any GitHub state."""
import datetime,json,pathlib,subprocess
head='ce10328c3d89d81509e47836fa4a48b22ecdbc20';p=pathlib.Path(__file__).resolve().parent
raw=json.loads(subprocess.check_output(['gh','api',f'repos/kebag-logic/milan-fpga/actions/runs?head_sha={head}&per_page=100']))
result={'observed':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':head,'runs':[]}
for run in raw['workflow_runs']:
 assert run['head_sha']==head
 jobs=json.loads(subprocess.check_output(['gh','api',f"repos/kebag-logic/milan-fpga/actions/runs/{run['id']}/jobs?per_page=100"]))['jobs']
 item={k:run[k] for k in ['id','name','head_sha','status','conclusion','html_url']};item['jobs']=[{k:j[k] for k in ['id','name','status','conclusion','html_url','steps']} for j in jobs];result['runs'].append(item)
 print(item['name'],item['status'],item['conclusion'])
 for j in jobs:print(' ',j['name'],j['status'],j['conclusion'])
(p/'hosted-snapshot.json').write_text(json.dumps(result,indent=2)+'\n')
fast=[r for r in result['runs'] if r['name']=='rtl-fast'];assert fast and fast[0]['conclusion']=='success'
assert any(j['name']=='rtl-fast' and j['conclusion']=='success' for j in fast[0]['jobs'])
print('PASS: exact-head rtl-fast workflow and aggregate job succeeded')
