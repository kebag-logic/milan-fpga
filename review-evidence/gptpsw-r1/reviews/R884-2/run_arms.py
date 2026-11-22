#!/usr/bin/env python3
"""Run normal/UBSan core arms and the original six-case outage matrix."""
from pathlib import Path
import sys, subprocess
sys.dont_write_bytecode=True
R=Path(sys.argv[1]).resolve()
P=Path(__file__).resolve().parent
S=P/'scratch'
sys.path.insert(0,str(R/'sw/firmware/ctrl/test'))
from ctrl_build import Tree
import fw_gtest, gptp_arms
t=Tree(R/'sw/firmware/ctrl',S/'arms',S/'reuse',fw_gtest.Build(jobs=1))
bad=False
for fn in [gptp_arms.arm_gptp,gptp_arms.arm_gptp_ubsan]:
    o=fn(t); print(o.log,flush=True); bad |= o.rc!=0
# Include the current Net fixture unchanged, then the public prior outage probe.
src=S/'outage.cpp'
src.write_text('#include "'+str(R/'sw/firmware/ctrl/test/test_gptp.cpp')+'"\n'+(P/'probe_outage.inc').read_text())
obj=S/'outage-core.o'; exe=S/'outage'
flags=['-fsanitize=undefined','-fno-sanitize-recover=undefined']
subprocess.run(['gcc','-std=c11','-O2',*flags,'-c',str(R/'sw/firmware/ctrl/gptp/gptp.c'),'-o',str(obj)],check=True)
subprocess.run(['g++','-std=c++20','-O1',*flags,'-I'+str(R/'sw/firmware/ctrl/gptp'),'-I'+str(R/'sw/firmware/gtest'),str(src),str(obj),'-lgtest_main','-lgtest','-lpthread','-o',str(exe)],check=True)
result=subprocess.run([str(exe),'--gtest_filter=Net.Outage*'],capture_output=True,text=True)
print(result.stdout,flush=True); print(result.stderr,flush=True)
lines=[l for l in result.stdout.splitlines() if l.startswith('[OUTAGE]')]
bad |= result.returncode!=0 or len(lines)!=6 or any('A 0 ms, B 0 ms;' not in l for l in lines)
print('OUTAGE MATRIX:', 'FAIL' if bad else 'PASS')
sys.exit(bad)
