// Reviewer probe (disposable): appended to a scratch copy's sw/firmware/ctrl/test/test_mbx_dma_driver.cpp at head
// e7e2b744, then run with scripts/run_unit_arm.py <copy> <out>. Expected (correct) behaviour: after a move that ends in
// ERR, a frame off a word takes the word loop and starts no move, so its record is committed. At the head it fails.
namespace {
TEST_F(MbxDma, ProbeAWordLoopRecordAfterAFailedMoveIsCommitted) {
    const std::uint16_t head = 100;
    open(0, head);
    alignas(4) static std::uint8_t aligned[200];
    alignas(4) static std::uint8_t buffer[72];
    for (std::uint32_t i = 0; i < sizeof aligned; ++i) aligned[i] = pattern(i);
    for (std::uint32_t i = 0; i < sizeof buffer; ++i) buffer[i] = pattern(i);
    mover.memory = {{aligned, sizeof aligned}, {buffer, sizeof buffer}};
    mover.fail = true;
    ASSERT_EQ(mbx_tx_send(kCh, 0, aligned, sizeof aligned), MBX_STATUS_BAD) << "probe: the failed move is refused";
    EXPECT_EQ(mbx_tx_send(kCh, 0, buffer + 1, 61), MBX_STATUS_OK)
        << "probe: a word-loop record after a failed move is sent";
    EXPECT_EQ(at(unit::ch_reg(kCh, MBX_CH_REG_TX_HEAD)), static_cast<std::uint16_t>(head + MBX_TX_HDR_WORDS + 16u))
        << "probe: and committed at TX_HEAD";
    EXPECT_EQ(mbx_tx_send(kCh, 0, buffer + 1, 61), MBX_STATUS_OK)
        << "probe: and so is the next word-loop record";
}
}  // namespace
