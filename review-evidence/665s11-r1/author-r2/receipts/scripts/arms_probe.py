#!/usr/bin/env python3
"""Run selected host arms of the lane's firmware: arms.py OUT [platboot1 platboot2 aecp] [--filter GTEST]"""
import sys
from pathlib import Path
ROOT = Path('<scratch>/probes/wt')
TEST = ROOT / 'sw/firmware/ctrl/test'
sys.path.insert(0, str(TEST)); sys.path.insert(0, str(ROOT / 'sw/firmware/gtest'))
import aecp_arms, fw_gtest, plat_arms  # noqa: E402
from ctrl_build import CTRL, STACK, Tree  # noqa: E402
out = Path(sys.argv[1]); arms = sys.argv[2:] or ['platboot1']
tree = Tree(CTRL, out / 'build', out / 'reuse', fw_gtest.Build(jobs=4), STACK)
rc = 0
for arm in arms:
    if arm.startswith('platboot'):
        o = plat_arms.arm_platboot(tree, int(arm[-1]))
    else:
        o = aecp_arms.core_arm(tree, ROOT / 'configs/endstation_ax7101_1x1_tdm8.yaml', 2, 'app', 'Core.*')
    (out / f'{arm}.log').write_text(o.log)
    fails = [l for l in o.log.splitlines() if '[FAIL]' in l or 'FAILED' in l or 'error' in l.lower()]
    print(f'{arm}: rc={o.rc}'); print('\n'.join(fails[:40]))
    rc |= o.rc
sys.exit(rc)
