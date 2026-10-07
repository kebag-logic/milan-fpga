// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_acmp.cpp - the ACMP core over fake ports (#665 lane F3; GoogleTest):
//
//   A   every listener command, response, timer and SRP event of Milan v1.2
//       5.5.3 in the states Table 5.30 gives it, each response field by field
//       against its table; the talker's answers of 5.5.4; the lock; response
//       routing by the consumer's unique ID; sequence IDs; the per-interface
//       timers; owed frames and the response-before-notification rule (#653);
//       the discovery machine of 5.6.4 cell by cell; the saved binding record;
//       the no-callback guard (#678).
//
// The walk of the processor's own Table 5.30 transcription is acmp_walk.cpp;
// the mailbox adapter, the latency bounds and the composition are
// test_acmp_mbx.cpp; the saved-state store is test_acmp_nvm.cpp.

#include <gtest/gtest.h>

#include <algorithm>
#include <cstdint>
#include <cstring>
#include <functional>

#include "acmp.h"
#include "acmp_fake.hpp"
#include "fw_gtest.hpp"
#include "wire.h"

FW_TALLY_LABEL("ctrl ACMP core and adapter (fake ports and host model)");

using namespace acmp_test;

// The host test build asserts the no-callback rule (CTRL_REENTRY_ASSERT): each
// refused call lands here.
namespace {
unsigned reentry_traps;
}

extern "C" void ctrl_reentry_assert(const char* module) {
    static_cast<void>(module);
    reentry_traps++;
}

namespace {

class AcmpCore : public ::testing::Test {
 protected:
    void SetUp() override {
        fk = Fake{};
        reentry_traps = 0;
        cfg = acmp_config{};
        cfg.entity_id = kOwn;
        cfg.n_interfaces = 2;
        cfg.mac[0] = kMac0;
        cfg.mac[1] = kMac1;
        cfg.n_sinks = 3;
        cfg.sink_interface[0] = 0;
        cfg.sink_interface[1] = 0;
        cfg.sink_interface[2] = 1;
        cfg.n_sources = 2;
        cfg.source_interface[0] = 0;
        cfg.source_interface[1] = 1;
        for (unsigned i = 0; i < ACMP_MAX_SOURCES; ++i) {
            fk.source[i] = acmp_source_state{true, {kSid + i, kDa + i, 2u}, false};
        }
        ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kEnv));
    }

    void rx(const Pdu& p, unsigned interface = 0) {
        auto f = acmpdu(p);
        acmp_rx(&a, interface, f.data(), f.size());
    }
    void adp(const Adp& d, unsigned interface = 0) {
        auto f = adpdu(d);
        acmp_adp_rx(&a, interface, f.data(), f.size());
    }
    static Pdu command(std::uint8_t msg, unsigned sink, std::uint64_t talker = kTkA, std::uint16_t uid = 1,
                       std::uint64_t ctlr = kCtl1, std::uint16_t flags = 0, std::uint16_t seq = 0x4100) {
        Pdu p;
        p.msg = msg;
        p.controller = ctlr;
        p.talker = talker;
        p.listener = kOwn;
        p.talker_uid = uid;
        p.listener_uid = static_cast<std::uint16_t>(sink);
        p.flags = flags;
        p.seq = seq;
        return p;
    }
    void bind(unsigned sink, std::uint64_t talker = kTkA, std::uint16_t uid = 1, std::uint64_t ctlr = kCtl1,
              bool sw = false) {
        rx(command(spec::MSG_BIND_RX_COMMAND, sink, talker, uid, ctlr, sw ? spec::FLAG_STREAMING_WAIT : 0u),
           a.sinks[sink].interface);
    }
    // The talker's answer to sink k's outstanding probe.
    Pdu probe_answer(unsigned k, std::uint8_t status = spec::STATUS_SUCCESS) const {
        const acmp_sink& s = a.sinks[k];
        Pdu p;
        p.msg = spec::MSG_PROBE_TX_RESPONSE;
        p.status = status;
        p.controller = s.probe_controller;
        p.talker = s.probe_talker;
        p.listener = kOwn;
        p.talker_uid = s.probe_talker_uid;
        p.listener_uid = static_cast<std::uint16_t>(k);
        p.seq = s.probe_seq;
        p.stream_id = kSid + k;
        p.dest_mac = kDa + k;
        p.vlan = 2;
        return p;
    }
    // Run the clock to sink k's connection deadline and deliver its interface's expiry.
    void fire(unsigned k) {
        fk.now = a.sinks[k].timer_deadline;
        acmp_timer_expired(&a, a.sinks[k].interface);
    }
    void fire_adp(unsigned k) {
        fk.now = a.sinks[k].adp_deadline;
        acmp_timer_expired(&a, a.sinks[k].interface);
    }
    // Sink k to `st` through legitimate stimulus only.
    void to_state(unsigned k, acmp_sink_state st) {
        if (st == ACMP_UNBOUND) {
            return;
        }
        if (st == ACMP_PRB_W_AVAIL || st == ACMP_PRB_W_DELAY) {
            bind(k);
            adp(Adp{}, a.sinks[k].interface);
            Adp gone;
            gone.msg = spec::ADPDU_ENTITY_DEPARTING;
            adp(gone, a.sinks[k].interface);            // 5.5.3.5.22: PRB_W_AVAIL
            if (st == ACMP_PRB_W_DELAY) {
                Adp back;
                back.index = 2;
                adp(back, a.sinks[k].interface);        // 5.5.3.5.9
            }
            return;
        }
        bind(k);
        if (st == ACMP_PRB_W_RESP2) {
            fire(k);
        } else if (st == ACMP_PRB_W_RETRY) {
            rx(probe_answer(k, 5u), a.sinks[k].interface);
        } else if (st == ACMP_SETTLED_NO_RSV || st == ACMP_SETTLED_RSV_OK) {
            rx(probe_answer(k), a.sinks[k].interface);
            if (st == ACMP_SETTLED_RSV_OK) {
                acmp_tk_registered(&a, k, false);
            }
        }
    }
    Pdu last() const { return read(fk.sent.back().bytes.data()); }
    acmp_sink_view view(unsigned k) const {
        acmp_sink_view v{};
        static_cast<void>(acmp_view(&a, k, &v));
        return v;
    }

    acmp_config cfg{};
    acmp a{};
};

// An xorshift32 state whose next TMR_DELAY draw is `ms`, by the core's own rule
// (one step, the high 16 bits scaled to 0..1000).
std::uint32_t state_drawing(std::uint32_t ms) {
    for (std::uint32_t s = 1;; ++s) {
        std::uint32_t x = s;
        x ^= x << 13;
        x ^= x >> 17;
        x ^= x << 5;
        if ((((x >> 16) * (spec::TMR_DELAY_MAX_MS + 1u)) >> 16) == ms) {
            return s;
        }
    }
}

constexpr acmp_sink_state kStates[] = {ACMP_UNBOUND,     ACMP_PRB_W_AVAIL,    ACMP_PRB_W_DELAY,
                                       ACMP_PRB_W_RESP,  ACMP_PRB_W_RESP2,    ACMP_PRB_W_RETRY,
                                       ACMP_SETTLED_NO_RSV, ACMP_SETTLED_RSV_OK};

// ---- A0: the configuration ----------------------------------------------------------

TEST_F(AcmpCore, A0InitRefusesWhatTheStaticSizesCannotHold) {
    // each configuration below is wrong in one way only, so no other check refuses it
    acmp b{};
    acmp_config bad = cfg;
    bad.n_interfaces = 0;
    bad.n_sinks = 0;
    bad.n_sources = 0;
    EXPECT_FALSE(acmp_init(&b, &bad, &kPorts, &kEnv)) << "A0 no interface is refused";
    bad = cfg;
    bad.n_interfaces = ACMP_MAX_INTERFACES + 1u;
    EXPECT_FALSE(acmp_init(&b, &bad, &kPorts, &kEnv)) << "A0 more interfaces than ACMP_MAX_INTERFACES are refused";
    bad = cfg;
    bad.n_sinks = ACMP_MAX_SINKS + 1u;
    bad.n_sources = 0;                                   // what a 17th sink's interface would be read from
    for (std::uint8_t& i : bad.sink_interface) {
        i = 0;
    }
    EXPECT_FALSE(acmp_init(&b, &bad, &kPorts, &kEnv)) << "A0 more sinks than ACMP_MAX_SINKS are refused";
    bad = cfg;
    bad.n_sources = ACMP_MAX_SOURCES + 1u;
    for (std::uint8_t& i : bad.source_interface) {
        i = 0;
    }
    EXPECT_FALSE(acmp_init(&b, &bad, &kPorts, &kEnv)) << "A0 more sources than ACMP_MAX_SOURCES are refused";
    bad = cfg;
    bad.sink_interface[2] = 2;
    EXPECT_FALSE(acmp_init(&b, &bad, &kPorts, &kEnv)) << "A0 a sink on an interface the entity lacks is refused";
    bad = cfg;
    bad.source_interface[1] = 2;
    EXPECT_FALSE(acmp_init(&b, &bad, &kPorts, &kEnv)) << "A0 a source on an interface the entity lacks is refused";
}

TEST_F(AcmpCore, A0EverySinkStartsUnboundAndNothingIsCalled) {
    for (unsigned k = 0; k < cfg.n_sinks; ++k) {
        acmp_sink_view v = view(k);
        EXPECT_TRUE(v.state == ACMP_UNBOUND && !v.bound && v.probing_status == ACMP_PROBING_DISABLED &&
                    v.acmp_status == 0u)
            << "A0 every sink starts UNBOUND, probing disabled, ACMP status 0 (5.5.3.5.1)";
    }
    EXPECT_TRUE(fk.calls.empty()) << "A0 init calls no port: nothing reads the mailbox before it is open";
    EXPECT_EQ(a.sinks[2].interface, 1u) << "A0 each sink keeps its descriptor's AVB interface";
    acmp_sink_view v{};
    EXPECT_FALSE(acmp_view(&a, cfg.n_sinks, &v)) << "A0 there is no view of a sink the configuration lacks";
    EXPECT_FALSE(acmp_change_pending(&a, cfg.n_sinks)) << "A0 nor a pending change";
}

