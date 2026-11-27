#!/usr/bin/env python3
"""Run both required target jobs in the foreground and retain raw receipts.

Usage: python3 run_gates.py CHECKOUT TOOL_ROOT
TOOL_ROOT supplies clang-18, clang-tidy-18 and gtest-1.14.0 installs.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
tool = Path(sys.argv[2]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
env = dict(os.environ)
env['PATH'] = f'{tool}/clang-18/bin:{tool}/clang-tidy-18/bin:' + env['PATH']
env['PKG_CONFIG_PATH'] = str(tool / 'gtest-1.14.0/lib/pkgconfig')
env['CMAKE_PREFIX_PATH'] = str(tool / 'gtest-1.14.0')
env['LD_LIBRARY_PATH'] = str(tool / 'gtest-1.14.0/lib')
for key in ('CPATH', 'CPLUS_INCLUDE_PATH', 'C_INCLUDE_PATH', 'LIBRARY_PATH'):
    env.pop(key, None)
for key in list(env):
    if key.startswith('GTEST_'):
        env.pop(key)

def run(name, script, extra):
    cmd = [sys.executable, f'scripts/{script}', '--work', str(scratch / name), '--jobs', '3', *extra]
    with (packet / f'{name}.log').open('w') as log:
        result = subprocess.run(cmd, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT)
    (packet / f'{name}.rc').write_text(f'{result.returncode}\n')
    print(f'{name}: rc {result.returncode}', flush=True)
    return {'job': name, 'argv': cmd, 'rc': result.returncode}

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(run, 'quality', 'validate.py', ['--graphs']),
               pool.submit(run, 'rv32', 'baremetal.py', [])]
    results = [f.result() for f in futures]
(packet / 'jobs.json').write_text(json.dumps(results, indent=2) + '\n')
raise SystemExit(any(r['rc'] for r in results))
