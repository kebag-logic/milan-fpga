#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Physical-removal check for the generated-entity freshness plant.

usage: entity_removal.py --tree <exported head tree> --work <dir>

physical_removal.py only edits tests/test_acmp.cpp. This companion applies the
registered dafresh-generated-window plant and runs the complete hosted suite
(all test binaries) twice: with EntityYaml.DaFreshRoundTrip present (must fail
in that test with its needle) and with that TEST block physically deleted from
tests/test_entity.cpp (must pass). It also runs the unplanted head as a control
and counts completed test instances in each run.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

NAME = 'dafresh-generated-window'


def run(tree, work, env, variant, plant, remove):
    out = work / variant
    if out.exists():
        shutil.rmtree(out)
    copy = out / 'tree'
    shutil.copytree(tree, copy)
    m = next(x for x in json.loads((copy / 'tests/mutations.json').read_text()) if x['name'] == NAME)
    if plant:
        text = (copy / m['path']).read_text()
        assert text.count(m['old']) == 1
        (copy / m['path']).write_text(text.replace(m['old'], m['new']))
    tf = copy / 'tests/test_entity.cpp'
    if remove:
        text = tf.read_text()
        start = text.rindex('// REQ:', 0, text.index('TEST(EntityYaml, DaFreshRoundTrip)'))
        stop = re.compile(r'^}\n', re.M).search(text, text.index('TEST(EntityYaml, DaFreshRoundTrip)')).end()
        tf.write_text(text[:start] + text[stop:])
    log = out / 'run.log'
    with open(log, 'w') as f:
        rc = subprocess.run(['cmake', '-S', str(copy), '-B', str(out / 'b'), '-DCMAKE_BUILD_TYPE=Debug'],
                            stdout=f, stderr=subprocess.STDOUT, env=env).returncode
        rc = rc or subprocess.run(['cmake', '--build', str(out / 'b'), '-j4'], stdout=f, stderr=subprocess.STDOUT, env=env).returncode
        build_rc = rc
        rc = rc or subprocess.run(['ctest', '--test-dir', str(out / 'b'), '--output-on-failure', '-V'],
                                  stdout=f, stderr=subprocess.STDOUT, env=env).returncode
    body = log.read_text()
    ran = sum(int(n) for n in re.findall(r'^\d+: \[==========\] (\d+) tests? from \d+ test suites? ran', body, re.M))
    binaries = len(re.findall(r'^\d+: \[==========\] \d+ tests? from \d+ test suites? ran', body, re.M))
    failing = sorted(set(re.findall(r'^\d+: \[  FAILED  \] (\w+\.\w+) \(', body, re.M)))
    return {'variant': variant, 'plant_applied': plant, 'killer_removed': remove,
            'killer_present_after': 'TEST(EntityYaml, DaFreshRoundTrip)' in tf.read_text(),
            'build_rc': build_rc, 'suite_rc': rc, 'binaries_completed': binaries, 'test_instances_ran': ran,
            'failing_tests': failing, 'needle_seen': m['kills'][0]['needle'] in body}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tree', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    a = p.parse_args()
    env = {k: v for k, v in os.environ.items() if not k.startswith('GTEST_')}
    a.work.mkdir(parents=True, exist_ok=True)
    variants = [('control', False, False), ('plant-killer-present', True, False), ('plant-killer-removed', True, True)]
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda v: run(a.tree.resolve(), a.work.resolve(), env, *v), variants))
    (a.work / 'entity-removal.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=1))


if __name__ == '__main__':
    main()
