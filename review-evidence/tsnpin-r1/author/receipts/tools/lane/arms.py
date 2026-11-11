"""arms.py <root> <out> <arm,...>: run only the named ctrl_arms arms of test_ctrl_firmware.py at <root>."""
import sys
from pathlib import Path
root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import test_ctrl_firmware as t, ctrl_arms, fw_gtest, srp_arms, plat_arms
tree = t.Tree(t.CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
print("tsn-c-stack at", t.stack_pin(), flush=True)
t.cut_reuse(tree.reuse)
res = []
lw = (root / "third_party/lwSRP").resolve()
for n in sys.argv[3].split(","):
    if n.startswith("srp:"):
        _, i, suite = n.split(":")
        res.append(srp_arms.arm_srp(tree, lw, int(i), test=suite))
    elif n == "rv32":
        res.append(ctrl_arms.arm_rv32(tree, True))
    elif n == "platrv32":
        res.append(plat_arms.arm_platrv32(tree, True))
    else:
        res.append(getattr(ctrl_arms, "arm_" + n)(tree))
sys.exit(1 if ctrl_arms.report(res) else 0)