// ---- A1: BIND_RX from UNBOUND (5.5.3.5.3) ------------------------------------------

TEST_F(AcmpCore, A1BindFromUnboundRespondsThenProbes) {
    rx(command(spec::MSG_BIND_RX_COMMAND, 0, kTkA, 1, kCtl1, spec::FLAG_STREAMING_WAIT | spec::FLAG_FAST_CONNECT, 0x4100));
    ASSERT_EQ(fk.sent.size(), 2u) << "A1 BIND_RX sends two frames: the response and the probe";
    Pdu r = read(fk.sent[0].bytes.data());
    Pdu want;
    want.msg = spec::MSG_BIND_RX_RESPONSE;
    want.status = spec::STATUS_SUCCESS;
    want.controller = kCtl1;
    want.talker = kTkA;
    want.listener = kOwn;
    want.talker_uid = 1;
    want.listener_uid = 0;
    want.seq = 0x4100;
    want.count = 1;
    want.flags = spec::FLAG_STREAMING_WAIT;
    EXPECT_TRUE(same(r, want)) << "A1 BIND_RX_RESPONSE is Table 5.32 field by field";
    Pdu p = read(fk.sent[1].bytes.data());
    Pdu probe;
    probe.msg = spec::MSG_PROBE_TX_COMMAND;
    probe.controller = kCtl1;
    probe.talker = kTkA;
    probe.listener = kOwn;
    probe.talker_uid = 1;
    probe.listener_uid = 0;
    probe.seq = 0;
    probe.flags = spec::FLAG_FAST_CONNECT;
    EXPECT_TRUE(same(p, probe)) << "A1 PROBE_TX_COMMAND is Table 5.33 field by field";
    EXPECT_EQ(fk.sent[1].interface, 0u) << "A1 the probe leaves on the sink's AVB interface";
    const uint8_t* b = fk.sent[0].bytes.data();
    EXPECT_TRUE(wire_be64(b) >> 16 == spec::MULTICAST_MAC && (wire_be64(b + 6) >> 16) == kMac0 &&
                wire_be16(b + 12) == spec::ETHERTYPE && b[14] == spec::SUBTYPE &&
                (wire_be16(b + 16) & 0x07FFu) == spec::CONTROL_DATA_LENGTH && wire_be16(b + 68) == 0u)
        << "A1 every frame goes to the ACMP multicast address from the interface's MAC, cdl 44 (8.2.1, 5.5.2.2)";
    const acmp_sink& s = a.sinks[0];
    EXPECT_TRUE(s.state == ACMP_PRB_W_RESP && s.probing == ACMP_PROBING_ACTIVE && s.acmp_status == 0u)
        << "A1 then PRB_W_RESP, PROBING_ACTIVE, ACMP status 0";
    EXPECT_TRUE(s.timer == ACMP_TIMER_NO_RESP && s.timer_deadline == fk.now + spec::TMR_NO_RESP_MS &&
                fk.armed[0] && fk.at[0] == fk.now + spec::TMR_NO_RESP_MS)
        << "A1 and TMR_NO_RESP armed 200 ms out on the interface's timer (Table 5.26)";
    EXPECT_TRUE(s.disc_running && !s.discovered) << "A1 the discovery machine starts, talker not discovered";
    EXPECT_TRUE(s.bound && s.binding.talker_entity_id == kTkA && s.binding.talker_unique_id == 1u &&
                s.binding.controller_entity_id == kCtl1 && s.binding.streaming_wait && !s.started)
        << "A1 the binding parameters are the command's; STREAMING_WAIT binds it stopped";
    EXPECT_TRUE(fk.count(Call::PERSIST) == 1u && fk.calls[static_cast<unsigned>(fk.position(Call::PERSIST))].index == 0u)
        << "A1 the binding is saved (5.5.2.4)";
    EXPECT_TRUE(fk.count(Call::CHANGED) == 1u && fk.position(Call::CHANGED) > fk.position(Call::SEND, 0))
        << "A1 the change is reported after the response was taken (#653)";
}

TEST_F(AcmpCore, A1BindWithoutStreamingWaitBindsStarted) {
    bind(0, kTkA, 1, kCtl1, false);
    EXPECT_TRUE(a.sinks[0].started && !a.sinks[0].binding.streaming_wait && read(fk.sent[0].bytes.data()).flags == 0u)
        << "A1 a bind without STREAMING_WAIT lands started (IEEE 1722.1-2021 7.4.35)";
}

// ---- A2: GET_RX_STATE (Tables 5.34, 5.37, 5.38, 5.39) ------------------------------

TEST_F(AcmpCore, A2GetRxStateInEveryState) {
    for (acmp_sink_state st : kStates) {
        SetUp();
        to_state(0, st);
        fk.clear();
        fk.source[0].dest_mac_valid = true;
        acmp_sink_state before = a.sinks[0].state;
        rx(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, 0x4300));
        ASSERT_EQ(fk.sent.size(), 1u) << "A2 GET_RX_STATE is answered in state " << st;
        Pdu r = last();
        Pdu want;
        want.msg = spec::MSG_GET_RX_STATE_RESPONSE;
        want.controller = kCtl2;
        want.listener = kOwn;
        want.seq = 0x4300;
        if (st != ACMP_UNBOUND) {
            want.talker = kTkA;
            want.talker_uid = 1;
            want.count = 1;
            want.flags = spec::FLAG_FAST_CONNECT;
        }
        if (st == ACMP_SETTLED_NO_RSV || st == ACMP_SETTLED_RSV_OK) {
            want.stream_id = kSid;
            want.dest_mac = kDa;
            want.vlan = 2;
        }
        EXPECT_TRUE(same(r, want)) << "A2 GET_RX_STATE_RESPONSE is Table 5.34/5.37/5.38/5.39 in state " << st;
        EXPECT_TRUE(a.sinks[0].state == before && fk.count(Call::CHANGED) == 0u && fk.count(Call::PERSIST) == 0u)
            << "A2 and GET_RX_STATE changes nothing in state " << st;
    }
}

TEST_F(AcmpCore, A2GetRxStateReportsStreamingWaitAndRegisteringFailed) {
    bind(0, kTkA, 1, kCtl1, true);
    rx(probe_answer(0));
    acmp_tk_registered(&a, 0, true);
    fk.clear();
    rx(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2));
    EXPECT_EQ(last().flags, spec::FLAG_FAST_CONNECT | spec::FLAG_STREAMING_WAIT | spec::FLAG_REGISTERING_FAILED)
        << "A2 SETTLED_RSV_OK on a Talker Failed: STREAMING_WAIT saved, REGISTERING_FAILED 1 (Table 5.39)";
    EXPECT_TRUE(view(0).registering_failed && view(0).talker_registered) << "A2 and the view says so (5.3.8.8)";
}

TEST_F(AcmpCore, A2UnknownSinkIsAnsweredListenerUnknownId) {
    for (std::uint8_t msg : {spec::MSG_BIND_RX_COMMAND, spec::MSG_UNBIND_RX_COMMAND, spec::MSG_GET_RX_STATE_COMMAND}) {
        fk.clear();
        rx(command(msg, cfg.n_sinks, kTkA, 7, kCtl1, spec::FLAG_STREAMING_WAIT, 0x77));
        ASSERT_EQ(fk.sent.size(), 1u) << "A2 a command for a sink the entity lacks is answered, msg " << unsigned(msg);
        Pdu want;
        want.msg = static_cast<std::uint8_t>(msg + 1u);
        want.status = spec::STATUS_LISTENER_UNKNOWN_ID;
        want.controller = kCtl1;
        want.talker = kTkA;
        want.listener = kOwn;
        want.talker_uid = 7;
        want.listener_uid = static_cast<std::uint16_t>(cfg.n_sinks);
        want.seq = 0x77;
        EXPECT_TRUE(same(last(), want)) << "A2 LISTENER_UNKNOWN_ID, the command's fields echoed (Table 5.27)";
    }
    EXPECT_TRUE(a.unknown_sink == 3u && fk.count(Call::PERSIST) == 0u && fk.count(Call::CHANGED) == 0u)
        << "A2 and nothing changes";
}

// ---- A3: UNBIND_RX (Table 5.36) ----------------------------------------------------

TEST_F(AcmpCore, A3UnbindInEveryState) {
    for (acmp_sink_state st : kStates) {
        SetUp();
        to_state(0, st);
        fk.clear();
        rx(command(spec::MSG_UNBIND_RX_COMMAND, 0, kTkA, 1, kCtl1, 0, 0x4200));
        ASSERT_FALSE(fk.sent.empty()) << "A3 UNBIND_RX is answered in state " << st;
        Pdu want;
        want.msg = spec::MSG_UNBIND_RX_RESPONSE;
        want.controller = kCtl1;
        want.listener = kOwn;
        want.seq = 0x4200;
        EXPECT_TRUE(same(last(), want)) << "A3 UNBIND_RX_RESPONSE is Table 5.36: talker_entity_id and "
                                           "talker_unique_id 0, in state "
                                        << st;
        const acmp_sink& s = a.sinks[0];
        EXPECT_TRUE(s.state == ACMP_UNBOUND && !s.bound && s.probing == ACMP_PROBING_DISABLED && s.acmp_status == 0u &&
                    s.timer == ACMP_TIMER_NONE && !s.disc_running && !s.adp_armed && !s.started &&
                    s.binding.talker_entity_id == 0u && s.binding.controller_entity_id == 0u)
            << "A3 then UNBOUND, binding cleared, nothing running, in state " << st;
        EXPECT_EQ(fk.count(Call::PERSIST), st == ACMP_UNBOUND ? 0u : 1u)
            << "A3 the cleared binding is saved, unless there was none, in state " << st;
        bool settled = st == ACMP_SETTLED_NO_RSV || st == ACMP_SETTLED_RSV_OK;
        EXPECT_TRUE(!settled || (fk.count(Call::SRP) == 1u && !fk.calls[unsigned(fk.position(Call::SRP))].flag &&
                                 fk.position(Call::SRP) < fk.position(Call::SEND)))
            << "A3 a settled sink stops SRP before the response (5.5.3.5.39, .45)";
        EXPECT_TRUE(st == ACMP_UNBOUND ||
                    (fk.count(Call::CHANGED) == 1u && fk.position(Call::CHANGED) > fk.position(Call::SEND)))
            << "A3 the change is reported after the response (#653), in state " << st;
        EXPECT_TRUE(!fk.armed[0]) << "A3 and the interface's timer is stopped, in state " << st;
    }
}

