// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_acmp_mbx.cpp - the ACMP module on the mailbox (#665 lane F3; GoogleTest):
//
//   B   the adapter on the host model: the acmp channel and its filter, the
//       own-unicast receive tolerance, the timers on one fabric slot per
//       interface with the tag rule for raced expiries, the ADP channel's tap
//       (ENTITY_DISCOVER still ADP's), the gPTP pair, the adapter's refusals;
//   C   every response path's service cost, counted access by access on the
//       model in the pass that takes the input (acmp_mbx.h ACMP_MBX_LAT_*):
//       the H-ACMP and H-DISC hooks of FR_NFR.md 3.4.2 on the host model;
//   E   a response owed behind a full transmit ring under a HAL that sleeps,
//       its change reported only after its TX_HEAD commit (#653), and the
//       pass in which it is committed with k frames owed ahead of it;
//   F   the bound with full legal backlogs: both rings full, every pass and
//       path held to the stated figures, events first in every pass;
//   U   the composition: ACMP after ADP, nothing read before the contract
//       check, the boot order's two halves.
//
// The tree's contract passes no ENTITY_AVAILABLE or ENTITY_DEPARTING into the
// adp channel (sw/mailbox/mailbox.yaml; the open item of
// docs/design/MAILBOX_SPLIT.md). The H-DISC paths are therefore measured from
// a record this test writes into the adp receive ring in the contract's
// record layout, as the fabric would post it once the contract carries the
// term; from RX_HEAD on, the driver, the loop, the tap and the core run as
// they do for any record. B5 first shows the tree's filter dropping the frame.

#include <gtest/gtest.h>

#include <cstddef>
#include <cstdint>
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

acmp_config acmp_shape() {
    acmp_config c{};
    c.entity_id = kOwn;
    c.n_interfaces = MBX_N_IF;
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        c.mac[i] = kMac0;
    }
    c.n_sinks = 2;
    c.n_sources = 2;
    return c;
}

