#!/usr/bin/env python3
"""Replay the retained diagnostic evidence without builds or hardware access."""
import argparse, csv, json, pathlib, subprocess, sys
p=argparse.ArgumentParser()
p.add_argument('source',type=pathlib.Path)
p.add_argument('output',type=pathlib.Path)
a=p.parse_args();a.source=a.source.resolve();a.output=a.output.resolve();a.output.mkdir(parents=True,exist_ok=True)
packet=pathlib.Path(__file__).resolve().parents[1]
reader=a.source/'tb/verilator/follow_ring/trace_table.py'
results=[]
def run(name,argv):
    with (a.output/(name+'.log')).open('w') as f:
        rc=subprocess.run(argv,stdout=f,stderr=subprocess.STDOUT).returncode
    (a.output/(name+'.rc')).write_text(str(rc)+'\n')
    results.append(dict(name=name,argv=list(map(str,argv)),rc=rc))
    assert rc==0,(name,rc)
    print('PASS:',name,flush=True)
run('standing',[sys.executable,'-B',a.source/'tb/verilator/follow_ring/test_trace_table.py'])
run('public-decimal',[sys.executable,'-B',packet/'scripts/decimal_boundaries.py',a.source,a.output/'public-decimal'])
for name,origin,start,end,step,counts in [('pullin','4.6','.7','1.0','.1',(0,0,1)),('duplicate','0','1.25','1.75','.25',(1,0,0)),('skip','0','38.5','38.75','.25',(1,1,0))]:
    out=a.output/(name+'.csv')
    run(name,[sys.executable,'-B',reader,packet/'jobs'/('trace-'+name+'.log'),packet/'fresh-tables'/(name+'.pdu-window.csv'),packet/'traces'/(name+'.servo.csv'),'--origin-s',origin,'--from-s',start,'--to-s',end,'--step-s',step,'--csv',out])
    with out.open() as f: rows=list(csv.DictReader(f))
    with (packet/'fresh-tables'/(name+'.bounded.csv')).open() as f: expected=list(csv.DictReader(f))
    assert rows==expected,name
    assert tuple(sum(int(r[k]) for r in rows) for k in ('slips','skips','recentres'))==counts
legacy=packet/'review/receipts/public/reviews/R474-5/receipts/trace-table-probe-inputs'
run('unchanged-public-probe',[sys.executable,'-B',reader,legacy/'run.log',legacy/'pdu.csv',legacy/'servo.csv','--from-s','0','--to-s','1','--step-s','.25','--csv',a.output/'legacy.csv'])
with (a.output/'legacy.csv').open() as f: rows=list(csv.DictReader(f))
assert len(rows)==4 and rows[2]['ring_margin_ticks']=='+1.300..+5.300'
assert all(r['slips']=='0' and r['event_trace']=='unavailable' for r in rows)
(a.output/'results.json').write_text(json.dumps(results,indent=2)+'\n')
