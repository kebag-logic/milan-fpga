"""RV32 SRP objects of a checkout at a shape (srp_arms.arm_srp_rv32), and listener's size (reviewer receipt).
Usage: python3 -B rv32_srp_size.py <checkout> <out> <interfaces> <config>"""
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import fw_gtest, fw_rv32, srp_arms  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
out = Path(sys.argv[2]).resolve()
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
o = srp_arms.arm_srp_rv32(tree, (root / "third_party/lwSRP").resolve(), int(sys.argv[3]), root / sys.argv[4])
print(o.log.splitlines()[-1])
nm = fw_rv32.compiler().removesuffix("gcc") + "nm"
obj = out / "checkout" / o.arm / "srp_srp_mbx.o"
for line in subprocess.run([nm, "-S", "--size-sort", str(obj)], capture_output=True, text=True).stdout.splitlines():
    if line.endswith((" listener", " declare_sources")):
        print("SYM", line, int(line.split()[1], 16))
print("SIZE", subprocess.run([nm.removesuffix("nm") + "size", str(obj)], capture_output=True, text=True).stdout.strip().splitlines()[-1])
