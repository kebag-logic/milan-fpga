import io,json,os,pathlib,subprocess,tarfile,time
root=pathlib.Path('$LANES/400-403-declaration-truth')
out=pathlib.Path('$MANAGEMENT/2026-09-23/400-403-a323')
export=pathlib.Path('$VALIDATION_STORAGE/400-403-a323-nogit')
export.mkdir(exist_ok=False)
data=subprocess.check_output(['git','archive','HEAD'],cwd=root)
with tarfile.open(fileobj=io.BytesIO(data)) as archive:archive.extractall(export,filter='data')
for name in ['tb/verilator/nvm_capture_cpu/measurements.json','docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md']:
 (export/name).write_bytes((root/name).read_bytes())
assert not (export/'.git').exists()
env=os.environ.copy();env.update(PATH='$WORKSPACE_HOME/litex-milan/venv/bin:'+env['PATH'],PYTHONPATH='$VALIDATION_STORAGE/517-a321-env/lib/python3.14/site-packages:$VALIDATION_TOOLS/md-venv-40cdefe08ebd/lib/python3.14/site-packages:/usr/lib/python3.14/site-packages',TMPDIR='$VALIDATION_STORAGE/400-403-a323-work',PIP_NO_INDEX='1')
for script in ['docs_check','check_feature_status']:
 cmd=['python3','scripts/'+script+'.py'];name='nogit-'+script;log=out/(name+'.log');begin=time.time()
 with log.open('w') as f:
  f.write('COMMAND '+' '.join(cmd)+'\nCWD '+str(export)+'\n');f.flush()
  proc=subprocess.run(cmd,cwd=export,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=14400)
 (out/(name+'.json')).write_text(json.dumps(dict(name=name,command=' '.join(cmd),cwd=str(export),rc=proc.returncode,seconds=round(time.time()-begin,3),log=log.name),indent=2)+'\n')
 print(name,'rc',proc.returncode,flush=True)
 if proc.returncode:raise SystemExit(proc.returncode)
