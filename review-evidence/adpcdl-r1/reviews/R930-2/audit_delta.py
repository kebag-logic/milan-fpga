#!/usr/bin/env python3
"""Read-only delta/document checks and exact-head hosted status capture."""
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
head = 'ec727b64663b4eef2fc8da1ea5e0eae6541597d1'
prior = 'e0b144904e57c96928f1dd3fca36a00df42f6ed3'
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True)

assert not git('diff', '--name-only', prior, head, '--', 'src', 'include')
assert not git('diff', '--check', prior, head)
mutations = json.loads((root/'tests/mutations.json').read_text())
assert len(mutations) == 489
links = []
for doc in ['docs/TRACEABILITY.md', 'docs/TESTS.md']:
    text = (root/doc).read_text()
    for name, path, line in re.findall(r'\[([^\]]+)\]\(\.\./(tests/[^#)]+)#L(\d+)\)', text):
        if path != 'tests/test_adp.cpp':
            continue
        actual = (root/path).read_text().splitlines()[int(line)-1]
        suite, test = name.split('.', 1)
        assert re.search(r'\bTEST(?:_P|_F)?\(' + re.escape(suite) + r',\s*' + re.escape(test) + r'\)', actual), (doc,name,line)
        links.append({'document': doc, 'test': name, 'line': int(line)})
assert '[Issue 37](https://github.com/kebag-logic/tsn-c-stack/issues/37) replaced the exact-length rule of issue 3' in (root/'docs/REQUIREMENTS.md').read_text()
assert '[issue 37](https://github.com/kebag-logic/tsn-c-stack/issues/37)' in (root/'CHANGELOG.md').read_text().splitlines()[4]
delta = git('diff', '--unified=0', prior, head, '--', 'tests/test_adp.cpp', 'examples/rv32/smoke.c')
comments = [line[1:] for line in delta.splitlines() if line.startswith('+') and '//' in line]
assert all(re.search(r'//\s*(?:IEEE|Milan|REQ:)', line) for line in comments)
result = {'head': head, 'prior': prior, 'production_unchanged': True, 'plant_count': len(mutations),
          'adp_document_links': links, 'issue_origin_and_changelog': 'PASS',
          'new_comment_lines': comments, 'whitespace': 'PASS'}
(out/'delta-audit.json').write_text(json.dumps(result,indent=2)+'\n')
def api(path):
    return json.loads(subprocess.check_output(['gh','api','repos/kebag-logic/tsn-c-stack/'+path]))
run = api('actions/runs/45684809576')
assert run['head_sha'] == head
jobs = api('actions/runs/45684809576/jobs')['jobs']
status = {k:run[k] for k in ['id','head_sha','status','conclusion','html_url','event']}
status['jobs'] = [{k:j[k] for k in ['id','name','status','conclusion','steps']} for j in jobs]
(out/'public-status.json').write_text(json.dumps(status,indent=2)+'\n')
print(f'PASS: {len(links)} ADP document links, 489 plants, issue origin, comments, unchanged production, hosted status.')
