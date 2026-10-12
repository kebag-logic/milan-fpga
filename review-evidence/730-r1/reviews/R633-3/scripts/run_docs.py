import concurrent.futures,json,subprocess,sys,time
from pathlib import Path
p=Path(sys.argv[1]);repo=sys.argv[2]
checks={
 'toc':['python3','scripts/gen_toc.py','--check'],
 'anchors':['python3','scripts/gen_toc.py','--verify-anchors'],
 'em-dash':['python3','scripts/check_em_dash.py','--base','dc4d06cb'],
 'py-idiom-selftest':['python3','scripts/check_py_idiom.py','--selftest'],
 'baremetal-selftest':['python3','scripts/check_baremetal_only.py','--selftest'],
 'diff-check':['git','diff','--check','dc4d06cb','HEAD']}
def run(item):
 name,cmd=item;start=time.monotonic()
 with (p/'receipts'/f'{name}.log').open('w') as out:
  r=subprocess.run(['sh',str(p/'scripts/reviewer_sandbox.sh'),repo,str(p),'env','PYTHONPATH=/packet/scratch/markdown',*cmd],stdout=out,stderr=subprocess.STDOUT,timeout=480)
 (p/'receipts'/f'{name}.rc').write_text(str(r.returncode)+'\n')
 result={'name':name,'command':cmd,'rc':r.returncode,'seconds':round(time.monotonic()-start,3)}
 print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,checks.items()))
(p/'receipts/docs-runs.json').write_text(json.dumps(results,indent=2)+'\n')
