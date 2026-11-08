#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# usage: escape_check4.py HEAD_TREE WORK OUT PLANTS_JSON
# Copies the exact-head tree once, builds acmp_tests (Debug) once, then for each reviewer plant object
# in PLANTS_JSON (name/path/old/new) rewrites the file from the pristine copy, rebuilds and runs the
# ACMP binary twice: the full suite, and the suite without the tests added since b7a5988 (NEW).
# For each plant it also finds the registered plant in tests/mutations.json with the same old/new
# text and reports whether every registered (test, needle) kill appears among the full run's failures.
# Needs TOOLS set to a prefix holding gtest-1.14.0. The reviewed tree is never modified.
import json, os, shutil, subprocess, sys
from pathlib import Path

NEW = ['AcmpOwed.OwedSetIsEightFramesOfEightyBytes', 'AcmpOwed.AnsweredOnlyBindAlsoWaitsForTwoSlots',
       'AcmpOwed.BindDeclinedBehindTheFullSetHoldsNoProbe', 'AcmpOwed.OnlyTimerProbesAreHeldBesideTheWaitingBind',
       'AcmpOwed.RefusedPollLeavesTheBindWaitingAndItsHold',
       'AcmpOwed.BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces', 'AcmpOwed.SameTalkerRebindKeepsTheHeldProbe',
       'AcmpOwed.GatedPortBudgetsOnePassPerProbeOwedAhead', 'AcmpOwed.KeptCommandsLeaveOnePassPerFrameOwedAheadOfThem',
       'AcmpOwed.KeptBacklogWithinTheDocumentedBudgetMeetsItsTimeout']


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def suite(binary, gfilter):
    r = run([str(binary), '--gtest_filter=' + gfilter], timeout=600)
    failed = sorted({l.split()[3] for l in r.stdout.splitlines() if l.startswith('[  FAILED  ] ') and '.' in l.split()[3]})
    total = [l for l in r.stdout.splitlines() if l.startswith('[==========] ') and 'ran' in l]
    return r.returncode, failed, (total[-1] if total else ''), r.stdout


def kills_seen(stdout, kills):
    # A kill counts when its needle is printed inside the failing test's block.
    seen = []
    for k in kills:
        block, inside = [], False
        for l in stdout.splitlines():
            if l.startswith('[ RUN      ] ' + k['test']):
                inside = True
            elif inside and (l.startswith('[       OK ] ') or l.startswith('[  FAILED  ] ')):
                break
            elif inside:
                block.append(l)
        seen.append((k['test'], k['needle'], any(k['needle'] in l for l in block)))
    return seen


def main():
    src, work, out, plants_json = map(Path, sys.argv[1:5])
    tools = os.environ['TOOLS']
    env = dict(os.environ, PKG_CONFIG_PATH=f'{tools}/gtest-1.14.0/lib/pkgconfig',
               CMAKE_PREFIX_PATH=f'{tools}/gtest-1.14.0', LD_LIBRARY_PATH=f'{tools}/gtest-1.14.0/lib')
    if work.exists():
        shutil.rmtree(work)
    tree = work / 'tree'
    shutil.copytree(src, tree, symlinks=True)
    registry = json.loads((tree / 'tests/mutations.json').read_text())
    plants = [p for p in json.loads(plants_json.read_text()) if isinstance(p, dict)]
    build = work / 'build'
    r = run(['cmake', '-S', str(tree), '-B', str(build), '-DCMAKE_BUILD_TYPE=Debug'], env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    lines = []

    def build_and_run(label, reg=None):
        b = run(['cmake', '--build', str(build), '--target', 'acmp_tests', '-j4'], env=env)
        if b.returncode != 0:
            lines.append(f'{label}: BUILD FAILED')
            return
        binary = build / 'acmp_tests'
        full = suite(binary, '*')
        rest = suite(binary, '-' + ':'.join(NEW))
        lines.append(f'{label}: full rc={full[0]} failed={full[1]} ({full[2]}) | without-new rc={rest[0]} failed={rest[1]} ({rest[2]})')
        if reg is not None:
            for t, n, ok in kills_seen(full[3], reg['kills']):
                lines.append(f"    registered {reg['name']} kill {t} needle {n!r}: {'SEEN' if ok else 'NOT SEEN'}")

    build_and_run('UNPLANTED head')
    for p in plants:
        f = tree / p['path']
        text = f.read_text()
        matches = [x for x in registry if x['path'] == p['path'] and x['new'].strip() == p['new'].strip()
                   and p['old'].strip() in x['old']]
        reg = matches[0] if len(matches) == 1 else None
        lines.append(f"{p['name']}: registered as {reg['name'] if reg else 'NONE (' + str(len(matches)) + ' matches)'}")
        if text.count(p['old']) != 1:
            lines.append(f"{p['name']}: OLD TEXT NOT UNIQUE ({text.count(p['old'])})")
            continue
        f.write_text(text.replace(p['old'], p['new']))
        build_and_run(p['name'], reg)
        f.write_text(text)
    build_and_run('UNPLANTED head (restored)')
    out.write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
