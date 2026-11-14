#!/usr/bin/env python3
"""arms.py TREE OUT NAME...: run the named arms of TREE's firmware suite (test_ctrl_firmware.py's own arm functions,
its Tree and build), each Outcome reported by ctrl_arms.report; exit 1 when any failed. Names: maap, maap_if2,
maap_debug, acmp, acmpif2, srp-acmp-if1, srp-acmp-if2, talker, platboot, plat, unit, hot, rv32, service."""
import sys
from pathlib import Path

tree_root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
names = sys.argv[3:]
sys.path.insert(0, str(tree_root / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(tree_root / 'sw/firmware/gtest'))
import ctrl_arms  # noqa: E402
import srp_arms  # noqa: E402
import plat_arms  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree, stack_pin  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

lwsrp = (tree_root / 'third_party/lwSRP').resolve()
out.mkdir(parents=True, exist_ok=True)
tree = Tree(CTRL, out / 'build', out / 'reuse', fw_gtest.Build(jobs=4))
print(f"tsn-c-stack at {stack_pin()}", flush=True)
cut_reuse(tree.reuse)
table = {
    'maap': lambda: [ctrl_arms.arm_maap(tree)],
    'maap_if2': lambda: [ctrl_arms.arm_maap_if2(tree)],
    'maap_debug': lambda: [ctrl_arms.arm_maap_debug(tree)],
    'acmp': lambda: [ctrl_arms.arm_acmp(tree)],
    'acmpif2': lambda: [ctrl_arms.arm_acmpif2(tree)],
    'unit': lambda: [ctrl_arms.arm_unit(tree)],
    'hot': lambda: [ctrl_arms.arm_hot()],
    'service': lambda: [ctrl_arms.arm_service_bounds(tree)],
    'rv32': lambda: [ctrl_arms.arm_rv32(tree, True)],
    'srp-acmp-if1': lambda: [srp_arms.arm_srp(tree, lwsrp, 1, test='test_acmp_mbx.cpp')],
    'srp-acmp-if2': lambda: [srp_arms.arm_srp(tree, lwsrp, 2, test='test_acmp_mbx.cpp')],
    'talker': lambda: srp_arms.talker_arms(tree, lwsrp),
    'platboot': lambda: [plat_arms.arm_platboot(tree, 1), plat_arms.arm_platboot(tree, 2)],
    'plat': lambda: plat_arms.all_arms(tree, True),
}
outcomes = []
for n in names:
    outcomes.extend(table[n]())
failed = ctrl_arms.report(outcomes)
print(f"arms {' '.join(names)}: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
