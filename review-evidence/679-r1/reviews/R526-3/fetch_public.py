#!/usr/bin/env python3
"""Fetch only the explicitly selected public scope and executable receipts."""
import hashlib
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
out = packet / 'public'
out.mkdir(exist_ok=True)
api = 'repos/kebag-logic/milan-fpga/'

def request(path, raw=False):
    command = ['gh', 'api', api + path]
    if raw:
        command += ['-H', 'Accept: application/vnd.github.raw+json']
    return subprocess.check_output(command)

issue = json.loads(request('issues/679'))
(out / 'issue-679.json').write_text(json.dumps({k:issue[k] for k in ('number','title','body','html_url')}, indent=2) + '\n')
for n in (679, 683):
    comments = json.loads(request(f'issues/{n}/comments?per_page=100'))
    selected = [{k:c[k] for k in ('id','html_url','created_at','body')} for c in comments if c['body'].startswith(('[A10]', '[A557]'))]
    (out / f'comments-{n}-scope.json').write_text(json.dumps(selected, indent=2) + '\n')
pr = json.loads(request('pulls/683'))
(out / 'pr-683.json').write_text(json.dumps({k:pr[k] for k in ('number','title','body','html_url','state','draft')}, indent=2) + '\n')
ref = '4c5eb3ab1e9ceeb076a9e274fd1a4c8cf52f72d0'
prefix = 'review-evidence/679-r1/'
manifest = request('contents/' + prefix + 'MANIFEST.json?ref=' + ref, True)
(out / 'evidence-manifest.json').write_bytes(manifest)
selected = {'author/EVIDENCE.md', 'author/TEST-MAP.md', 'author/ctrl-final.log', 'author/nvm-final.log', 'author/rv32-selftest-final.log', 'author/ci-events-check.log', 'author/ci-events-selftest.log', 'author/ci-scope-selftest.log'}
for record in json.loads(manifest):
    if record['file'] in selected:
        data = request('contents/' + prefix + record['file'] + '?ref=' + ref, True)
        assert hashlib.sha256(data).hexdigest() == record['published_sha256']
        (out / ('r1-' + Path(record['file']).name)).write_bytes(data)
        print(record['file'], record['published_sha256'], 'verified')
print('Public scope and selected source-round executable receipts fetched; no reviewer reports fetched.')
