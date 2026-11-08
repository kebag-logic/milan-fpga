#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build a disposable copy of the exact head with an optional wire.h substitution and
optional W1 removal, run all eight hosted binaries, and record which tests fail."""
import argparse, json, os, re, subprocess, sys
from pathlib import Path

HEAD = 'c687810b74b53b69c1fbdff7bfd0ec9da94eaa78'
W1 = '\n// REQ: ACMP-02\nTEST(Wire, W1PutBeWritesTheLowBytesMostSignificantFirst) {'

def sh(cmd, log, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log.write(' '.join(map(str, cmd)) + '\n' + r.stdout + '\nrc=' + str(r.returncode) + '\n')
    return r.returncode, r.stdout

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--clone', type=Path, required=True)
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--name', required=True)
    ap.add_argument('--old', default=None)
    ap.add_argument('--new', default=None)
    ap.add_argument('--wire-from', default=None, help='commit whose include/wire.h replaces the head copy')
    ap.add_argument('--drop-w1', action='store_true')
    ap.add_argument('--jobs', type=int, default=4)
    a = ap.parse_args()
    tree = a.work / a.name / 'tree'; build = a.work / a.name / 'build'
    subprocess.run(['rm', '-rf', str(a.work / a.name)], check=True)
    tree.mkdir(parents=True)
    archive = subprocess.run(['git', '-C', str(a.clone), 'archive', HEAD], stdout=subprocess.PIPE, check=True).stdout
    subprocess.run(['tar', '-x', '-C', str(tree)], input=archive, check=True)
    wire = tree / 'include/wire.h'
    if a.wire_from:
        wire.write_bytes(subprocess.run(['git', '-C', str(a.clone), 'show', a.wire_from + ':include/wire.h'],
                                        stdout=subprocess.PIPE, check=True).stdout)
    if a.old is not None:
        text = wire.read_text()
        old = a.old.encode().decode('unicode_escape'); new = a.new.encode().decode('unicode_escape')
        assert text.count(old) == 1, 'substitution must match once'
        wire.write_text(text.replace(old, new))
    if a.drop_w1:
        t = (tree / 'tests/test_acmp.cpp').read_text()
        i = t.index(W1)
        assert t[i:].count('\nTEST') == 1, 'W1 must be the last test'
        (tree / 'tests/test_acmp.cpp').write_text(t[:i] + '\n')
    with open(a.work / a.name / 'run.log', 'w') as log:
        rc, _ = sh(['cmake', '-S', str(tree), '-B', str(build), '-DCMAKE_BUILD_TYPE=Debug',
                    '-DCMAKE_C_COMPILER=gcc', '-DCMAKE_CXX_COMPILER=g++'], log)
        if rc == 0:
            rc, _ = sh(['cmake', '--build', str(build), '-j' + str(a.jobs)], log)
        result = {'name': a.name, 'old': a.old, 'new': a.new, 'wire_from': a.wire_from, 'drop_w1': a.drop_w1,
                  'build_rc': rc}
        if rc == 0:
            rc, out = sh(['ctest', '--test-dir', str(build), '--output-on-failure', '-j' + str(a.jobs)], log)
            result['ctest_rc'] = rc
            result['summary'] = next((l for l in out.splitlines() if 'tests passed' in l), '')
            result['failed_binaries'] = sorted(set(re.findall(r'\d+ - (\w+) \(Failed\)', out)))
            result['failed_tests'] = sorted(set(re.findall(r'\[  FAILED  \] ([\w./]+) \(', out)))
    (a.work / a.name / 'result.json').write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps(result))

if __name__ == '__main__':
    main()
