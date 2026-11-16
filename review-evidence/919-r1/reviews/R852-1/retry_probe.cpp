// Review probe: a PHY latches its advertised abilities at negotiation start.
// The existing test fixture supplies the pin-level bus and exact-head firmware.
#include "test_plat_phy.cpp"

namespace {
TEST_F(PlatPhy, ReviewRetryMustActivateTheVerifiedAdvertisement) {
    peer.gigabit(7u);
    peer.regs[10] = 0u; // partner supports 100BASE-TX full duplex only
    peer.regs[5] = 0x0101u;
#ifdef REVIEW_NO_WRITE_FAULT
    peer.ignored = 32u;
#else
    peer.ignored = 4u; // transient configuration-write failure
#endif
    peer.link(false);
    arm_again();
    unsigned negotiation_starts = peer.restarts;
    unsigned latched_anar = 0;
    unsigned active_speed = 0;
    auto opportunity = [&]() {
        const bool owed = call(now);
        if (peer.restarts != negotiation_starts) {
            negotiation_starts = peer.restarts;
            latched_anar = peer.regs[4];
            // Clause 28/40 negotiation uses the abilities latched at restart.
            active_speed = (latched_anar & peer.regs[5] & 0x0100u) ? 100u : 0u;
            peer.link(active_speed != 0u);
        }
        return owed;
    };
    for (unsigned i = 0; i < 64 && opportunity(); ++i) {}
    EXPECT_EQ(peer.restarts, 1u);
#ifdef REVIEW_NO_WRITE_FAULT
    EXPECT_EQ(active_speed, 0u);
#else
    EXPECT_EQ(active_speed, 100u);
#endif
    peer.ignored = 32u; // all later accesses succeed
    for (unsigned period = 0; period < 10u; ++period) {
        now += CTRL_PLAT_PHY_POLL_US;
        for (unsigned i = 0; i < 64 && opportunity(); ++i) {}
    }
    std::printf("RETRY-PROBE register4=%04x advertised-at-last-restart=%04x active-Mbps=%u restarts=%u owed=%u published=%u\n",
                peer.regs[4], latched_anar, active_speed, peer.restarts, phy.adv, peer.word);
    EXPECT_EQ(peer.regs[4], 0x0001u) << "the configuration write eventually succeeds";
    EXPECT_EQ(phy.adv, 0u) << "the driver considers readback verified";
    EXPECT_EQ(latched_anar & 0x01e0u, 0u) << "verified abilities must reach the active negotiation";
    EXPECT_EQ(active_speed, 0u) << "a 100BASE-TX-only partner must have no physical link after repair";
}
} // namespace
