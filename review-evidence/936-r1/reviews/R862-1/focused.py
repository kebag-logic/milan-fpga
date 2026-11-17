#!/usr/bin/env python3
"""Focused exact-head tests; all disposable builds live below packet/scratch.
Run: python3 -B focused.py CHECKOUT PACKET [srp1|srp2|aecp|all]
Uses the checkout's unchanged assertions, mutation definitions and graders.
"""
import concurrent.futures
import json
import pathlib
import shutil
import subprocess
import sys

checkout, packet = map(lambda x: pathlib.Path(x).resolve(), sys.argv[1:3])
mode = sys.argv[3] if len(sys.argv) > 3 else 'all'
if mode == 'all':
    def run(part):
        log = packet / (part + '.log')
        with log.open('w') as stream:
            result = subprocess.run([sys.executable, '-B', __file__, str(checkout), str(packet), part],
                                    stdout=stream, stderr=subprocess.STDOUT, timeout=550)
        (packet / (part + '.rc')).write_text(str(result.returncode) + '\n')
        return part, result.returncode
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, ['srp1', 'srp2', 'aecp']))
    print(json.dumps(results))
    sys.exit(int(any(code for _, code in results)))

sys.path.insert(0, str(checkout / 'sw/firmware/ctrl/test'))
from ctrl_build import CTRL, ROOT, Tree, Outcome
import fw_gtest
import srp_arms
import srp_mutants
import aecp_arms
import aecp_mutants

work = packet / 'scratch' / mode
work.mkdir(parents=True, exist_ok=True)
logs = packet / 'receipts' / mode
logs.mkdir(parents=True, exist_ok=True)
src = work / 'ctrl'
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
shutil.copytree(CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', dirs_exist_ok=True,
                ignore=shutil.ignore_patterns('test', '__pycache__', '*.pyc'))
tree = Tree(src, work / 'build', work / 'reuse', fw_gtest.Build(jobs=4))
records = []

def receipt(name, result, good):
    (logs / (name + '.log')).write_text(result.log)
    records.append(dict(name=name, rc=result.rc, accepted=bool(good)))
    print(name, 'PASS' if good else 'FAIL', flush=True)
    (logs / 'results.json').write_text(json.dumps(records, indent=2) + '\n')

if mode.startswith('srp'):
    interfaces = int(mode[-1])
    config = ROOT / ('configs/endstation_ax7101_8x8.yaml' if interfaces == 2 else
                     'configs/endstation_ax7101_1x1_tdm8.yaml')
    lw = ROOT / 'third_party/lwSRP'
    for suite, selected in [('srp_talker.cpp', '*'), ('test_acmp_mbx.cpp', 'SrpGate.*')]:
        result = srp_arms.arm_srp(tree, lw, interfaces, test=(suite, selected), config=config)
        receipt('baseline-' + suite, result, result.rc == 0)
    defects = [d for d in srp_mutants.DEFECTS if d.name.startswith('talker-notice-')]
    assert len(defects) == 12
    for d in defects:
        target = src / d.path
        original = target.read_text()
        assert original.count(d.old) == 1, d.name
        target.write_text(original.replace(d.old, d.new))
        try:
            result = srp_arms.arm_srp(tree, lw, interfaces, test=(d.suite, d.test), config=config)
            receipt(d.name, result, srp_mutants.caught(d.test, d.needle, result))
        finally:
            target.write_text(original)
elif mode == 'aecp':
    aecp_mutants.controls()
    config = ROOT / 'configs/endstation_ax7101_1x1_tdm8.yaml'
    selected = 'App.SrpDeclarationChangeIsItsStreamOutputsNotice'
    for interfaces in [1, 2]:
        result = aecp_arms.core_arm(tree, config, interfaces, 'app', selected)
        receipt('baseline-if' + str(interfaces), result, result.rc == 0)
    defects = [d for d in aecp_mutants.DEFECTS if d.name.startswith('app-output-notice-')]
    assert len(defects) == 4
    for d in defects:
        target = src / d.path
        original = target.read_text()
        assert original.count(d.old) == 1, d.name
        target.write_text(original.replace(d.old, d.new))
        try:
            result = aecp_arms.core_arm(tree, config, 2, 'app', ':'.join(t for t, _ in d.checks))
            receipt(d.name, result, all(aecp_mutants.caught(t, words, result) for t, words in d.checks))
        finally:
            target.write_text(original)
else:
    raise SystemExit('Unknown mode')
sys.exit(int(any(not r['accepted'] for r in records)))
