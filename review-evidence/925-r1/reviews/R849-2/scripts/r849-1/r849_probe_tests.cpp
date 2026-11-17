// Reviewer probe scenarios for #925 (appended to a disposable copy of srp_mbx.cpp; never committed).
// Each drives the real adapter and lwSRP through the SrpTalkerKinds fixture and checks the binding's
// Listener declaration, the Listener declarations on the wire, and the copied registration kinds.
#include <cstdio>
namespace {
class R849Probe : public SrpTalkerKinds {
protected:
    static constexpr unsigned kJoinMt=3u;
    // every Listener declaration of stream 0 sent from `from` on: none withdraws and every one is `subtype`
    void expect_wire_only(uint32_t from, unsigned subtype, const char *words) {
        for (const auto &d:listeners(from)) {
            EXPECT_NE(d.event,kLv)<<words<<": no withdrawal on the wire";
            EXPECT_EQ(d.subtype,subtype)<<words<<": no other declaration on the wire";
        }
    }
};

// P1: Failed, Advertise New (Ready), then the talker's next MRPDU carries the Advertise as JoinIn: lwSRP
// replaces the Failed; the declaration stays Ready with no flap on the wire.
TEST_F(R849Probe, P1AdvertiseJoinInAfterNewKeepsReadyWithoutFlap) {
    settle(); advance(400); bind(0);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"P1 first Failed");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"P1 Advertise New");
    const uint32_t from=model.tx_sent;
    offer(record(kAdvertise,kJoinIn)); advance(3u*kJoinMs);
    EXPECT_EQ(sink(0).registered_kinds,kAdvertise)<<"P1 the JoinIn replaced the Failed";
    EXPECT_EQ(sink(0).desired,kAdvertise);
    EXPECT_EQ(sink(0).declared,kAdvertise);
    EXPECT_FALSE(sink(0).withdrawn);
    expect_wire_only(from,kAdvertise,"P1");
}

// P2: the mirror: Advertise, Failed New (AskingFailed), Failed JoinIn replaces the Advertise; stays AskingFailed.
TEST_F(R849Probe, P2FailedJoinInAfterNewKeepsAskingFailedWithoutFlap) {
    settle(); advance(400); bind(0);
    expect_declared(record(kAdvertise,kJoinIn),0,kAdvertise,"P2 first Advertise");
    expect_declared(record(kFailed,kNew),0,kFailed,"P2 Failed New");
    const uint32_t from=model.tx_sent;
    offer(record(kFailed,kJoinIn)); advance(3u*kJoinMs);
    EXPECT_EQ(sink(0).registered_kinds,kFailed);
    EXPECT_EQ(sink(0).desired,kFailed);
    EXPECT_EQ(sink(0).declared,kFailed);
    EXPECT_FALSE(sink(0).withdrawn);
    expect_wire_only(from,kFailed,"P2");
}

// P3: a flapping talker: each New in turn decides while both stay registered.
TEST_F(R849Probe, P3EachNewInTurnDecides) {
    settle(); advance(400); bind(0);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"P3 Failed");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"P3 Advertise New");
    expect_declared(record(kFailed,kNew),0,kFailed,"P3 Failed New again");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"P3 Advertise New again");
    EXPECT_EQ(sink(0).registered_kinds,3u);
}

// P4: both registered with Advertise latest; the talker reverts with a Failed JoinIn: lwSRP replaces the
// Advertise and the Failed's registrar sees no Join! indication, so the stale latest must not keep Ready.
TEST_F(R849Probe, P4FailedJoinInRevertsAnAdvertiseLatest) {
    settle(); advance(400); bind(0);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"P4 Failed");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"P4 Advertise New");
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"P4 Failed JoinIn reverts");
    EXPECT_EQ(sink(0).registered_kinds,kFailed);
}

// P5: Advertise JoinMt over a registered Failed replaces it at once (35.2.6).
TEST_F(R849Probe, P5AdvertiseJoinMtReplacesFailed) {
    settle(); advance(400); bind(0);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"P5 Failed");
    expect_declared(record(kAdvertise,kJoinMt),0,kAdvertise,"P5 Advertise JoinMt");
    EXPECT_EQ(sink(0).registered_kinds,kAdvertise);
}

// P6: both registered, Advertise latest; the older Failed's Leave (rapid leave) changes nothing on the wire.
TEST_F(R849Probe, P6OlderFailedLeaveIsQuiet) {
    settle(); advance(400); bind(0);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"P6 Failed");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"P6 Advertise New");
    const uint32_t from=model.tx_sent;
    offer(record(kFailed,kLv)); advance(3u*kJoinMs);
    EXPECT_EQ(sink(0).registered_kinds,kAdvertise);
    EXPECT_EQ(sink(0).declared,kAdvertise);
    EXPECT_FALSE(sink(0).withdrawn);
    expect_wire_only(from,kAdvertise,"P6");
}

