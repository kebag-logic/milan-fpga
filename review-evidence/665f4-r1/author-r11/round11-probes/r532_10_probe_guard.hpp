// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe R532-10 (included after srp_binding.hpp in a disposable copy).
// Two discriminating checks for invariants ctrl_app_srp.c states but no
// existing test distinguishes: each passes at the head and is meant to fail
// under the matching reviewer plant in r532_10_escape.py.
namespace {
// "Never feed an old binding's registration to a replacement awaiting delivery"
// (ctrl_app_srp.c:78-79). Plant: r10-feedback-ignores-pending.
TEST_F(SrpBinding, R10ReplacementAwaitingDeliveryGetsNoOldRegistration) {
    bind(0); response(0); registration(0);
    ASSERT_EQ(core()->sinks[0].state,ACMP_SETTLED_RSV_OK);
    ASSERT_TRUE(sink(0).bound);
    refuse_receive();                         // SRP refuses every bind until recovery
    auto p=command(spec::MSG_BIND_RX_COMMAND,0); p.talker=kTkB;
    ASSERT_TRUE(offer(p,spec::MULTICAST_MAC,acfg.sink_interface[0])); settle();
    auto a=answer(0); a.stream_id=kSid+7u; a.dest_mac=kDa+7u;
    ASSERT_TRUE(offer(a,spec::MULTICAST_MAC,acfg.sink_interface[0])); settle();
    std::printf("  R10 replacement awaiting delivery: request pending %d, srp still holds old %d, acmp state %d\n",
                int(app.srp_requests[0].pending),int(sink(0).bound && wire_be64(sink(0).stream_id.bytes)==kSid),
                int(core()->sinks[0].state));
    ASSERT_TRUE(app.srp_requests[0].pending) << "replacement is still awaiting delivery";
    EXPECT_EQ(core()->sinks[0].state,ACMP_SETTLED_NO_RSV)
        << "R10 the old binding's registration must not settle the replacement";
    calloc_before_failure=-1; settle();
    EXPECT_EQ(core()->sinks[0].state,ACMP_SETTLED_NO_RSV) << "replacement has no talker registration yet";
}

// "Transient refusal keeps the request pending and the loop awake" (ctrl/README.md)
// for an earlier sink while a later sink has nothing owed.
// Plant: r10-transient-refusal-forgotten.
TEST_F(SrpBinding, R10EarlierSinkTransientRefusalKeepsDeliveryAwake) {
    refuse_receive();
    bind(0); response(0);
    ASSERT_TRUE(app.srp_requests[0].pending);
    ASSERT_FALSE(app.srp_requests[1].pending);
    EXPECT_TRUE(app.loop.polls[4].fn(app.loop.polls[4].ctx)) << "R10 earlier sink's refusal keeps delivery awake";
    calloc_before_failure=-1; settle();
    expect_stream(0);
}
} // namespace
