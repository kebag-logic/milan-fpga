#!/usr/bin/env python3
"""The firmware arms the composition touches, run through the checkout's own arm functions as test_ctrl_firmware.py
runs them: the platform arms (test_plat.cpp's K1 VERSION line and plat_bus.hpp's kVersion moved by #960), the sink
arms at both shapes (test_plat_sinks.cpp, this PR's S13/S14/T1, built on that plat_bus.hpp), and every AECP arm.

usage: fw_targeted.py CHECKOUT BUILD_DIR
"""
import sys
from pathlib import Path

clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(clone / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(clone / 'sw/firmware/gtest'))
import fw_gtest  # noqa: E402
import test_ctrl_firmware as t  # noqa: E402
import plat_arms  # noqa: E402
import aecp_arms  # noqa: E402

tree = t.Tree(t.CTRL, out / 'checkout', out / 'reuse', fw_gtest.Build(jobs=4))
print(f'toolchain: {fw_gtest.toolchain()}', flush=True)
outcomes = []
for make in (lambda: [plat_arms.arm_plat(tree)], lambda: plat_arms.sink_arms(tree),
             lambda: [plat_arms.arm_platboot(tree, 1), plat_arms.arm_platboot(tree, 2)],
             lambda: aecp_arms.all_arms(tree)):
    for o in make():
        outcomes.append(o)
        tail = [ln for ln in o.log.splitlines() if ln.strip()][-3:]
        print(f'ARM {o.arm} rc={o.rc} :: ' + ' | '.join(tail)[:400], flush=True)
        (out / f'arm-{len(outcomes):02d}-{o.arm}.log').write_text(o.log)
failed = [o.arm for o in outcomes if o.rc != 0]
print(f'fw_targeted: {len(outcomes)} arms, failed {failed}', flush=True)
sys.exit(1 if failed else 0)
