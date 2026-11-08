// SPDX-License-Identifier: MIT
// Reviewer probe (disposable), round 5. Inserted into the AcmpOwed fixture by run_probe.sh.
// Long sustained hold: the round 4 "sustained" setup (sink 2 TMR_DELAY and sink 3 TMR_NO_RESP retry due beside a
// deferred BIND_RX; sink 2 owed first, sink 3 held), but one GET_RX_STATE arrives after every pass for 5600 passes,
// longer than TMR_NO_RESP + TMR_RETRY + the largest TMR_DELAY draw. No ADP frame, no tk_unregistered, no rebind:
// no sink's probing restarts. Prints every PROBE_TX of sinks 2 and 3 with its pass, and sink 2's state changes,
// so the probes of sink 2 owed before sink 3's held retry can be counted.
TEST_F(AcmpOwed, R5ProbeLongHeldWait) {
    sinks_on_one_interface(4u);
    to_state(2u, ACMP_PRB_W_DELAY);
    a.sinks[2].timer_deadline = fk.now + 200u;
    retries_due(3u, 1u, 0u);
    const std::uint32_t dy = a.sinks[2].timer_deadline;
    fk.now = dy - kHoldMs - 1u;
    fill(0x7B80);
    fk.clear();
    deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7B88));
    fk.now += kHoldMs;
    fk.room = true;
    const std::uint32_t rel = fk.now;
    std::uint16_t seq = 0x6000;
    int last = -1;
    unsigned held3_until = 0;
    std::printf("PROBE r5 long-hold sink2 states:");
    for (unsigned n = 1; n <= 8000u && (n < 5600u || a.owed_count != 0u || !held.empty()); ++n) {
        pass();
        if (n >= 3u && n < 5600u) {
            deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, seq++));
        }
        if (static_cast<int>(a.sinks[2].state) != last) {
            last = static_cast<int>(a.sinks[2].state);
            std::printf(" [pass=%u state=%d held=%d]", n, last, a.sinks[2].probe_held ? 1 : 0);
        }
        held3_until = a.sinks[3].probe_held ? n : held3_until;
    }
    std::printf("\nPROBE r5 long-hold: sink3 held through pass %u; probes_lost=%u; PROBE_TX:", held3_until, a.probes_lost);
    unsigned sink2_before_sink3 = 0;
    bool sink3_left = false;
    for (const Sent& x : fk.sent) {
        Pdu q = read(x.bytes.data());
        if (q.msg == spec::MSG_PROBE_TX_COMMAND && (q.listener_uid == 2u || q.listener_uid == 3u)) {
            std::printf(" [sink%u pass=%u]", static_cast<unsigned>(q.listener_uid), x.at - rel);
            sink3_left = sink3_left || q.listener_uid == 3u;
            sink2_before_sink3 += (q.listener_uid == 2u && !sink3_left) ? 1u : 0u;
        }
    }
    std::printf("\nPROBE r5 long-hold: sink 2 PROBE_TX owed before sink 3's held retry left = %u\n", sink2_before_sink3);
}
