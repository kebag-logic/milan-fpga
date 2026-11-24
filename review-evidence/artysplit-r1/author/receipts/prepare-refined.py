"""Stage a fresh evidence namespace while the previous calibration drains."""
import json,shutil
from pathlib import Path
old=Path('$VALIDATION_STORAGE/artysplit-a829/r4');new=old/'refined'
assert not new.exists();new.mkdir();(new/'work-tmp').mkdir()
names=('harness_slots.py','census.py','parts.py','eventcost.py','merge-census.py','derive-own.py',
       'run-final-census.py','build-final-variant.py','watch-final-costs.py','qualify-final-census.py',
       'run-final-other-gates.py','final-product-identity.py','identity-final-build.py',
       'arty-product-final-build.py','identity-final-export.py','identity-export-worker.py',
       'final-product-docs.py','heartbeat.py','build-images.py','grade-images.py','publish-image.py',
       'check-old-rows.py')
for name in names:
 text=(old/name).read_text().replace(str(old),str(new))
 (new/name).write_text(text)
for name in ('identity-before','native-optimization'):(new/name).symlink_to(old/name,target_is_directory=True)
shutil.copy2(old/'identity-compare.json',new/'identity-compare.json')
(new/'docs').mkdir();shutil.copy2(old/'docs/results.json',new/'docs/results.json')
def edit(name,before,after):
 p=new/name;s=p.read_text();assert s.count(before)==1,(name,before);p.write_text(s.replace(before,after))
edit('final-product-docs.py',"out=r/'docs-final'","out=r/'docs-final-corrected'")
edit('watch-final-costs.py',"if not pending or (len(pending)<5 and seen and not complete):","if not pending:")
edit('watch-final-costs.py',"merged=r/'census-preliminary-complete.json';step=0",
     "merged=r/'census-preliminary-complete.json';step=0\n"
     "sys.path.insert(0,str(Path.cwd()/'tb/verilator/ctrl_service_budget'))\n"
     "import shape_costs\ninstalled=shape_costs.at(shape_costs.Shape(1,1,2),Path.cwd())")
edit('watch-final-costs.py'," if not model['choices']:\n",''' if model['choices']:
  choice=model['choices'][0];costs=model['costs']
  wanted=dict(CTRL_LOOP_SLICE_US=choice['slice_us'],CTRL_LOOP_BUILD_PASS_US=costs['build'],
   CTRL_LOOP_BUILD_ONE_PASS_US=costs['build_one'],CTRL_LOOP_SRP_UNIT_US=costs['record.srp'],
   CTRL_LOOP_RETRY_COLD_US=model['retry_us'][0],CTRL_LOOP_RETRY_ATTEMPT_US=model['retry_us'][1],
   CTRL_LOOP_QUEUED_MS=choice['queued_ms'],CTRL_LOOP_STEP_PASS_US=costs['step'],
   CTRL_LOOP_TICK_US=costs['centisecond'],AECP_NOTICE_US=model['retry_us'][2],AECP_PACE_MS=choice['pace_ms'])
  changes={key:dict(installed=installed[key],measured=value) for key,value in wanted.items() if installed[key]!=value}
  if changes:
   record['firmware_changes']=changes
   (campaign/'cost-adjustment-needed.json').write_text(json.dumps(record,indent=2)+'\\n')
   print('FIRMWARE COST ADJUSTMENT REQUIRED',changes,flush=True)
   break
 if not model['choices']:
''')
edit('run-final-census.py',"def one(job):\n with slot('service '+job[0]+' '+job[1].name):return measured(job)",
     "def one(job):\n if (out/'cost-adjustment-needed.json').exists():return\n"
     " with slot('service '+job[0]+' '+job[1].name):\n"
     "  if (out/'cost-adjustment-needed.json').exists():return\n  return measured(job)")
edit('run-final-census.py'," list(pool.map(one,jobs))",
     " # Complete the four scheduling/held-load cases before admitting long cases.\n"
     " list(pool.map(one,jobs[:4]))\n list(pool.map(one,jobs[4:]))")
edit('run-final-census.py',"assert len(records)==len(jobs)",
     "if (out/'cost-adjustment-needed.json').exists():\n"
     " for variant in variants:build.reused(out/variant)\n"
     " manifest.update(status='CALIBRATION COMPLETE; FIRMWARE COST ADJUSTMENT REQUIRED',completed=len(records))\n"
     " (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\\n')\n"
     " print(manifest['status'],len(records),flush=True)\n raise SystemExit(0)\n"
     "assert len(records)==len(jobs)")
edit('heartbeat.py',"ready=manifest.get('status','').startswith('NATIVE MEASUREMENTS COMPLETE')",
     "ready=manifest.get('status','').startswith('NATIVE MEASUREMENTS COMPLETE')\n"
     "adjusting=(r/'final-census/cost-adjustment-needed.json').exists()\n"
     "adjusted=manifest.get('status','').startswith('CALIBRATION COMPLETE; FIRMWARE COST ADJUSTMENT REQUIRED')")
edit('heartbeat.py',"ready_to_adjust=bool(drain and drain['status'].startswith('NATIVE DRAIN COMPLETE')))",
     "ready_to_adjust=adjusted or bool(drain and drain['status'].startswith('NATIVE DRAIN COMPLETE')),adjusting=adjusting)")
for name in names:compile((new/name).read_text(),str(new/name),'exec')
(new/'preparation.json').write_text(json.dumps(dict(status='PREPARED; SOURCE NOT YET CORRECTED',
    copied_helpers=list(names),old_evidence=str(old),new_evidence=str(new),
    note='No qualification job has started. Old artifacts and traces remain at their original paths.'),indent=2)+'\n')
print('Prepared',new,flush=True)
