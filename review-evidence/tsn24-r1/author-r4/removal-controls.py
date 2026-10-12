#!/usr/bin/env python3
"""Physically remove each new named test and rerun its mutation executable."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, required=True)
parser.add_argument('--campaign', type=Path, required=True)
parser.add_argument('--work', type=Path, required=True)
parser.add_argument('--jobs', type=int, default=16)
args = parser.parse_args()
root, campaign, work = args.root.resolve(), args.campaign.resolve(), args.work.resolve()
work.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / 'scripts'))
m = importlib.import_module('mutation')
m.MESSAGE_MARKERS = tuple(json.loads((campaign / 'message-markers.json').read_text()))
plants = [p for p in json.loads((root / 'tests/mutations.json').read_text()) if p['name'].startswith('dafresh-')]
results = json.loads((campaign / 'results.json').read_text())
assert all(next(r for r in results if r['name'] == p['name'])['status'] == 'CAUGHT' for p in plants)
flags, libs = m.package_flags('--cflags'), m.package_flags('--libs')
base = campaign / 'baseline'
required = {'NoProbe', 'StaleProbe', 'WindowEdge', 'ListenerWithoutProbe', 'InvalidAddress'}

def remove_test(text, name):
    suite, test = name.split('.')
    pattern = r'TEST(?:_F)?\(\s*' + re.escape(suite) + r'\s*,\s*' + re.escape(test) + r'\s*\)\s*\{'
    hits = list(re.finditer(pattern, text))
    assert len(hits) == 1, name
    start = hits[0].start()
    end = text.index('\n}', hits[0].end()) + 2
    return text[:start] + text[end:]

def check(p):
    d = work / p['name']
    d.mkdir(exist_ok=True)
    log = []
    k = p['kills'][0]
    arm = k.get('arm', 'acmp')
    source = root / 'tests' / m.SOURCES[arm]
    planted = campaign / p['name']
    original = (root / p['path']).read_text()
    assert (planted / p['path']).read_text() == original.replace(p['old'], p['new'])
    full_rc, failures, full_count = m.execute(planted / arm, d / 'full.xml', log)
    assert full_rc == 1 and full_count > 1 and m.matches(k, failures), (p['name'], failures)
    result = dict(name=p['name'], test=k['test'], full_rc=full_rc, full_tests=full_count,
                  full_failures=sorted(failures), removal=[k['test']])
    def trial(removed, label):
        text = source.read_text()
        for name in removed:
            text = remove_test(text, name)
        path = d / (label + '.cpp')
        path.write_text(m.instrument(text, m.MESSAGE_MARKERS))
        obj = d / (label + '.o')
        cmd = ['g++', *m.cppflags(arm), *flags, '-I' + str(root / 'include'),
               '-I' + str(root / 'examples'), '-I' + str(root / 'tests'), '-c', str(path), '-o', str(obj)]
        assert m.run(cmd, log) == 0, ''.join(log)
        if arm == 'entity':
            originals = ['src/adp.c', 'src/acmp.c', 'src/maap.c', 'examples/entity_roundtrip.c'] + [
                f'examples/entities/{persona}/entity_config.c' for persona in ('listener', 'talker', 'duplex', 'ax7101')]
            objects = [str(planted / 'entity.o') if path == p['path'] else str(base / f'entity_{i}.o')
                       for i, path in enumerate(originals)]
        else:
            objects = [str(planted / (arm + '.o'))]
        binary = d / label
        assert m.run(['g++', *objects, str(obj), str(base / 'main.o'), *libs, '-o', str(binary)], log) == 0
        rc, remaining, count = m.execute(binary, d / (label + '.xml'), log)
        assert count == full_count - len(removed), (p['name'], count, full_count)
        return rc, sorted(remaining), count
    rc, remaining, count = trial([k['test']], 'removed')
    result.update(removed_rc=rc, remaining_failures=remaining, remaining_tests=count,
                  single_test_escape=rc == 0 and not remaining)
    if not result['single_test_escape']:
        assert k['test'].split('.')[1] not in required, result
        removed = sorted(failures)
        group_rc, group_failures, group_count = trial(removed, 'all-killers-removed')
        assert group_rc == 0 and not group_failures
        result.update(group_removal=removed, group_rc=group_rc, group_tests=group_count)
    (d / 'run.log').write_text(''.join(log))
    print(p['name'], 'single escape' if result['single_test_escape'] else 'overlapping killers', flush=True)
    return result

with ThreadPoolExecutor(max_workers=min(args.jobs, 3)) as pool:
    rows = list(pool.map(check, plants))
(work / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
print('Required single-test removals: 5 passed', flush=True)
