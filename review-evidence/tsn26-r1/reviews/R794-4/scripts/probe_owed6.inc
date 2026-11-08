// SPDX-License-Identifier: MIT
// Reviewer probe: the answer pass of kept commands when the egress returns with seven frames owed, the
// only other count at which a command (a BIND_RX) is kept. PORTING states pass ACMP_OWED_MAX + 1 + f + r.
// Appended inside the anonymous namespace of a disposable copy of tests/test_acmp.cpp; never part of the
// reviewed tree.
class AcmpOwedProbe6 : public AcmpOwed {
 protected:
    void seven(const char* label, bool bind_first, std::uint32_t hold) {
        SetUp();
        sinks_on_one_interface(3u);
        fk.room = false;
        unsigned gets = bind_first ? 5u : 7u;
        for (unsigned k = 0; k < gets; ++k) {
            rx(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, static_cast<std::uint16_t>(0x7B00 + k)));
        }
        if (bind_first) {
            EXPECT_TRUE(deliver(command(spec::MSG_BIND_RX_COMMAND, 0, kTkB, 0, kCtl1, 0, 0x7B05)))
                << "a BIND_RX with two free owed slots is taken";
        }
        ASSERT_EQ(a.owed_count, ACMP_OWED_MAX - 1u);
        fk.clear();
        const std::uint32_t arrival_ms = fk.now;
        EXPECT_FALSE(deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7B08)));
        EXPECT_FALSE(deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 1, 0, 0, kCtl2, 0, 0x7B09)));
        EXPECT_FALSE(deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 2, 0, 0, kCtl2, 0, 0x7B0A)));
        const bool waiting = a.bind_waiting;
        const unsigned owed_at_return = a.owed_count;
        fk.now += hold;
        fk.room = true;
        const std::uint32_t rel = fk.now;
        drain();
        const Sent* b = answer(spec::MSG_BIND_RX_RESPONSE, 0x7B08);
        const Sent* g1 = answer(spec::MSG_GET_RX_STATE_RESPONSE, 0x7B09);
        const Sent* g2 = answer(spec::MSG_GET_RX_STATE_RESPONSE, 0x7B0A);
        ASSERT_TRUE(b && g1 && g2);
        std::printf("PROBE6 %s: owed_at_return=%u bind_waiting=%d hold_ms=%u | kept BIND_RX pass=%u (stated %u) "
                    "answer_ms=%u | GET behind pass=%u (stated %u) answer_ms=%u | 2nd GET behind pass=%u (stated %u) "
                    "answer_ms=%u | probes_lost=%u busy_declined=%u\n",
                    label, owed_at_return, waiting ? 1 : 0, static_cast<unsigned>(hold),
                    static_cast<unsigned>(b->at - rel), ACMP_OWED_MAX + 1u, static_cast<unsigned>(b->at - arrival_ms),
                    static_cast<unsigned>(g1->at - rel), ACMP_OWED_MAX + 1u + 2u, static_cast<unsigned>(g1->at - arrival_ms),
                    static_cast<unsigned>(g2->at - rel), ACMP_OWED_MAX + 1u + 3u, static_cast<unsigned>(g2->at - arrival_ms),
                    static_cast<unsigned>(a.probes_lost), static_cast<unsigned>(a.busy_declined));
    }
    void eight(std::uint32_t hold) {
        SetUp();
        sinks_on_one_interface(3u);
        fill(0x7B00);
        fk.clear();
        const std::uint32_t arrival_ms = fk.now;
        EXPECT_FALSE(deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7B08)));
        EXPECT_FALSE(deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 1, 0, 0, kCtl2, 0, 0x7B09)));
        EXPECT_FALSE(deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 2, 0, 0, kCtl2, 0, 0x7B0A)));
        fk.now += hold;
        fk.room = true;
        const std::uint32_t rel = fk.now;
        drain();
        const Sent* b = answer(spec::MSG_BIND_RX_RESPONSE, 0x7B08);
        const Sent* g1 = answer(spec::MSG_GET_RX_STATE_RESPONSE, 0x7B09);
        const Sent* g2 = answer(spec::MSG_GET_RX_STATE_RESPONSE, 0x7B0A);
        ASSERT_TRUE(b && g1 && g2);
        std::printf("PROBE6 control, eight owed: hold_ms=%u | kept BIND_RX pass=%u answer_ms=%u | GET behind pass=%u "
                    "answer_ms=%u | 2nd GET behind pass=%u answer_ms=%u\n", static_cast<unsigned>(hold),
                    static_cast<unsigned>(b->at - rel), static_cast<unsigned>(b->at - arrival_ms),
                    static_cast<unsigned>(g1->at - rel), static_cast<unsigned>(g1->at - arrival_ms),
                    static_cast<unsigned>(g2->at - rel), static_cast<unsigned>(g2->at - arrival_ms));
    }
};

TEST_F(AcmpOwedProbe6, EgressReturnsWithSevenOwed) {
    const std::uint32_t q3 = 193u - 2u * 3u;   // PORTING budget for Q = 3 kept commands, 1 ms passes
    eight(q3);
    seven("seven GET_RX_STATE owed, BIND_RX declined at one free slot", false, q3);
    seven("five owed plus a taken BIND_RX, second BIND_RX declined at one free slot", true, q3);
}
