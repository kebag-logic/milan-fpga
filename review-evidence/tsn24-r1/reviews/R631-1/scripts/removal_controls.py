#!/usr/bin/env python3
"""Physically remove each new hosted test, then run its mutant against the remaining arm."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import xml.etree.ElementTree as ET

p = argparse.ArgumentParser()
p.add_argument('source', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('--jobs', type=int, default=4)
a = p.parse_args()
source, packet = a.source.resolve(), a.packet.resolve()
baseline = packet / 'scratch/validate/mutations/baseline'
work = packet / 'scratch/removals'
work.mkdir(exist_ok=True)
receipts = packet / 'receipts/removals'
receipts.mkdir(exist_ok=True)
flags = shlex.split(subprocess.check_output(['pkg-config', '--cflags', 'gtest', 'gmock'], text=True))
libs = shlex.split(subprocess.check_output(['pkg-config', '--libs', 'gtest', 'gmock'], text=True))
mutants = [m for m in json.loads((source / 'tests/mutations.json').read_text()) if m['name'].startswith('dafresh-')]
assert len(mutants) == 15

def run(m):
    directory = work / m['name']
    directory.mkdir(exist_ok=True)
    test = m['kills'][0]['test']
    suite, name = test.split('.')
    arm = 'entity' if suite == 'EntityYaml' else 'acmp'
    original = (source / 'tests' / ('test_' + arm + '.cpp')).read_text()
    match = re.search(r'TEST(?:_F)?\(' + re.escape(suite) + r',\s*' + re.escape(name) + r'\)\s*\{', original)
    assert match
    end, depth = match.end(), 1
    while depth:
        depth += (original[end] == '{') - (original[end] == '}')
        end += 1
    text = original[:match.start()] + original[end:]
    assert not re.search(r'TEST(?:_F)?\(' + re.escape(suite) + r',\s*' + re.escape(name), text)
    test_source = directory / 'test.cpp'
    test_source.write_text(text)
    obj = directory / 'test.o'
    binary = directory / arm
    plant = packet / 'scratch/validate/mutations' / m['name'] / (arm + '.o')
    assert plant.exists()
    objects = [plant]
    if arm == 'entity':
        paths = ['src/adp.c', 'src/acmp.c', 'src/maap.c', 'examples/entity_roundtrip.c'] + [
            f'examples/entities/{persona}/entity_config.c' for persona in ('listener', 'talker', 'duplex', 'ax7101')]
        objects = [plant if path == m['path'] else baseline / ('entity_' + str(i) + '.o') for i, path in enumerate(paths)]
    commands = [
        ['g++', '-std=c++20', '-O0', '-g', '-Wall', '-Wextra', '-Werror', *flags,
         '-I' + str(source / 'include'), '-I' + str(source / 'examples'), '-I' + str(source / 'tests'),
         '-c', str(test_source), '-o', str(obj)],
        ['g++', *map(str, objects), str(obj), str(baseline / 'main.o'), *libs, '-o', str(binary)],
    ]
    log = receipts / (m['name'] + '.log')
    xml = receipts / (m['name'] + '.xml')
    with log.open('w') as f:
        for command in commands:
            result = subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)
            if result.returncode:
                return {'name': m['name'], 'removed': test, 'status': 'BUILD_ERROR', 'rc': result.returncode}
        env = {k:v for k,v in os.environ.items() if not k.startswith('GTEST_')}
        result = subprocess.run([str(binary), '--gtest_output=xml:' + str(xml)], env=env, stdout=f, stderr=subprocess.STDOUT)
    cases = list(ET.parse(xml).getroot().iter('testcase'))
    names = {c.get('classname') + '.' + c.get('name') for c in cases}
    failures = [c.get('classname') + '.' + c.get('name') for c in cases if c.findall('failure')]
    complete = bool(cases) and all(c.get('status') == 'run' and c.get('result') == 'completed' for c in cases)
    assert test not in names
    status = 'ESCAPED' if result.returncode == 0 and complete and not failures else 'STILL_CAUGHT'
    row = {'name': m['name'], 'removed': test, 'status': status, 'rc': result.returncode,
           'remaining_tests': len(cases), 'failures': failures, 'complete': complete}
    print(json.dumps(row), flush=True)
    return row

with ThreadPoolExecutor(max_workers=a.jobs) as pool:
    rows = list(pool.map(run, mutants))
(receipts / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
raise SystemExit(int(any(row['status'] != 'ESCAPED' for row in rows)))
