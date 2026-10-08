// SPDX-License-Identifier: CERN-OHL-W-2.0
// Real ACMP wire input must reach the attached SRP adapter through the loop.
namespace {
class SrpBinding : public AcmpMailbox {
protected:
    void SetUp() override {
        AcmpMailbox::SetUp();
        calloc_before_failure = -1;
        mbx_model_reset(&model);
        for (unsigned i = 0; i < MBX_N_IF; ++i) {
            mbx_model_set_gm(&model,i,kGm0,0);
            mbx_model_set_link(&model,i,true);
        }
        const auto cfg = three_way();
        ASSERT_TRUE(ctrl_app_start(&app,&cfg));
        attach_srp();
        settle();
    }
    void TearDown() override {
        calloc_before_failure = -1;
        srp_mbx_destroy(&srp_adapter);
        EXPECT_EQ(ctrl_pool_in_use(&app.pool),0u);
        shlan_port_bind_pool(nullptr);
    }
    srp_sink& sink(unsigned k) { return srp_adapter.ifs[acfg.sink_interface[k]].sinks[k]; }
    void response(unsigned k, unsigned variant = 0) {
        auto p = answer(k);
        p.stream_id += variant; p.dest_mac += variant; p.vlan += variant;
        ASSERT_TRUE(offer(p,spec::MULTICAST_MAC,acfg.sink_interface[k]));
        settle();
    }
    void unbind(unsigned k) {
        ASSERT_TRUE(offer(command(spec::MSG_UNBIND_RX_COMMAND,k),spec::MULTICAST_MAC,acfg.sink_interface[k]));
        settle();
    }
    void expect_stream(unsigned k, unsigned variant = 0) {
        EXPECT_TRUE(sink(k).bound) << "binding delivered";
        EXPECT_EQ(wire_be64(sink(k).stream_id.bytes),kSid + variant) << "stream identity delivered";
        EXPECT_EQ((static_cast<uint64_t>(wire_be16(sink(k).dest_mac)) << 32) |
                  wire_be32(sink(k).dest_mac + 2),kDa + variant) << "destination delivered";
        EXPECT_EQ(sink(k).vid,2u + variant) << "VLAN delivered";
    }
    template<class Fn> void without_delivery(Fn action) {
        const unsigned polls=app.loop.n_polls;
        --app.loop.n_polls;
        action();
        app.loop.n_polls=polls;
    }
    std::vector<uint8_t> talker(unsigned variant=0, bool failed=false, unsigned event=0) {
        std::vector<uint8_t> v(failed ? 34u : 25u);
        wire_put_be(v.data(),kSid+variant,8); wire_put_be(v.data()+8,kDa+variant,6);
        wire_put_be(v.data()+14,2u+variant,2); wire_put_be(v.data()+16,224,2);
        wire_put_be(v.data()+18,1,2); v[20]=0x60;
        if (failed) v[33]=1;
        const unsigned list=2+v.size()+1+2;
        std::vector<uint8_t> f(14+1+4+list+2);
        wire_put_be(f.data(),0x0180c200000eull,6);
        wire_put_be(f.data()+6,0x020304010203ull,6); wire_put_be(f.data()+12,0x22ea,2);
        auto *p=f.data()+14; p[1]=failed ? 2 : 1; p[2]=v.size();
        wire_put_be(p+3,list,2); wire_put_be(p+5,1,2);
        std::memcpy(p+7,v.data(),v.size()); p[7+v.size()]=event*36;
        return f;
    }
    void registration(unsigned k, bool failed=false, unsigned event=0, unsigned variant=0) {
        const auto f=talker(variant,failed,event);
        ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),acfg.sink_interface[k]));
        settle();
    }
    void refuse_receive() {
        // New Class A Domain requires allocation. Fail the library's port,
        // retaining a real mailbox record, never a fabricated adapter flag.
        std::array<uint8_t,30> f{};
        wire_put_be(f.data(),0x0180c200000eull,6);
        wire_put_be(f.data()+6,0x020304010203ull,6);
        wire_put_be(f.data()+12,0x22ea,2);
        f[15]=4; f[16]=4; f[18]=9; f[20]=1;
        f[21]=6; f[22]=3; f[24]=7;
        calloc_before_failure=0;
        ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),MBX_N_IF-1u));
        settle();
        ASSERT_NE(srp_adapter.pending_rx.len,0u);
    }
};

