// Reviewer probes (#956, #957), appended to a disposable copy of sw/firmware/ctrl/test/srp_talker.cpp after the
// prior reviewers' probes; never part of the reviewed tree.

// P1 (#957 F1's cause): a reset destroys the Listener registrations; no licence opens again on the interface without
// a Listener registering there after the reset, and none of the reset's clears leave the source counted registered.
TEST_F(Talker, R875P1NoLicenceWithoutAListenerAfterAReset) {
    settle(); gate(1u,kBaseA); advance(400);
    const unsigned i=MBX_N_IF-1u;
    EXPECT_CALL(licence,Change(::testing::_,::testing::_,::testing::_)).Times(::testing::AnyNumber());
    offer(frame(3,identity(i,0),1,2),i); advance(400);
    ASSERT_TRUE(adapter.ifs[i].active[0]) << "(the source is licensed with its Listener Ready)";
    ASSERT_TRUE(::testing::Mock::VerifyAndClearExpectations(&licence));
    EXPECT_CALL(licence,Change(::testing::_,::testing::_,::testing::_)).Times(::testing::AnyNumber());
    EXPECT_CALL(licence,Change(i,0,true)).Times(0);
    mbx_model_set_link(&model,i,false); settle();
    mbx_model_set_link(&model,i,true); settle();
    advance(3000);
    printf("PROBE P1 if%u after reset: active %d registered %d listener_present %d declaration %u\n",i,
           int(adapter.ifs[i].active[0]),int(adapter.ifs[i].registered[0]),int(adapter.ifs[i].listener_present[0]),
           unsigned(adapter.ifs[i].declaration[0]));
    EXPECT_FALSE(adapter.ifs[i].active[0]) << "PROBE P1: no licence without a Listener after the reset";
    EXPECT_FALSE(adapter.ifs[i].listener_present[0]);
    EXPECT_EQ(adapter.ifs[i].declaration[0],0u);
}

// P2 (#957): behind a closed gate after a reset a registration notices nothing, equal declaration or not.
TEST_F(Talker, R875P2ClosedGateAfterAResetIsSilent) {
    EXPECT_CALL(licence,Change(::testing::_,::testing::_,::testing::_)).Times(::testing::AnyNumber());
    settle(); gate(1u,kBaseA); advance(400);
    const unsigned i=0;
    offer(frame(3,identity(i,0),1,2),i); advance(20);
    adapter.ifs[i].noticed=0u;
    gate(0u,kBaseA); settle();
    mbx_model_set_link(&model,i,false); settle();
    mbx_model_set_link(&model,i,true); settle(); advance(400);
    adapter.ifs[i].noticed=0u;
    for (unsigned d=1u;d<=3u;++d) {
        offer(frame(3,identity(i,0),1,d),i); advance(20);
        printf("PROBE P2 closed gate declaration %u: noticed %u\n",d,unsigned(adapter.ifs[i].noticed));
        EXPECT_EQ(adapter.ifs[i].noticed&1u,0u) << "PROBE P2: a closed gate notices nothing";
    }
}

// P3 (#956): a reset of the interface whose build is paused between slices, and (two interfaces) of the other one,
// wedges nothing: the build ends, the poll and THE TRANSMIT's due settle, and the interfaces send again.
TEST_F(Talker, R875P3ResetBetweenSlicesWedgesNothing) {
    EXPECT_CALL(licence,Change(::testing::_,::testing::_,::testing::_)).Times(::testing::AnyNumber());
    for (unsigned victim=0;victim<MBX_N_IF;++victim) {
        settle(); gate(1u,kBaseA); advance(400);
        for (unsigned k=0;k<2000u && adapter.tx_owed!=0u;++k) advance(1);
        adapter.tx_due=1u;
        loop.transmit(loop.transmit_ctx,1u);
        ASSERT_NE(adapter.tx_resume,0u) << "(interface 0's build paused)";
        mbx_model_set_link(&model,victim,false);
        mbx_model_set_link(&model,victim,true);
        settle();
        advance(3000);
        const uint32_t before=model.tx_sent;
        advance(12000);
        printf("PROBE P3 victim if%u: tx_owed %u reentries %u frames in 12 s %u\n",victim,unsigned(adapter.tx_owed),
               unsigned(adapter.reentries),unsigned(model.tx_sent-before));
        EXPECT_EQ(adapter.reentries,0u);
        EXPECT_GE(model.tx_sent-before,MBX_N_IF*2u) << "PROBE P3: every interface sends again";
        for (unsigned k=0;k<2000u && adapter.tx_owed!=0u;++k) advance(1);
        EXPECT_EQ(adapter.tx_owed,0u) << "PROBE P3: THE TRANSMIT settles";
    }
}

// P4 (#956): the request off a centisecond (tick_div 1..9), the loop held from the tick that ends the count as the
// shipped latest-case test holds it: on the wire no later than 30,000 ms and no sooner than 29,000 ms after it.
class R875P4 : public Talker, public ::testing::WithParamInterface<std::tuple<unsigned,unsigned>> {};
TEST_P(R875P4, OffCentisecondRequest) {
    const unsigned phase=std::get<0>(GetParam());
    const unsigned sub=std::get<1>(GetParam());
    settle(); gate(1u,kBaseA); advance(phase);
    while (model.tick_div!=sub) advance(1);
    trace();
    const uint32_t first=model.tx_sent;
    const uint32_t at=model.now_ms;
    gate(0u,kBaseA); settle();
    advance(2000);
    gate(1u,kBaseB);
    advance_to(at+kHoldOffMs-100u);
    for (unsigned k=0;k<1000u && adapter.held_cs[0]>1u;++k) advance_to(model.now_ms+1u);
    while (model.tick_div!=9u) advance(1);
    mbx_model_advance_ms(&model,1u+kLatestMs);
    settle();
    advance(1500);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,0,first);
        const auto *lv=leave(ds,1);
        ASSERT_NE(lv,nullptr);
        const auto *adv=declared(ds,1,lv->time_ms+1u);
        ASSERT_NE(adv,nullptr);
        printf("PROBE P4 phase %u sub %u if%u: request-to-wire %u ms\n",phase,sub,i,unsigned(adv->time_ms-at));
        EXPECT_EQ(dest(*adv),kBaseB);
        EXPECT_LE(adv->time_ms,at+kTwoLongestLeaveAllMs) << "PROBE P4: within 30.0 s";
        EXPECT_GE(adv->time_ms,at+29000u) << "PROBE P4: no sooner than 29 s";
    }
}
INSTANTIATE_TEST_SUITE_P(R875, R875P4, ::testing::Combine(::testing::Values(300u,340u,370u,700u),
                                                         ::testing::Values(1u,5u,9u)));
