#!/usr/bin/env python3
"""Snapshot executed, pending and skipped hosted contexts without accepting them."""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

out = Path(sys.argv[1]).resolve()/'receipts'
repo = 'Mister-M-alt/protocol-processor-control-plane-avb-milan'
head = '66d1b501f4879402fe76485095aef7c6e07c32af'
observations = []
for run_id in [37969844803,37969840642]:
    run = json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/actions/runs/{run_id}']))
    jobs = json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/actions/runs/{run_id}/jobs?per_page=100']))
    assert run['head_sha'] == head
    rows = []
    for j in jobs['jobs']:
        row = {k:j[k] for k in ['id','name','status','conclusion','html_url','started_at','completed_at','steps']}
        rows.append(row)
        if j['name']=='docs-gates' and j['conclusion']=='success':
            data = subprocess.check_output(['gh','api','--allow-escape-sequences',f'repos/{repo}/actions/jobs/{j["id"]}/logs'])
            (out/f'hosted-docs-{run_id}.log').write_bytes(data)
    observations.append({'run_id':run_id,'event':run['event'],'head_sha':run['head_sha'],
        'status':run['status'],'conclusion':run['conclusion'],'html_url':run['html_url'],'jobs':rows})
result = {'observed_utc':datetime.now(timezone.utc).isoformat(),'runs':observations}
(out/'hosted-observation.json').write_text(json.dumps(result,indent=2)+'\n')
log = (out/'hosted-docs-37969844803.log').read_text()
match = re.search(r'git log -1 --format=%H\n[^\n]*? ([0-9a-f]{40})\n',log)
assert match
sha = match.group(1)
commit = json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/git/commits/{sha}']))
checkout = {'commit':sha,'tree':commit['tree']['sha'],
    'parents':[x['sha'] for x in commit['parents']],
    'matches_review_tree':commit['tree']['sha']=='36e735c0d54ceb20f2ca09f4ed07069e575a9717'}
(out/'hosted-pr-checkout.json').write_text(json.dumps(checkout,indent=2)+'\n')
checks = subprocess.run(['gh','pr','checks','171','--repo',repo],capture_output=True,text=True)
(out/'hosted-checks.txt').write_text(checks.stdout+checks.stderr)
(out/'hosted-checks.rc').write_text(str(checks.returncode)+'\n')
for r in observations:
    print(r['run_id'],r['event'],[(j['name'],j['status'],j['conclusion']) for j in r['jobs']])
print('observed_utc',result['observed_utc'])
