// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_unit_driver.cpp - the mailbox driver and the ADP adapter on a window
// the test writes (unit_window.hpp, behind MockMbxHal), for what the host
// model never posts (#665 lane FT):
//
//   D6   the MAAP range the filter's range_overlap test reads;
//   D7   a record whose length or position cannot be believed, each way the
//        driver checks it, refused and the ring resynchronised to RX_HEAD;
//   D8   a transmit on no channel, and a TX_TAIL that cannot be believed;
//   D9   an event of a type the contract does not define, the coherent
//        grandmaster read with no domain wanted, and the interrupt words;
//   D10  the lane and field helpers at their bounds;
//   D11  each interface's own MAC in its own filter block, an interface past
//        the contract's refused, and FILTER_MISMATCH read as its field (lane FC);
//   D14  the publication block (lane F-INT): each value in its interface's
//        register and field, a sink's stream_id written behind a clear
//        SID_VALID, and an interface or a sink past the contract's refused;
//   B2   the adapter's slots past the fabric's timer bank;
//   B3   a record or an event naming an interface with no instance, counted;
//   B4   an adapter the loop has no room for.

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <cstdint>

#include "adp_mbx.h"
#include "ctrl_loop.h"
#include "fw_gtest.hpp"
#include "mbx.h"
#include "mbx_wire.h"
#include "unit_window.hpp"

