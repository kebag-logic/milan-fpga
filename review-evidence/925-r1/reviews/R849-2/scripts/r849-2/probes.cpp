
// Reviewer probes for #925 round 3 (appended to a disposable copy of srp_mbx.cpp; never committed).
namespace {

// A withdrawal the receive filter's copy makes, followed in its MRPDU by a message that changes nothing (an unchanged
// Domain JoinIn, or a Talker of a StreamID no binding has): at an idle join timer the Listener Lv is on the wire
// within a JoinTime, as a replacement's declaration is.
TEST_F(SrpTalkerKinds, R8492WithdrawalBeforeAMessageThatChangesNothingIsSentWithinAJoinTime) {
    const auto domain=frame(4,{6,3,0,2},1);
    const auto ignored=mrpdu({{kAdvertise,kJoinIn,1}});
    for (unsigned kind : {kAdvertise,kFailed}) {
        for (const auto *trailer : {&domain,&ignored}) {
            settle(); advance(400); bind(0);
            expect_declared(record(kind,kJoinIn),0,kind,"the registration");
            idle();
            expect_declared(then(record(kind,kLv),*trailer),0,0u,"a Leave before a message that changes nothing");
            TearDown(); SetUp();
        }
    }
}

// The StreamID's only binding, replaced in place by one of another destination, then unbound while both kinds stay
// registered: the StreamID is held with its latest whatever that binding's destination, and its next binding of the
// registrations' destination declares the latest.
TEST_F(SrpTalkerKinds, R8492FinalUnbindingOfAnotherDestinationKeepsTheLatest) {
    for (unsigned latest : {kAdvertise,kFailed}) {
        settle(); advance(400); bind(0);
        offer(record(3u-latest,kJoinIn)); offer(record(latest,kNew)); advance(kJoinMs);
        ASSERT_EQ(sink(0).declared,latest);
        bind(0,0,1); advance(kJoinMs);
        ASSERT_EQ(sink(0).desired,0u);
        unbind(0); advance(kJoinMs);
        EXPECT_EQ(adapter.held_count,1u)<<"held whatever its last binding's destination";
        const uint32_t from=model.tx_sent;
        bind(0); advance(kJoinMs);
        EXPECT_EQ(sink(0).desired,latest)<<"the latest decides again";
        EXPECT_EQ(sink(0).declared,latest)<<"the latest decides again";
        EXPECT_EQ(sink(0).feedback_kind,latest)<<"ACMP sees the latest";
        for (const auto &d:listeners(from)) EXPECT_EQ(d.subtype,latest)<<"the latest on the wire";
        TearDown(); SetUp();
    }
}

// Two StreamIDs held on one interface, then its reset: every hold of that interface ends.
TEST_F(SrpTalkerKinds, R8492AResetEndsEveryHoldOfItsInterface) {
    settle(); advance(400); bind(0,0,0); bind(1,1,1);
    offer(mrpdu({{kFailed,kJoinIn,0}})); offer(mrpdu({{kAdvertise,kNew,0}}));
    offer(mrpdu({{kFailed,kJoinIn,1}})); offer(mrpdu({{kAdvertise,kNew,1}})); advance(kJoinMs);
    ASSERT_EQ(sink(0).declared,kAdvertise); ASSERT_EQ(sink(1).declared,kAdvertise);
    unbind(0); unbind(1); advance(kJoinMs);
    ASSERT_EQ(adapter.held_count,2u);
    mbx_model_set_link(&model,0,false); settle(); mbx_model_set_link(&model,0,true); settle(); advance(400);
    EXPECT_EQ(adapter.held_count,0u)<<"a reset ends every hold of its interface";
}

}  // namespace
