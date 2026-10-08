// SPDX-License-Identifier: CERN-OHL-W-2.0
// Ordered SRP feedback through real mailbox input and ACMP wire responses.
namespace {
class SrpFeedback : public SrpBinding {
protected:
    void current_kind(unsigned k, bool failed) {
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK) << "kind preserves settled state";
        EXPECT_EQ(core()->sinks[k].tk_failed,failed) << "current kind reaches ACMP";
        const auto sent=model.tx_sent;
        ASSERT_TRUE(offer(command(spec::MSG_GET_RX_STATE_COMMAND,k),spec::MULTICAST_MAC,acfg.sink_interface[k]));
        settle();
        bool found=false;
        for (unsigned n=sent;n<model.tx_sent;++n) {
            const auto *f=mbx_model_tx_frame(&model,n);
            if (f->channel!=MBX_CH_ACMP) { continue; }
            const auto p=read(f->bytes);
            if (p.msg!=spec::MSG_GET_RX_STATE_RESPONSE) { continue; }
            found=true;
            EXPECT_EQ(bool(p.flags & ACMP_FLAG_REGISTERING_FAILED),failed) << "wire reports current kind";
        }
        EXPECT_TRUE(found);
        EXPECT_EQ(core()->impossible,0u) << "kind is not a repeated registration event";
        EXPECT_EQ(core()->reentries,0u);
        EXPECT_EQ(srp_adapter.reentries,0u);
    }
    void queue(unsigned k, const std::vector<uint8_t>& frame) {
        ASSERT_TRUE(mbx_model_rx(&model,frame.data(),frame.size(),acfg.sink_interface[k]));
    }
    void reprobed(unsigned k) {
        EXPECT_EQ(core()->sinks[k].state,ACMP_PRB_W_AVAIL) << "retained withdrawal reprobes";
        EXPECT_FALSE(sink(k).bound) << "retained withdrawal retires binding";
        EXPECT_EQ(core()->impossible,0u) << "feedback stays ordered";
    }
};

TEST_F(SrpFeedback, AdvertiseToFailedUpdatesTheSettledWireView) {
    for (unsigned k=0;k<2u;++k) { bind(k); response(k,k); registration(k,false,0,k); }
    for (unsigned k=0;k<2u;++k) {
        without_delivery([&]{registration(k,true,0,k);});
        EXPECT_FALSE(core()->sinks[k].tk_failed) << "kind waits for delivery";
        fk.hook_kind=Call::CHANGED;
        fk.hook=[&] { EXPECT_FALSE(srp_adapter.busy); EXPECT_TRUE(core()->in_port); };
        settle();
        current_kind(k,true);
        registration(k,false,5,k); // Failed remains: this is not total withdrawal.
        registration(k,true,1,k);
        current_kind(k,true);
        if (k==0) { current_kind(1,false); }
    }
}

TEST_F(SrpFeedback, FailedToAdvertiseUpdatesTheSettledWireView) {
    for (unsigned k=0;k<2u;++k) { bind(k); response(k,k); registration(k,true,0,k); }
    for (unsigned k=0;k<2u;++k) {
        registration(k,false,1,k); // Atomic JoinIn replacement: no false withdrawal.
        current_kind(k,false);
        registration(k,false,1,k);
        current_kind(k,false);
        if (k==0) { current_kind(1,true); }
    }
}

TEST_F(SrpFeedback, WithdrawalThenRegistrationRetainsTheFirstEvent) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k);
        queue(k,talker(k,false,5)); queue(k,talker(k,false,0));
        const auto received=srp_adapter.received;
        settle();
        ASSERT_EQ(srp_adapter.received-received,2u);
        reprobed(k);
    }
}

TEST_F(SrpFeedback, SinglePduWithdrawalThenRegistrationRetainsTheFirstEvent) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k);
        auto frame=talker(k,false,5), join=talker(k,false,0);
        frame.resize(frame.size()-2u); // Replace PDU EndMark with a second Message.
        frame.insert(frame.end(),join.begin()+15,join.end());
        queue(k,frame); settle();
        reprobed(k);
    }
}

