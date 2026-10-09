#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Compile every mutation plant of two revisions to core objects and compare.

usage: plantcmp.py <git-repo> <rev-a> <rev-b> <scratch-dir> <out-json> [jobs]
Each revision is extracted to the SAME path; each plant is applied with that
revision's own tests/mutations.json and compiled with the mutation driver's
C flags for every arm the plant uses, with -g0. Hashes are compared by
(plant, arm). Unmatched names, anchor failures and hash differences are reported.
"""
import hashlib
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

repo, rev_a, rev_b, scratch, out = sys.argv[1:6]
jobs = int(sys.argv[6]) if len(sys.argv) > 6 else 8
tree = Path(scratch) / 'planttree'


def cflags(arm):
    return ['-std=c11', '-O0', '-g0', '-Wall', '-Wextra', '-Werror'] + (
        [] if arm.endswith('_debug') else ['-DNDEBUG', '-DCTRL_REENTRY_ASSERT'])


def extract(rev):
    shutil.rmtree(tree, ignore_errors=True)
    tree.mkdir(parents=True)
    archive = subprocess.run(['git', '-C', repo, 'archive', rev], check=True, capture_output=True).stdout
    subprocess.run(['tar', '-x', '-C', str(tree)], input=archive, check=True)


def build(plant):
    work = tree / 'plants' / plant['name']
    for name in ('src', 'include'):
        shutil.copytree(tree / name, work / name, dirs_exist_ok=True)
    target = work / plant['path']
    text = target.read_text()
    if text.count(plant['old']) != 1:
        return plant['name'], {'error': 'anchor count %d' % text.count(plant['old'])}
    target.write_text(text.replace(plant['old'], plant['new']))
    module = target.stem
    default = 'maap_debug' if any(k['test'].startswith('MaapDebug.') for k in plant['kills']) else module
    arms = sorted({k.get('arm', default) for k in plant['kills']})
    result = {}
    for arm in arms:
        obj = work / (arm + '.o')
        r = subprocess.run(['gcc', *cflags(arm), '-I' + str(work / 'include'), '-c',
                            str(work / 'src' / (module + '.c')), '-o', str(obj)],
                           capture_output=True, text=True)
        result[arm] = hashlib.sha256(obj.read_bytes()).hexdigest() if r.returncode == 0 else 'COMPILE-FAIL'
    result['kills'] = sorted((k['test'], k['needle'], k.get('arm', default)) for k in plant['kills'])
    return plant['name'], result


tables = {}
for rev in (rev_a, rev_b):
    extract(rev)
    table = json.loads((tree / 'tests/mutations.json').read_text())
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        tables[rev] = dict(pool.map(build, table))
a, b = tables[rev_a], tables[rev_b]
report = {'plants_a': len(a), 'plants_b': len(b),
          'only_a': sorted(set(a) - set(b)), 'only_b': sorted(set(b) - set(a)),
          'errors': sorted(n for n in set(a) | set(b) if 'error' in a.get(n, {}) or 'error' in b.get(n, {})),
          'object_differences': [], 'kill_mapping_differences': [], 'compile_failures': [],
          'identical_plants': 0}
for name in sorted(set(a) & set(b)):
    ra, rb = a[name], b[name]
    if 'error' in ra or 'error' in rb:
        continue
    oa = {k: v for k, v in ra.items() if k != 'kills'}
    ob = {k: v for k, v in rb.items() if k != 'kills'}
    if 'COMPILE-FAIL' in oa.values() or 'COMPILE-FAIL' in ob.values():
        report['compile_failures'].append(name)
    if oa != ob:
        report['object_differences'].append(name)
    if ra['kills'] != rb['kills']:
        report['kill_mapping_differences'].append(name)
    if oa == ob and ra['kills'] == rb['kills']:
        report['identical_plants'] += 1
Path(out).write_text(json.dumps(report, indent=1) + '\n')
print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in report.items()}))
sys.exit(0 if report['identical_plants'] == len(a) == len(b) else 1)
