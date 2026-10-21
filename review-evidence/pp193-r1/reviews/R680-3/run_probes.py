#!/usr/bin/env python3
"""Foreground-owned concurrent probes, archived from a supplied exact revision."""
import argparse,concurrent.futures,io,os,pathlib,subprocess,tarfile
p=argparse.ArgumentParser();p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--packet',type=pathlib.Path,required=True);p.add_argument('--revision',default='474346357043218c4e6b728f4ab4b83a2a8579e1');a=p.parse_args()
a.source=a.source.resolve();a.packet=a.packet.resolve();scratch=a.packet/'scratch'
data=subprocess.check_output(['git','archive',a.revision],cwd=a.source)
def run(name,script):
 tree=scratch/(name+'-tree');tree.mkdir(exist_ok=True)
 with tarfile.open(fileobj=io.BytesIO(data)) as t:t.extractall(tree,filter='data')
 subprocess.run(['python3',str(a.packet/'probes'/script),str(tree/'tb/srp_stream_fsms/sim_main.cpp')],check=True)
 env=dict(os.environ,VERILATOR=str(scratch/'compiler-cap.py'),REVIEW_BUILD_JOBS='2',MAKEFLAGS='-j16',TMPDIR=str(scratch))
 with (a.packet/(name+'.log')).open('w') as log:
  r=subprocess.run(['make','-j16','RUN_ARGS=suite'],cwd=tree/'tb/srp_stream_fsms',env=env,stdout=log,stderr=subprocess.STDOUT)
 (a.packet/(name+'.rc')).write_text(str(r.returncode)+'\n')
 lines=(a.packet/(name+'.log')).read_text().splitlines();matches=[x for x in lines if '-> MATCH' in x];diffs=[x for x in lines if '-> DIFF' in x]
 expected={'s2':20,'repark':1,'collateral':12}[name]
 ok=r.returncode==0 and len(matches)==expected and not diffs
 print(name, 'PASS' if ok else 'FAIL', 'MATCH',len(matches),'DIFF',len(diffs),'rc',r.returncode,flush=True)
 return ok
with concurrent.futures.ThreadPoolExecutor(3) as pool:
 fs=[pool.submit(run,n,s) for n,s in [('s2','s2_probe.py'),('repark','repark_probe.py'),('collateral','collateral_probe.py')]]
 results=[f.result() for f in fs]
raise SystemExit(not all(results))
