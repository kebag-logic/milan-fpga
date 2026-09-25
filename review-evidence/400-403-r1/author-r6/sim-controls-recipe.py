import concurrent.futures as cf,json,os,pathlib,shlex,subprocess,time
out=pathlib.Path('$MANAGEMENT/2026-09-23/400-403-a323')
env=os.environ.copy();env.update(PATH='$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin:$WORKSPACE_HOME/litex-milan/venv/bin:'+env['PATH'],LITEX_ENV_CC_TRIPLE='riscv32-linux',PYTHONHASHSEED='0',COURSIER_MODE='offline',SBT_OPTS='-Dsbt.offline=true')
def run(mutation):
 build=pathlib.Path('$VALIDATION_STORAGE/400-403-a323-control-'+mutation)
 cmd=['unshare','-Urn','python3','tb/verilator/nvm_capture_cpu/run.py','--shape','endstation_ax7101_1x1_tdm8','--captures','2','--mutation',mutation,'--build-dir',str(build)]
 log=out/('control-'+mutation+'.log');begin=time.time();print('START',mutation,flush=True)
 with log.open('w') as f:
  f.write('COMMAND '+shlex.join(cmd)+'\n');f.flush()
  proc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=14400)
 if (build/'capture.log').exists():(out/('control-'+mutation+'-rows.log')).write_bytes((build/'capture.log').read_bytes())
 result=dict(mutation=mutation,command=shlex.join(cmd),rc=proc.returncode,seconds=round(time.time()-begin,3),log=log.name)
 (out/('control-'+mutation+'.json')).write_text(json.dumps(result,indent=2)+'\n')
 print('END',mutation,'rc',proc.returncode,flush=True);return proc.returncode
with cf.ThreadPoolExecutor(max_workers=2) as pool:codes=list(pool.map(run,['skip-copy','no-traffic']))
raise SystemExit(1 if any(codes) else 0)
