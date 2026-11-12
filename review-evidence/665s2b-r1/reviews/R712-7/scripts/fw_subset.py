"""Run the firmware arms the round changed and a named subset of the planted defects, with the tree's own drivers.
usage: python3 -B fw_subset.py <repo-root> <workdir> arms|ctrl|aecp [names...]"""
import sys, shutil
from pathlib import Path
root, work, what, names = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4:]
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_arms, ctrl_mutants, aecp_mutants, fw_gtest
from ctrl_build import CTRL, Tree, stack_pin
from ctrl_reuse import cut_reuse
work.mkdir(parents=True, exist_ok=True)
print('toolchain:', fw_gtest.toolchain()); print('tsn-c-stack at', stack_pin())
if what == 'arms':
    tree = Tree(CTRL, work / 'checkout', work / 'reuse', fw_gtest.Build(jobs=4)); cut_reuse(tree.reuse)
    bad = 0
    for arm in (ctrl_arms.arm_unit, ctrl_arms.arm_port, ctrl_arms.arm_portable):
        o = arm(tree); bad |= o.rc != 0
        lines = [l for l in o.log.splitlines() if any(k in l for k in ('[  PASSED', '[  FAILED', '[FAIL]', 'tests ran',
                 'T2', 'T4', 'T5', 'P10', 'Portable.'))]
        print(f'== arm {o.arm if hasattr(o, "arm") else arm.__name__}: rc {o.rc}'); print('\n'.join(lines[-12:]))
    sys.exit(1 if bad else 0)
if what == 'ctrl':
    tree = Tree(CTRL, work / 'checkout', work / 'reuse', fw_gtest.Build(jobs=4)); cut_reuse(tree.reuse)
    ctrl_mutants.MUTANTS = [m for m in ctrl_mutants.MUTANTS if m.name in names]
    assert len(ctrl_mutants.MUTANTS) == len(names), [m.name for m in ctrl_mutants.MUTANTS]
    ctrl_mutants.unnamed_tests = lambda: []
    sys.exit(1 if ctrl_mutants.campaign(work / 'mutants', tree.reuse, 4, shard=[0, 1]) else 0)
if what == 'aecp':
    aecp_mutants.DEFECTS = tuple(d for d in aecp_mutants.DEFECTS if d.name in names)
    assert len(aecp_mutants.DEFECTS) == len(names), [d.name for d in aecp_mutants.DEFECTS]
    aecp_mutants.controls = lambda: None
    sys.exit(1 if aecp_mutants.campaign(work / 'aecp', 4) else 0)
