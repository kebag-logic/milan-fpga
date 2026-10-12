#!/usr/bin/env python3
"""Re-derive every table entry independently. Usage: measurements.py CHECKOUT PACKET."""
import ast
import csv
from datetime import datetime
from decimal import Decimal, ROUND_CEILING
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
out = packet/'receipts'
dev = out/'calibration-dev'
dev.mkdir(exist_ok=True)
repo = 'kebag-logic/milan-fpga'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet/'scratch'))
for path in (packet/'scratch').glob('tmp.*/*.log'):
    shutil.copyfile(path, dev/path.name)
metadata=packet/'scratch/dev-run.json'
if not metadata.exists():
    metadata.write_bytes(subprocess.check_output(['gh','run','view','38217650945','-R',repo,'--json','jobs,headSha,status,conclusion'],env=env,timeout=180))
jobs = json.loads(metadata.read_text())
for job in jobs['jobs']:
    if job['name'].startswith('Verilator shard') and not (dev/(str(job['databaseId'])+'.log')).exists():
        (dev/(str(job['databaseId'])+'.log')).write_bytes(subprocess.check_output(['gh','run','view','38217650945','-R',repo,'--job',str(job['databaseId']),'--log'],env=env,timeout=180))
assert len(list(dev.glob('*.log'))) == 5
maap = out/'calibration-maap.log'
with maap.open('w') as f:
    r = subprocess.run(['gh','run','view','38208503834','-R',repo,'--job','114677344710','--log'], stdout=f, stderr=subprocess.PIPE, text=True, env=env, timeout=180)
assert r.returncode == 0, r.stderr
(out/'calibration-maap.rc').write_text(str(r.returncode)+'\n')

def ceil(x):
    return int(x.to_integral_value(rounding=ROUND_CEILING))

def parse(path):
    rows=[]
    for line in path.read_text().splitlines():
        parts=line.split('\t',2)
        if len(parts)!=3:
            continue
        match=re.match(r'\ufeff?(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(\.\d+)?Z (.*)',parts[2])
        if match:
            stamp=datetime.fromisoformat(match[1])
            epoch=(stamp-datetime(1970,1,1)).total_seconds()
            rows.append((Decimal(int(epoch))+Decimal(match[2] or '0'),match[3],match[1]+(match[2] or '')+'Z'))
    start=next(i for i,(_,msg,_) in enumerate(rows) if re.fullmatch(r'shard: \d+/\d+ +selected suites: \d+',msg))
    _,worker,total,count=map(int,re.findall(r'\d+', '0 '+rows[start][1]))
    previous,_,previous_stamp=rows[start]
    measured=[]
    summary=False
    for stamp,msg,stamp_text in rows[start+1:]:
        if msg.startswith('suites: '):
            summary=True
            break
        match=re.fullmatch(r'(PASS|FAIL|TIMEOUT) +(\S+).*',msg)
        if match:
            assert match[1]=='PASS'
            measured.append({'suite':match[2],'start':previous_stamp,'end':stamp_text,'seconds_exact':str(stamp-previous),'seconds_ceil':ceil(stamp-previous),'worker':worker,'log':str(path.relative_to(packet))})
            previous=stamp
            previous_stamp=stamp_text
    if summary:
        assert len(measured)==count
    setup=rows[start][0]-rows[0][0]
    tail=rows[-1][0]-previous
    overhead={'worker':worker,'setup_exact':str(setup),'tail_exact':str(tail),'overhead_ceil':ceil(setup+tail) if summary else None,'complete':summary,'job_span_exact':str(rows[-1][0]-rows[0][0])}
    return measured,overhead

tables={}
for n in ast.parse((root/'scripts/suite_shards.py').read_text()).body:
    if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('SUITE_SECONDS','WORKER_OVERHEAD_SECONDS'):
        tables[n.targets[0].id]=ast.literal_eval(n.value)
rows=[]
overheads=[]
for path in sorted(dev.glob('*.log')):
    measured,overhead=parse(path)
    rows.extend(measured)
    overheads.append(overhead)
assert len(rows)==62
maap_rows,partial=parse(maap)
replacement=next(row for row in maap_rows if row['suite']=='maap')
rows=[row for row in rows if row['suite']!='maap']+[replacement]
assert {row['suite']:row['seconds_ceil'] for row in rows}==tables['SUITE_SECONDS']
assert tuple(v['overhead_ceil'] for v in sorted(overheads,key=lambda v:v['worker']))==tables['WORKER_OVERHEAD_SECONDS']
for name, data in [('suite-measurements',sorted(rows,key=lambda row:row['suite'])),('overhead-measurements',sorted(overheads,key=lambda row:row['worker']))]:
    with (out/(name+'.csv')).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]))
        w.writeheader();w.writerows(data)
for name,paths in [('dev',sorted(dev.glob('*.log'))),('maap',[maap])]:
    r=subprocess.run(['python3','scripts/suite_shards.py','--measure',*map(str,paths)],cwd=root,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30)
    (out/f'measure-{name}.log').write_text(r.stdout)
    (out/f'measure-{name}.rc').write_text(str(r.returncode)+'\n')
    assert r.returncode==0
    tree=ast.parse('\n'.join(line for line in r.stdout.splitlines() if not line.startswith('#')))
    result={n.targets[0].id:ast.literal_eval(n.value) for n in tree.body}
    expected={row['suite']:row['seconds_ceil'] for row in (parse(maap)[0] if name=='maap' else [x for p in dev.glob('*.log') for x in parse(p)[0]])}
    assert result['SUITE_SECONDS']==expected
    if name=='dev':
        assert result['WORKER_OVERHEAD_SECONDS']==tables['WORKER_OVERHEAD_SECONDS']
summary={'all_62_durations_match':True,'all_5_overheads_match':True,'maap':replacement,'partial_maap_log':partial,'dev_head':jobs['headSha'],'dev_jobs':[{'id':j['databaseId'],'name':j['name'],'conclusion':j['conclusion'],'start':j['startedAt'],'end':j['completedAt']} for j in jobs['jobs'] if j['name'].startswith('Verilator shard')],'method':'Independent Decimal differences between logged completion lines, first window begins at shard marker; ceil each duration; setup plus tail rounded together.'}
(out/'measurement-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print('PASS: every one of 62 durations and five overheads matches independently measured hosted logs; --measure agrees; maap is '+replacement['seconds_exact']+' s, rounded to '+str(replacement['seconds_ceil'])+' s.')
