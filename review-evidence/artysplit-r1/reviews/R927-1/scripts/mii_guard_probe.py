#!/usr/bin/env python3
"""Run the platmii arm (test_plat_phy_mii.cpp) on a copy of sw/firmware/ctrl,
optionally with one planted defect, and print the arm's rc and log.

usage: python3 -I mii_guard_probe.py <repo> <workdir> <mode>
  mode: clean      the sources as committed
        noguard    the CTRL_PLAT_PHY_100_ONLY publish guard removed (a
                   resolved mode other than 100 Mb/s full duplex is published)
        forcedten  clean sources; the test file gains one case (a PHY that
                   keeps autonegotiation off at 10 Mb/s full duplex) which
                   must never publish the link up
        forcedten-noguard  both of the above
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

GUARD = (
    "#ifdef CTRL_PLAT_PHY_100_ONLY\n"
    "\t// Never publish a lower-speed or half-duplex port as AVB-capable. If a\n"
    "\t// completed negotiation still resolves another mode, retry a lost restart.\n"
    "\tif (status != 0u && status != up(CTRL_PLAT_PHY_SPEED_100, 1u)) {\n"
    "\t\tstatus = 0u;\n"
    "\t\tphy->adv = CTRL_PLAT_PHY_ADV_OWED | CTRL_PLAT_PHY_ADV_RENEGOTIATE;\n"
    "\t}\n"
    "#endif\n"
)

EXTRA_TEST = r'''
TEST_F(ArtyPhy, ReviewProbeForcedTenNeverPublishesUp) {
    // after a normal boot at 100FD, the PHY drops every BMCR write and holds
    // autonegotiation off at 10 Mb/s full duplex; a latched loss makes the
    // poll re-resolve. The resolved mode is 10FD: never AVB-capable (802.1BA
    // Table 6-1), so the published word must never read link up.
    poll();
    ASSERT_EQ(peer.word & 1u, 1u) << "boot did not reach link up";
    peer.ignored = 0u;
    peer.regs[0] = 0x0100u;
    peer.latched_down = true;
    next();
    EXPECT_EQ(peer.word & 1u, 0u) << "MII forced 10 Mb/s published up (first poll)";
    next();
    EXPECT_EQ(peer.word & 1u, 0u) << "MII forced 10 Mb/s published up (second poll)";
}
'''


def main(argv: list[str]) -> int:
    repo, work, mode = Path(argv[0]).resolve(), Path(argv[1]).resolve(), argv[2]
    sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
    from ctrl_build import CTRL, Tree  # noqa: E402
    import fw_gtest  # noqa: E402
    import plat_arms  # noqa: E402
    if work.exists():
        shutil.rmtree(work)
    src = work / "src"
    shutil.copytree(CTRL, src)
    if mode.endswith("noguard"):
        phy = src / "plat/ctrl_plat_phy.c"
        text = phy.read_text()
        assert text.count(GUARD) == 1, "guard text not found exactly once"
        phy.write_text(text.replace(GUARD, ""))
    if mode.startswith("forcedten"):
        test = Path(plat_arms.HERE) / "test_plat_phy_mii.cpp"
        # the arm reads its tests from HERE (the repo's test dir); plant a copy
        # through a patched HERE so the repo stays untouched
        here = work / "tests"
        shutil.copytree(plat_arms.HERE, here)
        body = test.read_text()
        marker = "}  // namespace\n"
        assert body.count(marker) == 1
        (here / "test_plat_phy_mii.cpp").write_text(body.replace(marker, EXTRA_TEST + marker))
        plat_arms.HERE = here
    tree = Tree(src, work / "out", work / "reuse", fw_gtest.Build(jobs=4))
    outcome = plat_arms.arm_platboot(tree, 1, mii=True)
    print(outcome.log)
    print(f"MODE {mode} ARM {outcome.arm} RC {outcome.rc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
