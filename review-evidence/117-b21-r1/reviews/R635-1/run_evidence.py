#!/usr/bin/env python3
"""Replay published offline analyses and focused documentation gates concurrently.

Arguments: source checkout, extracted public author directory, raw archive, packet.
All generated products live in packet/scratch. No bench access.
"""
import concurrent.futures as cf
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

repo,E,raw,packet=map(Path,sys.argv[1:5]);work=packet/'scratch/replay';work.mkdir(parents=True,exist_ok=True)
tools=E/'tools';py=sys.executable
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1',B5_W='110')
jobs=[]
def job(name,args,cwd=None):jobs.append((name,list(map(str,args)),cwd or repo))
for name in ['identity','identity2','identity2-end']:
    dest=work/name;shutil.copytree(E/'r3'/name,dest,dirs_exist_ok=True)
    job(name,[py,'-B',tools/'identity_b15.py',dest])
bad=work/'identity-bad-version';shutil.copytree(work/'identity2',bad,dirs_exist_ok=True)
p=bad/'console-identity.txt';p.write_text(p.read_text().replace('VERSION=00020060','VERSION=00020061'))
job('identity-bad-version',[py,'-B',tools/'identity_b15.py',bad])
for name in ['dA','dB']:
    job(name+'-csr',[py,'-B',tools/'b21_grade.py','csr',E/'r3/runs'/name/'dut-poll.txt',work/name])
    job(name+'-counters',[py,'-B',tools/'b21_grade.py','counters',work/name,*[E/'r3/runs'/name/('counters-'+n+'.jsonl') for n in ['pre','mid','post']]])
job('dA-ext',[py,'-B',tools/'b21_grade.py','ext',raw/'dA-ext',work/'dA'])
for name in ['mst-dry','mst-long']:
    job(name,[py,'-B',tools/'b21_mcasp_ana.py',raw/name,name,work/name])
job('dB-reads',[py,'-B',tools/'b21_mcasp_ana.py',raw/'dB','dB',work/'dB-reads'])
def sized(d,size):
    ps=[p for p in d.iterdir() if p.is_file() and p.stat().st_size==size];assert len(ps)==1;return ps[0]
job('restarts',[py,'-B',tools/'b21_restart.py',sized(raw/'rA',370480818),sized(raw/'rA',370293984),raw/'rA-ext',work/'rA-restart.json'])
md=Path(os.environ.get('MD_PYTHON',sys.executable))
for name,args in [('docs-check',['scripts/docs_check.py']),('doc-style',['scripts/check_doc_style.py']),
                  ('toc',['scripts/gen_toc.py','--check']),('em-dash',['scripts/check_em_dash.py','--base','4a9b5a2a']),
                  ('doc-paths',['scripts/check_doc_paths.py'])]:job(name,[md,*args])
job('diff-check',['git','diff','--check','4a9b5a2a','HEAD'])

def run(j):
    name,args,cwd=j
    with (work/(name+'.log')).open('w') as log:
        r=subprocess.run(args,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=540)
    (work/(name+'.rc')).write_text(str(r.returncode)+'\n')
    return name,r.returncode
with cf.ThreadPoolExecutor(max_workers=4) as pool:
    results=dict(pool.map(run,jobs))
print(json.dumps(results,indent=2),flush=True)
assert all(v==(1 if k=='identity-bad-version' else 0) for k,v in results.items()),results
comp={}
for name in ['dA-csr','dB-csr','dA-counters','dB-counters','dA-ext','rA-restart']:
    a=json.loads((work/(name+'.json')).read_text());b=json.loads((E/'r3/summary'/(name+'.json')).read_text())
    comp[name]=(a==b)
assert all(comp.values()),comp
print('Published summary equality:',json.dumps(comp),flush=True)
(packet/'replay-results.json').write_text(json.dumps({'returncodes':results,'summary_equal':comp},indent=2)+'\n')
# Public copies of numerical receipts, without terminal paths or equipment names.
for name in ['dA-csr','dB-csr','dA-counters','dB-counters','dA-ext','rA-restart']:
    shutil.copyfile(work/(name+'.json'),packet/(name+'-replayed.json'))
for name in ['mst-dry','mst-long']:
    shutil.copyfile(work/name/(name+'-analysis.txt'),packet/(name+'-replayed.txt'))
shutil.copyfile(work/'dB-reads/dB-analysis.txt',packet/'dB-reads-replayed.txt')
