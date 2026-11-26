#!/usr/bin/env python3
"""Audit downloaded public manifests and derive the zero-mixing input."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

source, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
out = packet/'receipts'
out.mkdir(exist_ok=True)
checks=[]
for round_ in ['r1','r2']:
    d=packet/'scratch/review-evidence'/('adpseed-'+round_)
    for row in json.loads((d/'MANIFEST.json').read_text()):
        digest=hashlib.sha256((d/row['file']).read_bytes()).hexdigest()
        assert digest==row['published_sha256']
        checks.append(dict(round=round_,file=row['file'],sha256=digest,verified=True))
(out/'packet-integrity.json').write_text(json.dumps(checks,indent=2)+'\n')
mutants=json.loads((source/'tests/mutations.json').read_text())
d=packet/'scratch/review-evidence/adpseed-r2/author/receipts'
log=(d/'tsn-c-stack-mutation.log').read_text()
caught=[s.split(' ',1)[1] for s in log.splitlines() if s.startswith('CAUGHT ')]
assert len(caught)==len(set(caught))==len(mutants)==512
assert set(caught)=={x['name'] for x in mutants}
gates=json.loads((d/'tsn-c-stack-gates.json').read_text())
assert len(gates)==28 and all(g['rc']==0 for g in gates)
rv=json.loads((d/'tsn-c-stack-rv32.log').read_text())
assert {x['configuration'] for x in rv}=={'Debug','Release'}
assert all(x['rc']==0 and not x['unresolved_final'] for x in rv)
def git(*args):
    return subprocess.check_output(['git','-C',str(source),*args],text=True).strip()
ancestry={}
for ref in ['9e1cd60f','a795471c']:
    merged=git('merge-tree','--write-tree',ref,'HEAD')
    assert merged==git('rev-parse','HEAD^{tree}')
    ancestry[git('rev-parse',ref)]=merged
facts=dict(manifest_rows=len(checks),caught=512,gates=28,rv32=['Debug','Release'],ancestry=ancestry,tree=git('rev-parse','HEAD^{tree}'),gitlinks=[s for s in git('ls-tree','-r','HEAD').splitlines() if s.startswith('160000')])
(out/'evidence-audit.json').write_text(json.dumps(facts,indent=2)+'\n')

mod=1<<32
mask=mod-1
def undo_right(y,n):
    x=y
    for shift in range(n,32,n): x ^= y>>shift
    return x
def inverse(y):
    y=undo_right(y,16)
    y=y*pow(2057,-1,mod)&mask
    y=undo_right(y,4)
    y=y*pow(5,-1,mod)&mask
    y=undo_right(y,12)
    return (y+1)*pow(32767,-1,mod)&mask
def mix(x):
    x=(x*32767-1)&mask
    x^=x>>12
    x=x*5&mask
    x^=x>>4
    x=x*2057&mask
    return x^(x>>16)
eid=0x1122334455667788
mac=0x001B921122AA
fold=(eid&mask)^(eid>>32)
outer_input=inverse(0)
summed=inverse(outer_input^fold)
sample=(summed-mac)&mask
assert sample==0xDE81995D
assert mix(mix((mac+sample)&mask)^fold)==0
def step(x):
    x ^= (x<<13)&mask
    x ^= x>>17
    x ^= (x<<5)&mask
    return x
assert step(1)==0x42021 and step(0)==0
math=dict(entity_fold=hex(fold),outer_zero_preimage=hex(outer_input),sum=hex(summed),sample=hex(sample),mixed=0,fallback=1,first_state=hex(step(1)),zero_fixed_point=step(0),wrap_sum=hex((0xffffffff+5)&mask),end_around_sum=5,odd_multipliers=[32767,5,2057])
(out/'arithmetic.json').write_text(json.dumps(math,indent=2)+'\n')
print(json.dumps(facts,indent=2))
print(json.dumps(math,indent=2))
checks=[]
for name in ['docs/TESTS.md','docs/TRACEABILITY.md']:
    for test,path,line in re.findall(r'\[([^\]]+)\]\(\.\./(tests/[^#)\s]+)#L(\d+)\)',(source/name).read_text()):
        assert 'TEST' in (source/path).read_text().splitlines()[int(line)-1]
        checks.append([name,test,path,int(line)])
unchanged=['include/adp.h','tests/coverage.ratchet','docs/COVERAGE.md','CMakeLists.txt','examples/rv32/smoke.c']
for name in unchanged: assert not git('diff','5e6ab995..HEAD','--',name)
assert not git('diff','--check','5e6ab995..HEAD')
(out/'docs-audit.json').write_text(json.dumps(dict(test_line_links_checked=len(checks),unchanged=unchanged,diff_check='PASS'),indent=2)+'\n')
