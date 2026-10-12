#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check complete XML registration and exactly one physical test removal per plant."""
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

p = argparse.ArgumentParser()
p.add_argument('--work', type=Path, required=True)
p.add_argument('--jobs', type=int, default=4)
a = p.parse_args()
w = a.work.resolve()
tree = w / 'tree'
out = w / 'complete-suites'
out.mkdir(exist_ok=True)
env = {k:v for k,v in os.environ.items() if not k.startswith('GTEST_')}

def command(argv, file, cwd=None, extra=None):
    file.parent.mkdir(parents=True, exist_ok=True)
    with file.open('w') as log:
        rc = subprocess.run(argv, cwd=cwd, env=dict(env, **(extra or {})), stdout=log, stderr=subprocess.STDOUT).returncode
    file.with_suffix('.rc').write_text(str(rc) + '\n')
    return rc

def build(source, target, logdir):
    assert command(['cmake','-S',str(source),'-B',str(target),'-DCMAKE_BUILD_TYPE=Debug'], logdir/'configure.log') == 0
    assert command(['cmake','--build',str(target),'-j16'], logdir/'build.log') == 0

def suite(builddir, directory):
    xml = directory / 'xml'
    if xml.exists():
        shutil.rmtree(xml)
    xml.mkdir(parents=True)
    rc = command(['ctest','--test-dir',str(builddir),'--output-on-failure','-j16'], directory/'suite.log',
                 extra={'GTEST_OUTPUT':'xml:'+str(xml)+'/'})
    files = sorted(xml.glob('*.xml'))
    assert len(files) == 8
    names, failures = set(), {}
    for file in files:
        root = ET.parse(file).getroot()
        cases = root.findall('.//testcase')
        assert root.tag == 'testsuites' and int(root.get('tests')) == len(cases)
        assert int(root.get('errors')) == int(root.get('disabled')) == 0
        failed_count = 0
        for case in cases:
            name = case.get('classname')+'.'+case.get('name')
            key = (file.stem, name)
            assert key not in names
            names.add(key)
            assert case.get('status') == 'run' and case.get('result') == 'completed'
            assert case.find('skipped') is None and case.find('error') is None
            failed = case.findall('failure')
            if failed:
                failed_count += 1
                failures[name] = '\n'.join(f.get('message','') for f in failed)
        assert int(root.get('failures')) == failed_count
    return rc, names, failures

def remove_test(text, killer):
    owner, name = killer.split('.')
    hits = list(re.finditer(r'TEST(?:_F)?\(\s*'+re.escape(owner)+r'\s*,\s*'+re.escape(name)+r'\s*\)\s*\{', text))
    assert len(hits) == 1
    start = text.rindex('// REQ:',0,hits[0].start())
    end = re.compile(r'^}\n',re.M).search(text,hits[0].end()).end()
    return text[:start]+text[end:]

baseline_dir = w/'gcc'
build(tree, baseline_dir, out/'baseline')
baseline_rc, baseline, failures = suite(baseline_dir,out/'baseline')
assert baseline_rc == 0 and len(baseline) == 418 and not failures
snapshot = {str(f.relative_to(tree)):f.read_bytes() for f in tree.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
plants = [m for m in json.loads((tree/'tests/mutations.json').read_text())
          if m['name'].startswith('dafresh-') or m['name']=='x-zero-never-expires']

def check(m):
    name = m['name']
    killer = m['kills'][0]['test']
    target = 'tests/test_entity.cpp' if killer.startswith('EntityYaml.') else 'tests/test_acmp.cpp'
    before = snapshot[m['path']].decode()
    assert before.count(m['old']) == 1
    planted_bytes = before.replace(m['old'],m['new']).encode()
    deleted_bytes = remove_test(snapshot[target].decode(),killer).encode()
    planted = w/'escape'/name
    for file, data in snapshot.items():
        assert (planted/'tree'/file).read_bytes() == (planted_bytes if file == m['path'] else data)
    rc, full, failed = suite(planted/'build',out/name/'full')
    assert rc == 8 and full == baseline and set(failed) == {killer}, (name,rc,len(full),list(failed))
    assert m['kills'][0]['needle'] in failed[killer]
    removed = w/'physical-0'/name
    if name == 'dafresh-generated-window':
        removed = w/'physical-entity'/name
        if removed.exists():
            shutil.rmtree(removed)
        shutil.copytree(planted/'tree',removed/'tree')
        (removed/'tree'/target).write_bytes(deleted_bytes)
        build(removed/'tree',removed/'b',out/name/'physical-build')
    for file,data in snapshot.items():
        expected = planted_bytes if file == m['path'] else deleted_bytes if file == target else data
        assert (removed/'tree'/file).read_bytes() == expected, (name,file)
    rc2, remaining, failed = suite(removed/'b',out/name/'removed')
    assert rc2 == 0 and not failed
    assert remaining == {key for key in baseline if key[1] != killer} and len(remaining) == 417
    row = dict(plant=name,killer=killer,full_rc=rc,full_binaries=8,full_tests=len(full),
               full_failures=[killer],needle_verified=True,physical_removed_rc=rc2,
               remaining_binaries=8,remaining_tests=len(remaining),removed_tests=[killer],
               full_source_edits=[m['path']],removed_source_edits=[m['path'],target],
               snapshot_files_checked=len(snapshot),mutant_sha256=hashlib.sha256(planted_bytes).hexdigest(),escapes=True)
    (out/name/'result.json').write_text(json.dumps(row,indent=2)+'\n')
    print(name+': 418 complete cases; named catch; 417 complete cases after single physical removal',flush=True)
    return row

with ThreadPoolExecutor(max_workers=a.jobs) as pool:
    rows = list(pool.map(check,plants))
(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
print(str(len(rows))+' complete-suite proofs passed',flush=True)