// Failed Lv followed by New in one PDU must retain the withdrawal, even
// though the final registrar snapshot again contains the same Failed Talker.
TEST_F(SrpFeedback, FailedSinglePduWithdrawalThenRegistrationRetainsTheFirstEvent) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,true,0,k);
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        ASSERT_TRUE(core()->sinks[k].tk_failed);
        auto frame=talker(k,true,5), join=talker(k,true,0);
        frame.resize(frame.size()-2u); // Replace PDU EndMark with a second Message.
        frame.insert(frame.end(),join.begin()+15,join.end());
        const auto received=srp_adapter.received;
        queue(k,frame); settle();
        ASSERT_EQ(srp_adapter.received-received,1u);
        reprobed(k);
    }
}

// Advertise -> Failed JoinIn is continuous, but the following Failed Lv
// withdraws that replacement before Advertise returns in the same PDU.
TEST_F(SrpFeedback, FailedReplacementWithdrawnInsideOnePduStillReprobes) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k);
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        auto frame=talker(k,true,1);
        for (const auto& next : {talker(k,true,5),talker(k,false,1)}) {
            frame.resize(frame.size()-2u);
            frame.insert(frame.end(),next.begin()+15,next.end());
        }
        const auto received=srp_adapter.received;
        queue(k,frame); settle();
        ASSERT_EQ(srp_adapter.received-received,1u);
        reprobed(k);
    }
}

// New can register both kinds. Failed Lv plus Advertise refresh in one PDU
// leaves Advertise registered throughout: only the kind changes at delivery.
TEST_F(SrpFeedback, BothKindsFailedLeaveInsideOnePduIsNotAWithdrawal) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k); registration(k,true,0,k);
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        ASSERT_EQ(sink(k).registered_kinds,3u) << "both kinds registered";
        ASSERT_TRUE(core()->sinks[k].tk_failed);
        auto frame=talker(k,true,5), refresh=talker(k,false,1);
        frame.resize(frame.size()-2u);
        frame.insert(frame.end(),refresh.begin()+15,refresh.end());
        const auto received=srp_adapter.received;
        queue(k,frame); settle();
        ASSERT_EQ(srp_adapter.received-received,1u);
        EXPECT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK) << "continuous Advertise is not withdrawn";
        EXPECT_TRUE(sink(k).bound);
        current_kind(k,false);
    }
}

TEST_F(SrpFeedback, SinglePduKindReplacementsRemainContinuous) {
    for (bool initial_failed : {false,true}) {
        if (initial_failed) { TearDown(); SetUp(); }
        for (unsigned k=0;k<2u;++k) {
            bind(k); response(k,k); registration(k,initial_failed,0,k);
            auto frame=talker(k,!initial_failed,1);
            for (unsigned repeat=0;repeat<2u;++repeat) {
                const auto next=talker(k,initial_failed,1);
                frame.resize(frame.size()-2u);
                frame.insert(frame.end(),next.begin()+15,next.end());
            }
            queue(k,frame); settle();
            current_kind(k,initial_failed);
            EXPECT_TRUE(sink(k).bound) << "atomic replacements retain binding";
        }
    }
}

TEST_F(SrpFeedback, SinglePduIdentityMismatchThenRecoveryStillWithdraws) {
    for (bool wrong_vid : {false,true}) {
        if (wrong_vid) { TearDown(); SetUp(); }
        for (unsigned k=0;k<2u;++k) {
            bind(k); response(k,k); registration(k,false,0,k);
            auto frame=talker(k,false,0);
            frame[wrong_vid ? 36 : 29] ^= 1u; // Same StreamID, changed VID or destination.
            const auto recovery=talker(k,false,0);
            frame.resize(frame.size()-2u);
            frame.insert(frame.end(),recovery.begin()+15,recovery.end());
            queue(k,frame); settle();
            reprobed(k);
        }
    }
}

