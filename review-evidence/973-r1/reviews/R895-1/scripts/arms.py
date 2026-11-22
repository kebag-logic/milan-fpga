#!/usr/bin/env python3
"""arms.py CTRL_TEST_DIR OUT SPEC...: run single SRP host arms of the firmware gate on the checkout holding
CTRL_TEST_DIR (the firmware sources from $ARMS_SRC when set), each SPEC `suite[:filter]@interfaces@config-stem` (srp_arms.arm_srp). Prints each verdict and its log."""
import os
import sys
from pathlib import Path

here = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(here))
sys.path.insert(0, str(here.parents[1] / "gtest"))
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, ROOT, Tree  # noqa: E402

src = Path(os.environ.get("ARMS_SRC", str(CTRL))).resolve()  # a firmware source override (a probe copy)
print(f"firmware sources: {src}", flush=True)
tree = Tree(src, out / "checkout", out / "reuse", fw_gtest.Build(jobs=int(os.environ.get("ARMS_JOBS", "4"))))
lwsrp = (CTRL.parents[2] / "third_party/lwSRP").resolve()
bad = 0
for spec in sys.argv[3:]:
    test, n, stem = spec.split("@")
    suite, _, flt = test.partition(":")
    o = srp_arms.arm_srp(tree, lwsrp, int(n), test=(suite, flt) if flt else suite,
                         config=ROOT / "configs" / f"{stem}.yaml")
    print(f"=== {spec} arm={o.arm} rc={o.rc}", flush=True)
    print(o.log, flush=True)
    bad += o.rc != 0
print(f"ARMS {'FAIL' if bad else 'PASS'} ({bad} failed of {len(sys.argv) - 3})")
sys.exit(1 if bad else 0)
