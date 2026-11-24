"""Close every completed frozen input before calibration resumes."""
import datetime,hashlib,json,subprocess,sys
from pathlib import Path
root=Path.cwd();r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/refined');out=r/'final-census'
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import build
manifest=json.loads((out/'manifest.json').read_text())
assert manifest['status']=='CALIBRATION COMPLETE; FIRMWARE COST ADJUSTMENT REQUIRED'
rows=json.loads((out/'completed.json').read_text())
assert len(rows)==manifest['completed']
assert not (out/'stop-finding.json').exists()
expected=json.loads((r/'refinement.json').read_text())['firmware_tree']
assert build.tree_digest([root/p for p in build.FIRMWARE_TREES])==expected
specs={variant:build.reused(out/variant) for variant in manifest['groups']}
for row in rows:
 assert row['native_status']==0 and not any(row[k] for k in ('refusals','share','late','forbidden'))
 path=out/row['variant']/'results'/(row['group']+'.log')
 assert hashlib.sha256(path.read_bytes()).hexdigest()==row['trace_sha256']
 assert path.with_suffix('.status').read_text().strip()=='0'
assert len({(x['variant'],x['group']) for x in rows})==len(rows)
assert {(v,p.stem) for v in specs for p in (out/v/'results').glob('*.log')}=={
 (x['variant'],x['group']) for x in rows}
commands=[]
def command(name,argv):
 log=r/(name+'.log')
 with log.open('w') as stream:p=subprocess.run(argv,cwd=root,stdout=stream,stderr=subprocess.STDOUT,timeout=10800)
 commands.append(dict(command=argv,returncode=p.returncode,log=str(log)))
 assert p.returncode==0,name
command('calibration-before-continuation-census',[sys.executable,'-B',str(r/'census.py'),
 str(r/'calibration-before-continuation-census.json'),*[str(out/v/'results') for v in specs]])
command('calibration-base-merge',[sys.executable,'-B',str(r/'merge-census.py'),
 str(r/'calibration-base-census.json'),str(r/'census-preliminary-complete.json'),
 str(r/'calibration-before-continuation-census.json')])
command('calibration-base-model',[sys.executable,'-B',str(r/'derive-own.py'),str(r/'calibration-base-census.json')])
model=json.loads((r/'calibration-base-model.log').read_text())
(r/'calibration-base-model.json').write_text(json.dumps(model,indent=2)+'\n')
progress=r/'calibration-progress';progress.mkdir(exist_ok=True)
forecast=dict(status='PARTIAL CALIBRATION COST FORECAST',
 time=datetime.datetime.now(datetime.timezone.utc).isoformat(),completed_groups=len(rows),
 model=str(r/'calibration-base-model.json'),load=model['load'],choices=model['choices'],qualification=False)
(progress/'latest.json').write_text(json.dumps(forecast,indent=2)+'\n')
if not model['choices']:
 (progress/'owner-finding.json').write_text(json.dumps(forecast,indent=2)+'\n')
 raise SystemExit('OWNER: complete drained calibration has no choice satisfying the required bounds')
record=dict(status='INPUTS CLOSED FOR CALIBRATION CONTINUATION; NOT QUALIFIED',
 time=datetime.datetime.now(datetime.timezone.utc).isoformat(),firmware_tree=expected,
 groups=len(rows),commands=commands,
 builds={v:dict(executable_sha256=s['executable_sha256'],cpu_hz=s['cpu_hz']) for v,s in specs.items()},
 findings=[dict(variant=x['variant'],group=x['group'],stated=x['stated']) for x in rows if x['stated']],
 note='Preserved native and per-row results include the known under-stated build cost. No owner or unauthorized row failure is present.')
(r/'calibration-before-continuation-closure.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2),flush=True)
