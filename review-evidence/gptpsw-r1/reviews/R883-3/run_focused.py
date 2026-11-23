#!/usr/bin/env python3
"""Focused review checks; usage: python3 -B run_focused.py CHECKOUT. All builds stay in packet/scratch."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, sys, re, os
P=Path(__file__).resolve().parent; R=Path(sys.argv[1]).resolve(); S=P/'scratch'
S.mkdir(exist_ok=True)
def run(name, cmd):
    with (P/(name+'.log')).open('w') as f:
        f.write(repr(cmd)+'\n'); f.flush()
        rc=subprocess.run(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT).returncode
    (P/(name+'.rc')).write_text(str(rc)+'\n')
    return name,rc
def core():
    src=S/'steps.cpp'; obj=S/'steps-core.o'; exe=S/'steps'
    src.write_text('#include "'+str(R/'sw/firmware/ctrl/test/test_gptp.cpp')+'"\n'+(P/'probe_midstep_sweep.inc').read_text()+(P/'probe_matrix_ext.inc').read_text())
    flags=['-fsanitize=undefined','-fno-sanitize-recover=undefined']
    for name,cmd in [('step-core-build',['gcc','-std=c11','-O2',*flags,'-c',str(R/'sw/firmware/ctrl/gptp/gptp.c'),'-o',str(obj)]),('step-suite-build',['g++','-std=c++20','-O1',*flags,'-I'+str(R/'sw/firmware/ctrl/gptp'),'-I'+str(R/'sw/firmware/gtest'),str(src),str(obj),'-lgtest_main','-lgtest','-lpthread','-o',str(exe)]),('steps',[str(exe)])]:
        n,rc=run(name,cmd)
        if rc: return n,rc
    text=(P/'steps.log').read_text()
    rows=re.findall(r'A_asCapable_down_ms=(\d+) B_asCapable_down_ms=(\d+)',text)
    assert len(rows)==144 and all(a=='0' and b=='0' for a,b in rows), rows
    return 'steps and 144 outage assertions',0
with ThreadPoolExecutor(max_workers=3) as pool:
    fs=[pool.submit(core),pool.submit(run,'multi-driver',[sys.executable,'-B',str(P/'run_multi.py'),str(R)]),pool.submit(run,'hot-plants',[sys.executable,'-B',str(R/'sw/firmware/ctrl/test/ctrl_hot.py'),'--self-test'])]
    results=[f.result() for f in fs]
print(results)
sys.exit(any(rc for _,rc in results))
