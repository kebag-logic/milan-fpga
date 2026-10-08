// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe R532-10 (included at the end of test_acmp_mbx.cpp in a
// disposable copy, after srp_binding.hpp). Observes, does not change, the
// firmware: (1) a Talker attribute kind change while the composed listener is
// already SETTLED_RSV_OK; (2) the mailbox cost of withdrawal feedback for every
// bound sink in one delivery poll, against CTRL_APP_SRP_FEEDBACK_MAX.
namespace {
// GET_RX_STATE_RESPONSE flags for sink k off the model's wire; negative if absent.
#define R10_RX_FLAGS_LAMBDA \
    auto r10_flags=[&](unsigned k)->int { \
        const std::uint32_t sent=model.tx_sent; \
        if (!offer(command(spec::MSG_GET_RX_STATE_COMMAND,k),spec::MULTICAST_MAC,acfg.sink_interface[k])) return -1; \
        settle(); \
        for (std::uint32_t n=sent;n<model.tx_sent;++n) { \
            const Pdu p=wire(n); \
            if (p.msg==spec::MSG_GET_RX_STATE_RESPONSE) return p.flags; \
        } \
        return -2; \
    }
TEST_F(SrpBinding, R10KindChangeWhileSettledReachesAcmp) {
    R10_RX_FLAGS_LAMBDA;
    for (unsigned k=0;k<2u;++k) { bind(k); response(k,k); registration(k,false,0,k); }
    for (unsigned k=0;k<2u;++k) {
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        ASSERT_FALSE(core()->sinks[k].tk_failed);
    }
    // Advertise -> Failed: the talker declares Talker Failed (New) and leaves
    // the Advertise attribute; keep refreshing Failed for two seconds.
    for (unsigned k=0;k<2u;++k) { registration(k,true,0,k); registration(k,false,5,k); }
    for (unsigned t=0;t<200u;++t) {
        mbx_model_advance_ms(&model,10u); settle();
        if (t%50u==0u) for (unsigned k=0;k<2u;++k) registration(k,true,1,k);
    }
    for (unsigned k=0;k<2u;++k) {
        std::printf("  R10 kind A->F sink %u: srp desired %u, acmp state %d tk_failed %d impossible %u\n",k,
                    unsigned(sink(k).desired),int(core()->sinks[k].state),int(core()->sinks[k].tk_failed),
                    unsigned(core()->impossible));
        EXPECT_EQ(sink(k).desired,1u) << "SRP itself sees Talker Failed";
        EXPECT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        EXPECT_TRUE(core()->sinks[k].tk_failed) << "R10 Advertise->Failed reaches ACMP's REGISTERING_FAILED";
        const int flags=r10_flags(k);
        std::printf("  R10 kind A->F sink %u: GET_RX_STATE_RESPONSE flags 0x%04x\n",k,unsigned(flags));
        EXPECT_TRUE(flags>=0 && (flags&ACMP_FLAG_REGISTERING_FAILED)!=0) << "R10 wire REGISTERING_FAILED after A->F";
    }
}

TEST_F(SrpBinding, R10FailedToAdvertiseWhileSettledReachesAcmp) {
    R10_RX_FLAGS_LAMBDA;
    for (unsigned k=0;k<2u;++k) { bind(k); response(k,k); registration(k,true,0,k); }
    for (unsigned k=0;k<2u;++k) {
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        ASSERT_TRUE(core()->sinks[k].tk_failed);
    }
    // Failed -> Advertise: the talker declares Talker Advertise (New) and
    // leaves Talker Failed; keep refreshing Advertise for two seconds.
    for (unsigned k=0;k<2u;++k) { registration(k,false,0,k); registration(k,true,5,k); }
    for (unsigned t=0;t<200u;++t) {
        mbx_model_advance_ms(&model,10u); settle();
        if (t%50u==0u) for (unsigned k=0;k<2u;++k) registration(k,false,1,k);
    }
    for (unsigned k=0;k<2u;++k) {
        std::printf("  R10 kind F->A sink %u: srp desired %u, acmp state %d tk_failed %d impossible %u\n",k,
                    unsigned(sink(k).desired),int(core()->sinks[k].state),int(core()->sinks[k].tk_failed),
                    unsigned(core()->impossible));
        EXPECT_EQ(sink(k).desired,2u) << "SRP itself sees Talker Advertise";
        EXPECT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        EXPECT_FALSE(core()->sinks[k].tk_failed) << "R10 Failed->Advertise clears ACMP's REGISTERING_FAILED";
        const int flags=r10_flags(k);
        std::printf("  R10 kind F->A sink %u: GET_RX_STATE_RESPONSE flags 0x%04x\n",k,unsigned(flags));
        EXPECT_TRUE(flags>=0 && (flags&ACMP_FLAG_REGISTERING_FAILED)==0) << "R10 wire REGISTERING_FAILED after F->A";
    }
}

TEST_F(SrpBinding, R10WithdrawalFeedbackCostFitsAllowance) {
    for (unsigned k=0;k<2u;++k) { bind(k); response(k,k); registration(k,true,0,k); }
    for (unsigned k=0;k<2u;++k) ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
    std::printf("  R10 polls %u: deliver index fn==poll4 %d\n",app.loop.n_polls,
                int(app.loop.polls[4].ctx==static_cast<void*>(&app)));
    // Rapid leave (Failed, as the round-10 withdrawal case) with delivery held back.
    without_delivery([&]{ for (unsigned k=0;k<2u;++k) registration(k,true,5,k); });
    for (unsigned k=0;k<2u;++k)
        std::printf("  R10 before delivery sink %u: srp desired %u acmp state %d\n",k,unsigned(sink(k).desired),
                    int(core()->sinks[k].state));
    const auto before=model.reads+model.writes;
    app.loop.polls[4].fn(app.loop.polls[4].ctx);
    const auto cost=model.reads+model.writes-before;
    std::printf("  R10 withdrawal feedback for 2 sinks: %u accesses; allowance %u (per sink %u)\n",
                unsigned(cost),unsigned(CTRL_APP_SRP_FEEDBACK_MAX),unsigned(CTRL_APP_SRP_FEEDBACK_MAX/ACMP_MAX_SINKS));
    for (unsigned k=0;k<2u;++k) EXPECT_NE(core()->sinks[k].state,ACMP_SETTLED_RSV_OK) << "withdrawal delivered";
    EXPECT_GT(cost,0u) << "the measured poll did the withdrawal";
    EXPECT_LE(cost,2u*(CTRL_APP_SRP_FEEDBACK_MAX/ACMP_MAX_SINKS)) << "R10 per-sink withdrawal cost within allowance";
}

TEST_F(SrpBinding, R10DiscoveredWithdrawalFeedbackCostFitsAllowance) {
    for (unsigned k=0;k<2u;++k) { bind(k); response(k,k); registration(k,true,0,k); }
    // The talker's ENTITY_AVAILABLE on each sink's interface: discovered, so a
    // withdrawal reprobes through TMR_DELAY (clock, first-draw seed, re-arm).
    for (unsigned k=0;k<2u;++k) ASSERT_TRUE(available(Adp{},acfg.sink_interface[k]));
    settle();
    for (unsigned k=0;k<2u;++k) {
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        std::printf("  R10 discovered sink %u: %d adp_armed %d\n",k,int(core()->sinks[k].discovered),
                    int(core()->sinks[k].adp_armed));
    }
    without_delivery([&]{ for (unsigned k=0;k<2u;++k) registration(k,true,5,k); });
    const auto before=model.reads+model.writes;
    app.loop.polls[4].fn(app.loop.polls[4].ctx);
    const auto cost=model.reads+model.writes-before;
    std::printf("  R10 discovered withdrawal feedback for 2 sinks: %u accesses; states %d %d; allowance %u (per sink %u)\n",
                unsigned(cost),int(core()->sinks[0].state),int(core()->sinks[1].state),
                unsigned(CTRL_APP_SRP_FEEDBACK_MAX),unsigned(CTRL_APP_SRP_FEEDBACK_MAX/ACMP_MAX_SINKS));
    for (unsigned k=0;k<2u;++k) EXPECT_EQ(core()->sinks[k].state,ACMP_PRB_W_DELAY) << "withdrawal reprobes";
    EXPECT_GT(cost,0u);
    EXPECT_LE(cost,2u*(CTRL_APP_SRP_FEEDBACK_MAX/ACMP_MAX_SINKS)) << "R10 per-sink withdrawal cost within allowance";
}
} // namespace
