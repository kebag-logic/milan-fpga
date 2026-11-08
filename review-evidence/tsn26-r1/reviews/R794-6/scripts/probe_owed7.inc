// SPDX-License-Identifier: MIT
// Reviewer probe: how long a held retry waits when commands that arrive after the kept BIND_RX is taken
// take the freed slots ahead of it. PORTING bounds the wait: through the pass that takes the BIND_RX, plus one
// pass for each frame owed by a command kept behind the BIND_RX and for each other probe owed before it.
// Here no command is kept behind the BIND_RX and no other sink probes, so the stated wait ends in the pass
// after the BIND_RX is taken. Appended inside the anonymous namespace of a disposable copy of
// tests/test_acmp.cpp; never part of the reviewed tree.
class AcmpOwedProbe7 : public AcmpOwed {
 protected:
    // mode 0: no later command. mode 1: one GET_RX_STATE arrives in each of the next `fresh` passes after the
    // BIND_RX is taken and is offered after the accepting poll, before timer service (a waiting frame the port
    // offers for the first time; it is accepted, never declined). mode 2: the same GETs arrive between passes,
    // from the pass that takes the BIND_RX on, are declined by the full set and kept, then offered after the next
    // accepting poll.
    void run(int mode, unsigned fresh) {
        SetUp();
        sinks_on_one_interface(3u);
        retries_due(2u, 1u, 1u);
        fk.now = a.sinks[2].timer_deadline - kHoldMs - 1u;
        fill(0x7B40);
        fk.clear();
        EXPECT_FALSE(deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7B48)));
        fk.now += kHoldMs;
        fk.room = true;
        unsigned taken = 0, owed = 0, injected = 0, declined_fresh = 0;
        for (unsigned n = 1; n <= 8u * ACMP_OWED_MAX && (a.owed_count != 0u || !held.empty() || owed == 0u); ++n) {
            const bool inject = taken != 0u && injected < fresh;
            fk.now += 1u;
            static_cast<void>(acmp_poll(&a));
            while (!held.empty() &&
                   acmp_rx(&a, held.front().interface, held.front().bytes.data(), held.front().bytes.size())) {
                held.erase(held.begin());
            }
            if (inject && mode == 1) {
                const bool ok = deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0,
                                                static_cast<std::uint16_t>(0x7C00 + injected)));
                declined_fresh += ok ? 0u : 1u;
                ++injected;
            }
            if (fk.armed[0] && static_cast<std::int32_t>(fk.now - fk.at[0]) >= 0) {
                acmp_timer_expired(&a, 0);
            }
            taken = taken == 0u && a.sinks[1].bound ? n : taken;
            if (mode == 2 && taken != 0u && injected < fresh) {
                const bool ok = deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0,
                                                static_cast<std::uint16_t>(0x7C00 + injected)));
                declined_fresh += ok ? 0u : 1u;
                ++injected;
            }
            owed = owed == 0u && !a.sinks[2].probe_held && a.sinks[2].state == ACMP_PRB_W_RESP2 ? n : owed;
        }
        std::printf("PROBE7 mode=%d later_commands=%u (declined at arrival %u): BIND_RX taken in pass %u; held retry "
                    "owed in pass %u; stated owed by pass %u; excess %d pass(es); probes_held=%u probes_lost=%u\n",
                    mode, fresh, declined_fresh, taken, owed, taken + 1u, static_cast<int>(owed) - static_cast<int>(taken + 1u),
                    static_cast<unsigned>(a.probes_held), static_cast<unsigned>(a.probes_lost));
    }
};

TEST_F(AcmpOwedProbe7, CommandsAfterTheTakenBindDelayTheHeldRetry) {
    run(0, 0u);
    for (unsigned fresh : {1u, 3u, 10u}) {
        run(1, fresh);
        run(2, fresh);
    }
}
