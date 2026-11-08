// SPDX-License-Identifier: MIT
// Reviewer probe for the disclosed limit of the ACMP owed bound: a port that tests acmp_rx_ready and never
// offers a waiting frame. Appended inside the anonymous namespace of a disposable copy of
// tests/test_acmp.cpp; never part of the reviewed tree. Budget stated by PORTING: ACMP_OWED_MAX + 1 + n_sinks.
class AcmpOwedProbe4 : public AcmpOwed {
 protected:
    std::vector<std::array<std::uint8_t, spec::FRAME_BYTES>> ring;
    void gated_pass() {
        fk.now += 1u;
        static_cast<void>(acmp_poll(&a));
        while (!ring.empty() && acmp_rx_ready(&a)) {
            EXPECT_TRUE(acmp_rx(&a, 0, ring.front().data(), ring.front().size())) << "ready means taken";
            ring.erase(ring.begin());
        }
        if (fk.armed[0] && static_cast<std::int32_t>(fk.now - fk.at[0]) >= 0) {
            acmp_timer_expired(&a, 0);
        }
    }
    void scenario(const char* label, std::uint8_t msg, std::uint8_t rsp, unsigned expiring) {
        SetUp();
        held.clear();
        ring.clear();
        cfg.n_sinks = ACMP_MAX_SINKS;
        for (unsigned k = 0; k < ACMP_MAX_SINKS; ++k) {
            cfg.sink_interface[k] = 0;
        }
        ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kEnv));
        fk.room = true;
        std::uint32_t first_deadline = 0;
        for (unsigned k = 2; k < 2 + expiring; ++k) {
            fk.now += 1u;
            bind(k, kTkB, static_cast<std::uint16_t>(k));
            while (acmp_poll(&a)) {
            }
            first_deadline = k == 2 ? a.sinks[k].timer_deadline : first_deadline;
        }
        if (expiring) {
            fk.now = first_deadline - kHoldMs - 1u;
        }
        fill(0x7D00);
        fk.clear();
        ring.push_back(acmpdu(command(msg, 1, kTkA, 1, kCtl1, 0, 0x7D08)));
        EXPECT_FALSE(acmp_rx_ready(&a));
        fk.now += kHoldMs;
        fk.room = true;
        const std::uint32_t released = fk.now;
        for (unsigned n = 0; n < 8u * ACMP_OWED_MAX && (a.owed_count != 0u || !ring.empty()); ++n) {
            gated_pass();
        }
        const Sent* s = answer(rsp, 0x7D08);
        ASSERT_TRUE(s != nullptr) << label;
        const unsigned pass_no = static_cast<unsigned>(s->at - released);
        std::printf("PROBE4 gated %s: expiring_probes=%u answer_pass=%u budget=%u within_budget=%d probes_lost=%u "
                    "probes_held=%u busy_declined=%u\n", label, expiring, pass_no,
                    ACMP_OWED_MAX + 1u + cfg.n_sinks, pass_no <= ACMP_OWED_MAX + 1u + cfg.n_sinks ? 1 : 0,
                    a.probes_lost, a.probes_held, a.busy_declined);
        EXPECT_LE(pass_no, ACMP_OWED_MAX + 1u + cfg.n_sinks);
    }
};

TEST_F(AcmpOwedProbe4, GatedPortBudget) {
    for (unsigned expiring : {0u, 1u, 4u, 14u}) {
        scenario("get_rx_state", spec::MSG_GET_RX_STATE_COMMAND, spec::MSG_GET_RX_STATE_RESPONSE, expiring);
        scenario("bind_rx", spec::MSG_BIND_RX_COMMAND, spec::MSG_BIND_RX_RESPONSE, expiring);
    }
}
