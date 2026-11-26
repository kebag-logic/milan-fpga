#!/usr/bin/env python3
"""Run independent review checks concurrently; keep every child joined."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('source', type=Path)
p.add_argument('--dependency-prefix', type=Path, required=True)
p.add_argument('--compiler-bin', type=Path, required=True)
a = p.parse_args()
root = a.source.resolve()
packet = Path(__file__).resolve().parent
work = packet / 'scratch'
logs = packet / 'receipts'
logs.mkdir(exist_ok=True)
env = os.environ.copy()
env.update(CMAKE_PREFIX_PATH=str(a.dependency_prefix),
           PKG_CONFIG_PATH=str(a.dependency_prefix / 'lib/pkgconfig'),
           LD_LIBRARY_PATH=str(a.dependency_prefix / 'lib'),
           PATH=str(a.compiler_bin) + os.pathsep + env['PATH'])
for key in list(env):
    if key.startswith('GTEST_'):
        del env[key]
env['PYTHONDONTWRITEBYTECODE'] = '1'
temporary = work / 'temp'
temporary.mkdir(exist_ok=True)
env['TMPDIR'] = str(temporary)

def lane(name, commands):
    rc = 0
    with (logs / (name + '.log')).open('w') as out:
        for cmd in commands:
            out.write('COMMAND ' + ' '.join(map(str, cmd)) + '\n')
            out.flush()
            result = subprocess.run(list(map(str, cmd)), cwd=root, env=env,
                                    stdout=out, stderr=subprocess.STDOUT, timeout=540)
            rc = result.returncode
            out.write('RETURN ' + str(rc) + '\n')
            out.flush()
            if rc:
                break
    (logs / (name + '.rc')).write_text(str(rc) + '\n')
    return name, rc

native = work / 'native'
san = work / 'sanitize'
tasks = {
    'native': [
        ['cmake', '-S', '.', '-B', native, '-DCMAKE_BUILD_TYPE=Debug', '-DTSN_COVERAGE=ON'],
        ['cmake', '--build', native, '-j4'],
        ['ctest', '--test-dir', native, '--output-on-failure', '-j4'],
        ['python3', 'scripts/coverage.py', native]],
    'sanitize': [
        ['cmake', '-S', '.', '-B', san, '-DCMAKE_BUILD_TYPE=Debug', '-DTSN_SANITIZERS=ON', '-DCMAKE_C_COMPILER=clang', '-DCMAKE_CXX_COMPILER=clang++'],
        ['cmake', '--build', san, '--target', 'adp_tests', 'adp_release', 'adp_debug', 'port_tests', '-j4'],
        ['ctest', '--test-dir', san, '-R', 'adp|port', '--output-on-failure', '-j4']],
    'plants': [['python3', 'scripts/mutation.py', '--work', work / 'plants', '--jobs', '4', '--select', 'adp-']],
    'rv32': [['python3', 'scripts/baremetal.py', '--work', work / 'rv32', '--jobs', '2']],
}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = dict(pool.map(lambda pair: lane(*pair), tasks.items()))
(logs / 'checks.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results), flush=True)
raise SystemExit(any(results.values()))
