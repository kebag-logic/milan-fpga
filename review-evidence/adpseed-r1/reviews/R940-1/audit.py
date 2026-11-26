#!/usr/bin/env python3
"""Check documentation and test sensitivity without changing the source tree."""
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
env = os.environ.copy()
env.update(CMAKE_PREFIX_PATH=str(a.dependency_prefix), PKG_CONFIG_PATH=str(a.dependency_prefix / 'lib/pkgconfig'),
           LD_LIBRARY_PATH=str(a.dependency_prefix / 'lib'), PATH=str(a.compiler_bin) + os.pathsep + env['PATH'],
           PYTHONDONTWRITEBYTECODE='1')
temporary = work / 'temp'
temporary.mkdir(exist_ok=True)
env['TMPDIR'] = str(temporary)

def check(name, commands):
    with (logs / (name + '.log')).open('w') as out:
        for command, expected in commands:
            r = subprocess.run(list(map(str, command)), cwd=root, env=env, stdout=out, stderr=subprocess.STDOUT, timeout=300)
            out.write('RETURN ' + str(r.returncode) + '\n')
            out.flush()
            if r.returncode != expected:
                return name, False
    return name, True

base = work / 'base-adp.c'
base.write_bytes(subprocess.check_output(['git', 'show', 'a795471c0abc4e38f7e5146b4e539dd607b6f501:src/adp.c'], cwd=root))
native = work / 'native'
tasks = {
    'base-sensitivity': [
        (['gcc', '-std=c11', '-DNDEBUG', '-DCTRL_REENTRY_ASSERT', '-Iinclude', '-c', base, '-o', work / 'base-adp.o'], 0),
        (['g++', native / 'CMakeFiles/adp_tests.dir/tests/test_adp.cpp.o', native / 'CMakeFiles/adp_tests.dir/tests/main.cpp.o', work / 'base-adp.o', a.dependency_prefix / 'lib/libgmock.a', a.dependency_prefix / 'lib/libgtest.a', '-o', work / 'base-tests'], 0),
        ([work / 'base-tests', '--gtest_filter=AdpCore.A30*:AdpCore.A31*', '--gtest_output=xml:' + str(logs / 'base-sensitivity.xml')], 1),
        ([work / 'base-tests', '--gtest_filter=AdpCore.A29*'], 0)],
    'docs-audit': [(['python3', 'scripts/' + name] + (['--build', native, '--jobs', '16'] if name in ('traceability.py', 'test_inventory.py') else []), 0) for name in ['traceability.py', 'test_inventory.py', 'check_comments.py', 'check_port_contracts.py', 'needle_audit.py']],
}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    result = dict(pool.map(lambda pair: check(*pair), tasks.items()))
(logs / 'audit.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
raise SystemExit(not all(result.values()))
