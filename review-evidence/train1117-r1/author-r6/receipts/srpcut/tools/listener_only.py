"""listener_only.py CLONE OUT: srp_listeners.cpp at 1x1/1if and 8x8/1if (srp_arms.listener_arms), scratch."""
import sys
from pathlib import Path
clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
import test_ctrl_firmware as t  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import Tree, CTRL  # noqa: E402
import fw_gtest  # noqa: E402
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
t.cut_reuse(tree.reuse)
bad = 0
for o in srp_arms.listener_arms(tree, clone / "third_party/lwSRP"):
    print(f"== {o.arm} rc={o.rc}")
    print("\n".join(l for l in o.log.splitlines() if "FAIL" in l or "OK ]" in l or "Failure" in l or "Expected" in l
                    or "Which is" in l or "the cut" in l or "RESULT" in l or "checks:" in l)[:6000])
    bad += o.rc != 0
sys.exit(1 if bad else 0)