namespace {

using ::testing::NiceMock;
using unit::ch_reg;
using unit::Window;

constexpr unsigned kAdp = MBX_CH_ADP;

//! w0 of an RX record: length, interface and kind.
std::uint32_t rx_w0(std::uint32_t len, std::uint32_t iface, std::uint32_t kind = MBX_RX_KIND) {
    return mbx_place(len, MBX_RXREC_W0_LEN_LSB, MBX_RXREC_W0_LEN_WIDTH) |
           mbx_place(iface, MBX_RXREC_W0_IF_LSB, MBX_RXREC_W0_IF_WIDTH) |
           mbx_place(kind, MBX_RXREC_W0_KIND_LSB, MBX_RXREC_W0_KIND_WIDTH);
}

//! w0 of an event record.
std::uint32_t ev_w0(std::uint32_t type, std::uint32_t iface) {
    return mbx_place(type, MBX_EVREC_W0_TYPE_LSB, MBX_EVREC_W0_TYPE_WIDTH) |
           mbx_place(iface, MBX_EVREC_W0_IF_LSB, MBX_EVREC_W0_IF_WIDTH);
}

TEST(DriverUnit, D6MaapRangeWritten) {
    NiceMock<MockMbxHal> hal;
    Window w(hal);
    mbx_filter_set_maap_range(0x91E0F000FE00ull, 0x0200u);
    EXPECT_EQ(w.at(MBX_REG_MAAP_BASE_LO), 0xF000FE00u) << "D6 MAAP_BASE_LO holds the base's low word";
    EXPECT_EQ(w.at(MBX_REG_MAAP_BASE_HI), 0x91E0u) << "D6 MAAP_BASE_HI its high 16 bits";
    EXPECT_EQ(w.at(MBX_REG_MAAP_COUNT), 0x0200u) << "D6 MAAP_COUNT the count";
}

//! One record the driver must refuse: its w0, and the RX_HEAD it is read under.
struct Malformed {
    const char* name;
    std::uint32_t w0;
    std::uint32_t head;
};

class DriverMalformed : public ::testing::TestWithParam<Malformed> {};

TEST_P(DriverMalformed, D7RefusedAndResynchronised) {
    NiceMock<MockMbxHal> hal;
    Window w(hal);
    ASSERT_TRUE(mbx_open());
    const Malformed& c = GetParam();
    w.rx(kAdp, 0) = c.w0;
    w.words[ch_reg(kAdp, MBX_CH_REG_RX_HEAD)] = c.head;
    static mbx_frame got;
    EXPECT_EQ(mbx_rx_take(kAdp, &got), MBX_STATUS_BAD) << "D7 " << c.name << ": the record is refused";
    std::uint32_t tail = 0;
    EXPECT_TRUE(w.wrote(ch_reg(kAdp, MBX_CH_REG_RX_TAIL), &tail) && tail == c.head)
        << "D7 " << c.name << ": and the ring is resynchronised to RX_HEAD";
}

INSTANTIATE_TEST_SUITE_P(
    Records, DriverMalformed,
    ::testing::Values(Malformed{"shorter_than_a_header", rx_w0(13, 0), 8},
                      Malformed{"longer_than_the_channel_takes", rx_w0(MBX_CH_ADP_MAX_FRAME_BYTES + 1u, 0), 40},
                      Malformed{"RX_HEAD_past_the_ring", rx_w0(82, 0), MBX_CH_ADP_RX_WORDS + 1u},
                      Malformed{"record_past_RX_HEAD", rx_w0(82, 0), 3}),
    [](const ::testing::TestParamInfo<Malformed>& info) { return info.param.name; });

TEST(DriverUnit, D8TransmitRefusals) {
    NiceMock<MockMbxHal> hal;
    Window w(hal);
    ASSERT_TRUE(mbx_open());
    static const std::uint8_t frame[82] = {};
    EXPECT_EQ(mbx_tx_send(MBX_N_CH, 0, frame, sizeof frame), MBX_STATUS_BAD) << "D8 a channel past the contract's is refused";
    w.words[ch_reg(kAdp, MBX_CH_REG_TX_TAIL)] = 0x8000u;
    EXPECT_EQ(mbx_tx_send(kAdp, 0, frame, sizeof frame), MBX_STATUS_FULL)
        << "D8 a TX_TAIL more than a ring behind TX_HEAD is no room, never a negative fill";
    std::uint32_t head = 0;
    EXPECT_FALSE(w.wrote(ch_reg(kAdp, MBX_CH_REG_TX_HEAD), &head)) << "D8 and nothing is committed";
}

TEST(DriverUnit, D9UnknownEventTypeGrandmasterAndInterrupt) {
    NiceMock<MockMbxHal> hal;
    Window w(hal);
    ASSERT_TRUE(mbx_open());
    w.evt(0) = ev_w0(0x7Fu, 0);
    w.evt(1) = 0xFFFFFFFFu;
    w.words[MBX_REG_EVT_HEAD] = MBX_EV_WORDS;
    mbx_event ev{};
    EXPECT_TRUE(mbx_event_take(&ev) && ev.type == 0x7Fu && ev.timer_tag == 0u && ev.gm_id == 0u && !ev.link_up &&
                ev.tick_count == 0u)
        << "D9 an event of a type the contract does not define is taken with no field decoded";
    w.words[MBX_IF_BASE + MBX_IF_REG_GM_LO] = 0x55667788u;
    w.words[MBX_IF_BASE + MBX_IF_REG_GM_HI] = 0x11223344u;
    EXPECT_EQ(mbx_gm_id(0, nullptr), 0x1122334455667788ull) << "D9 the grandmaster read with no domain wanted";
    w.words[MBX_REG_IRQ_STATUS] = 0x80000003u;
    EXPECT_EQ(mbx_irq_status(), 0x80000003u) << "D9 IRQ_STATUS read as the fabric holds it";
    mbx_irq_clear_err();
    EXPECT_EQ(w.at(MBX_REG_IRQ_STATUS), 1u << MBX_IRQ_STATUS_ERR_LSB) << "D9 the sticky error cleared by writing its bit";
}

TEST(DriverUnit, D10LanesAndFieldsAtTheirBounds) {
    const std::uint8_t bytes[6] = {1, 2, 3, 4, 5, 6};
    EXPECT_EQ(ring_lanes_pack(bytes, 6), 0x04030201u) << "D10 a word packs four lanes, however many bytes are offered";
    std::uint8_t out[6] = {0, 0, 0, 0, 0xEE, 0xEE};
    ring_lanes_unpack(0x04030201u, out, 6);
    EXPECT_TRUE(out[3] == 4u && out[4] == 0xEEu && out[5] == 0xEEu) << "D10 and unpacks four, touching no fifth byte";
    EXPECT_EQ(mbx_place(0xDEADBEEFu, 0, 32), 0xDEADBEEFu) << "D10 a 32-bit field places whole";
    EXPECT_EQ(mbx_field(0xDEADBEEFu, 0, 32), 0xDEADBEEFu) << "D10 and reads whole";
}

TEST(DriverUnit, D11OwnMacPerInterfaceAndTheMismatchCount) {
    NiceMock<MockMbxHal> hal;
    Window w(hal);
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        EXPECT_TRUE(mbx_filter_set_own_mac(i, 0xA1B2C3D4E5F0ull + i)) << "D11 interface " << i << " takes its own MAC";
        const std::uint32_t block = MBX_IFF_BASE + MBX_IFF_STRIDE * i;
        EXPECT_EQ(w.at(block + MBX_IFF_REG_OWN_MAC_LO), 0xC3D4E5F0u + i) << "D11 OWN_MAC_LO holds MAC[31:0]";
        EXPECT_EQ(w.at(block + MBX_IFF_REG_OWN_MAC_HI), 0xA1B2u) << "D11 OWN_MAC_HI holds MAC[47:32]";
    }
    const std::size_t writes = w.writes.size();
    EXPECT_FALSE(mbx_filter_set_own_mac(MBX_N_IF, 0x001B92000001ull)) << "D11 an interface past the contract's is refused";
    EXPECT_EQ(w.writes.size(), writes) << "D11 and nothing is written";
    w.words[MBX_REG_FILTER_MISMATCH] = 0xFFFF0123u;
    EXPECT_EQ(mbx_filter_mismatch(), 0x0123u) << "D11 FILTER_MISMATCH is read as its COUNT field";
}

