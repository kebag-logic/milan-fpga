// SPDX-License-Identifier: MIT
// Reviewer probes for the round 3 probe hold of the ACMP owed bound. Appended inside the anonymous
// namespace of a disposable copy of tests/test_acmp.cpp so it reuses the AcmpOwed port model (poll, then
// deliver kept frames again, then service timers). Each expectation is the behaviour docs/PORTING.md
// "ACMP owed bound" and ACMP-12 state; never part of the reviewed tree.
class AcmpOwedProbe3 : public AcmpOwed {
 protected:
    // A BIND_RX for sink 1 is declined behind the full owed set, `hold` ms before sink 2's timer falls
    // due; the egress then returns and one pass runs, so the BIND_RX is declined again at 7 owed and the
    // timer service of that pass meets sink 2's timer while `bind_waiting` is set.
    void wait_beside(unsigned k, std::uint32_t hold) {
        fk.now = a.sinks[k].timer_deadline - hold - 1u;
        fill(0x7E00);
        fk.clear();
        EXPECT_FALSE(deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7E08)));
        fk.now += hold;
        fk.room = true;
        pass();
    }
};

// PORTING: only "a TMR_DELAY expiry or a TMR_NO_RESP retry" is held. A TMR_RETRY expiry sends no frame,
// so it must take its Milan v1.2 5.5.3.5.30 / 5.5.3.5.31 transition on time beside a waiting BIND_RX.
TEST_F(AcmpOwedProbe3, RetryTimerIsNotHeldBesideTheWaitingBind) {
    sinks_on_one_interface(3u);
    to_state(2u, ACMP_PRB_W_RETRY);
    ASSERT_TRUE(a.sinks[2].state == ACMP_PRB_W_RETRY && a.sinks[2].timer == ACMP_TIMER_RETRY);
    wait_beside(2u, kHoldMs);
    std::printf("PROBE3 retry-timer beside waiting BIND_RX: bind_waiting=%d state_after=%u timer=%u probe_held=%d "
                "probes_held=%u\n", a.bind_waiting ? 1 : 0, static_cast<unsigned>(a.sinks[2].state),
                static_cast<unsigned>(a.sinks[2].timer), a.sinks[2].probe_held ? 1 : 0, a.probes_held);
    EXPECT_TRUE(a.bind_waiting) << "the BIND_RX is waiting for its second slot";
    EXPECT_TRUE(a.sinks[2].state != ACMP_PRB_W_RETRY && !a.sinks[2].probe_held && a.probes_held == 0u)
        << "a TMR_RETRY expiry is not a timer probe and is not held";
}

// PORTING: the second TMR_NO_RESP (in PRB_W_RESP2) sends no frame; Milan v1.2 5.5.3.5.23 moves the sink to
// PRB_W_RETRY with LISTENER_TALKER_TIMEOUT. It must not be held beside a waiting BIND_RX.
TEST_F(AcmpOwedProbe3, SecondNoRespIsNotHeldBesideTheWaitingBind) {
    sinks_on_one_interface(3u);
    to_state(2u, ACMP_PRB_W_RESP2);
    ASSERT_TRUE(a.sinks[2].state == ACMP_PRB_W_RESP2 && a.sinks[2].timer == ACMP_TIMER_NO_RESP);
    wait_beside(2u, kHoldMs);
    std::printf("PROBE3 second no-resp beside waiting BIND_RX: bind_waiting=%d state_after=%u probe_held=%d "
                "probes_held=%u\n", a.bind_waiting ? 1 : 0, static_cast<unsigned>(a.sinks[2].state),
                a.sinks[2].probe_held ? 1 : 0, a.probes_held);
    EXPECT_TRUE(a.sinks[2].state == ACMP_PRB_W_RETRY && !a.sinks[2].probe_held && a.probes_held == 0u)
        << "the second TMR_NO_RESP is not a timer probe and is not held";
}

// PORTING: "A BIND_RX declined with one slot free also sets bind_waiting", and "With no probe held and no
// BIND_RX waiting, a timer probe that finds every slot owed ... is counted in probes_lost". A BIND_RX
// declined behind the full set, with the egress still held when another sink's retry falls due, sets no
// wait, so that retry is lost and counted, not held.
TEST_F(AcmpOwedProbe3, BindDeclinedAtTheFullSetHoldsNoProbe) {
    sinks_on_one_interface(3u);
    retries_due(2u, 1u, 1u);
    fk.now = a.sinks[2].timer_deadline - 10u;
    fill(0x7F00);
    fk.clear();
    EXPECT_FALSE(deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7F08)));
    fk.now = a.sinks[2].timer_deadline;
    acmp_timer_expired(&a, 0);
    std::printf("PROBE3 retry with egress held after a BIND_RX declined at 8 owed: bind_waiting=%d probe_held=%d "
                "probes_held=%u probes_lost=%u state=%u\n", a.bind_waiting ? 1 : 0, a.sinks[2].probe_held ? 1 : 0,
                a.probes_held, a.probes_lost, static_cast<unsigned>(a.sinks[2].state));
    EXPECT_TRUE(!a.bind_waiting && !a.sinks[2].probe_held && a.probes_held == 0u && a.probes_lost == 1u &&
                a.sinks[2].state == ACMP_PRB_W_RESP2)
        << "a BIND_RX declined at the full set holds no probe; the retry is lost and counted";
}