TEST_F(SrpBinding, BindIsDeferredAndKeepsEverySinkAndInterface) {
    for (unsigned k=0;k<2u;++k) {
        bind(k);
        fk.hook_kind=Call::SRP;
        fk.hook=[&,k] {
            EXPECT_FALSE(sink(k).bound) << "callback only queues the binding";
            EXPECT_TRUE(core()->in_port);
        };
        without_delivery([&]{response(k,k);});
        EXPECT_FALSE(sink(k).bound) << "binding waits for the delivery poll";
        const auto before=model.reads+model.writes;
        EXPECT_FALSE(app.loop.polls[4].fn(app.loop.polls[4].ctx));
        EXPECT_EQ(model.reads+model.writes,before) << "binding poll makes no mailbox access";
        EXPECT_FALSE(static_cast<bool>(fk.hook));
        expect_stream(k,k);
        EXPECT_FALSE(app.srp_requests[k].pending) << "accepted request retires";
        for (unsigned i=0;i<MBX_N_IF;++i) {
            if (i!=acfg.sink_interface[k]) {
                EXPECT_FALSE(srp_adapter.ifs[i].sinks[k].bound) << "binding keeps its interface";
            }
        }
    }
    EXPECT_NE(wire_be64(sink(0).stream_id.bytes),wire_be64(sink(1).stream_id.bytes)) << "binding keeps its sink";
    EXPECT_EQ(core()->reentries,0u);
    EXPECT_EQ(srp_adapter.reentries,0u);
    EXPECT_GT(fk.count(Call::LOCKED),0u);
    EXPECT_GT(fk.count(Call::PERSIST),0u);
    EXPECT_GT(fk.count(Call::CHANGED),0u);
    ASSERT_TRUE(offer(talker_command(spec::MSG_GET_TX_STATE_COMMAND),spec::MULTICAST_MAC,0));
    settle();
    EXPECT_GT(fk.count(Call::SOURCE),0u);
}

TEST_F(SrpBinding, RefusedReceiveRetriesAfterRecoveryOrExpiry) {
    for (bool expire : {false,true}) {
        for (unsigned k=0;k<2u;++k) bind(k);
        refuse_receive();
        for (unsigned k=0;k<2u;++k) {
            response(k,k);
            EXPECT_FALSE(sink(k).bound);
        }
        EXPECT_GT(ctrl_loop_service(&app.loop),0u) << "pending binding keeps service awake";
        if (expire) {
            mbx_model_advance_ms(&model,1000u);
        } else {
            calloc_before_failure=-1;
        }
        settle();
        EXPECT_EQ(srp_adapter.pending_rx.len,0u);
        for (unsigned k=0;k<2u;++k) expect_stream(k,k);
        calloc_before_failure=-1;
        for (unsigned k=0;k<2u;++k) unbind(k);
        // Recreate the participant so the same Domain is new on the next run.
        mbx_model_set_link(&model,MBX_N_IF-1u,false); settle();
        mbx_model_set_link(&model,MBX_N_IF-1u,true); settle();
    }
}

TEST_F(SrpBinding, OwedTransmissionRetriesAfterCommit) {
    for (unsigned k=0;k<2u;++k) bind(k);
    mbx_model_tx_pause(&model,true);
    auto f=srp_record();
    while (mbx_tx_send(MBX_CH_SRP,0,f.data(),f.size())==MBX_STATUS_OK) {}
    mbx_model_advance_ms(&model,200u); settle();
    ASSERT_GT(srp_adapter.owed_len,0u);
    for (unsigned k=0;k<2u;++k) {
        response(k,k);
        EXPECT_FALSE(sink(k).bound);
    }
    EXPECT_GT(ctrl_loop_service(&app.loop),0u);
    mbx_model_tx_pause(&model,false); settle();
    EXPECT_EQ(srp_adapter.owed_len,0u);
    for (unsigned k=0;k<2u;++k) expect_stream(k,k);
}

TEST_F(SrpBinding, UnbindCancelsPendingAndWithdrawsAcceptedBinding) {
    for (bool delivered : {false,true}) {
        for (unsigned k=0;k<2u;++k) bind(k);
        if (!delivered) refuse_receive();
        for (unsigned k=0;k<2u;++k) response(k,k);
        if (delivered) {
            for (unsigned k=0;k<2u;++k) expect_stream(k,k);
            refuse_receive();
        }
        for (unsigned k=0;k<2u;++k) unbind(k);
        calloc_before_failure=-1; settle();
        for (unsigned k=0;k<2u;++k) {
            EXPECT_FALSE(sink(k).bound) << "unbind supersedes pending bind";
            EXPECT_FALSE(app.srp_requests[k].pending);
        }
        mbx_model_set_link(&model,MBX_N_IF-1u,false); settle();
        mbx_model_set_link(&model,MBX_N_IF-1u,true); settle();
    }
}