// ---- A4: the lock (5.5.2.4, 5.5.2.5) -----------------------------------------------

TEST_F(AcmpCore, A4LockedByAnotherControllerRefusesBindAndUnbind) {
    for (acmp_sink_state st : {ACMP_UNBOUND, ACMP_PRB_W_RESP, ACMP_SETTLED_RSV_OK}) {
        for (std::uint8_t msg : {spec::MSG_BIND_RX_COMMAND, spec::MSG_UNBIND_RX_COMMAND}) {
            SetUp();
            to_state(0, st);
            fk.locked = true;
            fk.holder = kCtl2;
            fk.clear();
            acmp_sink before = a.sinks[0];
            rx(command(msg, 0, kTkB, 3, kCtl1, 0, 0x4400));
            ASSERT_EQ(fk.sent.size(), 1u) << "A4 one response";
            Pdu want;
            want.msg = static_cast<std::uint8_t>(msg + 1u);
            want.status = spec::STATUS_CONTROLLER_NOT_AUTHORIZED;
            want.controller = kCtl1;
            want.talker = kTkB;
            want.listener = kOwn;
            want.talker_uid = 3;
            want.listener_uid = 0;
            want.seq = 0x4400;
            EXPECT_TRUE(same(last(), want))
                << "A4 CONTROLLER_NOT_AUTHORIZED (16, IEEE 1722.1-2021 Table 8-3), fields echoed (Tables 5.31, 5.35)";
            EXPECT_TRUE(a.sinks[0].state == before.state && a.sinks[0].bound == before.bound &&
                        a.sinks[0].binding.talker_entity_id == before.binding.talker_entity_id &&
                        fk.count(Call::PERSIST) == 0u && fk.count(Call::CHANGED) == 0u && fk.count(Call::SRP) == 0u)
                << "A4 and nothing changes";
        }
    }
    EXPECT_EQ(a.refused_locked, 1u) << "A4 each refusal is counted";
}

TEST_F(AcmpCore, A4TheLockingControllerPassesAndGetRxStateIsNotLocked) {
    fk.locked = true;
    fk.holder = kCtl1;
    bind(0);
    EXPECT_EQ(a.sinks[0].state, ACMP_PRB_W_RESP) << "A4 the locking controller binds";
    fk.holder = kCtl2;
    fk.clear();
    rx(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl1));
    EXPECT_TRUE(last().status == spec::STATUS_SUCCESS && fk.count(Call::LOCKED) == 0u)
        << "A4 GET_RX_STATE asks no lock (5.5.3.5.4)";
}

// ---- A5: re-bind of the same source (step 2 of every bound state's RCV_BIND_RX_CMD) --

TEST_F(AcmpCore, A5RebindTheSameSourceUpdatesAndExits) {
    for (acmp_sink_state st : kStates) {
        if (st == ACMP_UNBOUND) {
            continue;
        }
        SetUp();
        to_state(0, st);
        acmp_sink before = a.sinks[0];
        std::uint16_t seq = a.sequence_id;
        fk.clear();
        rx(command(spec::MSG_BIND_RX_COMMAND, 0, kTkA, 1, kCtl2, spec::FLAG_STREAMING_WAIT, 0x4500));
        ASSERT_EQ(fk.sent.size(), 1u) << "A5 a re-bind of the same source sends the response alone, state " << st;
        EXPECT_TRUE(last().msg == spec::MSG_BIND_RX_RESPONSE && last().status == spec::STATUS_SUCCESS &&
                    last().count == 1u && last().flags == spec::FLAG_STREAMING_WAIT)
            << "A5 Table 5.32";
        const acmp_sink& s = a.sinks[0];
        EXPECT_TRUE(s.binding.controller_entity_id == kCtl2 && s.binding.streaming_wait && !s.started)
            << "A5 the controller and STREAMING_WAIT are updated, state " << st;
        EXPECT_TRUE(s.state == before.state && s.timer == before.timer && s.timer_deadline == before.timer_deadline &&
                    s.disc_running == before.disc_running && s.discovered == before.discovered &&
                    a.sequence_id == seq && fk.count(Call::SRP) == 0u)
            << "A5 and nothing else moves: no probe, no timer, discovery kept, state " << st;
        EXPECT_EQ(fk.count(Call::PERSIST), 1u) << "A5 the updated binding is saved, state " << st;
    }
}

// ---- A6: BIND_RX of another source in every bound state ------------------------------

TEST_F(AcmpCore, A6BindAnotherSourceRestartsTheSink) {
    for (acmp_sink_state st : kStates) {
        if (st == ACMP_UNBOUND) {
            continue;
        }
        SetUp();
        to_state(0, st);
        std::uint16_t seq = a.sequence_id;
        fk.clear();
        rx(command(spec::MSG_BIND_RX_COMMAND, 0, kTkB, 2, kCtl2, 0, 0x4600));
        ASSERT_EQ(fk.sent.size(), 2u) << "A6 response then probe, state " << st;
        Pdu p = read(fk.sent[1].bytes.data());
        EXPECT_TRUE(read(fk.sent[0].bytes.data()).msg == spec::MSG_BIND_RX_RESPONSE &&
                    p.msg == spec::MSG_PROBE_TX_COMMAND && p.talker == kTkB && p.talker_uid == 2u &&
                    p.controller == kCtl2 && p.seq == seq)
            << "A6 the new probe names the new source with the next sequence_id, state " << st;
        const acmp_sink& s = a.sinks[0];
        EXPECT_TRUE(s.state == ACMP_PRB_W_RESP && s.timer == ACMP_TIMER_NO_RESP && s.disc_running && !s.discovered &&
                    !s.adp_armed && s.probing == ACMP_PROBING_ACTIVE && s.acmp_status == 0u)
            << "A6 PRB_W_RESP, discovery restarted not discovered, TMR_NO_RESP, state " << st;
        bool settled = st == ACMP_SETTLED_NO_RSV || st == ACMP_SETTLED_RSV_OK;
        EXPECT_TRUE(settled ? (fk.count(Call::SRP) == 1u && !fk.calls[unsigned(fk.position(Call::SRP))].flag &&
                               view(0).stream.stream_id == 0u)
                            : fk.count(Call::SRP) == 0u)
            << "A6 SRP is stopped and its parameters cleared only when settled (5.5.3.5.37, .43), state " << st;
        EXPECT_EQ(fk.count(Call::PERSIST), 1u) << "A6 the new binding is saved, state " << st;
    }
}

TEST_F(AcmpCore, A6TheSameTalkerAnotherSourceIsANewBinding) {
    bind(0, kTkA, 1);
    fk.clear();
    rx(command(spec::MSG_BIND_RX_COMMAND, 0, kTkA, 2, kCtl1));
    ASSERT_EQ(fk.sent.size(), 2u) << "A6 the same talker with another talker_unique_id is a new source: a new probe";
    EXPECT_TRUE(a.sinks[0].binding.talker_unique_id == 2u && read(fk.sent[1].bytes.data()).talker_uid == 2u)
        << "A6 the binding and the probe name the new source (step 2 compares both fields)";
}

// ---- A7: probe responses route on the consumer's unique ID (5.5.3.1, 5.5.3.5.18) ----

TEST_F(AcmpCore, A7ResponsesKeyOnTheListenerUniqueId) {
    bind(0, kTkA, 1);
    bind(1, kTkA, 1);
    Pdu to1 = probe_answer(1);
    rx(to1);
    EXPECT_TRUE(a.sinks[1].state == ACMP_SETTLED_NO_RSV && a.sinks[0].state == ACMP_PRB_W_RESP)
        << "A7 the response belongs to the sink its listener_unique_id names, not to every sink probing that source";
    rx(probe_answer(0));
    EXPECT_EQ(a.sinks[0].state, ACMP_SETTLED_NO_RSV) << "A7 and sink 0 settles on its own response";
}

TEST_F(AcmpCore, A7EachGuardTermIsChecked) {
    bind(0);
    Pdu good = probe_answer(0);
    Pdu bad = good;
    bad.controller = kCtl2;
    rx(bad);
    bad = good;
    bad.talker = kTkB;
    rx(bad);
    bad = good;
    bad.talker_uid = 9;
    rx(bad);
    bad = good;
    bad.seq = static_cast<std::uint16_t>(good.seq + 1u);
    rx(bad);
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_RESP && a.probe_mismatch == 4u)
        << "A7 a response with another controller, talker, talker_unique_id or sequence_id is ignored (5.5.3.5.18 step 1)";
    rx(good);
    EXPECT_EQ(a.sinks[0].state, ACMP_SETTLED_NO_RSV) << "A7 and the right one settles, so no guard refuses everything";
}

TEST_F(AcmpCore, A7TheGuardReadsTheSentProbeNotTheBinding) {
    bind(0, kTkA, 1, kCtl1);
    Pdu answer = probe_answer(0);
    rx(command(spec::MSG_BIND_RX_COMMAND, 0, kTkA, 1, kCtl2));   // the same source: the controller updated
    ASSERT_EQ(a.sinks[0].binding.controller_entity_id, kCtl2);
    rx(answer);
    EXPECT_EQ(a.sinks[0].state, ACMP_SETTLED_NO_RSV)
        << "A7 the answer to the probe sent before a re-bind still matches the probe that was sent";
}

