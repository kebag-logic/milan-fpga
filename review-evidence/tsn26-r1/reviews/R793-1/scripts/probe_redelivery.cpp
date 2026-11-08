// SPDX-License-Identifier: MIT
// Reviewer probe (disposable): appended inside the test namespace of a copy of tests/test_acmp.cpp.
// BIND_RX and GET_TX_STATE are declined behind the full owed set, then delivered again by the
// AcmpOwed port model; each must get its specified answer within 200 ms and in arrival order.
TEST_F(AcmpOwed, ProbeBindRxAndGetTxStateServedAfterRedelivery) {
    fill(0x7700);
    fk.clear();
    const std::uint32_t arrival = fk.now;
    Pdu b = command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7708);
    EXPECT_FALSE(deliver(b)) << "probe: BIND_RX declined";
    Pdu t;
    t.msg = spec::MSG_GET_TX_STATE_COMMAND;
    t.talker = kOwn;
    t.controller = kCtl2;
    t.seq = 0x7709;
    EXPECT_FALSE(deliver(t)) << "probe: GET_TX_STATE waits behind it";
    EXPECT_TRUE(fk.calls.empty() && a.sinks[1].state == ACMP_UNBOUND) << "probe: nothing acted";
    release_after_hold();
    ASSERT_TRUE(held.empty() && a.owed_count == 0u) << "probe: all taken and drained";
    const Sent* br = answer(spec::MSG_BIND_RX_RESPONSE, 0x7708);
    const Sent* tr = answer(spec::MSG_GET_TX_STATE_RESPONSE, 0x7709);
    ASSERT_TRUE(br != nullptr && tr != nullptr) << "probe: both answered";
    EXPECT_EQ(read(br->bytes.data()).status, spec::STATUS_SUCCESS) << "probe: BIND_RX success";
    EXPECT_EQ(read(tr->bytes.data()).status, spec::STATUS_SUCCESS) << "probe: GET_TX_STATE success";
    EXPECT_LE(br->at - arrival, 200u) << "probe: BIND_RX within 200 ms";
    EXPECT_LE(tr->at - arrival, 200u) << "probe: GET_TX_STATE within 200 ms";
    EXPECT_LT(br->at, tr->at) << "probe: arrival order kept";
    EXPECT_TRUE(a.sinks[1].bound) << "probe: bound once taken";
    std::printf("PROBE bind_at=%u get_tx_at=%u probes_lost=%u busy_declined=%u sent=%zu state=%d\n",
                static_cast<unsigned>(br->at - arrival), static_cast<unsigned>(tr->at - arrival),
                static_cast<unsigned>(a.probes_lost), static_cast<unsigned>(a.busy_declined), fk.sent.size(),
                static_cast<int>(a.sinks[1].state));
}