TEST_F(SrpFeedback, ExpiryThenRegistrationRetainsTheFirstEvent) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k);
        auto la=talker(k,false,4); // LeaveAll plus Mt does not refresh the Talker.
        la[19]=0x20;
        queue(k,la); settle();
        without_delivery([&] {
            for (unsigned ms=0;ms<4990u;ms+=10u) { mbx_model_advance_ms(&model,10u); settle(); }
            ASSERT_NE(sink(k).desired,0u) << "registration lasts until original LeaveTime";
            mbx_model_advance_ms(&model,10u);
            queue(k,talker(k,false,0));
            settle(); // The expiry and fresh receive precede the same delivery.
            EXPECT_TRUE(sink(k).withdrawn) << "expiry retained before receive";
            EXPECT_EQ(sink(k).desired,2u);
        });
        settle(); reprobed(k);
    }
}

TEST_F(SrpFeedback, FirstRegistrationThenWithdrawalIsDeliveredInOrder) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k);
        queue(k,talker(k,true,0)); queue(k,talker(k,true,5));
        settle(); reprobed(k);
    }
}

TEST_F(SrpFeedback, KindThenWithdrawalIsDeliveredInOrder) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k);
        without_delivery([&] { registration(k,true,1,k); registration(k,true,5,k); });
        bool saw_failed=false;
        fk.hook_kind=Call::CHANGED;
        fk.hook=[&] { saw_failed=core()->sinks[k].tk_failed; EXPECT_FALSE(srp_adapter.busy); };
        settle();
        EXPECT_TRUE(saw_failed) << "kind precedes withdrawal";
        reprobed(k);
    }
}

TEST_F(SrpFeedback, WithdrawalIsIsolatedAndSupersededEvenForAnIdenticalStream) {
    for (unsigned k=0;k<2u;++k) { bind(k); response(k,k); registration(k,false,0,k); }
    without_delivery([&] {
        registration(0,false,5);
        registration(0,false,0);
    });
    current_kind(1,false); // Also delivers sink 0's withdrawal, never sink 1's.
    reprobed(0);
    for (unsigned k=0;k<2u;++k) {
        if (k==0) { unbind(k); bind(k); response(k,k); registration(k,false,0,k); }
        without_delivery([&] {
            registration(k,false,5,k); registration(k,false,0,k);
            auto p=command(spec::MSG_BIND_RX_COMMAND,k); p.talker=kTkB;
            ASSERT_TRUE(offer(p,spec::MULTICAST_MAC,acfg.sink_interface[k])); settle();
            response(k,k); // New ACMP binding, identical SRP wire identity.
        });
        settle();
        current_kind(k,false);
        EXPECT_TRUE(sink(k).bound) << "supersession retires obsolete withdrawal";
    }
}

// An undelivered withdrawal followed by an ACMP rebind to the identical SRP
// identity: no Talker is registered any more, so the new epoch must settle
// SETTLED_NO_RSV, never RSV_OK from the retired epoch's kind.
TEST_F(SrpFeedback, IdenticalRebindAfterUndeliveredWithdrawalSettlesNoRsv) {
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
        EXPECT_EQ(sink(k).desired,0u) << "no Talker registered";
        EXPECT_EQ(core()->sinks[k].state,ACMP_SETTLED_NO_RSV) << "retired kind cannot settle the new epoch";
        EXPECT_EQ(core()->impossible,0u);
    }
}

// A link reset destroys the registrar: the settled sink must observe a
// withdrawal and reprobe, also when the Talker re-registers before delivery.
TEST_F(SrpFeedback, LinkResetWithdrawsTheSettledRegistration) {
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
            EXPECT_EQ(core()->sinks[k].state,ACMP_PRB_W_AVAIL) << "link reset withdraws registration";
            EXPECT_EQ(core()->impossible,0u);
            if (!rejoin) { mbx_model_set_link(&model,i,true); settle(); }
            unbind(k);
        }
    }
}

