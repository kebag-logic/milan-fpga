import pathlib,sys,os,subprocess,time,json,signal
p=pathlib.Path(__file__).resolve().parent;root=pathlib.Path(sys.argv[1]).resolve()
env=dict(os.environ,TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1',PYTHONUNBUFFERED='1',MAKEFLAGS='-j16')
env['PATH']=str(p/'scratch/reference/bin')+':'+env['PATH']
cmd=['python3','sw/builder/test_firmware_compiler.py','--absent','--audit',str(p/'scratch/rv32-absent-retry.jsonl')]
start=time.monotonic()
with (p/'gate-logs/docs-034-retry.log').open('w') as out:
 proc=subprocess.Popen(cmd,cwd=root,env=env,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
 try:rc=proc.wait(timeout=1800)
 except subprocess.TimeoutExpired:
  os.killpg(proc.pid,signal.SIGTERM);proc.wait();rc=124
result={'command':cmd,'rc':rc,'seconds':round(time.monotonic()-start,3),'log':'gate-logs/docs-034-retry.log','initial_timeout_seconds':540}
(p/'compiler-absent-retry.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
