#!/usr/bin/env python3
"""Run the pinned library suites in an external build directory."""
import pathlib,sys,subprocess,os
root=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(__file__).resolve().parents[1];work=p/'scratch/upstream';env=os.environ.copy()
for cmd in [['cmake','-S',str(root/'third_party/lwSRP'),'-B',str(work),'-DCGREEN_LIB='+str(p/'scratch/cgreen-build/src/libcgreen.so'),'-DCGREEN_INCLUDE='+str(p/'scratch/cgreen-src/include')],['make','-C',str(work),'-j16'],[str(work/'unit_tests')]]:
 print('RUN',cmd,flush=True);subprocess.run(cmd,env=env,check=True)
env['SHLAN_LIBRARY']=str(work/'libshlan.so')
subprocess.run([sys.executable,'-m','behave',str(root/'third_party/lwSRP/tests/features')],env=env,check=True)
