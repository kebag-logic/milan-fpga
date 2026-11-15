#!/usr/bin/env python3
"""platboot.py REPO OUT: run the split platform's boot arm (test_plat_boot.cpp) at one and two
interfaces from REPO's sources, builds under OUT; prints each arm's rc and its log's tail."""
import sys
from pathlib import Path
repo, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path[:0] = [str(repo / 'sw/firmware/ctrl/test'), str(repo / 'sw/firmware/gtest')]
import fw_gtest
import plat_arms
from ctrl_build import CTRL, Tree
tree = Tree(CTRL, out / 'checkout', out / 'reuse', fw_gtest.Build(jobs=4))
rc = 0
for n in (1, 2):
    o = plat_arms.arm_platboot(tree, n)
    print(f'== platboot if{n} rc={o.rc}')
    print('\n'.join(o.log.splitlines()[-12:]))
    rc |= o.rc
sys.exit(1 if rc else 0)
