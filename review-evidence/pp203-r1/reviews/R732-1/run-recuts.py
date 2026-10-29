#!/usr/bin/env python3
"""Focused recut regression campaigns and documentation checks in disposable trees."""
import concurrent.futures, os, pathlib, subprocess, sys
P=pathlib.Path(__file__).resolve().parent
SRC=pathlib.Path(sys.argv[1]).resolve()
S=P/'scratch'
W=S/'compiler-limit'
env=dict(os.environ,TMPDIR=str(S),MAKEFLAGS='-j16',VERILATOR=str(W),PYTHONDONTWRITEBYTECODE='1')
def run(name,cmd,cwd=SRC):
    with (P/(name+'.log')).open('w') as f:
        f.write(repr(cmd)+'\n'); f.flush()
        rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
    (P/(name+'.rc')).write_text(str(rc)+'\n'); print(name,rc,flush=True)
def campaign(name,script,arms):
    pin=['--verilator',str(W)] if 'd3_mutants' in script else []
    run(name,['python3',str(SRC/script),'--jobs','1','--output',str(P/name)]+pin+['--only']+arms)
def docs():
    dest=S/'docs-git'
    if not dest.exists():
        subprocess.run(['git','clone','--quiet','--no-hardlinks',str(SRC),str(dest)],check=True)
    run('docs-check-git',['make','-j16','check'],dest)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    tasks=[
      pool.submit(campaign,'recut-aecp','tb/pp_top/aecp_mutants.py',['dl-kill-tied-off,acmp-waits-for-aecp,hz-stub-restored,hz-setcfg-not-barrier,hz-setcfg-not-barrier-talker']),
      pool.submit(campaign,'recut-adp','tb/adp_engine/mutants.py',['if-egress-collapsed,if-top-ingress-live']),
      pool.submit(campaign,'recut-d3','tb/pp_top/d3_mutants.py',['dispatch_not_held','enable_not_released_by_restore']),
      pool.submit(docs)]
    for task in tasks: task.result()
