"""Prepare a calibration-only continuation without changing repository source.

Retain the original runner and its cost-adjustment receipt. The continuation
uses the same frozen executables, grading, four slots and per-row stop rules.
It never writes the status accepted by image qualification.
"""
import hashlib,json
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/refined')
original=(r/'run-final-census.py').read_text()
text=original
start=text.index('if out.exists():')
end=text.index('def explicit_wait_ms(group):')
replacement='''assert (out/'cost-adjustment-needed.json').exists()
prior_manifest=json.loads((out/'manifest.json').read_text())
assert prior_manifest['status']=='CALIBRATION COMPLETE; FIRMWARE COST ADJUSTMENT REQUIRED'
prior_records=json.loads((out/'completed.json').read_text())
assert len(prior_records)==prior_manifest['completed']
assert all(not row['native_status'] and not any(row[k] for k in
           ('refusals','share','late','forbidden')) for row in prior_records)
assert not (out/'stop-finding.json').exists()
done={(row['variant'],row['group']) for row in prior_records}
variants=tuple(prior_manifest['groups'])
specs={};groups={};jobs=[]
for variant in variants:
 directory=out/variant
 spec=build.reused(directory)
 assert spec['cpu_hz']==spec['sys_hz']==80_000_000
 assert spec['measurement_pace_ms']==9
 specs[variant]=spec
 selected=run.all_groups(scenario.point('arty-1x1',spec),spec)
 if variant=='answering-ports':
  selected=[g for g in selected if g.name in ('aecp','aecp-fanout','aecp-largest-notice','aecp-reboot')]
 assert sorted(g.name for g in selected)==sorted(prior_manifest['groups'][variant])
 assert spec['executable_sha256']==prior_manifest['executables'][variant]
 groups[variant]=selected
 jobs += [(variant,g) for g in selected if (variant,g.name) not in done]
manifest=dict(prior_manifest,status='CALIBRATION CONTINUATION IN PROGRESS',
              calibration_only=True,prior_completed=len(prior_records))
(out/'manifest-before-continuation.json').write_text(json.dumps(prior_manifest,indent=2)+'\\n')
(out/'completed-before-continuation.json').write_text(json.dumps(prior_records,indent=2)+'\\n')
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\\n')
'''
text=text[:start]+replacement+text[end:]
old='lock=threading.Lock(); stopped=threading.Event(); active={}; records=[]'
assert text.count(old)==1
text=text.replace(old,'lock=threading.Lock(); stopped=threading.Event(); active={}; records=list(prior_records)')
assert text.count("if (out/'cost-adjustment-needed.json').exists():return")==2
text=text.replace("if (out/'cost-adjustment-needed.json').exists():return",
                  "if (scratch/'calibration-progress/owner-finding.json').exists():return")
start=text.index('with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:')
text=text[:start]+'''with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 list(pool.map(one,jobs))
if stopped.is_set():raise SystemExit('calibration ended on a finding; inspect stop-finding.json')
if (scratch/'calibration-progress/owner-finding.json').exists():
 raise SystemExit('OWNER: measured model cannot meet the required bounds')
assert len(records)==sum(map(len,groups.values()))
for variant in variants:build.reused(out/variant)
manifest.update(status='CALIBRATION MEASUREMENTS COMPLETE; FIRMWARE CHANGES STILL REQUIRED',completed=len(records))
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\\n')
print(manifest['status'],len(records),flush=True)
'''
text='"""Calibration-only continuation; cannot qualify an image."""\n'+text
target=r/'continue-calibration.py';assert not target.exists();target.write_text(text)

original_watch=(r/'watch-final-costs.py').read_text();watch=original_watch
watch=watch.replace("out=r/'final-progress'","out=r/'calibration-progress'")
watch=watch.replace("seen=set();merged=r/'census-preliminary-complete.json';step=0",
 "seen={(row['variant'],row['group']) for row in json.loads((campaign/'completed-before-continuation.json').read_text())};merged=r/'calibration-base-census.json';step=0")
watch=watch.replace("startswith('NATIVE MEASUREMENTS COMPLETE')","startswith('CALIBRATION MEASUREMENTS COMPLETE')")
watch=watch.replace("status='PARTIAL FINAL COST FORECAST'","status='PARTIAL CALIBRATION COST FORECAST'")
old="""   (campaign/'cost-adjustment-needed.json').write_text(json.dumps(record,indent=2)+'\\n')
   print('FIRMWARE COST ADJUSTMENT REQUIRED',changes,flush=True)
   break"""
assert old in watch
watch=watch.replace(old,"""   (out/'firmware-adjustments.json').write_text(json.dumps(record,indent=2)+'\\n')
   print('FIRMWARE COST ADJUSTMENTS RECORDED FOR AFTER COMPLETE CALIBRATION',changes,flush=True)""")
# The native supervisor creates its preserved pre-continuation receipt first.
watch=watch.replace("seen={(row['variant']", "while not (campaign/'completed-before-continuation.json').exists():time.sleep(0.2)\nseen={(row['variant']")
target_watch=r/'watch-calibration-costs.py';assert not target_watch.exists();target_watch.write_text(watch)
for p in (target,target_watch):compile(p.read_text(),str(p),'exec')
(r/'calibration-continuation-preparation.json').write_text(json.dumps(dict(
 status='PREPARED, NOT RUN',source_runner_sha256=hashlib.sha256(original.encode()).hexdigest(),
 continuation_sha256=hashlib.sha256(text.encode()).hexdigest(),
 source_watcher_sha256=hashlib.sha256(original_watch.encode()).hexdigest(),
 watcher_sha256=hashlib.sha256(watch.encode()).hexdigest(),
 note='Only admission/scheduling and calibration labeling change; native commands and per-case grading are preserved.'),indent=2)+'\n')
print('Prepared and syntax-checked calibration-only continuation')
