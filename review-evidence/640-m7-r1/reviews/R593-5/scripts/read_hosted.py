#!/usr/bin/env python3
"""Read the assigned hosted run; retain raw logs only after jobs finish."""
import io
import json
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

packet = Path(__file__).resolve().parents[1]
repo = 'repos/kebag-logic/milan-fpga'
run_id = 38529993870
head = '4c5d70b50230fbd5da347852d39daf7f23b3df0b'
scratch = packet / 'scratch/hosted'
scratch.mkdir(parents=True, exist_ok=True)

def raw(endpoint):
    return subprocess.check_output(['gh', 'api', '--allow-escape-sequences', f'{repo}/{endpoint}'])

def api(endpoint):
    return json.loads(raw(endpoint))

run = api(f'actions/runs/{run_id}')
assert run['head_sha'] == head
jobs = api(f'actions/runs/{run_id}/jobs?per_page=100')
snapshot = dict(observed_at=datetime.now(timezone.utc).isoformat(), run=run, jobs=jobs)
(scratch / 'observation-full.json').write_text(json.dumps(snapshot, indent=2) + '\n')
run_fields = ('id', 'name', 'head_sha', 'event', 'status', 'conclusion', 'run_attempt', 'html_url', 'created_at', 'updated_at', 'run_started_at')
job_fields = ('id', 'name', 'run_id', 'head_sha', 'status', 'conclusion', 'html_url', 'started_at', 'completed_at', 'steps')
public = dict(observed_at=snapshot['observed_at'], run={k: run[k] for k in run_fields if k in run}, jobs={'jobs': [{k: j[k] for k in job_fields if k in j} for j in jobs['jobs']]})
(packet / 'receipts/hosted-observation.json').write_text(json.dumps(public, indent=2) + '\n')
for job in jobs['jobs']:
    print(job['id'], job['name'], job['status'], job['conclusion'], flush=True)
if '--download' not in sys.argv:
    sys.exit(0)
for job in jobs['jobs']:
    if not (job['name'].startswith('Verilator shard') or job['name'] in {'verilator-suites', 'full-ci-gate', 'yosys-portability'}):
        continue
    if job['status'] != 'completed' or job['conclusion'] == 'skipped':
        continue
    saved = scratch / f"job-{job['id']}.raw.log"
    data = saved.read_bytes() if saved.exists() else raw(f"actions/jobs/{job['id']}/logs")
    saved.write_bytes(data)
    clean = re.sub(rb'\x1b\[[0-?]*[ -/]*[@-~]', b'', data).decode(errors='replace')
    (scratch / f"job-{job['id']}.log").write_text(clean)
    needles = ('HEAD is now', 'PR_HEAD_SHA:', 'event=pull_request', 'target SHA', 'target-sha',
               'TARGET_SHA', 'ci_events: OK', 'draft=false rtl=true run_full=true',
               'shard: ', 'PASS     ', 'FAIL     ', 'TIMEOUT  ', 'suites:', 'checks:',
               'gptp_tables', 'suite_tally', 'total checks', '0 failed', 'target_sha=',
               'RESULT:', '36 checks', 'UNKNOWN', 'SUM', 'TOTAL', 'consistent', 'matched')
    excerpt = '\n'.join(line for line in clean.splitlines() if any(n in line for n in needles)) + '\n'
    (packet / 'receipts' / f"hosted-job-{job['id']}.log").write_text(excerpt)
artifacts = api(f'actions/runs/{run_id}/artifacts?per_page=100')
(packet / 'receipts/hosted-artifacts.json').write_text(json.dumps(artifacts, indent=2) + '\n')
for item in artifacts['artifacts']:
    if not item['name'].startswith('suite-logs-'):
        continue
    saved = scratch / f"{item['name']}.zip"
    data = saved.read_bytes() if saved.exists() else raw(f"actions/artifacts/{item['id']}/zip")
    saved.write_bytes(data)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        (packet / 'receipts' / f"{item['name']}-inventory.txt").write_text('\n'.join(names) + '\n')
        for name in names:
            if name.endswith('TARGET_SHA'):
                text = archive.read(name).decode()
                (packet / 'receipts' / f"{item['name']}-TARGET_SHA.txt").write_text(text)
            if name.endswith('gptp_tables.log'):
                text = archive.read(name).decode(errors='replace')
                (scratch / 'gptp_tables.raw.log').write_text(text)
                start = text.index('stimulus:')
                # Runtime and campaign lines verbatim; skip unrelated compiler paths.
                lines = text[start:].splitlines()
                selected = [line for line in lines if not line.startswith(('make[', 'make:', 'g++', 'python3 ', 'Verilator'))]
                (packet / 'receipts/hosted-gptp-tables.log').write_text('\n'.join(selected) + '\n')
print('Downloaded completed-job evidence; unfinished jobs are not successes.', flush=True)
