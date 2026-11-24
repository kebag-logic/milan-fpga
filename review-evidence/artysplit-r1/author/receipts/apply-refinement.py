"""Apply the measured SRP margin correction after closing all 295 us traces."""
import hashlib,json,subprocess,sys
from pathlib import Path
root=Path.cwd();old=Path('$VALIDATION_STORAGE/artysplit-a829/r4');out=old/'refined'
closure=json.loads((old/'calibration-295-input-closure.json').read_text())
assert closure['status']=='PASS'
a=json.loads((old/'model-preliminary-complete.json').read_text())
b=json.loads((old/'model-through-295.json').read_text())
changes={key:dict(old=a['costs'].get(key),new=value) for key,value in b['costs'].items() if a['costs'].get(key)!=value}
assert set(changes)<= {'record.srp','item.retained','item.record'},changes
assert b['costs']['record.srp']==300 and b['retry_us']==a['retry_us']
chosen=b['choices'][0]
assert (chosen['slice_us'],chosen['pace_ms'],chosen['queued_ms'])==(950,9,125)
assert not chosen['owner_findings']
before={};after={}
def write(name,transform):
 p=root/name;s=p.read_text();before[name]=hashlib.sha256(p.read_bytes()).hexdigest()
 text=transform(s);assert text!=s,name;p.write_text(text)
 after[name]=hashlib.sha256(p.read_bytes()).hexdigest()
def header(s):
 start=s.index('#elif CTRL_LOOP_SHAPE(1u, 1u, 2u)');end=s.index('#else',start)
 own=s[start:end];assert own.count('#define CTRL_LOOP_SRP_UNIT_US 295u')==1
 return s[:start]+own.replace('#define CTRL_LOOP_SRP_UNIT_US 295u','#define CTRL_LOOP_SRP_UNIT_US 300u')+s[end:]
write('sw/firmware/ctrl/loop/ctrl_loop.h',header)
def poll(s):
 lines=s.splitlines(keepends=True);hits=0
 for i,line in enumerate(lines):
  if line.startswith('STATED_US[shape_costs.Shape(1, 1, 2)] = '):
   assert line.count("'retained': 295")==1;lines[i]=line.replace("'retained': 295","'retained': 300");hits+=1
 assert hits==1;return ''.join(lines)
write('tb/verilator/ctrl_service_budget/poll_grade.py',poll)
def load(s):
 lines=s.splitlines(keepends=True);hits=0
 for i,line in enumerate(lines):
  if line.startswith("    'arty-1x1': {'record.srp':"):
   assert line.count("'record.srp': 295")==line.count("'item.retained': 295")==1
   lines[i]=line.replace("'record.srp': 295","'record.srp': 300").replace("'item.retained': 295","'item.retained': 300");hits+=1
 assert hits==2;return ''.join(lines)
write('tb/verilator/ctrl_service_budget/load_grade.py',load)
traces=json.loads((old/'calibration-295-traces.json').read_text())
worst=max(134507,max(row['worst_pass_cycles'] for row in traces))
def docs(s):
 before,section=s.split('## 15. Arty split at 80 MHz\n',1)
 section=section.replace('| SRP record | 295 |','| SRP record | 300 |')
 section=section.replace('Its initial 80 MHz calibration gives the following statements; fresh images',
                         'Its 80 MHz calibration gives the following statements; fresh images')
 section=section.replace('load 0.4916654474',f"load {b['load']:.10f}")
 section=section.replace('121.20 ms',f"{chosen['rows_ms']['last']:.2f} ms")
 section=section.replace('The observed maximum whole pass in the initial calibration is 134507 cycles,\nor 1.6813375 ms at 80 MHz.',
                         f'The observed maximum whole pass in the calibration is {worst} cycles,\nor {worst/80000:.7f} ms at 80 MHz.')
 return before+'## 15. Arty split at 80 MHz\n'+section
write('docs/design/SPLIT_CONTROL_MEMORY.md',docs)
(out/'census-preliminary-complete.json').write_bytes((old/'census-through-295.json').read_bytes())
(out/'model-calibration.json').write_bytes((old/'model-through-295.json').read_bytes())
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import arty_grade,build
model,findings=arty_grade.inspect(root);assert not findings,findings
assert abs(model['load']-b['load'])<=1e-12
assert all(abs(model['rows_ms'][key]-value)<=1e-12 for key,value in chosen['rows_ms'].items())
subprocess.run([sys.executable,'-B',str(out/'check-old-rows.py')],check=True,cwd=root)
record=dict(status='APPLIED; FRESH QUALIFICATION REQUIRED',changes=changes,before=before,after=after,
            firmware_tree=build.tree_digest([root/p for p in build.FIRMWARE_TREES]),
            model=model,calibration=str(old/'calibration-295-input-closure.json'))
(out/'refinement.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2),flush=True)
