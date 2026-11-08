// SPDX-License-Identifier: MIT
// Reviewer probe (disposable), round 3. A port that follows PORTING literally: it delivers a kept frame
// again only after an acmp_poll that accepts an owed frame, then services due timers. The egress accepts in
// pass 1, refuses in pass 2 and accepts from pass 3; another sink's TMR_NO_RESP retry falls due in pass 2.
TEST_F(AcmpOwed, R3ProbeRefusedPollKeepsTheHold) {
    sinks_on_one_interface(3u);
    retries_due(2u, 1u, 1u);
    const std::uint32_t due = a.sinks[2].timer_deadline;
    fk.now = due - kHoldMs - 2u;
    fill(0x7A00);
    fk.clear();
    EXPECT_FALSE(deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7A08)));
    fk.now += kHoldMs;
    const std::uint32_t released = fk.now;
    for (unsigned n = 1; n <= 40u && (a.owed_count != 0u || !held.empty()); ++n) {
        fk.room = n != 2u;
        fk.now += 1u;
        const unsigned before = a.owed_count;
        static_cast<void>(acmp_poll(&a));
        if (a.owed_count < before) {
            while (!held.empty() &&
                   acmp_rx(&a, held.front().interface, held.front().bytes.data(), held.front().bytes.size())) {
                held.erase(held.begin());
            }
        }
        for (unsigned i = 0; i < cfg.n_interfaces; ++i) {
            if (fk.armed[i] && static_cast<std::int32_t>(fk.now - fk.at[i]) >= 0) {
                acmp_timer_expired(&a, i);
            }
        }
    }
    const Sent* s = answer(spec::MSG_BIND_RX_RESPONSE, 0x7A08);
    ASSERT_TRUE(s != nullptr);
    unsigned probe_pos = 0;
    for (const Sent& x : fk.sent) {
        Pdu q = read(x.bytes.data());
        if (q.msg == spec::MSG_PROBE_TX_COMMAND && q.listener_uid == 2u) {
            probe_pos = position(&x);
        }
    }
    std::printf("PROBE refused_poll bind_answer_pass=%u bind_position=%u other_probe_position=%u busy_declined=%u "
                "probes_held=%u probes_lost=%u\n",
                s->at - released, position(s), probe_pos, a.busy_declined, a.probes_held, a.probes_lost);
}
