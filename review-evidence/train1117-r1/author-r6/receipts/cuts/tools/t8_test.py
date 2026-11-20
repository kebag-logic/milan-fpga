"""t8_test.py TREE: the DMA driver's T8 in TREE's test_mbx_dma_driver.cpp (attempt 2's inline commit): a record the
word loop wrote, left uncommitted, is committed by the next mbx_tx_begin judging no move, an earlier move's ERR held."""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / 'sw/firmware/ctrl/test/test_mbx_dma_driver.cpp'; t = p.read_text()
test = '''
TEST_F(MbxDma, T8ARecordTheWordLoopWroteIsCommittedByTheNextBeginJudgingNoMove) {
    const std::uint16_t head = 100;
    open(0, head);
    alignas(4) static std::uint8_t frame[200];
    alignas(4) static std::uint8_t buffer[72];
    for (std::uint32_t i = 0; i < sizeof frame; ++i) frame[i] = pattern(i);
    for (std::uint32_t i = 0; i < sizeof buffer; ++i) buffer[i] = pattern(i + 5u);
    const std::uint8_t* off = buffer + 1;
    const std::uint16_t len = 61, record = MBX_TX_HDR_WORDS + 16u;
    mover.memory = {{frame, sizeof frame}, {buffer, sizeof buffer}};
    mover.fail = true;
    ASSERT_EQ(mbx_tx_send(kCh, 0, frame, sizeof frame), MBX_STATUS_BAD) << "T8 a move that ends in ERR is refused";
    ASSERT_EQ(ctrl_test_dma[kStatus], kErr) << "T8 the mover holds its ERR until its next start";
    mover.fail = false;
    ASSERT_EQ(mbx_tx_begin(kCh, 0, off, len), MBX_STATUS_OK) << "T8 a frame off a word is begun by the word loop";
    EXPECT_EQ(at(unit::ch_reg(kCh, MBX_CH_REG_TX_HEAD)), head) << "T8 and not yet committed";
    EXPECT_EQ(mbx_tx_begin(kCh, 0, frame, sizeof frame), MBX_STATUS_OK)
        << "T8 the next begin commits the word loop's record, judging no move: the earlier ERR is not its";
    EXPECT_EQ(at(unit::ch_reg(kCh, MBX_CH_REG_TX_HEAD)), head + record) << "T8 the word loop's record at TX_HEAD";
    bool same = true;
    for (std::uint32_t k = 0; k < (len + 3u) / 4u; ++k) same = same && tx_ring(head + MBX_TX_HDR_WORDS + k) == lanes(off, len, k);
    EXPECT_TRUE(same) << "T8 the ring holds its words";
    EXPECT_TRUE(mbx_tx_commit(kCh)) << "T8 the moved frame after it is committed by its own commit";
    EXPECT_EQ(at(unit::ch_reg(kCh, MBX_CH_REG_TX_HEAD)), head + record + MBX_TX_HDR_WORDS + sizeof frame / 4u)
        << "T8 at TX_HEAD";
}
'''
anchor = 'TEST_F(MbxDma, T7AFullCompletionQueueRefusesOnlyOnceTheLastFrameIsCommitted) {'
i = t.index(anchor); j = t.index('\n}\n', i) + 3
t = t[:j] + test + t[j:]
p.write_text(t)
print('T8 added')
