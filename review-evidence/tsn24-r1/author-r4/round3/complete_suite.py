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
    args = parser.parse_args()
    work = args.work.resolve()
    tree = work / 'tree'
    out = work / 'complete-suite'
    out.mkdir(exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith('GTEST_')}
    baseline_rc, baseline, failures = suite(work / 'registration', out / 'baseline', env)
    assert baseline_rc == 0 and not failures
    plants = [p for p in json.loads((tree / 'tests/mutations.json').read_text())
              if p['name'].startswith('g-expiry-skipped-')]
    assert len(plants) == 2
    gaps = {r['mutant']: r for r in json.loads((work / 'gap/gap-mutants.json').read_text())}
    physical = {r['plant']: r for r in json.loads((work / 'physical/physical-removal.json').read_text())}
    assert set(physical) == {p['name'] for p in plants}
    rows = []
    for plant in plants:
        name = plant['name']
        killer = plant['kills'][0]['test']
        assert gaps[name]['result'] == 'CAUGHT' and gaps[name]['suite_rc'] == 8
        assert gaps[name]['failing_tests'] == [killer] and gaps[name]['failing_count'] == 1
        assert physical[name]['escapes'] and physical[name]['build_rc'] == 0
        assert physical[name]['suite_rc'] == 0 and not physical[name]['removed_present_after']
        assert not physical[name]['still_failing_tests']
        original = (tree / plant['path']).read_text()
        assert original.count(plant['old']) == 1
        expected = original.replace(plant['old'], plant['new'])
        planted = work / 'gap' / name
        removed = work / 'physical' / name
        for source in tree.rglob('*'):
            if not source.is_file():
                continue
            relative = source.relative_to(tree)
            for location, is_removed in [(planted, False), (removed, True)]:
                wanted = source.read_bytes()
                if str(relative) == plant['path']:
                    wanted = expected.encode()
                elif is_removed and str(relative) == 'tests/test_acmp.cpp':
                    wanted = remove(source.read_text(), killer).encode()
                assert (location / 'tree' / relative).read_bytes() == wanted, (name, relative)
        full_rc, names, failures = suite(planted / 'b', out / name / 'full', env)
        assert full_rc == 8 and names == baseline
        assert set(failures) == {killer}
        assert plant['kills'][0]['needle'] in failures[killer]
        removed_rc, remaining, failures = suite(removed / 'b', out / name / 'removed', env)
        expected_names = {key for key in baseline if key[1] != killer}
        assert len(expected_names) == len(baseline) - 1
        assert removed_rc == 0 and remaining == expected_names and not failures
        rows.append(dict(plant=name, killer=killer, full_rc=full_rc, full_binaries=8,
                         full_tests=len(names), full_failures=[killer],
                         killer_needle=plant['kills'][0]['needle'], physical_removed_rc=removed_rc,
                         remaining_binaries=8, remaining_tests=len(remaining),
                         removed_tests=[killer], escapes=True,
                         mutant_source_sha256=hashlib.sha256(expected.encode()).hexdigest()))
    (out / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(f'{len(rows)} plants: complete-suite catches and single physical-removal escapes passed')


if __name__ == '__main__':
    main()
