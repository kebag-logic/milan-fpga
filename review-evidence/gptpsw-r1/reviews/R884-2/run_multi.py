#!/usr/bin/env python3
"""Reproduce stale asCapable with multiple responders and absent Follow_Up."""
from pathlib import Path
import subprocess, sys
P=Path(__file__).resolve().parent; R=Path(sys.argv[1]).resolve(); S=P/'scratch'
S.mkdir(exist_ok=True)
src=S/'multi.cpp'; obj=S/'multi-core.o'; exe=S/'multi'
src.write_text('#include "'+str(R/'sw/firmware/ctrl/test/test_gptp.cpp')+'"\n'+(P/'probe_multi.inc').read_text())
flags=['-fsanitize=undefined','-fno-sanitize-recover=undefined']
commands=[
 ['gcc','-std=c11','-O2',*flags,'-c',str(R/'sw/firmware/ctrl/gptp/gptp.c'),'-o',str(obj)],
 ['g++','-std=c++20','-O1',*flags,'-I'+str(R/'sw/firmware/ctrl/gptp'),'-I'+str(R/'sw/firmware/gtest'),str(src),str(obj),'-lgtest_main','-lgtest','-lpthread','-o',str(exe)]
]
with (P/'multi-build.log').open('w') as f:
    for cmd in commands:
        f.write(repr(cmd)+'\n');f.flush();subprocess.run(cmd,check=True,stdout=f,stderr=subprocess.STDOUT)
with (P/'multi.log').open('w') as f:
    result=subprocess.run([str(exe),'--gtest_filter=Scripted.MultipleResponses*'],stdout=f,stderr=subprocess.STDOUT)
(P/'multi.rc').write_text(str(result.returncode)+'\n')
print((P/'multi.log').read_text())
sys.exit(result.returncode)
