#!/usr/bin/env python3
"""run_fg5.py REPO OUT: F-G5's two tests in the firmware harness, built and run in REPO into OUT: the sink suite
(test_plat_sinks.cpp) at both of its shapes, 8x8/1if and 1x1/1if (plat_arms.arm_platsinks), and the AECP suite's
Face tests on the mailbox model (aecp_arms.core_arm, app mode, the shipping config, one interface). GTEST_FILTER
narrows the sink suite when set. Prints each outcome and exits 0 when all pass."""
import os
import sys
from pathlib import Path

repo, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(repo / 'sw/firmware/gtest'))
import aecp_arms  # noqa: E402
import ctrl_build  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402

out.mkdir(parents=True, exist_ok=True)
tree = ctrl_build.Tree(repo / 'sw/firmware/ctrl', out / 'checkout', out / 'reuse', fw_gtest.Build(jobs=8))
rc = 0
for config, n in plat_arms.SINK_SHAPES:
    try:
        outcome = plat_arms.arm_platsinks(tree, config, n)
    except Exception as exc:  # the harness's Refusal and anything else: a failed run
        print(f'platsinks {config.stem}: REFUSED: {type(exc).__name__}: {exc}')
        rc = 1
        continue
    print(f'== platsinks {config.stem} rc={outcome.rc}')
    print('\n'.join(ln for ln in outcome.log.splitlines() if 'S12' in ln or '[  FAILED' in ln or 'checks:' in ln))
    rc |= outcome.rc != 0
os.environ.pop('GTEST_FILTER', None)
face = aecp_arms.core_arm(tree, plat_arms.SHIPPING, 1, 'app', 'Face.*')
print(f'== aecp app Face.* rc={face.rc}')
print('\n'.join(ln for ln in face.log.splitlines() if 'FormatVerdict' in ln or '[  FAILED' in ln or 'checks:' in ln
                or 'PASSED' in ln))
rc |= face.rc != 0
print(f'run_fg5 rc={rc}')
sys.exit(rc)
