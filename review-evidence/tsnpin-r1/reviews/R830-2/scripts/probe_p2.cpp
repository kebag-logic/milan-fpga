// Reviewer probe P2 (disposable; inserted into a scratch copy of test_acmp_mbx.cpp before its closing
// namespace). acmp_mbx.h THE KEPT COMMAND: after a poll that sends an owed frame the adapter offers the kept
// record, then the waiting records "each until acmp_rx declines one, which it keeps". With the owed set full
// and THREE commands behind it (one kept, two in the ring), the redelivery that frees one slot must stop at
// the second command's decline, so the third stays in the ring and every command is answered once, in
// arrival order. K1 has only two commands, so nothing waits behind the decline there.
TEST_F(AcmpMailbox, ProbeP2RedeliveryStopsAtTheDeclineAndLosesNoCommand) {
    fill_owed();
    const unsigned i = acfg.sink_interface[1];
    for (std::uint16_t s : {0x7101, 0x7102, 0x7103}) {
        ASSERT_TRUE(offer(command(spec::MSG_GET_RX_STATE_COMMAND, 1, kCtl1, s), spec::MULTICAST_MAC, i));
    }
    for (unsigned p = 0; p < 20u; ++p) {
        static_cast<void>(pass());
    }
    ASSERT_NE(app.acmp.kept.len, 0u);
    mbx_model_tx_pause(&model, false);
    std::uint32_t base = model.tx_sent;
    std::vector<std::uint16_t> order;
    for (unsigned p = 1; p <= ACMP_MBX_KEPT_PASSES + 8u; ++p) {
        static_cast<void>(pass());
        for (std::uint32_t j = base; j < model.tx_sent; ++j) {
            order.push_back(wire(j).seq);
        }
        base = model.tx_sent;
    }
    std::vector<std::uint16_t> expected;
    for (unsigned j = 0; j < ACMP_OWED_MAX; ++j) {
        expected.push_back(static_cast<std::uint16_t>(0x6000u + j));
    }
    for (std::uint16_t s : {0x7101, 0x7102, 0x7103}) {
        expected.push_back(s);
    }
    std::printf("P2 order:");
    for (auto s : order) {
        std::printf(" %04x", s);
    }
    std::printf("\n");
    EXPECT_EQ(order, expected) << "P2 every command behind the full owed set answered once, in arrival order";
    EXPECT_TRUE(app.acmp.kept.len == 0u && core()->owed_count == 0u) << "P2 nothing kept or owed after";
}
