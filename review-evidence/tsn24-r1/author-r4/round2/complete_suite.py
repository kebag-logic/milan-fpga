#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Grade complete-suite kills and individual physical-removal escapes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET


def command(argv, log, env):
    with log.open('w') as stream:
        rc = subprocess.run(argv, env=env, stdout=stream, stderr=subprocess.STDOUT).returncode
    log.with_suffix('.rc').write_text(str(rc) + '\n')
    return rc


def suite(build, out, env):
    out.mkdir(parents=True, exist_ok=True)
    reports = out / 'xml'
    if reports.exists():
        shutil.rmtree(reports)
    reports.mkdir()
    rc = command(['ctest', '--test-dir', str(build), '--output-on-failure', '-j16'],
                 out / 'suite.log', dict(env, GTEST_OUTPUT='xml:' + str(reports) + '/'))
    paths = sorted(reports.glob('*.xml'))
    assert len(paths) == 8, paths
    names, failures = set(), {}
    for path in paths:
        root = ET.parse(path).getroot()
        assert root.tag == 'testsuites' and int(root.get('errors', '0')) == 0
        assert int(root.get('disabled', '0')) == 0
        cases = root.findall('.//testcase')
        assert int(root.get('tests')) == len(cases)
        for case in cases:
            name = case.get('classname') + '.' + case.get('name')
            key = (path.stem, name)
            assert key not in names and case.get('status') == 'run' and case.get('result') == 'completed'
            assert case.find('skipped') is None
            names.add(key)
            failed = case.findall('failure')
            if failed:
                failures[name] = '\n'.join(f.get('message', '') + (f.text or '') for f in failed)
    return rc, names, failures


def remove(text, killer):
    owner, name = killer.split('.')
    pattern = r'TEST(?:_F)?\(\s*' + re.escape(owner) + r'\s*,\s*' + re.escape(name) + r'\s*\)\s*\{'
    hits = list(re.finditer(pattern, text))
    assert len(hits) == 1
    start = text.rindex('// REQ:', 0, hits[0].start())
    stop = re.compile(r'^}\n', re.M).search(text, hits[0].end()).end()
    return text[:start] + text[stop:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    work = args.work.resolve()
    tree = work / 'tree'
    out = work / 'complete-suite'
    out.mkdir(exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith('GTEST_')}
    baseline_rc, baseline, failures = suite(work / 'gcc', out / 'baseline', env)
    assert baseline_rc == 0 and not failures
    plants = [p for p in json.loads((tree / 'tests/mutations.json').read_text())
              if p['name'].startswith('dafresh-') or p['name'] == 'x-zero-never-expires']
    physical = {}
    for path in sorted(work.glob('physical-*/physical-removal.json')):
        for row in json.loads(path.read_text()):
            assert row['plant'] not in physical
            assert row['escapes'] and row['build_rc'] == 0 and row['suite_rc'] == 0
            assert not row['removed_present_after'] and not row['still_failing_tests']
            physical[row['plant']] = path.parent / row['plant']
    probe = json.loads((work / 'escape/escape-probe.json').read_text())
    registered = [r for r in probe if 'killer' in r]
    assert len(registered) == len(plants) - 1
    assert all(r['escapes_without_killer'] and r['killer_fails_with_needle'] for r in registered)
    assert next(r for r in probe if r['plant'] == 'x-zero-never-expires')['result'] == 'CAUGHT'

    def check(plant):
        name = plant['name']
        killer = plant['kills'][0]['test']
        target = 'tests/test_entity.cpp' if killer.startswith('EntityYaml.') else 'tests/test_acmp.cpp'
        directory = out / name
        original = (tree / plant['path']).read_text()
        expected = original.replace(plant['old'], plant['new'])
        assert original.count(plant['old']) == 1
        planted = work / 'escape' / name
        assert (planted / 'tree' / plant['path']).read_text() == expected
        full_rc, names, failures = suite(planted / 'build', directory / 'full', env)
        assert full_rc == 8 and names == baseline, (name, full_rc, len(names))
        assert set(failures) == {killer}, (name, sorted(failures))
        assert plant['kills'][0]['needle'] in failures[killer]
        if name in physical:
            removed = physical[name]
            build = removed / 'b'
        else:
            assert name == 'dafresh-generated-window'
            removed = work / 'physical-entity' / name
            copy = removed / 'tree'
            if copy.exists():
                shutil.rmtree(copy)
            shutil.copytree(planted / 'tree', copy)
            (copy / target).write_text(remove((copy / target).read_text(), killer))
            build = removed / 'b'
            assert command(['cmake', '-S', str(copy), '-B', str(build), '-DCMAKE_BUILD_TYPE=Debug'],
                           removed / 'configure.log', env) == 0
            assert command(['cmake', '--build', str(build), '-j16'], removed / 'build.log', env) == 0
        assert (removed / 'tree' / plant['path']).read_text() == expected
        assert (removed / 'tree' / target).read_text() == remove((tree / target).read_text(), killer)
        removed_rc, remaining, failures = suite(build, directory / 'removed', env)
        expected_names = {key for key in baseline if key[1] != killer}
        assert len(expected_names) == len(baseline) - 1
        assert removed_rc == 0 and remaining == expected_names and not failures
        row = dict(plant=name, killer=killer, full_rc=full_rc, full_binaries=8, full_tests=len(names),
                   full_failures=[killer], killer_needle=plant['kills'][0]['needle'],
                   physical_removed_rc=removed_rc, remaining_binaries=8, remaining_tests=len(remaining),
                   removed_tests=[killer], escapes=True,
                   mutant_source_sha256=hashlib.sha256(expected.encode()).hexdigest())
        (directory / 'result.json').write_text(json.dumps(row, indent=2) + '\n')
        print(name + ': complete-suite catch and single physical-removal escape', flush=True)
        return row

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        rows = list(pool.map(check, plants))
    (out / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(f'{len(rows)} plants: every complete-suite catch and physical-removal escape passed', flush=True)


if __name__ == '__main__':
    main()
