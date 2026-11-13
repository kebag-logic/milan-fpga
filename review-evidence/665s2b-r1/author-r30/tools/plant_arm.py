"""Run one control-campaign plant's arm and print its failing checks: plant_arm.py CHECKOUT OUT MUTANT ARM"""
import sys
from pathlib import Path
co, out, name, arm = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
sys.path[:0] = [str(co / 'sw/firmware/ctrl/test'), str(co / 'sw/firmware/gtest')]
import ctrl_mutants as m, ctrl_arms, fw_gtest
from ctrl_build import Tree
mut = next(x for x in m.MUTANTS if x.name == name)
ctrl, stack = m.plant(mut, out)
tree = Tree(ctrl, out / 'work' / 'build', out / 'reuse', fw_gtest.Build(jobs=8), stack)
o = getattr(ctrl_arms, 'arm_' + arm)(tree)
print('\n'.join(ln for ln in o.log.splitlines() if '[FAIL]' in ln or 'checks:' in ln or 'C5' in ln))
