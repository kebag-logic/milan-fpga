#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Apply each probe plant to a disposable copy of the tree, rebuild, run every test
binary, and record which tests fail and with which assertion messages.

Usage: run_probes.py <disposable-tree> <probes.json> <build-dir> <out.json> [jobs]
The tree must be a disposable export of the reviewed head; src/adp.c is restored
after each probe and its bytes are checked against the original.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

tree, probes_path, build, out = map(Path, sys.argv[1:5])
jobs = sys.argv[5] if len(sys.argv) > 5 else '12'
probes = json.loads(probes_path.read_text())
original = {}


def run(cmd, **kw):
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw)


r = run(['cmake', '-S', str(tree), '-B', str(build), '-DCMAKE_BUILD_TYPE=Debug', '-DCMAKE_C_COMPILER=gcc', '-DCMAKE_CXX_COMPILER=g++'])
if r.returncode:
    sys.exit('configure failed\n' + r.stdout)


def build_and_test():
    b = run(['cmake', '--build', str(build), '-j' + jobs])
    if b.returncode:
        return {'build': 'failed', 'log': b.stdout[-2000:]}
    failures = {}
    for exe in sorted(p for p in build.iterdir() if p.is_file() and p.stat().st_mode & 0o111 and p.suffix == ''):
        t = run([str(exe)], timeout=300)
        failed = sorted(set(re.findall(r'^\[  FAILED  \] ([A-Za-z_/]+\.[A-Za-z0-9_/]+)', t.stdout, re.M)))
        if failed:
            msgs = sorted(set(m for m in re.findall(r'^(A\d\d[^\n]*)$', t.stdout, re.M)))
            failures[exe.name] = {'rc': t.returncode, 'failed': failed, 'messages': msgs[:12]}
        elif t.returncode:
            failures[exe.name] = {'rc': t.returncode, 'failed': [], 'tail': t.stdout[-600:]}
    return {'build': 'ok', 'failures': failures}


results = {'baseline': build_and_test()}
for p in probes:
    target = tree / p['path']
    text = target.read_text()
    original.setdefault(p['path'], hashlib.sha256(text.encode()).hexdigest())
    if text.count(p['old']) != 1:
        results[p['name']] = {'error': 'old text does not match once'}
        continue
    target.write_text(text.replace(p['old'], p['new']))
    try:
        results[p['name']] = build_and_test()
    finally:
        target.write_text(text)
    if hashlib.sha256(target.read_text().encode()).hexdigest() != original[p['path']]:
        sys.exit('restore failed for ' + p['path'])
    res = results[p['name']]
    caught = sorted(t for f in res.get('failures', {}).values() for t in f['failed'])
    print(p['name'], 'CAUGHT by ' + ', '.join(caught) if caught else ('BUILD FAILED' if res.get('build') != 'ok' else 'ESCAPED (no test fails)'), flush=True)
results['restored_sha256'] = original
out.write_text(json.dumps(results, indent=2) + '\n')
base = results['baseline']
print('baseline', 'clean' if base.get('build') == 'ok' and not base['failures'] else json.dumps(base)[:500])
