#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Physically delete a named AcmpFresh test, apply its registered plant, run the full suite.

usage: physical_removal.py --tree <exported head tree> --work <dir> --plants a,b,c
"""
import argparse
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
import subprocess


def one(tree, work, env, m):
    name, killer = m['name'], m['kills'][0]['test']
    out = work / name
    if out.exists():
        shutil.rmtree(out)
    copy = out / 'tree'
    shutil.copytree(tree, copy)
    src = (copy / m['path']).read_text()
    assert src.count(m['old']) == 1
    (copy / m['path']).write_text(src.replace(m['old'], m['new']))
    suite, test = killer.split('.')
    tf = copy / 'tests/test_acmp.cpp'
    text = tf.read_text()
    start = text.index(f'TEST_F({suite}, {test})')
    start = text.rindex('// REQ:', 0, start)
    stop = re.compile(r'^}\n', re.M).search(text, start).end()
    tf.write_text(text[:start] + text[stop:])
    log = out / 'run.log'
    with open(log, 'w') as f:
        rc = subprocess.run(['cmake', '-S', str(copy), '-B', str(out / 'b'), '-DCMAKE_BUILD_TYPE=Debug'], stdout=f, stderr=subprocess.STDOUT, env=env).returncode
        rc = rc or subprocess.run(['cmake', '--build', str(out / 'b'), '-j2'], stdout=f, stderr=subprocess.STDOUT, env=env).returncode
        build_rc = rc
        rc = rc or subprocess.run(['ctest', '--test-dir', str(out / 'b'), '--output-on-failure', '-j2'], stdout=f, stderr=subprocess.STDOUT, env=env).returncode
    body = log.read_text()
    failing = sorted(set(re.findall(r'^\[  FAILED  \] (\w+\.\w+) \(', body, re.M)))
    return {'plant': name, 'removed_test': killer, 'removed_present_after': f'TEST_F({suite}, {test})' in tf.read_text(),
            'build_rc': build_rc, 'suite_rc': rc, 'escapes': rc == 0, 'still_failing_tests': failing}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tree', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--plants', required=True)
    a = p.parse_args()
    env = {k: v for k, v in os.environ.items() if not k.startswith('GTEST_')}
    wanted = a.plants.split(',')
    plants = [m for m in json.loads((a.tree / 'tests/mutations.json').read_text()) if m['name'] in wanted]
    a.work.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda m: one(a.tree.resolve(), a.work.resolve(), env, m), plants))
    (a.work / 'physical-removal.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=1))


if __name__ == '__main__':
    main()
