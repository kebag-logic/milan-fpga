// Reviewer probes for early registration retention; includes unchanged test fixtures.

namespace {
// A single legal Talker vector: successive StreamIDs and destinations,
// packed JoinIn events, with correct list length and both EndMarks.
std::vector<uint8_t> review_batch(std::vector<uint8_t> f, unsigned count) {
    f.resize(46u);
    wire_put_be(f.data()+19,count,2);
    wire_put_be(f.data()+17,29u+(count+2u)/3u,2);
    for (unsigned k=0;k<count;k+=3u) {
        f.push_back(static_cast<uint8_t>(36u+(k+1u<count ? 6u : 0u)+(k+2u<count ? 1u : 0u)));
    }
    f.insert(f.end(),{0,0,0,0});
    return f;
}
TEST_F(SrpEarlyTalker, ReviewFreshFullBatchControl) {
    settle(); advance(400);
    offer(review_batch(talker(0,kAdvertise,kJoinIn),CTRL_SRP_SINKS)); quiet(400);
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k)
        expect_bound_declares(k,k,kAdvertise,"fresh registrar accepts the full vector");
}
TEST_F(SrpEarlyTalker, ReviewResetRestoresFullAdmissionCapacity) {
    settle(); advance(400);
    offer(talker(0xe0u,kAdvertise,kJoinIn));
    ASSERT_EQ(adapter.kept_count[0],1u);
    mbx_model_set_link(&model,0,false); settle();
    mbx_model_set_link(&model,0,true); settle(); advance(400);
    auto batch=review_batch(talker(0,kAdvertise,kJoinIn),CTRL_SRP_SINKS);
    offer(batch); quiet(400);
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k)
        expect_bound_declares(k,k,kAdvertise,"after reset, the first full batch fits the empty registrar");
}
TEST_F(SrpEarlyTalker, ReviewFreedBelowBoundRestoresFullAdmissionCapacity) {
    settle(); advance(400);
    offer(talker(0xe0u,kAdvertise,kJoinIn));
    offer(talker(0xe0u,kAdvertise,kLv));
    quiet(400);
    auto batch=review_batch(talker(0,kAdvertise,kJoinIn),CTRL_SRP_SINKS);
    offer(batch); quiet(400);
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k)
        expect_bound_declares(k,k,kAdvertise,"after reclaim, the first full batch fits the empty registrar");
}
TEST_F(SrpEarlyTalker, ReviewUnboundFloodDoesNotStarveBoundInputs) {
    settle(); advance(400);
    const auto before=ctrl_pool_in_use(&pool);
    const auto refused=adapter.refused;
    const auto walks=adapter.walks;
    for (unsigned k=0;k<1000;++k) { offer(talker(0x40u+(k%128u),kAdvertise,kJoinIn)); advance(2); }
    EXPECT_LE(ctrl_pool_in_use(&pool),before+CTRL_SRP_SINKS);
    EXPECT_EQ(adapter.refused,refused);
    EXPECT_EQ(adapter.walks,walks)<<"unbound registrations owe no snapshot walk";
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) {
        bind_stream(k,k); settle();
        offer(talker(k,kAdvertise,kJoinIn)); advance(kJoinMs);
        EXPECT_EQ(sink(k).declared,kAdvertise)<<"flood does not starve input "<<k;
    }
}
TEST_F(SrpEarlyTalker, ReviewUnbindRebindControlEveryInput) {
    settle(); advance(400);
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) {
        bind_stream(k,k); settle();
        offer(talker(k,kAdvertise,kJoinIn)); advance(kJoinMs);
        ASSERT_EQ(sink(k).declared,kAdvertise);
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,k,nullptr,nullptr,0)); settle(); advance(kJoinMs);
        expect_bound_declares(k,k,kAdvertise,"UNBIND_RX/BIND_RX adapter control on every input");
    }
}
}
