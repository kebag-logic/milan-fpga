#!/usr/bin/env python3
"""Read exact-publication runtime receipts and compare recorded artifact hashes."""
import json
import re
import subprocess

REV='82a41140e1a7cc7779ab05eef732e569cb8a6157'
BASE='review-evidence/584-r1/'
HEAD='599c79af9cfe242bc3d60dd1c80f3e8d57cca12e'
def read(name):
    return subprocess.check_output(['git','--no-replace-objects','show',REV+':'+BASE+name],text=True)

for name, expected in [
    ('ship8.log', ['checks: 130   failures: 0', 'ship8_rc=0']),
    ('ship8-mutants.txt', ['11 checks: 11 PASS, 0 FAIL', 'mutants_rc=0', '--defect-stale-rebind', '--defect-stale-reset']),
    ('milan_dp_render-suite.txt', ['checks: 263   failures: 0', 'checks: 79   failures: 0', 'checks: 130   failures: 0', '5 checks: 5 PASS, 0 FAIL', 'suite_rc=0']),
    ('rebind1.log', ['[FAIL] B3 FRESHNESS: from the rebind', '12 stale', 'rc=1']),
    ('reset1.log', ['[FAIL] Z3 FRESHNESS: from the rebind', '12 stale', 'rc=1']),
]:
    artifact='author-r3/receipts/rtl/'+name
    data=read(artifact)
    for text in expected:
        assert text in data, (name,text)
    if name in ('ship8.log','ship8-mutants.txt','milan_dp_render-suite.txt'):
        assert 'Head: '+HEAD in data
    print('ARTIFACT',artifact)
    for n,line in enumerate(data.splitlines(),1):
        if any(x in line for x in ('record:', 'FRESHNESS:', '[FAIL]', 'checks:', '_rc=', 'rc=', 'leg defect caught')):
            print(f'{n}: {line}')

old=json.loads(read('author-r1/receipts/builder/artifacts-receipt.json'))['head']
baseline=json.loads(read('author-r3/receipts/builder/final-artifacts.json'))
assert old == baseline, 'carried final-artifacts is the round-1 baseline'
new=json.loads(read('author-r3/receipts/builder/r3-artifacts.json'))
assert old.keys()==new.keys()
total=same=0
differences=[]
for point in sorted(old):
    a,b=old[point]['files'],new[point]['files']
    assert a.keys()==b.keys()
    for name in a:
        total+=1
        if a[name]==b[name]: same+=1
        else: differences.append((point,name,a[name]['bytes'],b[name]['bytes']))
    assert {k:v for k,v in old[point].items() if k!='files'}=={k:v for k,v in new[point].items() if k!='files'}
assert total==155 and same==153
assert {x[:2] for x in differences}=={('endstation_ax7101_8x8/'+p,'build_plan.md') for p in ('all-fabric','split')}
assert all(b-a==17 for _,_,a,b in differences)
print(f'ARTIFACT-HASH COMPARISON: {same}/{total} identical; differences={differences}')
print('All recorded model IDs, descriptor counts, cluster counts and size metadata unchanged from round 1.')
summary=read('author-r3/receipts/docs/workflow-summary.txt')
rows=re.findall(r'^\d+[^\n]*? rc=(\d+)',summary,re.M)
assert len(rows)==103 and rows.count('0')==99
print('Published docs commands: 99/103 rc=0; four hosted-environment failures, not passes.')
for line in summary.splitlines():
    if re.search(r' rc=[1-9]',line): print(line)
union=read('author-r3/receipts/gates/builder-union.txt')
assert HEAD in union and '113 gates exactly once' in union and '2 arm(s) did not run' in union and 'rc=0' in union
print('Published builder union: exact head, 113 gates once, two recorded NOT RUN arms, rc=0.')
print('PASS: publication is internally consistent for these execution and artifact claims.')
