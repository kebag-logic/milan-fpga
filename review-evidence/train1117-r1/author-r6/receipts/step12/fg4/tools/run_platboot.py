#!/usr/bin/env python3
"""run_platboot.py REPO OUT [FILTER]: the firmware harness's platboot arm alone (ctrl_plat.c's boot and composition,
with test_plat_boot.cpp and test_plat_phy.cpp, at the shipping shape, one interface), built and run in REPO into
OUT. FILTER, a gtest filter, narrows the run (GTEST_FILTER). Prints the outcome and exits 0 on a pass."""
import os
import sys
from pathlib import Path

repo, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
if len(sys.argv) > 3:
    os.environ['GTEST_FILTER'] = sys.argv[3]
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(repo / 'sw/firmware/gtest'))
import ctrl_build  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402

out.mkdir(parents=True, exist_ok=True)
tree = ctrl_build.Tree(repo / 'sw/firmware/ctrl', out / 'checkout', out / 'reuse', fw_gtest.Build(jobs=8))
try:
    outcome = plat_arms.arm_platboot(tree, 1)
except Exception as exc:  # the harness's Refusal and anything else: a failed run
    print(f'REFUSED: {type(exc).__name__}: {exc}')
    sys.exit(2)
print(outcome.log[-6000:])
print(f'platboot rc={outcome.rc}')
sys.exit(0 if outcome.rc == 0 else 1)
