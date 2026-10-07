// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_acmp_mbx.cpp - the ACMP module on the mailbox (#665 lane F3; GoogleTest):
//
//   B   the adapter on the host model: the acmp channel and its filter, the
//       own-unicast receive tolerance, the timers on one fabric slot per
//       interface with the tag rule for raced expiries, the ADP channel's tap
//       (ENTITY_DISCOVER still ADP's), the gPTP pair, the adapter's refusals,
//       the bound-talker table each binding writes, another AVTP version
//       passing the filter and changing nothing;
//   C   every response path's service cost, counted access by access on the
//       model in the pass that takes the input (acmp_mbx.h ACMP_MBX_LAT_*):
//       the H-ACMP and H-DISC hooks of FR_NFR.md 3.4.2 on the host model;
//   E   a response owed behind a full transmit ring under a HAL that sleeps,
//       its change reported only after its TX_HEAD commit (#653), and the
//       pass in which it is committed with k frames owed ahead of it;
//   F   the bound with full legal backlogs: both rings full, every pass and
//       path held to the stated figures, events first in every pass; with
//       lane F2's MAAP composed too, every pass held to CTRL_APP_PASS_MAX;
//   U   the composition: ACMP after ADP, nothing read before the contract
//       check, the boot order's two halves; ADP, ACMP and lane F2's MAAP in
//       one app (the attach order, every channel and its interrupt opened,
//       disjoint timer slots, MAAP acquiring beside the other two) and the
//       three-way composition's refusals.
//
// The contract's adp channel passes the ENTITY_AVAILABLE and ENTITY_DEPARTING of
// a talker bound on the receiving interface (sw/mailbox/mailbox.yaml 2.1, the
// eq_bound term). Every H-DISC path here is measured from the record the
// model's filter commits (its RX_HEAD), so the frame takes the fabric's own
// path into the ring. The file is written for any interface count: the
// `acmpif2` arm builds it again on the contract's two-interface variant, where
// B3, B4, B6, B8 and the C paths run per interface (sink i on interface i).

#include <gtest/gtest.h>

#include <algorithm>
#include <array>
#include <climits>
#include <cstddef>
#include <cstdint>
#include <initializer_list>
#include <string>
#include <cstdio>
#include <cstring>
#include <vector>

#include "acmp.h"
#include "acmp_fake.hpp"
#include "acmp_mbx.h"
#include "ctrl_app.h"
#include "fw_gtest.hpp"
#include "mbx_model.h"
#include "mbx_wire.h"
#include "wire.h"

using namespace acmp_test;

namespace {

const adp_entity kEntity = {kOwn, 0x99AABBCCDDEEFF01ull, kMac0, 0xC588u, 2u, 0x4801u, 2u, 0x4801u, 0u};

struct mbx_model model;
struct ctrl_app app;
alignas(std::max_align_t) std::uint8_t arena[1024];
const ctrl_pool_class kClasses[] = {{32u, 8u}};
acmp_config acfg;

// Two sinks and two sources, each k on interface k % MBX_N_IF: at two
// interfaces, sink i and source i are interface i's.
acmp_config acmp_shape() {
    acmp_config c{};
    c.entity_id = kOwn;
    c.n_interfaces = MBX_N_IF;
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        c.mac[i] = kMac0;
    }
    c.n_sinks = 2;
    c.n_sources = 2;
    for (unsigned k = 0; k < 2u; ++k) {
        c.sink_interface[k] = static_cast<std::uint8_t>(k % MBX_N_IF);
        c.source_interface[k] = static_cast<std::uint8_t>(k % MBX_N_IF);
    }
    return c;
}

// Interface i's ACMP timer slot.
constexpr unsigned slot(unsigned i) {
    return CTRL_APP_ACMP_FIRST_SLOT + i;
}

ctrl_app_config app_config() {
    return ctrl_app_config{&kEntity, 0, arena, sizeof arena, kClasses, 1, nullptr, nullptr, &acfg, &kEnv,
                           nullptr, nullptr, 0};
}

// What MAAP published through the three-way composition's stream-address port.
struct Allocation {
    unsigned calls = 0;
    std::uint64_t base = 0;
    std::uint16_t count = 0;
    bool valid = false;
};
Allocation published;

void allocation(void* ctx, unsigned, std::uint64_t base, std::uint16_t count, bool valid) {
    Allocation& a = *static_cast<Allocation*>(ctx);
    ++a.calls;
    a.base = base;
    a.count = count;
    a.valid = valid;
}

// A range inside the B.4 pool (IEEE 1722-2016 Table B.9).
constexpr std::uint64_t kMaapBase = MAAP_POOL_BASE + 0x100u;

// True when a module's timer slot on the model is armed exactly when the
// module holds an arm there, with that arm's tag.
template <typename If>
bool holds(const If& i) {
    const mbx_model_timer& t = model.timers[i.slot];
    return t.armed == i.armed && (!i.armed || t.tag == i.tag);
}

// The app with ADP, ACMP and MAAP, MAAP claiming its range from kMaapBase.
ctrl_app_config three_way() {
    ctrl_app_config c = app_config();
    c.maap_allocation = allocation;
    c.maap_ctx = &published;
    c.maap_preferred = kMaapBase;
    return c;
}

struct acmp* core() {
    return &app.acmp.acmp;
}

// One service pass; returns its mailbox accesses.
std::uint64_t pass() {
    std::uint64_t before = model.reads + model.writes;
    static_cast<void>(ctrl_loop_service(&app.loop));
    return model.reads + model.writes - before;
}

// Passes until one handles nothing and owes nothing; bounded, since a frame
// owed behind a paused merge keeps every pass busy.
void settle() {
    for (unsigned k = 0; k < 256u && ctrl_loop_service(&app.loop) != 0u; ++k) {}
}

// The measured accesses of a path against its bound, printed as evidence and checked.
void bound(const std::string& path, std::uint64_t accesses, unsigned limit) {
    std::printf("  %-72s %4u accesses (bound %u)\n", path.c_str(), static_cast<unsigned>(accesses), limit);
    EXPECT_TRUE(accesses <= limit) << path;
}

// A path's label with the interface it ran on.
std::string on_if(unsigned i, const char* path) {
    return std::string(path) + ", interface " + std::to_string(i);
}

// A frame offered to the model's ingress on `iface`; true when the filter committed it.
bool offer(const Pdu& p, std::uint64_t dst = spec::MULTICAST_MAC, unsigned iface = 0) {
    auto f = acmpdu(p);
    wire_put_be(f.data(), dst, 6);
    return mbx_model_rx(&model, f.data(), f.size(), iface);
}

// An ADPDU offered to the model's ingress on `iface`; true when the filter
// committed it (RX_HEAD past its record): the fabric's path into the adp ring.
bool available(const Adp& d, unsigned iface = 0) {
    auto f = adpdu(d);
    return mbx_model_rx(&model, f.data(), f.size(), iface);
}

// A record in the adp receive ring as the fabric posts one (KL_mbx_rx, the
// model's rx_commit): the header words, the frame in little-endian lanes, then
// RX_HEAD past it.
void post_adp_record(const std::uint8_t* frame, std::size_t len) {
    mbx_model_channel* ch = &model.ch[MBX_CH_ADP];
    auto word = [](std::uint32_t index) -> std::uint32_t& {
        return model.window[(MBX_CH_ADP_RX_BASE + 4u * (index & (MBX_CH_ADP_RX_WORDS - 1u))) / 4u];
    };
    word(ch->rx_head) = mbx_place(static_cast<std::uint32_t>(len), MBX_RXREC_W0_LEN_LSB, MBX_RXREC_W0_LEN_WIDTH) |
                        mbx_place(0u, MBX_RXREC_W0_IF_LSB, MBX_RXREC_W0_IF_WIDTH) |
                        mbx_place(MBX_RX_KIND, MBX_RXREC_W0_KIND_LSB, MBX_RXREC_W0_KIND_WIDTH);
    word(static_cast<std::uint32_t>(ch->rx_head) + 1u) = model.now_ms;
    for (std::size_t k = 0; k < len; k += 4u) {
        word(static_cast<std::uint32_t>(ch->rx_head) + MBX_RX_HDR_WORDS + static_cast<std::uint32_t>(k / 4u)) =
            ring_lanes_pack(frame + k, len - k > 4u ? 4u : static_cast<unsigned>(len - k));
    }
    ch->rx_head = static_cast<std::uint16_t>(ch->rx_head + MBX_RX_HDR_WORDS + (len + 3u) / 4u);
}

