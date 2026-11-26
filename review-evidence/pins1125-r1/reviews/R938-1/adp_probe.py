#!/usr/bin/env python3
"""Run the complete ADP arm and the five changed consumer length controls."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_arms
import ctrl_mutants
from ctrl_build import CTRL, STACK, Tree, stack_pin
import fw_gtest

stack_pin()
build = fw_gtest.Build(jobs=4)
tree = Tree(CTRL, out / 'clean', out / 'reuse', build, STACK)
result = ctrl_arms.arm_adp(tree)
print('CLEAN ADP rc', result.rc, flush=True)
print(result.log, flush=True)
assert result.rc == 0
names = {'pin-adp-discovery-length', 'pin-adp-discovery-valid-time',
         'pin-adp-discovery-length-octet', 'pin-adp-long-discovery', 'pin-adp-valid-discovery'}
selected = [m for m in ctrl_mutants.MUTANTS if m.name in names]
assert len(selected) == 5
for m in selected:
    dest = out / m.name
    ctrl, stack = ctrl_mutants.plant(m, dest)
    result = ctrl_arms.arm_adp(Tree(ctrl, dest / 'build', out / 'reuse', build, stack))
    print('MUTANT', m.name, 'rc', result.rc, flush=True)
    print(result.log, flush=True)
    for arm, test, needle in m.kills():
        assert ctrl_mutants.caught(test, needle, result), (m.name, test, needle)
    print('CAUGHT', m.name, flush=True)
print('ADP focused campaign: clean PASS; 5/5 named defects caught', flush=True)
