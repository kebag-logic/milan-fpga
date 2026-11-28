"""Apply the existing cost, slice, pace and queued-bound rules to only Arty 4x4 measurements (round 9's derive-own.py
at arty-4x4, shape (1,5,5)).
The output is a candidate model; complete trace qualification remains mandatory.
"""
import json, math, sys
from pathlib import Path
from unittest.mock import patch
root=Path.cwd()
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import arty_grade, edit_rows, load_grade, paced_rows, queued_bound
import rows_grade as rg, rows_tiers as rt, shape_costs as sc
point='arty-4x4'; shape=sc.Shape(1,5,5)
raw=json.loads(Path(sys.argv[1]).read_text())
assert raw['cpu_hz']==80_000_000 and raw['shape']==list(shape)
c={k:v['rule_us'] for k,v in raw['costs'].items()}
required=['base','build','build_one','step','centisecond','events_none','event.LINK','event.GM','event.TICK',
          'record.srp','record.aecp.other','record.aecp.long','record.aecp.paced','record.acmp','record.adp','record.maap',
          'tx.aecp.notice','tx.aecp.response',*('item.'+x for x in ('withdraw','rebuild','walk','reclaim','acmp','acmp_declined','aecp','aecp_long')),
          *('event.TIMER#'+str(x) for x in range(4)),*('event.'+x for x in rt.DATAPATH)]
missing=[k for k in required if c.get(k,0)<=0]
if missing:
 print(json.dumps(dict(status='UNQUALIFIED',missing_costs=missing),indent=2));raise SystemExit(2)
for slot,name in enumerate(('ADP','ACMP','MAAP','AECP')):c['event.'+name]=c['event.TIMER#'+str(slot)]
c.update({'record.aecp':c['record.aecp.other'],'item.retained':c['record.srp'],'item.mrpdu':c['build_one'],
          'item.aecp.long':c['item.aecp_long'],'item.aecp.notice':c['tx.aecp.notice'],
          'item.aecp.response':c['tx.aecp.response'],'item.aecp.probe':c.get('tx.aecp.probe',c['tx.aecp.response'])})
rounds={tuple(map(int,k.split(':'))):v['cycles'] for k,v in raw['rounds'].items()}
k=max(k for n,k in rounds if n==0)
if not k or not any(n for n,k in rounds):raise SystemExit('UNQUALIFIED: retry measurements incomplete')
full=rounds[(0,k)]
cold=max([rounds.get((0,0),0)]+[(cost*k-full*j)/(k-j) for (n,j),cost in rounds.items() if n==0 and j<k])
attempt=(full-cold)/k
notice=max((cost-cold-j*attempt)/n for (n,j),cost in rounds.items() if n)
rule=lambda cycles:math.ceil(cycles/80*1.05/5-1e-9)*5
cold_us,attempt_us,notice_us=map(rule,(cold,attempt,notice))
assert all(cost<=(cold_us+n*notice_us+k*attempt_us)*80 for (n,k),cost in rounds.items())
h=rg.header(root,shape)
h.update(CTRL_LOOP_STEP_PASS_US=c['step'],CTRL_LOOP_TICK_US=c['centisecond'],CTRL_LOOP_BUILD_PASS_US=c['build'],
         CTRL_LOOP_BUILD_ONE_PASS_US=c['build_one'],AECP_ROUND_COLD_US=cold_us,AECP_NOTICE_US=notice_us)
h['AECP_NOTICES_MOST']=sc.notices_most(root/'configs/endstation_arty_split_4x4.yaml',1,root)
s=dict(n_if=1,sources=5,sinks_per_if=5,registrations=16,counter_descriptors=12,notices=h['AECP_NOTICES_MOST'])
rate,tick=rg.contract(root)
built=rt.built_constants(root,point)
i=rt.Inputs(h,c,s,rate,tick,8,1300,built[1],built[2],built[3],built[4],9)
# Only the new named point is supplied. Existing points' costs never enter.
edit_rows.PACED[point]={'a one-row edit':max(c['paced.44'],c['paced.45']),
                        'an accepted SET_CONFIGURATION':c['paced.6']}
edit_rows.EDIT_RECORD_US[point]=max(edit_rows.PACED[point].values())
load_grade.POINTS[point]=s
load_grade.STATED_US[point]=c
load_h={**load_grade.macros(root,shape),**h}
with patch.object(load_grade,'macros',lambda *args:load_h):
 load_terms=load_grade.load(root,point,load_grade.STATED_US)
load=sum(load_terms.values())
choices=[];candidates=[]
for queued in (125,130,135,140):
 for pace in range(1,paced_rows.PACE_MOST_MS+1):
  base=i._replace(h={**h,'AECP_QUEUED_MS':queued},pace_ms=pace)
  with patch.object(rt,'point_inputs',lambda *args:base):sl,margin=rt.slice_choice(root,point)
  at=base._replace(slice_us=sl)
  with patch.object(rt,'point_inputs',lambda *args:at):taken=paced_rows.choice(root,point)
  rows={name:val for name,(val,_) in rt.rows(root,point,rt.BUILT,at).items()}
  findings=arty_grade.owner_findings(load,rows)
  record=dict(queued_ms=queued,pace_ms=pace,slice_us=sl,least_margin=margin,pace_rule=taken,
              queued_rule=queued_bound.ruled(rows['last']),rows_ms=rows,owner_findings=findings)
  candidates.append(record)
  if taken==pace and record['queued_rule']==queued and sl>=c['build_one'] and not findings:choices.append(record)
result=dict(status='CANDIDATE MODEL' if choices else 'NO QUALIFIED MODEL',cpu_hz=80_000_000,shape=list(shape),
            load=load,load_terms=load_terms,retry_raw_cycles=[cold,attempt,notice],retry_us=[cold_us,attempt_us,notice_us],
            costs=c,choices=sorted(choices,key=lambda x:(x['pace_ms'],x['queued_ms'],x['slice_us'])),candidates=candidates)
print(json.dumps(result,indent=2))
