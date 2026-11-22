"""RV32 srp_mbx.o of a checkout at a shape (srp_arms.arm_srp_rv32): the sizes of the functions the delta touches.
Usage: python3 -B rv32_fn_sizes.py <checkout> <out> <interfaces> <config>"""
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import fw_gtest, fw_rv32, srp_arms  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
out = Path(sys.argv[2]).resolve()
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
o = srp_arms.arm_srp_rv32(tree, (root / "third_party/lwSRP").resolve(), int(sys.argv[3]), root / sys.argv[4])
print("ARM", o.arm, "rc", o.rc, o.log.splitlines()[-1] if o.log else "")
nm = fw_rv32.compiler().removesuffix("gcc") + "nm"
obj = out / "checkout" / o.arm / "srp_srp_mbx.o"
want = ("transmit", "transmit_aged", "poll", "reset_interface", "tick")
for line in subprocess.run([nm, "-S", str(obj)], capture_output=True, text=True).stdout.splitlines():
    f = line.split()
    if len(f) == 4 and f[3] in want:
        print("SYM", f[3], int(f[1], 16))
print("SIZE", subprocess.run([nm.removesuffix("nm") + "size", str(obj)], capture_output=True, text=True).stdout.strip().splitlines()[-1])
