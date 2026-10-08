#!/usr/bin/env python3
"""Capture read-only public decisions and exact-head hosted execution status."""
import concurrent.futures
import json
from pathlib import Path
import subprocess

REPO = 'repos/kebag-logic/milan-fpga/'
HEAD = '9c601b5983acfd60fb269b9a88c27b48cab7cf65'

def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', REPO + path]))

def main():
    out = Path(__file__).resolve().parent
    comments = [6029233665, 6043036997, 6047563934, 6050832603,
                6051028263, 6052017268, 6052220964, 6052221929]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        decisions = list(pool.map(lambda n: api(f'issues/comments/{n}'), comments))
    selected = [{k: d[k] for k in ['id', 'html_url', 'created_at', 'updated_at', 'body']} for d in decisions]
    (out / 'public-decisions.json').write_text(json.dumps(selected, indent=2) + '\n')
    issue = api('issues/686')
    (out / 'public-issue.json').write_text(json.dumps({k: issue[k] for k in ['number', 'title', 'body', 'html_url']}, indent=2) + '\n')
    pr = api('pulls/695')
    assert pr['head']['sha'] == HEAD
    (out / 'public-pr.json').write_text(json.dumps({
        'number': pr['number'], 'head': pr['head']['sha'], 'html_url': pr['html_url'],
        'body': pr['body'], 'state': pr['state'], 'draft': pr['draft']}, indent=2) + '\n')
    d = api('commits/' + HEAD + '/check-runs?per_page=100')
    checks = [{k: r[k] for k in ['id', 'name', 'head_sha', 'status', 'conclusion', 'details_url', 'started_at', 'completed_at']}
              for r in d['check_runs']]
    assert len(checks) == d['total_count']
    assert all(c['head_sha'] == HEAD for c in checks)
    ids = [c['details_url'].split('/job/')[-1].split('?')[0] for c in checks
           if '/job/' in c['details_url']]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        jobs = list(pool.map(lambda n: api('actions/jobs/' + n), ids))
    jobs = [{k: j[k] for k in ['id', 'name', 'head_sha', 'conclusion', 'steps']} for j in jobs]
    (out / 'hosted-checks.json').write_text(json.dumps(checks, indent=2) + '\n')
    (out / 'hosted-job-steps.json').write_text(json.dumps(jobs, indent=2) + '\n')
    for c in checks:
        print(c['name'], c['conclusion'])
    print('Snapshot only; workflow acceptance remains the manager duty.')

if __name__ == '__main__':
    main()
