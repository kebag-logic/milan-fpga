#!/usr/bin/env python3
"""Focused real-owner persistence and three pending-mark fault controls.

Usage: python3 aecp_probe.py REPOSITORY PACKET --jobs 4
All generated trees stay in PACKET/scratch.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('repository', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('--jobs', type=int, default=4)
p.add_argument('--controls-only', action='store_true')
p.add_argument('--tests-only', action='store_true')
a = p.parse_args()
root, packet = a.repository.resolve(), a.packet.resolve()
(packet / 'scratch').mkdir(parents=True, exist_ok=True)
os.environ['TMPDIR'] = str(packet / 'scratch')
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import aecp_arms
import aecp_mutants
from ctrl_build import Tree, CTRL, stack_pin
import fw_gtest

print('stack pin:', stack_pin(), flush=True)
work = packet / 'scratch/aecp'
tree = Tree(CTRL, work / 'normal', work / 'reuse', fw_gtest.Build(jobs=a.jobs))
failed = False
for shape in (() if a.controls_only else ('endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8')):
    config = root / 'configs' / (shape + '.yaml')
    # The broad Nvm map cases use the default 1x1 dynamic-input-map fixture.
    # At 8x8 the input maps are static, so run the new shape-independent name case.
    selected_test = ('Nvm.*' if shape.endswith('1x1_tdm8') else
                     'Nvm.EveryAcknowledgedNameSurvivesTheRealStorePowerCycle')
    outcome = aecp_arms.core_arm(tree, config, 1, 'nvm', selected_test)
    print(outcome.log, flush=True)
    failed |= outcome.rc != 0
    (packet / 'receipts' / (shape + '-nvm.log')).write_text(outcome.log)
selected = [(i, d) for i, d in enumerate(aecp_mutants.DEFECTS)
            if d.name in ('nvm-ids-past-256-dropped', 'nvm-pending-counted-twice', 'nvm-pending-count-kept')]
assert len(selected) == 3
for i, d in (() if a.tests_only else selected):
    failed |= aecp_mutants.campaign(work / 'mutants', jobs=a.jobs, shard=(i, len(aecp_mutants.DEFECTS)))
    for name in ('results.json', d.name + '.log'):
        dest = ('aecp-' + d.name + '-results.json') if name == 'results.json' else ('aecp-' + name)
        shutil.copyfile(work / 'mutants' / name, packet / 'receipts' / dest)
print('Focused AECP persistence:', 'FAIL' if failed else 'PASS', flush=True)
raise SystemExit(int(failed))
