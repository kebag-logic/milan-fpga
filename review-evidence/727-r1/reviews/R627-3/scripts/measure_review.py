#!/usr/bin/env python3
"""Re-derive recorded figures from public hosted logs, independently and via --measure."""
import csv
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

root=Path(sys.argv[1]).resolve(); packet=Path(sys.argv[2]).resolve()
receipts=packet/'receipts'; hosted=receipts/'hosted'; hosted.mkdir(exist_ok=True)
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(packet/'scratch')}
refresh=(receipts/'refresh-verbatim.log').read_text()
logs=Path(re.search(r'REVIEW_LOG_DIRECTORY=(.+)',refresh).group(1))
for path in logs.glob('*.log'): shutil.copyfile(path,hosted/path.name)
maap=hosted/'114677344710.log'
with maap.open('wb') as out:
    result=subprocess.run(['gh','run','view','38208503834','-R','kebag-logic/milan-fpga',
                           '--job','114677344710','--log'],stdout=out,stderr=subprocess.PIPE,env=env,check=True)
spec=importlib.util.spec_from_file_location('selector',root/'scripts/suite_shards.py')
selector=importlib.util.module_from_spec(spec);spec.loader.exec_module(selector)

def measure(path):
    events=[]
    for line in path.read_text().splitlines():
        parts=line.split('\t',2)
        if len(parts)!=3: continue
        tail=parts[2].lstrip('\ufeff')
        stamp,sep,message=tail.partition(' ')
        if not sep or not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z',stamp): continue
        whole,_,fraction=stamp[:-1].partition('.')
        seconds=Decimal(int(datetime.strptime(whole,'%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc).timestamp()))
        if fraction: seconds+=Decimal('0.'+fraction)
        events.append((seconds,message,stamp))
    begin=next(i for i,(_,message,_) in enumerate(events) if re.fullmatch(r'shard: \d+/\d+ +selected suites: \d+',message))
    shard=re.search(r'shard: (\d+)/(\d+)',events[begin][1]);index=int(shard[1])
    previous=events[begin]; rows=[]; completed=False
    for event in events[begin+1:]:
        _,message,_=event
        if message.startswith('suites: '): completed=True; break
        match=re.fullmatch(r'(PASS|FAIL|TIMEOUT) +(\S+).*',message)
        if not match: continue
        assert match[1]=='PASS',message
        elapsed=event[0]-previous[0]
        assert elapsed>0
        rows.append({'suite':match[2],'job':path.stem,'worker':index,'start':previous[2],
            'end':event[2],'elapsed_seconds':str(elapsed),'ceil_seconds':int(elapsed.to_integral_value(rounding=ROUND_CEILING))})
        previous=event
    overhead=None
    if completed:
        value=events[begin][0]-events[0][0]+events[-1][0]-previous[0]
        overhead={'worker':index,'job':path.stem,'setup_seconds':str(events[begin][0]-events[0][0]),
            'tail_seconds':str(events[-1][0]-previous[0]),'elapsed_seconds':str(value),
            'ceil_seconds':int(value.to_integral_value(rounding=ROUND_CEILING))}
    return rows,overhead

rows=[]; overheads=[]
for path in sorted(hosted.glob('*.log')):
    measured,overhead=measure(path)
    if path==maap: rows.extend(x for x in measured if x['suite']=='maap')
    else:
        rows.extend(x for x in measured if x['suite']!='maap')
        overheads.append(overhead)
    parsed=selector.measure_log(path.read_text())
    assert {x['suite']:x['ceil_seconds'] for x in measured}==parsed.seconds
    assert (overhead['ceil_seconds'] if overhead else None)==parsed.overhead
assert {r['suite']:r['ceil_seconds'] for r in rows}==selector.SUITE_SECONDS
assert tuple(x['ceil_seconds'] for x in sorted(overheads,key=lambda x:x['worker']))==selector.WORKER_OVERHEAD_SECONDS
for name,data in [('suite-measurements',sorted(rows,key=lambda x:x['suite'])),('overhead-measurements',sorted(overheads,key=lambda x:x['worker']))]:
    with (receipts/(name+'.csv')).open('w') as out:
        writer=csv.DictWriter(out,fieldnames=data[0]);writer.writeheader();writer.writerows(data)
for name,paths in [('dev',[p for p in sorted(hosted.glob('*.log')) if p!=maap]),('maap',[maap])]:
    r=subprocess.run(['python3','scripts/suite_shards.py','--measure',*map(str,paths)],cwd=root,env=env,capture_output=True,check=True)
    (receipts/('measure-'+name+'.log')).write_bytes(r.stdout+r.stderr)
    (receipts/('measure-'+name+'.rc')).write_text('0\n')
summary={'suite_figures_checked':len(rows),'overhead_figures_checked':len(overheads),
         'all_committed_figures_match':True,'maap':next(x for x in rows if x['suite']=='maap'),
         'overheads':overheads,'dev_run':'38217650945','maap_run':'38208503834',
         'refresh_verbatim_rc':int((receipts/'refresh-verbatim.rc').read_text())}
(receipts/'measurement-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
