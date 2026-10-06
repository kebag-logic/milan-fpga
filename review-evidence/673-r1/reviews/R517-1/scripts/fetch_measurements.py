#!/usr/bin/env python3
"""Retrieve the frozen public survey inputs without accessing private storage."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import base64
from pathlib import Path
import re
import subprocess
import sys

packet = Path(sys.argv[1]).resolve()
(packet / 'scratch').mkdir(exist_ok=True)
source = 'contents/review-evidence/673-r1/author/HANDOFF.md?ref=ff5010496ab2c4efdd8a7e89b36463f7d5fb0ee4'
body = subprocess.check_output(['gh', 'api', 'repos/kebag-logic/milan-fpga/' + source])
handoff = base64.b64decode(json.loads(body)['content']).decode()
(packet / 'scratch/public-HANDOFF.md').write_text(handoff)
out = packet / 'scratch/hosted'
out.mkdir(exist_ok=True)
receipts = packet / 'receipts/hosted'
receipts.mkdir(parents=True, exist_ok=True)
runs = ['37457223191', '37455131093', '37453634481', '37445962113',
        '37439568024', '37432004413', '37430728685', '37429204551',
        '37424768281', '37420502040']
entries = re.findall(r'\| resume-hosted/job-(\d+)\.log \| (\d+) \| ([a-f0-9]{64}) \|', handoff)
assert len(entries) == 39
work = [(f'run-{run}.json', f'actions/runs/{run}/jobs?per_page=100', None, None)
        for run in runs]
work += [(f'job-{job}.log', f'actions/jobs/{job}/logs', int(size), digest)
         for job, size, digest in entries]

def fetch(item):
    name, api, size, expected = item
    if (out / name).exists():
        p = subprocess.CompletedProcess([], 0, (out / name).read_bytes(), b'')
    else:
        p = subprocess.run(['gh', 'api', 'repos/kebag-logic/milan-fpga/' + api,
                            '--allow-escape-sequences'], capture_output=True, timeout=90)
    result = {'file': name, 'api': api, 'rc': p.returncode}
    if p.returncode:
        result['error'] = p.stderr.decode(errors='replace')
    else:
        (out / name).write_bytes(p.stdout)
        digest = hashlib.sha256(p.stdout).hexdigest()
        result.update(bytes=len(p.stdout), sha256=digest)
        if expected:
            normalized = re.sub(rb'\x1b\[[0-?]*[ -/]*[@-~]', b'', p.stdout)
            normalized = re.sub(rb'\x1b\][^\x07]*(?:\x07|\x1b\\)', b'', normalized)
            normalized_digest = hashlib.sha256(normalized).hexdigest()
            result.update(normalized_bytes=len(normalized), normalized_sha256=normalized_digest)
            result['matches_public_hash'] = normalized_digest == expected and size == len(normalized)
            # Retain raw timestamp lines used by the calculation, byte for byte.
            selected = [line for line in p.stdout.splitlines(keepends=True)
                        if re.search(rb'(shard: \d+/\d+|(?:PASS|FAIL|TIMEOUT) +[a-z0-9_]+|driver_wall_seconds=)', line)]
            (receipts / (name + '.timestamps')).write_bytes(b''.join(selected))
        else:
            obj = json.loads(p.stdout)
            # Only public job attributes needed for arithmetic; full response stays disposable.
            jobs = [{k: job[k] for k in ('id', 'run_id', 'name', 'status', 'conclusion',
                                         'started_at', 'completed_at', 'head_sha', 'html_url')}
                    for job in obj['jobs']]
            (receipts / name).write_text(json.dumps(jobs, indent=2) + '\n')
    return result

with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(fetch, work))
(packet / 'receipts/measurement-fetch.json').write_text(json.dumps(results, indent=2) + '\n')
for result in results:
    print(json.dumps(result))
assert all(r['rc'] == 0 and r.get('matches_public_hash', True) for r in results)
