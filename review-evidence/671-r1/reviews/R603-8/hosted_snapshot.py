#!/usr/bin/env python3
"""Read exact-head check runs and their job steps; never wait for acceptance."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

out = Path(__file__).resolve().parent
head = 'd5cd863561ba1ee7bc6342fb1b00f57dd786bd97'
repo = 'repos/kebag-logic/milan-fpga/'
def api(path):
    return json.loads(subprocess.check_output(['gh','api',repo+path]))
checks=api('commits/'+head+'/check-runs?per_page=100')
assert checks['total_count'] <= 100
for c in checks['check_runs']:
    assert c['head_sha']==head
def job(c):
    url=c.get('details_url','')
    if '/job/' in url:
        return api('actions/jobs/'+url.rsplit('/',1)[1])
    return None
with ThreadPoolExecutor(max_workers=6) as pool:
    jobs=list(pool.map(job, checks['check_runs']))
snapshot=dict(observed_utc=datetime.now(timezone.utc).isoformat(),head=head,
              check_runs=checks,jobs=[j for j in jobs if j])
(out/'hosted-snapshot.json').write_text(json.dumps(snapshot,indent=2)+'\n')
lines=[snapshot['observed_utc']+' exact head '+head]
for c in checks['check_runs']:
    lines.append(f"{c['name']}: {c['status']} / {c['conclusion'] or 'pending'}: {c['details_url']}")
(out/'hosted-snapshot.log').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
