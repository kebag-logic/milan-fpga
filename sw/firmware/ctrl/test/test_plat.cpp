// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_plat.cpp - the split platform's CSR window and console on the host bus
// (#665; plat/ctrl_plat_csr.c, plat/ctrl_plat_console.c, plat_bus.hpp):
//
//   C1  the identity: ID 'MILN' passes, anything else refuses; VERSION is read
//   C2  the policy: configure_fabric()'s fifteen writes, in its order, each
//       word from its policy field, the three read-modify-writes on the
//       window's own words, and neither compatibility enable left set
//   C3  the status words, read in milan_status_handler()'s order
//   C4  the time of day: snapshot first, HI LO HI, a torn read retried, and
//       a read that never agrees refused after CTRL_PLAT_TOD_TRIES
//   K1  milan_status answers the grader's two lines and the time, field for
//       field, with AEM loaded or disabled
//   K2  milan_gettime answers TAI_NS, or no number when the read is torn
//   K3  lines: CR, LF and CR LF end one; an empty line is no command; any
//       other line is refused, a NUL where a command's name ends among them;
//       a line past CTRL_PLAT_LINE_MAX is dropped whole
//   K4  the bound: at most CTRL_PLAT_RX_PER_PASS bytes in and
//       CTRL_PLAT_TX_PER_PASS out per pass, never into a full FIFO, one
//       command per pass, run only with room for the longest response
//   K5  the ring: text past its room is dropped and counted
//   K6  numbers: %08lx and %lu at their edges

#include <gtest/gtest.h>

#include <cstdint>
#include <string>

#include "fw_gtest.hpp"
#include "plat_bus.hpp"

FW_TALLY_LABEL("ctrl split platform CSR window and console (host bus)");

