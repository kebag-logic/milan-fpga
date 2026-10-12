#!/usr/bin/env python3
"""Read the ten complete attempt job records and independently derive timings."""
import concurrent.futures
from datetime import datetime
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
head = '941e15593ef3dbf561bd8ed75aaf680f5d146a41'
run_id = 38180290290
jobs = ['firmware-unit', 'firmware-control-mutants', 'firmware-srp-mutants', 'firmware-aecp-mutants']
expected = [[695,611,524,187], [697,899,625,244], [677,895,697,256], [426,894,715,241], [551,814,575,254], [675,897,638,210], [683,588,712,176], [672,625,494,220], [691,916,482,223], [705,916,486,250]]

def api(endpoint, name):
    raw = subprocess.check_output(['gh', 'api', 'repos/kebag-logic/milan-fpga/' + endpoint])
    (packet / name).write_bytes(raw)
    return json.loads(raw)

def attempt(n):
    run = api(f'actions/runs/{run_id}/attempts/{n}', f'actions-attempt-{n}.json')
    result = api(f'actions/runs/{run_id}/attempts/{n}/jobs?per_page=100', f'actions-jobs-{n}.json')
    assert run['head_sha'] == head and run['run_attempt'] == n
    assert run['event'] == 'pull_request'
    assert result['total_count'] == len(result['jobs'])
    row = []
    for name in jobs:
        found = [j for j in result['jobs'] if j['name'] == name]
        assert len(found) == 1, (n, name)
        job = found[0]
        assert job['head_sha'] == head and job['conclusion'] == 'success'
        assert job['status'] == 'completed' and job['run_attempt'] == n
        assert all(s['conclusion'] == 'success' for s in job['steps']), (n,name,job['steps'])
        seconds = int((datetime.fromisoformat(job['completed_at']) - datetime.fromisoformat(job['started_at'])).total_seconds())
        assert seconds <= 1890
        row.append(seconds)
    assert row == expected[n-1], (n,row,expected[n-1])
    return dict(attempt=n, seconds=row, conclusion=run['conclusion'], job_conclusions={j['name']:j['conclusion'] for j in result['jobs']})

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(attempt, range(1,11)))
maxima = [max(row['seconds'][i] for row in rows) for i in range(4)]
summary = dict(head=head, run_id=run_id, jobs=jobs, rows=rows, maxima=maxima, slowest_percent=max(maxima)/2700*100)
(packet / 'hosted-verification.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
