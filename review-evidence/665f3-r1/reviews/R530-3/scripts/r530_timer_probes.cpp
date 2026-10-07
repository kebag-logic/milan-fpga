// [R530] R530-3 reviewer probes: TMR_NO_RESP from the clock after each accepted probe send,
// on paths the round's own A30 tests do not exercise with a moving clock.
#include <gtest/gtest.h>
#include "acmp_fake.hpp"
#include "fw_gtest.hpp"
using namespace acmp_test;
FW_TALLY_LABEL("R530-3 moving-clock TMR_NO_RESP probes");
namespace {
struct Rig {
    acmp a{}; acmp_config cfg{};
    explicit Rig(unsigned sinks = 1, std::uint32_t t0 = 1000u) {
        fk = Fake{}; fk.now = t0;
        cfg.entity_id = kOwn; cfg.n_interfaces = 1; cfg.n_sinks = sinks; cfg.mac[0] = kMac0;
        EXPECT_TRUE(acmp_init(&a, &cfg, &kPorts, &kEnv));
    }
    void cmd(std::uint8_t msg, unsigned sink, std::uint64_t talker, std::uint16_t seq = 0) {
        Pdu c{}; c.msg = msg; c.controller = kCtl1; c.talker = talker; c.listener = kOwn;
        c.talker_uid = 1; c.listener_uid = static_cast<std::uint16_t>(sink); c.seq = seq;
        auto f = acmpdu(c); acmp_rx(&a, 0, f.data(), f.size());
    }
    void bind(unsigned sink, std::uint64_t talker = kTkA) { cmd(spec::MSG_BIND_RX_COMMAND, sink, talker); }
    void answer(unsigned sink) {
        const auto& s = a.sinks[sink];
        Pdu r{}; r.msg = spec::MSG_PROBE_TX_RESPONSE; r.controller = s.probe_controller; r.talker = s.probe_talker;
        r.listener = kOwn; r.talker_uid = s.probe_talker_uid; r.listener_uid = static_cast<std::uint16_t>(sink);
        r.seq = s.probe_seq; r.stream_id = kSid; r.dest_mac = kDa; r.vlan = 2;
        auto f = acmpdu(r); acmp_rx(&a, 0, f.data(), f.size());
    }
    std::uint32_t last_probe_at() const {
        for (auto it = fk.sent.rbegin(); it != fk.sent.rend(); ++it) {
            if ((it->bytes[15] & 15u) == spec::MSG_PROBE_TX_COMMAND) return it->at;
        }
        ADD_FAILURE() << "no probe sent"; return 0;
    }
};

// P1: the duplicate waits for room, then leaves 50 ms later with a 5 ms send: 200 ms from after that send.
TEST(R530Timers, OwedDuplicateRunsFromThePollsSend) {
    Rig r; r.bind(0); ASSERT_EQ(r.a.sinks[0].timer_deadline, 1200u);
    fk.now = 1200u; fk.room = false; acmp_timer_expired(&r.a, 0);
    ASSERT_EQ(r.a.sinks[0].state, ACMP_PRB_W_RESP2);
    EXPECT_TRUE(r.a.sinks[0].timer_held) << "duplicate owed: its TMR_NO_RESP held";
    fk.now = 1250u; fk.room = true; fk.send_ms = 5u; fk.clear();
    (void)acmp_poll(&r.a);
    ASSERT_EQ(fk.sent.size(), 1u);
    const std::uint32_t at = fk.sent[0].at; ASSERT_EQ(at, 1255u);
    EXPECT_EQ(r.a.sinks[0].timer_deadline, at + 200u);
    EXPECT_FALSE(r.a.sinks[0].timer_held);
    fk.now = at + 199u; acmp_timer_expired(&r.a, 0);
    EXPECT_EQ(r.a.sinks[0].state, ACMP_PRB_W_RESP2) << "199 ms after the owed duplicate left is no timeout";
    r.answer(0);
    EXPECT_EQ(r.a.sinks[0].state, ACMP_SETTLED_NO_RSV) << "a success at 199 ms settles";
}
TEST(R530Timers, OwedDuplicateTimesOutAtTheFullInterval) {
    Rig r; r.bind(0);
    fk.now = 1200u; fk.room = false; acmp_timer_expired(&r.a, 0);
    fk.now = 1250u; fk.room = true; fk.send_ms = 5u; (void)acmp_poll(&r.a);
    fk.send_ms = 0u; fk.clear(); fk.now = 1455u; acmp_timer_expired(&r.a, 0);
    EXPECT_EQ(r.a.sinks[0].state, ACMP_PRB_W_RETRY);
    EXPECT_EQ(r.a.sinks[0].acmp_status, spec::STATUS_LISTENER_TALKER_TIMEOUT);
    EXPECT_TRUE(fk.sent.empty()) << "no third probe";
}
// P2: two sinks whose duplicates both leave in one expiry: each from its own send.
TEST(R530Timers, TwoDuplicatesInOneExpiryEachFromItsOwnSend) {
    Rig r(2); r.bind(0, kTkA); r.bind(1, kTkB);
    ASSERT_EQ(r.a.sinks[0].timer_deadline, 1200u); ASSERT_EQ(r.a.sinks[1].timer_deadline, 1200u);
    const std::uint16_t s0 = r.a.sinks[0].probe_seq, s1 = r.a.sinks[1].probe_seq;
    EXPECT_NE(s0, s1);
    fk.now = 1200u; fk.send_ms = 5u; fk.clear(); acmp_timer_expired(&r.a, 0);
    ASSERT_EQ(fk.sent.size(), 2u);
    EXPECT_EQ(read(fk.sent[0].bytes.data()).seq, s0); EXPECT_EQ(read(fk.sent[1].bytes.data()).seq, s1);
    EXPECT_EQ(r.a.sinks[0].timer_deadline, fk.sent[0].at + 200u);
    EXPECT_EQ(r.a.sinks[1].timer_deadline, fk.sent[1].at + 200u);
    EXPECT_EQ(fk.sent[1].at, 1210u);
    EXPECT_TRUE(fk.armed[0] && fk.at[0] == fk.sent[0].at + 200u) << "the interface timer at the earliest";
}
// P3: the send carries the clock across the 32-bit wrap.
TEST(R530Timers, SendAcrossTheWrap) {
    Rig r(1, 0xFFFFFFF0u); fk.send_ms = 10u; r.bind(0);
    const std::uint32_t at = r.last_probe_at();
    ASSERT_EQ(at, 0x4u);
    EXPECT_EQ(r.a.sinks[0].timer_deadline, at + 200u);
    fk.send_ms = 0u; fk.now = at + 199u; acmp_timer_expired(&r.a, 0);
    EXPECT_EQ(r.a.sinks[0].state, ACMP_PRB_W_RESP);
    fk.now = at + 200u; acmp_timer_expired(&r.a, 0);
    EXPECT_EQ(r.a.sinks[0].state, ACMP_PRB_W_RESP2);
}
// P4: the lost-probe policy: no send, TMR_NO_RESP from the attempt, counted.
TEST(R530Timers, LostProbeRunsFromTheAttempt) {
    Rig r; fk.room = false;
    for (int i = 0; i < 7; ++i) r.cmd(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, static_cast<std::uint16_t>(i));
    ASSERT_EQ(r.a.owed_count, 7u);
    fk.now = 3000u; r.bind(0);
    EXPECT_EQ(r.a.owed_count, 8u);
    EXPECT_EQ(r.a.probes_lost, 1u);
    EXPECT_FALSE(r.a.sinks[0].timer_held);
    EXPECT_EQ(r.a.sinks[0].timer, ACMP_TIMER_NO_RESP);
    EXPECT_EQ(r.a.sinks[0].timer_deadline, 3200u) << "lost: from the attempt";
    fk.room = true; fk.send_ms = 5u; for (int i = 0; i < 8; ++i) (void)acmp_poll(&r.a);
    EXPECT_EQ(r.a.sinks[0].timer_deadline, 3200u) << "nothing that leaves restarts a lost probe's timer";
    fk.send_ms = 0u; fk.now = 3200u; fk.clear(); acmp_timer_expired(&r.a, 0);
    EXPECT_EQ(r.a.sinks[0].state, ACMP_PRB_W_RESP2) << "the duplicate recovers it";
    ASSERT_EQ(fk.sent.size(), 1u);
}
// P5: re-bound while the first probe is owed: only the current probe's send starts the timer.
TEST(R530Timers, RebindWhileOwedStartsOnlyOnTheCurrentProbe) {
    Rig r; fk.room = false; r.bind(0, kTkA);
    const std::uint16_t first = r.a.sinks[0].probe_seq;
    r.bind(0, kTkB);
    const std::uint16_t second = r.a.sinks[0].probe_seq;
    ASSERT_NE(first, second);
    fk.room = true; fk.send_ms = 5u;
    std::uint32_t current_at = 0;
    while (r.a.owed_count) {
        (void)acmp_poll(&r.a);
        const auto& f = fk.sent.back();
        const Pdu p = read(f.bytes.data());
        if (p.msg == spec::MSG_PROBE_TX_COMMAND && p.seq == first) {
            EXPECT_TRUE(r.a.sinks[0].timer_held) << "the superseded probe leaving starts nothing";
        }
        if (p.msg == spec::MSG_PROBE_TX_COMMAND && p.seq == second) current_at = f.at;
    }
    ASSERT_NE(current_at, 0u);
    EXPECT_EQ(r.a.sinks[0].timer_deadline, current_at + 200u);
    EXPECT_FALSE(r.a.sinks[0].timer_held);
}
// P6: unbound while owed: the probe leaving afterwards starts no timer.
TEST(R530Timers, UnbindWhileOwedLeavesNoTimer) {
    Rig r; fk.room = false; r.bind(0);
    r.cmd(spec::MSG_UNBIND_RX_COMMAND, 0, kTkA);
    EXPECT_EQ(r.a.sinks[0].state, ACMP_UNBOUND);
    fk.room = true; fk.send_ms = 5u; while (r.a.owed_count) (void)acmp_poll(&r.a);
    EXPECT_EQ(r.a.sinks[0].timer, ACMP_TIMER_NONE);
    EXPECT_FALSE(fk.armed[0]) << "no interface timer";
}
}  // namespace
