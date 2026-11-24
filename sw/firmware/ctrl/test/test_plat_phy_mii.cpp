// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The Arty split's Clause-22 policy on a 10/100-only peer (#878).
// Milan v1.2 4.2.1 and IEEE 802.1BA-2011 Table 6-1: 100 Mb/s,
// full duplex; 10 Mb/s and half duplex cannot be AVB ports.

#include <gtest/gtest.h>
#include "fw_gtest.hpp"

FW_TALLY_LABEL("platboot-mii");

#include <cstdint>
#include <vector>

#include "plat_bus.hpp"
#include "ctrl_plat_phy.h"

namespace {

constexpr ctrl_plat_phy_bus kBus = {0xf0002004u, 0xf0002008u, 0xf000201cu};
std::uint64_t clock_us;
std::uint64_t clock_read(void*) { return clock_us; }

struct ArtyPhy : ::testing::Test {
    phy_peer::Peer peer;
    ctrl_plat_phy phy{};
    std::uint32_t now = 1000u;

    void SetUp() override {
        plat_bus::bus().reset();
        peer.w = kBus.mdio_w;
        peer.r = kBus.mdio_r;
        peer.status = kBus.link_status;
        peer.gigabit(1u);
        peer.regs[1] = 0x0024u;
        peer.regs[9] = peer.regs[10] = peer.regs[15] = 0u;
        peer.negotiates = true;
        plat_bus::bus().phy = &peer;
        clock_us = now;
        ctrl_plat_phy_arm(&phy, &kBus, clock_read, nullptr);
    }
    void poll() {
        clock_us = now;
        unsigned n = 0;
        while (n < 64u && ctrl_plat_phy_step(&phy, 2000)) ++n;
        ASSERT_LT(n, 64u);
        ASSERT_TRUE(peer.fault.empty()) << peer.fault;
    }
    void next() {
        now += 125000u;
        poll();
    }
    std::vector<unsigned> writes() const {
        std::vector<unsigned> result;
        for (const auto& f : peer.frames) if (f.write) result.push_back(f.reg);
        return result;
    }
};

TEST_F(ArtyPhy, BootAdvertisesOnly100FullWithoutGigabitRegisters) {
    poll();
    EXPECT_EQ(peer.regs[4], 0x0101u) << "MII only 100 full advertised";
    EXPECT_EQ(peer.active_anar, 0x0101u);
    EXPECT_EQ(peer.active_speed, 100u);
    EXPECT_EQ(peer.word, 11u);
    EXPECT_EQ(peer.restarts, 1u);
    EXPECT_EQ(writes(), (std::vector<unsigned>{4u, 0u}));
    for (const auto& f : peer.frames) {
        EXPECT_NE(f.reg, 9u);
        EXPECT_NE(f.reg, 10u);
        EXPECT_NE(f.reg, 15u);
    }
    next();
    EXPECT_EQ(peer.restarts, 1u);
}

TEST_F(ArtyPhy, TenOnlyPartnerNeverPublishesUp) {
    peer.regs[5] = 0x0061u;
    poll();
    next();
    EXPECT_EQ(peer.active_speed, 0u) << "MII no unsupported negotiation";
    EXPECT_EQ(peer.word, 0u);
    for (const auto& p : peer.published) EXPECT_EQ(p.word, 0u);
}

TEST_F(ArtyPhy, HalfDuplexPartnerNeverPublishesUp) {
    peer.regs[5] = 0x0081u;
    poll();
    EXPECT_EQ(peer.active_speed, 0u) << "MII no unsupported negotiation";
    EXPECT_EQ(peer.word, 0u);
}

TEST_F(ArtyPhy, ForcedTenWithDroppedRestartNeverPublishesUp) {
    // A forced 10BASE-T full-duplex link ignores the attempted AN restart.
    // Advertisement alone cannot reject the mode resolved from BMCR.
    peer.regs[0] = 0x0100u;
    peer.regs[1] = 0x0004u;
    peer.ignored = 0u;
    poll();
    next();
    EXPECT_EQ(peer.regs[0], 0x0100u);
    EXPECT_EQ(peer.word, 0u) << "MII forced 10 Mb/s must stay down";
    for (const auto& p : peer.published) {
        EXPECT_EQ(p.word, 0u) << "MII forced 10 Mb/s must stay down";
    }
    EXPECT_NE(phy.adv, 0u) << "MII unsupported mode keeps negotiation owed";
}

TEST_F(ArtyPhy, LatchedLossRechecksWithoutAnotherRestart) {
    poll();
    peer.latched_down = true;
    const auto before = peer.published.size();
    next();
    ASSERT_EQ(peer.published.size(), before + 2u) << "MII both link edges";
    EXPECT_EQ(peer.published[before].word, 0u);
    EXPECT_EQ(peer.published.back().word, 11u);
    EXPECT_EQ(peer.restarts, 1u);
}

TEST_F(ArtyPhy, ResetAdvertisementIsRepairedAndRenegotiated) {
    poll();
    peer.regs[4] = 0x01e1u;
    peer.latched_down = true;
    next();
    EXPECT_EQ(peer.regs[4], 0x0101u) << "MII only 100 full advertised";
    EXPECT_EQ(peer.active_anar, 0x0101u);
    EXPECT_EQ(peer.restarts, 2u);
}

TEST_F(ArtyPhy, DroppedAdvertisementStaysOwedUntilReadback) {
    peer.ignored = 4u;
    poll();
    EXPECT_NE(phy.adv, 0u) << "MII advertisement remains owed";
    peer.ignored = 32u;
    next();
    EXPECT_EQ(phy.adv, 0u);
    EXPECT_EQ(peer.active_anar, 0x0101u);
    EXPECT_EQ(peer.restarts, 2u);
}

TEST_F(ArtyPhy, UnacknowledgedAdvertisementWritesNothing) {
    peer.nak = 4u;
    poll();
    EXPECT_TRUE(writes().empty()) << "MII no write before read acknowledgement";
    EXPECT_NE(phy.adv, 0u) << "MII advertisement remains owed";
    EXPECT_EQ(peer.word, 0u);
    peer.nak = 32u;
    next();
    EXPECT_EQ(peer.regs[4], 0x0101u) << "MII only 100 full advertised";
    EXPECT_EQ(peer.word, 11u);
}

TEST_F(ArtyPhy, NoFrameWithoutStepBudget) {
    clock_us = now;
    EXPECT_TRUE(ctrl_plat_phy_step(&phy, CTRL_PLAT_PHY_STEP_US - 1));
    EXPECT_TRUE(peer.frames.empty()) << "MII no frame without room";
    poll();
    EXPECT_EQ(peer.word, 11u);
}

}  // namespace
