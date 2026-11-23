#!/usr/bin/env python3
"""Run review checks in foreground-owned workers.

Usage: python3 reproduce.py CHECKOUT PACKET
Set PATH for required compilers and CMAKE_PREFIX_PATH/PKG_CONFIG_PATH for
GoogleTest 1.14.0 first. All disposable output stays under PACKET/scratch.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import subprocess as sp
import sys

repo, packet = (Path(p).resolve() for p in sys.argv[1:])
scratch=packet/'scratch'
scratch.mkdir(parents=True,exist_ok=True)
def run(name,args):
    with (scratch/(name+'.log')).open('w') as log:
        p=sp.run(args,cwd=repo,stdout=log,stderr=sp.STDOUT,timeout=3600)
    (scratch/(name+'.rc')).write_text(str(p.returncode)+'\n')
    if p.returncode: raise RuntimeError(name+' failed: see scratch log')
    return p.returncode
python=sys.executable
# The validator has at most four workers using two slots each; RV32 uses
# two workers with two slots each; the focused probe uses four slots.
with ThreadPoolExecutor(max_workers=3) as pool:
    tasks=[pool.submit(run,'validate',[python,'scripts/validate.py','--work',str(scratch/'validate'),'--jobs','2','--graphs']),
           pool.submit(run,'baremetal',[python,'scripts/baremetal.py','--work',str(scratch/'baremetal'),'--jobs','2']),
           pool.submit(run,'probe',[python,str(packet/'probe.py'),str(repo),str(packet)])]
    for t in tasks: t.result()
old=scratch/'probe/old-Debug-gm-change-rearms-without-a-draw'
build=scratch/'old-full'
run('old-configure',['cmake','-S',str(old),'-B',str(build),'-DCMAKE_BUILD_TYPE=Debug'])
run('old-build',['make','-C',str(build),'-j16'])
run('old-ctest',['ctest','--test-dir',str(build),'--output-on-failure','-j16'])
run('integrity',[python,str(packet/'audit.py'),str(repo)])
