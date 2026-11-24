"""Calibration-only continuation; cannot qualify an image."""
"""Fresh Arty images and complete foreground measurement, four native legs.

No result is promoted to image qualification here. Every completed group is
graded immediately, and an owner/share or non-ledger miss ends native work.
"""
import concurrent.futures,hashlib,json,os,re,subprocess,sys,threading
from pathlib import Path
from harness_slots import slot
root=Path.cwd(); scratch=Path('$VALIDATION_STORAGE/artysplit-a829/r4/refined'); out=scratch/'final-census'
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import arty_grade,build,egress_ledger,run,scenario,rows_tiers
model,findings=arty_grade.inspect(root)
if findings:raise SystemExit('refused: own model is not ready: '+repr(findings))
for entry in Path('/proc').glob('[0-9]*/cmdline'):
 try: executable=entry.read_bytes().split(b'\0')[0]
 except OSError:continue
 if executable.startswith(str(scratch).encode()) and executable.endswith(b'/native/Vsim'):
  raise SystemExit('refused: another Arty native measurement still owns a slot')
assert (out/'cost-adjustment-needed.json').exists()
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
(out/'manifest-before-continuation.json').write_text(json.dumps(prior_manifest,indent=2)+'\n')
(out/'completed-before-continuation.json').write_text(json.dumps(prior_records,indent=2)+'\n')
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
def explicit_wait_ms(group):
 # `wait cycles` is relative; `wait ms` is an absolute firmware-clock target
 # (sim_main.cpp::satisfied). This schedules work; it changes no stimulus.
 elapsed=0.0
 for line in group.script().splitlines():
  if match:=re.fullmatch(r'wait cycles (\d+)',line):elapsed+=int(match[1])/80000
  elif match:=re.fullmatch(r'wait ms (\d+)',line):elapsed=max(elapsed,int(match[1]))
 return elapsed
# Check the changed scheduler under held load before the long campaign, then
# schedule remaining cases longest first. No script or coverage is changed.
first={('none','backlog-adp'),('none','backlog-owed'),
       ('declaring-outputs','aecp-largest-notice'),('valid-destinations','srp-talker-held')}
jobs.sort(key=lambda pair:((pair[0],pair[1].name) not in first,-explicit_wait_ms(pair[1])))
lock=threading.Lock(); stopped=threading.Event(); active={}; records=list(prior_records)
def measured(job):
 variant,g=job
 with lock:
  if stopped.is_set():return
  directory=out/variant; results=directory/'results';spec=specs[variant]
  script=results/(g.name+'.txt');script.write_text(g.script())
  log=results/(g.name+'.log')
  argv=[str(directory/'native/Vsim'),str(script),spec.get('flash_image') or '-']
  env=dict(os.environ,BUDGET_JOURNAL_OUT=str(run.journal_of(results,g))) if g.save.get('journal') else None
  sink=log.open('w')
  process=subprocess.Popen(argv,cwd=directory/'gateware',stdout=sink,stderr=subprocess.STDOUT,env=env)
  active[process.pid]=process
  print('START',variant,g.name,process.pid,flush=True)
 try: rc=process.wait(timeout=86400)
 except subprocess.TimeoutExpired:
  process.terminate()
  try:process.wait(timeout=10)
  except subprocess.TimeoutExpired:process.kill();process.wait()
  rc=124
 finally:
  sink.close()
  with lock:active.pop(process.pid,None)
 if stopped.is_set():return
 (results/(g.name+'.status')).write_text(str(rc)+'\n')
 graded,refusals,misses=run.graded([g],[log],spec,results)
 shares=run.share_misses(graded)
 late=run.save_misses(graded)+run.burst_misses(graded)+run.notice_misses(graded,1)
 for result in graded:
  joins=result['passes'].get('joins',{})
  late += [f"{g.name}: join interval {row['ms']} ms outside protocol range" for row in joins.get('over',[])]
  late += [run.run_out_miss(g.name,row) for row in joins.get('failing',[])]
  late += [run.leave_all_miss(g.name,row) for row in joins.get('leave_all',{}).get('failing',[])]
 forbidden=[]
 for result in graded:
  for p in result['probes']:
   if p.get('within_budget',True):continue
   entry={**p,'group':g.name,'exact':True};ledger=egress_ledger.LEDGER['arty-1x1']
   if not egress_ledger.is_row(entry,ledger) or egress_ledger.over(entry,ledger[p['probe']]):forbidden.append(p)
 record=dict(variant=variant,group=g.name,native_status=rc,trace_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),
             refusals=refusals,misses=misses,share=shares,late=late,forbidden=forbidden,
             stated=run.stated_misses(graded),worst_pass_cycles=max([x['passes']['worst']['cycles'] for x in graded] or [0]))
 with lock:
  records.append(record)
  (out/'completed.json').write_text(json.dumps(records,indent=2)+'\n')
  print('DONE',variant,g.name,rc,'stated',len(record['stated']),flush=True)
  if rc or refusals or shares or late or forbidden:
   stopped.set();(out/'stop-finding.json').write_text(json.dumps(record,indent=2)+'\n')
   for other in active.values():other.terminate()
def one(job):
 if (scratch/'calibration-progress/owner-finding.json').exists():return
 with slot('service '+job[0]+' '+job[1].name):
  if (scratch/'calibration-progress/owner-finding.json').exists():return
  return measured(job)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 list(pool.map(one,jobs))
if stopped.is_set():raise SystemExit('calibration ended on a finding; inspect stop-finding.json')
if (scratch/'calibration-progress/owner-finding.json').exists():
 raise SystemExit('OWNER: measured model cannot meet the required bounds')
assert len(records)==sum(map(len,groups.values()))
for variant in variants:build.reused(out/variant)
manifest.update(status='CALIBRATION MEASUREMENTS COMPLETE; FIRMWARE CHANGES STILL REQUIRED',completed=len(records))
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(manifest['status'],len(records),flush=True)