TEST(DriverUnit, D13BoundTalkerEntries) {
    NiceMock<MockMbxHal> hal;
    Window w(hal);
    const std::uint64_t talker = 0x0022110099887766ull;
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        const unsigned e = MBX_N_BOUND - 1u - i;
        const std::uint32_t entry = MBX_BND_BASE + MBX_BND_STRIDE * i + MBX_BND_ENTRY_STRIDE * e;
        std::size_t first = w.writes.size();
        EXPECT_TRUE(mbx_filter_set_bound_talker(i, e, true, talker + i)) << "D13 interface " << i << " takes an entry";
        ASSERT_EQ(w.writes.size(), first + 4u) << "D13 four writes: BOUND_EN, BOUND_EID_LO, BOUND_EID_HI, BOUND_EN";
        EXPECT_TRUE(w.writes[first].first == entry + MBX_BND_REG_BOUND_EN && w.writes[first].second == 0u &&
                    w.writes[first + 3u].first == entry + MBX_BND_REG_BOUND_EN)
            << "D13 BOUND_EN is cleared before the identity is written, and set after it";
        EXPECT_EQ(w.at(entry + MBX_BND_REG_BOUND_EID_LO), 0x99887766u + i) << "D13 BOUND_EID_LO holds talker[31:0]";
        EXPECT_EQ(w.at(entry + MBX_BND_REG_BOUND_EID_HI), 0x00221100u) << "D13 BOUND_EID_HI holds talker[63:32]";
        EXPECT_EQ(w.at(entry + MBX_BND_REG_BOUND_EN), 1u) << "D13 BOUND_EN set";
        first = w.writes.size();
        EXPECT_TRUE(mbx_filter_set_bound_talker(i, e, false, talker + i));
        EXPECT_TRUE(w.writes.size() == first + 1u && w.at(entry + MBX_BND_REG_BOUND_EN) == 0u)
            << "D13 a withdrawn entry: BOUND_EN cleared, one write";
    }
    const std::size_t writes = w.writes.size();
    EXPECT_FALSE(mbx_filter_set_bound_talker(MBX_N_IF, 0, true, talker)) << "D13 an interface past the contract's is refused";
    EXPECT_FALSE(mbx_filter_set_bound_talker(0, MBX_N_BOUND, true, talker)) << "D13 an entry past the table's is refused";
    EXPECT_EQ(w.writes.size(), writes) << "D13 and nothing is written";
}

