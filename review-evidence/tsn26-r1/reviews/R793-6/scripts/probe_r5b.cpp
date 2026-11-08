// SPDX-License-Identifier: MIT
// Reviewer probe (disposable), round 5, part b. Inserted into the AcmpOwed fixture by run_probe.sh.
// As probe_r5.cpp, but the port receives no command after passes `gap` and `gap` + 1: in each of the next two passes
// nothing waits, so the lowest held sinks (sink 1, whose binding's TMR_NO_RESP retry is held, then sink 2) take the
// freed slots, and sink 3 stays held behind the full set.
// Commands then arrive after every pass again, past TMR_NO_RESP + TMR_RETRY + the largest TMR_DELAY draw.
// No ADP frame, no tk_unregistered, no rebind: no sink's probing restarts. Counts the PROBE_TX of every other sink owed
// before sink 3's held retry leaves.
TEST_F(AcmpOwed, R5ProbeLongHeldWaitWithOneGap) {
    for (unsigned gap : {300u, 1000u}) {
        SetUp();
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
        int last1 = -1;
        unsigned held3_from = 0, held3_until = 0;
        std::printf("PROBE r5b gap=%u sink states (sink2 unless marked):", gap);
        for (unsigned n = 1; n <= 9000u && (n < 6400u || a.owed_count != 0u || !held.empty()); ++n) {
            pass();
            if (n >= 3u && n < 6400u && n != gap && n != gap + 1u) {
                deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, seq++));
            }
            if (static_cast<int>(a.sinks[2].state) != last) {
                last = static_cast<int>(a.sinks[2].state);
                std::printf(" [pass=%u state=%d held=%d]", n, last, a.sinks[2].probe_held ? 1 : 0);
            }
            if (static_cast<int>(a.sinks[1].state) != last1) {
                last1 = static_cast<int>(a.sinks[1].state);
                std::printf(" [sink1 pass=%u state=%d]", n, last1);
            }
            held3_from = held3_from == 0u && a.sinks[3].probe_held ? n : held3_from;
            held3_until = a.sinks[3].probe_held ? n : held3_until;
        }
        std::printf("\nPROBE r5b gap=%u: sink3 held from pass %u through pass %u; probes_lost=%u; PROBE_TX:", gap,
                    held3_from, held3_until, a.probes_lost);
        unsigned before[4] = {0, 0, 0, 0};
        bool sink3_left = false;
        for (const Sent& x : fk.sent) {
            Pdu q = read(x.bytes.data());
            if (q.msg == spec::MSG_PROBE_TX_COMMAND && q.listener_uid <= 3u) {
                std::printf(" [sink%u pass=%u]", static_cast<unsigned>(q.listener_uid), x.at - rel);
                sink3_left = sink3_left || q.listener_uid == 3u;
                if (!sink3_left) { before[q.listener_uid]++; }
            }
        }
        std::printf("\nPROBE r5b gap=%u: PROBE_TX owed before sink 3's held retry left: sink1=%u sink2=%u\n", gap, before[1],
                    before[2]);
    }
}
