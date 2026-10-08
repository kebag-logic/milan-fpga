// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe R532-11 (included at the end of test_acmp_mbx.cpp in a
// disposable copy, after srp_feedback.hpp). Observes, does not change, the
// firmware. Each case drives real mailbox ingress and the composition poll.
namespace {
class R11Feedback : public SrpBinding {};

// An undelivered withdrawal followed by an ACMP rebind to the identical SRP
// identity: no Talker is registered any more, so the new epoch must settle
// SETTLED_NO_RSV, never RSV_OK from the retired epoch's kind.
TEST_F(R11Feedback, IdenticalRebindAfterUndeliveredWithdrawalSettlesNoRsv) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k);
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        without_delivery([&] {
            registration(k,false,5,k);   // Lv: registrar empties at once (Milan rapid leave)
            auto p=command(spec::MSG_BIND_RX_COMMAND,k); p.talker=kTkB;
            ASSERT_TRUE(offer(p,spec::MULTICAST_MAC,acfg.sink_interface[k])); settle();
            response(k,k);               // identical StreamID, destination and VID
        });
        settle();
        EXPECT_TRUE(sink(k).bound);
        EXPECT_EQ(sink(k).desired,0u) << "r11 no Talker registered";
        EXPECT_EQ(core()->sinks[k].state,ACMP_SETTLED_NO_RSV) << "r11 retired kind cannot settle the new epoch";
        EXPECT_EQ(core()->impossible,0u);
    }
}

// A link reset destroys the registrar: the settled sink must observe a
// withdrawal and reprobe, also when the Talker re-registers before delivery.
TEST_F(R11Feedback, LinkResetWithdrawsTheSettledRegistration) {
    for (bool rejoin : {false,true}) {
        if (rejoin) { TearDown(); SetUp(); }
        for (unsigned k=0;k<2u;++k) {
            bind(k); response(k,k); registration(k,false,0,k);
            ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
            const unsigned i=acfg.sink_interface[k];
            without_delivery([&] {
                mbx_model_set_link(&model,i,false); settle();
                if (rejoin) { mbx_model_set_link(&model,i,true); settle(); registration(k,false,0,k); }
            });
            settle();
            EXPECT_EQ(core()->sinks[k].state,ACMP_PRB_W_AVAIL) << "r11 link reset withdraws registration";
            EXPECT_EQ(core()->impossible,0u);
            if (!rejoin) { mbx_model_set_link(&model,i,true); settle(); }
            unbind(k);
        }
    }
}

// A withdrawal retains its preceding kind: a later Failed registration in
// the same pass must not be reported before the withdrawal reprobes.
TEST_F(R11Feedback, LaterKindAfterWithdrawalIsNotReported) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k);
        ASSERT_FALSE(core()->sinks[k].tk_failed);
        without_delivery([&] { registration(k,false,5,k); registration(k,true,0,k); });
        bool saw_failed=false;
        fk.hook_kind=Call::CHANGED;
        fk.hook=[&] { saw_failed=saw_failed || core()->sinks[k].tk_failed; };
        settle();
        EXPECT_FALSE(saw_failed) << "r11 retained pre-withdrawal kind";
        EXPECT_EQ(core()->sinks[k].state,ACMP_PRB_W_AVAIL);
        EXPECT_EQ(core()->impossible,0u);
        fk.hook=nullptr;
    }
}

// Unchanged repeated registration in SETTLED_RSV_OK stays idempotent: no
// view notification and no impossible event over many refreshes.
TEST_F(R11Feedback, UnchangedRepeatsAreIdempotent) {
    for (unsigned k=0;k<2u;++k) { bind(k); response(k,k); registration(k,true,0,k); }
    const auto changed=fk.count(Call::CHANGED);
    for (unsigned n=0;n<20u;++n) {
        for (unsigned k=0;k<2u;++k) { registration(k,true,1,k); }
        mbx_model_advance_ms(&model,100u); settle();
    }
    EXPECT_EQ(fk.count(Call::CHANGED),changed) << "r11 unchanged repeats notify nothing";
    for (unsigned k=0;k<2u;++k) {
        EXPECT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        EXPECT_TRUE(core()->sinks[k].tk_failed);
    }
    EXPECT_EQ(core()->impossible,0u);
}
} // namespace
