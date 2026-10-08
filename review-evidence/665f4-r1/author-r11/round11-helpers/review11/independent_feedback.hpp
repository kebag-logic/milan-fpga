// Public wire probes added by the independent reviewer.
namespace {
class R533Feedback : public SrpBinding {
protected:
    void check_current_flag(unsigned k, bool failed) {
        // A real withdrawal may already have initiated reprobe. If the core
        // still reports settled, Table 5.39 requires the CURRENT SRP type.
        if (core()->sinks[k].state != ACMP_SETTLED_RSV_OK) {
            EXPECT_FALSE(sink(k).bound) << "reprobe clears SRP";
            return;
        }
        const auto sent=model.tx_sent;
        ASSERT_TRUE(offer(command(spec::MSG_GET_RX_STATE_COMMAND,k),spec::MULTICAST_MAC,acfg.sink_interface[k]));
        settle();
        bool found=false;
        for(unsigned n=sent;n<model.tx_sent;++n) {
            const auto *f=mbx_model_tx_frame(&model,n);
            if(f->channel!=MBX_CH_ACMP) continue;
            const auto response=read(f->bytes);
            if(response.msg!=spec::MSG_GET_RX_STATE_RESPONSE) continue;
            found=true;
            std::printf("probe: IF=%u sink=%u port=%u SRP desired=%u ACMP failed=%u wire flags=0x%x expected failed=%u\n",
                        MBX_N_IF,k,acfg.sink_interface[k],sink(k).desired,core()->sinks[k].tk_failed,response.flags,failed);
            EXPECT_EQ(bool(response.flags & ACMP_FLAG_REGISTERING_FAILED),failed)
                << "Table 5.39 GET_RX_STATE must report the current registration type";
        }
        EXPECT_TRUE(found) << "real GET_RX_STATE response observed";
    }
};
TEST_F(R533Feedback, R533FailedReplacementUpdatesReportedRegistration) {
    for(unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k);
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        ASSERT_FALSE(core()->sinks[k].tk_failed);
        // Conflicting New registrations retain Failed precedence (35.2.6).
        // No total unregistration is required for this value change.
        registration(k,true,0,k);
        ASSERT_EQ(sink(k).desired,1u) << "SRP selected the Failed registration";
        check_current_flag(k,true);
    }
}
TEST_F(R533Feedback, R533AdvertiseReplacementClearsReportedFailure) {
    for(unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,true,0,k);
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        ASSERT_TRUE(core()->sinks[k].tk_failed);
        registration(k,false,1,k);
        if(core()->sinks[k].state==ACMP_SETTLED_RSV_OK) {
            ASSERT_EQ(sink(k).desired,2u) << "SRP selected the Advertise replacement";
        }
        check_current_flag(k,false);
    }
}
TEST_F(R533Feedback, R533WithdrawalBeforeReregistrationStillReprobes) {
    for(unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k);
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        auto leave=talker(k,false,5), join=talker(k,false,0);
        ASSERT_TRUE(mbx_model_rx(&model,leave.data(),leave.size(),acfg.sink_interface[k]));
        ASSERT_TRUE(mbx_model_rx(&model,join.data(),join.size(),acfg.sink_interface[k]));
        const auto received=srp_adapter.received;
        settle();
        ASSERT_EQ(srp_adapter.received-received,2u);
        std::printf("probe: IF=%u sink=%u port=%u two records received; ACMP state=%u SRP bound=%u desired=%u\n",
                    MBX_N_IF,k,acfg.sink_interface[k],core()->sinks[k].state,sink(k).bound,sink(k).desired);
        EXPECT_EQ(core()->sinks[k].state,ACMP_PRB_W_AVAIL) << "withdrawal triggers Milan 5.5.3.5.48";
        EXPECT_FALSE(sink(k).bound) << "withdrawal stops SRP before another probe";
    }
}
TEST_F(R533Feedback, R533SeparatePassWithdrawalDoesReprobe) {
    for(unsigned k=0;k<2u;++k) {
        bind(k); response(k,k); registration(k,false,0,k);
        ASSERT_EQ(core()->sinks[k].state,ACMP_SETTLED_RSV_OK);
        registration(k,false,5,k);
        EXPECT_EQ(core()->sinks[k].state,ACMP_PRB_W_AVAIL);
        EXPECT_FALSE(sink(k).bound);
    }
}
}
