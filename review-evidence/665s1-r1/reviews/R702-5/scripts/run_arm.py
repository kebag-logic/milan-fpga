# Build and run one AECP host arm from the reviewed checkout, optionally with a
# different test_aecp.cpp (a probe copy). Outputs stay under --output.
# REVIEW_SRC, if set, names a planted copy of sw/firmware/ctrl to build instead.
# usage: python3 -B run_arm.py REPO OUTPUT MODE IF [TESTDIR] [FILTER] [--asan]
import sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]).resolve()
mode = sys.argv[3]; interfaces = int(sys.argv[4])
testdir = Path(sys.argv[5]).resolve() if len(sys.argv) > 5 and sys.argv[5] != "-" else None
selected = sys.argv[6] if len(sys.argv) > 6 else "*"
asan = "--asan" in sys.argv
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_arms, fw_gtest
from ctrl_build import CTRL, STACK, Tree
if testdir is not None:
    aecp_arms.HERE = testdir
build = fw_gtest.Build(coverage=False, address_sanitizer=asan, jobs=4)
import os
src = Path(os.environ["REVIEW_SRC"]).resolve() if os.environ.get("REVIEW_SRC") else CTRL
tree = Tree(src, out, out / "reuse", build, STACK.resolve())
cfg = repo / "configs/endstation_ax7101_1x1_tdm8.yaml"
r = aecp_arms.core_arm(tree, cfg, interfaces, mode, selected)
print(r.log)
raise SystemExit(r.rc)
