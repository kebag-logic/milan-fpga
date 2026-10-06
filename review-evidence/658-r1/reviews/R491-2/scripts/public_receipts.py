#!/usr/bin/env python3
"""Read public scope, PR body, checks and selected executable evidence only."""
import base64
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

packet = Path(sys.argv[1])
out = packet / 'receipts'
def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', path]))
repo = 'repos/kebag-logic/milan-fpga/'
head = '5747a8cb99495cb0331658cdd499b9c44e3eda91'
pr = api(repo + 'pulls/670')
assert pr['head']['sha'] == head
(out / 'pr-body.md').write_text(pr['body'] + '\n')
checks = api(repo + f'commits/{head}/check-runs?per_page=100')
snapshot = {'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'head': head, 'checks': [{'name': x['name'], 'status': x['status'],
            'conclusion': x['conclusion'], 'url': x['html_url']} for x in checks['check_runs']]}
(out / 'hosted-checks.json').write_text(json.dumps(snapshot, indent=2) + '\n')
commit = 'd445cbd4d2dadfa01fbefc36bec82d9ffde5695f'
paths = ['stage2_dynmap_leg_in_sweep.txt', 'stage2_dynmap_mutants_head.txt',
         'stage2_sweep_rest_summary.txt', 'stage2_sweep_sharded_tally.txt',
         'area_reset_image_microbench.txt']
index = []
for name in paths:
    path = 'review-evidence/658-r1/author/' + name
    obj = api(repo + f'contents/{path}?ref={commit}')
    data = base64.b64decode(obj['content'])
    (packet / 'scratch' / ('public-' + name)).write_bytes(data)
    index.append({'path': path, 'git_blob': obj['sha'], 'sha256': hashlib.sha256(data).hexdigest(),
                  'url': f'https://github.com/kebag-logic/milan-fpga/blob/{commit}/{path}'})
(out / 'public-evidence-index.json').write_text(json.dumps(index, indent=2) + '\n')
print('PASS: public exact-head PR/check snapshot and five historical executable receipts fetched')
