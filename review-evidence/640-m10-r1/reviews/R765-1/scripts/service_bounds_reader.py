"""Run the repository's MAILBOX_SPLIT.md service-figure reader (ctrl_service_bounds.arm_service_bounds).

Usage: python3 -I service_bounds_reader.py <clone> <build-dir>
Exits 0 only when the arm reports success.
"""
import sys
from pathlib import Path

clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(clone / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_service_bounds import arm_service_bounds  # noqa: E402

if CTRL != clone / "sw/firmware/ctrl":
    sys.exit(f"ctrl_build resolved {CTRL}, not the clone under review")
out.mkdir(parents=True, exist_ok=True)
res = arm_service_bounds(Tree(CTRL, out / "build", out / "reuse", fw_gtest.Build(jobs=1)))
print(getattr(res, "log", res))
rc = getattr(res, "rc", 1)
print("rc", rc)
sys.exit(1 if rc else 0)