ctrl_app_config app_config() {
    return ctrl_app_config{&kEntity, 0, arena, sizeof arena, kClasses, 1, nullptr, nullptr, &acfg, &kEnv};
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
void bound(const char* path, std::uint64_t accesses, unsigned limit) {
    std::printf("  %-52s %4u accesses (bound %u)\n", path, static_cast<unsigned>(accesses), limit);
    EXPECT_TRUE(accesses <= limit) << path;
}

// A frame offered to the model's ingress; true when the filter committed it.
bool offer(const Pdu& p, std::uint64_t dst = ACMP_MULTICAST_MAC) {
    auto f = acmpdu(p);
    wire_put_be(f.data(), dst, 6);
    return mbx_model_rx(&model, f.data(), f.size(), 0);
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

void post_adp(const Adp& d) {
    auto f = adpdu(d);
    post_adp_record(f.data(), f.size());
}

// The k-th frame the model sent, read back.
Pdu wire(std::uint32_t k) {
    const mbx_model_tx* t = mbx_model_tx_frame(&model, k);
    return t != nullptr ? read(t->bytes) : Pdu{};
}

const struct mbx_model_tmr_op* last_tmr() {
    return mbx_model_tmr_op(&model, model.tmr_ops - 1u);
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
        mbx_model_set_gm(&model, 0, kGm0, 0);
        const ctrl_app_config cfg = app_config();
        ASSERT_TRUE(ctrl_app_start(&app, &cfg)) << "B0 the app with ACMP starts on the model";
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
    Pdu answer(unsigned k, std::uint8_t status = ACMP_STATUS_SUCCESS) const {
        const acmp_sink& s = core()->sinks[k];
        Pdu p;
        p.msg = ACMP_MSG_PROBE_TX_RESPONSE;
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
    // Run the model to the ACMP slot's armed deadline.
    void to_deadline() {
        const mbx_model_timer& t = model.timers[CTRL_APP_ACMP_FIRST_SLOT];
        ASSERT_TRUE(t.armed);
        mbx_model_advance_ms(&model, t.deadline_ms - model.now_ms);
    }
    void bind(unsigned k) {
        ASSERT_TRUE(offer(command(ACMP_MSG_BIND_RX_COMMAND, k)));
        settle();
    }
    void restore(unsigned k) {
        std::uint8_t record[ACMP_BINDING_BYTES] = {0x03, 0, 0, 1};
        wire_put_be(record + 4, kTkA, 8);
        wire_put_be(record + 12, kCtl1, 8);
        ASSERT_EQ(acmp_restore_binding(core(), k, record, sizeof record), ACMP_RESTORE_APPLIED);
    }
};

// ---- B: the adapter on the model ------------------------------------------------------

TEST_F(AcmpMailbox, B1TheChannelCarriesCommandsAndResponsesInOrder) {
    std::uint32_t sent = model.tx_sent;
    ASSERT_TRUE(offer(command(ACMP_MSG_BIND_RX_COMMAND, 0))) << "B1 the filter passes a BIND_RX for this listener";
    settle();
    ASSERT_EQ(model.tx_sent, sent + 2u) << "B1 two frames leave";
    const mbx_model_tx* r = mbx_model_tx_frame(&model, sent);
    const mbx_model_tx* p = mbx_model_tx_frame(&model, sent + 1u);
    EXPECT_TRUE(r->channel == MBX_CH_ACMP && r->interface == 0u && r->len == ACMP_FRAME_BYTES &&
                read(r->bytes).msg == ACMP_MSG_BIND_RX_RESPONSE && p->channel == MBX_CH_ACMP &&
                read(p->bytes).msg == ACMP_MSG_PROBE_TX_COMMAND)
        << "B1 the response, then the probe, on the acmp channel, 70 bytes each, in commit order";
    EXPECT_TRUE((wire_be64(r->bytes) >> 16) == ACMP_MULTICAST_MAC && (wire_be64(r->bytes + 6) >> 16) == kMac0)
        << "B1 to the ACMP multicast address from the interface's MAC";
    Pdu other = command(ACMP_MSG_BIND_RX_COMMAND, 1);
    other.listener = kTkB;
    EXPECT_FALSE(offer(other)) << "B1 a BIND_RX for another listener never reaches the core (the identity term)";
    EXPECT_TRUE(offer(talker_command(ACMP_MSG_GET_TX_STATE_COMMAND))) << "B1 a GET_TX_STATE for this talker passes";
    settle();
    EXPECT_EQ(wire(model.tx_sent - 1u).msg, ACMP_MSG_GET_TX_STATE_RESPONSE) << "B1 and is answered";
}

TEST_F(AcmpMailbox, B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused) {
    ASSERT_TRUE(offer(command(ACMP_MSG_GET_RX_STATE_COMMAND, 0), kMac0))
        << "B2 a command to this interface's own unicast MAC passes (the owner's receive tolerance)";
    settle();
    EXPECT_EQ(wire(model.tx_sent - 1u).msg, ACMP_MSG_GET_RX_STATE_RESPONSE)
        << "B2 and is answered, to the multicast address (8.2.1)";
    std::uint16_t mismatch = model.filter_mismatch;
    EXPECT_FALSE(offer(command(ACMP_MSG_GET_RX_STATE_COMMAND, 0), kMac0 ^ 1u)) << "B2 a foreign unicast is refused";
    EXPECT_EQ(model.filter_mismatch, mismatch + 1u) << "B2 and counted once in FILTER_MISMATCH";
}

TEST_F(AcmpMailbox, B3TheTimersRunOnTheInterfaceSlot) {
    std::uint32_t t0 = model.now_ms;
    bind(0);
    const struct mbx_model_tmr_op* arm = last_tmr();
    EXPECT_TRUE(arm->op == MBX_TMR_OP_ARM && arm->slot == CTRL_APP_ACMP_FIRST_SLOT &&
                arm->deadline_ms == t0 + ACMP_TMR_NO_RESP_MS && app.acmp.ifs[0].armed)
        << "B3 TMR_NO_RESP is armed on the interface's ACMP slot at NOW_MS + 200 (Table 5.26)";
    std::uint32_t sent = model.tx_sent;
    mbx_model_advance_ms(&model, ACMP_TMR_NO_RESP_MS - 1u);
    settle();
    EXPECT_EQ(model.tx_sent, sent) << "B3 nothing at 199 ms";
    mbx_model_advance_ms(&model, 1);
    settle();
    const mbx_model_tx* dup = mbx_model_tx_frame(&model, sent);
    EXPECT_TRUE(model.tx_sent == sent + 1u && dup != nullptr && dup->now_ms == t0 + ACMP_TMR_NO_RESP_MS &&
                read(dup->bytes).msg == ACMP_MSG_PROBE_TX_COMMAND && core()->sinks[0].state == ACMP_PRB_W_RESP2)
        << "B3 the duplicate leaves at 200 ms exactly (5.5.3.5.16)";
}

TEST_F(AcmpMailbox, B4AnExpiryThatRacedAStopOrAReArmIsDiscarded) {
    bind(0);
    ASSERT_TRUE(offer(answer(0)));
    settle();
    ASSERT_EQ(core()->sinks[0].state, ACMP_SETTLED_NO_RSV);
    to_deadline();                                       // TMR_NO_TK's expiry is posted, not yet taken
    acmp_tk_registered(core(), 0, false);                // the SRP side, from another handler: nothing left to time
    settle();
    EXPECT_TRUE(app.acmp.ifs[0].stale_expiries == 1u && core()->sinks[0].state == ACMP_SETTLED_RSV_OK &&
                !app.acmp.ifs[0].armed)
        << "B4 the expiry of a stopped arm is counted, never acted on";
    SetUp();
    bind(0);
    post_adp(Adp{});                                     // discovered: TMR_NO_ADP 20 s runs beside TMR_NO_TK 10 s
    settle();
    ASSERT_TRUE(offer(answer(0)));
    settle();
    to_deadline();
    acmp_tk_registered(core(), 0, false);                // the slot re-armed at TMR_NO_ADP with a new tag
    settle();
    EXPECT_TRUE(app.acmp.ifs[0].stale_expiries == 1u && core()->sinks[0].state == ACMP_SETTLED_RSV_OK &&
                app.acmp.ifs[0].armed && model.timers[CTRL_APP_ACMP_FIRST_SLOT].deadline_ms ==
                core()->sinks[0].adp_deadline)
        << "B4 the expiry of a replaced arm carries its old tag and is discarded; the new arm stands";
    mbx_event other{};
    other.type = MBX_EV_TYPE_TIMER;
    other.timer_slot = CTRL_APP_ADP_FIRST_SLOT;
    for (unsigned i = 0; i < app.loop.n_sinks; ++i) {
        if (app.loop.sinks[i].ctx == &app.acmp) {
            app.loop.sinks[i].fn(app.loop.sinks[i].ctx, &other);
        }
    }
    EXPECT_TRUE(app.acmp.ifs[0].stale_expiries == 1u && app.acmp.ifs[0].armed)
        << "B4 another module's slot is not ACMP's";
}

TEST_F(AcmpMailbox, B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp) {
    restore(0);
    auto avail = adpdu(Adp{});
    EXPECT_FALSE(mbx_model_rx(&model, avail.data(), avail.size(), 0))
        << "B5 the tree's contract passes no ENTITY_AVAILABLE into the adp channel (the published blocker)";
    post_adp(Adp{});
    settle();
    EXPECT_TRUE(core()->sinks[0].discovered && core()->sinks[0].state == ACMP_PRB_W_DELAY)
        << "B5 a record the contract's term would post reaches discovery through the tap (5.5.3.5.9)";
    mbx_model_set_link(&model, 0, true);
    for (unsigned k = 0; k < 12000u && app.adp.ifs[0].adp.state != ADP_STATE_WAITING; ++k) {
        mbx_model_advance_ms(&model, 1);
        settle();
    }
    ASSERT_EQ(app.adp.ifs[0].adp.state, ADP_STATE_WAITING);
    std::uint8_t discover[ACMP_ADP_FRAME_BYTES] = {};
    wire_put_be(discover, 0x91E0F0010000ull, 6);
    wire_put_be(discover + 12, ACMP_ETHERTYPE, 2);
    discover[14] = ACMP_ADP_SUBTYPE;
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
    restore(0);
    mbx_model_set_gm(&model, 0, kGm0 + 7u, 3);
    Adp d;
    d.gm = kGm0;
    post_adp(d);
    settle();
    EXPECT_FALSE(core()->sinks[0].discovered) << "B6 an AVAILABLE from another grandmaster than GM_LO/GM_HI is ignored";
    d.gm = kGm0 + 7u;
    d.domain = 3;
    post_adp(d);
    settle();
    EXPECT_TRUE(core()->sinks[0].discovered) << "B6 one from the interface's grandmaster and domain is taken";
}

TEST(AcmpAdapterUnit, B7RefusalsOfTheAdapter) {
    acmp_mbx m{};
    acmp_config c = acmp_shape();
    EXPECT_FALSE(acmp_mbx_init(&m, &c, &kEnv, MBX_N_TIMERS - MBX_N_IF + 1u))
        << "B7 slots past the fabric's timer bank are refused";
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

// ---- C: the service cost of every path (H-ACMP, H-DISC) -----------------------------------

TEST_F(AcmpMailbox, C0ToC4CommandsAreAnsweredInThePassThatTakesThem) {
    std::uint32_t sent = model.tx_sent;
    ASSERT_TRUE(offer(command(ACMP_MSG_BIND_RX_COMMAND, 0)));
    std::uint64_t n = pass();
    EXPECT_EQ(model.tx_sent, sent + 2u) << "C0 BIND_RX: the response and the probe in the pass that takes it";
    bound("C0 BIND_RX -> response, PROBE_TX, TMR_NO_RESP", n, ACMP_MBX_LAT_BIND);
    ASSERT_TRUE(offer(command(ACMP_MSG_GET_RX_STATE_COMMAND, 0)));
    n = pass();
    EXPECT_EQ(model.tx_sent, sent + 3u) << "C1 GET_RX_STATE answered in one pass";
    bound("C1 GET_RX_STATE -> response", n, ACMP_MBX_LAT_GET_RX);
    ASSERT_TRUE(offer(answer(0)));
    n = pass();
    EXPECT_EQ(core()->sinks[0].state, ACMP_SETTLED_NO_RSV) << "C2 PROBE_TX_RESPONSE settles in one pass";
    bound("C2 PROBE_TX_RESPONSE -> TMR_NO_TK armed", n, ACMP_MBX_LAT_PROBE_RESP);
    ASSERT_TRUE(offer(command(ACMP_MSG_UNBIND_RX_COMMAND, 0)));
    n = pass();
    EXPECT_TRUE(model.tx_sent == sent + 4u && core()->sinks[0].state == ACMP_UNBOUND)
        << "C3 UNBIND_RX answered in one pass";
    bound("C3 UNBIND_RX -> response, timer stopped", n, ACMP_MBX_LAT_UNBIND);
    for (std::uint8_t msg : {ACMP_MSG_PROBE_TX_COMMAND, ACMP_MSG_GET_TX_STATE_COMMAND,
                             ACMP_MSG_DISCONNECT_TX_COMMAND, ACMP_MSG_GET_TX_CONNECTION_COMMAND}) {
        std::uint32_t before = model.tx_sent;
        ASSERT_TRUE(offer(talker_command(msg)));
        n = pass();
        EXPECT_EQ(model.tx_sent, before + 1u) << "C4 a talker command is answered in one pass";
        bound("C4 talker command -> response", n, ACMP_MBX_LAT_TALKER);
    }
    bind(1);
    ASSERT_TRUE(offer(answer(1, 5u)));
    n = pass();
    bound("C2 PROBE_TX_RESPONSE (failed) -> TMR_RETRY armed", n, ACMP_MBX_LAT_PROBE_RESP);
}

TEST_F(AcmpMailbox, C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry) {
    bind(0);
    to_deadline();
    std::uint32_t sent = model.tx_sent;
    std::uint64_t n = pass();
    EXPECT_TRUE(model.tx_sent == sent + 1u && core()->sinks[0].state == ACMP_PRB_W_RESP2)
        << "C5 TMR_NO_RESP: the duplicate in the pass that takes the expiry";
    bound("C5 TMR_NO_RESP -> duplicate PROBE_TX, TMR_NO_RESP", n, ACMP_MBX_LAT_TIMER_PROBE);
    to_deadline();
    n = pass();
    EXPECT_EQ(core()->sinks[0].state, ACMP_PRB_W_RETRY) << "C6 the second TMR_NO_RESP";
    bound("C6 TMR_NO_RESP -> TMR_RETRY armed", n, ACMP_MBX_LAT_TIMER_ARM);
    post_adp(Adp{});
    settle();
    to_deadline();
    n = pass();
    EXPECT_EQ(core()->sinks[0].state, ACMP_PRB_W_DELAY) << "C7 TMR_RETRY, talker discovered";
    bound("C7 TMR_RETRY -> TMR_DELAY armed", n, ACMP_MBX_LAT_TIMER_ARM);
    to_deadline();
    n = pass();
    EXPECT_EQ(core()->sinks[0].state, ACMP_PRB_W_RESP) << "C8 TMR_DELAY";
    bound("C8 TMR_DELAY -> PROBE_TX, TMR_NO_RESP", n, ACMP_MBX_LAT_TIMER_PROBE);
    ASSERT_TRUE(offer(answer(0)));
    settle();
    to_deadline();
    n = pass();
    EXPECT_EQ(core()->sinks[0].state, ACMP_PRB_W_DELAY) << "C9 TMR_NO_TK, talker discovered";
    bound("C9 TMR_NO_TK -> TMR_DELAY armed", n, ACMP_MBX_LAT_TIMER_ARM);
}

TEST_F(AcmpMailbox, C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord) {
    restore(0);
    post_adp(Adp{});
    std::uint64_t n = pass();
    EXPECT_EQ(core()->sinks[0].state, ACMP_PRB_W_DELAY) << "C10 ENTITY_AVAILABLE: TMR_DELAY in the same pass";
    bound("C10 ENTITY_AVAILABLE -> TMR_DELAY armed (H-DISC)", n, ACMP_MBX_LAT_AVAILABLE);
    Adp gone;
    gone.msg = ACMP_ADP_MSG_ENTITY_DEPARTING;
    post_adp(gone);
    n = pass();
    EXPECT_TRUE(core()->sinks[0].state == ACMP_PRB_W_AVAIL && !app.acmp.ifs[0].armed)
        << "C11 ENTITY_DEPARTING: PRB_W_AVAIL, the slot stopped, in the same pass";
    bound("C11 ENTITY_DEPARTING -> timer stopped (H-DISC)", n, ACMP_MBX_LAT_DEPARTING);
}

TEST_F(AcmpMailbox, C12AgingIsServedInThePassThatTakesTheExpiry) {
    bind(0);
    Adp v;
    v.valid_time = 1;
    post_adp(v);
    settle();
    ASSERT_TRUE(offer(answer(0)));
    settle();
    ASSERT_EQ(model.timers[CTRL_APP_ACMP_FIRST_SLOT].deadline_ms, core()->sinks[0].adp_deadline)
        << "C12 TMR_NO_ADP (2 s) is the slot's earliest deadline";
    to_deadline();
    std::uint64_t n = pass();
    EXPECT_TRUE(!core()->sinks[0].discovered && core()->sinks[0].state == ACMP_SETTLED_NO_RSV)
        << "C12 TMR_NO_ADP: TK_NOT_DISCOVERED in the pass that takes the expiry (5.6.4.5.4)";
    bound("C12 TMR_NO_ADP -> TK_NOT_DISCOVERED, timer re-armed (H-DISC)", n, ACMP_MBX_LAT_NO_ADP);
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
    p.msg = ACMP_MSG_GET_RX_STATE_RESPONSE;
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
    ASSERT_TRUE(offer(command(ACMP_MSG_BIND_RX_COMMAND, 0)));
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
    EXPECT_EQ(wire(drained).msg, ACMP_MSG_BIND_RX_RESPONSE) << "E1 and the response is the first frame after the room";
    settle();
    EXPECT_TRUE(wire(drained + 1u).msg == ACMP_MSG_PROBE_TX_COMMAND && core()->owed_count == 0u)
        << "E1 then the probe; nothing owed";
    mbx_model_bind(&model, nullptr, nullptr);
}

TEST_F(AcmpMailbox, E2AnOwedResponseIsCommittedInPassKPlus1) {
    for (unsigned k : {0u, 3u, ACMP_OWED_MAX - 1u}) {
        SetUp();
        fill_acmp_tx();
        for (unsigned j = 0; j < k; ++j) {
            ASSERT_TRUE(offer(command(ACMP_MSG_GET_RX_STATE_COMMAND, 1, kCtl2, static_cast<std::uint16_t>(j))));
            mbx_model_advance_ms(&model, MBX_CH_ACMP_RATE_REFILL_MS);
            settle();
        }
        ASSERT_TRUE(offer(command(ACMP_MSG_GET_RX_STATE_COMMAND, 0, kCtl1, 0x7777)));
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
    for (unsigned slot = 0; slot < MBX_N_TIMERS; ++slot) {
        if (slot != CTRL_APP_ACMP_FIRST_SLOT) {
            mbx_timer_arm(slot, 0x77u, mbx_now_ms());
        }
    }
    to_deadline();                                       // every sink's TMR_NO_RESP: the slot's expiry, last
    ASSERT_EQ(static_cast<std::uint16_t>(model.evt_head - model.evt_tail), MBX_EVT_WORDS)
        << "F0 the event ring is full";
    unsigned stored = 0;
    for (unsigned j = 0; j < 100000u && model.ch[MBX_CH_ACMP].rx_drop == 0u; ++j) {
        Pdu p = command(ACMP_MSG_BIND_RX_COMMAND, j % acfg.n_sinks, kCtl1, static_cast<std::uint16_t>(j));
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
    auto f = acmpdu(talker_command(ACMP_MSG_GET_TX_STATE_COMMAND));
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
    ASSERT_TRUE(ctrl_app_open(&app, &cfg));
    EXPECT_TRUE(mbx_field(model.filter_en, 0u, 8u) == ((1u << MBX_CH_ADP) | (1u << MBX_CH_ACMP)) &&
                ((model.irq_enable >> MBX_CH_ACMP) & 1u) == 1u)
        << "U5 opening opens the acmp channel and its interrupt";
    acmp_config bad = acmp_shape();
    bad.n_sinks = ACMP_MAX_SINKS + 1u;
    acfg = bad;
    EXPECT_FALSE(ctrl_app_compose(&app, &cfg)) << "U5 an ACMP configuration the module refuses fails the composition";
}

}  // namespace
