// Reviewer probes for PR #933 at 1a1e6665 (inserted before test_plat_phy.cpp's closing namespace brace by
// scripts/probe.sh). Each prints its measured figures; EXPECT lines state what the round-4 design claims.

// A PHY that brings a 100 Mb/s link up after every restart whatever it advertises (a partner that does not
// autonegotiate, parallel-detected, or a PHY that downshifts): the restart loop's rate and what is published.
TEST_F(PlatPhy, RvProbeParallelDetectLoop) {
    hundred_in_force(*this);
    peer.negotiates = false;
    arm_again();
    (void)poll(now);
    const unsigned r0 = peer.restarts;
    for (unsigned k = 0; k < 20u; ++k) {
        peer.link(true);
        peer.regs[1] |= 0x0020u;
        peer.regs[10] = 0x0000u;
        next();
    }
    std::printf("PROBE parallel-detect: boot restarts=%u, 20 polls restarts=%u renegotiations=%u below_gig=%zu\n", r0,
                peer.restarts - r0, phy.renegotiations, below_gigabit(*this, 0).size());
    EXPECT_TRUE(below_gigabit(*this, 0).empty()) << "probe: no 100 link published";
    EXPECT_LE(peer.restarts - r0, 20u) << "probe: at most one restart a poll";
}

// A restart that takes but whose link drop lags past the poll's next BMSR read: the stale 100 Mb/s link is
// judged once; the loop must stop once the PHY has renegotiated.
TEST_F(PlatPhy, RvProbeSlowRestart) {
    hundred_in_force(*this);
    peer.negotiates = false;
    arm_again();
    (void)poll(now);
    const unsigned after_boot = peer.restarts;
    const unsigned owed = phy.renegotiations;
    peer.negotiate();   // the boot's restart completes late: gigabit-only, 100-only partner, no link
    for (unsigned k = 0; k < 10u; ++k) {
        const unsigned before = peer.restarts;
        next();
        if (peer.restarts != before) peer.negotiate();   // each later restart completes before the next poll
    }
    std::printf("PROBE slow-restart: boot restarts=%u owed-at-boot=%u, then restarts=%u renegotiations=%u "
                "active=%u word=%u\n", after_boot, owed, peer.restarts - after_boot, phy.renegotiations,
                peer.active_speed, peer.word);
    EXPECT_LE(peer.restarts - after_boot, 1u) << "probe: one extra restart at most";
    EXPECT_EQ(peer.active_speed, 0u);
    EXPECT_TRUE(below_gigabit(*this, 0).empty());
}

// The reviewer's F1 case with the second poll's restart also lost: register 4's writes dropped on the first poll,
// then the repair's register-0 write lost once; a 100BASE-TX-only partner.
TEST_F(PlatPhy, RvProbeRepairThenRestartLost) {
    peer.gigabit(7u);
    peer.negotiates = true;
    peer.regs[5] = 0x0101u;
    peer.regs[10] = 0x0000u;
    peer.link(false);
    peer.ignored = 4u;
    arm_again();
    (void)poll(now);
    const std::size_t boot_pubs = peer.published.size();
    const auto boot_below = below_gigabit(*this, 0).size();
    peer.ignored = 32u;
    peer.drop_restarts = 1u;
    for (unsigned k = 0; k < 10u; ++k) next();
    std::printf("PROBE F1+lost-restart: boot below-gig publications=%zu (of %zu), total below-gig=%zu, "
                "restarts=%u renegotiations=%u active=%u anar=%04x adv=%u word=%u\n", boot_below, boot_pubs,
                below_gigabit(*this, 0).size(), peer.restarts, phy.renegotiations, peer.active_speed,
                peer.active_anar, phy.adv, peer.word);
    EXPECT_EQ(peer.active_speed, 0u) << "probe: no link at 100 after recovery";
    EXPECT_EQ(peer.active_anar & 0x03e0u, 0u);
    EXPECT_EQ(peer.word, 0u);
}

// Register 4's write and the restart both lost at boot, a 100 Mb/s link in force before boot: is the earlier
// link published, and for how long?
TEST_F(PlatPhy, RvProbeBothLostAtBoot) {
    hundred_in_force(*this);
    peer.ignored = 4u;
    peer.drop_restarts = 1u;
    arm_again();
    (void)poll(now);
    const auto boot_words = words_since(0);
    peer.ignored = 32u;
    for (unsigned k = 0; k < 10u; ++k) next();
    std::printf("PROBE both-lost-at-boot: boot words=");
    for (const auto w : boot_words) std::printf("%u ", w);
    std::printf("; all words=");
    for (const auto w : words_since(0)) std::printf("%u ", w);
    std::printf("; restarts=%u renegotiations=%u active=%u\n", peer.restarts, phy.renegotiations,
                peer.active_speed);
    EXPECT_EQ(peer.active_speed, 0u) << "probe: no link at 100 after recovery";
}

// A PHY in forced 100BASE-TX full duplex before boot whose restart write is lost: published as the release
// publishes a forced mode (stated as known).
TEST_F(PlatPhy, RvProbeForcedModeRestartLost) {
    hundred_in_force(*this);
    peer.regs[0] = 0x2100u;   // speed 100, full duplex, autonegotiation off
    peer.drop_restarts = 1u;
    arm_again();
    (void)poll(now);
    for (unsigned k = 0; k < 5u; ++k) next();
    std::printf("PROBE forced-100: word=%u restarts=%u renegotiations=%u below_gig=%zu\n", peer.word, peer.restarts,
                phy.renegotiations, below_gigabit(*this, 0).size());
    SUCCEED();
}

// The same PHY with a realistic restart: a restart drops the link and clears negotiation complete, and the
// sub-gigabit link (parallel detection or a downshift) returns 8 polls (about 1 s) later. The loop's real rate.
TEST_F(PlatPhy, RvProbeParallelDetectLoopTimed) {
    hundred_in_force(*this);
    peer.negotiates = false;
    peer.restart_drops = true;   // a restart drops the link at once (latched low)
    arm_again();
    unsigned down_for = 0;
    for (unsigned k = 0; k < 90u; ++k) {
        const unsigned before = peer.restarts;
        if (k == 0) (void)poll(now); else next();
        if (peer.restarts != before) {
            peer.link(false);
            peer.regs[1] &= static_cast<std::uint16_t>(~0x0020u);
            down_for = 8;

        } else if (down_for != 0 && --down_for == 0) {
            peer.link(true);
            peer.regs[1] |= 0x0020u;
            peer.regs[10] = 0x0000u;
        }
    }
    std::printf("PROBE parallel-detect-timed: 90 polls (11.25 s): restarts=%u renegotiations=%u below_gig=%zu "
                "word=%u\n", peer.restarts, phy.renegotiations, below_gigabit(*this, 0).size(), peer.word);
    EXPECT_TRUE(below_gigabit(*this, 0).empty());
}