// A withdrawal retains its preceding kind: a later Failed registration in
// the same pass must not be reported before the withdrawal reprobes.
TEST_F(SrpFeedback, LaterKindAfterWithdrawalIsNotReported) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k);
        ASSERT_FALSE(core()->sinks[k].tk_failed);
        without_delivery([&] { registration(k,false,5,k); registration(k,true,0,k); });
        bool saw_failed=false;
        fk.hook_kind=Call::CHANGED;
        fk.hook=[&] { saw_failed=saw_failed || core()->sinks[k].tk_failed; };
        settle();
        EXPECT_FALSE(saw_failed) << "retained pre-withdrawal kind";
        EXPECT_EQ(core()->sinks[k].state,ACMP_PRB_W_AVAIL);
        EXPECT_EQ(core()->impossible,0u);
        fk.hook=nullptr;
    }
}

TEST_F(SrpFeedback, ReplacementAwaitingDeliveryGetsNoOldRegistration) {
    bind(0); response(0); registration(0);
    refuse_receive();
    auto p=command(spec::MSG_BIND_RX_COMMAND,0); p.talker=kTkB;
    ASSERT_TRUE(offer(p,spec::MULTICAST_MAC,acfg.sink_interface[0])); settle();
    response(0,7);
    ASSERT_TRUE(app.srp_requests[0].pending);
    EXPECT_EQ(core()->sinks[0].state,ACMP_SETTLED_NO_RSV) << "old registration cannot settle replacement";
    calloc_before_failure=-1; settle();
    EXPECT_EQ(core()->sinks[0].state,ACMP_SETTLED_NO_RSV);
}

TEST_F(SrpFeedback, EarlierSinkTransientRefusalKeepsDeliveryAwake) {
    refuse_receive(); bind(0); response(0);
    ASSERT_TRUE(app.srp_requests[0].pending);
    ASSERT_FALSE(app.srp_requests[1].pending);
    EXPECT_TRUE(app.loop.polls[4].fn(app.loop.polls[4].ctx)) << "earlier refusal keeps delivery awake";
    calloc_before_failure=-1; settle(); expect_stream(0);
}

TEST_F(SrpFeedback, DiscoveredWithdrawalMeasuresTheFundedPath) {
    for (bool first : {false,true}) {
        if (first) { TearDown(); SetUp(); } // Each path funds its first random seed.
        for (unsigned k=0;k<2u;++k) {
            bind(k); response(k,k);
            if (!first) { registration(k,true,0,k); }
            ASSERT_TRUE(available(Adp{},acfg.sink_interface[k])); settle();
        }
        without_delivery([&] {
            for (unsigned k=0;k<2u;++k) {
                if (first) { registration(k,true,0,k); }
                registration(k,true,5,k);
            }
        });
        const auto before=model.reads+model.writes;
        app.loop.polls[4].fn(app.loop.polls[4].ctx);
        const auto cost=model.reads+model.writes-before;
        std::printf("feedback: IF=%u initial=%u sinks=2 accesses=%u allowance=%u\n",
                    MBX_N_IF,first,unsigned(cost),2u*(CTRL_APP_SRP_FEEDBACK_MAX/ACMP_MAX_SINKS));
        EXPECT_GT(cost,2u) << "discovery withdrawal reaches funded timer path";
        EXPECT_LE(cost,2u*(CTRL_APP_SRP_FEEDBACK_MAX/ACMP_MAX_SINKS)) << "measured feedback per sink allowance";
        for (unsigned k=0;k<2u;++k) {
            EXPECT_EQ(core()->sinks[k].state,ACMP_PRB_W_DELAY);
            unbind(k);
        }
    }
}
} // namespace
