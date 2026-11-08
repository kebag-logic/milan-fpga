"""Run ctrl_service_bounds.arm_service_bounds (the reader of MAILBOX_SPLIT.md's
service figures, rtl-fast firmware-unit) on the clone. Usage:
    python3 -I service_bounds_arm.py <clone> <outdir>"""
import sys
from pathlib import Path

clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(clone / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_service_bounds import arm_service_bounds  # noqa: E402

assert CTRL == clone / "sw/firmware/ctrl", CTRL
out.mkdir(parents=True, exist_ok=True)
res = arm_service_bounds(Tree(CTRL, out / "build", out / "reuse", fw_gtest.Build(jobs=1)))
print(res.log if hasattr(res, "log") else res)
print("rc", res.rc if hasattr(res, "rc") else res)
sys.exit(1 if getattr(res, "rc", 1) else 0)
