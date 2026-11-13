#!/usr/bin/env python3
"""Run the delta tests and three plants at both points, in disposable trees.

Usage: python3 -B focused.py CHECKOUT PACKET
Two foreground workers, eight compile jobs each; no source checkout edits.
"""
import concurrent.futures
import os
from pathlib import Path
import shutil
import sys

repo, packet = map(lambda s: Path(s).resolve(), sys.argv[1:])
os.environ['TMPDIR'] = str(packet / 'scratch')
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
from ctrl_build import Tree, CTRL, fw_gtest
from srp_arms import arm_srp
import srp_mutants

names = ('talker-refused-withdrawal-forgotten', 'talker-refused-withdrawal-not-owed',
         'talker-transmit-publishes-past-its-terms')
def run(point):
    work = packet / 'scratch' / f'focused-{point}'
    work.mkdir(parents=True, exist_ok=True)
    output = packet / 'receipts' / f'focused-{point}'
    output.mkdir(parents=True, exist_ok=True)
    build = fw_gtest.Build(jobs=8)
    cfg = repo / 'configs' / ('endstation_ax7101_1x1_tdm8.yaml' if point == 1 else 'endstation_ax7101_8x8.yaml')
    src = work / 'ctrl'
    def write_log(name, log):
        for root, token in ((str(packet), '<packet>'), (str(repo), '<clone>')):
            log = log.replace(root, token)
        (output / (name + '.log')).write_text(log)
    def arm(name, selected):
        return arm_srp(Tree(src, work / name, work / 'reuse', build), repo / 'third_party/lwSRP', point,
                       test=('srp_talker.cpp', selected), config=cfg)
    shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    good = arm('clean', 'Talker.*')
    write_log('clean', good.log)
    checks = [('clean', good.rc == 0)]
    for d in (x for x in srp_mutants.DEFECTS if x.name in names):
        target = src / d.path
        original = target.read_text()
        assert original.count(d.old) == 1, d.name
        target.write_text(original.replace(d.old, d.new))
        result = arm(d.name, d.test)
        caught = srp_mutants.caught(d.test, d.needle, result)
        write_log(d.name, result.log)
        checks.append((d.name, caught))
        target.write_text(original)
    lines = [f'{name}: {"PASS" if ok else "FAIL"}' for name, ok in checks]
    (output / 'summary.txt').write_text('\n'.join(lines) + '\n')
    print(f'point {point}: ' + '; '.join(lines), flush=True)
    return all(ok for _, ok in checks)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, (1, 2)))
sys.exit(0 if all(results) else 1)
