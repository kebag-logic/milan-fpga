#!/usr/bin/env python3
"""Read exact-head check status and job steps; no workflow execution or writes."""
import concurrent.futures
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
packet=Path(sys.argv[1]).resolve()
head='c7d0ad63510cf1aaee41ef440675d110ad2730d7'
def api(endpoint):
    return json.loads(subprocess.check_output(['gh','api','repos/kebag-logic/milan-fpga/'+endpoint]))
checks=api('commits/'+head+'/check-runs?per_page=100')
assert len(checks['check_runs'])==checks['total_count']
def one(c):
    assert c['head_sha']==head
    row={k:c[k] for k in ('id','name','head_sha','status','conclusion','started_at','completed_at','details_url')}
    if '/job/' in c['details_url']:
        job=api('actions/jobs/'+c['details_url'].rsplit('/',1)[1])
        row['steps']=[{k:s[k] for k in ('name','status','conclusion','number','started_at','completed_at')}
                      for s in job['steps']]
    return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows=list(pool.map(one,checks['check_runs']))
pr=api('pulls/715')
assert pr['head']['sha']==head
out={'snapshot_utc':datetime.now(timezone.utc).isoformat(),'head':head,'draft':pr['draft'],
     'checks':rows,'formal_reviews':len(api('pulls/715/reviews')),
     'inline_comments':len(api('pulls/715/comments'))}
(packet/'receipts/hosted-snapshot.json').write_text(json.dumps(out,indent=2)+'\n')
for r in rows:
    print(r['name'],r['status'],r['conclusion'])
print('Snapshot',out['snapshot_utc'])
