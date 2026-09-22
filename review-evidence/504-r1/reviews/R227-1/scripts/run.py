import datetime,json,os,pathlib,subprocess,sys,time
OUT=pathlib.Path('$WORKSPACE_HOME/milan-fpga-management/2026-09-22/504-r1-r227')
ROOT=pathlib.Path('$VALIDATION_STORAGE/reviews/r227-504-r1')
label,*cmd=sys.argv[1:]; argv=['rtk','proxy',*cmd]; env=os.environ.copy(); env.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(OUT/'tmp'),MAKEFLAGS='-j8',CMAKE_BUILD_PARALLEL_LEVEL='8')
(OUT/'tmp').mkdir(exist_ok=True)
start=time.monotonic(); begun=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (OUT/'raw'/f'{label}.log').open('w') as log:
 p=subprocess.run(argv,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
r={'label':label,'argv':argv,'cwd':str(ROOT),'started_utc':begun,'duration_seconds':round(time.monotonic()-start,3),'returncode':p.returncode,'head':subprocess.check_output(['rtk','proxy','git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),'env_overrides':{k:env[k] for k in ('PYTHONDONTWRITEBYTECODE','TMPDIR','MAKEFLAGS','CMAKE_BUILD_PARALLEL_LEVEL')}}
(OUT/'raw'/f'{label}.json').write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps(r)); sys.exit(p.returncode)
