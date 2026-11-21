"""Run srp_talker.cpp's ReviewerPhase.* probe of a checkout at one shape (reviewer receipt).
Usage: python3 -B phase_arm.py <checkout> <out> <interfaces> <config>"""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import fw_gtest, srp_arms  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
out = Path(sys.argv[2]).resolve()
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
o = srp_arms.arm_srp(tree, (root / "third_party/lwSRP").resolve(), int(sys.argv[3]),
                     test=("srp_talker.cpp", "ReviewerPhase.*:Talker.ChangedDestination*"), config=root / sys.argv[4])
print(o.log)
sys.exit(o.rc)
