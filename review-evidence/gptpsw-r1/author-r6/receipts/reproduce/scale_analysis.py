#!/usr/bin/env python3
"""Read completed two-hart scale observations; preserve refused grades and label every borrowed cost."""
from pathlib import Path
import collections, copy, hashlib, json, math, sys
ROOT=Path('/data-2/milan/lanes/opt-hart2')
sys.path.insert(0,str(ROOT/'tb/verilator/ctrl_service_budget'))
import harts_load, load_grade, shape_costs, run, scale_guard, scenario
BUILD=Path(sys.argv[1]); POINT=sys.argv[2]+'/2if'; OUT=Path(sys.argv[3])
spec=json.loads((BUILD/'build.json').read_text())
clock=spec['cpu_hz']; limit=clock*2//1000
spans=[{},{}]; group_rows=[]; elapsed_cycles=0
def note(h,label,count,total,maximum,unfinished,where):
 row=spans[h].setdefault(label,dict(count=0,sum=0,maximum=0,unfinished=0,where=''))
 row['count']+=count; row['sum']+=total; row['unfinished']+=unfinished
 if maximum>row['maximum']:row.update(maximum=maximum,where=where)
for path in sorted((BUILD/'results').glob('*.log')):
 text=path.read_text(errors='replace')
 completed='RESULT: PASS' in text[-8000:]
 if not completed:
  group_rows.append(dict(group=path.stem,completed=False));continue
 scale_guard.require_harts(text,spec)
 passes=[dict(work=0,idle=0,worst=0,work_over=0,idle_runs_over=0) for _ in range(2)]
 for line in text.splitlines():
  f=line.split()
  if not f:continue
  if f[0]=='SUMMARY':
   totals=dict(kv.split('=',1) for kv in f[1:]);elapsed_cycles+=int(totals['cpu'])
  if f[0] in ('PASS','H1PASS'):
   h=int(f[0]=='H1PASS'); c=int(f[3] if h else f[4]);p=passes[h]
   p['work']+=1;p['worst']=max(p['worst'],c);p['work_over']+=c>limit
  elif f[0] in ('IDLE','H1IDLE'):
   h=int(f[0]=='H1IDLE');p=passes[h];p['idle']+=int(f[1]);p['worst']=max(p['worst'],int(f[3]));p['idle_runs_over']+=int(f[3])>limit
  elif f[0]=='SPAN':note(0,f[5],1,int(f[3]),int(f[3]),0,path.stem)
  elif f[0]=='H1COST':note(1,f[5],int(f[1]),int(f[2]),int(f[3]),int(f[4]),path.stem)
 gradepath=path.with_suffix('.json');graded=json.loads(gradepath.read_text()) if gradepath.exists() else None
 group_rows.append(dict(group=path.stem,completed=True,harts=passes,graded=graded is not None,
                        sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
# Use the accepted long-window equations, preserving their rates. These local registrations do not change
# any repository cost statement or gate. 64 sources and sinks have 132 counter-bearing descriptors.
point_shape=scenario.point(POINT.split('/')[0],spec)
aem=shape_costs.descriptors(Path(spec['elf']).with_name('srp_entity_gen.h').read_text())
model_counts=dict(n_if=2,sinks_per_if=math.ceil(point_shape.sinks/2),registrations=16,
                  counter_descriptors=sum(aem.values()))
load_grade.POINTS[POINT]=model_counts
shape_costs.BUILT.update({'32x32/2if':run.POINTS['32x32'],'64x64/2if':run.POINTS['64x64']})
costs=copy.deepcopy(load_grade.GRADED['32x32/2if'])
provenance={k:dict(kind='unmeasured transfer',source='historical one-hart 32x32 GRADED table',us=v) for k,v in costs.items()}
def use(key,h,label,proxy=False):
 r=spans[h].get(label)
 if not r or not r['count']:return
 v=math.ceil(r['maximum']*1e6/clock*1.05/5-1e-9)*5
 costs[key]=v
 provenance[key]=dict(kind='measured conservative proxy' if proxy else 'measured',hart=h,function=label,
                       maximum_cycles=r['maximum'],count=r['count'],unfinished=r['unfinished'],where=r['where'],us=v)
for ch,label in [('aecp','aecp_mbx:frame'),('acmp','acmp_mbx:on_frame'),('adp','acmp_mbx:on_adp_frame'),('maap','maap_mbx:receive')]:use('record.'+ch,1,label)
use('record.srp',0,'srp_mbx:receive')
# The normal apply_receive span does not stage the retained retry; retain its historical cost.
for key,label in [('item.reclaim','mrp_reclaim'),('item.walk','mrp_attr_visit')]:use(key,0,label)
# Inclusive polls are conservative proxies: they include non-send work and no selection by output kind.
use('item.acmp',1,'acmp_mbx:on_poll',True)
use('item.aecp.response',1,'aecp:transmit',True)
# A transmit sample is not evidence that a notice build or a registration probe was staged.
# Keep those two costs explicitly transferred; do not substitute the response sample.
for family,label in [('ADP','adp_mbx:on_event'),('ACMP','acmp_mbx:on_event'),('AECP','aecp_mbx:event'),('MAAP','maap_mbx:event')]:use('event.'+family,1,label,True)
# Measured whole-pass build costs are available even when the group's row grade fails.
for path in (BUILD/'results').glob('*.json'):
 if path.name=='results.json':continue
 g=json.loads(path.read_text())
 for key,kind in [('build','build'),('build_one','build-one')]:
  c=g.get('passes',{}).get('stated',{}).get('heaviest',{}).get(kind,0)
  if c and (provenance[key]['kind'].startswith('unmeasured') or c>provenance[key].get('maximum_cycles',0)):
   costs[key]=math.ceil(c*1e6/clock*1.05/5-1e-9)*5
   provenance[key]=dict(kind='measured',hart=0,maximum_cycles=c,where=g['group'],us=costs[key])
# The owed MRPDU send is not equivalent to building one, so it retains its explicitly unmeasured fallback.
# Charge each centisecond consumer separately, leaving the event dispatch overhead transferred and named.
tick_cost=[]
for h in (0,1):
 r=spans[h].get('ctrl_loop:dispatch_ticks')
 tick_cost.append(math.ceil(r['maximum']*1e6/clock*1.05/5-1e-9)*5 if r and r['count'] else None)
terms=harts_load.harts(ROOT,POINT,{POINT:costs},gptp_hart=None)
k=load_grade.contract(ROOT)
for h,c in enumerate(tick_cost):
 if c is not None:terms[h]['ticks']=(costs['event.TICK']+c)/k['tick_ms']/1000
charges=[]
for gh in (0,1):
 charged=copy.deepcopy(terms);charged[gh]['gptp']=harts_load.GPTP_SHARE
 charges.append(dict(gptp_hart=gh,loads=[sum(h.values()) for h in charged],terms=charged))
result=dict(point=POINT,model_counts=model_counts,geometry=spec['hart1_geometry'],clock_hz=clock,share_cycles=limit,groups=group_rows,
 costs=costs,provenance=provenance,centisecond_by_hart_us=tick_cost,charge_cases=charges,
 top_terms=[sorted(h.items(),key=lambda kv:-kv[1]) for h in terms],spans=spans,
 observed_elapsed_cycles=elapsed_cycles,
 inclusive_function_fractions=[sorted([(name,r['sum']/elapsed_cycles if elapsed_cycles else 0)
                                      for name,r in h.items() if r['count']],key=lambda kv:-kv[1]) for h in spans],
 unmeasured=[k for k,p in provenance.items() if p['kind'].startswith('unmeasured')],
 external_terms={'send.* / take.*':'6.4 us from historical 1x1 cross-hart record; not remeasured at scale',
 'hart0.steps':'PHY 155 us per 125 ms, not staged at scale',
 'gptp':'0.0042 per hart for both ports, transferred from gPTP lane; not staged by Arm A',
 'ticks':'event.TICK overhead transferred; each hart dispatch_ticks maximum measured where nonzero',
 'notices':'cold-round and notice costs from shape header; item.aecp.notice and item.aecp.probe remain historical transfers because their costs are not separately staged; long notice/declaring arms not staged',
 'background':'empty-pass base is not a long-window term in the inherited equations; report is demand model, not CPU occupancy',
 'stream counts':'derived from the generated shape; worst sinks/interface rounded up (17 for the 33-slot 32x32 image)',
 'unfinished calls':'only completed entry-to-return calls contribute maxima; tail calls and unfinished calls are not complete samples. Counts are retained; this is sampled cost evidence, not a proof of WCET',
 '16-value cap':'full-declaring chunk counts per JoinTime, and their build, reclaim, walk, owed-send and NOTICED rates, are not validated by these nondeclaring Arm A groups; inherited rates are retained explicitly',
 'retained SRP retry':'item.retained remains historical: normal apply_receive samples do not stage the refusal, pool-release and retry scheduling paths',
 'inclusive overlap':'sampled handlers and polls can already include cross-hart sends or redelivery; separate historical record charges are retained and can conservatively double-count that work, with no overlap deduction',
 'cross-hart retries':'queue-full retries beyond one send/take per admitted record are not separately measured or modeled',
 'bus and cache interaction':'handler samples include their observed waits; unstaged combinations and empty-loop overhead are not separately bounded',
 'bitmap scans':'MRP walk is observed; ACMP bitmap scan inside handlers is not separately attributed',
 'scope':'Arm A nine groups only; saved-state, PHY and live-Talker declarations are not measured here'})
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('point','geometry','charge_cases','unmeasured')},indent=2))