// The k-th frame the model sent, read back.
Pdu wire(std::uint32_t k) {
    const mbx_model_tx* t = mbx_model_tx_frame(&model, k);
    return t != nullptr ? read(t->bytes) : Pdu{};
}

// The last TMR_CMD, or nullptr when none was written.
const struct mbx_model_tmr_op* last_tmr() {
    return model.tmr_ops == 0u ? nullptr : mbx_model_tmr_op(&model, model.tmr_ops - 1u);
}

class AcmpMailbox : public ::testing::Test {
 protected:
    void SetUp() override {
        fk = Fake{};
        for (unsigned i = 0; i < ACMP_MAX_SOURCES; ++i) {
            fk.source[i] = acmp_source_state{true, {kSid + i, kDa + i, 2u}, false};
        }
        acfg = acmp_shape();
        mbx_model_reset(&model);
        mbx_model_bind(&model, nullptr, nullptr);
        for (unsigned i = 0; i < MBX_N_IF; ++i) {
            mbx_model_set_gm(&model, i, kGm0, 0);
        }
        const ctrl_app_config cfg = app_config();
        ASSERT_TRUE(ctrl_app_start(&app, &cfg)) << "B0 the app with ACMP starts on the model";
        settle();
        fk.clear();
    }
    // A power cycle with the sinks' bindings (talker kTkA) saved, in the boot
    // order ctrl_app.h gives: compose, the store's binding walk, then open.
    void boot_restored(std::initializer_list<unsigned> sinks) {
        mbx_model_reset(&model);
        mbx_model_bind(&model, nullptr, nullptr);
        for (unsigned i = 0; i < MBX_N_IF; ++i) {
            mbx_model_set_gm(&model, i, kGm0, 0);
        }
        const ctrl_app_config cfg = app_config();
        ASSERT_TRUE(ctrl_app_compose(&app, &cfg));
        std::uint8_t record[spec::BINDING_BYTES] = {0x03, 0, 0, 1};
        wire_put_be(record + 4, kTkA, 8);
        wire_put_be(record + 12, kCtl1, 8);
        for (unsigned k : sinks) {
            ASSERT_EQ(acmp_restore_binding(core(), k, record, sizeof record), ACMP_RESTORE_APPLIED);
        }
        ASSERT_TRUE(ctrl_app_open(&app, &cfg));
        settle();
        fk.clear();
    }
    static Pdu command(std::uint8_t msg, unsigned sink, std::uint64_t ctlr = kCtl1, std::uint16_t seq = 0x4100) {
        Pdu p;
        p.msg = msg;
        p.controller = ctlr;
        p.talker = kTkA;
        p.listener = kOwn;
        p.talker_uid = 1;
        p.listener_uid = static_cast<std::uint16_t>(sink);
        p.seq = seq;
        return p;
    }
    static Pdu talker_command(std::uint8_t msg, std::uint16_t source = 0) {
        Pdu p;
        p.msg = msg;
        p.controller = kCtl1;
        p.talker = kOwn;
        p.listener = kTkB;
        p.talker_uid = source;
        p.listener_uid = 3;
        p.seq = 0x5100;
        return p;
    }
    Pdu answer(unsigned k, std::uint8_t status = spec::STATUS_SUCCESS) const {
        const acmp_sink& s = core()->sinks[k];
        Pdu p;
        p.msg = spec::MSG_PROBE_TX_RESPONSE;
        p.status = status;
        p.controller = s.probe_controller;
        p.talker = s.probe_talker;
        p.listener = kOwn;
        p.talker_uid = s.probe_talker_uid;
        p.listener_uid = static_cast<std::uint16_t>(k);
        p.seq = s.probe_seq;
        p.stream_id = kSid;
        p.dest_mac = kDa;
        p.vlan = 2;
        return p;
    }
    // Run the model to interface i's ACMP slot's armed deadline.
    void to_deadline(unsigned i = 0) {
        const mbx_model_timer& t = model.timers[slot(i)];
        ASSERT_TRUE(t.armed) << "the ACMP slot of interface " << i << " is armed";
        mbx_model_advance_ms(&model, t.deadline_ms - model.now_ms);
    }
    // Bind sink k, the command arriving on the sink's interface.
    void bind(unsigned k) {
        ASSERT_TRUE(offer(command(spec::MSG_BIND_RX_COMMAND, k), spec::MULTICAST_MAC, acfg.sink_interface[k]))
            << "the filter passes the BIND_RX";
        settle();
    }
};

// ---- B: the adapter on the model ------------------------------------------------------

TEST_F(AcmpMailbox, B1TheChannelCarriesCommandsAndResponsesInOrder) {
    std::uint32_t sent = model.tx_sent;
    ASSERT_TRUE(offer(command(spec::MSG_BIND_RX_COMMAND, 0))) << "B1 the filter passes a BIND_RX for this listener";
    settle();
    ASSERT_EQ(model.tx_sent, sent + 2u) << "B1 two frames leave";
    const mbx_model_tx* r = mbx_model_tx_frame(&model, sent);
    const mbx_model_tx* p = mbx_model_tx_frame(&model, sent + 1u);
    EXPECT_TRUE(r->channel == MBX_CH_ACMP && r->interface == 0u && r->len == spec::FRAME_BYTES &&
                read(r->bytes).msg == spec::MSG_BIND_RX_RESPONSE && p->channel == MBX_CH_ACMP &&
                read(p->bytes).msg == spec::MSG_PROBE_TX_COMMAND)
        << "B1 the response, then the probe, on the acmp channel, 70 bytes each, in commit order";
    EXPECT_TRUE((wire_be64(r->bytes) >> 16) == spec::MULTICAST_MAC && (wire_be64(r->bytes + 6) >> 16) == kMac0)
        << "B1 to the ACMP multicast address from the interface's MAC";
    Pdu other = command(spec::MSG_BIND_RX_COMMAND, 1);
    other.listener = kTkB;
    EXPECT_FALSE(offer(other)) << "B1 a BIND_RX for another listener never reaches the core (the identity term)";
    EXPECT_TRUE(offer(talker_command(spec::MSG_GET_TX_STATE_COMMAND))) << "B1 a GET_TX_STATE for this talker passes";
    settle();
    EXPECT_EQ(wire(model.tx_sent - 1u).msg, spec::MSG_GET_TX_STATE_RESPONSE) << "B1 and is answered";
}

TEST_F(AcmpMailbox, B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused) {
    ASSERT_TRUE(offer(command(spec::MSG_GET_RX_STATE_COMMAND, 0), kMac0))
        << "B2 a command to this interface's own unicast MAC passes (the owner's receive tolerance)";
    settle();
    const mbx_model_tx* r = mbx_model_tx_frame(&model, model.tx_sent - 1u);
    EXPECT_TRUE(r != nullptr && read(r->bytes).msg == spec::MSG_GET_RX_STATE_RESPONSE &&
                (wire_be64(r->bytes) >> 16) == spec::MULTICAST_MAC)
        << "B2 and is answered, to the multicast address (8.2.1)";
    std::uint16_t mismatch = model.filter_mismatch;
    EXPECT_FALSE(offer(command(spec::MSG_GET_RX_STATE_COMMAND, 0), kMac0 ^ 1u)) << "B2 a foreign unicast is refused";
    EXPECT_EQ(model.filter_mismatch, mismatch + 1u) << "B2 and counted once in FILTER_MISMATCH";
}

