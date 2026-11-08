// SPDX-License-Identifier: MIT
// Reviewer probe (disposable), round 3. Inserted inside the anonymous test namespace of a copy of
// tests/test_acmp.cpp, after the AcmpOwed tests. Uses the committed AcmpOwed port model (pass(): poll once,
// deliver kept frames in order until one is declined, then service due timers) and prints, in 1 ms passes
// after the egress returns, when each kept command is answered and what happened to timer probes.
struct R3Kept {
    std::uint8_t msg;
    std::uint8_t rsp;
    unsigned sink;
    std::uint64_t talker;
    std::uint16_t uid;
    std::uint16_t seq;
};
class TimerProbesAgainstTheDeferredBind : public AcmpOwed {
 protected:
    std::vector<unsigned> timed;
    std::uint32_t r3_arrival = 0;
    std::uint32_t r3_released = 0;
    // n sinks; sinks 2..2+count-1 are bound to kTkB before the fill so that their TMR_NO_RESP retries
    // fall due from pass 1 after release, `step` ms apart. two_if puts odd sinks on interface 1.
    void setup(unsigned n, unsigned count, std::uint32_t step, bool two_if = false) {
        held.clear();
        timed.clear();
        cfg.n_sinks = n;
        for (unsigned k = 0; k < n; ++k) {
            cfg.sink_interface[k] = two_if ? (k % 2u) : 0u;
        }
        ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kEnv));
        fk.room = true;
        for (unsigned k = 2; k < 2u + count; ++k) {
            fk.now += step;
            bind(k, kTkB, static_cast<std::uint16_t>(k));
            timed.push_back(k);
        }
    }
    std::uint32_t first_due() const {
        std::uint32_t f = a.sinks[timed.front()].timer_deadline;
        for (unsigned k : timed) {
            f = static_cast<std::int32_t>(a.sinks[k].timer_deadline - f) < 0 ? a.sinks[k].timer_deadline : f;
        }
        return f;
    }
    // Fills the owed set, offers the kept commands, releases the egress hold_ms later (one ms before the
    // first timed retry falls due) and runs passes until nothing is owed or kept. gated: the port offers
    // the head kept frame only when acmp_rx_ready is true, and so never has it declined.
    void run(std::uint32_t hold_ms, const std::vector<R3Kept>& kept, bool gated = false) {
        fk.now = (timed.empty() ? fk.now + 1000u : first_due()) - hold_ms - 1u;
        fill(0x7A00);
        fk.clear();
        r3_arrival = fk.now;
        for (const R3Kept& k : kept) {
            Pdu p = command(k.msg, k.sink, k.talker, k.uid, kCtl1, 0, k.seq);
            if (gated) {
                held.push_back({0u, acmpdu(p)});
            } else {
                EXPECT_FALSE(deliver(p)) << "probe: a kept command is declined behind the full owed set";
            }
        }
        fk.now += hold_ms;
        fk.room = true;
        r3_released = fk.now;
        for (unsigned n = 0; n < 400u && (a.owed_count != 0u || !held.empty()); ++n) {
            if (!gated) {
                pass();
                continue;
            }
            fk.now += 1u;
            static_cast<void>(acmp_poll(&a));
            while (!held.empty() && acmp_rx_ready(&a)) {
                EXPECT_TRUE(acmp_rx(&a, held.front().interface, held.front().bytes.data(), held.front().bytes.size()));
                held.erase(held.begin());
            }
            for (unsigned i = 0; i < cfg.n_interfaces; ++i) {
                if (fk.armed[i] && static_cast<std::int32_t>(fk.now - fk.at[i]) >= 0) {
                    acmp_timer_expired(&a, i);
                }
            }
        }
    }
    void report(const char* name, const std::vector<R3Kept>& kept) {
        std::printf("PROBE %s n_sinks=%u timed=%zu", name, cfg.n_sinks, timed.size());
        for (const R3Kept& k : kept) {
            const Sent* s = answer(k.rsp, k.seq);
            if (s == nullptr) {
                std::printf(" [msg%u seq%04x UNANSWERED]", k.msg, k.seq);
                continue;
            }
            std::printf(" [msg%u answer_pass=%u since_arrival_ms=%u pos=%u]", k.msg, s->at - r3_released,
                        s->at - r3_arrival, position(s));
        }
        unsigned sent_timed = 0;
        std::uint32_t last_probe_pass = 0;
        for (unsigned k : timed) {
            for (const Sent& s : fk.sent) {
                Pdu q = read(s.bytes.data());
                if (q.msg == spec::MSG_PROBE_TX_COMMAND && q.listener_uid == k && q.seq == a.sinks[k].probe_seq &&
                    s.at > r3_released) {
                    ++sent_timed;
                    last_probe_pass = std::max(last_probe_pass, s.at - r3_released);
                }
            }
        }
        unsigned stale = 0;
        for (unsigned k = 0; k < cfg.n_sinks; ++k) {
            stale += a.sinks[k].probe_held ? 1u : 0u;
        }
        std::printf(" probes_lost=%u probes_held=%u timed_probes_sent=%u last_timed_probe_pass=%u busy_declined=%u "
                    "probe_held_left=%u bind_waiting=%d owed=%u kept_left=%zu\n",
                    a.probes_lost, a.probes_held, sent_timed, last_probe_pass, a.busy_declined, stale,
                    a.bind_waiting ? 1 : 0, a.owed_count, held.size());
    }
    static R3Kept bind_rx(unsigned sink, std::uint16_t seq) {
        return {spec::MSG_BIND_RX_COMMAND, spec::MSG_BIND_RX_RESPONSE, sink, kTkA, 1u, seq};
    }
    static R3Kept get_rx(unsigned sink, std::uint16_t seq) {
        return {spec::MSG_GET_RX_STATE_COMMAND, spec::MSG_GET_RX_STATE_RESPONSE, sink, 0u, 0u, seq};
    }
    static R3Kept unbind_rx(unsigned sink, std::uint16_t seq) {
        return {spec::MSG_UNBIND_RX_COMMAND, spec::MSG_UNBIND_RX_RESPONSE, sink, 0u, 0u, seq};
    }
    static R3Kept get_tx(std::uint16_t seq) {
        return {spec::MSG_GET_TX_STATE_COMMAND, spec::MSG_GET_TX_STATE_RESPONSE, 0u, kOwn, 1u, seq};
    }
};

