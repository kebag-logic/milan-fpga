// SPDX-License-Identifier: MIT
// Reviewer probes for the two-slot BIND_RX rule of the ACMP owed bound. Appended inside the anonymous
// namespace of a disposable copy of tests/test_acmp.cpp so it reuses the AcmpOwed port model, which
// polls, then delivers kept frames again, then services timers. Never part of the reviewed tree.
class AcmpOwedProbe2 : public AcmpOwed {
 protected:
    // Re-initialise with every sink on interface 0 so many sinks can share one timer.
    void many_sinks() {
        cfg.n_sinks = ACMP_MAX_SINKS;
        for (unsigned k = 0; k < ACMP_MAX_SINKS; ++k) {
            cfg.sink_interface[k] = 0;
        }
        ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kEnv));
    }
    // Bind sinks first..last-1 one millisecond apart with the egress open; each sends its first probe
    // and arms its 200 ms NO_RESP timeout, so their retries expire one per millisecond later on.
    std::uint32_t stagger(unsigned first, unsigned last) {
        fk.room = true;
        std::uint32_t first_deadline = 0;
        for (unsigned k = first; k < last; ++k) {
            fk.now += 1u;
            bind(k, kTkB, static_cast<std::uint16_t>(k));
            while (acmp_poll(&a)) {
            }
            if (k == first) {
                first_deadline = a.sinks[k].timer_deadline;
            }
        }
        return first_deadline;
    }
    unsigned sent_of(std::uint8_t msg) const {
        unsigned n = 0;
        for (const Sent& s : fk.sent) {
            n += read(s.bytes.data()).msg == msg ? 1u : 0u;
        }
        return n;
    }
    // One scenario: `expiring` retry probes fall due one per pass from pass 1 after the egress returns,
    // while the command `msg` waits behind a full owed set. Returns the pass its answer leaves in.
    void scenario(const char* label, std::uint8_t msg, std::uint8_t rsp, unsigned expiring,
                  std::uint32_t hold = kHoldMs) {
        SetUp();
        held.clear();
        many_sinks();
        std::uint32_t first_deadline = expiring ? stagger(2, 2 + expiring) : 0u;
        fk.clear();
        if (expiring) {
            fk.now = first_deadline - hold - 1u;
        }
        fill(0x7D00);
        fk.clear();
        const std::uint32_t arrival = fk.now;
        EXPECT_FALSE(deliver(command(msg, 1, kTkA, 1, kCtl1, 0, 0x7D08)));
        const std::uint32_t lost_before = a.probes_lost;
        fk.now += hold;
        fk.room = true;
        const std::uint32_t released = fk.now;
        drain();
        const Sent* s = answer(rsp, 0x7D08);
        ASSERT_TRUE(s != nullptr) << label;
        std::printf("PROBE2 %s: hold_ms=%u expiring_probes=%u answer_pass=%u answer_position=%u answer_ms=%u within_200=%d "
                    "probes_sent=%u probes_lost_delta=%u busy_declined=%u\n",
                    label, static_cast<unsigned>(hold), expiring, static_cast<unsigned>(s->at - released), position(s),
                    static_cast<unsigned>(s->at - arrival), (s->at - arrival) <= kCommandTimeoutMs ? 1 : 0,
                    sent_of(spec::MSG_PROBE_TX_COMMAND), a.probes_lost - lost_before, a.busy_declined);
    }
};

// The documented bound is pass ACMP_OWED_MAX + 1 after the egress returns, for a port that polls once per
// pass and delivers again in that pass, before timer service. Compare a one-slot command with a BIND_RX
// while 0, 1, 4 and 14 retry probes of other sinks fall due one per pass.
TEST_F(AcmpOwedProbe2, TimerProbesAgainstTheDeferredBind) {
    for (unsigned expiring : {0u, 1u, 4u, 14u}) {
        scenario("get_rx_state", spec::MSG_GET_RX_STATE_COMMAND, spec::MSG_GET_RX_STATE_RESPONSE, expiring);
        scenario("bind_rx", spec::MSG_BIND_RX_COMMAND, spec::MSG_BIND_RX_RESPONSE, expiring);
    }
}

// The stated trade-off: a BIND_RX that is only answered (unknown sink) also waits for two free slots.
// Record when it is answered compared with a GET_RX_STATE for the same unknown sink, from 7 owed.
TEST_F(AcmpOwedProbe2, AnsweredOnlyBindFromSevenOwed) {
    for (std::uint8_t msg : {spec::MSG_GET_RX_STATE_COMMAND, spec::MSG_BIND_RX_COMMAND}) {
        SetUp();
        held.clear();
        fk.room = false;
        for (unsigned k = 0; k + 1u < ACMP_OWED_MAX; ++k) {
            rx(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, static_cast<std::uint16_t>(0x7E00 + k)));
        }
        fk.clear();
        const bool taken = deliver(command(msg, 9, kTkA, 1, kCtl1, 0, 0x7E08));
        fk.now += kHoldMs;
        fk.room = true;
        const std::uint32_t released = fk.now;
        drain();
        const std::uint8_t rsp = msg == spec::MSG_BIND_RX_COMMAND ? spec::MSG_BIND_RX_RESPONSE
                                                                  : spec::MSG_GET_RX_STATE_RESPONSE;
        const Sent* s = answer(rsp, 0x7E08);
        ASSERT_TRUE(s != nullptr);
        std::printf("PROBE2 unknown-sink msg=%u from_7_owed taken_at_once=%d answer_pass=%u position=%u status=%u "
                    "busy_declined=%u\n",
                    static_cast<unsigned>(msg), taken ? 1 : 0, static_cast<unsigned>(s->at - released), position(s),
                    static_cast<unsigned>(read(s->bytes.data()).status), a.busy_declined);
    }
}

// Answer time of a deferred BIND_RX against the egress hold, for a port polling once per 1 ms pass.
TEST_F(AcmpOwedProbe2, BindHoldSweep) {
    for (std::uint32_t hold : {0u, 60u, 131u, 191u, 192u}) {
        SetUp();
        held.clear();
        fill(0x7F00);
        fk.clear();
        const std::uint32_t arrival = fk.now;
        EXPECT_FALSE(deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7F08)));
        fk.now += hold;
        fk.room = true;
        drain();
        const Sent* s = answer(spec::MSG_BIND_RX_RESPONSE, 0x7F08);
        ASSERT_TRUE(s != nullptr);
        std::printf("PROBE2 bind sweep: hold_ms=%u answer_ms=%u within_200=%d probes_lost=%u\n", hold,
                    static_cast<unsigned>(s->at - arrival), (s->at - arrival) <= kCommandTimeoutMs ? 1 : 0,
                    a.probes_lost);
    }
}

// A port sized to the documented figure: hold 191 ms leaves exactly the 9 passes of ACMP_OWED_MAX + 1 at 1 ms per
// pass. One other sink's retry probe falling due in pass 1 is enough to push a deferred BIND_RX past 200 ms.
TEST_F(AcmpOwedProbe2, DocumentedBudgetAtTheMargin) {
    for (unsigned expiring : {0u, 1u}) {
        scenario("margin get_rx_state", spec::MSG_GET_RX_STATE_COMMAND, spec::MSG_GET_RX_STATE_RESPONSE, expiring, 191u);
        scenario("margin bind_rx", spec::MSG_BIND_RX_COMMAND, spec::MSG_BIND_RX_RESPONSE, expiring, 191u);
    }
}