TEST(DriverUnit, D14PublicationBlock) {
    NiceMock<MockMbxHal> hal;
    Window w(hal);
    const std::uint32_t valid = mbx_place(1u, MBX_BINDING_SID_VALID_LSB, MBX_BINDING_SID_VALID_WIDTH);
    const std::uint32_t bound = mbx_place(1u, MBX_BINDING_BOUND_LSB, MBX_BINDING_BOUND_WIDTH);
    const std::uint32_t started = mbx_place(1u, MBX_BINDING_STARTED_LSB, MBX_BINDING_STARTED_WIDTH);
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        const std::uint32_t block = MBX_PUB_BASE + MBX_PUB_STRIDE * i;
        std::size_t first = w.writes.size();
        EXPECT_TRUE(mbx_pub_da_gate(i, 0x00A5u + i) && mbx_pub_licence(i, 0x5A00u + i) &&
                    mbx_pub_idle_slope(i, 0x01312D00u + i) && mbx_pub_domain(i, true, 5u, 0x123u + i) &&
                    mbx_pub_talker_decl(i, 0x0C30u + i))
            << "D14 interface " << i << " takes every publication";
        EXPECT_EQ(w.writes.size(), first + 5u) << "D14 one write each";
        EXPECT_EQ(w.at(block + MBX_PUB_REG_DA_GATE), 0x00A5u + i) << "D14 DA_GATE.OPEN holds the gate";
        EXPECT_EQ(w.at(block + MBX_PUB_REG_LICENCE), 0x5A00u + i) << "D14 LICENCE.ACTIVE holds the licences";
        EXPECT_EQ(w.at(block + MBX_PUB_REG_TALKER_DECL), 0x0C30u + i)
            << "D14 TALKER_DECL.DECLARED holds the declarations";
        EXPECT_EQ(w.at(block + MBX_PUB_REG_IDLE_SLOPE), 0x01312D00u + i) << "D14 IDLE_SLOPE.BPS holds the slope";
        EXPECT_EQ(w.at(block + MBX_PUB_REG_SR_DOMAIN),
                  mbx_place(0x123u + i, MBX_SR_DOMAIN_VID_LSB, MBX_SR_DOMAIN_VID_WIDTH) |
                      mbx_place(5u, MBX_SR_DOMAIN_PRIORITY_LSB, MBX_SR_DOMAIN_PRIORITY_WIDTH) |
                      mbx_place(1u, MBX_SR_DOMAIN_ADOPTED_LSB, MBX_SR_DOMAIN_ADOPTED_WIDTH))
            << "D14 SR_DOMAIN holds VID, PRIORITY and ADOPTED in their fields";
        EXPECT_TRUE(mbx_pub_domain(i, false, 3u, 2u) &&
                    w.at(block + MBX_PUB_REG_SR_DOMAIN) ==
                        (mbx_place(2u, MBX_SR_DOMAIN_VID_LSB, MBX_SR_DOMAIN_VID_WIDTH) |
                         mbx_place(3u, MBX_SR_DOMAIN_PRIORITY_LSB, MBX_SR_DOMAIN_PRIORITY_WIDTH)))
            << "D14 the default Domain, not adopted";
        const unsigned k = MBX_N_PUB_SINKS - 1u - i;
        const std::uint32_t entry = block + MBX_PUB_SINK_BASE + MBX_PUB_SINK_STRIDE * k;
        first = w.writes.size();
        EXPECT_TRUE(mbx_pub_sink(i, k, true, true, 0x0011223344556677ull + i))
            << "D14 sink " << k << " takes its stream";
        ASSERT_EQ(w.writes.size(), first + 4u) << "D14 four writes: BINDING, SID_LO, SID_HI, BINDING";
        EXPECT_TRUE(w.writes[first].first == entry + MBX_PUB_SINK_REG_BINDING &&
                    w.writes[first].second == (bound | started) &&
                    w.writes[first + 3u].first == entry + MBX_PUB_SINK_REG_BINDING &&
                    w.writes[first + 3u].second == (bound | started | valid))
            << "D14 SID_VALID is clear while the stream_id is written, and set after it";
        EXPECT_EQ(w.at(entry + MBX_PUB_SINK_REG_SID_LO), 0x44556677u + i) << "D14 SID_LO holds stream_id[31:0]";
        EXPECT_EQ(w.at(entry + MBX_PUB_SINK_REG_SID_HI), 0x00112233u) << "D14 SID_HI holds stream_id[63:32]";
        first = w.writes.size();
        EXPECT_TRUE(mbx_pub_sink_binding(i, k, true, false, true));
        EXPECT_TRUE(w.writes.size() == first + 1u && w.at(entry + MBX_PUB_SINK_REG_BINDING) == (bound | valid))
            << "D14 a stop with the stream unchanged: BINDING alone, STARTED clear, SID_VALID kept, one write";
        first = w.writes.size();
        EXPECT_TRUE(mbx_pub_sink_binding(i, k, true, true, false));
        EXPECT_TRUE(w.writes.size() == first + 1u && w.at(entry + MBX_PUB_SINK_REG_BINDING) == (bound | started))
            << "D14 a start with no stream: BINDING alone, STARTED set, SID_VALID clear, one write";
        first = w.writes.size();
        EXPECT_TRUE(mbx_pub_sink(i, k, true, false, 0u));
        EXPECT_TRUE(w.writes.size() == first + 1u && w.at(entry + MBX_PUB_SINK_REG_BINDING) == bound)
            << "D14 a bound, stopped sink with no stream: BINDING with SID_VALID clear, one write";
        first = w.writes.size();
        EXPECT_TRUE(mbx_pub_sink(i, k, false, false, 0u));
        EXPECT_TRUE(w.writes.size() == first + 1u && w.at(entry + MBX_PUB_SINK_REG_BINDING) == 0u)
            << "D14 an unbound sink: BINDING 0, one write";
    }
    const std::size_t writes = w.writes.size();
    EXPECT_FALSE(mbx_pub_da_gate(MBX_N_IF, 1u) || mbx_pub_licence(MBX_N_IF, 1u) || mbx_pub_idle_slope(MBX_N_IF, 1u) ||
                 mbx_pub_domain(MBX_N_IF, true, 1u, 1u) || mbx_pub_talker_decl(MBX_N_IF, 1u) ||
                 mbx_pub_sink(MBX_N_IF, 0, true, true, 1u) || mbx_pub_sink_binding(MBX_N_IF, 0, true, true, true))
        << "D14 an interface past the contract's is refused";
    EXPECT_FALSE(mbx_pub_sink(0, MBX_N_PUB_SINKS, true, true, 1u) ||
                 mbx_pub_sink_binding(0, MBX_N_PUB_SINKS, true, true, true))
        << "D14 a sink past the block's is refused";
    EXPECT_EQ(w.writes.size(), writes) << "D14 and nothing is written";
}

