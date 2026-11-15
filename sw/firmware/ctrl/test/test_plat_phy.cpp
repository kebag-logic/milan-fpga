// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_plat_phy.cpp - the split platform's PHY poll (#919; plat/ctrl_plat_phy.c)
// on a pin-level Clause-22 peer behind the host bus (phy_peer.hpp), the
// release's phy_link_tick cases (sw/firmware/nvm_hosttest/phy_host.c) and the
// split's own: one frame a call, THE STEP's admission, the owed report.
//
//   P1  no PHY found: one address probed a call, each miss publishing link
//       down, at once again, until PHYID1 answers; never a scan in one call
//   P2  THE PACE: a poll starts CTRL_PLAT_PHY_POLL_US after the last one
//       started, the release's PHY_POLL_NS, and none before
//   P3  a loss latched while the link was published up is published first,
//       link down, and the second BMSR read publishes the current state in
//       the same poll; a sustained loss publishes link down until it ends
//   P4  the resolved mode: 1000BASE-T full and half, 100 and 10 full and
//       half, the forced modes, incomplete negotiation and a master-slave
//       fault, each the release's word
//   P5  an unacknowledged read, a NAKed register and an all-ones BMSR are
//       link down, never a mode
//   P6  every frame a Clause-22 read of the release's registers in its order,
//       its preamble and command driven and its turnaround and data released
//   P7  one frame a call, and only with CTRL_PLAT_PHY_STEP_US left before the
//       deadline; a call without that room takes none and owes it
//   P8  the owed report: true while a poll owes a frame, false once it has
//       published and none is due
//   P9  a bus with no MDIO pair arms nothing and touches nothing; the half
//       period's spin is ceil(cpu_hz / CTRL_PLAT_PHY_HALF_HZ) turns
//   P10 the clock wraps: a poll is due by the wrapped difference, and at once
//       when the clock went back

#include <gtest/gtest.h>

#include <cstdint>
#include <vector>

#include "fw_gtest.hpp"
#include "plat_bus.hpp"

#include "ctrl_plat_phy.h"
#include <generated/soc.h>