TEST_F(AcmpCore, A7ResponsesOutsideProbingAreIgnored) {
    for (acmp_sink_state st : kStates) {
        if (st == ACMP_PRB_W_RESP || st == ACMP_PRB_W_RESP2) {
            continue;
        }
        SetUp();
        to_state(0, st);
        acmp_sink before = a.sinks[0];
        fk.clear();
        Pdu r = probe_answer(0);
        rx(r);
        EXPECT_TRUE(a.sinks[0].state == before.state && fk.calls.empty())
            << "A7 RCV_PROBE_TX_RESP is ignored outside PRB_W_RESP and PRB_W_RESP2 (Table 5.30 -), state " << st;
    }
    SetUp();
    Pdu r = probe_answer(0);
    r.listener_uid = static_cast<std::uint16_t>(cfg.n_sinks);
    rx(r);
    EXPECT_TRUE(fk.sent.empty() && a.unknown_sink == 1u)
        << "A7 a probe response for a sink the entity lacks is ignored, never answered (5.5.3.1)";
}

// ---- A8, A9: the probe answered (5.5.3.5.18, 5.5.3.5.25) --------------------------------

TEST_F(AcmpCore, A8SuccessSettles) {
    for (acmp_sink_state st : {ACMP_PRB_W_RESP, ACMP_PRB_W_RESP2}) {
        SetUp();
        to_state(0, st);
        fk.clear();
        Pdu r = probe_answer(0);
        r.vlan = 0x1002;                                 // kept exactly, all 16 bits (Milan v1.2 5.3.8.9)
        rx(r);
        const acmp_sink& s = a.sinks[0];
        EXPECT_TRUE(s.state == ACMP_SETTLED_NO_RSV && s.probing == ACMP_PROBING_COMPLETED && s.acmp_status == 0u)
            << "A8 SUCCESS: SETTLED_NO_RSV, PROBING_COMPLETED, state " << st;
        EXPECT_TRUE(s.timer == ACMP_TIMER_NO_TK && s.timer_deadline == fk.now + spec::TMR_NO_TK_MS)
            << "A8 TMR_NO_RESP stopped and TMR_NO_TK 10 s started";
        ASSERT_EQ(fk.count(Call::SRP), 1u) << "A8 SRP is started";
        const Call& c = fk.calls[unsigned(fk.position(Call::SRP))];
        EXPECT_TRUE(c.flag && c.stream.stream_id == kSid && c.stream.dest_mac == kDa && c.stream.vlan_id == 0x1002u)
            << "A8 with the response's stream_id, stream_dest_mac and stream_vlan_id exactly";
        EXPECT_TRUE(view(0).settled && view(0).stream.vlan_id == 0x1002u) << "A8 and the view holds them";
        EXPECT_TRUE(fk.sent.empty()) << "A8 a response is not answered";
    }
}

TEST_F(AcmpCore, A9FailureWaitsForTheRetry) {
    for (acmp_sink_state st : {ACMP_PRB_W_RESP, ACMP_PRB_W_RESP2}) {
        SetUp();
        to_state(0, st);
        rx(probe_answer(0, spec::STATUS_TALKER_DEST_MAC_FAIL));
        const acmp_sink& s = a.sinks[0];
        EXPECT_TRUE(s.state == ACMP_PRB_W_RETRY && s.acmp_status == spec::STATUS_TALKER_DEST_MAC_FAIL &&
                    s.probing == ACMP_PROBING_ACTIVE)
            << "A9 a failed response: PRB_W_RETRY, the ACMP status is its status (5.5.3.5.18 step 3), state " << st;
        EXPECT_TRUE(s.timer == ACMP_TIMER_RETRY && s.timer_deadline == fk.now + spec::TMR_RETRY_MS)
            << "A9 and TMR_RETRY 4 s";
    }
}

// ---- A10 to A13: the timers --------------------------------------------------------------

TEST_F(AcmpCore, A10NoResponseSendsTheDuplicateThenGivesUp) {
    bind(0);
    auto first = fk.sent.back();
    std::uint16_t seq = a.sequence_id;
    fk.clear();
    fire(0);
    ASSERT_EQ(fk.sent.size(), 1u) << "A10 the first TMR_NO_RESP sends one frame";
    EXPECT_TRUE(fk.sent[0].bytes == first.bytes && fk.sent[0].interface == first.interface && a.sequence_id == seq)
        << "A10 an exact duplicate of the first probe, same sequence_id (5.5.3.5.16)";
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_RESP2 && a.sinks[0].probe_retried &&
                a.sinks[0].timer == ACMP_TIMER_NO_RESP && a.sinks[0].timer_deadline == fk.now + spec::TMR_NO_RESP_MS)
        << "A10 PRB_W_RESP2 with TMR_NO_RESP 200 ms";
    fk.clear();
    fire(0);
    EXPECT_TRUE(fk.sent.empty() && a.sinks[0].state == ACMP_PRB_W_RETRY &&
                a.sinks[0].acmp_status == spec::STATUS_LISTENER_TALKER_TIMEOUT &&
                a.sinks[0].timer == ACMP_TIMER_RETRY && a.sinks[0].timer_deadline == fk.now + spec::TMR_RETRY_MS)
        << "A10 the second: no frame, LISTENER_TALKER_TIMEOUT, TMR_RETRY 4 s (5.5.3.5.23)";
}

TEST_F(AcmpCore, A11RetryWaitsForTheTalkerOrDelays) {
    to_state(0, ACMP_PRB_W_RETRY);
    fire(0);
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_AVAIL && a.sinks[0].probing == ACMP_PROBING_PASSIVE &&
                a.sinks[0].acmp_status == 0u && a.sinks[0].timer == ACMP_TIMER_NONE)
        << "A11 TMR_RETRY, talker not discovered: PRB_W_AVAIL, PASSIVE, status 0 (5.5.3.5.30 step 1)";
    SetUp();
    bind(0);
    adp(Adp{});                                          // discovered while probing: noted
    rx(probe_answer(0, spec::STATUS_TALKER_DEST_MAC_FAIL));
    fire(0);
    const acmp_sink& s = a.sinks[0];
    EXPECT_TRUE(s.state == ACMP_PRB_W_DELAY && s.timer == ACMP_TIMER_DELAY &&
                s.timer_deadline - fk.now <= spec::TMR_DELAY_MAX_MS && s.timer_deadline - fk.now == a.last_draw_ms)
        << "A11 TMR_RETRY, talker discovered: TMR_DELAY 0 to 1 s, PRB_W_DELAY (5.5.3.5.30 step 2)";
    EXPECT_TRUE(s.acmp_status == spec::STATUS_TALKER_DEST_MAC_FAIL && s.probing == ACMP_PROBING_ACTIVE)
        << "A11 and the ACMP status stays: step 2 sets none";
}

TEST_F(AcmpCore, A12DelaySendsANewProbe) {
    to_state(0, ACMP_PRB_W_DELAY);
    std::uint16_t seq = a.sequence_id;
    fk.clear();
    fire(0);
    ASSERT_EQ(fk.sent.size(), 1u) << "A12 TMR_DELAY sends the probe (5.5.3.5.10)";
    EXPECT_TRUE(last().msg == spec::MSG_PROBE_TX_COMMAND && last().seq == seq && a.sequence_id == seq + 1u &&
                a.sinks[0].probe_seq == seq)
        << "A12 a new PROBE_TX_COMMAND with the next sequence_id, its copy kept";
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_RESP && a.sinks[0].timer == ACMP_TIMER_NO_RESP &&
                a.sinks[0].timer_deadline == fk.now + spec::TMR_NO_RESP_MS)
        << "A12 PRB_W_RESP, TMR_NO_RESP 200 ms";
}

TEST_F(AcmpCore, A13NoTalkerAttributeReprobes) {
    to_state(0, ACMP_SETTLED_NO_RSV);
    fk.clear();
    fire(0);
    EXPECT_TRUE(fk.count(Call::SRP) == 1u && !fk.calls[unsigned(fk.position(Call::SRP))].flag &&
                view(0).stream.stream_id == 0u)
        << "A13 TMR_NO_TK clears the SRP parameters and stops SRP (5.5.3.5.36 step 1)";
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_AVAIL && a.sinks[0].probing == ACMP_PROBING_PASSIVE)
        << "A13 talker not discovered: PRB_W_AVAIL, PASSIVE (step 2)";
    SetUp();
    bind(0);
    adp(Adp{});
    rx(probe_answer(0));
    rx(probe_answer(0));
    a.sinks[0].acmp_status = 0;
    fire(0);
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_DELAY && a.sinks[0].probing == ACMP_PROBING_ACTIVE &&
                a.sinks[0].acmp_status == 0u && a.sinks[0].timer == ACMP_TIMER_DELAY)
        << "A13 talker discovered: TMR_DELAY, PRB_W_DELAY, ACTIVE, status 0 (step 3)";
}

// ---- A14, A15: the SRP side --------------------------------------------------------------

TEST_F(AcmpCore, A14RegisteredSettlesTheReservation) {
    to_state(0, ACMP_SETTLED_NO_RSV);
    fk.clear();
    acmp_tk_registered(&a, 0, false);
    EXPECT_TRUE(a.sinks[0].state == ACMP_SETTLED_RSV_OK && a.sinks[0].timer == ACMP_TIMER_NONE && !fk.armed[0])
        << "A14 EVT_TK_REGISTERED: TMR_NO_TK cleared, SETTLED_RSV_OK (5.5.3.5.42)";
    EXPECT_TRUE(fk.count(Call::CHANGED) == 1u && view(0).talker_registered && !view(0).registering_failed)
        << "A14 the registration state is a Table 5.22 item: reported";
    for (acmp_sink_state st : kStates) {
        if (st == ACMP_SETTLED_NO_RSV) {
            continue;
        }
        SetUp();
        to_state(0, st);
        acmp_sink before = a.sinks[0];
        acmp_tk_registered(&a, 0, true);
        EXPECT_TRUE(a.sinks[0].state == before.state && a.sinks[0].tk_failed == before.tk_failed &&
                    a.impossible == 1u)
            << "A14 EVT_TK_REGISTERED anywhere else is Table 5.30's x: counted, nothing changes, state " << st;
    }
    acmp_tk_registered(&a, cfg.n_sinks, false);
    EXPECT_EQ(a.impossible, 2u) << "A14 as is one for a sink the entity lacks";
}

