#!/usr/bin/env python3
import concurrent.futures, os, pathlib, subprocess, sys
packet=pathlib.Path(__file__).resolve().parents[1]
source=pathlib.Path(sys.argv[1]).resolve()
scratch=packet/'scratch'; receipts=packet/'receipts'
def run(name,cmd):
 with (receipts/(name+'.log')).open('w') as log:
  log.write('COMMAND '+repr(cmd)+'\n'); log.flush()
  r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 (receipts/(name+'.rc')).write_text(str(r.returncode)+'\n')
 print(name,r.returncode,flush=True)
 return r.returncode
jobs=[('scratch-clone',['git','clone','--quiet','--no-hardlinks',str(source),str(scratch/'tree')]),('python-env',[sys.executable,'-m','venv',str(scratch/'venv')])]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 assert all(x==0 for x in pool.map(lambda x:run(*x),jobs))
assert run('renderer-install',[str(scratch/'venv/bin/python'),'-m','pip','install','wavedrom==2.0.3.post3'])==0
