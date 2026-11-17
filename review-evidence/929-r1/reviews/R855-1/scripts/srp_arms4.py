#!/usr/bin/env python3
"""srp_arms4.py <tree-root> <build-dir> [suite]: the suite (default srp_mbx.cpp) through srp_arms.arm_srp at the
1x1 and 8x8 AX7101 entities, each at one and two interfaces; prints each arm's tally and failing tests, rc 1 if any
arm failed."""
import sys
from pathlib import Path
root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
suite = sys.argv[3] if len(sys.argv) > 3 else "srp_mbx.cpp"
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import fw_gtest  # noqa: E402
from ctrl_build import Tree, CTRL  # noqa: E402
import srp_arms  # noqa: E402
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
bad = False
for config in ("endstation_ax7101_1x1_tdm8.yaml", "endstation_ax7101_8x8.yaml"):
    for i in (1, 2):
        o = srp_arms.arm_srp(tree, root / "third_party/lwSRP", i, test=suite, config=root / "configs" / config)
        print(f"== {o.arm}: rc {o.rc}")
        for line in o.log.splitlines():
            if line.startswith(("[==========]", "[  PASSED  ]", "[  FAILED  ]", "[FAIL]")) or "Failure" in line:
                print("   " + line)
        bad |= bool(o.rc)
sys.exit(1 if bad else 0)