TEST_F(AcmpCore, A15UnregisteredReprobes) {
    to_state(0, ACMP_SETTLED_RSV_OK);
    fk.clear();
    acmp_tk_unregistered(&a, 0);
    EXPECT_TRUE(fk.count(Call::SRP) == 1u && !fk.calls[unsigned(fk.position(Call::SRP))].flag &&
                a.sinks[0].state == ACMP_PRB_W_AVAIL && a.sinks[0].probing == ACMP_PROBING_PASSIVE)
        << "A15 EVT_TK_UNREGISTERED, talker not discovered: SRP stopped, PRB_W_AVAIL (5.5.3.5.48 steps 1, 2)";
    SetUp();
    bind(0);
    adp(Adp{});
    rx(probe_answer(0));
    acmp_tk_registered(&a, 0, false);
    acmp_tk_unregistered(&a, 0);
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_DELAY && a.sinks[0].probing == ACMP_PROBING_ACTIVE &&
                a.sinks[0].timer == ACMP_TIMER_DELAY)
        << "A15 talker discovered: TMR_DELAY, PRB_W_DELAY (step 3)";
    for (acmp_sink_state st : kStates) {
        if (st == ACMP_SETTLED_RSV_OK) {
            continue;
        }
        SetUp();
        to_state(0, st);
        acmp_sink before = a.sinks[0];
        fk.clear();
        acmp_tk_unregistered(&a, 0);
        EXPECT_TRUE(a.sinks[0].state == before.state && fk.calls.empty() && a.impossible == 1u)
            << "A15 EVT_TK_UNREGISTERED anywhere else is Table 5.30's x, state " << st;
    }
    acmp_tk_unregistered(&a, cfg.n_sinks);
    EXPECT_EQ(a.impossible, 2u) << "A15 as is one for a sink the entity lacks";
}

// ---- A16: sequence IDs (IEEE 1722.1-2021 8.2.1.15) ----------------------------------------

TEST_F(AcmpCore, A16OneCounterForEveryNewProbe) {
    bind(0);
    bind(1, kTkB, 2);
    EXPECT_TRUE(a.sinks[0].probe_seq == 0u && a.sinks[1].probe_seq == 1u)
        << "A16 each new PROBE_TX_COMMAND takes the next sequence_id, across sinks";
    fire(0);
    EXPECT_EQ(a.sequence_id, 2u) << "A16 a duplicate takes none";
    a.sequence_id = 0xFFFFu;
    bind(2);
    bind(0, kTkB, 3);
    EXPECT_TRUE(a.sinks[2].probe_seq == 0xFFFFu && a.sinks[0].probe_seq == 0u) << "A16 the counter wraps at 2^16";
}

// ---- A17, A18: one timer per interface, the earliest deadline -------------------------------

TEST_F(AcmpCore, A17EachInterfaceTimerHoldsItsEarliestDeadline) {
    bind(0);                                             // TMR_NO_RESP at now + 200 on interface 0
    bind(2);                                             // the same deadline on interface 1
    fk.now += 50;
    bind(1, kTkB, 2);                                    // at now + 200, 50 ms later
    EXPECT_TRUE(fk.armed[0] && fk.at[0] == a.sinks[0].timer_deadline && fk.armed[1] &&
                fk.at[1] == a.sinks[2].timer_deadline)
        << "A17 each interface's timer is armed at the earliest deadline of its own sinks";
    fk.clear();
    fire(0);
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_RESP2 && a.sinks[1].state == ACMP_PRB_W_RESP &&
                a.sinks[2].state == ACMP_PRB_W_RESP && fk.sent.size() == 1u)
        << "A17 an expiry takes the due timers only, of its own interface's sinks";
    EXPECT_TRUE(fk.armed[0] && fk.at[0] == a.sinks[1].timer_deadline) << "A17 and re-arms at the next deadline";
    EXPECT_EQ(fk.count(Call::TIMER), 1u) << "A17 the port is called only when the earliest deadline moves";
    fk.clear();
    rx(command(spec::MSG_UNBIND_RX_COMMAND, 2, kTkA, 1, kCtl1), 1);
    EXPECT_TRUE(!fk.armed[1] && fk.count(Call::TIMER) == 1u && fk.calls[unsigned(fk.position(Call::TIMER))].index == 1u)
        << "A17 an interface whose sinks hold no deadline has its timer stopped";
    fk.clear();
    acmp_timer_expired(&a, 0);
    EXPECT_TRUE(fk.sent.empty() && a.sinks[1].state == ACMP_PRB_W_RESP && fk.armed[0] && fk.count(Call::TIMER) == 1u)
        << "A17 an expiry with nothing due changes nothing and re-arms the timer it consumed";
    acmp_timer_expired(&a, cfg.n_interfaces);
    EXPECT_EQ(a.impossible, 1u) << "A17 an expiry of an interface the entity lacks is counted";
}

TEST_F(AcmpCore, A18AZeroDelayProbesInTheSameExpiry) {
    bind(0);
    adp(Adp{});
    rx(probe_answer(0, 5u));
    a.rng = state_drawing(spec::TMR_DELAY_MAX_MS);
    a.seeded = true;
    fire(0);
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_DELAY && a.last_draw_ms == spec::TMR_DELAY_MAX_MS &&
                a.sinks[0].timer_deadline == fk.now + spec::TMR_DELAY_MAX_MS)
        << "A18 the longest draw is 1000 ms (Table 5.29)";
    SetUp();
    bind(0);
    adp(Adp{});
    rx(probe_answer(0, 5u));
    a.rng = state_drawing(0);
    a.seeded = true;
    fk.clear();
    fire(0);
    EXPECT_TRUE(a.last_draw_ms == 0u && a.sinks[0].state == ACMP_PRB_W_RESP && fk.sent.size() == 1u &&
                last().msg == spec::MSG_PROBE_TX_COMMAND)
        << "A18 TMR_RETRY drawing 0 ms sends its probe in the same expiry";
}

TEST_F(AcmpCore, A18TheSeedIsTakenAtTheFirstDraw) {
    to_state(0, ACMP_PRB_W_DELAY);
    EXPECT_EQ(fk.count(Call::SEED), 1u) << "A18 the seed port is read at the first draw";
    fire(0);
    rx(probe_answer(0, 5u));
    fire(0);
    adp(Adp{0, kTkA, 10, 9, kGm0, 0, 0});
    EXPECT_EQ(fk.count(Call::SEED), 1u) << "A18 and never again";
    SetUp();
    fk.seed = static_cast<std::uint32_t>(kOwn) ^ static_cast<std::uint32_t>(kOwn >> 32) ^ 0x7F4A7C15u;
    to_state(0, ACMP_PRB_W_DELAY);
    EXPECT_TRUE(a.rng != 0u && a.sinks[0].timer == ACMP_TIMER_DELAY)
        << "A18 a seed that cancels the state to 0 leaves it 1: xorshift never leaves 0";
}

// ---- A20: the talker (5.5.4) ----------------------------------------------------------------

TEST_F(AcmpCore, A20ProbeTxIsAnsweredFromTheSource) {
    Pdu cmd;
    cmd.msg = spec::MSG_PROBE_TX_COMMAND;
    cmd.controller = kCtl1;
    cmd.talker = kOwn;
    cmd.listener = kTkB;
    cmd.talker_uid = 0;
    cmd.listener_uid = 5;
    cmd.seq = 0x1234;
    cmd.flags = 0xFFFFu;                                 // every flag set: only FAST_CONNECT and STREAMING_WAIT echo
    fk.source[0] = acmp_source_state{true, {kSid, kDa, 2u}, true};
    rx(cmd);
    ASSERT_EQ(fk.sent.size(), 1u);
    Pdu want;
    want.msg = spec::MSG_PROBE_TX_RESPONSE;
    want.controller = kCtl1;
    want.talker = kOwn;
    want.listener = kTkB;
    want.listener_uid = 5;
    want.seq = 0x1234;
    want.flags = spec::FLAG_FAST_CONNECT | spec::FLAG_STREAMING_WAIT;
    want.stream_id = kSid;
    want.dest_mac = kDa;
    want.vlan = 2;
    EXPECT_TRUE(same(last(), want))
        << "A20 PROBE_TX_RESPONSE is Table 5.43: cc 0, FAST_CONNECT and STREAMING_WAIT echoed, REGISTERING_FAILED 0";
    fk.source[0].dest_mac_valid = false;
    rx(cmd);
    want.status = spec::STATUS_TALKER_DEST_MAC_FAIL;
    want.flags = 0;
    want.stream_id = 0;
    want.dest_mac = 0;
    want.vlan = 0;
    EXPECT_TRUE(same(last(), want)) << "A20 no destination MAC: TALKER_DEST_MAC_FAILED (Table 5.42)";
    cmd.talker_uid = static_cast<std::uint16_t>(cfg.n_sources);
    rx(cmd);
    want.status = spec::STATUS_TALKER_UNKNOWN_ID;
    want.talker_uid = cmd.talker_uid;
    EXPECT_TRUE(same(last(), want)) << "A20 an unknown source: TALKER_UNKNOWN_ID (Table 5.40)";
    cmd.talker_uid = 1;                                  // source 1 is on interface 1
    rx(cmd, 0);
    want.status = spec::STATUS_INCOMPATIBLE_REQUEST;
    want.talker_uid = 1;
    EXPECT_TRUE(same(last(), want) && fk.sent.back().interface == 0u)
        << "A20 a probe from another interface than the source's: INCOMPATIBLE_REQUEST (5.5.4.1 step 2, Table 5.41)";
    fk.clear();
    rx(cmd, 1);
    EXPECT_TRUE(last().status == spec::STATUS_SUCCESS && fk.sent.back().interface == 1u &&
                last().stream_id == kSid + 1u)
        << "A20 on its own interface source 1 is answered there";
}

