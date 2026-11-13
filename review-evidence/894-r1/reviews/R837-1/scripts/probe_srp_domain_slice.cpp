
// Reviewer probe (appended to a disposable copy of srp_mbx.cpp; never committed).
// A Domain adoption that moves the VID, with a Talker licensed, built whole (most 2) and
// sliced (most 1, CTRL_LOOP_BUILD_MOST at two interfaces): counts the licence changes the
// adapter reports and whether a slice boundary leaves the adopted VID unsent.
namespace {
ctrl_transmit_fn probe_whole;
unsigned probe_most;
bool probe_gap_unsent;  // a slice ended with a resume owed and interface 0's VLAN unsent
bool probe_poll_unsent; // and SRP's poll ran in that gap
ctrl_poll_fn probe_poll_fn;
bool probe_poll(void *ctx) {
    auto *m = static_cast<srp_mbx *>(ctx);
    if (m->tx_resume != 0u && !m->ifs[0].vlan_sent) probe_poll_unsent = true;
    return probe_poll_fn(ctx);
}
void probe_transmit(void *ctx, unsigned) {
    probe_whole(ctx, probe_most);
    auto *m = static_cast<srp_mbx *>(ctx);
    if (m->tx_resume != 0u && !m->ifs[0].vlan_sent) probe_gap_unsent = true;
}
}

TEST_F(Srp, ProbeReviewerDomainAdoptionAcrossSlices) {
    unsigned falses[3] = {0, 0, 0}, trues[3] = {0, 0, 0};
    bool gap[3] = {false, false, false}, polled[3] = {false, false, false};
    for (unsigned most : {2u, 1u}) {
        TearDown();
        SetUp();
        probe_whole = loop.transmit;
        probe_most = most;
        probe_gap_unsent = false;
        probe_poll_unsent = false;
        loop.transmit = probe_transmit;
        for (unsigned k = 0; k < loop.n_polls; ++k) {
            if (loop.polls[k].ctx == &adapter) { probe_poll_fn = loop.polls[k].fn; loop.polls[k].fn = probe_poll; }
        }
        settle();
        EXPECT_CALL(licence, Change(0, 0, true));
        offer(frame(3, identity(0), 1, 2), 0);
        ASSERT_TRUE(::testing::Mock::VerifyAndClearExpectations(&licence));
        EXPECT_CALL(licence, Change(::testing::_, ::testing::_, false))
            .WillRepeatedly([&, most](unsigned, unsigned, bool) { ++falses[most]; });
        EXPECT_CALL(licence, Change(::testing::_, ::testing::_, true))
            .WillRepeatedly([&, most](unsigned, unsigned, bool) { ++trues[most]; });
        offer(frame(4, {6, 4, 0, 3}, 0));
        advance(400);
        gap[most] = probe_gap_unsent;
        polled[most] = probe_poll_unsent;
        EXPECT_EQ(adapter.ifs[0].domain.vid, 3u) << "(the Domain was adopted)";
        ::testing::Mock::VerifyAndClearExpectations(&licence);
        EXPECT_CALL(licence, Change(::testing::_, ::testing::_, ::testing::_)).Times(::testing::AnyNumber());
        loop.transmit = probe_whole;
    }
    std::printf("PROBE MBX_N_IF=%u whole(most=2): revoked=%u granted=%u gap=%d polled=%d | sliced(most=1): revoked=%u granted=%u gap=%d polled=%d\n",
                (unsigned)MBX_N_IF, falses[2], trues[2], (int)gap[2], (int)polled[2], falses[1], trues[1], (int)gap[1], (int)polled[1]);
    EXPECT_EQ(falses[1], falses[2]) << "a sliced build revokes the licence as often as the build made whole";
    EXPECT_FALSE(gap[1]) << "no slice boundary stands between the adoption and its MVRP commit";
}
