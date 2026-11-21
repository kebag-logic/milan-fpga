#!/usr/bin/env python3
import concurrent.futures,os,pathlib,subprocess,sys
p=pathlib.Path(__file__).resolve().parent;r=pathlib.Path(sys.argv[1]).resolve()
jobs=[('docs-check',['python3','-B','scripts/docs_check.py']),('docs-inventory',['python3','-B','scripts/docs_inventory.py','--check']),('em-dash',['python3','-B','scripts/check_em_dash.py','--base','15168e14'])]
def run(item):
 n,c=item
 with (p/(n+'.log')).open('w') as f:
  f.write(repr(c)+'\n');f.flush();s=subprocess.run(c,cwd=r,stdout=f,stderr=subprocess.STDOUT)
 (p/(n+'.rc')).write_text(str(s.returncode)+'\n');return n,s.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for result in pool.map(run,jobs):print(result)