TEST_F(SrpBinding, ReplacementSupersedesPendingIdentity) {
    for (unsigned k=0;k<2u;++k) bind(k);
    refuse_receive();
    for (unsigned k=0;k<2u;++k) response(k,k);
    for (unsigned k=0;k<2u;++k) {
        auto p=command(spec::MSG_BIND_RX_COMMAND,k); p.talker=kTkB;
        ASSERT_TRUE(offer(p,spec::MULTICAST_MAC,acfg.sink_interface[k])); settle();
        response(k,k+3u);
    }
    calloc_before_failure=-1; settle();
    for (unsigned k=0;k<2u;++k) expect_stream(k,k+3u);
}

TEST_F(SrpBinding, PermanentRefusalParksAndDoesNotBlockAnotherSink) {
    for (unsigned vid : {0u,4095u,65535u}) {
        bind(0); bind(1);
        without_delivery([&] {
            auto invalid=answer(0); invalid.vlan=vid;
            ASSERT_TRUE(offer(invalid,spec::MULTICAST_MAC,acfg.sink_interface[0])); settle();
            response(1,1);
        });
        EXPECT_FALSE(app.loop.polls[4].fn(app.loop.polls[4].ctx)) << "permanent refusal allows sleep";
        EXPECT_TRUE(app.srp_requests[0].parked) << "permanent refusal is visible";
        EXPECT_FALSE(app.srp_requests[0].pending);
        EXPECT_FALSE(sink(0).bound);
        expect_stream(1,1);
        EXPECT_EQ(ctrl_loop_service(&app.loop),0u) << "parked request does not keep loop awake";
        // A new binding replaces the parked request, including a valid VID.
        auto replacement=command(spec::MSG_BIND_RX_COMMAND,0); replacement.talker=kTkB;
        ASSERT_TRUE(offer(replacement,spec::MULTICAST_MAC,acfg.sink_interface[0])); settle();
        response(0);
        EXPECT_FALSE(app.srp_requests[0].parked) << "replacement clears parking";
        expect_stream(0);
        unbind(0); unbind(1);
        EXPECT_FALSE(app.srp_requests[0].parked) << "unbind clears parking";
        mbx_model_advance_ms(&model,1000u); settle();
    }
}

TEST_F(SrpBinding, ParkedReplacementRetiresThePreviouslyAcceptedBinding) {
    for (bool transient : {false,true}) {
        for (unsigned k=0;k<2u;++k) { bind(k); response(k,k); expect_stream(k,k); }
        if (transient) refuse_receive();
        without_delivery([&] {
            for (unsigned k=0;k<2u;++k) {
                auto p=command(spec::MSG_BIND_RX_COMMAND,k); p.talker=kTkB;
                ASSERT_TRUE(offer(p,spec::MULTICAST_MAC,acfg.sink_interface[k])); settle();
                auto invalid=answer(k); invalid.vlan=4095;
                ASSERT_TRUE(offer(invalid,spec::MULTICAST_MAC,acfg.sink_interface[k])); settle();
            }
        });
        for (unsigned k=0;k<2u;++k) ASSERT_TRUE(sink(k).bound);
        EXPECT_EQ(app.loop.polls[4].fn(app.loop.polls[4].ctx),transient);
        calloc_before_failure=-1; settle();
        for (unsigned k=0;k<2u;++k) {
            EXPECT_FALSE(sink(k).bound) << "parking retires the old accepted binding";
            EXPECT_TRUE(app.srp_requests[k].parked);
            EXPECT_FALSE(app.srp_requests[k].pending);
            unbind(k);
            EXPECT_FALSE(app.srp_requests[k].parked);
        }
        mbx_model_advance_ms(&model,1000u); settle();
    }
}

TEST_F(SrpBinding, AdvertiseFeedbackIsDeferredAndSurvivesNoTalkerDeadline) {
    for (unsigned k=0;k<2u;++k) { bind(k); response(k); }
    without_delivery([&] { for (unsigned k=0;k<2u;++k) registration(k); });
    for (unsigned k=0;k<2u;++k) {
        EXPECT_EQ(core()->sinks[k].state,ACMP_SETTLED_NO_RSV) << "registration waits for delivery poll";
    }
    fk.hook_kind=Call::CHANGED;
    fk.hook=[&] {
        EXPECT_TRUE(core()->in_port);
        EXPECT_FALSE(srp_adapter.busy) << "feedback runs after SRP returns";
    };
    const auto before=model.reads+model.writes;
    EXPECT_FALSE(app.loop.polls[4].fn(app.loop.polls[4].ctx));
    EXPECT_LE(model.reads+model.writes-before,CTRL_APP_SRP_FEEDBACK_MAX);
    for (unsigned second=0;second<12u;++second) {
        for (unsigned k=0;k<2u;++k) {
            registration(k,false,1);
            EXPECT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK) << "Advertise reaches ACMP";
            EXPECT_FALSE(core()->sinks[k].tk_failed);
        }
        for (unsigned ms=0;ms<1000u;ms+=10u) { mbx_model_advance_ms(&model,10u); settle(); }
    }
    for (unsigned k=0;k<2u;++k) expect_stream(k);
    EXPECT_EQ(core()->impossible,0u) << "unchanged registration is delivered once";
    EXPECT_EQ(core()->reentries,0u); EXPECT_EQ(srp_adapter.reentries,0u);
}