TEST_F(AcmpMailbox, B3TheTimersRunOnTheInterfaceSlot) {
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        SetUp();
        mbx_model_advance_ms(&model, 1234);              // a deadline is absolute: NOW_MS must not be 0
        const unsigned k = i;                            // sink i is interface i's
        std::uint32_t t0 = model.now_ms;
        bind(k);
        const struct mbx_model_tmr_op* arm = last_tmr();
        ASSERT_NE(arm, nullptr) << "B3 the bind arms a fabric timer";
        EXPECT_TRUE(arm->op == MBX_TMR_OP_ARM && arm->slot == slot(i) && arm->deadline_ms == t0 + spec::TMR_NO_RESP_MS &&
                    app.acmp.ifs[i].armed)
            << "B3 TMR_NO_RESP is armed on interface " << i << "'s ACMP slot at NOW_MS + 200 (Table 5.26)";
        std::uint32_t sent = model.tx_sent;
        mbx_model_advance_ms(&model, spec::TMR_NO_RESP_MS - 1u);
        settle();
        EXPECT_EQ(model.tx_sent, sent) << "B3 nothing at 199 ms, interface " << i;
        mbx_model_advance_ms(&model, 1);
        settle();
        const mbx_model_tx* dup = mbx_model_tx_frame(&model, sent);
        EXPECT_TRUE(model.tx_sent == sent + 1u && dup != nullptr && dup->now_ms == t0 + spec::TMR_NO_RESP_MS &&
                    dup->interface == i && read(dup->bytes).msg == spec::MSG_PROBE_TX_COMMAND &&
                    core()->sinks[k].state == ACMP_PRB_W_RESP2)
            << "B3 the duplicate leaves at 200 ms exactly, on interface " << i << " (5.5.3.5.16)";
    }
}

TEST_F(AcmpMailbox, B4AnExpiryThatRacedAStopOrAReArmIsDiscarded) {
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        SetUp();
        const unsigned k = i;
        bind(k);
        ASSERT_TRUE(offer(answer(k), spec::MULTICAST_MAC, i));
        settle();
        ASSERT_EQ(core()->sinks[k].state, ACMP_SETTLED_NO_RSV);
        to_deadline(i);                                  // TMR_NO_TK's expiry is posted, not yet taken
        acmp_tk_registered(core(), k, false);            // the SRP side, from another handler: nothing left to time
        settle();
        EXPECT_TRUE(app.acmp.ifs[i].stale_expiries == 1u && core()->sinks[k].state == ACMP_SETTLED_RSV_OK &&
                    !app.acmp.ifs[i].armed)
            << "B4 the expiry of a stopped arm is counted, never acted on, interface " << i;
        SetUp();
        bind(k);
        ASSERT_TRUE(available(Adp{}, i));                // discovered: TMR_NO_ADP 20 s runs beside TMR_NO_TK 10 s
        settle();
        ASSERT_TRUE(offer(answer(k), spec::MULTICAST_MAC, i));
        settle();
        to_deadline(i);
        acmp_tk_registered(core(), k, false);            // the slot re-armed at TMR_NO_ADP with a new tag
        settle();
        EXPECT_TRUE(app.acmp.ifs[i].stale_expiries == 1u && core()->sinks[k].state == ACMP_SETTLED_RSV_OK &&
                    app.acmp.ifs[i].armed && model.timers[slot(i)].deadline_ms == core()->sinks[k].adp_deadline)
            << "B4 the expiry of a replaced arm carries its old tag and is discarded; the new arm stands, interface " << i;
        mbx_event other{};
        other.type = MBX_EV_TYPE_TIMER;
        other.timer_slot = CTRL_APP_ADP_FIRST_SLOT + i;
        for (unsigned j = 0; j < app.loop.n_sinks; ++j) {
            if (app.loop.sinks[j].ctx == &app.acmp) {
                app.loop.sinks[j].fn(app.loop.sinks[j].ctx, &other);
            }
        }
        EXPECT_TRUE(app.acmp.ifs[i].stale_expiries == 1u && app.acmp.ifs[i].armed)
            << "B4 another module's slot is not ACMP's, interface " << i;
    }
}

TEST_F(AcmpMailbox, B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp) {
    boot_restored({0});
    EXPECT_TRUE(model.bound_en[0][0] && model.bound_eid[0][0] == kTkA)
        << "B5 the open wrote the restored binding's talker into interface 0's bound-talker table";
    Adp other;
    other.entity = kTkB;
    std::uint16_t mismatch = model.filter_mismatch;
    EXPECT_FALSE(available(other)) << "B5 an ENTITY_AVAILABLE of a talker no sink is bound to is refused";
    EXPECT_EQ(model.filter_mismatch, mismatch) << "B5 by the identity term, uncounted";
    EXPECT_TRUE(available(Adp{})) << "B5 the bound talker's ENTITY_AVAILABLE passes the filter (the eq_bound term)";
    settle();
    EXPECT_TRUE(core()->sinks[0].discovered && core()->sinks[0].state == ACMP_PRB_W_DELAY)
        << "B5 and reaches discovery through the tap (5.5.3.5.9)";
    mbx_model_set_link(&model, 0, true);
    for (unsigned k = 0; k < 12000u && app.adp.ifs[0].adp.state != ADP_STATE_WAITING; ++k) {
        mbx_model_advance_ms(&model, 1);
        settle();
    }
    ASSERT_EQ(app.adp.ifs[0].adp.state, ADP_STATE_WAITING);
    std::uint8_t discover[spec::ADPDU_FRAME_BYTES] = {};
    wire_put_be(discover, 0x91E0F0010000ull, 6);
    wire_put_be(discover + 12, spec::ETHERTYPE, 2);
    discover[14] = spec::ADPDU_SUBTYPE;
    discover[15] = 2;
    ASSERT_TRUE(mbx_model_rx(&model, discover, sizeof discover, 0));
    settle();
    EXPECT_EQ(app.adp.ifs[0].adp.state, ADP_STATE_DELAY)
        << "B5 an ENTITY_DISCOVER still goes to ADP's own handler (5.6.3.5.4)";
    std::uint32_t discarded = app.adp.ifs[0].adp.discarded;
    discover[15] = 3;
    post_adp_record(discover, sizeof discover);
    settle();
    EXPECT_EQ(app.adp.ifs[0].adp.discarded, discarded + 1u) << "B5 and so does any other ADPDU, which ADP discards";
}

TEST_F(AcmpMailbox, B6TheGrandmasterIsTheInterfaces) {
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        boot_restored({i});
        for (unsigned j = 0; j < MBX_N_IF; ++j) {
            mbx_model_set_gm(&model, j, j == i ? kGm0 + 7u : kGm0 + 9u, j == i ? 3 : 5);
        }
        Adp d;
        d.gm = kGm0;
        ASSERT_TRUE(available(d, i));
        settle();
        EXPECT_FALSE(core()->sinks[i].discovered)
            << "B6 an AVAILABLE from another grandmaster than interface " << i << "'s GM_LO/GM_HI is ignored";
        d.gm = kGm0 + 7u;
        d.domain = 3;
        ASSERT_TRUE(available(d, i));
        settle();
        EXPECT_TRUE(core()->sinks[i].discovered)
            << "B6 one from interface " << i << "'s grandmaster and domain is taken";
    }
}

