#!/usr/bin/env python3
"""Usage: replay_public.py B18_AUTHOR B17_AUTHOR SCRATCH_DIR. Offline only."""
import concurrent.futures, hashlib, json, shutil, subprocess, sys
from pathlib import Path
src, old, scratch = map(Path, sys.argv[1:])
scratch.mkdir(parents=True,exist_ok=True)
p=scratch/'replay-author'
shutil.copytree(src,p,dirs_exist_ok=True)
commands=[['python3',str(p/'tools/identity_b15.py'),str(p/'identity')],['python3',str(p/'tools/summ_b18.py'),str(p),str(old)]]
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    return r.returncode,r.stdout,r.stderr
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,commands))
for name,result in zip(['identity','summary'],results):
    rc,out,err=result
    (scratch/(name+'.stdout')).write_text(out); (scratch/(name+'.stderr')).write_text(err)
    print(name,'RC',rc)
    assert rc==0
for f in ['identity/identity-verdict.txt','summary/cycles.json','summary/table.md','summary/compare.md','summary/counters.md','summary/counter-logs.sha256']:
    assert (p/f).read_bytes()==(src/f).read_bytes(),f
    print('Byte-identical regenerated output:',f,hashlib.sha256((p/f).read_bytes()).hexdigest())
print('OFFLINE REPLAY PASS')