TEST_F(AcmpCore, A20DisconnectGetTxStateAndGetTxConnection) {
    Pdu cmd;
    cmd.controller = kCtl1;
    cmd.talker = kOwn;
    cmd.listener = kTkB;
    cmd.talker_uid = 0;
    cmd.listener_uid = 5;
    cmd.seq = 0x99;
    cmd.flags = 0xFFFFu;
    cmd.msg = spec::MSG_DISCONNECT_TX_COMMAND;
    rx(cmd);
    Pdu want;
    want.msg = spec::MSG_DISCONNECT_TX_RESPONSE;
    want.controller = kCtl1;
    want.talker = kOwn;
    want.listener = kTkB;
    want.listener_uid = 5;
    want.seq = 0x99;
    EXPECT_TRUE(same(last(), want)) << "A20 DISCONNECT_TX: SUCCESS, cc 0, flags 0, stream 0 (Table 5.45)";
    cmd.talker_uid = 9;
    rx(cmd);
    want.status = spec::STATUS_TALKER_UNKNOWN_ID;
    want.talker_uid = 9;
    EXPECT_TRUE(same(last(), want)) << "A20 DISCONNECT_TX of an unknown source: TALKER_UNKNOWN_ID (Table 5.44)";
    cmd.msg = spec::MSG_GET_TX_STATE_COMMAND;
    rx(cmd);
    want.msg = spec::MSG_GET_TX_STATE_RESPONSE;
    EXPECT_TRUE(same(last(), want)) << "A20 GET_TX_STATE of an unknown source: TALKER_UNKNOWN_ID (Table 5.46)";
    cmd.talker_uid = 0;
    fk.source[0] = acmp_source_state{true, {kSid, kDa, 2u}, true};
    rx(cmd);
    want.status = spec::STATUS_SUCCESS;
    want.talker_uid = 0;
    want.listener = 0;
    want.listener_uid = 0;
    want.flags = spec::FLAG_REGISTERING_FAILED;
    want.stream_id = kSid;
    want.dest_mac = kDa;
    want.vlan = 2;
    EXPECT_TRUE(same(last(), want))
        << "A20 GET_TX_STATE: listener fields 0, cc 0, REGISTERING_FAILED live, the stream (Table 5.47)";
    fk.source[0] = acmp_source_state{false, {kSid, kDa, 2u}, false};
    rx(cmd);
    want.flags = 0;
    want.dest_mac = 0;
    EXPECT_TRUE(same(last(), want)) << "A20 with no destination MAC held, none is reported";
    cmd.msg = spec::MSG_GET_TX_CONNECTION_COMMAND;
    cmd.talker_uid = 9;
    rx(cmd);
    want = Pdu{};
    want.msg = spec::MSG_GET_TX_CONNECTION_RESPONSE;
    want.status = spec::STATUS_NOT_SUPPORTED;
    want.controller = kCtl1;
    want.talker = kOwn;
    want.listener = kTkB;
    want.talker_uid = 9;
    want.listener_uid = 5;
    want.seq = 0x99;
    EXPECT_TRUE(same(last(), want)) << "A20 GET_TX_CONNECTION: NOT_SUPPORTED, fields echoed (5.5.4.4, Table 5.48)";
    EXPECT_TRUE(fk.count(Call::CHANGED) == 0u && fk.count(Call::PERSIST) == 0u)
        << "A20 the talker keeps no state (5.5.2.7)";
}

// ---- A21: what the core does not take ----------------------------------------------------------

TEST_F(AcmpCore, A21MessagesNotForThisEntityAreIgnored) {
    Pdu p = command(spec::MSG_BIND_RX_COMMAND, 0);
    p.listener = kTkB;
    rx(p);
    Pdu t;
    t.msg = spec::MSG_PROBE_TX_COMMAND;
    t.talker = kTkB;
    t.listener = kOwn;
    rx(t);
    Pdu resp = command(spec::MSG_PROBE_TX_RESPONSE, 0);
    resp.listener = kTkB;
    rx(resp);
    for (std::uint8_t msg : {3, 5, 7, 9, 11, 13, 14, 15}) {
        rx(command(msg, 0));
    }
    EXPECT_TRUE(fk.sent.empty() && fk.calls.empty() && a.rx_ignored == 11u && a.sinks[0].state == ACMP_UNBOUND)
        << "A21 commands for another listener or talker, every response but PROBE_TX_RESPONSE and the reserved "
           "types are ignored (5.5.3.1, 8.2.1.9, 8.2.1.10)";
}

TEST_F(AcmpCore, A21MalformedFramesAreCounted) {
    auto f = acmpdu(command(spec::MSG_BIND_RX_COMMAND, 0));
    acmp_rx(&a, 0, f.data(), spec::FRAME_BYTES - 1u);
    auto g = f;
    g[12] = 0x81;
    acmp_rx(&a, 0, g.data(), g.size());
    g = f;
    g[14] = spec::ADPDU_SUBTYPE;
    acmp_rx(&a, 0, g.data(), g.size());
    acmp_rx(&a, cfg.n_interfaces, f.data(), f.size());
    EXPECT_TRUE(a.rx_malformed == 4u && fk.calls.empty() && a.sinks[0].state == ACMP_UNBOUND)
        << "A21 a frame shorter than the Milan ACMPDU, another EtherType or subtype, or an unknown interface is "
           "counted and not read (5.5.2.2)";
    std::array<std::uint8_t, spec::FRAME_BYTES + 26u> longer{};
    std::memcpy(longer.data(), f.data(), f.size());
    acmp_rx(&a, 0, longer.data(), longer.size());
    EXPECT_EQ(a.sinks[0].state, ACMP_PRB_W_RESP) << "A21 the longer IEEE 1722.1-2021 PDU is accepted (5.5.2.2)";
}


// ---- A19: owed frames, in order, and the response before its notification (#653) ---------

TEST_F(AcmpCore, A19AResponseWithoutRoomIsOwedAndItsChangeWaits) {
    fk.room = false;
    bind(0);
    EXPECT_TRUE(fk.sent.empty() && a.owed_count == 2u && a.deferred_sends == 2u)
        << "A19 no room: the response and the probe are owed, in order";
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_RESP && fk.count(Call::PERSIST) == 1u)
        << "A19 the bind itself takes effect and is saved";
    EXPECT_TRUE(fk.count(Call::CHANGED) == 0u && acmp_change_pending(&a, 0))
        << "A19 but its change is not reported while its response waits (#653)";
    EXPECT_TRUE(acmp_poll(&a) && fk.sent.empty()) << "A19 a poll with no room sends nothing and says a frame is owed";
    fk.room = true;
    fk.clear();
    EXPECT_TRUE(acmp_poll(&a)) << "A19 one frame per poll: the probe is still owed after the response";
    ASSERT_EQ(fk.sent.size(), 1u);
    EXPECT_EQ(last().msg, spec::MSG_BIND_RX_RESPONSE) << "A19 the oldest first: the response";
    EXPECT_TRUE(fk.count(Call::CHANGED) == 1u && fk.position(Call::CHANGED) > fk.position(Call::SEND) &&
                !acmp_change_pending(&a, 0))
        << "A19 the change is reported once its response has left";
    EXPECT_FALSE(acmp_poll(&a)) << "A19 then the probe, and nothing is owed";
    EXPECT_EQ(last().msg, spec::MSG_PROBE_TX_COMMAND) << "A19 the probe left second";
    EXPECT_FALSE(acmp_poll(&a)) << "A19 a poll with nothing owed sends nothing";
}

TEST_F(AcmpCore, A19NothingPassesAnOwedFrame) {
    fk.room = false;
    rx(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, 1));
    fk.room = true;
    rx(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, 2));
    EXPECT_TRUE(fk.sent.empty() && a.owed_count == 2u) << "A19 a response does not pass one already owed";
    static_cast<void>(acmp_poll(&a));
    static_cast<void>(acmp_poll(&a));
    ASSERT_EQ(fk.sent.size(), 2u);
    EXPECT_TRUE(read(fk.sent[0].bytes.data()).seq == 1u && read(fk.sent[1].bytes.data()).seq == 2u)
        << "A19 they leave in the order they were made";
}

TEST_F(AcmpCore, A19AFullQueueDropsTheCommandBeforeItActs) {
    fk.room = false;
    for (unsigned k = 0; k < ACMP_OWED_MAX; ++k) {
        rx(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, static_cast<std::uint16_t>(k)));
    }
    ASSERT_EQ(a.owed_count, ACMP_OWED_MAX);
    fk.clear();
    bind(1);
    Pdu t;
    t.msg = spec::MSG_GET_TX_STATE_COMMAND;
    t.talker = kOwn;
    rx(t);
    EXPECT_TRUE(a.busy_drops == 2u && a.sinks[1].state == ACMP_UNBOUND && fk.calls.empty())
        << "A19 a command whose response would find the queue full is dropped before it changes anything";
}