TEST(AcmpAdapterUnit, B7RefusalsOfTheAdapter) {
    acmp_mbx m{};
    acmp_config c = acmp_shape();
    EXPECT_TRUE(acmp_mbx_init(&m, &c, &kEnv, MBX_N_TIMERS - MBX_N_IF)) << "B7 the last slot range that fits is taken";
    EXPECT_TRUE(m.ifs[0].slot == MBX_N_TIMERS - MBX_N_IF && m.ifs[MBX_N_IF - 1u].slot == MBX_N_TIMERS - 1u)
        << "B7 its last interface on the bank's last slot";
    for (unsigned first : {MBX_N_TIMERS - MBX_N_IF + 1u, MBX_N_TIMERS, 0x100u, 0x100u + MBX_N_TIMERS - MBX_N_IF,
                           UINT_MAX - MBX_N_IF + 1u, UINT_MAX}) {
        EXPECT_FALSE(acmp_mbx_init(&m, &c, &kEnv, first))
            << "B7 a first slot of " << first << " is refused: past the bank, wrapping the sum, or truncating to a slot";
    }
    c.n_interfaces = MBX_N_IF + 1u;
    EXPECT_FALSE(acmp_mbx_init(&m, &c, &kEnv, 0)) << "B7 more interfaces than the mailbox has are refused";
    c = acmp_shape();
    c.n_sinks = ACMP_MAX_SINKS + 1u;
    EXPECT_FALSE(acmp_mbx_init(&m, &c, &kEnv, 0)) << "B7 a configuration the core refuses is refused";
    c = acmp_shape();
    ASSERT_TRUE(acmp_mbx_init(&m, &c, &kEnv, 0));
    ctrl_loop loop{};
    ctrl_loop_init(&loop);
    EXPECT_FALSE(acmp_mbx_attach(&m, &loop)) << "B7 attaching before ADP bound the adp channel is refused";
    ASSERT_TRUE(ctrl_loop_bind_rx(&loop, MBX_CH_ADP, [](void*, const mbx_frame*) {}, nullptr));
    for (unsigned k = 0; k < CTRL_LOOP_MAX_SINKS; ++k) {
        ASSERT_TRUE(ctrl_loop_add_sink(&loop, [](void*, const mbx_event*) {}, nullptr));
    }
    EXPECT_FALSE(acmp_mbx_attach(&m, &loop)) << "B7 a loop with no room for the event sink is refused";
    ctrl_loop_init(&loop);
    ASSERT_TRUE(ctrl_loop_bind_rx(&loop, MBX_CH_ADP, [](void*, const mbx_frame*) {}, nullptr));
    for (unsigned k = 0; k < CTRL_LOOP_MAX_POLLS; ++k) {
        ASSERT_TRUE(ctrl_loop_add_poll(&loop, [](void*) { return false; }, nullptr));
    }
    EXPECT_FALSE(acmp_mbx_attach(&m, &loop)) << "B7 a loop with no room for the poll is refused";
}

// The adp channel's bound-talker term (#665 comment 6029368753): each binding
// writes its sink's entry of its interface's table, and the filter passes
// exactly that talker's ENTITY_AVAILABLE on exactly that interface.
TEST_F(AcmpMailbox, B8TheBoundTalkerTableFollowsEachBinding) {
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        SetUp();
        const unsigned k = i;
        Adp b;
        b.entity = kTkB;
        EXPECT_FALSE(available(Adp{}, i)) << "B8 before any binding no ENTITY_AVAILABLE passes, interface " << i;
        bind(k);
        EXPECT_TRUE(model.bound_en[i][k] && model.bound_eid[i][k] == kTkA)
            << "B8 a BIND_RX writes its sink's entry of interface " << i << "'s table";
        EXPECT_TRUE(available(Adp{}, i)) << "B8 and the bound talker's ENTITY_AVAILABLE passes on that interface";
        settle();
        EXPECT_FALSE(available(Adp{}, i + 1u)) << "B8 but on no other interface index";
        Pdu rebind = command(spec::MSG_BIND_RX_COMMAND, k);
        rebind.talker = kTkB;
        ASSERT_TRUE(offer(rebind, spec::MULTICAST_MAC, i));
        settle();
        EXPECT_TRUE(model.bound_en[i][k] && model.bound_eid[i][k] == kTkB)
            << "B8 a BIND_RX of another talker rewrites the entry";
        EXPECT_FALSE(available(Adp{}, i)) << "B8 the old talker's ENTITY_AVAILABLE is refused";
        EXPECT_TRUE(available(b, i)) << "B8 the new talker's passes";
        settle();
        ASSERT_TRUE(offer(command(spec::MSG_UNBIND_RX_COMMAND, k), spec::MULTICAST_MAC, i));
        settle();
        EXPECT_FALSE(model.bound_en[i][k]) << "B8 an UNBIND_RX clears the entry's BOUND_EN";
        EXPECT_FALSE(available(b, i)) << "B8 and its talker's ENTITY_AVAILABLE is refused again";
    }
}

// The filter reads the message type and the identity, never the AVTP
// version: a frame of another version reaches the core, which discards it
// before it is read (IEEE 1722-2016 4.4.3.4).
template <std::size_t N>
std::array<std::uint8_t, N> versioned(std::array<std::uint8_t, N> f, unsigned v) {
    f[15] = static_cast<std::uint8_t>((f[15] & 0x8Fu) | (v << 4));
    return f;
}

TEST_F(AcmpMailbox, B9AnotherAvtpVersionPassesTheFilterAndChangesNothing) {
    for (unsigned v : {1u, 7u}) {
        SetUp();
        const std::uint32_t sent = model.tx_sent;
        auto bindf = versioned(acmpdu(command(spec::MSG_BIND_RX_COMMAND, 0)), v);
        ASSERT_TRUE(mbx_model_rx(&model, bindf.data(), bindf.size(), 0))
            << "B9 the filter reads no version: a BIND_RX of version " << v << " reaches the acmp ring";
        settle();
        EXPECT_TRUE(model.tx_sent == sent && core()->sinks[0].state == ACMP_UNBOUND && !model.bound_en[0][0] &&
                    core()->rx_malformed == 1u)
            << "B9 the core discards it: no response, no binding, no bound-talker entry, version " << v;
        bind(0);
        auto resp = versioned(acmpdu(answer(0)), v);
        ASSERT_TRUE(mbx_model_rx(&model, resp.data(), resp.size(), 0));
        settle();
        EXPECT_EQ(core()->sinks[0].state, ACMP_PRB_W_RESP) << "B9 a PROBE_TX_RESPONSE of version " << v << " is not taken";
        auto avail = versioned(adpdu(Adp{}), v);
        ASSERT_TRUE(mbx_model_rx(&model, avail.data(), avail.size(), 0))
            << "B9 the bound talker's ENTITY_AVAILABLE of version " << v << " passes the filter";
        settle();
        EXPECT_FALSE(core()->sinks[0].discovered) << "B9 and discovers nothing, version " << v;
        ASSERT_TRUE(available(Adp{}));
        settle();
        ASSERT_TRUE(core()->sinks[0].discovered) << "B9 the same AVAILABLE at version 0 discovers the talker";
        Adp gone;
        gone.msg = spec::ADPDU_ENTITY_DEPARTING;
        auto dep = versioned(adpdu(gone), v);
        ASSERT_TRUE(mbx_model_rx(&model, dep.data(), dep.size(), 0));
        settle();
        EXPECT_TRUE(core()->sinks[0].discovered) << "B9 an ENTITY_DEPARTING of version " << v << " departs nothing";
    }
}

// ---- C: the service cost of every path (H-ACMP, H-DISC) -----------------------------------

