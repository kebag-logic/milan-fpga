// SPDX-License-Identifier: MIT
// Reviewer probe (disposable), round 4. Inserted into the AcmpOwed fixture by run_probe.sh.
// Compares two ports that both deliver a declined frame again after each accepting acmp_poll, before timer
// service, and never deliver a later frame before a kept one:
//   all : after an accepting poll, offers its waiting frames in order until one is declined (the test model);
//   one : after an accepting poll, offers only the oldest waiting frame.
// A TMR_NO_RESP retry of sink 3 falls due in pass 1. Each case prints the pass of every kept answer, the
// position of the retry's PROBE_TX among the sent frames, and the counters.
namespace {
struct R4Case {
    const char* name;
    unsigned head;   // 0: unknown-sink BIND_RX; 1: same-talker rebind; 2: GET_RX_STATE then a foreign frame
};
}  // namespace

TEST_F(AcmpOwed, R4ProbeOneFramePerAcceptedPoll) {
    for (const R4Case& c : {R4Case{"unknown-sink-bind,get", 0u}, R4Case{"same-talker-rebind,get", 1u},
                            R4Case{"get,foreign,get", 2u}}) {
        for (bool one : {false, true}) {
            SetUp();
            sinks_on_one_interface(4u);
            if (c.head == 1u) {
                to_state(1u, ACMP_SETTLED_NO_RSV);
            }
            retries_due(3u, 1u, 1u);
            fk.now = a.sinks[3].timer_deadline - kHoldMs - 1u;
            fill(0x7B00);
            fk.clear();
            std::vector<std::pair<std::uint8_t, std::uint16_t>> want;
            if (c.head == 0u) {
                deliver(command(spec::MSG_BIND_RX_COMMAND, 40, kTkA, 1, kCtl1, 0, 0x7B08));
                want.push_back({spec::MSG_BIND_RX_RESPONSE, 0x7B08});
            } else if (c.head == 1u) {
                deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7B08));
                want.push_back({spec::MSG_BIND_RX_RESPONSE, 0x7B08});
            } else {
                deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 1, 0, 0, kCtl2, 0, 0x7B08));
                want.push_back({spec::MSG_GET_RX_STATE_RESPONSE, 0x7B08});
                Pdu foreign = command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, 0x7B0E);
                foreign.listener = kTkB;
                deliver(foreign);
            }
            deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 2, 0, 0, kCtl2, 0, 0x7B09));
            want.push_back({spec::MSG_GET_RX_STATE_RESPONSE, 0x7B09});
            fk.now += kHoldMs;
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
            std::printf("PROBE r4 case=%s port=%s", c.name, one ? "one" : "all");
            unsigned f = 0;
            for (unsigned i = 0; i < want.size(); ++i) {
                const Sent* s = answer(want[i].first, want[i].second);
                std::printf(" answer%u_pass=%d(formula %u)", i, s ? static_cast<int>(s->at - rel) : -1,
                            ACMP_OWED_MAX + 1u + f);
                f += 1u;
            }
            int probe_pos = -1;
            for (const Sent& x : fk.sent) {
                Pdu q = read(x.bytes.data());
                if (q.msg == spec::MSG_PROBE_TX_COMMAND && q.listener_uid == 3u) {
                    probe_pos = static_cast<int>(position(&x));
                }
            }
            const Sent* last = answer(want.back().first, want.back().second);
            std::printf(" retry_position=%d last_answer_position=%d probes_held=%u probes_lost=%u busy_declined=%u\n",
                        probe_pos, last ? static_cast<int>(position(last)) : -1, a.probes_held, a.probes_lost,
                        a.busy_declined);
        }
    }
}
