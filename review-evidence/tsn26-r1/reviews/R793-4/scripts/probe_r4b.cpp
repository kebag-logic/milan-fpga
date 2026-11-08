// SPDX-License-Identifier: MIT
// Reviewer probe (disposable), round 4, part b. Inserted into the AcmpOwed fixture by run_probe.sh.
// Measures a kept backlog at the egress hold PORTING budgets (193 - 2 * Q ms for Q kept commands, 1 ms
// passes, no refused poll) for two ports that both deliver a declined frame again after each accepting
// acmp_poll, before timer service, and never deliver a later frame before a kept one:
//   all  : after an accepting poll, offers its waiting frames in order until one is declined (the test model);
//   one  : after an accepting poll, offers only the oldest waiting frame.
// Retries of sinks 2 and 3 fall due in passes 2 and 3.
// Backlog A: GET_RX_STATE, foreign frame, foreign frame, GET_RX_STATE (Q = 2, budget 189 ms).
// Backlog B: unknown-sink BIND_RX, GET_RX_STATE (Q = 2, budget 189 ms), and the exact hold 200 - (9 + f).
TEST_F(AcmpOwed, R4ProbeBudgetForAPortThatOffersOneFramePerPoll) {
    struct C {
        const char* name;
        bool unknown_bind_head;
        std::uint32_t hold;
    };
    for (const C& c : {C{"get,foreign,foreign,get@189", false, 189u}, C{"unknown-bind,get@189", true, 189u},
                       C{"unknown-bind,get@190(=200-(9+f))", true, 190u}}) {
        for (bool one : {false, true}) {
            SetUp();
            sinks_on_one_interface(4u);
            retries_due(2u, 2u, 1u);
            fk.now = a.sinks[2].timer_deadline - c.hold - 2u;
            fill(0x7B40);
            fk.clear();
            const std::uint32_t arr = fk.now;
            std::vector<std::pair<std::uint8_t, std::uint16_t>> want;
            Pdu foreign = command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, 0x7B4E);
            foreign.listener = kTkB;
            if (c.unknown_bind_head) {
                deliver(command(spec::MSG_BIND_RX_COMMAND, 40, kTkA, 1, kCtl1, 0, 0x7B48));
                want.push_back({spec::MSG_BIND_RX_RESPONSE, 0x7B48});
            } else {
                deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 1, 0, 0, kCtl2, 0, 0x7B48));
                want.push_back({spec::MSG_GET_RX_STATE_RESPONSE, 0x7B48});
                deliver(foreign);
                deliver(foreign);
            }
            deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 1, 0, 0, kCtl2, 0, 0x7B49));
            want.push_back({spec::MSG_GET_RX_STATE_RESPONSE, 0x7B49});
            fk.now += c.hold;
            fk.room = true;
            const std::uint32_t rel = fk.now;
            for (unsigned n = 1; n <= 40u && (a.owed_count != 0u || !held.empty()); ++n) {
                fk.now += 1u;
                const unsigned before = a.owed_count;
                static_cast<void>(acmp_poll(&a));
                if (a.owed_count < before) {
                    while (!held.empty() &&
                           acmp_rx(&a, held.front().interface, held.front().bytes.data(), held.front().bytes.size())) {
                        held.erase(held.begin());
                        if (one) {
                            break;
                        }
                    }
                }
                if (fk.armed[0] && static_cast<std::int32_t>(fk.now - fk.at[0]) >= 0) {
                    acmp_timer_expired(&a, 0);
                }
            }
            std::printf("PROBE r4b case=%s port=%s", c.name, one ? "one" : "all");
            for (unsigned i = 0; i < want.size(); ++i) {
                const Sent* s = answer(want[i].first, want[i].second);
                std::printf(" answer%u[pass=%d since_arrival_ms=%d pos=%d]", i, s ? static_cast<int>(s->at - rel) : -1,
                            s ? static_cast<int>(s->at - arr) : -1, s ? static_cast<int>(position(s)) : -1);
            }
            std::printf(" probes_held=%u probes_lost=%u sent=%zu\n", a.probes_held, a.probes_lost, fk.sent.size());
        }
    }
}