TEST_F(AcmpMailbox, C0ToC4CommandsAreAnsweredInThePassThatTakesThem) {
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        SetUp();
        const unsigned k = i;                            // sink i, source i: interface i's
        const unsigned other = (k + 1u) % 2u;
        auto on = [i](const Pdu& p) { return offer(p, spec::MULTICAST_MAC, i); };
        std::uint32_t sent = model.tx_sent;
        ASSERT_TRUE(on(command(spec::MSG_BIND_RX_COMMAND, k)));
        std::uint64_t n = pass();
        EXPECT_EQ(model.tx_sent, sent + 2u) << "C0 BIND_RX: the response and the probe in the pass that takes it";
        EXPECT_TRUE(model.bound_en[i][k]) << "C0 and its talker admitted in that pass";
        bound(on_if(i, "C0 BIND_RX -> response, PROBE_TX, TMR_NO_RESP, talker admitted"), n, ACMP_MBX_LAT_BIND);
        ASSERT_TRUE(on(command(spec::MSG_GET_RX_STATE_COMMAND, k)));
        n = pass();
        EXPECT_EQ(model.tx_sent, sent + 3u) << "C1 GET_RX_STATE answered in one pass";
        bound(on_if(i, "C1 GET_RX_STATE -> response"), n, ACMP_MBX_LAT_GET_RX);
        ASSERT_TRUE(on(answer(k)));
        n = pass();
        EXPECT_EQ(core()->sinks[k].state, ACMP_SETTLED_NO_RSV) << "C2 PROBE_TX_RESPONSE settles in one pass";
        bound(on_if(i, "C2 PROBE_TX_RESPONSE -> TMR_NO_TK armed"), n, ACMP_MBX_LAT_PROBE_RESP);
        ASSERT_TRUE(on(command(spec::MSG_UNBIND_RX_COMMAND, k)));
        n = pass();
        EXPECT_TRUE(model.tx_sent == sent + 4u && core()->sinks[k].state == ACMP_UNBOUND && !model.bound_en[i][k])
            << "C3 UNBIND_RX answered in one pass, its talker withdrawn";
        bound(on_if(i, "C3 UNBIND_RX -> response, timer stopped, talker withdrawn"), n, ACMP_MBX_LAT_UNBIND);
        for (std::uint8_t msg : {spec::MSG_PROBE_TX_COMMAND, spec::MSG_GET_TX_STATE_COMMAND,
                                 spec::MSG_DISCONNECT_TX_COMMAND, spec::MSG_GET_TX_CONNECTION_COMMAND}) {
            std::uint32_t before = model.tx_sent;
            ASSERT_TRUE(on(talker_command(msg, static_cast<std::uint16_t>(k))));
            n = pass();
            const mbx_model_tx* r = mbx_model_tx_frame(&model, model.tx_sent - 1u);
            EXPECT_TRUE(model.tx_sent == before + 1u && r != nullptr && r->interface == i &&
                        read(r->bytes).status == (msg == spec::MSG_GET_TX_CONNECTION_COMMAND
                                                      ? spec::STATUS_NOT_SUPPORTED : spec::STATUS_SUCCESS))
                << "C4 a talker command for interface " << i << "'s source is answered in one pass, on that interface";
            bound(on_if(i, "C4 talker command -> response"), n, ACMP_MBX_LAT_TALKER);
        }
        bind(other);
        ASSERT_TRUE(offer(answer(other, 5u), spec::MULTICAST_MAC, acfg.sink_interface[other]));
        n = pass();
        bound(on_if(i, "C2 PROBE_TX_RESPONSE (failed) -> TMR_RETRY armed"), n, ACMP_MBX_LAT_PROBE_RESP);
    }
}

TEST_F(AcmpMailbox, C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry) {
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        SetUp();
        const unsigned k = i;
        bind(k);
        to_deadline(i);
        std::uint32_t sent = model.tx_sent;
        std::uint64_t n = pass();
        EXPECT_TRUE(model.tx_sent == sent + 1u && core()->sinks[k].state == ACMP_PRB_W_RESP2)
            << "C5 TMR_NO_RESP: the duplicate in the pass that takes the expiry";
        bound(on_if(i, "C5 TMR_NO_RESP -> duplicate PROBE_TX, TMR_NO_RESP"), n, ACMP_MBX_LAT_TIMER_PROBE);
        to_deadline(i);
        n = pass();
        EXPECT_EQ(core()->sinks[k].state, ACMP_PRB_W_RETRY) << "C6 the second TMR_NO_RESP";
        bound(on_if(i, "C6 TMR_NO_RESP -> TMR_RETRY armed"), n, ACMP_MBX_LAT_TIMER_ARM);
        ASSERT_TRUE(available(Adp{}, i));
        settle();
        to_deadline(i);
        n = pass();
        EXPECT_EQ(core()->sinks[k].state, ACMP_PRB_W_DELAY) << "C7 TMR_RETRY, talker discovered";
        bound(on_if(i, "C7 TMR_RETRY -> TMR_DELAY armed"), n, ACMP_MBX_LAT_TIMER_ARM);
        to_deadline(i);
        n = pass();
        EXPECT_EQ(core()->sinks[k].state, ACMP_PRB_W_RESP) << "C8 TMR_DELAY";
        bound(on_if(i, "C8 TMR_DELAY -> PROBE_TX, TMR_NO_RESP"), n, ACMP_MBX_LAT_TIMER_PROBE);
        ASSERT_TRUE(offer(answer(k), spec::MULTICAST_MAC, i));
        settle();
        to_deadline(i);
        n = pass();
        EXPECT_EQ(core()->sinks[k].state, ACMP_PRB_W_DELAY) << "C9 TMR_NO_TK, talker discovered";
        bound(on_if(i, "C9 TMR_NO_TK -> TMR_DELAY armed"), n, ACMP_MBX_LAT_TIMER_ARM);
    }
}

TEST_F(AcmpMailbox, C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord) {
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        boot_restored({i});
        const unsigned k = i;
        ASSERT_TRUE(available(Adp{}, i)) << "C10 the filter commits the bound talker's ENTITY_AVAILABLE (RX_HEAD)";
        std::uint64_t n = pass();
        EXPECT_EQ(core()->sinks[k].state, ACMP_PRB_W_DELAY) << "C10 ENTITY_AVAILABLE: TMR_DELAY in the same pass";
        bound(on_if(i, "C10 ENTITY_AVAILABLE from its RX_HEAD -> TMR_DELAY armed (H-DISC)"), n, ACMP_MBX_LAT_AVAILABLE);
        Adp gone;
        gone.msg = spec::ADPDU_ENTITY_DEPARTING;
        ASSERT_TRUE(available(gone, i)) << "C11 and its ENTITY_DEPARTING";
        n = pass();
        EXPECT_TRUE(core()->sinks[k].state == ACMP_PRB_W_AVAIL && !app.acmp.ifs[i].armed)
            << "C11 ENTITY_DEPARTING: PRB_W_AVAIL, the slot stopped, in the same pass";
        bound(on_if(i, "C11 ENTITY_DEPARTING from its RX_HEAD -> timer stopped (H-DISC)"), n, ACMP_MBX_LAT_DEPARTING);
    }
}

TEST_F(AcmpMailbox, C12AgingIsServedInThePassThatTakesTheExpiry) {
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        SetUp();
        const unsigned k = i;
        bind(k);
        Adp v;
        v.valid_time = 1;
        ASSERT_TRUE(available(v, i));
        settle();
        ASSERT_TRUE(offer(answer(k), spec::MULTICAST_MAC, i));
        settle();
        ASSERT_EQ(model.timers[slot(i)].deadline_ms, core()->sinks[k].adp_deadline)
            << "C12 TMR_NO_ADP (2 s) is the slot's earliest deadline";
        to_deadline(i);
        std::uint64_t n = pass();
        EXPECT_TRUE(!core()->sinks[k].discovered && core()->sinks[k].state == ACMP_SETTLED_NO_RSV)
            << "C12 TMR_NO_ADP: TK_NOT_DISCOVERED in the pass that takes the expiry (5.6.4.5.4)";
        bound(on_if(i, "C12 TMR_NO_ADP -> TK_NOT_DISCOVERED, timer re-armed (H-DISC)"), n, ACMP_MBX_LAT_NO_ADP);
    }
}

// ---- E: owed frames through the mailbox, and #653 ----------------------------------------

struct waiter {
    unsigned waits;
    unsigned dead;
};
waiter waits;

void wait_for_irq(void* ctx) {
    auto* w = static_cast<waiter*>(ctx);
    w->waits++;
    for (unsigned ms = 0; ms < 30000u && !mbx_model_irq(&model); ++ms) {
        mbx_model_advance_ms(&model, 1);
    }
    w->dead += mbx_model_irq(&model) ? 0u : 1u;
}

// Every access numbered; the ACMP channel's TX_HEAD writes remembered. A
// notification recorded at count n came after the n-th access.
std::uint64_t accesses;
std::vector<std::uint64_t> acmp_commits;

void count_access(void*, bool write, std::uint32_t off, std::uint32_t) {
    accesses++;
    if (write && off == MBX_CH_BASE + MBX_CH_STRIDE * MBX_CH_ACMP + MBX_CH_REG_TX_HEAD) {
        acmp_commits.push_back(accesses);
    }
}

// The env's notifier, numbered on the same count.
std::vector<std::uint64_t> changes;

void fill_acmp_tx() {
    mbx_model_tx_pause(&model, true);
    Pdu p;
    p.msg = spec::MSG_GET_RX_STATE_RESPONSE;
    auto filler = acmpdu(p);
    while (mbx_tx_send(MBX_CH_ACMP, 0, filler.data(), filler.size()) == MBX_STATUS_OK) {}
}