const adp_entity kEntity = {0x1122334455667788ull, 0x99AABBCCDDEEFF01ull, 0x001B921122AAull, 0xC588u, 8u, 0x4801u,
                            8u, 0x4801u, 5u};
const std::uint64_t kOwnMac[MBX_N_IF] = {kEntity.mac};

TEST(AdpAdapterUnit, B2SlotsPastTheTimerBankRefused) {
    static adp_mbx m;
    EXPECT_FALSE(adp_mbx_init(&m, &kEntity, MBX_N_TIMERS, 0)) << "B2 slots past the fabric's timer bank are refused";
    EXPECT_TRUE(adp_mbx_init(&m, &kEntity, MBX_N_TIMERS - MBX_N_IF, 0)) << "B2 the last slots that fit are taken";
}

TEST(AdpAdapterUnit, B3ForeignInterfaceCounted) {
    static adp_mbx m;
    static ctrl_loop loop;
    NiceMock<MockMbxHal> hal;
    Window w(hal);
    ctrl_loop_init(&loop);
    ASSERT_TRUE(adp_mbx_init(&m, &kEntity, 0, 0) && adp_mbx_attach(&m, &loop) && ctrl_loop_open(&loop, 1, kOwnMac));
    w.rx(kAdp, 0) = rx_w0(26, MBX_N_IF);
    w.words[ch_reg(kAdp, MBX_CH_REG_RX_HEAD)] = 2u + 7u;
    w.evt(0) = ev_w0(MBX_EV_TYPE_LINK, MBX_N_IF);
    w.evt(1) = 1u;
    w.evt(4) = ev_w0(MBX_EV_TYPE_GM, MBX_N_IF);
    w.words[MBX_REG_EVT_HEAD] = 2u * MBX_EV_WORDS;
    static_cast<void>(ctrl_loop_service(&loop));
    EXPECT_EQ(loop.stats.rx_records, 1u) << "B3 (the record is taken)";
    EXPECT_EQ(m.foreign_if, 3u) << "B3 a record, a LINK and a GM naming an interface with no instance are counted";
    EXPECT_TRUE(m.ifs[0].adp.state == ADP_STATE_DOWN && m.ifs[0].adp.gm_changed == 0u && m.ifs[0].adp.discarded == 0u)
        << "B3 and no instance acts on them";
}

TEST(AdpAdapterUnit, B4LoopWithNoRoomRefused) {
    static adp_mbx m;
    static ctrl_loop loop;
    ASSERT_TRUE(adp_mbx_init(&m, &kEntity, 0, 0));
    ctrl_loop_init(&loop);
    for (unsigned k = 0; k < CTRL_LOOP_MAX_SINKS; ++k) {
        ASSERT_TRUE(ctrl_loop_add_sink(&loop, [](void*, const mbx_event*) {}, nullptr));
    }
    EXPECT_FALSE(adp_mbx_attach(&m, &loop)) << "B4 a loop with no room for the event sink is refused";
    ctrl_loop_init(&loop);
    for (unsigned k = 0; k < CTRL_LOOP_MAX_POLLS; ++k) {
        ASSERT_TRUE(ctrl_loop_add_poll(&loop, [](void*) { return false; }, nullptr));
    }
    EXPECT_FALSE(adp_mbx_attach(&m, &loop)) << "B4 a loop with no room for the poll is refused";
}

}  // namespace
