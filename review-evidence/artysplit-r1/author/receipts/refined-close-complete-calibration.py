"""Close all 145 calibration traces before changing the frozen firmware.

The incremental census has already parsed every completed group. Preserve its
merged maximum and model, and independently close exact scripts, trace hashes,
executable inputs and native outcomes. This is never image qualification.
"""
import datetime,hashlib,json,shutil,sys
from pathlib import Path
root=Path.cwd();r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/refined');out=r/'final-census'
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import build,run,scenario
manifest=json.loads((out/'manifest.json').read_text())
assert manifest['status']=='CALIBRATION MEASUREMENTS COMPLETE; FIRMWARE CHANGES STILL REQUIRED'
commands=json.loads((r/'calibration-pipeline-results.json').read_text())
assert len(commands)==2 and not any(row['returncode'] for row in commands)
rows=json.loads((out/'completed.json').read_text())
expected={(v,g) for v,names in manifest['groups'].items() for g in names}
assert len(rows)==manifest['completed']==len(expected)==145
assert {(row['variant'],row['group']) for row in rows}==expected
assert not (out/'stop-finding.json').exists()
assert not (r/'calibration-progress/owner-finding.json').exists()
firmware_tree=build.tree_digest([root/p for p in build.FIRMWARE_TREES])
assert firmware_tree==json.loads((r/'refinement.json').read_text())['firmware_tree']
specs={};scripts={}
for variant,names in manifest['groups'].items():
 spec=build.reused(out/variant);specs[variant]=spec
 assert spec['cpu_hz']==spec['sys_hz']==80_000_000 and spec['measurement_pace_ms']==9
 assert spec['executable_sha256']==manifest['executables'][variant]
 for group in run.all_groups(scenario.point('arty-1x1',spec),spec):
  if group.name not in names:continue
  path=out/variant/'results'/(group.name+'.txt')
  assert path.read_text()==group.script(),path
  scripts[(variant,group.name)]=hashlib.sha256(path.read_bytes()).hexdigest()
assert set(scripts)==expected
for row in rows:
 assert row['native_status']==0 and not any(row[k] for k in ('refusals','share','late','forbidden'))
 path=out/row['variant']/'results'/(row['group']+'.log')
 with path.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
 assert digest==row['trace_sha256'],path
 assert path.with_suffix('.status').read_text().strip()=='0'
latest=json.loads((r/'calibration-progress/latest.json').read_text())
assert latest['completed_groups']==145 and not latest['qualification']
model_path=Path(latest['model']);model=json.loads(model_path.read_text())
assert model['choices'] and not model['choices'][0]['owner_findings']
assert model['cpu_hz']==80_000_000 and model['shape']==[1,1,2]
census_path=model_path.parent/'merged.json'
census=json.loads(census_path.read_text())
assert census['cpu_hz']==80_000_000 and census['shape']==[1,1,2]
for source,name in ((census_path,'calibration-complete-census.json'),(model_path,'calibration-complete-model.json')):
 target=r/name;assert not target.exists()
 shutil.copy2(source,target);assert target.read_bytes()==source.read_bytes()
record=dict(status='COMPLETE CALIBRATION INPUTS CLOSED; FIRMWARE CORRECTION AND FRESH QUALIFICATION REQUIRED',
 time=datetime.datetime.now(datetime.timezone.utc).isoformat(),firmware_tree=firmware_tree,groups=145,
 census_source=str(census_path),census_sha256=hashlib.sha256(census_path.read_bytes()).hexdigest(),
 model_source=str(model_path),model_sha256=hashlib.sha256(model_path.read_bytes()).hexdigest(),
 model_choice=model['choices'][0],load=model['load'],
 worst_pass=max(rows,key=lambda row:row['worst_pass_cycles']),
 builds={v:dict(executable_sha256=s['executable_sha256'],cpu_hz=s['cpu_hz']) for v,s in specs.items()},
 scripts=[dict(variant=v,group=g,sha256=digest) for (v,g),digest in sorted(scripts.items())],
 statement_findings=[dict(variant=row['variant'],group=row['group'],findings=row['stated']) for row in rows if row['stated']],
 note='All native outcomes and required service/SHARE/ledger checks pass. Under-stated costs remain explicit calibration findings; no image is qualified by this receipt.')
(r/'calibration-complete-closure.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ('scripts','builds')},indent=2),flush=True)
