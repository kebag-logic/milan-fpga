#!/usr/bin/env python3
"""Independently tally published logs and compare them with source documentation."""
import pathlib
import re
import sys
repo = pathlib.Path(sys.argv[1])
root = pathlib.Path(sys.argv[2]) / 'published/author-r3c/receipts/round3c'
def read(p): return (root / p).read_text()
log = read('milan-dp/leg-dynmap.log')
def counts(s):
    return len(re.findall(r'^\s*\[(?:ok|FAIL)\]', s, re.M)), len(re.findall(r'^\s*\[FAIL\]', s,re.M))
# Use actual section starts, rather than the supplied section summaries.
markers = ['-- [DYNMAP]', '-- [762-DP] the AX7101', '-- [MAPREC] #637:']
idx = [0] + [log.index(m) for m in markers] + [len(log)]
expected = [52,110,37,487]
for i,name in enumerate(['preamble','DYNMAP','762-DP','MAPREC']):
    got=counts(log[idx[i]:idx[i+1]])
    assert got==(expected[i],0),(name,got)
    print('PASS raw section',name,*got)
assert counts(log)==(686,0)
print('PASS raw dynmap total 686/0')
for i,want in enumerate([0,2,2,1]):
    text=read(f'wiring/m{i}-run.log')
    assert counts(text)==(686,want),(i,counts(text))
    failed=re.findall(r'^.*\[FAIL\].*$',text,re.M)
    assert all('[762-DP]' in l for l in failed)
    if i in (1,2):
        assert any('2 stopped gap' in l for l in failed)
        assert any('3 stopped silence' in l for l in failed)
    if i==3: assert '4 started gap' in failed[0]
    print('PASS raw wiring',i,'686 checks',want,'failures confined to named counter assertions')
v=read('campaign/campaign-d26fca65.verdicts.txt')
assert v.count('[PASS] mutant caught:')==63
assert '68 checks: 68 PASS, 0 FAIL' in v and 'CAMPAIGN rc=0' in v
rows=[l for l in (repo/'tb/verilator/milan_dp/README.md').read_text().splitlines() if re.match(r'\| \d+ \|',l)]
table=[]
for l in rows:
    cells=[c.strip() for c in l.strip('|').split('|')]
    if len(cells)==5 and re.fullmatch(r'\d+ of \d+',cells[-1]):
        table.append((int(cells[0]), tuple(map(int,cells[-1].split(' of ')))))
measured=[tuple(map(int,m)) for m in re.findall(r'its tallies report (\d+) failure\(s\) across (\d+) checks',v)]
assert len(table)==len(measured)==63,(len(table),len(measured))
assert [n for n,_ in table]==list(range(1,64))
assert [x for _,x in table]==measured
print('PASS all 63 README failure/total pairs match campaign receipt; five clean legs plus 63 caught controls')
for name,n in [('docs',95),('builder',2)]:
    lines=read(name+'/rc.tsv').splitlines()
    assert len(lines)==n and all(l.split('\t')[1]=='0' for l in lines)
    print('PASS',name,n,'zero exit receipts')
total_suites=total_checks=0
for i in range(4):
    s=read(f'sweep/shard-{i}.log')
    suites,passed,failed,timed=map(int,re.findall(r'suites: (\d+)\s+passed: (\d+)\s+failed: (\d+)\s+timed out: (\d+)',s)[-1])
    checks,failures=map(int,re.findall(r'checks: (\d+)\s+in-suite failures: (\d+)',s)[-1])
    assert suites==passed and failed==timed==failures==0
    assert f'SHARD {i}/4 rc=0' in s
    total_suites+=suites; total_checks+=checks
    print('PASS sweep shard',i,suites,'suites',checks,'checks')
assert (total_suites,total_checks)==(63,2188446)
print('PASS author sweep 63 suites, 2188446 checks; declared field skips do not prove hardware')
print('These are audits of published execution evidence, not new simulation or bank executions.')
