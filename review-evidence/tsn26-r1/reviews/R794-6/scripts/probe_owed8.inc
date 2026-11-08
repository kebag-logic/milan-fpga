// SPDX-License-Identifier: MIT
// Reviewer probe: how many held probes take freed slots in one pass when the port's passes are less than
// 1 ms apart. PORTING says held probes take freed slots one per pass and follow the last kept command one per
// pass; the hold re-arms a held probe 1 ms on. Four TMR_NO_RESP retries fall due 1 ms apart, or all in one
// ms, beside a BIND_RX kept behind the full set. The port then runs `per_ms` passes per millisecond, each pass as the fixture's pass(): an
// accepting poll, the kept frames offered until one is declined, then timer service if the timer is due.
// Appended inside the anonymous namespace of a disposable copy of tests/test_acmp.cpp; never part of the
// reviewed tree.
class AcmpOwedProbe8 : public AcmpOwed {
 protected:
    void run(unsigned per_ms, std::uint32_t step_ms) {
        SetUp();
        sinks_on_one_interface(6u);
        retries_due(2u, 4u, step_ms);
        std::uint32_t first_due = a.sinks[2].timer_deadline;  // sink 2's retry falls due first
        fk.now = first_due - kHoldMs - 1u;
        fill(0x7C00);
        fk.clear();
        static_cast<void>(deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7C08)));
        fk.now += kHoldMs;
        fk.room = true;
        bool was_held[6] = {};
        unsigned most = 0, most_pass = 0, taken = 0;
        std::string owed_at;
        for (unsigned n = 1; n <= 40u * per_ms && (a.owed_count != 0u || !held.empty() || n < 4u); ++n) {
            if ((n - 1u) % per_ms == 0u) {
                fk.now += 1u;
            }
            for (unsigned k = 2; k < 6; ++k) {
                was_held[k] = a.sinks[k].probe_held;
            }
            static_cast<void>(acmp_poll(&a));
            while (!held.empty() &&
                   acmp_rx(&a, held.front().interface, held.front().bytes.data(), held.front().bytes.size())) {
                held.erase(held.begin());
            }
            if (fk.armed[0] && static_cast<std::int32_t>(fk.now - fk.at[0]) >= 0) {
                acmp_timer_expired(&a, 0);
            }
            taken = taken == 0u && a.sinks[1].bound ? n : taken;
            unsigned left_hold = 0;
            for (unsigned k = 2; k < 6; ++k) {
                if (was_held[k] && !a.sinks[k].probe_held) {
                    ++left_hold;
                    owed_at += " sink" + std::to_string(k) + "@pass" + std::to_string(n);
                }
            }
            if (left_hold > most) {
                most = left_hold;
                most_pass = n;
            }
        }
        const Sent* s = answer(spec::MSG_BIND_RX_RESPONSE, 0x7C08);
        std::printf("PROBE8 passes_per_ms=%u retry_step_ms=%u: BIND_RX taken in pass %u, answered %u ms after release; held probes owed:%s;"
                    " most owed in one pass=%u (pass %u); probes_held=%u probes_lost=%u owed_left=%u\n",
                    per_ms, static_cast<unsigned>(step_ms), taken, s ? static_cast<unsigned>(s->at - (first_due - 1u)) : 0u, owed_at.c_str(), most,
                    most_pass, static_cast<unsigned>(a.probes_held), static_cast<unsigned>(a.probes_lost),
                    static_cast<unsigned>(a.owed_count));
    }
};

TEST_F(AcmpOwedProbe8, OnePassPerMs) { run(1u, 1u); run(1u, 0u); }
TEST_F(AcmpOwedProbe8, TwoPassesPerMs) { run(2u, 1u); run(2u, 0u); }
TEST_F(AcmpOwedProbe8, FourPassesPerMs) { run(4u, 1u); run(4u, 0u); }