TEST_F(AcmpMailbox, E1AnOwedResponseLeavesFirstAndItsChangeAfterIt) {
    waits = waiter{};
    mbx_model_bind(&model, wait_for_irq, &waits);
    accesses = 0;
    acmp_commits.clear();
    changes.clear();
    fill_acmp_tx();
    ASSERT_TRUE(offer(command(spec::MSG_BIND_RX_COMMAND, 0)));
    for (unsigned k = 0; k < 8u; ++k) {
        ctrl_loop_step(&app.loop);
    }
    EXPECT_TRUE(core()->owed_count == 2u && core()->sinks[0].state == ACMP_PRB_W_RESP && acmp_change_pending(core(), 0))
        << "E1 BIND_RX behind a full ring: bound, its response and probe owed, its change waiting";
    unsigned w = waits.waits;
    EXPECT_TRUE(fk.count(Call::CHANGED) == 0u && w == 0u)
        << "E1 nothing reported yet, and the loop does not sleep while frames are owed";
    mbx_host_trace(count_access, nullptr);
    fk.hook_kind = Call::CHANGED;
    fk.hook = [] { changes.push_back(accesses); };       // inside the notifier: when it was called
    mbx_model_tx_pause(&model, false);
    std::uint32_t drained = model.tx_sent;
    for (unsigned k = 0; k < 4u && changes.empty(); ++k) {
        static_cast<void>(ctrl_loop_service(&app.loop));
    }
    mbx_host_trace(nullptr, nullptr);
    ASSERT_EQ(changes.size(), 1u) << "E1 the change is reported once the room returns";
    ASSERT_FALSE(acmp_commits.empty());
    EXPECT_TRUE(changes.back() >= acmp_commits.front())
        << "E1 the change is reported after the response's TX_HEAD commit (#653)";
    EXPECT_EQ(wire(drained).msg, spec::MSG_BIND_RX_RESPONSE) << "E1 and the response is the first frame after the room";
    settle();
    EXPECT_TRUE(wire(drained + 1u).msg == spec::MSG_PROBE_TX_COMMAND && core()->owed_count == 0u)
        << "E1 then the probe; nothing owed";
    mbx_model_bind(&model, nullptr, nullptr);
}

TEST_F(AcmpMailbox, E2AnOwedResponseIsCommittedInPassKPlus1) {
    for (unsigned k : {0u, 3u, ACMP_OWED_MAX - 1u}) {
        SetUp();
        fill_acmp_tx();
        for (unsigned j = 0; j < k; ++j) {
            ASSERT_TRUE(offer(command(spec::MSG_GET_RX_STATE_COMMAND, 1, kCtl2, static_cast<std::uint16_t>(j))));
            mbx_model_advance_ms(&model, MBX_CH_ACMP_RATE_REFILL_MS);
            settle();
        }
        ASSERT_TRUE(offer(command(spec::MSG_GET_RX_STATE_COMMAND, 0, kCtl1, 0x7777)));
        settle();
        ASSERT_EQ(core()->owed_count, k + 1u);
        mbx_model_tx_pause(&model, false);
        std::uint32_t base = model.tx_sent;
        std::uint64_t spent = 0;
        unsigned at = 0;
        for (unsigned p = 1; p <= ACMP_OWED_MAX + 1u && at == 0u; ++p) {
            spent += pass();
            for (std::uint32_t j = base; j < model.tx_sent; ++j) {
                at = wire(j).seq == 0x7777u ? p : at;
            }
        }
        char what[160];
        std::snprintf(what, sizeof what, "E2 %u frames owed ahead: the response in pass k + 1 after the room returns", k);
        EXPECT_TRUE(at == k + 1u && at <= ACMP_MBX_OWED_PASSES) << what;
        std::snprintf(what, sizeof what, "E2 %u owed ahead: room to response", k);
        bound(what, at != 0u ? spent : UINT64_MAX, ACMP_MBX_OWED_ACCESSES);
    }
}

// ---- F: the bound with full backlogs (ctrl_loop.h A1 to A4) ------------------------------

TEST_F(AcmpMailbox, F0ToF3FullRingsAreTakenWithinTheBound) {
    for (unsigned k = 0; k < acfg.n_sinks; ++k) {
        bind(k);
    }
    mbx_tick_enable(false);
    for (unsigned t = 0; t < MBX_N_TIMERS; ++t) {
        if (t < slot(0) || t >= slot(MBX_N_IF)) {        // every slot but ACMP's
            mbx_timer_arm(t, 0x77u, mbx_now_ms());
        }
    }
    to_deadline();                                       // every sink's TMR_NO_RESP: the ACMP slots' expiries, last
    ASSERT_EQ(static_cast<std::uint16_t>(model.evt_head - model.evt_tail), MBX_EVT_WORDS)
        << "F0 the event ring is full";
    unsigned stored = 0;
    for (unsigned j = 0; j < 100000u && model.ch[MBX_CH_ACMP].rx_drop == 0u; ++j) {
        Pdu p = command(spec::MSG_BIND_RX_COMMAND, j % acfg.n_sinks, kCtl1, static_cast<std::uint16_t>(j));
        p.talker = kTkB + j;
        if (offer(p)) {
            stored++;
        } else if (model.ch[MBX_CH_ACMP].rx_drop == 0u) {
            mbx_model_advance_ms(&model, 1);
        }
    }
    EXPECT_TRUE(stored > 0u && stored <= ACMP_MBX_RX_BACKLOG) << "F0 the acmp ring holds no more records than A1 assumes";
    std::uint64_t worst = 0;
    unsigned rx_at = 0;
    unsigned evt_at = 0;
    std::uint32_t events0 = app.loop.stats.events;
    std::uint32_t rx0 = app.loop.stats.rx_records;
    for (unsigned p = 1; p <= 64u && (rx_at == 0u || evt_at == 0u); ++p) {
        std::uint64_t n = pass();
        worst = n > worst ? n : worst;
        evt_at = evt_at == 0u && app.loop.stats.events - events0 == CTRL_LOOP_EVT_BACKLOG ? p : evt_at;
        rx_at = rx_at == 0u && app.loop.stats.rx_records - rx0 == stored ? p : rx_at;
    }
    std::printf("  backlog: 16 event records, %u acmp records of 70 bytes; worst pass %u accesses\n", stored,
                static_cast<unsigned>(worst));
    EXPECT_TRUE(evt_at != 0u && evt_at <= CTRL_LOOP_EVT_PASSES) << "F1 every event is taken by pass 2";
    EXPECT_TRUE(rx_at != 0u && rx_at <= ACMP_MBX_RX_PASSES) << "F2 every acmp record is taken by ACMP_MBX_RX_PASSES";
    bound("F3 the worst pass of the backlog", worst, ACMP_MBX_PASS_MAX);
    settle();
}

TEST_F(AcmpMailbox, F4TheSmallestRecordsTheFilterPassesFillTheRing) {
    auto f = acmpdu(talker_command(spec::MSG_GET_TX_STATE_COMMAND));
    const std::size_t smallest = MBX_CH_ACMP_T0_OFFSET + MBX_TERM_FIELD_BYTES;
    EXPECT_FALSE(mbx_model_rx(&model, f.data(), smallest - 1u, 0))
        << "F4 a frame that ends inside talker_entity_id holds no identity term and is not passed";
    unsigned stored = 0;
    for (unsigned j = 0; j < 100000u && model.ch[MBX_CH_ACMP].rx_drop == 0u; ++j) {
        if (mbx_model_rx(&model, f.data(), smallest, 0)) {
            stored++;
        } else if (model.ch[MBX_CH_ACMP].rx_drop == 0u) {
            mbx_model_advance_ms(&model, 1);
        }
    }
    EXPECT_EQ(stored, ACMP_MBX_RX_BACKLOG) << "F4 the ring holds ACMP_MBX_RX_BACKLOG records of the smallest frame";
    std::uint32_t rx0 = app.loop.stats.rx_records;
    unsigned at = 0;
    for (unsigned p = 1; p <= 64u && at == 0u; ++p) {
        static_cast<void>(pass());
        at = app.loop.stats.rx_records - rx0 == stored ? p : 0u;
    }
    EXPECT_TRUE(at == ACMP_MBX_RX_PASSES && core()->rx_malformed == stored)
        << "F4 taken by pass ACMP_MBX_RX_PASSES, each a malformed ACMPDU the core counts";
}

