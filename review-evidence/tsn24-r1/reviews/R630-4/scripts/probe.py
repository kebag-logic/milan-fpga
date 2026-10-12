#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: plant one source edit, run all eight hosted binaries, then
physically remove only the named killer test and run them again.

Usage: probe.py --src TREE --work DIR --plants PLANTS.json [--jobs N] [--per-build J] --out RESULTS.json

PLANTS.json is a list of {"name", "path", "old", "new", "killer"} objects;
"edits": [[old, new], ...] may replace "old"/"new" for several ordered edits.
"killer" may be null (record the full-suite outcome only).
A plant with "path" null is the unplanted control.
"old" must occur exactly once in "path" or the plant is reported ERROR.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BINARIES = ['adp_tests', 'acmp_tests', 'maap_tests', 'entity_tests', 'port_tests',
            'adp_release', 'adp_debug', 'maap_debug']


def run(argv, cwd, log, env=None):
    r = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    log.write(' '.join(map(str, argv)) + '\n' + r.stdout.decode(errors='replace') + f'rc {r.returncode}\n')
    return r.returncode


def suite(build, tag, log):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GTEST_')}
    instances, failures, skipped, missing = 0, [], [], []
    for b in BINARIES:
        xml = build / f'{tag}-{b}.xml'
        if xml.exists():
            xml.unlink()
        run([str(build / b), f'--gtest_output=xml:{xml}'], build, log, env)
        if not xml.exists():
            missing.append(b)
            continue
        for case in ET.parse(xml).getroot().iter('testcase'):
            name = case.get('classname') + '.' + case.get('name')
            if case.get('status') != 'run' or case.get('result') not in (None, 'completed'):
                skipped.append(name)
                continue
            if case.find('skipped') is not None:
                skipped.append(name)
                continue
            instances += 1
            if case.find('failure') is not None:
                failures.append(name)
    return {'instances': instances, 'failures': sorted(set(failures)), 'skipped': skipped, 'missing': missing}


def remove_test(root, killer):
    suite_name, test = killer.split('.', 1)
    pattern = re.compile(r'^(TEST|TEST_F)\(\s*' + re.escape(suite_name) + r'\s*,\s*' + re.escape(test) + r'\s*\)')
    for path in sorted((root / 'tests').glob('test_*.cpp')):
        lines = path.read_text().split('\n')
        for i, line in enumerate(lines):
            if pattern.match(line):
                depth, j, opened = 0, i, False
                while j < len(lines):
                    depth += lines[j].count('{') - lines[j].count('}')
                    opened = opened or '{' in lines[j]
                    if opened and depth == 0:
                        break
                    j += 1
                del lines[i:j + 1]
                path.write_text('\n'.join(lines))
                return str(path.relative_to(root))
    return None


def probe(plant, args):
    name = plant['name']
    base = args.work / name
    shutil.rmtree(base, ignore_errors=True)
    src, build = base / 'src', base / 'build'
    shutil.copytree(args.src, src, ignore=shutil.ignore_patterns('.git'))
    result = {'plant': name, 'killer': plant.get('killer')}
    with (base / 'run.log').open('w') as log:
        if plant.get('path'):
            target = src / plant['path']
            text = target.read_text()
            for old, new in plant.get('edits') or [[plant['old'], plant['new']]]:
                if text.count(old) != 1:
                    result['result'] = 'ERROR'
                    result['why'] = f"old occurs {text.count(old)} times"
                    return result
                text = text.replace(old, new)
            target.write_text(text)
        if run(['cmake', '-S', src, '-B', build, '-DCMAKE_BUILD_TYPE=Debug', '-DCMAKE_C_COMPILER=gcc',
                '-DCMAKE_CXX_COMPILER=g++'], base, log) or run(['cmake', '--build', build, '-j' + str(args.per_build)], base, log):
            result['result'] = 'BUILD-FAILED'
            return result
        full = suite(build, 'full', log)
        result['full'] = full
        if full['missing'] or full['skipped']:
            result['result'] = 'ERROR'
        elif full['failures']:
            result['result'] = 'CAUGHT'
        else:
            result['result'] = 'ESCAPED'
        if plant.get('killer') and result['result'] == 'CAUGHT':
            removed = remove_test(src, plant['killer'])
            result['removed_from'] = removed
            if removed is None or run(['cmake', '--build', build, '-j' + str(args.per_build)], base, log):
                result['escapes'] = None
            else:
                rem = suite(build, 'removed', log)
                result['removed'] = rem
                result['escapes'] = (not rem['failures'] and not rem['missing'] and not rem['skipped']
                                     and rem['instances'] == full['instances'] - 1)
            result['only_killer'] = full['failures'] == [plant['killer']]
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--src', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--plants', type=Path, required=True)
    p.add_argument('--jobs', type=int, default=8)
    p.add_argument('--per-build', type=int, default=2)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    args.src, args.work = args.src.resolve(), args.work.resolve()
    args.work.mkdir(parents=True, exist_ok=True)
    plants = json.loads(args.plants.read_text())
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda pl: probe(pl, args), plants))
    args.out.write_text(json.dumps(results, indent=2) + '\n')
    for r in results:
        print(r['plant'], r['result'], 'full', (r.get('full') or {}).get('failures'),
              'escapes', r.get('escapes'), 'only_killer', r.get('only_killer'))


if __name__ == '__main__':
    raise SystemExit(main())
