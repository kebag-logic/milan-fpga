import json,os,pathlib,shlex,subprocess,sys,time
name=sys.argv[1];want=int(sys.argv[2]);cmd=sys.argv[3:]
out=pathlib.Path('$MANAGEMENT/2026-09-23/400-403-a323')
env=os.environ.copy();env.update(PATH='$WORKSPACE_HOME/litex-milan/venv/bin:'+env['PATH'],PYTHONPATH='$VALIDATION_STORAGE/517-a321-env/lib/python3.14/site-packages:$VALIDATION_TOOLS/md-venv-40cdefe08ebd/lib/python3.14/site-packages:/usr/lib/python3.14/site-packages',PYTHONHASHSEED='0',TMPDIR='$VALIDATION_STORAGE/400-403-a323-work',PIP_NO_INDEX='1')
start=time.time();log=out/(name+'.log');print('START',name,flush=True)
with log.open('w') as f:
 f.write('COMMAND '+shlex.join(cmd)+'\n');f.flush()
 result=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=14400)
record=dict(name=name,command=shlex.join(cmd),rc=result.returncode,expected_rc=want,seconds=round(time.time()-start,3),log=log.name)
(out/(name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print('END',name,'rc',result.returncode,'expected',want,flush=True)
raise SystemExit(0 if result.returncode==want else 1)
