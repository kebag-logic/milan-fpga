#!/usr/bin/env python3
"""Summarize published receipts without treating summaries as new executions."""
import json
from pathlib import Path
import re
import sys

packet=Path(__file__).resolve().parent
public=packet/'scratch/public/review-evidence/train1123-r1'
rows={}
def read(path):
    return (public/path).read_text()
for point in ('1x1-1if','8x8-1if'):
    path=f'author/receipts/budget/cpu-{point}-formal-c2b2ba1a.md'
    text=read(path)
    legs=re.findall(r'^- (\S+) (part\d+): (\d+) groups; rc (\d+); image ([0-9a-f]+); HEAD ([0-9a-f]+)',text,re.M)
    assert len(legs)==12 and sum(int(x[2]) for x in legs)==245
    hashes={}
    for arm,part,n,rc,sha,head in legs:
        assert head=='c2b2ba1a4742335e0678ec1f00f9033d1913b1da'
        assert hashes.setdefault(arm,sha)==sha
    rows[point]=dict(artifact=path,legs=legs,groups=245,images=hashes,
                    summary=[l for l in text.splitlines() if 'work passes over the per-pass share' in l],
                    survey=[l for l in text.splitlines() if 'statement(s) exceeded' in l or l.startswith('record_classes')])
for part in range(4):
    path=f'author/receipts/firmware/fw-gate-f5a1585e-s{part}.txt'
    text=read(path)
    assert 'test_ctrl_firmware: PASS' in text and 'porcelain-after 0 END rc=0' in text
    assert '2003 live invocations in exactly one shard' in text
    rows[f'firmware-shard-{part}']=dict(artifact=path,ok_lines=len(re.findall(r'^\[ok\]',text,re.M)),
                                     ending=text.splitlines()[-2:])
path='author/receipts/firmware/builder-union-c2b2ba1a.json.txt'
text=read(path)
data=json.loads(text[text.index('{'):])
pop=[name for leg in data['legs'] for name in leg['cases']]
assert len(pop)==len(set(pop))==113 and data['union']=='pass'
rows['builder']=dict(artifact=path,union=data['union'],distinct_cases=len(pop),not_run=data['not_run'])
for point in ('1x1','8x8-1if'):
    for arm in ('arm-A','answering-ports'):
        path=f'author-r2/receipts/budget/kept-grade-{point}-{arm}-r2.txt'
        text=read(path)
        assert 'kept_grade: PASS (0 finding(s)' in text
        rows[f'kept-{point}-{arm}']=dict(artifact=path,lines=[l for l in text.splitlines()
            if l.startswith(('KEPT <= BOUND','SHARE','BUILD','OWED','kept_grade:'))])
for route in ('8x8-ExtraPostPlacementOpt','1x1-ExtraTimingOpt','1x1-ExtraPostPlacementOpt'):
    path=f'author/receipts/route/{route}'
    rows[route]=dict(artifact=path,signoff=read(path+'/signoff.txt').splitlines(),
                    utilization=read(path+'/utilization.txt').splitlines()[0],
                    identity=read(path+'/identity.log').strip())
path='author-r2/receipts/docs/docs-workflow-steps-43076d0f.txt'
text=read(path)
rows['docs']=dict(artifact=path,passed=len(re.findall(r'\trc=0\t',text)),
                  refused=[l for l in text.splitlines() if '\trc=1\t' in l],
                  skipped=len(re.findall(r'\tSKIP\t',text)))
for key,path in [('suites-A','author/receipts/rtl/suites-A-c2b2ba1a.txt'),
                 ('suites-B','author/receipts/rtl/suites-B-c2b2ba1a.txt'),
                 ('suites-C','author/receipts/rtl/suites-C-c2b2ba1a.txt')]:
    rows[key]=dict(artifact=path,receipt=read(path))
print(json.dumps(rows,indent=2))
