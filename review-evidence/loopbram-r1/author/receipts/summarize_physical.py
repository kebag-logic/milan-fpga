import json,re,hashlib
from pathlib import Path
s=Path('$SCRATCH')
def util(p):
 text=p.read_text();ans={}
 for k in ['Slice LUTs*','Slice Registers','Block RAM Tile','RAMB36/FIFO*','RAMB18']:
  m=re.search(r'^\| +'+re.escape(k.rstrip('*'))+r'\*? +\| +([0-9.]+) +\|',text,re.M)
  if not m:raise ValueError((p,k))
  ans[k]=float(m.group(1))
 m=re.search(r'^\| +Slice +\| +([0-9.]+) +\|',text,re.M)
 if m:ans['Occupied slices']=float(m[1])
 return ans
def timing(p):
 text=p.read_text();m=re.search(r'WNS\(ns\).*?\n[^\n]*\n\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(\d+)\s+(\d+)\s+(-?\d+\.\d+)',text,re.S)
 if not m:raise ValueError(p)
 values=text[m.start():].splitlines()[2].split()
 return {'WNS_ns':float(m[1]),'TNS_ns':float(m[2]),'WHS_ns':float(m[5]),'setup_failing_endpoints':int(values[2]),'hold_failing_endpoints':int(values[6]),'WPWS_ns':float(values[8]),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
leaf={}
for p in sorted((s/'leaf-capture').glob('*/leaf_util.rpt')):leaf[p.parent.name]=util(p)
if set(leaf)=={'off','mapped','legacy'}:
 q=json.loads((s/'leaf-queue-summary.json').read_text())
 leaf['mapped_delta']={k:leaf['mapped'][k]-leaf['off'][k] for k in leaf['off']}
 leaf['legacy_delta']={k:leaf['legacy'][k]-leaf['off'][k] for k in leaf['off']}
 leaf['new_total_delta']={k:leaf['mapped_delta'][k]+q['delta'][k] for k in q['delta']}
(s/'leaf-capture-summary.json').write_text(json.dumps(leaf,indent=2)+'\n')
rows=[]
for gate in sorted((s/'route').glob('*/gateware')):
 for directive in ['ExtraPostPlacementOpt','AltSpreadLogic_high','ExtraTimingOpt']:
  d=gate/directive;row={'shape':gate.parent.name,'directive':directive}
  if (d/'measure_route.json').exists():row['run']=json.loads((d/'measure_route.json').read_text())
  if (d/'routed_util.rpt').exists():row['utilization']=util(d/'routed_util.rpt')
  row['corners']={p.name:timing(p) for p in sorted(d.glob('*signoff*_*C_timing.rpt'))}
  status=d/'alinx_ax7101_route_status.rpt'
  if status.exists():
   m=re.search(r'nets with routing errors[^:]*:\s*(\d+)',status.read_text());assert m
   row['routing_errors']=int(m[1])
  row['complete']=len(row['corners'])==4 and 'utilization' in row
  if row['complete']:
   row['min_WNS_ns']=min(c['WNS_ns'] for c in row['corners'].values());row['min_WHS_ns']=min(c['WHS_ns'] for c in row['corners'].values())
   row['floor_pass']=row['min_WNS_ns']>=.030 and row['min_WHS_ns']>=0 and row.get('run',{}).get('exit')==0 and row.get('routing_errors')==0 and all(c['setup_failing_endpoints']==0 and c['hold_failing_endpoints']==0 for c in row['corners'].values())
  rows.append(row)
(s/'route-summary.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Capture leaf:',leaf.get('new_total_delta','pending'))
for row in rows:
 if row['complete']:print(row['shape'],row['directive'],row['min_WNS_ns'],row['min_WHS_ns'],row['utilization'])
print('Routes complete:',sum(row['complete'] for row in rows),'/ 6')