TEST_F(AcmpMailbox, F5AnAvailableBehindAFullAdpRingIsServedWithinTheBound) {
    acfg.sink_interface[1] = 0;                          // two sinks of one talker on interface 0
    boot_restored({0, 1});
    // Through the filter, as the fabric fills it: the smallest ENTITY_DISCOVER
    // the filter passes (26 bytes, through entity_id), as adp_mbx.h's backlog
    // test sends, until only the ENTITY_AVAILABLE's record still fits; then
    // the bound talker's ENTITY_AVAILABLE, the ring's last record. The token
    // bucket refills while the core is stalled.
    Adp d;
    d.msg = spec::ADPDU_ENTITY_DISCOVER;
    d.entity = 0;
    auto discover = adpdu(d);
    const unsigned available_words = MBX_RX_HDR_WORDS + (spec::ADPDU_FRAME_BYTES + 3u) / 4u;
    const unsigned discover_words = MBX_RX_HDR_WORDS + (26u + 3u) / 4u;
    auto room = [] {
        const mbx_model_channel& ch = model.ch[MBX_CH_ADP];
        return MBX_CH_ADP_RX_WORDS - static_cast<std::uint16_t>(ch.rx_head - ch.rx_tail);
    };
    unsigned stored = 0;
    for (unsigned j = 0; j < 100000u && room() >= available_words + discover_words; ++j) {
        if (mbx_model_rx(&model, discover.data(), 26u, 0)) {
            stored++;
        } else {
            mbx_model_advance_ms(&model, 1);
        }
    }
    bool committed = false;
    for (unsigned j = 0; j < 1000u && !committed; ++j) {
        committed = available(Adp{});
        if (!committed) {
            mbx_model_advance_ms(&model, 1);
        }
    }
    ASSERT_TRUE(committed && model.ch[MBX_CH_ADP].rx_drop == 0u) << "F5 the ENTITY_AVAILABLE's record is committed";
    stored++;
    EXPECT_TRUE(room() < discover_words && stored <= CTRL_LOOP_RX_BACKLOG(MBX_CH_ADP_RX_WORDS))
        << "F5 the adp ring is full, the ENTITY_AVAILABLE its last record";
    std::uint64_t spent = 0;
    unsigned at = 0;
    for (unsigned p = 1; p <= 64u && at == 0u; ++p) {
        spent += pass();
        at = core()->sinks[0].state == ACMP_PRB_W_DELAY ? p : 0u;
        EXPECT_EQ(core()->sinks[1].state, core()->sinks[0].state)
            << "F5 every matching bound sink takes it in the same pass (5.6.4.1)";
    }
    std::printf("  adp backlog: %u records through the filter, the ENTITY_AVAILABLE served in pass %u\n", stored, at);
    EXPECT_TRUE(at != 0u && at <= CTRL_LOOP_RX_PASSES(MBX_CH_ADP_RX_WORDS))
        << "F5 the ENTITY_AVAILABLE is taken by pass CTRL_LOOP_RX_PASSES(256)";
    bound("F5 ENTITY_AVAILABLE behind a full adp ring, from its RX_HEAD (H-DISC)", at != 0u ? spent : UINT64_MAX,
          ACMP_MBX_ADP_RX_ACCESSES);
}

// A MAAP PROBE from another station for `count` addresses at kMaapBase: it
// overlaps the range MAAP claims, so the maap channel's filter passes it.
std::array<std::uint8_t, 60> maap_probe(std::uint16_t count) {
    std::array<std::uint8_t, 60> f{};
    wire_put_be(f.data(), MAAP_MULTICAST, 6);
    wire_put_be(f.data() + 6, 0x060000000040ull, 6);
    f[12] = 0x22;
    f[13] = 0xF0;
    f[14] = 0xFE;                                   // the MAAP subtype
    f[15] = MAAP_MSG_PROBE;
    f[17] = 16;                                     // control_data_length
    wire_put_be(f.data() + 26, kMaapBase, 6);
    wire_put_be(f.data() + 32, count, 2);
    return f;
}

TEST_F(AcmpMailbox, F6WithMaapComposedEveryPassStaysWithinTheThreeWayBound) {
    mbx_model_reset(&model);
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        mbx_model_set_gm(&model, i, kGm0, 0);
        mbx_model_set_link(&model, i, true);
    }
    const ctrl_app_config cfg = three_way();
    ASSERT_TRUE(ctrl_app_start(&app, &cfg));
    settle();
    for (unsigned k = 0; k < acfg.n_sinks; ++k) {
        bind(k);
    }
    mbx_tick_enable(false);
    for (unsigned t = 0; t < MBX_N_TIMERS; ++t) {
        if ((t < slot(0) || t >= slot(MBX_N_IF)) && (t < app.maap.ifs[0].slot || t > app.maap.ifs[MBX_N_IF - 1u].slot)) {
            mbx_timer_arm(t, 0x77u, mbx_now_ms());      // every slot but ACMP's and MAAP's
        }
    }
    to_deadline();                                   // every sink's TMR_NO_RESP, last
    unsigned acmp_stored = 0;
    for (unsigned j = 0; j < 100000u && model.ch[MBX_CH_ACMP].rx_drop == 0u; ++j) {
        Pdu q = command(spec::MSG_BIND_RX_COMMAND, j % acfg.n_sinks, kCtl1, static_cast<std::uint16_t>(j));
        q.talker = kTkB + j;
        acmp_stored += offer(q) ? 1u : 0u;
    }
    unsigned maap_stored = 0;
    for (unsigned j = 0; j < 1000u && model.ch[MBX_CH_MAAP].rx_drop == 0u; ++j) {
        const auto f = maap_probe(static_cast<std::uint16_t>(1u + j % 8u));
        maap_stored += mbx_model_rx(&model, f.data(), f.size(), 0) ? 1u : 0u;
    }
    const unsigned events = static_cast<std::uint16_t>(model.evt_head - model.evt_tail) / MBX_EV_WORDS;
    ASSERT_TRUE(events > 0u && acmp_stored > 0u && maap_stored > 0u) << "F6 events, acmp and maap records wait";
    std::uint64_t worst = 0;
    std::uint32_t rx0 = app.loop.stats.rx_records;
    std::uint32_t events0 = app.loop.stats.events;
    unsigned at = 0;
    for (unsigned q = 1; q <= 64u && at == 0u; ++q) {
        std::uint64_t n = pass();
        worst = n > worst ? n : worst;
        at = app.loop.stats.rx_records - rx0 >= acmp_stored + maap_stored && app.loop.stats.events - events0 >= events
                 ? q
                 : 0u;
    }
    std::printf("  three-way backlog: %u event records, %u acmp and %u maap records; worst pass %u accesses\n", events,
                acmp_stored, maap_stored, static_cast<unsigned>(worst));
    EXPECT_TRUE(at != 0u && at <= ACMP_MBX_RX_PASSES) << "F6 every record and event is taken, by ACMP_MBX_RX_PASSES";
    EXPECT_EQ(model.ch[MBX_CH_MAAP].rx_tail, model.ch[MBX_CH_MAAP].rx_head) << "F6 the maap ring is drained";
    bound("F6 the worst pass of the three-way backlog", worst, CTRL_APP_PASS_MAX);
    settle();
}

// ---- U: the composition ---------------------------------------------------------------------