namespace {

using plat_bus::bus;
using plat_bus::kCsr;
using plat_bus::seed;

const ctrl_plat_policy kPolicy = {0x11111111u, 0x22222222u, 0x33333333u, 0x44444444u, 0x55555555u, 0x00006666u,
                                  0x00000008u, 0x00000001u, 0x00020001u, 0x00000002u, 0x00000010u, 0x00000201u,
                                  0x00000003u};

struct Plat : ::testing::Test {
    ctrl_plat_console console{};
    void SetUp() override {
        bus().reset();
        ctrl_plat_console_init(&console, &plat_bus::kUartRegs, kCsr);
    }
    // Poll until nothing is owed (at most `passes` times); the passes it took.
    unsigned drain(unsigned passes = 200) {
        unsigned n = 0;
        while (n < passes && ctrl_plat_console_poll(&console)) ++n;
        return n;
    }
    std::string answer(const std::string& line) {
        bus().tx.clear();
        bus().type(line);
        drain();
        return bus().tx;
    }
};

TEST_F(Plat, C1IdentityIsMilnAndReadsVersion) {
    std::uint32_t version = 0;
    EXPECT_TRUE(ctrl_plat_csr_identity(kCsr, &version)) << "C1 ID 'MILN' is a Milan datapath";
    EXPECT_EQ(version, plat_bus::kVersion) << "C1 VERSION is read with ID";
    bus().csr[CTRL_PLAT_CSR_ID] = 0x4d494c4fu;
    EXPECT_FALSE(ctrl_plat_csr_identity(kCsr, &version)) << "C1 any other ID is refused";
    EXPECT_TRUE(bus().writes().empty()) << "C1 the identity check writes nothing";
}

TEST_F(Plat, C2PolicyIsConfigureFabricsFifteenWritesInOrder) {
    ctrl_plat_csr_policy(kCsr, &kPolicy);
    const std::vector<std::pair<std::uint32_t, std::uint32_t>> want = {
        {0x600u, seed(0x600u) & ~1u}, {0x920u, seed(0x920u) & ~1u}, {0x604u, 0x11111111u}, {0x608u, 0x22222222u},
        {0x60cu, 0x33333333u}, {0x610u, 0x44444444u}, {0x108u, 0x55555555u}, {0x10cu, 0x00006666u},
        {0x100u, seed(0x100u) | 0x8u}, {0x700u, 0x1u}, {0x654u, 0x00020001u}, {0x684u, 0x2u}, {0x680u, 0x13u},
        {0x6ccu, 0x00000201u}, {0x750u, 0x3u}};
    EXPECT_EQ(bus().writes(), want) << "C2 configure_fabric's writes, in its order, from the policy";
    EXPECT_EQ(bus().word(CTRL_PLAT_CSR_ADP_CTRL) & 1u, 0u) << "C2 no fabric advertiser beside the core";
    EXPECT_EQ(bus().word(CTRL_PLAT_CSR_PP_CTRL) & 1u, 0u) << "C2 no processor beside the core";
}

TEST_F(Plat, C3StatusIsReadInMilanStatusOrder) {
    ctrl_plat_status s{};
    ctrl_plat_csr_status(kCsr, &s);
    const std::vector<std::uint32_t> order = {0x624u, 0x628u, 0x730u, 0x734u, 0x6e4u, 0x7e4u, 0x77cu,
                                              0x7f0u, 0x000u, 0x004u, 0x500u, 0x600u, 0x920u, 0x924u};
    std::vector<std::uint32_t> got;
    for (const auto& a : bus().log) got.push_back(static_cast<std::uint32_t>(a.address - kCsr));
    EXPECT_EQ(got, order) << "C3 each pair low then high, the gPTP half first";
    EXPECT_EQ(s.gm_hi, seed(0x628u)) << "C3 each word lands in its field";
    EXPECT_EQ(s.pp_stat, seed(0x924u)) << "C3 each word lands in its field";
}

TEST_F(Plat, C4TimeOfDayIsSnapshotThenAgreeingHighWords) {
    bus().csr[CTRL_PLAT_CSR_TOD_RD_LO] = 0x89abcdefu;
    bus().csr[CTRL_PLAT_CSR_TOD_RD_HI] = 0x01234567u;
    std::uint64_t ns = 0;
    ASSERT_TRUE(ctrl_plat_csr_tod(kCsr, &ns)) << "C4 a still snapshot reads at once";
    EXPECT_EQ(ns, 0x0123456789abcdefull) << "C4 HI:LO";
    ASSERT_GE(bus().log.size(), 4u) << "C4 the snapshot strobe comes first";
    EXPECT_TRUE(bus().log[0].write && bus().log[0].address == kCsr + CTRL_PLAT_CSR_PTP_CMD &&
                bus().log[0].value == CTRL_PLAT_PTP_SNAPSHOT) << "C4 the snapshot strobe comes first";
    bus().log.clear();
    bus().tod_hi = {1u, 2u, 2u, 2u};
    ASSERT_TRUE(ctrl_plat_csr_tod(kCsr, &ns)) << "C4 a torn read is retried";
    EXPECT_EQ(ns >> 32, 2u) << "C4 the agreeing high word";
    bus().tod_hi = {1u, 2u, 3u, 4u, 5u, 6u};
    ns = 7;
    EXPECT_FALSE(ctrl_plat_csr_tod(kCsr, &ns)) << "C4 a read that never agrees is refused";
    EXPECT_EQ(ns, 7u) << "C4 a refused read writes no time";
}

TEST_F(Plat, K1MilanStatusAnswersTheGradersLines) {
    bus().csr[CTRL_PLAT_CSR_GM_LO] = 0xfe001122u;
    bus().csr[CTRL_PLAT_CSR_GM_HI] = 0x001bc5ffu;
    bus().csr[CTRL_PLAT_CSR_PARENT_LO] = 0xfe334455u;
    bus().csr[CTRL_PLAT_CSR_PARENT_HI] = 0x001bc5ffu;
    bus().csr[CTRL_PLAT_CSR_PDELAY] = 600u;
    bus().csr[CTRL_PLAT_CSR_AS_PATH_CMD] = 0x73u;
    bus().csr[CTRL_PLAT_CSR_CLKV_STAT] = 0x00010002u;
    bus().csr[CTRL_PLAT_CSR_GPTP_LAT] = 0x029000dbu;
    bus().csr[CTRL_PLAT_CSR_PTP_CTRL] = 1u;
    bus().csr[CTRL_PLAT_CSR_ADP_CTRL] = 0u;
    bus().csr[CTRL_PLAT_CSR_PP_CTRL] = 0u;
    bus().csr[CTRL_PLAT_CSR_PP_STAT] = 0x5b000010u;
    bus().csr[CTRL_PLAT_CSR_TOD_RD_HI] = 1u;
    bus().csr[CTRL_PLAT_CSR_TOD_RD_LO] = 0x1000u;
    console.aem_loaded = true;
    EXPECT_EQ(answer("milan_status\r"),
              "ID=4d494c4e VERSION=00020060 PTP_CTRL=00000001 ADP_CTRL=00000000 PP_CTRL=00000000 "
              "PP_STAT=5b000010 AEM=loaded\r\n"
              "GPTP_GM=001bc5fffe001122 GPTP_PARENT=001bc5fffe334455 PDELAY_NS=600 AS_PATH_COUNT=3 "
              "AS_PATH_GEN=7 CLKV_STAT=00010002 SYNC=1 ASCAPABLE=1 TU=0 GPTP_LAT=029000db\r\n"
              "TAI_NS=0x0000000100001000\r\n")
        << "K1 milan_status's lines, field for field";
    console.aem_loaded = false;
    EXPECT_NE(answer("milan_status\n").find(" AEM=disabled\r\n"), std::string::npos)
        << "K1 an unverified image reads AEM=disabled";
    EXPECT_EQ(console.commands, 2u) << "K1 each line ran once";
}

TEST_F(Plat, K2MilanGettimeAnswersTaiNs) {
    bus().csr[CTRL_PLAT_CSR_TOD_RD_HI] = 0xdeadbeefu;
    bus().csr[CTRL_PLAT_CSR_TOD_RD_LO] = 0x00c0ffeeu;
    EXPECT_EQ(answer("milan_gettime\r\n"), "TAI_NS=0xdeadbeef00c0ffee\r\n") << "K2 TAI_NS in sixteen digits";
    bus().tod_hi = {1u, 2u, 3u, 4u, 5u, 6u};
    EXPECT_EQ(answer("milan_gettime\r"), "TAI_NS=none\r\n") << "K2 a torn read prints no number";
}

TEST_F(Plat, K3LinesEndOnceAndOthersAreRefused) {
    EXPECT_EQ(answer("\r\n\r"), "") << "K3 an empty line is no command";
    EXPECT_EQ(answer("help\r"), "?\r\n") << "K3 any other line is refused in one line";
    EXPECT_EQ(answer("milan_statu\r"), "?\r\n") << "K3 a prefix is no command";
    EXPECT_EQ(answer("milan_status_\r"), "?\r\n") << "K3 a longer word is no command";
    // a NUL where a command's name ends: refused, read no further than the
    // command's terminator (this binary runs under AddressSanitizer)
    EXPECT_EQ(answer(std::string("milan_status\0XYZ\r", 17)), "?\r\n") << "K3 a line holding a NUL is no command";
    EXPECT_EQ(answer(std::string("milan_gettime\0\r", 15)), "?\r\n") << "K3 a line holding a NUL is no command";
    EXPECT_EQ(console.refused, 5u) << "K3 refusals are counted";
    std::string longest(CTRL_PLAT_LINE_MAX, 'x');
    EXPECT_EQ(answer(longest + "\r"), "?\r\n") << "K3 a line of CTRL_PLAT_LINE_MAX bytes is kept";
    EXPECT_EQ(answer(longest + "milan_gettime\rmilan_gettime\r").find("?"), std::string::npos)
        << "K3 an overflowed line is dropped whole";
    EXPECT_EQ(console.overflows, 1u) << "K3 overflows are counted";
    EXPECT_EQ(console.commands, 1u) << "K3 the next line runs";
}

TEST_F(Plat, K4EachPassIsBounded) {
    bus().type(std::string(2u * CTRL_PLAT_RX_PER_PASS, 'x'));
    EXPECT_TRUE(ctrl_plat_console_poll(&console)) << "K4 a full slice of input is owed another pass";
    EXPECT_EQ(bus().rx.size(), CTRL_PLAT_RX_PER_PASS) << "K4 at most RX_PER_PASS bytes in";
    bus().rx.clear();
    bus().type("\rmilan_status\rmilan_gettime\r");
    (void)ctrl_plat_console_poll(&console);
    bus().log.clear();
    bus().tx.clear();
    const std::size_t before = bus().log.size();
    bus().tx_room = 5u;
    EXPECT_TRUE(ctrl_plat_console_poll(&console)) << "K4 output is owed after the pass";
    EXPECT_LE(bus().count(before, plat_bus::kUartRegs.ev_pending, true), CTRL_PLAT_RX_PER_PASS)
        << "K4 at most RX_PER_PASS bytes in";
    EXPECT_EQ(console.commands, 1u) << "K4 one command per pass";
    EXPECT_EQ(bus().tx.size(), 5u) << "K4 never into a full FIFO";
    EXPECT_EQ(bus().overruns, 0u) << "K4 never into a full FIFO";
    bus().tx_room = ~0u;
    const std::size_t sent = bus().tx.size();
    (void)ctrl_plat_console_poll(&console);
    EXPECT_EQ(bus().tx.size() - sent, CTRL_PLAT_TX_PER_PASS) << "K4 at most TX_PER_PASS bytes out";
    // the ring without room for the longest response: a complete line waits, no input is taken
    bus().tx_room = ~0u;
    drain(400);
    console.head = static_cast<std::uint16_t>(console.tail + CTRL_PLAT_TX_BYTES - CTRL_PLAT_RESPONSE_MAX + 1u);
    bus().tx_room = 0u;
    bus().type("milan_gettime\rmilan_gettime\r");
    const unsigned run = console.commands;
    EXPECT_TRUE(ctrl_plat_console_poll(&console)) << "K4 a waiting command is owed";
    EXPECT_TRUE(console.waiting) << "K4 a command runs only with room for the longest response";
    EXPECT_EQ(console.commands, run) << "K4 a command runs only with room for the longest response";
    (void)ctrl_plat_console_poll(&console);
    EXPECT_EQ(bus().rx.size(), 14u) << "K4 no input is taken while a line waits";
    bus().tx_room = ~0u;
    drain(400);
    EXPECT_FALSE(ctrl_plat_console_poll(&console)) << "K4 nothing owed once drained";
    EXPECT_EQ(console.commands, run + 2u) << "K4 the waiting command runs once room returns";
}

TEST_F(Plat, K5TextPastTheRingIsDroppedAndCounted) {
    std::string text(CTRL_PLAT_TX_BYTES + 3u, 'y');
    ctrl_plat_console_puts(&console, text.c_str());
    EXPECT_EQ(console.dropped, 3u) << "K5 the ring holds TX_BYTES and drops the rest";
    drain(400);
    EXPECT_EQ(bus().tx.size(), CTRL_PLAT_TX_BYTES) << "K5 every byte it held is sent";
}

TEST_F(Plat, K6NumbersAtTheirEdges) {
    bus().csr[CTRL_PLAT_CSR_PDELAY] = 0u;
    EXPECT_NE(answer("milan_status\r").find(" PDELAY_NS=0 "), std::string::npos) << "K6 zero is one digit";
    bus().csr[CTRL_PLAT_CSR_PDELAY] = 4294967295u;
    EXPECT_NE(answer("milan_status\r").find(" PDELAY_NS=4294967295 "), std::string::npos) << "K6 the largest";
    bus().csr[CTRL_PLAT_CSR_PDELAY] = 1000000000u;
    EXPECT_NE(answer("milan_status\r").find(" PDELAY_NS=1000000000 "), std::string::npos) << "K6 inner zeros";
    bus().csr[CTRL_PLAT_CSR_PDELAY] = 7u;
    bus().csr[CTRL_PLAT_CSR_GPTP_LAT] = 0xa0b0c0d0u;
    const std::string s = answer("milan_status\r");
    EXPECT_NE(s.find(" PDELAY_NS=7 "), std::string::npos) << "K6 no leading zeros";
    EXPECT_NE(s.find(" GPTP_LAT=a0b0c0d0"), std::string::npos) << "K6 eight lower-case digits";
}

}  // namespace
