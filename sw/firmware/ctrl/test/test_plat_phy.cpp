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
//   P11 THE ADVERTISEMENT at boot (#840), as the release's PHY init: register
//       9, then 4, then 0, each property by its own name from start values
//       in opposite states, autonegotiation restarted once after both, read
//       back, and never again while the link stands
//   P12 a 10/100 PHY, without BMSR's extended capability or without
//       1000BASE-T full duplex ability, is never written, at boot or after a
//       loss
//   P13 after every link loss the advertisement is written and read back
//       again, with no restart where the PHY still held it, so a restart's
//       own latched loss restarts nothing
//   P14 a PHY that lost the advertisement behind a loss, both registers
//       reset to their defaults, register 4 alone or register 9 alone, is
//       written and restarted once
//   P15 an advertisement that does not read back stays owed, written again
//       and negotiation restarted each poll, until it reads back
//   P16 a read the advertisement needs unacknowledged writes nothing; the
//       next poll retries
//   P17 the abilities in force are the verified advertisement: with
//       register 4's writes dropped through a try, at boot and after a loss,
//       the repair restarts negotiation, so a 100BASE-TX-only partner has no
//       link once it reads back, and no restart follows

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
    // The poll armed afresh, as a boot arms it, on the peer as the test set it.
    void arm_again() { arm(kBus); }
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
    // The writes from frame `k` on.
    std::vector<phy_peer::Frame> writes_since(std::size_t k) const {
        std::vector<phy_peer::Frame> out;
        for (; k < peer.frames.size(); ++k) {
            if (peer.frames[k].write) out.push_back(peer.frames[k]);
        }
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
    // the loss owes THE ADVERTISEMENT (P13), whose eight frames come between the two BMSR reads
    ASSERT_GE(regs.size(), 10u);
    EXPECT_EQ(regs[0], CTRL_PLAT_PHY_BMSR) << "P3 the latched BMSR, then the current one";
    EXPECT_EQ(regs[9], CTRL_PLAT_PHY_BMSR) << "P3 the latched BMSR, then the current one";
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
    // MII: no extended status register, the PHY's own advertisement (the boot wrote the gigabit PHY's)
    peer.regs[1] = 0x0024u;
    peer.regs[4] = 0x01e1u;
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
    // the loss before it owes the advertisement: its ability read finds no 1000BASE-T full duplex and writes nothing
    EXPECT_EQ(regs_since(frames), (std::vector<unsigned>{1, 15, 1, 0, 15, 4, 5})) << "P4 the release's registers in order";
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
    // the fault's loss owes the advertisement, which restarts negotiation on a PHY that no longer holds it (P14):
    // the link resolved again, then the forced modes, autonegotiation off
    next();
    EXPECT_EQ(peer.word, kGigFull) << "P4 the fault's end resolves 1000BASE-T full duplex";
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
    peer.regs[4] = 0x01e1u;   // an MII PHY's own advertisement
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
    // each later register unacknowledged: BMCR, the extended status and the 1000BASE-T pair on a gigabit PHY,
    // the advertisement on an MII one
    peer.gigabit(7u);
    for (const unsigned reg : {0u, 15u, 9u, 10u}) {
        peer.nak = reg;
        next();
        EXPECT_EQ(peer.word, 0u) << "P5 an unacknowledged register " << reg << " is link down";
        peer.nak = 32u;
        next();
        EXPECT_EQ(peer.word, kGigFull) << "P5 the register answering again resolves";
    }
    peer.regs[1] = 0x0024u;
    peer.nak = 4u;
    next();
    EXPECT_EQ(peer.word, 0u) << "P5 an unacknowledged register 4 is link down";
    peer.nak = 32u;
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
    EXPECT_TRUE(peer.fault.empty()) << "P6 every frame a Clause-22 read or write, driven as 22.2.4.5 drives it: "
                                    << peer.fault;
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
    EXPECT_EQ(calls, 7u + 1u + 6u + 9u)
        << "P7 seven misses, the probe, then the first poll's six frames (BMSR twice: nothing published up yet) and "
           "the boot's advertisement's nine";
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

// THE ADVERTISEMENT's three writes from frame `from` on, each property graded by its own name against the registers
// the PHY held before them (`start`, registers 0, 4 and 9), as the release's host test grades its PHY init (#840)
void expect_gigabit_only(const std::vector<phy_peer::Frame>& frames, std::size_t from, const std::uint16_t start[3],
                         const char* arm) {
    int at0 = -1;
    int at4 = -1;
    int at9 = -1;
    std::uint16_t ctl = 0;
    std::uint16_t adv = 0x03e0u;
    std::uint16_t gig = 0;
    unsigned writes = 0;
    for (std::size_t k = from; k < frames.size(); ++k) {
        if (!frames[k].write) continue;
        ++writes;
        const int at = static_cast<int>(k);
        if (frames[k].reg == 0u) at0 = at, ctl = frames[k].value;
        if (frames[k].reg == 4u) at4 = at, adv = frames[k].value;
        if (frames[k].reg == 9u) at9 = at, gig = frames[k].value;
    }
    EXPECT_EQ(writes, 3u) << "P11 three writes, " << arm;
    EXPECT_TRUE(at4 >= 0 && (adv & 0x0060u) == 0u) << "P11 no 10BASE-T advertised, " << arm;
    EXPECT_TRUE(at4 >= 0 && (adv & 0x0180u) == 0u) << "P11 no 100BASE-TX advertised, " << arm;
    EXPECT_TRUE(at4 >= 0 && (adv & 0x0200u) == 0u) << "P11 no 100BASE-T4 advertised, " << arm;
    EXPECT_TRUE(at4 >= 0 && (adv & 0x4000u) == 0u) << "P11 reserved bit 14 cleared, " << arm;
    EXPECT_EQ(adv & 0x0c00u, start[1] & 0x0c00u) << "P11 the pause bits kept, " << arm;
    EXPECT_EQ(adv & 0x001fu, start[1] & 0x001fu) << "P11 the selector kept, " << arm;
    EXPECT_TRUE(at9 >= 0 && (gig & 0x0200u) != 0u) << "P11 1000BASE-T full duplex advertised, " << arm;
    EXPECT_TRUE(at9 >= 0 && (gig & 0x01ffu) == 0u) << "P11 no 1000BASE-T half duplex advertised, " << arm;
    EXPECT_EQ(gig & 0x1c00u, start[2] & 0x1c00u) << "P11 MASTER-SLAVE kept, " << arm;
    EXPECT_TRUE(at9 >= 0 && (gig & 0xe000u) == 0u) << "P11 the test mode cleared, " << arm;
    EXPECT_TRUE(at0 >= 0 && (ctl & 0x0200u) != 0u) << "P11 autonegotiation restarted, " << arm;
    EXPECT_TRUE(at0 >= 0 && (ctl & 0x1000u) != 0u) << "P11 autonegotiation enabled, " << arm;
    EXPECT_TRUE(at0 >= 0 && (ctl & 0x8000u) == 0u) << "P11 reset cleared, " << arm;
    EXPECT_TRUE(at0 >= 0 && (ctl & 0x0400u) == 0u) << "P11 isolate cleared, " << arm;
    EXPECT_EQ(ctl & 0x0800u, start[0] & 0x0800u) << "P11 power-down kept, " << arm;
    EXPECT_EQ(ctl & 0x4000u, start[0] & 0x4000u) << "P11 loopback kept, " << arm;
    EXPECT_TRUE(at0 > at4 && at0 > at9) << "P11 the restart after both, " << arm;
    EXPECT_TRUE(at9 >= 0 && at9 < at4) << "P11 register 9, then 4, as the release's init writes them, " << arm;
}

TEST_F(PlatPhy, P11TheBootAdvertisesGigabitOnly) {
    // two arms whose kept bits start in opposite states (the release's host test's): the selector 00001 then
    // 11110, pause 10 then 01, MASTER-SLAVE 101 then 010, power-down 1 then 0, loopback 0 then 1; every bit the
    // init clears set
    const std::uint16_t arms[2][3] = {{0x9c00u, 0x4be1u, 0xf5ffu}, {0xc400u, 0x47feu, 0xebffu}};
    for (unsigned a = 0; a < 2u; ++a) {
        const char* arm = a == 0u ? "first arm" : "second arm";
        peer.gigabit(7u);
        peer.regs[0] = arms[a][0];
        peer.regs[4] = arms[a][1];
        peer.regs[9] = arms[a][2];
        arm_again();
        const std::size_t from = peer.frames.size(), pubs = peer.published.size();
        const unsigned restarts = peer.restarts;
        (void)poll(now);
        expect_gigabit_only(peer.frames, from, arms[a], arm);
        EXPECT_EQ(peer.restarts, restarts + 1u) << "P11 autonegotiation restarted once, " << arm;
        // read back after the restart, then the link resolved and published
        const auto w = writes_since(from);
        ASSERT_EQ(w.size(), 3u);
        std::size_t k = from;
        while (k < peer.frames.size() && peer.frames[k].at != w[2].at) ++k;
        ASSERT_LT(k + 2u, peer.frames.size());
        EXPECT_EQ(peer.frames[k + 1u].reg, 4u) << "P11 register 4 read back after the writes, " << arm;
        EXPECT_FALSE(peer.frames[k + 1u].write) << "P11 register 4 read back after the writes, " << arm;
        EXPECT_EQ(peer.frames[k + 2u].reg, 9u) << "P11 register 9 read back after the writes, " << arm;
        ASSERT_GT(peer.published.size(), pubs);
        EXPECT_GT(peer.published.back().at, w[2].at) << "P11 the link is resolved after the advertisement, " << arm;
        EXPECT_EQ(peer.word, kGigFull) << "P11 the link negotiated on the advertisement, " << arm;
        // verified: the next polls write nothing while the link stands
        const std::size_t later = peer.frames.size();
        next();
        next();
        EXPECT_TRUE(writes_since(later).empty()) << "P11 the advertisement is written once while the link stands, "
                                                 << arm;
        EXPECT_TRUE(peer.fault.empty()) << peer.fault;
    }
    // a PHY that already holds the advertisement is restarted at boot all the same, as the release's init restarts
    // it (a link it formed before the init is never published)
    peer.gigabit(7u);
    peer.regs[4] = 0x0001u;
    peer.regs[9] = 0x0200u;
    arm_again();
    const unsigned restarts = peer.restarts;
    (void)poll(now);
    EXPECT_EQ(peer.restarts, restarts + 1u) << "P11 the boot restarts negotiation whatever the PHY holds";
}

TEST_F(PlatPhy, P12A10100PhyIsNeverWritten) {
    // MII: BMSR without the extended capability, register 15 as a gigabit PHY's would read
    peer.gigabit(7u);
    peer.regs[1] = 0x002cu;
    peer.regs[5] = 0x01e1u;
    arm_again();
    std::size_t from = peer.frames.size();
    (void)poll(now);
    EXPECT_EQ(peer.word, kFull100) << "P12 an MII PHY resolves its own advertisement";
    EXPECT_TRUE(writes_since(from).empty()) << "P12 a PHY without BMSR's extended capability is never written";
    auto read = regs_since(from);
    read.erase(read.begin(), read.begin() + 8);   // the probe's PHYID1 reads, addresses 0 to 7
    EXPECT_EQ(read, (std::vector<unsigned>{1, 1, 0, 4, 5})) << "P12 and its poll reads no ability";
    peer.link(false);
    next();
    peer.link(true);
    peer.latched_down = true;
    next();
    EXPECT_TRUE(writes_since(from).empty()) << "P12 a PHY without BMSR's extended capability is never written";
    // extended, without 1000BASE-T full duplex ability: half duplex alone
    peer.gigabit(7u);
    peer.regs[15] = 0x1000u;
    peer.regs[10] = 0x0000u;
    arm_again();
    from = peer.frames.size();
    (void)poll(now);
    EXPECT_TRUE(writes_since(from).empty()) << "P12 a PHY without 1000BASE-T full duplex ability is never written";
    peer.link(false);
    next();
    peer.link(true);
    next();
    EXPECT_TRUE(writes_since(from).empty()) << "P12 a PHY without 1000BASE-T full duplex ability is never written";
    EXPECT_EQ(peer.regs[4], 0x01e1u) << "P12 its advertisement is its own";
    EXPECT_EQ(peer.regs[9], 0x0300u) << "P12 its advertisement is its own";
    EXPECT_TRUE(peer.fault.empty()) << peer.fault;
}

TEST_F(PlatPhy, P13ALossWritesAndVerifiesItAgain) {
    // a PHY whose restart latches a loss of its own, as a real PHY's renegotiation does
    peer.restart_drops = true;
    arm_again();
    (void)poll(now);
    next();
    ASSERT_EQ(peer.word, kGigFull);
    EXPECT_EQ(peer.restarts, 1u) << "P13 the boot's restart is the only one: its own latched loss restarts nothing";
    for (unsigned loss = 0; loss < 3u; ++loss) {
        const std::size_t from = peer.frames.size();
        if (loss == 1u) {
            peer.link(false);   // a sustained loss, then its end
            next();
            peer.link(true);
        }
        peer.latched_down = true;
        next();
        EXPECT_EQ(peer.restarts, 1u) << "P13 a loss with the advertisement held restarts nothing, loss " << loss;
        const auto w = writes_since(from);
        ASSERT_EQ(w.size(), 2u) << "P13 after a link loss the advertisement is written again, loss " << loss;
        EXPECT_EQ(w[0].reg, 9u) << "P13 after a link loss the advertisement is written again, loss " << loss;
        EXPECT_EQ(w[0].value, 0x0200u) << "P13 after a link loss the advertisement is written again, loss " << loss;
        EXPECT_EQ(w[1].reg, 4u) << "P13 after a link loss the advertisement is written again, loss " << loss;
        EXPECT_EQ(w[1].value, 0x0001u) << "P13 after a link loss the advertisement is written again, loss " << loss;
        std::size_t k = from;
        while (k < peer.frames.size() && peer.frames[k].at != w[1].at) ++k;
        ASSERT_LT(k + 2u, peer.frames.size());
        EXPECT_TRUE(peer.frames[k + 1u].reg == 4u && peer.frames[k + 2u].reg == 9u && !peer.frames[k + 2u].write)
            << "P13 and read back, loss " << loss;
        EXPECT_EQ(peer.word, kGigFull) << "P13 the link's return is published in the same poll, loss " << loss;
        const std::size_t later = peer.frames.size();
        next();
        EXPECT_TRUE(writes_since(later).empty()) << "P13 verified, the next poll writes nothing, loss " << loss;
    }
    EXPECT_TRUE(peer.fault.empty()) << peer.fault;
}

TEST_F(PlatPhy, P14AResetPhyIsAdvertisedAgain) {
    found();
    EXPECT_EQ(peer.restarts, 1u) << "P14 the boot restarts negotiation once";
    // behind a loss, the PHY reset to its defaults (10/100 and 1000BASE-T half duplex advertised again), then one
    // that lost register 4 alone, then one that lost register 9 alone: each is written and restarted once
    struct Lost {
        const char* what;
        bool local;
        bool gig;
    };
    for (const Lost lost : {Lost{"both registers", true, true}, Lost{"register 4 alone", true, false},
                            Lost{"register 9 alone", false, true}}) {
        if (lost.local) peer.regs[4] = 0x01e1u;
        if (lost.gig) peer.regs[9] = 0x0300u;
        peer.latched_down = true;
        const std::size_t from = peer.frames.size();
        const unsigned restarts = peer.restarts;
        next();
        const auto w = writes_since(from);
        ASSERT_EQ(w.size(), 3u) << "P14 a PHY that lost the advertisement is written and restarted once, "
                                << lost.what;
        EXPECT_EQ(w[2].reg, 0u) << "P14 a PHY that lost the advertisement is written and restarted once, "
                                << lost.what;
        EXPECT_EQ(peer.restarts, restarts + 1u)
            << "P14 a PHY that lost the advertisement is written and restarted once, " << lost.what;
        EXPECT_EQ(peer.regs[4], 0x0001u) << "P14 the advertisement written again, " << lost.what;
        EXPECT_EQ(peer.regs[9], 0x0200u) << "P14 the advertisement written again, " << lost.what;
        EXPECT_EQ(peer.word, kGigFull) << "P14 the link's return is published in the same poll, " << lost.what;
        const std::size_t later = peer.frames.size();
        next();
        EXPECT_TRUE(writes_since(later).empty()) << "P14 verified, the next poll writes nothing, " << lost.what;
        EXPECT_EQ(peer.restarts, restarts + 1u) << "P14 verified, the next poll restarts nothing, " << lost.what;
    }
    EXPECT_TRUE(peer.fault.empty()) << peer.fault;
}

TEST_F(PlatPhy, P15AnUnverifiedAdvertisementStaysOwed) {
    // a PHY that drops its writes to register 4, then one that drops them to register 9: each try writes and
    // restarts again, the registers as read not holding the advertisement, until it reads back
    for (const unsigned reg : {4u, 9u}) {
        peer.gigabit(7u);
        peer.ignored = reg;
        arm_again();
        (void)poll(now);
        EXPECT_GE(peer.restarts, 1u) << "P15 the boot restarts negotiation, register " << reg;
        for (unsigned k = 0; k < 3u; ++k) {
            const std::size_t from = peer.frames.size();
            const unsigned restarts = peer.restarts;
            next();
            EXPECT_EQ(writes_since(from).size(), 3u)
                << "P15 an advertisement that does not read back is written again each poll, register " << reg
                << ", poll " << k;
            EXPECT_EQ(peer.restarts, restarts + 1u)
                << "P15 and negotiation restarts after every repaired write, register " << reg << ", poll " << k;
        }
        peer.ignored = 32u;
        std::size_t from = peer.frames.size();
        unsigned restarts = peer.restarts;
        next();
        EXPECT_EQ(writes_since(from).size(), 3u) << "P15 once the PHY takes it, it reads back, register " << reg;
        EXPECT_TRUE(peer.regs[4] == 0x0001u && peer.regs[9] == 0x0200u)
            << "P15 once the PHY takes it, it reads back, register " << reg;
        EXPECT_EQ(peer.restarts, restarts + 1u) << "P15 the repaired advertisement is negotiated, register " << reg;
        from = peer.frames.size();
        restarts = peer.restarts;
        next();
        EXPECT_TRUE(writes_since(from).empty()) << "P15 verified, the next poll writes nothing, register " << reg;
        EXPECT_EQ(peer.restarts, restarts) << "P15 verified, the next poll restarts nothing, register " << reg;
    }
    EXPECT_TRUE(peer.fault.empty()) << peer.fault;
}

TEST_F(PlatPhy, P16AnUnacknowledgedReadWritesNothing) {
    for (const unsigned reg : {15u, 4u, 9u, 0u}) {
        peer.nak = reg;
        const std::size_t from = peer.frames.size();
        now += CTRL_PLAT_PHY_POLL_US;
        (void)poll(now);
        EXPECT_TRUE(writes_since(from).empty()) << "P16 no write before its read: register " << reg << " unacknowledged";
    }
    peer.nak = 32u;
    const std::size_t from = peer.frames.size();
    next();
    EXPECT_EQ(writes_since(from).size(), 3u) << "P16 the next poll with every read answered writes it";
    EXPECT_EQ(peer.restarts, 1u) << "P16 the next poll with every read answered writes it";
    // a read-back unacknowledged, register 4's or 9's after the writes: the advertisement stays owed
    for (const unsigned reg : {4u, 9u}) {
        peer.gigabit(7u);
        arm_again();
        for (unsigned k = 0; k < 64u && !(!peer.frames.empty() && peer.frames.back().write &&
                                          peer.frames.back().reg == 0u); ++k) {
            (void)call(now);
        }
        if (reg == 9u) (void)call(now);   // register 4 read back, acknowledged
        peer.nak = reg;
        (void)call(now);
        peer.nak = 32u;
        (void)poll(now);
        const std::size_t again = peer.frames.size();
        next();
        EXPECT_EQ(writes_since(again).size(), 2u)
            << "P16 a read-back unacknowledged leaves the advertisement owed: register " << reg;
    }
}

// P17's oracle: after a repair, the registers, the verification and the abilities in force (phy_peer.hpp
// `negotiates`) are the gigabit-only advertisement, a partner of 100BASE-TX full duplex alone has no link, and no
// restart follows.
void expect_in_force(PlatPhy& f, const char* arm) {
    EXPECT_EQ(f.peer.regs[4], 0x0001u) << "P17 the repaired advertisement reads back, " << arm;
    EXPECT_EQ(f.phy.adv, 0u) << "P17 the repaired advertisement is verified, " << arm;
    EXPECT_EQ(f.peer.active_anar & 0x03e0u, 0u) << "P17 the active advertisement is 1000BASE-T only, " << arm;
    EXPECT_EQ(f.peer.active_gctrl & 0x0300u, 0x0200u) << "P17 the active advertisement is 1000BASE-T only, " << arm;
    EXPECT_EQ(f.peer.active_speed, 0u) << "P17 a 100BASE-TX-only partner has no link, " << arm;
    EXPECT_EQ(f.peer.word, 0u) << "P17 a 100BASE-TX-only partner has no link, " << arm;
    const unsigned restarts = f.peer.restarts;
    f.next();
    f.next();
    EXPECT_EQ(f.peer.restarts, restarts) << "P17 no restart once the advertisement in force is the verified one, "
                                         << arm;
}

TEST_F(PlatPhy, P17TheRepairedAdvertisementIsTheOneInForce) {
    // at boot: register 4's writes dropped through the first poll, a partner of 100BASE-TX full duplex alone
    peer.gigabit(7u);
    peer.negotiates = true;
    peer.regs[5] = 0x0101u;
    peer.regs[10] = 0x0000u;
    peer.link(false);
    peer.ignored = 4u;
    arm_again();
    (void)poll(now);
    EXPECT_EQ(peer.active_speed, 100u) << "P17 the first restart negotiated the dropped write's 10/100 advertisement";
    peer.ignored = 32u;
    for (unsigned k = 0; k < 10u; ++k) next();
    expect_in_force(*this, "at boot");
    // after a loss: a 1000BASE-T link, then the PHY reset to its defaults behind a partner of 100BASE-TX full
    // duplex alone, renegotiating on them, the repair's first register-4 write dropped
    peer.regs[5] = 0x01e1u;
    peer.regs[10] = 0x0c00u;
    peer.negotiate();
    next();
    next();
    EXPECT_EQ(peer.word, kGigFull) << "P17 a 1000BASE-T partner links at 1000 Mb/s";
    peer.regs[4] = 0x01e1u;
    peer.regs[9] = 0x0300u;
    peer.regs[5] = 0x0101u;
    peer.regs[10] = 0x0000u;
    peer.negotiate();
    peer.latched_down = true;
    peer.ignored = 4u;
    next();
    EXPECT_EQ(peer.active_speed, 100u) << "P17 the loss's first restart negotiated 10/100 again";
    peer.ignored = 32u;
    for (unsigned k = 0; k < 10u; ++k) next();
    expect_in_force(*this, "after a loss");
    EXPECT_TRUE(peer.fault.empty()) << peer.fault;
}

}  // namespace
