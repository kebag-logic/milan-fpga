#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Apply registered plants one at a time to disposable copies of a tree and record which tests fail.

usage: plant_probe.py TREE WORK OUT.json NAME [NAME ...]
For each plant: build acmp_tests with the plant, run the full ACMP suite, list failed tests; when exactly
one test fails, rerun without it to show whether the plant escapes. Uses the pinned GoogleTest from env.
"""
import json, os, shutil, subprocess, sys, xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

tree, work, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
names = sys.argv[4:]
plants = {p['name']: p for p in json.loads((tree / 'tests/mutations.json').read_text())}
tools = os.environ['TOOLS']  # pinned toolchain prefix holding gtest-1.14.0
env = {k: v for k, v in os.environ.items() if not k.startswith('GTEST_')}
env.update(CMAKE_PREFIX_PATH=tools + '/gtest-1.14.0', LD_LIBRARY_PATH=tools + '/gtest-1.14.0/lib')

def run_suite(binary, xml, exclude=None):
    cmd = [str(binary), '--gtest_output=xml:' + str(xml)]
    if exclude:
        cmd.append('--gtest_filter=-' + exclude)
    rc = subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300).returncode
    doc = ET.parse(xml).getroot()
    failed = sorted(c.get('classname') + '.' + c.get('name') for c in doc.iter('testcase') if c.findall('failure'))
    return {'rc': rc, 'tests': int(doc.get('tests')), 'failed': failed}

def one(name):
    p = plants[name]
    d = work / name
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(tree, d / 'tree')
    f = d / 'tree' / p['path']
    text = f.read_text()
    assert text.count(p['old']) == 1, name
    f.write_text(text.replace(p['old'], p['new']))
    subprocess.run(['cmake', '-S', str(d / 'tree'), '-B', str(d / 'build'), '-DCMAKE_BUILD_TYPE=Debug'], env=env,
                   check=True, stdout=subprocess.DEVNULL)
    subprocess.run(['cmake', '--build', str(d / 'build'), '--target', 'acmp_tests', '-j2'], env=env, check=True,
                   stdout=subprocess.DEVNULL)
    full = run_suite(d / 'build/acmp_tests', d / 'full.xml')
    result = {'plant': name, 'full_suite': full}
    if len(full['failed']) == 1:
        result['without_sole_killer'] = run_suite(d / 'build/acmp_tests', d / 'without.xml', full['failed'][0])
    return result

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(one, names))
out.write_text(json.dumps(results, indent=1) + '\n')
for r in results:
    w = r.get('without_sole_killer')
    print(r['plant'], 'failed=', r['full_suite']['failed'], 'escape_without=', None if w is None else (w['rc'] == 0 and not w['failed']))