TEST_F(AcmpCore, A19AProbeWithoutRoomIsLostAndRecovered) {
    to_state(0, ACMP_PRB_W_DELAY);
    fk.room = false;
    for (unsigned k = 0; k < ACMP_OWED_MAX; ++k) {
        rx(command(spec::MSG_GET_RX_STATE_COMMAND, 1, 0, 0, kCtl2));
    }
    fire(0);
    EXPECT_TRUE(a.probes_lost == 1u && a.sinks[0].state == ACMP_PRB_W_RESP && a.sinks[0].timer == ACMP_TIMER_NO_RESP)
        << "A19 a probe the full queue cannot take is lost and counted; TMR_NO_RESP will send its duplicate";
    fk.room = true;
    for (unsigned k = 0; k < ACMP_OWED_MAX; ++k) {
        static_cast<void>(acmp_poll(&a));
    }
    fk.clear();
    fire(0);
    EXPECT_TRUE(fk.sent.size() == 1u && last().msg == spec::MSG_PROBE_TX_COMMAND && last().seq == a.sinks[0].probe_seq)
        << "A19 and it does";
}

TEST_F(AcmpCore, A19TwoOwedResponsesForOneSinkReleaseTogether) {
    fk.room = false;
    bind(0);
    rx(command(spec::MSG_UNBIND_RX_COMMAND, 0));
    fk.room = true;
    fk.clear();
    static_cast<void>(acmp_poll(&a));                    // the bind's response
    static_cast<void>(acmp_poll(&a));                    // its probe
    EXPECT_TRUE(fk.count(Call::CHANGED) == 0u && acmp_change_pending(&a, 0))
        << "A19 the bind's response left but the unbind's is still owed: the sink's change still waits";
    static_cast<void>(acmp_poll(&a));
    EXPECT_TRUE(fk.count(Call::CHANGED) == 0u && !acmp_change_pending(&a, 0))
        << "A19 once the unbind's response leaves nothing is reported: the sink is as it was (unbound)";
}

// ---- A22: the listener's discovery machine (5.6.4, Table 5.54) ---------------------------------

TEST_F(AcmpCore, A22AvailableDiscoversWhenTheGrandmasterMatches) {
    rx(command(spec::MSG_BIND_RX_COMMAND, 0));
    Adp d;
    d.gm = kGm0 + 1u;
    adp(d);
    EXPECT_TRUE(!a.sinks[0].discovered && !a.sinks[0].adp_armed)
        << "A22 TK_NOT_DISCOVERED: an AVAILABLE from another grandmaster is ignored (5.6.4.5.1 step 1)";
    d.gm = kGm0;
    d.domain = 1;
    adp(d);
    EXPECT_FALSE(a.sinks[0].discovered) << "A22 and from another domain";
    for (std::uint8_t vt : {1, 10, 31}) {
        SetUp();
        fk.now = 70000;
        bind(0);
        Adp v;
        v.valid_time = vt;
        v.index = 33;
        v.interface_index = 4;
        adp(v);
        const acmp_sink& s = a.sinks[0];
        EXPECT_TRUE(s.discovered && s.disc_interface_index == 4u && s.disc_available_index == 33u)
            << "A22 a matching AVAILABLE: TK_DISCOVERED, interface_index and available_index saved (5.6.4.5.1)";
        EXPECT_TRUE(s.adp_armed && s.adp_deadline == 70000u + vt * spec::VALID_TIME_UNIT_MS)
            << "A22 TMR_NO_ADP is the received valid_time in two-second units, valid_time " << unsigned(vt);
        EXPECT_TRUE(fk.armed[0] && fk.at[0] == 70000u + spec::TMR_NO_RESP_MS)
            << "A22 and the interface's timer keeps the earlier deadline";
    }
}

TEST_F(AcmpCore, A22DiscoveredStartsTheProbeFromPrbWAvail) {
    std::uint8_t record[spec::BINDING_BYTES] = {0x03, 0, 0, 1};
    wire_put_be(record + 4, kTkA, 8);
    wire_put_be(record + 12, kCtl1, 8);
    ASSERT_EQ(acmp_restore_binding(&a, 0, record, sizeof record), ACMP_RESTORE_APPLIED);
    fk.clear();
    adp(Adp{});
    const acmp_sink& s = a.sinks[0];
    EXPECT_TRUE(s.state == ACMP_PRB_W_DELAY && s.probing == ACMP_PROBING_ACTIVE && s.timer == ACMP_TIMER_DELAY &&
                s.timer_deadline - fk.now <= spec::TMR_DELAY_MAX_MS)
        << "A22 EVT_TK_DISCOVERED in PRB_W_AVAIL: TMR_DELAY 0 to 1 s, PRB_W_DELAY, ACTIVE (5.5.3.5.9)";
    EXPECT_EQ(fk.count(Call::GPTP), 1u) << "A22 the grandmaster is sampled once for the frame";
}

TEST_F(AcmpCore, A22DiscoveredStateCells) {
    // TK_DISCOVERED with the connection machine in PRB_W_RESP, where EVT_TK_DISCOVERED
    // is noted and EVT_TK_DEPARTED goes to PRB_W_AVAIL, so each event shows.
    auto discovered = [this]() {
        SetUp();
        bind(0);
        Adp d;
        d.index = 700;
        d.interface_index = 2;
        adp(d);
        fk.clear();
    };
    discovered();
    Adp d;
    d.index = 701;
    d.interface_index = 3;
    adp(d);
    EXPECT_TRUE(a.sinks[0].disc_available_index == 700u && a.sinks[0].state == ACMP_PRB_W_RESP && fk.calls.empty())
        << "A22 TK_DISCOVERED: an AVAILABLE with another interface_index is ignored (5.6.4.5.2 step 1)";
    discovered();
    d.interface_index = 2;
    d.valid_time = 5;
    fk.now += 1000;
    adp(d);
    EXPECT_TRUE(a.sinks[0].disc_available_index == 701u && a.sinks[0].adp_deadline == fk.now + 5u * 2000u &&
                a.sinks[0].state == ACMP_PRB_W_RESP)
        << "A22 a rising available_index is noted and TMR_NO_ADP restarted, no event (step 3)";
    for (std::uint32_t index : {700u, 699u, 0u}) {
        discovered();
        d.index = index;
        d.valid_time = 10;
        adp(d);
        EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_DELAY && a.sinks[0].discovered &&
                    a.sinks[0].disc_available_index == index && a.sinks[0].adp_deadline == fk.now + 20000u)
            << "A22 available_index " << index << " <= last: EVT_TK_DEPARTED then EVT_TK_DISCOVERED, the index noted "
            << "(5.6.4.5.2 steps 2a, 2c, 3)";
    }
    discovered();
    d.index = 600;
    d.gm = kGm0 + 1u;
    adp(d);
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_AVAIL && !a.sinks[0].discovered && !a.sinks[0].adp_armed &&
                a.sinks[0].disc_available_index == 700u)
        << "A22 index <= last from another grandmaster: EVT_TK_DEPARTED, TMR_NO_ADP stopped, TK_NOT_DISCOVERED (2b)";
    discovered();
    d.gm = kGm0;
    d.domain = 7;
    adp(d);
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_AVAIL && !a.sinks[0].discovered) << "A22 and from another domain";
    discovered();
    d.index = 800;
    d.domain = 7;
    adp(d);
    EXPECT_TRUE(a.sinks[0].discovered && a.sinks[0].disc_available_index == 800u)
        << "A22 a rising index reads no grandmaster: step 2 alone does";
}

TEST_F(AcmpCore, A22DepartingAndAging) {
    bind(0);
    Adp gone;
    gone.msg = spec::ADPDU_ENTITY_DEPARTING;
    adp(gone);
    EXPECT_TRUE(a.sinks[0].state == ACMP_PRB_W_RESP && !a.sinks[0].discovered)
        << "A22 a DEPARTING in TK_NOT_DISCOVERED is ignored (Table 5.54 -)";
    adp(Adp{});
    gone.interface_index = 1;
    adp(gone);
    EXPECT_TRUE(a.sinks[0].discovered && a.sinks[0].adp_armed)
        << "A22 a DEPARTING with another interface_index is ignored (5.6.4.5.3 step 1)";
    gone.interface_index = 0;
    adp(gone);
    EXPECT_TRUE(!a.sinks[0].discovered && !a.sinks[0].adp_armed && a.sinks[0].state == ACMP_PRB_W_AVAIL)
        << "A22 a DEPARTING: TMR_NO_ADP stopped, TK_NOT_DISCOVERED, EVT_TK_DEPARTED (5.6.4.5.3)";
    SetUp();
    bind(0);
    Adp v;
    v.valid_time = 1;
    adp(v);
    fire_adp(0);
    EXPECT_TRUE(!a.sinks[0].discovered && !a.sinks[0].adp_armed && a.sinks[0].state == ACMP_PRB_W_AVAIL)
        << "A22 TMR_NO_ADP: TK_NOT_DISCOVERED and EVT_TK_DEPARTED (5.6.4.5.4)";
}

TEST_F(AcmpCore, A22OnlyBoundSinksOfThatTalkerOnThatInterface) {
    bind(0, kTkA);
    bind(1, kTkA, 2);
    bind(2, kTkA);                                       // interface 1
    fk.clear();
    adp(Adp{});
    EXPECT_TRUE(a.sinks[0].discovered && a.sinks[1].discovered && !a.sinks[2].discovered)
        << "A22 every bound sink of the talker processes it (5.6.4.1), only on the interface it arrived on";
    EXPECT_EQ(fk.count(Call::GPTP), 1u) << "A22 and the grandmaster is sampled once for the frame";
    Adp other;
    other.entity = kTkB;
    std::uint32_t ignored = a.adp_ignored;
    adp(other);
    EXPECT_EQ(a.adp_ignored, ignored + 1u) << "A22 an AVAILABLE no bound sink takes is counted";
    SetUp();
    Adp zero;
    zero.entity = 0;                                     // what an unbound sink's cleared binding names
    adp(zero);
    EXPECT_TRUE(!a.sinks[0].discovered && !a.sinks[0].adp_armed && a.adp_ignored == 1u)
        << "A22 an unbound sink runs no discovery";
}

