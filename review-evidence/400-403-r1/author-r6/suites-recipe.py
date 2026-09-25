import json,os,pathlib,subprocess,time
out=pathlib.Path('$MANAGEMENT/2026-09-23/400-403-a323')
env=os.environ.copy();env.update(PATH='$VALIDATION_STORAGE/400-403-a323-bin:$WORKSPACE_HOME/litex-milan/venv/bin:'+env['PATH'],TMPDIR='$VALIDATION_STORAGE/400-403-a323-work',PYTHONHASHSEED='0')
results=[]
for suite in ['csr','pp_shadow','nvm_cosim']:
 cmd=['make','-C','tb/verilator/'+suite];log=out/(suite+'.log')
 print('START',suite,flush=True);start=time.time()
 with log.open('w') as f:
  f.write('COMMAND '+' '.join(cmd)+'\n');f.flush()
  proc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=14400)
 results.append(dict(suite=suite,command=' '.join(cmd),rc=proc.returncode,seconds=round(time.time()-start,3),log=log.name))
 (out/'suite-results.json').write_text(json.dumps(results,indent=2)+'\n')
 with (out/'HANDOFF.md').open('a') as f:f.write(f"\nSuite `{suite}`: rc {proc.returncode}; log `{log.name}`.\n")
 print('END',suite,'rc',proc.returncode,flush=True)
 if proc.returncode:raise SystemExit(proc.returncode)
