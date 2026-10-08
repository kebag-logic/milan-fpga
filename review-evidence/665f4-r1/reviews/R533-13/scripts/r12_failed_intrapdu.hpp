// R532-12 reviewer probe test (appended to a disposable copy of srp_feedback.hpp).
// The intra-PDU Lv-then-New guarantee, exercised for the Talker Failed kind:
// a settled Failed registration withdrawn and re-registered inside ONE PDU
// must still reprobe, exactly as the Advertise case in
// SinglePduWithdrawalThenRegistrationRetainsTheFirstEvent.
namespace {
TEST_F(SrpFeedback, R12FailedSinglePduWithdrawalThenRegistrationRetainsTheFirstEvent) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,true,0,k);
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        ASSERT_TRUE(core()->sinks[k].tk_failed);
        auto frame=talker(k,true,5), join=talker(k,true,0);
        frame.resize(frame.size()-2u);
        frame.insert(frame.end(),join.begin()+15,join.end());
        queue(k,frame); settle();
        reprobed(k);
    }
}
}  // namespace
// Both kinds registered for one StreamID (a New Failed does not replace a
// registered Advertise). One PDU withdraws Failed, then refreshes Advertise:
// Advertise was registered throughout, so this is a kind change, never a withdrawal.
namespace {
TEST_F(SrpFeedback, R12BothKindsFailedLeaveInsideOnePduIsNotAWithdrawal) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k); registration(k,true,0,k);
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        ASSERT_EQ(sink(k).registered_kinds,3u) << "both kinds registered";
        auto frame=talker(k,true,5), refresh=talker(k,false,1);
        frame.resize(frame.size()-2u);
        frame.insert(frame.end(),refresh.begin()+15,refresh.end());
        queue(k,frame); settle();
        EXPECT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK) << "continuous Advertise is not withdrawn";
        EXPECT_FALSE(core()->sinks[k].tk_failed) << "kind change reaches ACMP";
        EXPECT_TRUE(sink(k).bound);
        EXPECT_EQ(core()->impossible,0u);
    }
}
}  // namespace
// Advertise settled; one PDU: Failed JoinIn (atomic replacement), Failed Lv,
// Advertise JoinIn. The Failed registration is withdrawn mid-PDU, so the
// listener must reprobe even though Advertise returns before delivery.
namespace {
TEST_F(SrpFeedback, R12FailedReplacementWithdrawnInsideOnePduStillReprobes) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k);
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        auto frame=talker(k,true,1);
        for (const auto& next : {talker(k,true,5),talker(k,false,1)}) {
            frame.resize(frame.size()-2u);
            frame.insert(frame.end(),next.begin()+15,next.end());
        }
        queue(k,frame); settle();
        reprobed(k);
    }
}
}  // namespace
