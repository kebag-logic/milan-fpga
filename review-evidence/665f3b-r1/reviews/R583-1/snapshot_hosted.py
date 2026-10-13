#!/usr/bin/env python3
"""Read exact-head hosted checks and the PR's public finding census."""
import concurrent.futures
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
p=Path(sys.argv[1]).resolve()
prefix='repos/kebag-logic/milan-fpga/'
head='db29bdd07529fbc697b7956827092f64b1241714'
urls={
 'checks':prefix+f'commits/{head}/check-runs?per_page=100',
 'runs':prefix+f'actions/runs?head_sha={head}&per_page=100',
 'comments':prefix+'issues/736/comments?per_page=100',
 'reviews':prefix+'pulls/736/reviews?per_page=100',
 'inline':prefix+'pulls/736/comments?per_page=100',
}
def api(item):
    name,url=item
    return name,json.loads(subprocess.check_output(['gh','api',url]))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    data=dict(pool.map(api,urls.items()))
summary={'observed_at':datetime.now(timezone.utc).isoformat(),'head':head,
 'checks':[{k:c.get(k) for k in ['name','head_sha','status','conclusion','started_at','completed_at','details_url']}
           for c in data['checks']['check_runs']],
 'runs':[{k:r.get(k) for k in ['id','name','head_sha','status','conclusion','html_url','run_attempt']}
         for r in data['runs']['workflow_runs']]}
assert all(c['head_sha']==head for c in summary['checks'])
assert all(r['head_sha']==head for r in summary['runs'])
(p/'hosted-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
jobs=[]
for run in summary['runs']:
    raw=json.loads(subprocess.check_output(['gh','api',prefix+f"actions/runs/{run['id']}/jobs?per_page=100"]))
    for job in raw['jobs']:
        jobs.append({k:job.get(k) for k in ['id','run_id','head_sha','name','status','conclusion','started_at','completed_at','html_url','steps']})
(p/'hosted-jobs.json').write_text(json.dumps(jobs,indent=2)+'\n')
history={'observed_at':summary['observed_at'],'comments':[
 {'id':c['id'],'url':c['html_url'],'header':c['body'].splitlines()[0] if c['body'] else ''} for c in data['comments']],
 'submitted_reviews':len(data['reviews']),'inline_comments':len(data['inline'])}
(p/'review-history.json').write_text(json.dumps(history,indent=2)+'\n')
print(json.dumps(history,indent=2))
for c in summary['checks']:
    print(c['name'],c['status'],c['conclusion'])
