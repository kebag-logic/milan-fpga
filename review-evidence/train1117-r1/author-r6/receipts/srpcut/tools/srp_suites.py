"""srp_suites.py CLONE OUT [SUITE...]: the SRP arms of test_ctrl_firmware.py's run_suites on CLONE, alone (scratch,
#665's ruling of 2026-11-20, item 3): srp_mbx.cpp and its debug arm at one and two interfaces, the named suites at
both (srp_rx_retry.cpp, srp_app.cpp, test_acmp_mbx.cpp, srp_latency.cpp and srp_walk.cpp by default), then the
talker, listener and 8x8 entity arms, and the RV32 shapes. Built and run as the runner builds them."""
import sys
from pathlib import Path

clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
suites = sys.argv[3:] or ["srp_rx_retry.cpp", "srp_app.cpp", "test_acmp_mbx.cpp", "srp_latency.cpp", "srp_walk.cpp"]
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
import test_ctrl_firmware as t  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import Tree, CTRL  # noqa: E402
import fw_gtest  # noqa: E402

lwsrp = clone / "third_party/lwSRP"
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
t.cut_reuse(tree.reuse)
outcomes = []
for i in (1, 2):
    outcomes.append(srp_arms.arm_srp(tree, lwsrp, i))
    outcomes.append(srp_arms.arm_srp(tree, lwsrp, i, debug=True))
    for suite in suites:
        outcomes.append(srp_arms.arm_srp(tree, lwsrp, i, test=suite))
outcomes.extend(srp_arms.talker_arms(tree, lwsrp))
outcomes.extend(srp_arms.listener_arms(tree, lwsrp))
outcomes.extend(srp_arms.mbx_entity_arms(tree, lwsrp))
outcomes.extend(srp_arms.all_shapes(tree, lwsrp, True))
bad = 0
for o in outcomes:
    tail = [l for l in o.log.splitlines() if l.strip()][-1:] if o.log else []
    print(f"{o.arm:60s} rc={o.rc} {tail[0][:120] if tail else ''}")
    bad += o.rc != 0
print(f"SRP arms: {len(outcomes)} run, {bad} failed")
sys.exit(1 if bad else 0)
