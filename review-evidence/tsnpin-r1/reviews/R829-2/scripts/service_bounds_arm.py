"""Reviewer probe: run the firmware gate's service_bounds arm (MAILBOX_SPLIT.md held to the compiled headers).
Usage: python3 -I service_bounds_arm.py <checkout> <workdir>"""
import sys
from pathlib import Path
co, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(co / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(co / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_service_bounds import arm_service_bounds  # noqa: E402
work.mkdir(parents=True, exist_ok=True)
o = arm_service_bounds(Tree(CTRL, work / "build", work / "reuse", fw_gtest.Build(jobs=4)))
print(o.log)
print("rc", o.rc)
sys.exit(o.rc)
