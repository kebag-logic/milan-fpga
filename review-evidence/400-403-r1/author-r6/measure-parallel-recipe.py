import concurrent.futures as cf,json,os,pathlib,shlex,signal,subprocess,threading,time
root=pathlib.Path('$LANES/400-403-declaration-truth')
out=pathlib.Path('$MANAGEMENT/2026-09-23/400-403-a323')
points=[('8x8',50000000,'on'),('8x8',50000000,'off'),('1x1_tdm8',50000000,'on'),('1x1_tdm8',50000000,'off'),('8x8',100000000,'on'),('8x8',100000000,'off')]
env=os.environ.copy();env.update(PATH='$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin:$WORKSPACE_HOME/litex-milan/venv/bin:'+env['PATH'],LITEX_ENV_CC_TRIPLE='riscv32-linux',PYTHONHASHSEED='0',COURSIER_MODE='offline',SBT_OPTS='-Dsbt.offline=true')
lock=threading.Lock();running={};results={};abort=threading.Event()
def run(point):
 shape,clock,arm=point;label=f'{shape}-{clock//1000000}-{arm}'
 build=pathlib.Path('$VALIDATION_STORAGE/400-403-a323-capture-'+label)
 cmd=['unshare','-Urn','python3','tb/verilator/nvm_capture_cpu/run.py','--shape','endstation_ax7101_'+shape,'--cpu-hz',str(clock),'--captures','16','--traffic',arm,'--build-dir',str(build)]
 log=out/('capture-'+label+'.log');start=time.time()
 print('START',label,flush=True)
 with log.open('w') as f:
  f.write('COMMAND '+shlex.join(cmd)+'\n');f.flush()
  proc=subprocess.Popen(cmd,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
  with lock:running[label]=proc
  try:rc=proc.wait(timeout=14400)
  except BaseException:
   os.killpg(proc.pid,signal.SIGTERM);proc.wait();raise
 result=dict(label=label,command=shlex.join(cmd),rc=rc,seconds=round(time.time()-start,3),build_dir=str(build),log=log.name)
 if rc==0:
  result['measurement']=json.loads((build/'measurement.json').read_text())
  (out/('measurement-'+label+'.json')).write_text(json.dumps(result['measurement'],indent=2)+'\n')
 if (build/'capture.log').exists():(out/('rows-'+label+'.log')).write_bytes((build/'capture.log').read_bytes())
 with lock:
  running.pop(label,None);results[point]=result
  ordered=[results[p] for p in points if p in results]
  (out/'measurement-runs.json').write_text(json.dumps(ordered,indent=2)+'\n')
  with (out/'HANDOFF.md').open('a') as f:f.write(f"\nMeasurement `{label}`: rc {rc}; log `{log.name}`.\n")
  if rc:
   abort.set()
   for other in running.values():
    if other.poll() is None:os.killpg(other.pid,signal.SIGTERM)
 print('END',label,'rc',rc,'maximum_ms',result.get('measurement',{}).get('maximum_ms'),flush=True)
 return rc
with cf.ThreadPoolExecutor(max_workers=6) as pool:
 futures=[pool.submit(run,p) for p in points]
 codes=[f.result() for f in futures]
raise SystemExit(1 if any(codes) else 0)
