#!/usr/bin/env python3
"""Read-only exact-head workflow snapshot; preserve execution and skip states."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

HEAD = '97e713168470bfae2685521fa557dc462b782b32'
REPO = 'kebag-logic/milan-fpga'
packet = Path(__file__).resolve().parent

def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', path], text=True))

def subset(obj, keys):
    return {key: obj.get(key) for key in keys.split()}

def one_run(run):
    row = subset(run, 'id name head_sha event status conclusion html_url created_at')
    data = api(f'repos/{REPO}/actions/runs/{run["id"]}/jobs?per_page=100')
    assert data['total_count'] <= 100, 'job pagination required'
    row['jobs'] = []
    for job in data['jobs']:
        result = subset(job, 'id name status conclusion started_at completed_at html_url')
        result['steps'] = [subset(step, 'name status conclusion number started_at completed_at')
                           for step in job['steps']]
        row['jobs'].append(result)
    return row

runs = api(f'repos/{REPO}/actions/runs?head_sha={HEAD}&per_page=100')
assert runs['total_count'] <= 100, 'run pagination required'
pr = api(f'repos/{REPO}/pulls/705')
assert pr['head']['sha'] == HEAD, 'published head has changed'
with ThreadPoolExecutor(max_workers=4) as pool:
    result = {'observed_utc': datetime.now(timezone.utc).isoformat(),
              'pr': {'head': pr['head']['sha'], 'base': pr['base']['sha'],
                     'draft': pr['draft'], 'url': pr['html_url']},
              'runs': list(pool.map(one_run, runs['workflow_runs']))}
(packet / 'hosted-final.json').write_text(json.dumps(result, indent=2) + '\n')
print(result['observed_utc'])
for run in result['runs']:
    print(run['id'], run['name'], run['status'], run['conclusion'])
    for job in run['jobs']:
        print(' ', job['name'], job['status'], job['conclusion'],
              job['started_at'], job['completed_at'])
