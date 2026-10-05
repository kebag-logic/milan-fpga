#!/usr/bin/env python3
"""Foreground coordinator; two builds with four workers each, plus light docs gates."""
import concurrent.futures, os, pathlib, subprocess
p=pathlib.Path(__file__).resolve().parents[1]; root=p/'scratch/tree'
env=os.environ.copy(); env['TMPDIR']=str(p/'scratch'); env['PATH']=str(p/'scratch/venv/bin')+os.pathsep+env['PATH']
wrapper=p/'scratch/simulator'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=="-j": a[i+1]="4"\nos.execv("$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", ["verilator"]+a)\n')
wrapper.chmod(0o755)
def run(name,cmd):
 with (p/'receipts'/f'{name}.log').open('w') as out:
  out.write('COMMAND '+repr(cmd)+'\n'); out.flush()
  r=subprocess.run(cmd,cwd=root,env=env,stdout=out,stderr=subprocess.STDOUT)
 (p/'receipts'/f'{name}.rc').write_text(str(r.returncode)+'\n')
 print(name,r.returncode,flush=True)
 return r.returncode
jobs=[('make-check',['make','-j16','check']),('side-port',['make','-j16','-C','tb/side_port','run','VERILATOR='+str(wrapper)]),('rx-validator',['make','-j16','-C','tb/rx_validator','run','VERILATOR='+str(wrapper)])]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(lambda j:run(*j),jobs))
raise SystemExit(any(results))
