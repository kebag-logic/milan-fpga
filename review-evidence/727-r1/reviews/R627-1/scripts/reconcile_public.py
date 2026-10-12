#!/usr/bin/env python3
"""Read public dispositions only after the independent verdict/ledger exists."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('packet', type=Path)
a = p.parse_args()
packet = a.packet.resolve()
report = (packet / 'REPORT.md').read_bytes()
assert report.startswith(b'[R627] POSITIVE - exact head ') or report.startswith(b'[R627] NEGATIVE - exact head ')
assert b'Covering round' in report and b'| Conformance |' in report
out = packet / 'receipts'
start = {'observed_at': datetime.now(timezone.utc).isoformat(),
         'independent_report_sha256_before_reconciliation': hashlib.sha256(report).hexdigest()}
(out / 'reconciliation-start.json').write_text(json.dumps(start, indent=2) + '\n')
head = 'a57d384dc697249c2a69f80079b676875d4f7560'
requests = [
    ('final-issue-comments', 'issues/727/comments?per_page=100'),
    ('final-pr-comments', 'issues/728/comments?per_page=100'),
    ('final-pr-reviews', 'pulls/728/reviews?per_page=100'),
    ('final-pr-inline', 'pulls/728/comments?per_page=100'),
    ('final-head-runs', f'actions/runs?head_sha={head}&per_page=100'),
    ('final-head-checks', f'commits/{head}/check-runs?per_page=100'),
]
def get(task):
    name, path = task
    r = subprocess.run(['gh', 'api', 'repos/kebag-logic/milan-fpga/' + path],
                       capture_output=True, text=True, timeout=60)
    (out / (name + '.json')).write_text(r.stdout)
    (out / (name + '.rc')).write_text(str(r.returncode) + '\n')
    assert r.returncode == 0, r.stderr
    return name, json.loads(r.stdout)
with ThreadPoolExecutor(max_workers=6) as pool:
    results = dict(pool.map(get, requests))
for name in ('final-issue-comments', 'final-pr-comments', 'final-pr-reviews', 'final-pr-inline'):
    data = results[name]
    print(name, len(data))
    for item in data:
        print(item['html_url'], item.get('body', '').splitlines()[:1])
        if item.get('body', '').startswith('[R'):
            print(item['body'])
print('RUNS')
for run in results['final-head-runs']['workflow_runs']:
    print(run['id'], run['name'], run['head_sha'], run['status'], run['conclusion'])
print('CHECKS')
for check in results['final-head-checks']['check_runs']:
    print(check['name'], check['status'], check['conclusion'])
