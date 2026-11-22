#!/usr/bin/env python3
"""Focused independent review. All builds and plants live under packet/scratch.

Usage: python3 run_review.py REPO PACKET GTEST_PREFIX CLANG18
Requires cmake, Ninja, GCC, Clang, GoogleTest/GMock 1.14.0 and Clang 18 lexer.
Runs child processes synchronously; independent tasks share a bounded executor.
"""
import concurrent.futures as cf
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess as sp
import sys
import xml.etree.ElementTree as ET

repo, packet, prefix, lexer = map(lambda p: Path(p).resolve(), sys.argv[1:5])
selected = set(sys.argv[5:])
work = packet / 'scratch'
env = dict(os.environ, CMAKE_PREFIX_PATH=str(prefix),
           PKG_CONFIG_PATH=str(prefix / 'lib/pkgconfig'), TSN_CLANG=str(lexer),
           PYTHONDONTWRITEBYTECODE='1', ASAN_OPTIONS='detect_leaks=1:halt_on_error=1',
           UBSAN_OPTIONS='halt_on_error=1:print_stacktrace=1')
for key in list(env):
    if key.startswith('GTEST_') or key in ('CPATH', 'CPLUS_INCLUDE_PATH', 'C_INCLUDE_PATH', 'LIBRARY_PATH'):
        del env[key]

def run(name, command, expected=0):
    command = list(map(str, command))
    with (packet / (name + '.log')).open('w') as log:
        log.write('$ ' + shlex.join(command) + '\n')
        log.flush()
        rc = sp.run(command, cwd=repo, env=env, stdout=log, stderr=sp.STDOUT, timeout=540).returncode
    (packet / (name + '.rc')).write_text(str(rc) + '\n')
    if rc != expected:
        raise RuntimeError(f'{name}: rc {rc}, expected {expected}')
    return rc

def hosted():
    build = work / 'gcc'
    run('gcc-configure', ['cmake', '-G', 'Ninja', '-S', repo, '-B', build, '-DCMAKE_BUILD_TYPE=Debug', '-DTSN_COVERAGE=ON'])
    run('gcc-build', ['cmake', '--build', build, '-j8'])
    run('gcc-test', ['ctest', '--test-dir', build, '--output-on-failure', '-j8'])
    run('coverage', ['python3', 'scripts/coverage.py', build])

def sanitized():
    build = work / 'sanitize'
    run('sanitize-configure', ['cmake', '-G', 'Ninja', '-S', repo, '-B', build, '-DCMAKE_BUILD_TYPE=Debug', '-DCMAKE_C_COMPILER=clang', '-DCMAKE_CXX_COMPILER=clang++', '-DTSN_SANITIZERS=ON'])
    run('sanitize-build', ['cmake', '--build', build, '--target', 'adp_tests', 'adp_debug', 'adp_release', '-j4'])
    run('sanitize-adp', ['ctest', '--test-dir', build, '-R', '^adp_', '--output-on-failure', '-j3'])

def registered_plant():
    build = work / 'mutation'
    run('registered-plant', ['python3', 'scripts/mutation.py', '--work', build, '--jobs', '2', '--select', 'gm-change-draws-startup-kind'])
    out = packet / 'registered-plant'
    out.mkdir(exist_ok=True)
    for path in build.rglob('*'):
        if path.is_file() and path.suffix in ('.log', '.xml', '.json'):
            target = out / path.relative_to(build)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)

def sensitivity():
    build = work / 'sensitivity'
    build.mkdir(exist_ok=True)
    rows = json.loads((repo / 'tests/mutations.json').read_text())
    plant = next(r for r in rows if r['name'] == 'gm-change-draws-startup-kind')
    src = (repo / plant['path']).read_text()
    assert src.count(plant['old']) == 1
    (build / 'mutant.c').write_text(src.replace(plant['old'], plant['new']))
    (packet / 'plant.json').write_text(json.dumps(plant, indent=2) + '\n')
    raw_flags = shlex.split(sp.check_output(['pkg-config', '--cflags', '--libs', 'gmock', 'gtest'], env=env, text=True))
    flags = []
    for flag in raw_flags:
        flags.extend(['-isystem', flag[2:]] if flag.startswith('-I') else [flag])
    run('probe-core-build', ['gcc', '-std=c11', '-O0', '-g', '-Wall', '-Wextra', '-Werror', '-DNDEBUG', '-DCTRL_REENTRY_ASSERT', '-I', repo / 'include', '-c', build / 'mutant.c', '-o', build / 'mutant.o'])
    for label, ref, expected in [('base', '715589c1', 0), ('head', '61a504e', 1)]:
        source = sp.check_output(['git', 'show', ref + ':tests/test_adp.cpp'], cwd=repo)
        (build / (label + '.cpp')).write_bytes(source)
        run('probe-' + label + '-build', ['g++', '-std=c++20', '-O0', '-g', '-Wall', '-Wextra', '-Werror', '-I', repo / 'include', build / (label + '.cpp'), repo / 'tests/main.cpp', build / 'mutant.o', *flags, '-o', build / label])
        xml = packet / ('probe-' + label + '.xml')
        run('probe-' + label, [build / label, '--gtest_output=xml:' + str(xml)], expected)
        cases = list(ET.parse(xml).getroot().iter('testcase'))
        assert cases and all(c.get('status') == 'run' and c.get('result') == 'completed' for c in cases)
        failures = [c for c in cases if c.findall('failure')]
        if label == 'head':
            assert len(failures) == 1
            assert failures[0].get('name') == 'A0toA2Schedule'
            assert plant['kills'][0]['needle'] in ET.tostring(failures[0], encoding='unicode')
        else:
            assert not failures

with cf.ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(f): f.__name__ for f in (hosted, sanitized, registered_plant, sensitivity)
               if not selected or f.__name__ in selected}
    failures = []
    for future in cf.as_completed(futures):
        try:
            future.result()
            print(futures[future] + ': PASS', flush=True)
        except Exception as error:
            failures.append(str(error))
            print(futures[future] + ': FAIL ' + str(error), flush=True)
    if failures:
        raise SystemExit('\n'.join(failures))

for name, command in [
    ('traceability', ['python3', 'scripts/traceability.py', '--selftest', '--build', work / 'gcc', '--jobs', '16']),
    ('test-inventory', ['python3', 'scripts/test_inventory.py', '--build', work / 'gcc', '--jobs', '16']),
    ('needles', ['python3', 'scripts/needle_audit.py', '--selftest']),
    ('comments', ['python3', 'scripts/check_comments.py']),
    ('license', ['python3', 'scripts/check_license.py']),
    ('privacy', ['python3', 'scripts/check_privacy.py'])]:
    run(name, command)
    print(name + ': PASS', flush=True)
print('Focused independent review checks: PASS', flush=True)
