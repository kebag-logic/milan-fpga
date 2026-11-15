#!/usr/bin/env python3
"""Read-only table and receipt probes. Usage: probe.py SOURCE EVIDENCE."""
import json
import math
from pathlib import Path
import re
import sys

src, ev = map(Path, sys.argv[1:])
sys.path.insert(0,str(src/'tb/verilator/ctrl_service_budget'))
import load_grade as lg
import poll_grade as pg
import rows_tiers as rt
import selftest_notice as sn

for point in ('1x1/1if','8x8/2if'):
    n = lg.POINTS[point]['n_if']
    h = lg.macros(src,n)
    h['CTRL_LOOP_TX_MS'] = rt.built_value((src/'sw/firmware/ctrl/loop/ctrl_loop.h').read_text(),'CTRL_LOOP_TX_MS',n,0)
    print('HEADERS',point,'join',h['SRP_JOIN_CS'],'tx',h['CTRL_LOOP_TX_MS'],
          'hold cs',2000+h['SRP_JOIN_CS']+(h['CTRL_LOOP_TX_MS']+9)//10)
    for name,table in lg.COLUMNS:
        terms=lg.load(src,point,table)
        print('LOAD',point,name,json.dumps(terms,sort_keys=True),'sum',sum(terms.values()))
    # Compare the parser measurements against all matching live cost tables.
    cp=ev/'author-r8/receipts/costs'/('1x1' if n==1 else '8x8')
    records={}
    for line in (cp/'costs.txt').read_text().splitlines():
        m=re.match(r'\S+\s+(\S+)\s+most\s+([\d,]+) CPU',line)
        if m:
            records[m[1]]=int(m[2].replace(',',''))
    for name,table in lg.COLUMNS:
        costs=lg.stated(src,point,table)
        for key,value in costs.items():
            alias={'item.aecp.notice':'item.aecp'}.get(key,key)
            cycles=records.get(alias)
            if cycles is None or key=='record.aecp':
                continue
            rule=math.ceil(cycles*1.05/500-1e-9)*5
            print('COST',point,name,key,cycles,rule,value,'OK' if value>=rule else 'UNDER')
    events=json.loads((cp/'events.json').read_text())
    for key,value in rt.DATAPATH_US[point].items():
        cycles=events[key]['most_cycles']
        rule=math.ceil(cycles*1.05/500-1e-9)*5
        print('DATAPATH',point,key,cycles,rule,value,'OK' if value>=rule else 'UNDER')

print('QUEUE CONTROLS',sn.queue_checks())
oldp=pg.STATED_US[1]['base']; oldl=lg.STATED_US_DONOR['1x1/1if']['base']
for own in (260,278,279):
    base=own-lg.STATED_US_DONOR['1x1/1if']['events_none']
    pg.STATED_US[1]['base']=base
    lg.STATED_US_DONOR['1x1/1if']['base']=base
    i=rt.point_inputs(src,'1x1/1if')
    bounds=rt.bounds_at(i)
    rows=rt.rows(src,'1x1/1if',rt.BUILT,i)
    print('HEADROOM',own,json.dumps({k:[v[0],bounds[k]] for k,v in rows.items()},sort_keys=True))
pg.STATED_US[1]['base']=oldp
lg.STATED_US_DONOR['1x1/1if']['base']=oldl

r=ev/'author-r9/receipts'
table=(r/'gates/verify-table.md').read_text()
print('WORKFLOW TABLE counts',sum('| PASS |' in l for l in table.splitlines()),sum('| NOT RUN |' in l for l in table.splitlines()))
print('WORKFLOW RC files',len(list((r/'gates/workflows').glob('*.rc'))),'nonzero',[(p.name,p.read_text().strip()) for p in (r/'gates/workflows').glob('*.rc') if p.read_text().strip()!='0'])
for x in range(4):
    s=r/f'sweep/shard-{x}'
    print('SWEEP',x,json.loads((s/'spec.json').read_text())['head'],(s/'complete.json').read_text().strip())
    log=(s/'01.log').read_text()
    print('\n'.join(l for l in log.splitlines() if re.search('suites,|failed|checks|PASS|SKIP',l))[-1800:])
print('RERUN', (r/'legs/R9-W8-vs-R8-W8.txt').read_text())
