#!/usr/bin/env python3
"""Read only exact-head hosted jobs, distinguishing skipped steps."""
import argparse, datetime, json, subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
repo='kebag-logic/milan-fpga';head='614b4aa5f408d75673b546ce6efb6ef126437be2'
def api(path):return json.loads(subprocess.check_output(['gh','api','repos/'+repo+'/'+path]))
pr=api('pulls/699');assert pr['head']['sha']==head
r=subprocess.run(['gh','pr','checks','699','--repo',repo,'--json','name,state,bucket,workflow,link'],capture_output=True,text=True)
assert r.returncode in (0,8)
out={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':head,'pr_base':pr['base']['sha'],'live_dev':api('git/ref/heads/dev')['object']['sha'],'checks_command_rc':r.returncode,'checks':json.loads(r.stdout),'runs':[]}
for run in api('actions/runs?head_sha='+head+'&per_page=100')['workflow_runs']:
 assert run['head_sha']==head
 item={k:run[k] for k in ('id','name','event','head_sha','status','conclusion','html_url')}
 item['jobs']=[]
 for j in api('actions/runs/'+str(run['id'])+'/jobs?per_page=100')['jobs']:
  item['jobs'].append({k:j.get(k) for k in ('id','name','status','conclusion','html_url','head_sha','started_at','completed_at','steps')})
 out['runs'].append(item)
a.output.write_text(json.dumps(out,indent=2)+'\n')
for c in out['checks']:print(c['workflow'],c['name'],c['state'])
