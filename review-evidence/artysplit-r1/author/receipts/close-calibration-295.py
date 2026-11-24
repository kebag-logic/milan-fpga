"""Attest and grade every completed 295 us calibration trace before changing sources."""
import hashlib,json,subprocess,sys
from pathlib import Path
root=Path.cwd();r=Path('$VALIDATION_STORAGE/artysplit-a829/r4');out=r/'final-census'
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import build,egress_ledger,run,scenario
drain=json.loads((r/'calibration-drain.json').read_text())
assert drain['status'].startswith('NATIVE DRAIN COMPLETE')
assert all(child['returncode']==0 for child in drain['children'])
manifest=json.loads((out/'manifest.json').read_text())
records=[];inputs=[];results=[];failures=[]
for variant in manifest['groups']:
 directory=out/variant;spec=build.reused(directory)
 inputs.append(dict(variant=variant,build_sha256=hashlib.sha256((directory/'build.json').read_bytes()).hexdigest(),
                    executable_sha256=spec['executable_sha256'],firmware_tree=spec['inputs']['tree:firmware']))
 groups={g.name:g for g in run.all_groups(scenario.point('arty-1x1',spec),spec)}
 found=[]
 for status in sorted((directory/'results').glob('*.status')):
  name=status.stem;assert name in manifest['groups'][variant]
  code=int(status.read_text());log=status.with_suffix('.log');assert code==0,(name,code)
  graded,refusals,misses=run.graded([groups[name]],[log],spec,directory/'results')
  shares=run.share_misses(graded)
  late=run.save_misses(graded)+run.burst_misses(graded)+run.notice_misses(graded,1)
  forbidden=[]
  for result in graded:
   joins=result['passes'].get('joins',{})
   late += [f"{name}: join interval {row['ms']} ms outside protocol range" for row in joins.get('over',[])]
   late += [run.run_out_miss(name,row) for row in joins.get('failing',[])]
   late += [run.leave_all_miss(name,row) for row in joins.get('leave_all',{}).get('failing',[])]
   for probe in result['probes']:
    if probe.get('within_budget',True):continue
    entry={**probe,'group':name,'exact':True};ledger=egress_ledger.LEDGER['arty-1x1']
    if not egress_ledger.is_row(entry,ledger) or egress_ledger.over(entry,ledger[probe['probe']]):forbidden.append(probe)
  record=dict(variant=variant,group=name,native_status=code,
              trace_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),refusals=refusals,misses=misses,
              share=shares,late=late,forbidden=forbidden,stated=run.stated_misses(graded),
              worst_pass_cycles=max(x['passes']['worst']['cycles'] for x in graded))
  records.append(record);found.append(name)
  if refusals or shares or late or forbidden:failures.append(record)
  print('CALIBRATION',variant,name,'PASS' if not(refusals or shares or late or forbidden) else 'FAIL',flush=True)
  (r/'calibration-295-traces.json').write_text(json.dumps(records,indent=2)+'\n')
 if found:results.append(str(directory/'results'))
closure=dict(status='PASS' if not failures else 'FAIL',kind='Completed calibration traces; not a full point qualification',
             inputs=inputs,groups=len(records),findings=failures,
             note='Admission was closed after the 5 percent SRP rule grew from 295 to 300 us. All started native traces finished.')
(r/'calibration-295-input-closure.json').write_text(json.dumps(closure,indent=2)+'\n')
assert not failures,failures
def command(name,args):
 with (r/(name+'.log')).open('w') as log:
  subprocess.run([sys.executable,'-B',*args],cwd=root,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=28800)
 print(name,'PASS',flush=True)
command('census-calibration-295',[str(r/'census.py'),str(r/'census-calibration-295.json'),*results])
command('merge-calibration-295',[str(r/'merge-census.py'),str(r/'census-through-295.json'),
                              str(r/'census-preliminary-complete.json'),str(r/'census-calibration-295.json')])
command('derive-calibration-295',[str(r/'derive-own.py'),str(r/'census-through-295.json')])
model=json.loads((r/'derive-calibration-295.log').read_text())
(r/'model-through-295.json').write_text(json.dumps(model,indent=2)+'\n')
assert model['choices'],'OWNER: the completed calibration has no qualified choice'
print('CALIBRATION CLOSED; APPLY THE MEASURED COST CORRECTION BEFORE FRESH QUALIFICATION',flush=True)
