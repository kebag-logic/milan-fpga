// SPDX-License-Identifier: MIT
// Reviewer probe (disposable): inserted inside the anonymous test namespace of a copy of tests/test_acmp.cpp,
// after the AcmpOwed tests. It measures, in 1 ms passes after the egress returns, when a kept command is
// answered while other sinks' TMR_NO_RESP probes come due during the release. The port model is the
// committed AcmpOwed one: poll, deliver kept frames, then service due timers.
struct ProbeResult {
    unsigned answer_pass;
    unsigned position;
    unsigned probes_lost;
    unsigned busy_declined;
};
class AcmpOwedProbe : public AcmpOwed {
 protected:
    // Self-contained copy of the head's port model, so the probe runs unchanged at earlier revisions:
    // poll once, deliver kept frames in order until one is declined, then service due timers.
    void probe_pass() {
        fk.now += 1u;
        static_cast<void>(acmp_poll(&a));
        while (!held.empty() &&
               acmp_rx(&a, held.front().interface, held.front().bytes.data(), held.front().bytes.size())) {
            held.erase(held.begin());
        }
        for (unsigned i = 0; i < cfg.n_interfaces; ++i) {
            if (fk.armed[i] && static_cast<std::int32_t>(fk.now - fk.at[i]) >= 0) {
                acmp_timer_expired(&a, i);
            }
        }
    }
    void probe_drain() {
        for (unsigned n = 0; n < 4u * ACMP_OWED_MAX && (a.owed_count != 0u || !held.empty()); ++n) {
            probe_pass();
        }
    }
    // timed_sinks: sinks bound before the fill whose TMR_NO_RESP falls due in passes 1, 2, ... after release.
    ProbeResult run(std::uint8_t kept_msg, std::initializer_list<unsigned> timed_sinks) {
        const std::uint32_t t0 = fk.now;
        unsigned step = 0;
        for (unsigned k : timed_sinks) {
            fk.now = t0 + step++;
            bind(k);
        }
        fk.now = t0 + step;
        fill(0x7a00);
        fk.clear();
        Pdu kept = command(kept_msg, 1, kTkA, 1, kCtl1, 0, 0x7a08);
        EXPECT_FALSE(deliver(kept)) << "probe: the kept command is declined behind the full set";
        const std::uint32_t release = t0 + spec::TMR_NO_RESP_MS - 1u;   // first timer due in pass 1
        fk.now = release;
        fk.room = true;
        probe_drain();
        const std::uint8_t resp = kept_msg == spec::MSG_BIND_RX_COMMAND ? spec::MSG_BIND_RX_RESPONSE
                                                                         : spec::MSG_GET_RX_STATE_RESPONSE;
        const Sent* s = answer(resp, 0x7a08);
        EXPECT_TRUE(s != nullptr) << "probe: the kept command is answered";
        if (s == nullptr) {
            return {0u, 0u, 0u, 0u};
        }
        return {s->at - release, static_cast<unsigned>(s - fk.sent.data()), a.probes_lost, a.busy_declined};
    }
};
static void probe_print(const char* name, const ProbeResult& r) {
    std::printf("PROBE %s answer_pass=%u position=%u probes_lost=%u busy_declined=%u\n", name, r.answer_pass,
                r.position, r.probes_lost, r.busy_declined);
}
TEST_F(AcmpOwedProbe, BindNoTimer) {
    ProbeResult r = run(spec::MSG_BIND_RX_COMMAND, {});
    probe_print("bind_rx_no_timer", r);
    EXPECT_EQ(r.answer_pass, ACMP_OWED_MAX + 1u);
}
TEST_F(AcmpOwedProbe, BindOneTimer) {
    ProbeResult r = run(spec::MSG_BIND_RX_COMMAND, {0u});
    probe_print("bind_rx_one_timer", r);
}
TEST_F(AcmpOwedProbe, BindTwoTimers) {
    ProbeResult r = run(spec::MSG_BIND_RX_COMMAND, {0u, 2u});
    probe_print("bind_rx_two_timers", r);
}
TEST_F(AcmpOwedProbe, GetRxStateOneTimer) {
    ProbeResult r = run(spec::MSG_GET_RX_STATE_COMMAND, {0u});
    probe_print("get_rx_state_one_timer", r);
}
TEST_F(AcmpOwedProbe, GetRxStateTwoTimers) {
    ProbeResult r = run(spec::MSG_GET_RX_STATE_COMMAND, {0u, 2u});
    probe_print("get_rx_state_two_timers", r);
}