TEST_F(AcmpCore, A22OtherAdpFramesAreIgnored) {
    bind(0);
    auto f = adpdu(Adp{});
    std::uint32_t n = a.adp_ignored;
    acmp_adp_rx(&a, 0, f.data(), spec::ADPDU_FRAME_BYTES - 1u);
    auto g = f;
    g[15] = 2;                                           // ENTITY_DISCOVER
    acmp_adp_rx(&a, 0, g.data(), g.size());
    g = f;
    g[14] = spec::SUBTYPE;
    acmp_adp_rx(&a, 0, g.data(), g.size());
    g = f;
    g[13] = 0xF1;
    acmp_adp_rx(&a, 0, g.data(), g.size());
    acmp_adp_rx(&a, cfg.n_interfaces, f.data(), f.size());
    EXPECT_TRUE(a.adp_ignored == n + 5u && !a.sinks[0].discovered)
        << "A22 a short ADPDU, a DISCOVER, another subtype or EtherType, or an unknown interface is not discovery's";
}

// ---- A23: the no-callback rule (#678) ------------------------------------------------------------

TEST_F(AcmpCore, A23EveryEntryRefusesACallFromInsideAPort) {
    std::uint8_t record[spec::BINDING_BYTES] = {0x01};
    auto bindf = acmpdu(command(spec::MSG_BIND_RX_COMMAND, 1));
    auto adpf = adpdu(Adp{});
    const std::function<void()> calls[] = {
        [&] { acmp_rx(&a, 0, bindf.data(), bindf.size()); },
        [&] { acmp_adp_rx(&a, 0, adpf.data(), adpf.size()); },
        [&] { acmp_timer_expired(&a, 0); },
        [&] { acmp_tk_registered(&a, 0, false); },
        [&] { acmp_tk_unregistered(&a, 0); },
        [&] { EXPECT_FALSE(acmp_set_started(&a, 0, false)); },
        [&] { static_cast<void>(acmp_poll(&a)); },
        [&] { EXPECT_EQ(acmp_restore_binding(&a, 1, record, sizeof record), ACMP_RESTORE_REFUSED); },
        [&] { acmp_restore_rollback(&a); },
    };
    unsigned n = 0;
    for (const auto& call : calls) {
        SetUp();
        fk.room = false;                                 // the owed queue is not empty: acmp_poll says so
        fk.hook_kind = Call::SEND;
        fk.hook = call;
        bind(0);
        const acmp_sink& s = a.sinks[0];
        EXPECT_TRUE(a.reentries == 1u && reentry_traps == 1u)
            << "A23 a call made from inside the send port is refused, counted and trapped, entry " << n;
        EXPECT_TRUE(s.state == ACMP_PRB_W_RESP && s.timer == ACMP_TIMER_NO_RESP && fk.armed[0] &&
                    a.sinks[1].state == ACMP_UNBOUND && a.owed_count == 2u)
            << "A23 and the outer call completes as if it had not been made: TMR_NO_RESP running, entry " << n;
        n++;
    }
}

TEST_F(AcmpCore, A23EveryPortIsGuarded) {
    const Call::Kind kinds[] = {Call::TIMER, Call::NOW, Call::GPTP, Call::SEED, Call::LOCKED,
                                Call::SOURCE, Call::SRP, Call::PERSIST, Call::CHANGED};
    for (Call::Kind kind : kinds) {
        SetUp();
        fk.locked = true;
        fk.holder = kCtl1;
        fk.hook_kind = kind;
        fk.hook = [this] { acmp_timer_expired(&a, 0); };
        bind(0);                                         // LOCKED, NOW, SEND, TIMER, PERSIST, CHANGED
        Pdu t;
        t.msg = spec::MSG_GET_TX_STATE_COMMAND;
        t.talker = kOwn;
        rx(t);                                           // SOURCE
        adp(Adp{});                                      // GPTP
        rx(probe_answer(0, 5u));
        fire(0);                                         // TMR_RETRY, discovered: the first draw, SEED
        fire(0);
        rx(probe_answer(0));                             // SRP
        rx(command(spec::MSG_UNBIND_RX_COMMAND, 0));
        EXPECT_TRUE(a.reentries == 1u && reentry_traps == 1u) << "A23 the port kind " << kind << " is guarded";
    }
}

// ---- A24: the saved binding record --------------------------------------------------------------

TEST_F(AcmpCore, A24ARestoredBindingFastConnects) {
    std::uint8_t record[spec::BINDING_BYTES] = {0x07, 0xAA, 0x12, 0x34};
    wire_put_be(record + 4, kTkB, 8);
    wire_put_be(record + 12, kCtl2, 8);
    EXPECT_EQ(acmp_restore_binding(&a, 1, record, sizeof record), ACMP_RESTORE_APPLIED) << "A24 a saved binding applies";
    const acmp_sink& s = a.sinks[1];
    EXPECT_TRUE(s.bound && s.started && s.binding.streaming_wait && s.binding.talker_unique_id == 0x1234u &&
                s.binding.talker_entity_id == kTkB && s.binding.controller_entity_id == kCtl2)
        << "A24 the record's flags and parameters, big-endian (the processor's BINDING payload)";
    EXPECT_TRUE(s.state == ACMP_PRB_W_AVAIL && s.probing == ACMP_PROBING_PASSIVE && s.acmp_status == 0u &&
                s.disc_running && !s.discovered && s.timer == ACMP_TIMER_NONE)
        << "A24 startup with a saved binding: discovery started, PROBING_PASSIVE, PRB_W_AVAIL (5.5.3.5.2)";
    EXPECT_TRUE(fk.calls.empty()) << "A24 a boot restore calls no port: nothing to save or report";
    std::uint8_t back[spec::BINDING_BYTES];
    ASSERT_TRUE(acmp_binding_latch(&a, 1, back));
    record[1] = 0;                                       // the reserved byte is saved 0
    EXPECT_EQ(std::memcmp(back, record, sizeof back), 0) << "A24 the latch gives the same record back";
}

TEST_F(AcmpCore, A24UnboundRecordsRefusalsAndRollback) {
    std::uint8_t record[spec::BINDING_BYTES] = {0x06, 0, 0, 1};
    EXPECT_EQ(acmp_restore_binding(&a, 0, record, sizeof record), ACMP_RESTORE_APPLIED)
        << "A24 a record without the valid flag applies";
    EXPECT_TRUE(a.sinks[0].state == ACMP_UNBOUND && !a.sinks[0].bound) << "A24 and leaves the sink unbound (5.5.3.5.1)";
    record[0] = 0x01;
    EXPECT_EQ(acmp_restore_binding(&a, cfg.n_sinks, record, sizeof record), ACMP_RESTORE_REFUSED)
        << "A24 a record of a sink the configuration lacks is refused";
    EXPECT_EQ(acmp_restore_binding(&a, 0, record, sizeof record - 1u), ACMP_RESTORE_REFUSED)
        << "A24 a payload of another length is refused";
    ASSERT_EQ(acmp_restore_binding(&a, 0, record, sizeof record), ACMP_RESTORE_APPLIED);
    ASSERT_EQ(acmp_restore_binding(&a, 2, record, sizeof record), ACMP_RESTORE_APPLIED);
    acmp_restore_rollback(&a);
    EXPECT_TRUE(!a.sinks[0].bound && !a.sinks[2].bound && a.sinks[0].state == ACMP_UNBOUND && !a.sinks[2].disc_running &&
                a.sinks[2].interface == 1u && fk.calls.empty())
        << "A24 the roll-back drops every restored binding, keeps each sink's interface, calls no port";
    std::uint8_t back[spec::BINDING_BYTES];
    std::memset(back, 0xEE, sizeof back);
    ASSERT_TRUE(acmp_binding_latch(&a, 0, back));
    EXPECT_TRUE(std::all_of(back, back + sizeof back, [](std::uint8_t b) { return b == 0u; }))
        << "A24 an unbound sink's record is all zeros: how an unbind is saved";
    EXPECT_FALSE(acmp_binding_latch(&a, cfg.n_sinks, back)) << "A24 there is no record of a sink the entity lacks";
}

TEST_F(AcmpCore, A24StartedIsSavedAndReported) {
    EXPECT_FALSE(acmp_set_started(&a, 0, true)) << "A24 an unbound sink has no started state (5.3.8.7)";
    EXPECT_FALSE(acmp_set_started(&a, cfg.n_sinks, true)) << "A24 nor a sink the entity lacks";
    bind(0, kTkA, 1, kCtl1, true);
    fk.clear();
    EXPECT_TRUE(acmp_set_started(&a, 0, true)) << "A24 START_STREAMING of a bound sink";
    EXPECT_TRUE(a.sinks[0].started && fk.count(Call::PERSIST) == 1u && fk.count(Call::CHANGED) == 1u)
        << "A24 the started state is saved (5.3.8.7) and is a Table 5.22 item";
    fk.clear();
    EXPECT_TRUE(acmp_set_started(&a, 0, true));
    EXPECT_TRUE(fk.calls.empty()) << "A24 setting it again changes nothing";
}

// ---- A25: the notification follows Table 5.22's items ---------------------------------------------

TEST_F(AcmpCore, A25OnlyTable522ItemsAreReported) {
    to_state(0, ACMP_SETTLED_NO_RSV);
    fk.clear();
    adp(Adp{});
    EXPECT_EQ(fk.count(Call::CHANGED), 0u) << "A25 discovery noted while settled moves no Table 5.22 item";
    SetUp();
    bind(0);
    fk.clear();
    fire(0);
    EXPECT_EQ(fk.count(Call::CHANGED), 0u) << "A25 the duplicate probe moves none: still PROBING_ACTIVE, status 0";
    fire(0);
    EXPECT_EQ(fk.count(Call::CHANGED), 1u) << "A25 the ACMP status LISTENER_TALKER_TIMEOUT does";
    fk.clear();
    rx(command(spec::MSG_BIND_RX_COMMAND, 0, kTkA, 1, kCtl1));
    EXPECT_TRUE(fk.count(Call::CHANGED) == 0u && fk.count(Call::PERSIST) == 0u)
        << "A25 a re-bind that changes nothing reports and saves nothing";
}

}  // namespace
