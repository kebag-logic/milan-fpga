#!/usr/bin/env python3
"""Check the public documentary correction against its adopted authorities."""
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
pr = json.loads((packet / 'pr.json').read_text())
comments = json.loads((packet / 'issue_comments.json').read_text())
correction = next(c for c in comments if c['id'] == 6389770127)
replacement = ('The behave sweep uses generic ENTITY[0] operands and its GET_AVB_INFO inventory row returns SUCCESS; '
               'it does not grade the wrong-type wire response. It contains no status-1 expectation for this case. '
               'The processor V5 tests and the parent-boundary probe establish the adopted status.')
assert replacement in correction['body']
assert replacement in pr['body']
assert pr['head_sha'] == '25f05752f7e50e3cf7e27008e434ffde930b4b6f'
assert 'docs/00_MILAN_COMPLIANCE_REVIEW.md`, section 8, row 14' in pr['body']
assert 'docs/architecture/06_aecp_engine.md` section 6.10' in pr['body']
print('PASS correction issuecomment-6389770127 and PR body contain exact F1 replacement')
print('PASS PR metadata head:', pr['head_sha'])
print('PASS PR compliance pointer names section 8 row 14 and implementation section 6.10')
pin = 'ed2118035e4cec76fb1b59cfbf8a053aeacc8af8'
for path, first, last in [('docs/00_MILAN_COMPLIANCE_REVIEW.md', 581, 598),
                          ('docs/architecture/06_aecp_engine.md', 974, 1013)]:
    data = subprocess.check_output(['git', '-C', 'protocol-processor', 'show', pin + ':' + path],
                                   env={**__import__('os').environ, 'GIT_NO_REPLACE_OBJECTS': '1'}).decode()
    section = data.splitlines()[first-1:last]
    assert any('GET_AVB_INFO' in line for line in section)
    assert any('NOT_SUPPORTED' in line for line in section)
    print('\nAUTHORITY', pin, path)
    for number, line in enumerate(section, first):
        print(f'{number}: {line}')
prior = next(c for c in pr['comments'] if c['id'] == 6389766089)
assert prior['body'].startswith('[R696] NEGATIVE - exact head ' + pr['head_sha'])
assert '5db8e8298734d18c8a50ba24cd8c46140292302b' in prior['body']
assert 'R696-1-F1: MINOR; Tests, Docs' in prior['body']
assert 'R696-1-R1: RESIDUE; Docs' in prior['body']
print('\nPASS prior public findings reconciled: F1 (Tests, Docs), R1 (Docs); same head and tree')
