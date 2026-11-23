#!/usr/bin/env python3
"""Run named arms of milan-fpga's firmware gate (lane-local driver, not committed).

The arms are the gate's own functions, on the gate's own Tree, exactly as
test_ctrl_firmware.run_suites calls them; only the selection differs.

usage: fw_arms.py REPO ARM...   (ARM: service_bounds | srp_all_shapes | aecp_all | plat_all | plat_sinks)
"""
import sys
import tempfile
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_arms  # noqa: E402
import ctrl_arms  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, Refusal, Tree, stack_pin  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

lwsrp = (repo / "third_party/lwSRP").resolve()
ARMS = {
    "service_bounds": lambda t: [ctrl_arms.arm_service_bounds(t)],
    "srp_all_shapes": lambda t: srp_arms.all_shapes(t, lwsrp, True),
    "aecp_all": lambda t: aecp_arms.all_arms(t),
    "plat_all": lambda t: plat_arms.all_arms(t, True),
    "plat_sinks": lambda t: plat_arms.sink_arms(t),
}
print(f"toolchain: {fw_gtest.toolchain()}")
with tempfile.TemporaryDirectory(prefix="ctrl-fw-arms-") as tmp:
    try:
        tree = Tree(CTRL, Path(tmp) / "checkout", Path(tmp) / "reuse", fw_gtest.Build(jobs=4))
        print(f"tsn-c-stack at {stack_pin()}")
        cut_reuse(tree.reuse)
        outcomes = [o for name in sys.argv[2:] for o in ARMS[name](tree)]
    except Refusal as exc:
        print(f"REFUSED: {exc}")
        sys.exit(2)
failed = ctrl_arms.report(outcomes)
print(f"fw_arms {' '.join(sys.argv[2:])}: {'FAIL' if failed else 'PASS'} ({len(outcomes)} arm(s))")
sys.exit(1 if failed else 0)
