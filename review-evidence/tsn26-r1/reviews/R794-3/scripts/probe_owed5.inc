// SPDX-License-Identifier: MIT
// Reviewer probe (written after reading the concurrent review's F3): answer times of commands the port keeps
// behind a first kept command, at the 191 ms hold the margin test calls documented. Appended inside the
// anonymous namespace of a disposable copy of tests/test_acmp.cpp; never part of the reviewed tree.
class AcmpOwedProbe5 : public AcmpOwed {
 protected:
    void kept(const char* label, std::uint8_t first, std::uint8_t first_rsp, std::uint32_t hold) {
        SetUp();
        held.clear();
        fk.room = true;
        fill(0x7900);
        fk.clear();
        const std::uint32_t arrival = fk.now;
        EXPECT_FALSE(deliver(command(first, 1, kTkA, 1, kCtl1, 0, 0x7908)));
        EXPECT_FALSE(deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 1, 0, 0, kCtl2, 0, 0x7909)));
        EXPECT_FALSE(deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, 0x790A)));
        fk.now += hold;
        fk.room = true;
        drain();
        const Sent* a1 = answer(first_rsp, 0x7908);
        const Sent* a2 = answer(spec::MSG_GET_RX_STATE_RESPONSE, 0x7909);
        const Sent* a3 = answer(spec::MSG_GET_RX_STATE_RESPONSE, 0x790A);
        ASSERT_TRUE(a1 && a2 && a3);
        std::printf("PROBE5 %s hold_ms=%u: first answer_ms=%u, 2nd kept answer_ms=%u, 3rd kept answer_ms=%u "
                    "(timeout 200)\n", label, static_cast<unsigned>(hold), static_cast<unsigned>(a1->at - arrival),
                    static_cast<unsigned>(a2->at - arrival), static_cast<unsigned>(a3->at - arrival));
    }
};

TEST_F(AcmpOwedProbe5, CommandsKeptBehindTheFirst) {
    const std::uint32_t margin = kCommandTimeoutMs - (ACMP_OWED_MAX + 1u);
    kept("BIND_RX then two GET_RX_STATE", spec::MSG_BIND_RX_COMMAND, spec::MSG_BIND_RX_RESPONSE, margin);
    kept("three GET_RX_STATE", spec::MSG_GET_RX_STATE_COMMAND, spec::MSG_GET_RX_STATE_RESPONSE, margin);
}
