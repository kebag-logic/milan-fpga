#!/usr/bin/env python3
"""Read immutable public source evidence and current exact-head check metadata.

Usage: python3 read_public_evidence.py OUTPUT_DIRECTORY
Full responses and source logs stay under scratch; receipts contain hashes,
provenance, exact selected log lines and public check metadata only.
"""
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

REPO = 'repos/kebag-logic/milan-fpga'
REF = 'e5cae5f54a7efc54eb1b22095e310bb8324ace4e'
HEAD = 'd0e29f6dda6f04f3ace1dbb395f57379e58cacaf'
ROOT = 'review-evidence/656-r1'
FILES = [
    'author/logs/head-driver.log',
    'author/logs/head-driver-milan_dp_gptp.log',
    'author/logs/c-0b074298.log',
    'author/logs/c-d676ecfd.log',
    'author/logs/ctl-dev-noA2a.log',
    'author/logs/ctl-fix-noA2a.log',
    'author/logs/trace-dev.log',
    'author/logs/gates/head-test_builder.log',
]


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', f'{REPO}/{path}']))


def content(path):
    result = api(f'contents/{ROOT}/{path}?ref={REF}')
    return base64.b64decode(result['content'])


def main():
    output = Path(sys.argv[1])
    scratch, receipts = output / 'scratch', output / 'receipts'
    scratch.mkdir(exist_ok=True, parents=True)
    receipts.mkdir(exist_ok=True, parents=True)
    manifest = {item['file']: item for item in json.loads(content('MANIFEST.json'))}

    def fetch(name):
        data = content(name)
        digest = hashlib.sha256(data).hexdigest()
        assert digest == manifest[name]['published_sha256'], name
        target = scratch / 'public-evidence' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        patterns = (r'^.*== .*checks:.*$', r'^AUDIO result .*$',
                    r'^TRACE (?:ORDER|STATE).*$', r'^ALL GATES.*$',
                    r'^PASS milan_dp_gptp.*$', r'^NOT RUN:.*$',
                    r'^\d+ GATE ARM\(S\) DID NOT RUN.*$',
                    r'^.*rc=\d+.*$', r'^.*driver rc.*$', r'^.*tally rc.*$')
        lines = [line for line in data.decode().splitlines()
                 if any(re.match(p, line) for p in patterns)
                 and not line.startswith(('+', '-'))]
        # Source logs were already public-scrubbed; refuse local path shapes.
        assert not any('/home/' in line or '/data/' in line for line in lines)
        return {'path': f'{ROOT}/{name}',
                'url': f'https://github.com/kebag-logic/milan-fpga/blob/{REF}/{ROOT}/{name}',
                'sha256': digest, 'manifest_match': True,
                'exact_selected_lines': lines}

    with ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(fetch, FILES))
    (receipts / 'public-source-evidence.json').write_text(json.dumps(records, indent=2) + '\n')
    checks = api(f'commits/{HEAD}/check-runs?per_page=100')['check_runs']
    assert all(check['head_sha'] == HEAD for check in checks)
    keys = ('id', 'name', 'head_sha', 'status', 'conclusion', 'html_url', 'started_at', 'completed_at')
    snapshot = {'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
                'checks': [{key: c[key] for key in keys} for c in checks]}
    jobs = api('actions/runs/37249252013/jobs?per_page=100')['jobs']
    assert all(job['head_sha'] == HEAD for job in jobs)
    snapshot['exhaustive_jobs'] = [
        {**{key: job[key] for key in ('id', 'name', 'head_sha', 'status', 'conclusion', 'html_url')},
         'steps': [{key: step[key] for key in ('name', 'status', 'conclusion')}
                   for step in job['steps']]}
        for job in jobs]
    (receipts / 'hosted-checks.json').write_text(json.dumps(snapshot, indent=2) + '\n')
    print('PASS: immutable public log hashes matched', len(records), 'of', len(FILES))
    for record in records:
        tallies = [x for x in record['exact_selected_lines'] if 'checks:' in x or 'ALL GATES' in x]
        print(record['path'], '; '.join(tallies))
    for check in snapshot['checks']:
        print(check['name'], check['conclusion'])


if __name__ == '__main__':
    main()
