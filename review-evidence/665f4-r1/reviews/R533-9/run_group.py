#!/usr/bin/env python3
"""Foreground controller: bounded concurrent children, individual logs and exit receipts."""
import argparse, concurrent.futures, os, subprocess, sys, time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True);ap.add_argument('group',choices=['srp','a0']);a=ap.parse_args()
p=a.packet.resolve();script=p/'focused.py'
jobs=[(f'{mode}-if{i}',['--mode',mode,'--interfaces',str(i)]) for mode in ['native','plants'] for i in [1,2]] if a.group=='srp' else [(f'a0-{cc}',['--mode','a0','--compiler',cc]) for cc in ['gcc','clang','asan']]
def run(job):
    name,opts=job;start=time.monotonic();env=dict(os.environ,TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1')
    with (p/(name+'.log')).open('w') as log:
        r=subprocess.run([sys.executable,'-B',str(script),'--repo',str(a.repo.resolve()),'--packet',str(p),'--jobs','4',*opts],stdout=log,stderr=subprocess.STDOUT,env=env,timeout=580)
    (p/(name+'.rc')).write_text(str(r.returncode)+'\n')
    print(name,'rc',r.returncode,'seconds',round(time.monotonic()-start,2),flush=True)
    return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: results=list(ex.map(run,jobs))
sys.exit(any(results))
