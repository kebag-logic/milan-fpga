import sys
from pathlib import Path
R = Path(sys.argv[1]); W = Path(sys.argv[2])
sys.path[:0] = [str(R / "sw/firmware/gtest"), str(R / "sw/firmware/ctrl/test")]
import ctrl_arms
from ctrl_build import CTRL, Tree
got = ctrl_arms.arm_rv32(Tree(CTRL, W / "build", W / "reuse"), True)
print(got.log); print("rc", got.rc); sys.exit(1 if got.rc else 0)
