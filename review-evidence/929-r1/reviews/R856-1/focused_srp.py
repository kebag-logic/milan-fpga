#!/usr/bin/env python3
"""Run the four complete mailbox arms and shape-sensitive mutation probes.
Usage: focused_srp.py CHECKOUT PACKET [--jobs N]
Builds and source copies remain under PACKET/scratch.
"""
import argparse
import concurrent.futures
import shutil
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('checkout', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('--jobs', type=int, default=4)
a = p.parse_args()
root, packet = a.checkout.resolve(), a.packet.resolve()
sys.path[:0] = [str(root / 'sw/firmware/ctrl/test'), str(root / 'sw/firmware/gtest')]
import fw_gtest
import srp_arms
import srp_mutants
from ctrl_build import Tree, CTRL
from ctrl_reuse import cut_reuse

def execute(item):
    name, shape, interfaces, defect = item
    work = packet / 'scratch' / 'srp' / name
    work.mkdir(parents=True, exist_ok=True)
    src = CTRL
    if defect:
        src = work / 'ctrl'
        shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        path = src / defect.path
        data = path.read_text()
        assert data.count(defect.old) == 1
        path.write_text(data.replace(defect.old, defect.new))
    tree = Tree(src, work / 'build', work / 'reuse', fw_gtest.Build(jobs=2))
    cut_reuse(tree.reuse)
    test = 'srp_mbx.cpp' if defect is None else (defect.suite, 'Srp.' + defect.test)
    result = srp_arms.arm_srp(tree, root / 'third_party/lwSRP', interfaces,
                              test=test, config=root / 'configs' / (shape + '.yaml'))
    (packet / (name + '.log')).write_text(result.log)
    (packet / (name + '.rc')).write_text(str(result.rc) + '\n')
    if defect is None:
        ok = result.rc == 0
        expected = 'PASS'
    elif shape.endswith('8x8') or defect.name == 'duplicate-tick-owner-8x8':
        ok = srp_mutants.caught('Srp.' + defect.test, defect.needle, result)
        expected = 'CAUGHT by named assertion'
    else:
        ok = result.rc == 0
        expected = 'INERT at two-source shape'
    print(f'{name}: rc={result.rc}; expected {expected}; verified={ok}', flush=True)
    return ok

small, large = 'endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8'
controls = [(f'srp-control-{s}-if{i}', s, i, None) for s in (small, large) for i in (1, 2)]
names = {'startup-8x8-sources-past-two-undeclared', 'startup-8x8-failure-code-past-two', 'duplicate-tick-owner-8x8'}
defects = [d for d in srp_mutants.DEFECTS if d.name in names]
assert len(defects) == 3
plants = [(f'srp-{d.name}-{s}', s, 2, d) for d in defects for s in (small, large)]
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
    good = all(list(pool.map(execute, controls)))
    good = all(list(pool.map(execute, plants))) and good
sys.exit(0 if good else 1)