// P7: one MRPDU {Advertise New, Failed JoinIn}: the JoinIn replaces the New's Advertise, so Failed decides,
// and no Ready reaches the wire.
TEST_F(R849Probe, P7NewThenReplacingJoinInInOneMrpdu) {
    settle(); advance(400); bind(0);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"P7 Failed");
    const uint32_t from=model.tx_sent;
    offer(mrpdu({{kAdvertise,kNew,0},{kFailed,kJoinIn,0}})); advance(3u*kJoinMs);
    EXPECT_EQ(sink(0).registered_kinds,kFailed);
    EXPECT_EQ(sink(0).desired,kFailed);
    EXPECT_EQ(sink(0).declared,kFailed);
    expect_wire_only(from,kFailed,"P7");
}

// P8: two bindings of one StreamID and destination, bound before the registrations: both follow the latest,
// and the one shared Listener declaration is Ready, not ReadyFailed.
TEST_F(R849Probe, P8TwoBindingsBeforeRegistrationsShareTheLatest) {
    settle(); advance(400); bind(0); bind(1);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"P8 Failed");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"P8 Advertise New");
    EXPECT_EQ(sink(1).desired,kAdvertise);
    EXPECT_EQ(sink(1).declared,kAdvertise);
    EXPECT_EQ(sink(0).latest_kind,sink(1).latest_kind);
}

// P9: the latest leaves, then registers New again over the remaining older one: it decides again.
TEST_F(R849Probe, P9LatestLeavesAndReturns) {
    settle(); advance(400); bind(0);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"P9 Failed");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"P9 Advertise New");
    expect_declared(record(kAdvertise,kLv),0,kFailed,"P9 Advertise leaves: Failed decides");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"P9 Advertise New again");
}

// P10: binding replaced in place by the same StreamID to another destination keeps the latest it held.
TEST_F(R849Probe, P10RebindInPlaceKeepsLatest) {
    settle(); advance(400); bind(0);
    offer(record(kFailed,kJoinIn)); offer(record(kAdvertise,kNew)); advance(kJoinMs);
    ASSERT_EQ(sink(0).desired,kAdvertise);
    bind(0,0,1); advance(kJoinMs);
    EXPECT_EQ(sink(0).latest_kind,kAdvertise)<<"P10 the replacement carries the StreamID's latest";
    bind(0,0,0); advance(kJoinMs);
    EXPECT_EQ(sink(0).desired,kAdvertise)<<"P10 back to the registered destination: Ready";
}
// P11 (observation, prints and does not assert): a stream VID other than the Domain's. The Failed is declared
// AskingFailed; then an Advertise arrives, as New (#925's path) or as JoinIn (the replacement path the base had).
// The Listener events on the wire after it are printed, to see whether Ready waits for the VLAN membership.
TEST_F(R849Probe, P11NonDomainVidObservation) {
    for (unsigned path : {kNew,kJoinIn}) {
        settle(); advance(400);
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid[0],da[0],3)); settle();
        auto adv=talker_value(sid[0],da[0],3);
        auto fail=adv; fail.resize(34); fail[33]=1;
        offer(frame(2,fail,kJoinIn)); advance(kJoinMs);
        EXPECT_EQ(sink(0).declared,kFailed)<<"P11 the Failed is declared AskingFailed";
        const uint32_t from=model.tx_sent; const unsigned start=model.now_ms;
        offer(frame(1,adv,path)); advance(3u*kJoinMs);
        std::printf("P11 path=%s desired=%u declared=%u kinds=%u:", path==kNew ? "New" : "JoinIn",
                    sink(0).desired,sink(0).declared,sink(0).registered_kinds);
        for (const auto &d:listeners(from)) std::printf(" [+%ums ev=%u sub=%u]",d.time_ms-start,d.event,d.subtype);
        std::printf("\n");
        offer(frame(1,adv,kLv)); offer(frame(2,fail,kLv)); advance(kJoinMs);
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0)); advance(kJoinMs);
    }
}
// P12: a link reset during the conflict (Advertise latest beside Failed) destroys the registrations; the latest the
// binding held is stale. After the reset a Failed alone asks Failed, and a later Advertise New decides again.
TEST_F(R849Probe, P12ResetDuringConflictLeavesNoStaleLatest) {
    settle(); advance(400); bind(0);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"P12 Failed");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"P12 Advertise New");
    mbx_model_set_link(&model,0,false); settle(); mbx_model_set_link(&model,0,true); settle(); advance(400);
    EXPECT_EQ(sink(0).registered_kinds,0u)<<"P12 the reset destroyed the registrations";
    EXPECT_EQ(sink(0).desired,0u);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"P12 after the reset a Failed alone asks Failed");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"P12 after the reset an Advertise New decides");
    expect_declared(record(kFailed,kNew),0,kFailed,"P12 after the reset a Failed New decides");
}
} // namespace
