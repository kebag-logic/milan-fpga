#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# usage: escape_check.py HEAD_TREE WORK OUT PLANTS_JSON
# Copies the exact-head tree once, builds acmp_tests (Debug) once, then for each plant rewrites
# src/acmp.c from the pristine copy, rebuilds only what changed and runs the ACMP binary twice:
# the full suite, and the suite without the three round 3 tests. PLANTS_JSON is a list whose items
# are either a registered plant name (taken from tests/mutations.json) or an object with
# name/path/old/new for a reviewer plant. The reviewed tree is never modified.
# Needs TOOLS set to a prefix holding gtest-1.14.0.
import json, os, shutil, subprocess, sys
from pathlib import Path

ROUND3 = ['AcmpOwed.ProbesFallingDueInTheDrainWaitForTheDeferredBind',
          'AcmpOwed.DeferredBindAtTheDocumentedMarginMeetsItsTimeout',
          'AcmpOwed.HoldEndsWithTheLastHeldProbe']


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def suite(binary, gfilter):
    r = run([str(binary), '--gtest_filter=' + gfilter], timeout=600)
    failed = sorted({l.split()[3] for l in r.stdout.splitlines() if l.startswith('[  FAILED  ] ') and '.' in l.split()[3]})
    total = [l for l in r.stdout.splitlines() if l.startswith('[==========] ') and 'ran' in l]
    return r.returncode, failed, (total[-1] if total else '')


def main():
    src, work, out, plants_json = map(Path, sys.argv[1:5])
    tools = os.environ['TOOLS']
    env = dict(os.environ, PKG_CONFIG_PATH=f'{tools}/gtest-1.14.0/lib/pkgconfig',
               CMAKE_PREFIX_PATH=f'{tools}/gtest-1.14.0', LD_LIBRARY_PATH=f'{tools}/gtest-1.14.0/lib')
    if work.exists():
        shutil.rmtree(work)
    tree = work / 'tree'
    shutil.copytree(src, tree, symlinks=True)
    registry = {x['name']: x for x in json.loads((tree / 'tests/mutations.json').read_text())}
    plants = [registry[p] if isinstance(p, str) else p for p in json.loads(plants_json.read_text())]
    pristine = {}
    build = work / 'build'
    r = run(['cmake', '-S', str(tree), '-B', str(build), '-DCMAKE_BUILD_TYPE=Debug'], env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    lines = []

    def build_and_run(label):
        b = run(['cmake', '--build', str(build), '--target', 'acmp_tests', '-j4'], env=env)
        if b.returncode != 0:
            lines.append(f'{label}: BUILD FAILED')
            return
        binary = build / 'acmp_tests'
        full = suite(binary, '*')
        rest = suite(binary, '-' + ':'.join(ROUND3))
        lines.append(f'{label}: full rc={full[0]} failed={full[1]} | without-round3 rc={rest[0]} failed={rest[1]} ({rest[2]})')

    build_and_run('UNPLANTED head')
    for p in plants:
        f = tree / p['path']
        pristine.setdefault(f, f.read_text())
        text = pristine[f]
        if text.count(p['old']) != 1:
            lines.append(f"{p['name']}: OLD TEXT NOT UNIQUE ({text.count(p['old'])})")
            continue
        f.write_text(text.replace(p['old'], p['new']))
        build_and_run(p['name'])
        f.write_text(text)
    build_and_run('UNPLANTED head (restored)')
    out.write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
