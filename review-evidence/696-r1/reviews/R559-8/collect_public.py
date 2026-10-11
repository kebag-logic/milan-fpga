#!/usr/bin/env python3
"""Collect selected public task decisions and historical executable receipts."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

EVIDENCE = '97f433d668907446e83c074b21e81d03a34988af'
PREFIX = 'review-evidence/696-r1/author/merge-receipts/'

def main():
    root = Path(sys.argv[1]).resolve()
    packet = Path(__file__).resolve().parent
    out = packet / 'public-evidence'
    out.mkdir(exist_ok=True)
    def git(path):
        return subprocess.check_output(['git', '-C', str(root), 'show', EVIDENCE + ':' + PREFIX + path])
    index = {}
    for n in range(1, 15):
        for row in json.loads(git(f'PROVENANCE-{n:03}.json'))['receipts']:
            index[row['published'].removeprefix('merge-receipts/')] = row
    selected = ['PROVENANCE.json', 'parent-suites-results.json',
                'focus-merged/results.json', 'focus-merged/maap-unit.log',
                'focus-merged/maap-mutants.log', 'focus-merged/maap-integration.log',
                'focus-merged/maap-coverage.log', 'check-route-1x1.log',
                'check-ooc-1x1.log', 'check-ooc-8x8.log', 'record.log', 'maap-ooc-results.json']
    receipts = []
    for path in selected:
        data = git(path)
        digest = hashlib.sha256(data).hexdigest()
        if path in index:
            assert digest == index[path]['published_sha256'], path
            assert len(data) == index[path]['published_bytes'], path
        name = path.replace('/', '__')
        (out / name).write_bytes(data)
        receipts.append({'path': PREFIX + path, 'sha256': digest, 'bytes': len(data),
                         'manifest_verified': path in index})
    (out / 'receipt-index.json').write_text(json.dumps({'commit': EVIDENCE, 'receipts': receipts}, indent=2) + '\n')
    def api(path):
        return json.loads(subprocess.check_output(['gh', 'api', path]))
    repo = 'repos/kebag-logic/milan-fpga/'
    issue = api(repo + 'issues/696')
    (out / 'issue.json').write_text(json.dumps({'url': issue['html_url'], 'body': issue['body']}, indent=2) + '\n')
    ids = [6076750392, 6076940309, 6079087547, 6079463350, 6080332335,
           6089712293, 6102832618, 6103504186, 6113981032]
    comments = []
    for ident in ids:
        data = api(repo + f'issues/comments/{ident}')
        comments.append({'id': ident, 'url': data['html_url'], 'body': data['body']})
    (out / 'scope-and-evidence-comments.json').write_text(json.dumps(comments, indent=2) + '\n')
    data = api(repo + 'commits/aa980479aafd1d72c72015707fa6618b5aa47cb1/check-runs?per_page=100')
    checks = [{k: x[k] for k in ['name', 'head_sha', 'status', 'conclusion', 'started_at', 'completed_at', 'details_url']} for x in data['check_runs']]
    (packet / 'hosted-observation.json').write_text(json.dumps(checks, indent=2) + '\n')
    print(f'Collected {len(receipts)} historical receipts and {len(comments)} public scope/evidence comments.')

if __name__ == '__main__':
    main()
