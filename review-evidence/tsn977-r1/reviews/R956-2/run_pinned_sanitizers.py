#!/usr/bin/env python3
"""Supplement the complete host job with Clang 18 sanitizer execution.

Usage: run_pinned_sanitizers.py CHECKOUT TOOL_ROOT
"""
import json
import os
from pathlib import Path
import subprocess
import sys
p = Path(__file__).resolve().parent
root = Path(sys.argv[1]).resolve()
tools = Path(sys.argv[2]).resolve()
build = p/'scratch/clang18-sanitizers'
env = dict(os.environ)
env['CMAKE_PREFIX_PATH'] = str(tools/'gtest-1.14.0')
env['LD_LIBRARY_PATH'] = str(tools/'gtest-1.14.0/lib')
env['ASAN_OPTIONS'] = 'detect_leaks=1:halt_on_error=1'
env['UBSAN_OPTIONS'] = 'halt_on_error=1'
for key in list(env):
    if key.startswith('GTEST_') or key in ('CPATH','CPLUS_INCLUDE_PATH','C_INCLUDE_PATH','LIBRARY_PATH'):
        env.pop(key)
commands=[['cmake','-S',str(root),'-B',str(build),'-DCMAKE_BUILD_TYPE=Debug','-DTSN_SANITIZERS=ON',
           '-DCMAKE_C_COMPILER='+str(tools/'clang-18/bin/clang-18'),
           '-DCMAKE_CXX_COMPILER='+str(tools/'clang-18/bin/clang-18'),'-DCMAKE_CXX_COMPILER_ARG1=--driver-mode=g++'],
          ['cmake','--build',str(build),'-j16'],
          ['ctest','--test-dir',str(build),'--output-on-failure','-j16']]
results=[]
for name,cmd in zip(('configure','build','test'),commands):
    with (p/f'clang18-{name}.log').open('w') as log:
        rc=subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    results.append({'stage':name,'rc':rc})
    print(name,rc,flush=True)
    if rc: break
(p/'clang18-results.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(any(r['rc'] for r in results))
