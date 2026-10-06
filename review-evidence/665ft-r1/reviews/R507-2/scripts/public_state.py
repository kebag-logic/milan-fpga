#!/usr/bin/env python3
"""Read-only public evidence snapshot; review bodies are deliberately excluded."""
import concurrent.futures
import datetime
import json
from pathlib import Path
import subprocess
import sys

packet=Path(sys.argv[1]).resolve()
repo='repos/kebag-logic/milan-fpga'
sha='e7e0c10f4d4e9f3180b5650507a83aa300c5d4d7'
def api(path):
    return json.loads(subprocess.check_output(['gh','api',f'{repo}/{path}']))
runs=api(f'actions/runs?head_sha={sha}&per_page=100')['workflow_runs']
def read_run(r):
    jobs=api(f'actions/runs/{r["id"]}/jobs?per_page=100')['jobs']
    return dict(id=r['id'],name=r['name'],head_sha=r['head_sha'],url=r['html_url'],status=r['status'],
                conclusion=r['conclusion'],jobs=[{k:j[k] for k in ('id','name','status','conclusion','steps')} for j in jobs])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records=list(pool.map(read_run,runs))
result={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':sha,'runs':records}
(packet/'receipts/hosted-snapshot.json').write_text(json.dumps(result,indent=2)+'\n')
for r in records:
    print(r['id'],r['name'],r['status'],r['conclusion'])
    for j in r['jobs']:
        print(' ',j['name'],j['status'],j['conclusion'])
for n in [665,675]:
    comments=api(f'issues/{n}/comments?per_page=100')
    selected=[{k:c[k] for k in ('id','html_url','created_at','body')} for c in comments
              if c['body'].startswith('[A10]') and c['id']>6013755036]
    (packet/f'scratch/manager-updates-{n}.json').write_text(json.dumps(selected,indent=2)+'\n')
    for c in selected:
        print('MANAGER',n,c['id'],c['body'])