TEST_F(AcmpMailbox, U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract) {
    mbx_model_reset(&model);
    std::uint64_t before = model.reads + model.writes;
    const ctrl_app_config cfg = app_config();
    ASSERT_TRUE(ctrl_app_compose(&app, &cfg)) << "U5 the app composes ADP and ACMP";
    EXPECT_EQ(model.reads + model.writes, before) << "U5 composing touches no mailbox register";
    EXPECT_TRUE(app.loop.rx[MBX_CH_ACMP].fn != nullptr && app.loop.rx[MBX_CH_ADP].ctx == &app.acmp &&
                app.acmp.adp_next.ctx == &app.adp)
        << "U5 ACMP binds its channel and stands in front of ADP's handler";
    std::uint8_t record[spec::BINDING_BYTES] = {0x03, 0, 0, 1};
    wire_put_be(record + 4, kTkA, 8);
    ASSERT_EQ(acmp_restore_binding(core(), 1, record, sizeof record), ACMP_RESTORE_APPLIED);
    EXPECT_EQ(model.reads + model.writes, before) << "U5 the store's binding walk between the two touches none either";
    ASSERT_TRUE(ctrl_app_open(&app, &cfg));
    EXPECT_TRUE(mbx_field(model.filter_en, 0u, 8u) == ((1u << MBX_CH_ADP) | (1u << MBX_CH_ACMP)) &&
                ((model.irq_enable >> MBX_CH_ACMP) & 1u) == 1u)
        << "U5 opening opens the acmp channel and its interrupt";
    EXPECT_TRUE(model.bound_en[acfg.sink_interface[1]][1] && model.bound_eid[acfg.sink_interface[1]][1] == kTkA &&
                !model.bound_en[0][0])
        << "U5 and writes the bound-talker entry of the binding restored between compose and open, only that one";
    acmp_config bad = acmp_shape();
    bad.n_sinks = ACMP_MAX_SINKS + 1u;
    acfg = bad;
    EXPECT_FALSE(ctrl_app_compose(&app, &cfg)) << "U5 an ACMP configuration the module refuses fails the composition";
}

TEST_F(AcmpMailbox, U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen) {
    mbx_model_reset(&model);
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        mbx_model_set_gm(&model, i, kGm0, 0);
        mbx_model_set_link(&model, i, true);
    }
    published = Allocation{};
    const std::uint64_t before = model.reads + model.writes;
    const ctrl_app_config cfg = three_way();
    ASSERT_TRUE(ctrl_app_compose(&app, &cfg)) << "U6 the app composes ADP, ACMP and MAAP";
    EXPECT_EQ(model.reads + model.writes, before) << "U6 composing the three touches no mailbox register";
    EXPECT_TRUE(app.loop.n_sinks == 3u && app.loop.sinks[0].ctx == &app.adp && app.loop.sinks[1].ctx == &app.acmp &&
                app.loop.sinks[2].ctx == &app.maap && app.loop.n_polls == 3u && app.loop.polls[0].ctx == &app.adp &&
                app.loop.polls[1].ctx == &app.acmp && app.loop.polls[2].ctx == &app.maap)
        << "U6 ADP, then ACMP, then MAAP attach, each with its sink and its poll";
    EXPECT_TRUE(app.loop.rx[MBX_CH_ADP].ctx == &app.acmp && app.acmp.adp_next.ctx == &app.adp &&
                app.loop.rx[MBX_CH_ACMP].ctx == &app.acmp && app.loop.rx[MBX_CH_MAAP].ctx == &app.maap)
        << "U6 ACMP still stands in front of ADP's handler, and MAAP holds its own channel";
    std::vector<unsigned> slots;
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        slots.insert(slots.end(), {app.adp.ifs[i].slot, app.acmp.ifs[i].slot, app.maap.ifs[i].slot});
    }
    std::sort(slots.begin(), slots.end());
    EXPECT_TRUE(std::adjacent_find(slots.begin(), slots.end()) == slots.end() && slots.back() < MBX_N_TIMERS)
        << "U6 every interface's ADP, ACMP and MAAP slots are distinct and inside the timer bank";
    std::uint8_t record[spec::BINDING_BYTES] = {0x03, 0, 0, 1};
    wire_put_be(record + 4, kTkA, 8);
    ASSERT_EQ(acmp_restore_binding(core(), 1, record, sizeof record), ACMP_RESTORE_APPLIED);
    ASSERT_TRUE(ctrl_app_open(&app, &cfg));
    const std::uint32_t channels = (1u << MBX_CH_ADP) | (1u << MBX_CH_ACMP) | (1u << MBX_CH_MAAP);
    EXPECT_EQ(model.filter_en, channels) << "U6 opening opens the adp, acmp and maap channels and no other";
    EXPECT_EQ(model.irq_enable, mbx_place(channels, MBX_IRQ_ENABLE_RX_LSB, MBX_IRQ_ENABLE_RX_WIDTH) |
                                    mbx_place(1u, MBX_IRQ_ENABLE_EVT_LSB, MBX_IRQ_ENABLE_EVT_WIDTH))
        << "U6 with each one's receive interrupt and the events'";
    EXPECT_TRUE(model.bound_en[acfg.sink_interface[1]][1] && model.bound_eid[acfg.sink_interface[1]][1] == kTkA)
        << "U6 the binding restored between compose and open reaches the bound-talker table";
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        EXPECT_EQ(app.maap.ifs[i].core.state, MAAP_PROBE) << on_if(i, "U6 MAAP probes from the open");
    }
    // Four seconds: MAAP's probes and its acquisition, ADP's advertisements and
    // the restored sink's TMR_NO_ADP, each on its own slots.
    for (unsigned ms = 0; ms < 4000u; ms += 10u) {
        mbx_model_advance_ms(&model, 10u);
        settle();
    }
    std::array<unsigned, MBX_N_CH> sent{};
    for (std::uint32_t k = 0; k < model.tx_sent; ++k) {
        ++sent[mbx_model_tx_frame(&model, k)->channel];
    }
    EXPECT_TRUE(sent[MBX_CH_ADP] > 0u && sent[MBX_CH_MAAP] >= 3u * MBX_N_IF)
        << "U6 ADP advertises and MAAP probes on every interface";
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        EXPECT_EQ(app.maap.ifs[i].core.state, MAAP_DEFEND) << on_if(i, "U6 MAAP acquires its range");
        EXPECT_TRUE(app.adp.ifs[i].stale_expiries == 0u && app.acmp.ifs[i].stale_expiries == 0u &&
                    app.maap.ifs[i].stale_expiries == 0u)
            << on_if(i, "U6 no module takes an expiry of another's arm");
        EXPECT_TRUE(holds(app.adp.ifs[i]) && holds(app.acmp.ifs[i]) && holds(app.maap.ifs[i]))
            << on_if(i, "U6 and each slot holds its own module's current arm");
    }
    EXPECT_TRUE(published.valid && published.base == kMaapBase && published.count == kEntity.talker_stream_sources)
        << "U6 the acquired range reaches the stream-address port";
}

TEST_F(AcmpMailbox, U7TheThreeWayCompositionRefusesWithNothingOpened) {
    mbx_model_reset(&model);
    const std::uint64_t before = model.reads + model.writes;
    ctrl_app_config cfg = three_way();
    cfg.maap_preferred = MAAP_POOL_BASE - 1u;
    EXPECT_FALSE(ctrl_app_start(&app, &cfg)) << "U7 a preferred range below the B.4 pool is refused";
    cfg.maap_preferred = MAAP_POOL_BASE + MAAP_POOL_SIZE - kEntity.talker_stream_sources + 1u;
    EXPECT_FALSE(ctrl_app_start(&app, &cfg)) << "U7 one that runs past the pool's end is refused";
    cfg.maap_preferred = MAAP_POOL_BASE + MAAP_POOL_SIZE - kEntity.talker_stream_sources;
    EXPECT_TRUE(ctrl_app_compose(&app, &cfg)) << "U7 the pool's last range is not";
    adp_entity silent = kEntity;
    silent.talker_stream_sources = 0u;
    cfg = three_way();
    cfg.entity = &silent;
    EXPECT_FALSE(ctrl_app_compose(&app, &cfg)) << "U7 MAAP for an entity with no talker source is refused";
    acfg.n_sinks = ACMP_MAX_SINKS + 1u;
    cfg = three_way();
    EXPECT_FALSE(ctrl_app_start(&app, &cfg)) << "U7 a refused ACMP configuration fails the three-way composition";
    EXPECT_TRUE(app.loop.rx[MBX_CH_MAAP].fn == nullptr) << "U7 before MAAP attaches";
    acfg = acmp_shape();
    EXPECT_FALSE(ctrl_app_start_maap(&app, &cfg, nullptr, nullptr, 0u))
        << "U7 the explicit MAAP entry refuses a missing stream-address port";
    EXPECT_TRUE(model.reads + model.writes == before && model.filter_en == 0u && model.irq_enable == 0u)
        << "U7 and no refusal touched a mailbox register";
}

}  // namespace
