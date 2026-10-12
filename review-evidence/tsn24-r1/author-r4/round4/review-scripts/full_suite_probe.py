#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: grade source plants against the COMPLETE hosted suite.

For every plant the probe copies the exact-head tree, applies the plant, builds
all eight hosted GoogleTest binaries through the repository CMake project, runs
each binary with XML output and records every failing test, its message and the
completed instance count.

Modes per plant:
  full     plant applied, every test present: records the failing set.
  removed  plant applied AND the named killer physically deleted from its test
           source: the suite must complete with no failure (escape).
  control  no plant: the unmodified suite must pass (baseline).

Usage:
  full_suite_probe.py --repo R --work W --plants P.json --jobs N --out OUT.json
P.json is a list of {"name", "path", "old", "new", "killer", "needle", "modes"}.
"old" must occur exactly once. Requires GoogleTest 1.14.0 discoverable by CMake.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import tarfile
import io
import time
import xml.etree.ElementTree as ET
from pathlib import Path


def fresh(path):
    # Restored or planted files must look newer than every object built from
    # an earlier plant; preserved timestamps would let make skip the rebuild.
    t = time.time() + 2.0
    os.utime(path, (t, t))

BINARIES = ['adp_tests', 'acmp_tests', 'maap_tests', 'entity_tests', 'port_tests',
            'adp_release', 'adp_debug', 'maap_debug']
TEST_FILES = ['tests/test_acmp.cpp', 'tests/test_entity.cpp', 'tests/test_adp.cpp',
              'tests/test_maap.cpp', 'tests/test_port.cpp', 'tests/test_adp_reentry.cpp',
              'tests/test_maap_debug.cpp']


def sh(cmd, cwd=None, timeout=1800):
    r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, timeout=timeout)
    return r.returncode, r.stdout


def export(repo, rev, dest):
    data = subprocess.run(['git', '-C', repo, 'archive', rev], check=True,
                          stdout=subprocess.PIPE).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        t.extractall(dest, filter='data')


def remove_test(text, killer):
    fixture, name = killer.split('.')
    pat = re.compile(r'^(?:// REQ:[^\n]*\n)?TEST(?:_F)?\(\s*' + re.escape(fixture) + r'\s*,\s*' +
                     re.escape(name) + r'\s*\)\s*\{', re.M)
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError('killer not found exactly once: ' + killer)
    m = matches[0]
    depth = 0
    i = text.index('{', m.end() - 1)
    while True:
        c = text[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                break
        i += 1
    return text[:m.start()] + text[i + 1:].lstrip('\n')


def run_suite(build, tag):
    results = {'tests': 0, 'failures': [], 'skipped': 0, 'disabled': 0, 'binaries': {}}
    for b in BINARIES:
        xml = build / (tag + '-' + b + '.xml')
        xml.unlink(missing_ok=True)
        env = dict(os.environ)
        env.pop('GTEST_FILTER', None)
        rc, out = sh([str(build / b), '--gtest_output=xml:' + str(xml)], timeout=600)
        if not xml.exists():
            results['binaries'][b] = {'rc': rc, 'xml': False}
            results['failures'].append({'test': b + '.<no-xml>', 'message': out[-400:]})
            continue
        root = ET.parse(xml).getroot()
        n = 0
        for case in root.iter('testcase'):
            if case.get('result', 'completed') != 'completed' or case.get('status') == 'notrun':
                results['skipped'] += 1
                continue
            if case.find('skipped') is not None:
                results['skipped'] += 1
                continue
            n += 1
            fails = case.findall('failure')
            if fails:
                results['failures'].append({'test': case.get('classname') + '.' + case.get('name'),
                                            'binary': b,
                                            'message': '\n'.join(f.get('message', '') for f in fails)})
        results['tests'] += n
        results['disabled'] += int(root.get('disabled', '0'))
        results['binaries'][b] = {'rc': rc, 'xml': True, 'completed': n}
    return results


def worker(args, idx, jobs):
    root = Path(args.work) / ('w%d' % idx)
    pristine = root / 'pristine'
    src = root / 'src'
    build = root / 'build'
    if not pristine.exists():
        export(args.repo, args.rev, pristine)
    if src.exists():
        shutil.rmtree(src)
    shutil.copytree(pristine, src)
    rc, out = sh(['cmake', '-S', str(src), '-B', str(build), '-DCMAKE_BUILD_TYPE=Debug'])
    if rc:
        raise RuntimeError(out)
    out_rows = []
    for plant, mode in jobs:
        touched = set()
        try:
            if plant is not None:
                f = src / plant['path']
                text = f.read_text()
                if text.count(plant['old']) != 1:
                    raise RuntimeError('plant old text not found exactly once: ' + plant['name'])
                f.write_text(text.replace(plant['old'], plant['new']))
                fresh(f)
                touched.add(plant['path'])
            if mode == 'removed':
                killer = plant['killer']
                done = False
                for tf in TEST_FILES:
                    t = (src / tf).read_text()
                    fx, nm = killer.split('.')
                    if re.search(r'TEST(?:_F)?\(\s*' + re.escape(fx) + r'\s*,\s*' + re.escape(nm) + r'\s*\)', t):
                        (src / tf).write_text(remove_test(t, killer))
                        fresh(src / tf)
                        touched.add(tf)
                        done = True
                        break
                if not done:
                    raise RuntimeError('killer source not found: ' + killer)
            rc, out = sh(['cmake', '--build', str(build), '-j1'])
            if rc:
                row = {'plant': plant and plant['name'], 'mode': mode, 'build_rc': rc,
                       'build_tail': out[-1500:]}
            else:
                tag = (plant['name'] if plant else 'control') + '-' + mode
                res = run_suite(build, tag)
                row = {'plant': plant and plant['name'], 'mode': mode, 'build_rc': 0, **res}
                if plant is not None:
                    row['killer'] = plant.get('killer')
                    failing = sorted({x['test'] for x in res['failures']})
                    row['failing_set'] = failing
                    if mode == 'full':
                        row['caught'] = bool(failing)
                        row['only_killer'] = failing == [plant.get('killer')]
                        row['needle_seen'] = any(plant.get('needle', '\0') in x['message']
                                                 for x in res['failures'] if x['test'] == plant.get('killer'))
                    else:
                        row['escapes'] = not failing and res['skipped'] == 0
        finally:
            for p in touched:
                shutil.copyfile(pristine / p, src / p)
                fresh(src / p)
        out_rows.append(row)
        print(json.dumps({k: row.get(k) for k in ('plant', 'mode', 'build_rc', 'tests', 'failing_set',
                                                   'caught', 'only_killer', 'needle_seen', 'escapes')}),
              flush=True)
    return out_rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--rev', default='HEAD')
    ap.add_argument('--work', required=True)
    ap.add_argument('--plants', required=True)
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--control', action='store_true')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    plants = json.load(open(a.plants))
    jobs = [(None, 'control')] if a.control else []
    for p in plants:
        for mode in p.get('modes', ['full']):
            jobs.append((p, mode))
    buckets = [jobs[i::a.jobs] for i in range(a.jobs)]
    rows = []
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for r in ex.map(lambda ij: worker(a, ij[0], ij[1]), enumerate(buckets)):
            rows.extend(r)
    Path(a.out).write_text(json.dumps(rows, indent=1) + '\n')


if __name__ == '__main__':
    main()
