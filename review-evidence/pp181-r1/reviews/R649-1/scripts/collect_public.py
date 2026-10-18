#!/usr/bin/env python3
"""Read-only public metadata inventory, after the independent verdict is written."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--packet', required=True, type=Path)
a = p.parse_args()
out = a.packet / 'receipts'
def api(endpoint):
    return json.loads(subprocess.check_output(['gh', 'api', endpoint]))
def pages(endpoint):
    groups = json.loads(subprocess.check_output(['gh', 'api', '--paginate', '--slurp', endpoint]))
    return [row for group in groups for row in group]
repo = 'repos/Mister-M-alt/protocol-processor-control-plane-avb-milan'
comments = {}
for name, endpoint in [('issue181', '/issues/181/comments'), ('pr187', '/issues/187/comments'),
                       ('pr187-reviews', '/pulls/187/reviews'), ('pr187-inline', '/pulls/187/comments')]:
    comments[name] = pages(repo + endpoint)
    (out / (name + '-public-final.json')).write_text(json.dumps(comments[name], indent=2)+'\n')
head = '42eb9aef3642f6d98058fe634a70f6a9c749cd25'
checks = api(repo + '/commits/' + head + '/check-runs')
(out / 'hosted-checks-final.json').write_text(json.dumps(checks, indent=2)+'\n')
runs = api(repo + '/actions/runs?head_sha=' + head)
(out / 'hosted-runs-final.json').write_text(json.dumps(runs, indent=2)+'\n')
jobs = []
for run in runs['workflow_runs']:
    rows = api(repo + '/actions/runs/' + str(run['id']) + '/jobs?per_page=100')
    (out / ('hosted-jobs-' + str(run['id']) + '.json')).write_text(json.dumps(rows, indent=2)+'\n')
    jobs += [{'run': run['id'], 'name': row['name'], 'status': row['status'], 'conclusion': row['conclusion'],
              'steps': [{'name': s['name'], 'status': s['status'], 'conclusion': s['conclusion']} for s in row['steps']]}
             for row in rows['jobs']]
evidence_sha = '5131f4ad9f4e4a9e8bd195c78a693e59aa4d9859'
tree = api('repos/kebag-logic/milan-fpga/git/trees/' + evidence_sha + '?recursive=1')
assert not tree['truncated']
files = [row for row in tree['tree'] if row['path'].startswith('review-evidence/pp181-r1/')]
inventory = {'captured_utc': datetime.now(timezone.utc).isoformat(), 'parent_commit': evidence_sha,
             'tree_response_truncated': False, 'published_evidence_entries': files,
             'public_comment_counts': {k:len(v) for k,v in comments.items()},
             'public_comment_index': {k:[{'id': c['id'], 'url': c['html_url'], 'first_line': (c.get('body') or '').split('\n')[0]} for c in v] for k,v in comments.items()},
             'hosted_jobs': jobs,
             'independent_verdict_sha256': hashlib.sha256((out / 'independent-verdict-before-prior-findings.md').read_bytes()).hexdigest()}
(out / 'public-evidence-audit.json').write_text(json.dumps(inventory, indent=2)+'\n')
print(json.dumps(inventory, indent=2))
