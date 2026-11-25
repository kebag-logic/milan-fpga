#!/usr/bin/env python3
"""Usage: python3 read_hosted.py OUTDIR. Read only the four published run IDs."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys

out = Path(sys.argv[1])
expected = 'b0f2bc1a784d9f006204491c883ac2b1783e970a'
runs = (45550366428, 45550366444, 45550366332, 45550366343)
def get(path):
    return json.loads(subprocess.check_output(['gh', 'api', 'repos/kebag-logic/milan-fpga/'+path]))
def inspect(run_id):
    r = get(f'actions/runs/{run_id}')
    assert r['head_sha'] == expected, (run_id, r['head_sha'])
    jobs = []
    page = 1
    while True:
        j = get(f'actions/runs/{run_id}/jobs?per_page=100&page={page}')
        jobs.extend(j['jobs'])
        if len(jobs) >= j['total_count']:
            break
        page += 1
    run = {k:r[k] for k in ('id','head_sha','event','status','conclusion','run_attempt','html_url')}
    run['jobs'] = []
    for j in jobs:
        job = {k:j[k] for k in ('id','name','status','conclusion','started_at','completed_at','html_url')}
        job['steps'] = [{k:s.get(k) for k in ('name','status','conclusion','started_at','completed_at')} for s in j['steps']]
        run['jobs'].append(job)
    return run
with ThreadPoolExecutor(max_workers=4) as pool:
    result = list(pool.map(inspect, runs))
(out/'hosted-api.json').write_text(json.dumps(result, indent=2)+'\n')
lines = ['run\tjob\tconclusion\tseconds\tminutes']
for r in result:
    print(r['id'], r['conclusion'], 'attempt', r['run_attempt'], len(r['jobs']), 'jobs')
    for j in r['jobs']:
        # A skipped job has no execution duration, even if API timestamps exist.
        seconds = ''
        if j['conclusion'] != 'skipped' and j['started_at'] and j['completed_at']:
            seconds = (datetime.fromisoformat(j['completed_at'].replace('Z','+00:00')) - datetime.fromisoformat(j['started_at'].replace('Z','+00:00'))).total_seconds()
        minutes = '' if seconds == '' else f'{seconds/60:.3f}'
        lines.append(f"{r['id']}\t{j['name']}\t{j['conclusion']}\t{seconds}\t{minutes}")
(out/'hosted-minutes.tsv').write_text('\n'.join(lines)+'\n')
print('PASS: all run heads match requested source head; executed and skipped jobs retained separately')
