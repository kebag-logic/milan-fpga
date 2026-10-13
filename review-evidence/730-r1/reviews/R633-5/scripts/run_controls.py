#!/usr/bin/env python3
"""Run public signal mutations and focused document gates, four tasks at once."""
import concurrent.futures,json,os,shutil,subprocess,sys,time
from pathlib import Path
p=Path(__file__).resolve().parent.parent
repo=Path(sys.argv[1]).resolve()
controls=json.loads((p/'public-inputs/author-r5/receipts/r5/mutations-r5-controls.json').read_text())
base=p/'scratch/pristine'
def run(name,cmd,cwd):
 start=time.monotonic()
 with (p/'receipts'/f'{name}.log').open('w') as f:
  try:rc=subprocess.run(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,timeout=300).returncode
  except subprocess.TimeoutExpired:rc=124
 (p/'receipts'/f'{name}.rc').write_text(str(rc)+'\n')
 row={'name':name,'command':cmd,'rc':rc,'seconds':round(time.monotonic()-start,3)}
 print(json.dumps(row),flush=True);return row
def mutation(c):
 ident,mode,old,new=c
 tree=p/'scratch/signal-mutants'/ident
 shutil.copytree(base,tree,copy_function=os.link)
 target=tree/'scripts/act_ci.py';text=target.read_text();assert text.count(old)==1
 target.unlink();target.write_text(text.replace(old,new))
 sb=['sh',str(p/'scripts/reviewer_sandbox.sh'),str(tree),str(p)]
 return run(ident,sb+['python3','-I','/packet/public-inputs/author-r5/receipts/r5/run_masked_arms.py','/work/scripts/act_ci.py',mode],repo)
gates={
'docs-check':['python3','scripts/docs_check.py'],
'doc-style':['python3','scripts/check_doc_style.py'],
'doc-paths':['python3','scripts/check_doc_paths.py'],
'baremetal':['python3','scripts/check_baremetal_only.py','--check'],
'baremetal-selftest':['python3','scripts/check_baremetal_only.py','--selftest'],
'diff-check':['git','diff','--check','dc4d06cb','HEAD'],
}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
 fs=[e.submit(mutation,c) for c in controls]
 fs.extend(e.submit(run,n,cmd,repo) for n,cmd in gates.items())
 rows=[f.result() for f in fs]
(p/'receipts/controls-gates.json').write_text(json.dumps(rows,indent=2)+'\n')
sys.exit(0 if all(x['rc']==(1 if x['name'].startswith('E') else 0) for x in rows) else 1)