namespace {

using plat_bus::bus;

constexpr ctrl_plat_phy_bus kBus = {0xf0002004u, 0xf0002008u, 0xf000201cu};
constexpr std::int32_t kRoom = 2000;   // a call's room: THE SHARE's 2.0 ms
constexpr std::uint32_t kGigFull = 13u, kGigHalf = 5u, kFull100 = 11u, kHalf100 = 3u, kFull10 = 9u, kHalf10 = 1u;

// The arming clock, the poll's pace: each read `step` microseconds after the last (0: a clock that stands, as F1's
// model's does between its advances).
std::uint64_t clock_us = 0, clock_step = 0;
std::uint64_t clock_read(void*) { return clock_us += clock_step; }

struct PlatPhy : ::testing::Test {
    phy_peer::Peer peer;
    ctrl_plat_phy phy{};
    std::uint32_t now = 1000u;
    void arm(const ctrl_plat_phy_bus& b, std::uint64_t step = 0) {
        clock_step = step;
        ctrl_plat_phy_arm(&phy, &b, clock_read, nullptr);
        clock_step = 0;
    }
    // One call at `at` with `room` microseconds of the pass's share left.
    bool step(std::uint32_t at, std::int32_t room) {
        clock_us = at;
        return ctrl_plat_phy_step(&phy, room);
    }
    void SetUp() override {
        bus().reset();
        peer.w = kBus.mdio_w;
        peer.r = kBus.mdio_r;
        peer.status = kBus.link_status;
        peer.gigabit(7u);
        bus().phy = &peer;
        arm(kBus);
    }
    bool call(std::uint32_t at) { return step(at, kRoom); }
    // Calls at `at` until nothing is owed, at most `most`; the calls taken.
    unsigned poll(std::uint32_t at, unsigned most = 64) {
        unsigned n = 0;
        while (n < most && call(at)) ++n;
        return n + 1u;
    }
    // A poll one period on.
    void next() {
        now += CTRL_PLAT_PHY_POLL_US;
        (void)poll(now);
    }
    std::vector<std::uint32_t> words_since(std::size_t k) const {
        std::vector<std::uint32_t> out;
        for (; k < peer.published.size(); ++k) out.push_back(peer.published[k].word);
        return out;
    }
    std::vector<unsigned> regs_since(std::size_t k) const {
        std::vector<unsigned> out;
        for (; k < peer.frames.size(); ++k) out.push_back(peer.frames[k].reg);
        return out;
    }
    // The address's PHY found and the peer's link published (the first poll).
    void found() {
        (void)poll(now);
        ASSERT_EQ(peer.word, kGigFull) << "the first poll publishes the peer's link";
    }
};

TEST_F(PlatPhy, P1OneAddressIsProbedACall) {
    std::vector<unsigned> probed;
    std::vector<std::uint32_t> words;
    for (unsigned k = 0; k < 8u; ++k) {
        const std::size_t frames = peer.frames.size(), pubs = peer.published.size();
        EXPECT_TRUE(call(now)) << "P1 a miss owes the next address at once";
        ASSERT_EQ(peer.frames.size(), frames + 1u) << "P1 one address an opportunity, no scan in one call";
        probed.push_back(peer.frames.back().address);
        EXPECT_EQ(peer.frames.back().reg, CTRL_PLAT_PHY_PHYID1) << "P1 each probe reads PHYID1";
        for (std::size_t p = pubs; p < peer.published.size(); ++p) words.push_back(peer.published[p].word);
    }
    EXPECT_EQ(probed, (std::vector<unsigned>{0, 1, 2, 3, 4, 5, 6, 7})) << "P1 the addresses in order, one a call";
    EXPECT_EQ(words, std::vector<std::uint32_t>(7u, 0u)) << "P1 each miss publishes link down";
    (void)poll(now);
    EXPECT_EQ(peer.word, kGigFull) << "P1 the PHY found at its address publishes its link";
    EXPECT_TRUE(peer.fault.empty()) << peer.fault;
}

TEST_F(PlatPhy, P2PollsArePaced) {
    found();
    const std::size_t frames = peer.frames.size();
    EXPECT_FALSE(call(now + CTRL_PLAT_PHY_POLL_US - 1u)) << "P2 no poll before CTRL_PLAT_PHY_POLL_US";
    EXPECT_EQ(peer.frames.size(), frames) << "P2 no poll before CTRL_PLAT_PHY_POLL_US";
    EXPECT_TRUE(call(now + CTRL_PLAT_PHY_POLL_US)) << "P2 a poll starts CTRL_PLAT_PHY_POLL_US after the last";
    EXPECT_EQ(peer.frames.size(), frames + 1u) << "P2 a poll starts CTRL_PLAT_PHY_POLL_US after the last";
    EXPECT_EQ(CTRL_PLAT_PHY_POLL_US, 125000u) << "P2 the release's PHY_POLL_NS, NVM_HEARTBEAT_NS / 2";
}

TEST_F(PlatPhy, P3LatchedLossPublishesBothEdges) {
    found();
    // a loss that ended before this poll: BMSR reads link down once
    peer.latched_down = true;
    std::size_t pubs = peer.published.size(), frames = peer.frames.size();
    now += CTRL_PLAT_PHY_POLL_US;
    (void)poll(now);
    EXPECT_EQ(words_since(pubs), (std::vector<std::uint32_t>{0u, kGigFull}))
        << "P3 a loss that recovered between two polls publishes link down, then link up";
    const auto regs = regs_since(frames);
    ASSERT_GE(regs.size(), 2u);
    EXPECT_EQ(regs[0], CTRL_PLAT_PHY_BMSR) << "P3 the latched BMSR, then the current one";
    EXPECT_EQ(regs[1], CTRL_PLAT_PHY_BMSR) << "P3 the latched BMSR, then the current one";
    EXPECT_LT(peer.published[pubs].at, peer.frames[frames + 1u].at)
        << "P3 the loss is published before the current state is read: a frame between the two words";
    // a sustained loss, then its end
    peer.link(false);
    pubs = peer.published.size();
    next();
    EXPECT_EQ(words_since(pubs), (std::vector<std::uint32_t>{0u, 0u})) << "P3 a sustained loss publishes link down";
    pubs = peer.published.size();
    next();
    EXPECT_EQ(words_since(pubs), (std::vector<std::uint32_t>{0u})) << "P3 a sustained loss publishes link down";
    peer.link(true);
    peer.latched_down = true;
    pubs = peer.published.size();
    next();
    EXPECT_EQ(words_since(pubs), (std::vector<std::uint32_t>{kGigFull}))
        << "P3 the first poll after the loss ends publishes the link up";
    pubs = peer.published.size();
    next();
    EXPECT_EQ(words_since(pubs), (std::vector<std::uint32_t>{kGigFull})) << "P3 a steady link publishes no edge";
    EXPECT_TRUE(peer.fault.empty()) << peer.fault;
}

TEST_F(PlatPhy, P4ResolvedModesAreTheReleases) {
    found();
    peer.regs[9] = 0x0100u;   // 1000BASE-T half duplex advertised, and the partner's alone
    peer.regs[10] = 0x0400u;
    next();
    EXPECT_EQ(peer.word, kGigHalf) << "P4 1000BASE-T half duplex";
    // MII: no extended status register
    peer.regs[1] = 0x0024u;
    const std::uint16_t partner[4] = {0x0101u, 0x0081u, 0x0041u, 0x0021u};
    const std::uint32_t want[4] = {kFull100, kHalf100, kFull10, kHalf10};
    for (unsigned k = 0; k < 4u; ++k) {
        peer.regs[5] = partner[k];
        next();
        EXPECT_EQ(peer.word, want[k]) << "P4 the highest common mode of 4 and 5, case " << k;
    }
    peer.regs[5] = 0x0001u;
    next();
    EXPECT_EQ(peer.word, 0u) << "P4 no common mode is link down";
    // the extended status without 1000BASE-T falls to 4 and 5
    peer.regs[1] = 0x0124u;
    peer.regs[15] = 0x0000u;
    peer.regs[5] = 0x0101u;
    std::size_t frames = peer.frames.size();
    next();
    EXPECT_EQ(peer.word, kFull100) << "P4 an extended status without 1000BASE-T resolves from 4 and 5";
    EXPECT_EQ(regs_since(frames), (std::vector<unsigned>{1, 1, 0, 15, 4, 5})) << "P4 the release's registers in order";
    // 1000BASE-T offered but not common: 4 and 5 after 9 and 10
    peer.regs[15] = 0x3000u;
    peer.regs[10] = 0x0000u;
    frames = peer.frames.size();
    next();
    EXPECT_EQ(peer.word, kFull100) << "P4 1000BASE-T not common resolves from 4 and 5";
    EXPECT_EQ(regs_since(frames), (std::vector<unsigned>{1, 0, 15, 9, 10, 4, 5}))
        << "P4 the release's registers in order";
    peer.regs[10] = 0x8c00u;
    next();
    EXPECT_EQ(peer.word, 0u) << "P4 a master-slave configuration fault is link down";
    peer.regs[10] = 0x0c00u;
    peer.regs[9] = 0x0300u;
    // the forced modes, autonegotiation off
    const std::uint16_t forced[3] = {0x2100u, 0x0140u, 0x0000u};
    const std::uint32_t mode[3] = {kFull100, kGigFull, kHalf10};
    for (unsigned k = 0; k < 3u; ++k) {
        peer.regs[0] = forced[k];
        next();
        EXPECT_EQ(peer.word, mode[k]) << "P4 the forced mode BMCR names, case " << k;
    }
    peer.regs[0] = 0x1000u;
    peer.regs[1] = 0x0104u;   // link, negotiation incomplete
    next();
    EXPECT_EQ(peer.word, 0u) << "P4 incomplete negotiation stays link down";
    EXPECT_TRUE(peer.fault.empty()) << peer.fault;
}

TEST_F(PlatPhy, P5ErrorsAreLinkDown) {
    found();
    peer.regs[1] = 0x0024u;
    peer.regs[5] = 0x0101u;
    peer.nak = 5u;
    next();
    EXPECT_EQ(peer.word, 0u) << "P5 a NAKed register is link down: 0xffff would resolve 100 full";
    peer.nak = 32u;
    next();
    EXPECT_EQ(peer.word, kFull100) << "P5 the register answering again resolves";
    peer.acknowledge = false;
    next();
    EXPECT_EQ(peer.word, 0u) << "P5 an unacknowledged BMSR is link down";
    peer.acknowledge = true;
    peer.regs[1] = 0xffffu;
    next();
    EXPECT_EQ(peer.word, 0u) << "P5 an all-ones BMSR is link down";
    // a PHY that never answers is probed forever, one address a call, link down meanwhile
    arm(kBus);
    peer.acknowledge = false;
    for (unsigned k = 0; k < 40u; ++k) EXPECT_TRUE(call(now)) << "P5 an absent PHY is probed again at once";
    EXPECT_EQ(peer.word, 0u) << "P5 an absent PHY is link down";
    EXPECT_EQ(peer.frames.back().address, 39u % CTRL_PLAT_PHY_ADDRESSES) << "P5 the probe wraps at 32 addresses";
}

TEST_F(PlatPhy, P6FramesAreClause22Reads) {
    found();
    const std::size_t from = peer.frames.size();
    peer.latched_down = true;
    next();
    EXPECT_TRUE(peer.fault.empty()) << "P6 every frame a Clause-22 read, driven then released: " << peer.fault;
    for (std::size_t k = from; k < peer.frames.size(); ++k) {
        EXPECT_EQ(peer.frames[k].address, 7u) << "P6 every frame at the PHY's address once found";
    }
    std::uint32_t last = ~0u;
    for (const auto& a : bus().log) {
        if (a.write && a.address == kBus.mdio_w) last = a.value;
    }
    EXPECT_EQ(last, 0u) << "P6 the pins are released after a frame";
}

TEST_F(PlatPhy, P7OneFrameACallWithItsRoom) {
    unsigned calls = 0;
    while (calls < 64u) {
        const std::size_t frames = peer.frames.size();
        const bool owed = call(now);
        EXPECT_EQ(peer.frames.size(), frames + 1u) << "P7 one frame a call";
        ++calls;
        if (!owed) break;
    }
    EXPECT_EQ(calls, 7u + 1u + 6u)
        << "P7 seven misses, the probe, then the first poll's six frames (BMSR twice: nothing published up yet)";
    now += CTRL_PLAT_PHY_POLL_US;
    std::size_t frames = peer.frames.size();
    EXPECT_TRUE(step(now, CTRL_PLAT_PHY_STEP_US - 1)) << "P7 a frame without its room is owed";
    EXPECT_EQ(peer.frames.size(), frames) << "P7 a frame is taken only with CTRL_PLAT_PHY_STEP_US left";
    EXPECT_TRUE(step(now, CTRL_PLAT_PHY_STEP_US)) << "P7 a frame with exactly its room is taken";
    EXPECT_EQ(peer.frames.size(), frames + 1u) << "P7 a frame with exactly its room is taken";
    frames = peer.frames.size();
    EXPECT_TRUE(step(now, -1)) << "P7 a deadline already past takes no frame";
    EXPECT_EQ(peer.frames.size(), frames) << "P7 a deadline already past takes no frame";
}

TEST_F(PlatPhy, P8OwedWhileAFrameIsDue) {
    EXPECT_TRUE(call(now)) << "P8 a probe that missed owes the next";
    found();
    EXPECT_FALSE(call(now)) << "P8 a published poll owes nothing until the next is due";
    EXPECT_FALSE(call(now + CTRL_PLAT_PHY_POLL_US - 1u)) << "P8 a published poll owes nothing until the next is due";
    EXPECT_TRUE(step(now + CTRL_PLAT_PHY_POLL_US, 0)) << "P8 a due poll is owed though it has no room";
    EXPECT_TRUE(call(now + CTRL_PLAT_PHY_POLL_US)) << "P8 a poll in progress owes its next frame";
}

TEST_F(PlatPhy, P9NoMdioArmsNothing) {
    ctrl_plat_phy_bus none = kBus;
    none.mdio_w = 0u;
    arm(none);
    const std::size_t accesses = bus().log.size();
    EXPECT_FALSE(call(now)) << "P9 a bus with no MDIO pair owes nothing";
    EXPECT_EQ(bus().log.size(), accesses) << "P9 and touches nothing";
    arm(kBus);
    EXPECT_EQ(phy.spin, (CONFIG_CLOCK_FREQUENCY + 4999999u) / 5000000u)
        << "P9 the half period at the SoC's clock: 200 ns, a turn a cycle";
    EXPECT_EQ(phy.spin, 20u) << "P9 the half period at 100 MHz: 200 ns, 20 turns";
    // a timed run: e us for CTRL_PLAT_PHY_CALIBRATION_TURNS turns, so a turn takes at least (e - 1) us / 1024
    arm(kBus, 277u);
    EXPECT_EQ(phy.spin, 1u) << "P9 a run of 277 us: one turn holds 200 ns";
    arm(kBus, 206u);
    EXPECT_EQ(phy.spin, 1u) << "P9 a run of 206 us: one turn holds 200 ns, 205 / 1024 us";
    arm(kBus, 205u);
    EXPECT_EQ(phy.spin, 20u) << "P9 a run of 205 us bounds a turn under 200 ns: the cycle bound's 20";
    arm(kBus, 1u);
    EXPECT_EQ(phy.spin, 20u) << "P9 a run of 205 us bounds a turn under 200 ns: the cycle bound's 20";
}

TEST_F(PlatPhy, P10TheClockWraps) {
    now = 0xfffff000u;
    found();
    EXPECT_FALSE(call(now + 10u)) << "P10 a poll is not due again before the clock wraps";
    EXPECT_FALSE(call(now + CTRL_PLAT_PHY_POLL_US - 1u)) << "P10 the wrapped difference paces the poll";
    EXPECT_TRUE(call(now + CTRL_PLAT_PHY_POLL_US)) << "P10 the wrapped difference paces the poll";
    (void)poll(now + CTRL_PLAT_PHY_POLL_US);
    const std::size_t frames = peer.frames.size();
    EXPECT_TRUE(call(5u)) << "P10 a clock that went back makes a poll due at once";
    EXPECT_EQ(peer.frames.size(), frames + 1u) << "P10 a clock that went back makes a poll due at once";
}

}  // namespace