TEST_F(SrpBinding, FailedRegistrationReachesAcmpAndWithdrawalReprobes) {
    for (unsigned k=0;k<2u;++k) {
        bind(k); response(k,k);
        without_delivery([&]{registration(k,true,0,k);});
        app.loop.polls[4].fn(app.loop.polls[4].ctx);
        EXPECT_TRUE(core()->sinks[k].tk_failed) << "Failed flag reaches ACMP";
    }
    for (unsigned k=0;k<2u;++k) {
        EXPECT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK) << "Failed registration reaches ACMP";
        EXPECT_TRUE(core()->sinks[k].tk_failed) << "Failed flag reaches ACMP";
        without_delivery([&]{registration(k,true,5,k);});
    }
    // Milan 4.2.7.2.2 rapid leave from IN retires immediately in SRP.
    // ACMP observes it only after the delivery poll runs.
    for (unsigned k=0;k<2u;++k) EXPECT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
    settle();
    for (unsigned k=0;k<2u;++k) {
        EXPECT_EQ(core()->sinks[k].state,ACMP_PRB_W_AVAIL) << "withdrawal reaches ACMP";
        EXPECT_FALSE(sink(k).bound) << "withdrawal delivers the resulting unbind";
    }
    EXPECT_EQ(core()->impossible,0u);
    EXPECT_EQ(core()->reentries,0u); EXPECT_EQ(srp_adapter.reentries,0u);
}

TEST_F(SrpBinding, RegistrationKeepsSinkAndInterfaceIdentity) {
    for (unsigned k=0;k<2u;++k) { bind(k); response(k,k); }
    // Matching identity on the wrong interface cannot settle this sink.
    const auto f=talker();
    if (MBX_N_IF==2u) {
        ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),1u)); settle();
        EXPECT_EQ(core()->sinks[0].state,ACMP_SETTLED_NO_RSV);
    }
    registration(0);
    EXPECT_EQ(core()->sinks[0].state,ACMP_SETTLED_RSV_OK) << "feedback uses configured interface";
    EXPECT_EQ(core()->sinks[1].state,ACMP_SETTLED_NO_RSV) << "feedback keeps sink identity";
    registration(1,true,0,1);
    EXPECT_EQ(core()->sinks[1].state,ACMP_SETTLED_RSV_OK) << "second interface registration delivered; feedback keeps sink identity";
    EXPECT_TRUE(core()->sinks[1].tk_failed);
    EXPECT_FALSE(core()->sinks[0].tk_failed);
    unbind(0);
    EXPECT_EQ(core()->sinks[1].state,ACMP_SETTLED_RSV_OK) << "other sink survives unbind";
    EXPECT_EQ(core()->impossible,0u);
}

TEST_F(SrpBinding, AttachmentRefusesMissingRoomAndShapeWithoutPartialBinding) {
    const auto srp_config=srp_adapter.config;
    EXPECT_FALSE(ctrl_app_attach_srp(&app,&srp_adapter)) << "duplicate composition attachment refused";
    srp_mbx_destroy(&srp_adapter);
    // The delivery poll has no work once its SRP participant is detached.
    EXPECT_FALSE(app.loop.polls[4].fn(app.loop.polls[4].ctx));
    ASSERT_TRUE(srp_mbx_init(&srp_adapter,&srp_config));
    EXPECT_FALSE(ctrl_app_attach_srp(&app,&srp_adapter)) << "recompose before replacing the attached adapter";
    srp_mbx_destroy(&srp_adapter);
    const auto cfg=three_way();
    ASSERT_TRUE(ctrl_app_start(&app,&cfg));
    ASSERT_TRUE(srp_mbx_init(&srp_adapter,&srp_config));
    const unsigned count=app.loop.n_polls;
    app.loop.n_polls=CTRL_LOOP_MAX_POLLS-1u;
    EXPECT_FALSE(ctrl_app_attach_srp(&app,&srp_adapter));
    EXPECT_EQ(app.loop.rx[MBX_CH_SRP].fn,nullptr);
    app.loop.n_polls=count;
    core()->cfg.n_sinks=CTRL_SRP_SINKS+1u;
    EXPECT_FALSE(ctrl_app_attach_srp(&app,&srp_adapter));
    EXPECT_EQ(app.loop.rx[MBX_CH_SRP].fn,nullptr);
}
} // namespace
