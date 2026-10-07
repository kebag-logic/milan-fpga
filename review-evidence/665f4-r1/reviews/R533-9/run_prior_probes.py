#!/usr/bin/env python3
"""Run prior public probes in the foreground, retaining original exits."""
import concurrent.futures, os, subprocess, sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve(); p=Path(__file__).resolve().parent
env=dict(os.environ,TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1')
names=['srp-poll-drops-tx','srp-pass-drops-rx-and-poll','srp-rx-max-zero','srp-event-max-zero','control-none']
def run(name):
    argv=[sys.executable,'-B',str(p/'probe_mutants.py'),str(repo),str(repo/'third_party/lwSRP'),str(p/'scratch'/('external-'+name)),name]
    r=subprocess.run(argv,cwd=repo,capture_output=True,text=True,env=env,timeout=300)
    (p/(name+'.log')).write_text(r.stdout+r.stderr);(p/(name+'.rc')).write_text(str(r.returncode)+'\n')
    expected=0 if name=='control-none' else 1
    assert r.returncode==expected and 'REFUSED' not in r.stdout
    if expected:
        for i in (1,2): assert f'{name} srp_app.cpp IF={i}: FAIL' in r.stdout
    print(name,'PASS control' if expected==0 else 'CAUGHT at IF=1/2',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(run,names))
