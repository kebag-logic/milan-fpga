"""Run the firmware suites the composition reaches (ADP, the platform and its boot at one and two interfaces,
the store-backed ACMP suite) through test_ctrl_firmware.py's own Tree, arms and report.
Usage: python3 -B focused_arms.py <checkout> <build-dir> <jobs>."""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import test_ctrl_firmware as t  # noqa: E402
import ctrl_arms, plat_arms, fw_gtest  # noqa: E402,E401
out = Path(sys.argv[2]).resolve()
tree = t.Tree(t.CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=int(sys.argv[3])))
print(f"toolchain: {fw_gtest.toolchain()}")
print(f"tsn-c-stack at {t.stack_pin()}")
t.cut_reuse(tree.reuse)
outcomes = [ctrl_arms.arm_adp(tree), plat_arms.arm_plat(tree), plat_arms.arm_platboot(tree, 1),
            plat_arms.arm_platboot(tree, 2), ctrl_arms.arm_acmpnvm(tree)]
failed = ctrl_arms.report(outcomes)
print(f"focused arms: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
