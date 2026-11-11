"""Run the unit arm (driver, MMIO window and record mover driver tests) of the control-plane firmware's host test from
a tree, printing every failed test line. Usage: python3 -I run_unit_arm.py <tree root> <out dir>"""
import sys
from pathlib import Path
root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(root / 'sw/firmware/gtest'))
import ctrl_arms, fw_gtest
from ctrl_build import CTRL, Tree
o = ctrl_arms.arm_unit(Tree(CTRL, out / 'checkout', out / 'reuse', fw_gtest.Build(jobs=4)))
for l in o.log.splitlines():
    if 'FAILED' in l or 'Probe' in l or 'probe:' in l or 'Failure' in l or 'Expected' in l or 'Which is' in l:
        print('   ', l[:220])
print(f'arm {o.arm}: rc {o.rc}')
sys.exit(o.rc != 0)
