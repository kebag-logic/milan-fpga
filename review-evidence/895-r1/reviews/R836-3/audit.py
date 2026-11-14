#!/usr/bin/env python3
"""Read-only source and public-receipt audit. Arguments: source, extracted packet."""
import ast
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys

root, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
sys.dont_write_bytecode = True
head = '62298ab5cbfeb7056e4567f70e69d578201c75e0'
def git(*args):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(root), *args])

assert git('rev-parse','HEAD').decode().strip() == head
manifest = json.loads((packet/'MANIFEST.json').read_text())
checked = 0
for row in manifest:
    if row['file'].split('/')[0] not in ('author-r2','author-r3','author-r3r','author-r4','author-r5'):
        continue
    assert hashlib.sha256((packet/row['file']).read_bytes()).hexdigest() == row['published_sha256'], row['file']
    checked += 1
print('Public manifest:',checked,'published SHA-256 hashes verified; no original/redacted hash substitution.')
print('Archive signature status:',git('log','-1','--format=%G?','689125c2').decode().strip(),'(N = unsigned).')
r = packet/'author-r5/receipts'
table = (r/'gates/verify-table.md').read_text().splitlines()
counts = {'executed':0,'not_run':0}
for line in table:
    if not line.startswith('| ') or line.startswith('| Workflow'):
        continue
    cells = [s.strip() for s in line.split('|')[1:-1]]
    if len(cells) != 6:
        continue
    if cells[4] == 'NOT RUN':
        assert cells[5]
        counts['not_run'] += 1
    else:
        assert cells[4] == '0', cells
        filename = cells[5].strip('`')
        log = r/'gates/workflows'/filename
        if log.exists():
            assert head in log.read_text().splitlines()[0],filename
        else:
            assert filename in (r/'gates/large.txt').read_text(),filename
        assert (r/'gates/workflows'/filename.replace('.log','.rc')).read_text().strip() == '0',filename
        counts['executed'] += 1
print('Workflow rows and rc files:',counts)
total_suites = total_checks = 0
suite_names=[]
for n in range(4):
    p=r/f'sweep/shard-{n}'
    for name in ('spec.json','results.json','complete.json'):
        doc=json.loads((p/name).read_text()); assert doc['head']==head
        if name=='results.json': assert all(x['exit_code']==0 for x in doc['results'])
        if name=='complete.json': assert doc['exit_code']==0
    text=(p/'01.log').read_text()
    suites,passed,failed,timed=map(int,re.search(r'suites: (\d+)\s+passed: (\d+)\s+failed: (\d+)\s+timed out: (\d+)',text).groups())
    checks,errors=map(int,re.search(r'checks: (\d+)\s+in-suite failures: (\d+)',text).groups())
    assert suites==passed and failed==timed==errors==0
    names=re.findall(r'^PASS\s+(\S+)\s*$',text,re.M)
    assert len(names)==suites
    suite_names+=names
    total_suites+=suites; total_checks+=checks
    print('Sweep shard',n,'suites',suites,'checks',checks,'exit 0; exact head.')
assert len(set(suite_names))==total_suites==65
print('Sweep total:',total_suites,'distinct suites;',total_checks,'checks; no in-suite failures.')
for arm in ('A1','A8','N1','N8','W1','W8','B1','B8'):
    for suffix in ('compare','cmp','sample','regrade'):
        assert (r/f'gates/harness/{arm}-{suffix}.rc').read_text().strip()=='0'
    assert 'RESULT PASS' in (r/f'gates/harness/{arm}-compare.txt').read_text()
    assert not (r/f'gates/harness/{arm}-tree-after.txt').read_text().strip()
print('Eight exact-head rebuild comparisons, sample comparisons, samples and regrades: rc 0; final trees clean.')
print('Executable hash rc=1 is disclosed; acceptance uses image bytes, generated logic and byte-identical sample logs.')

def plants(ref):
    p='sw/firmware/ctrl/test/srp_talker_mutants.py'
    namespace={};exec(compile(git('show',f'{ref}:{p}'),p,'exec'),namespace)
    return namespace['defects'](lambda *a,**k:(a,k))
a,b=plants('10cd5472^'),plants('10cd5472')
assert a==b and len(a)==34
print('10cd5472: all 34 plant tuples identical in order, payload, oracle, path, entity and suite.')
p='tb/verilator/ctrl_service_budget/build.py'
assert ast.dump(ast.parse(git('show',f'10cd5472^:{p}')))==ast.dump(ast.parse(git('show',f'10cd5472:{p}')))
print('10cd5472 build.py: identical Python AST.')
text=(r/'fw/plants-talker.log').read_text()
print('Published focused plant receipt:', '\n'.join(text.splitlines()[-4:]))

sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import load_grade as lg
import rows_tiers as rt
import paced_rows as pr
for point,tag in [('1x1/1if','1x1'),('8x8/2if','8x8')]:
    costs=lg.stated(root,point,lg.STATED_US)
    rows=[]
    source='1x1-without-largest-notice' if tag=='1x1' else tag
    for line in (r/f'costs/{source}/costs.txt').read_text().splitlines():
        m=re.match(r'\S+\s+(\S+)\s+most\s+([\d,]+) CPU cycles, stated\s+(\d+) us;',line)
        assert m,line
        name,cycles,margin=m.groups();cycles=int(cycles.replace(',',''))
        if name in costs and cycles:
            raw_us=cycles/100
            status='WITHIN' if costs[name]>=raw_us else 'KNOWN #902' if name=='record.aecp' and point=='1x1/1if' else 'UNDER'
            assert status!='UNDER',(point,name,raw_us,costs[name])
            rows.append((name,raw_us,costs[name],status))
    print('Measured ordinary-cost comparisons',point,json.dumps(rows))
    for table_name,t in [('pin',lg.STATED_US),('second column',lg.STATED_US_DONOR)]:
        terms=lg.load(root,point,t)
        print('Load terms',point,table_name,json.dumps(terms,sort_keys=True),'total',sum(terms.values()))
    i=rt.point_inputs(root,point)
    header=lg.macros(root,lg.POINTS[point]['n_if'])
    print('Hold-off from headers:',point,2000+header['SRP_JOIN_CS']+math.ceil(i.tx_stated/10),'cs')
i=rt.point_inputs(root,'1x1/1if')
for pace in range(1,12):
    at=i._replace(pace_ms=pace)
    print('Pace',pace,'txL',rt.solve('txL',at,rt.BUILT)[0],'R4L',rt.solve('R4L',at,rt.BUILT)[0])
assert pr.choice(root)==9 and rt.ruled(root)==900
print('Pace rule 9; slice rule 900; transmit statement findings:',rt.tx_statements(root))
for point,key,cycles,want in [('1x1/1if','event.AECP',6805,75),('1x1/1if','event.TICK',4385,50),
        ('8x8/2if','event.AECP',10824,115),('8x8/2if','event.TICK',4948,55),
        ('8x8/2if','events_none',2882,35),('8x8/2if','record.maap',14361,155)]:
    derived=math.ceil(cycles*1.05/100/5)*5
    assert derived==want==lg.STATED_US[point][key]
    assert lg.STATED_US_DONOR[point][key]>=want
    print('Restatement:',point,key,cycles,'cycles ->',want,'us; both columns cover measurement + 5%, rounded up to 5 us.')
print('AUDIT PASS')