// (1) Sixteen sinks, fourteen other sinks' retries one per pass from pass 1, BIND_RX kept alone.
TEST_F(TimerProbesAgainstTheDeferredBind, SixteenSinksOnePerPass) {
    setup(16u, 14u, 1u);
    std::vector<R3Kept> k{bind_rx(1u, 0x7A08)};
    run(kHoldMs, k);
    report("sixteen_sinks_one_per_pass", k);
    const Sent* s = answer(spec::MSG_BIND_RX_RESPONSE, 0x7A08);
    ASSERT_TRUE(s != nullptr);
    EXPECT_EQ(s->at - r3_released, ACMP_OWED_MAX + 1u);
    EXPECT_EQ(a.probes_lost, 0u);
}
// (1) Fourteen retries all in pass 1.
TEST_F(TimerProbesAgainstTheDeferredBind, SixteenSinksAllInPassOne) {
    setup(16u, 14u, 0u);
    std::vector<R3Kept> k{bind_rx(1u, 0x7A08)};
    run(kHoldMs, k);
    report("sixteen_sinks_all_in_pass_one", k);
    const Sent* s = answer(spec::MSG_BIND_RX_RESPONSE, 0x7A08);
    ASSERT_TRUE(s != nullptr);
    EXPECT_EQ(s->at - r3_released, ACMP_OWED_MAX + 1u);
    EXPECT_EQ(a.probes_lost, 0u);
}
// (1) Sinks split over two interfaces.
TEST_F(TimerProbesAgainstTheDeferredBind, TwoInterfaces) {
    setup(16u, 14u, 1u, true);
    std::vector<R3Kept> k{bind_rx(1u, 0x7A08)};
    run(kHoldMs, k);
    report("two_interfaces", k);
    const Sent* s = answer(spec::MSG_BIND_RX_RESPONSE, 0x7A08);
    ASSERT_TRUE(s != nullptr);
    EXPECT_EQ(s->at - r3_released, ACMP_OWED_MAX + 1u);
    EXPECT_EQ(a.probes_lost, 0u);
}
// (1)/(2) Mixed commands kept behind the BIND_RX: GET_RX_STATE, a second BIND_RX, UNBIND_RX, GET_TX_STATE.
TEST_F(TimerProbesAgainstTheDeferredBind, MixedCommandsBehind) {
    setup(16u, 6u, 1u);
    std::vector<R3Kept> k{bind_rx(1u, 0x7A08), get_rx(1u, 0x7A09), bind_rx(0u, 0x7A0A), unbind_rx(15u, 0x7A0B),
                          get_tx(0x7A0C)};
    run(kHoldMs, k);
    report("mixed_commands_behind", k);
    EXPECT_EQ(a.probes_lost, 0u);
}
// (2) A BIND_RX that owes one frame (unknown sink) still waits for two slots; when does the held probe go?
TEST_F(TimerProbesAgainstTheDeferredBind, UnknownSinkBind) {
    setup(16u, 1u, 1u);
    std::vector<R3Kept> k{bind_rx(40u, 0x7A08)};
    run(kHoldMs, k);
    report("unknown_sink_bind", k);
    for (const Sent& s : fk.sent) {
        Pdu q = read(s.bytes.data());
        if (q.msg == spec::MSG_PROBE_TX_COMMAND && q.listener_uid == 2u) {
            std::printf("PROBE unknown_sink_bind held_probe_sent_pass=%u position=%u\n", s.at - r3_released,
                        position(&s));
        }
    }
}
// Margin: 191 ms hold, BIND_RX alone and with a GET_RX_STATE kept behind it.
TEST_F(TimerProbesAgainstTheDeferredBind, DocumentedBudgetAtTheMargin) {
    const std::uint32_t margin = kCommandTimeoutMs - (ACMP_OWED_MAX + 1u);
    setup(16u, 7u, 1u);
    std::vector<R3Kept> k{bind_rx(1u, 0x7A08)};
    run(margin, k);
    report("margin_bind_alone_7_retries", k);
    const Sent* s = answer(spec::MSG_BIND_RX_RESPONSE, 0x7A08);
    ASSERT_TRUE(s != nullptr);
    EXPECT_EQ(s->at - r3_arrival, kCommandTimeoutMs);
}
TEST_F(TimerProbesAgainstTheDeferredBind, DocumentedBudgetAtTheMarginWithBacklog) {
    const std::uint32_t margin = kCommandTimeoutMs - (ACMP_OWED_MAX + 1u);
    setup(16u, 2u, 1u);
    std::vector<R3Kept> k{bind_rx(1u, 0x7A08), get_rx(1u, 0x7A09)};
    run(margin, k);
    report("margin_bind_then_get", k);
}
// Gated port (tests acmp_rx_ready, never has a frame declined): the disclosed limit.
TEST_F(TimerProbesAgainstTheDeferredBind, GatedPortOnePerPass) {
    setup(16u, 14u, 1u);
    std::vector<R3Kept> k{bind_rx(1u, 0x7A08)};
    run(kHoldMs, k, true);
    report("gated_port_one_per_pass", k);
    const Sent* s = answer(spec::MSG_BIND_RX_RESPONSE, 0x7A08);
    ASSERT_TRUE(s != nullptr);
    EXPECT_LE(s->at - r3_released, ACMP_OWED_MAX + 1u + cfg.n_sinks);
}
TEST_F(TimerProbesAgainstTheDeferredBind, GatedPortAllInPassOne) {
    setup(16u, 14u, 0u);
    std::vector<R3Kept> k{bind_rx(1u, 0x7A08)};
    run(kHoldMs, k, true);
    report("gated_port_all_in_pass_one", k);
}
// Sustained commands: after the BIND_RX is taken a GET_RX_STATE arrives every pass for 40 passes.
TEST_F(TimerProbesAgainstTheDeferredBind, SustainedCommandsBehind) {
    setup(4u, 2u, 0u);
    std::vector<R3Kept> k{bind_rx(1u, 0x7A08)};
    fk.now = first_due() - kHoldMs - 1u;
    fill(0x7A00);
    fk.clear();
    r3_arrival = fk.now;
    EXPECT_FALSE(deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7A08)));
    fk.now += kHoldMs;
    fk.room = true;
    r3_released = fk.now;
    for (unsigned n = 0; n < 40u; ++n) {
        static_cast<void>(deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 1, 0, 0, kCtl2, 0,
                                          static_cast<std::uint16_t>(0x7B00 + n))));
        pass();
    }
    std::printf("PROBE sustained_after_40_passes probes_held=%u probes_lost=%u held_flags=%u%u state2=%d state3=%d\n",
                a.probes_held, a.probes_lost, a.sinks[2].probe_held ? 1u : 0u, a.sinks[3].probe_held ? 1u : 0u,
                static_cast<int>(a.sinks[2].state), static_cast<int>(a.sinks[3].state));
    for (unsigned n = 0; n < 400u && (a.owed_count != 0u || !held.empty()); ++n) {
        pass();
    }
    report("sustained_commands_behind", k);
}
// Backlog without any BIND_RX or timer, 191 ms hold: two GET_RX_STATE kept. Uses only fixture API present at
// round 2 (fill, deliver, pass, answer), so it also runs at 968a164.
TEST_F(AcmpOwed, R3ProbeBacklogAtTheMargin) {
    const std::uint32_t margin = kCommandTimeoutMs - (ACMP_OWED_MAX + 1u);
    fill(0x7A00);
    fk.clear();
    const std::uint32_t arrival = fk.now;
    EXPECT_FALSE(deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 1, 0, 0, kCtl1, 0, 0x7A08)));
    EXPECT_FALSE(deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 1, 0, 0, kCtl1, 0, 0x7A09)));
    fk.now += margin;
    fk.room = true;
    for (unsigned n = 0; n < 40u && (a.owed_count != 0u || !held.empty()); ++n) {
        pass();
    }
    const Sent* s1 = answer(spec::MSG_GET_RX_STATE_RESPONSE, 0x7A08);
    const Sent* s2 = answer(spec::MSG_GET_RX_STATE_RESPONSE, 0x7A09);
    ASSERT_TRUE(s1 != nullptr && s2 != nullptr);
    std::printf("PROBE backlog_two_gets_margin first_ms=%u second_ms=%u\n", s1->at - arrival, s2->at - arrival);
}
