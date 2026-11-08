// SPDX-License-Identifier: MIT
// Reviewer probe (disposable), round 4, part c. Inserted into the AcmpOwed fixture by run_probe.sh.
// (1) Per-sink count of the held-probe bound. Sink 2 (Y) has a TMR_DELAY expiry and sink 3 (X) a retry due
//     beside a deferred BIND_RX; Y is owed first and X stays held. One new GET_RX_STATE then arrives after every pass for 237
//     passes (each declined and kept, so X keeps waiting), longer than TMR_NO_RESP. Prints every PROBE_TX
//     that Y and X send, with its pass, so the probes owed before X can be counted.
// (2) A held retry and a PROBE_TX_RESPONSE with a failure status. Prints the sink's state, probing and hold.
TEST_F(AcmpOwed, R4ProbeHeldProbeBoundAndCancel) {
    {
        sinks_on_one_interface(4u);
        to_state(2u, ACMP_PRB_W_DELAY);
        // A TMR_DELAY draw is uniform in 0..ACMP_TMR_DELAY_MAX_MS; the probe moves this draw to 200 ms after
        // now so that it falls due with sink 3's retry, as another draw in the same range would.
        a.sinks[2].timer_deadline = fk.now + 200u;
        retries_due(3u, 1u, 0u);
        const std::uint32_t dy = a.sinks[2].timer_deadline;
        std::printf("PROBE r4c sustained setup: sink2 TMR_DELAY due +%u ms, sink3 TMR_NO_RESP due +%u ms\n",
                    a.sinks[2].timer_deadline - fk.now, a.sinks[3].timer_deadline - fk.now);
        fk.now = dy - kHoldMs - 1u;
        fill(0x7B80);
        fk.clear();
        deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7B88));
        fk.now += kHoldMs;
        fk.room = true;
        const std::uint32_t rel = fk.now;
        std::uint16_t seq = 0x6000;
        for (unsigned n = 1; n <= 400u && (n < 240u || a.owed_count != 0u || !held.empty()); ++n) {
            pass();
            if (n >= 3u && n < 240u) {
                deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, seq++));
            }
        }
        std::printf("PROBE r4c sustained: probes_held=%u probes_lost=%u held_left=%d%d", a.probes_held, a.probes_lost,
                    a.sinks[2].probe_held ? 1 : 0, a.sinks[3].probe_held ? 1 : 0);
        for (const Sent& x : fk.sent) {
            Pdu q = read(x.bytes.data());
            if (q.msg == spec::MSG_PROBE_TX_COMMAND && (q.listener_uid == 2u || q.listener_uid == 3u)) {
                std::printf(" [sink%u pass=%u pos=%u]", static_cast<unsigned>(q.listener_uid), x.at - rel, position(&x));
            }
        }
        std::printf("\n");
    }
    {
        SetUp();
        sinks_on_one_interface(3u);
        retries_due(2u, 1u, 1u);
        fk.now = a.sinks[2].timer_deadline - kHoldMs - 1u;
        fill(0x7BC0);
        fk.clear();
        deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7BC8));
        fk.now += kHoldMs;
        fk.room = true;
        pass();
        const bool held_before = a.sinks[2].probe_held;
        deliver(probe_answer(2u, spec::STATUS_LISTENER_TALKER_TIMEOUT));
        pass();
        std::printf("PROBE r4c failure-response: held_before=%d held_after=%d state=%d (PRB_W_RETRY=%d) probing=%d "
                    "(ACTIVE=%d) timer=%d (RETRY=%d) probes_held=%u\n",
                    held_before ? 1 : 0, a.sinks[2].probe_held ? 1 : 0, static_cast<int>(a.sinks[2].state),
                    static_cast<int>(ACMP_PRB_W_RETRY), static_cast<int>(a.sinks[2].probing),
                    static_cast<int>(ACMP_PROBING_ACTIVE), static_cast<int>(a.sinks[2].timer),
                    static_cast<int>(ACMP_TIMER_RETRY), a.probes_held);
    }
}
