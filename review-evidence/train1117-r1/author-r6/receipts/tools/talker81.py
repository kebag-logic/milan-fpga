#!/usr/bin/env python3
"""talker81.py CLONE OUT: srp_talker.cpp (the host tests that read CTRL_LOOP_TX_MS: kHoldOffMs and kLatestLeaveMs) at
each shape it runs at and at 8x8/1if, the shape whose CTRL_LOOP_TX_MS the final head restates, through srp_arms.arm_srp
exactly as test_ctrl_firmware.py runs it. Scratch only; prints each arm's outcome."""
import sys
from pathlib import Path

clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(clone / 'sw/firmware/ctrl/test'), str(clone / 'sw/firmware/gtest')]
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

tree = Tree(CTRL, out / 'checkout', out / 'reuse', fw_gtest.Build(jobs=4))
cut_reuse(tree.reuse)
lwsrp = (CTRL.parents[2] / 'third_party/lwSRP').resolve()
arms = [('1x1/1if', srp_arms.arm_srp(tree, lwsrp, 1, test='srp_talker.cpp')),
        ('8x8/1if', srp_arms.arm_srp(tree, lwsrp, 1, test='srp_talker.cpp', config=srp_arms.ENTITY_8X8)),
        ('8x8/2if', srp_arms.arm_srp(tree, lwsrp, 2, test='srp_talker.cpp', config=srp_arms.ENTITY_8X8))]
bad = 0
for point, o in arms:
    print(f'{point}: {o.arm} rc={o.rc}')
    tail = [l for l in str(o.log).splitlines() if '[  PASSED' in l or '[  FAILED' in l or 'tests ran' in l]
    print('   ', ' | '.join(tail[-3:]))
    bad += o.rc != 0
sys.exit(1 if bad else 0)
