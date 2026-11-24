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
if out.exists():raise SystemExit('refused: use a fresh final-census directory; preserve prior evidence')
out.mkdir()
variants=('none','answering-ports','answering-every-port','valid-destinations',
          'declaring-outputs','answering-later','talker-notices','shutdown-entry')
specs={}; groups={}; jobs=[]
for variant in variants:
 directory=out/variant
 print('BUILD',variant,flush=True)
 with (out/(variant+'-build.log')).open('w') as sink:
  command=[sys.executable,'-B',str(scratch/'build-final-variant.py'),str(directory),variant]
  subprocess.run(command,cwd=root,stdout=sink,stderr=subprocess.STDOUT,check=True,timeout=10800)
 spec=build.reused(directory)
 spec['measurement_pace_ms']=rows_tiers.built_constants(root,'arty-1x1')[-1]
 assert spec['measurement_pace_ms']==model['pace_ms']
 (directory/'build.json').write_text(json.dumps(spec,indent=2)+'\n')
 assert spec['cpu_hz']==spec['sys_hz']==80_000_000
 specs[variant]=spec
 selected=run.all_groups(scenario.point('arty-1x1',spec),spec)
 if variant=='answering-ports':
  selected=[g for g in selected if g.name in ('aecp','aecp-fanout','aecp-largest-notice','aecp-reboot')]
 groups[variant]=selected
 (directory/'results').mkdir()
 jobs += [(variant,g) for g in selected]
manifest=dict(status='MEASUREMENT IN PROGRESS',model=model,groups={v:[g.name for g in gs] for v,gs in groups.items()},
              executables={v:s['executable_sha256'] for v,s in specs.items()},max_native_legs=4)
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
lock=threading.Lock(); stopped=threading.Event(); active={}; records=[]
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
 if (out/'cost-adjustment-needed.json').exists():return
 with slot('service '+job[0]+' '+job[1].name):
  if (out/'cost-adjustment-needed.json').exists():return
  return measured(job)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 # Complete the four scheduling/held-load cases before admitting long cases.
 list(pool.map(one,jobs[:4]))
 list(pool.map(one,jobs[4:]))
if stopped.is_set():raise SystemExit('measurement ended on a finding; inspect stop-finding.json')
if (out/'cost-adjustment-needed.json').exists():
 for variant in variants:build.reused(out/variant)
 manifest.update(status='CALIBRATION COMPLETE; FIRMWARE COST ADJUSTMENT REQUIRED',completed=len(records))
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(manifest['status'],len(records),flush=True)
 raise SystemExit(0)
assert len(records)==len(jobs)
for variant in variants:build.reused(out/variant)
manifest.update(status='NATIVE MEASUREMENTS COMPLETE; FINAL COST AND CLASS CHECKS REQUIRED',completed=len(records))
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(manifest['status'],len(records),flush=True)
