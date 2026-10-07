// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "srp_fixture.hpp"
#include "ctrl_app.h"
FW_TALLY_LABEL("ctrl ADP MAAP SRP composition");
namespace {
TEST(SrpApp, AttachRefusalPreservesExistingComposition) {
    mbx_model model{}; mbx_model_reset(&model); mbx_model_bind(&model,nullptr,nullptr);
    ctrl_app app{};
    srp_mbx adapter{};
    auto receive=[](void*,const mbx_frame*) {};
    EXPECT_FALSE(ctrl_app_attach_srp(&app,&adapter));
    app.loop.rx[MBX_CH_ADP].fn=receive;
    EXPECT_FALSE(ctrl_app_attach_srp(&app,&adapter));
    app.loop.rx[MBX_CH_MAAP].fn=receive;
    EXPECT_FALSE(ctrl_app_attach_srp(&app,&adapter));
    EXPECT_EQ(app.loop.rx[MBX_CH_ADP].fn,receive);
    EXPECT_EQ(app.loop.rx[MBX_CH_MAAP].fn,receive);
    EXPECT_EQ(app.loop.rx[MBX_CH_SRP].fn,nullptr);
    EXPECT_EQ(app.loop.n_ticks,0u);
}

TEST(SrpApp, AllThreeProtocolsShareTheLoopAndWakeSources) {
    mbx_model model{}; mbx_model_reset(&model); mbx_model_bind(&model,nullptr,nullptr);
    ctrl_app app{}; srp_mbx adapter{};
    alignas(std::max_align_t) uint8_t arena[SRP_POOL_ARENA_BYTES]{};
    adp_entity entity{};
    entity.mac=0x020304050600ull; entity.entity_id=0x020304fffe050600ull;
    entity.talker_stream_sources=CTRL_SRP_SOURCES;
    ctrl_app_config cfg{&entity,0,arena,sizeof(arena),srp_pool_classes,SRP_POOL_N_CLASSES,nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,0};
    unsigned allocations=0;
    auto allocation=[](void *ctx,unsigned,uint64_t,uint16_t,bool valid) {
        if(valid) ++*static_cast<unsigned*>(ctx);
    };
    for(unsigned i=0;i<MBX_N_IF;++i) mbx_model_set_link(&model,i,true);
    ASSERT_TRUE(ctrl_app_start_maap(&app,&cfg,allocation,&allocations,0));
    srp_source sources[MBX_N_IF][CTRL_SRP_SOURCES]{};
    srp_mbx_config config{}; config.link_rate_bps=1000000000;
    config.licence=[](void*,unsigned,unsigned,bool) {};
    for(unsigned i=0;i<MBX_N_IF;++i) {
        config.mac[i]=entity.mac; config.sources[i]=sources[i];
        for(unsigned s=0;s<CTRL_SRP_SOURCES;++s) {
            auto &v=sources[i][s].value;
            wire_put_be(v.stream_id.bytes,entity.mac,6);
            wire_put_be(v.stream_id.bytes+6,s,2);
            v.vlan_id=2; v.max_frame_size=224; v.max_interval_frames=1; v.priority_and_rank=0x60;
        }
    }
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ASSERT_TRUE(ctrl_app_attach_srp(&app,&adapter));
    const unsigned channels=(1u<<MBX_CH_ADP)|(1u<<MBX_CH_MAAP)|(1u<<MBX_CH_SRP);
    EXPECT_EQ(model.filter_en,channels);
    EXPECT_EQ(model.irq_enable,(channels<<MBX_IRQ_ENABLE_RX_LSB)|(1u<<MBX_IRQ_ENABLE_EVT_LSB));
    EXPECT_EQ(app.loop.n_sinks,3u);
    EXPECT_EQ(app.loop.n_polls,3u);
    EXPECT_EQ(app.loop.n_ticks,1u);
    EXPECT_FALSE(ctrl_app_attach_srp(&app,&adapter));
    EXPECT_EQ(model.filter_en,channels);
    for(unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_NE(app.maap.ifs[i].slot,app.adp.ifs[i].slot);
        EXPECT_EQ(model.own_mac[i],entity.mac);
    }
    for(unsigned ms=0;ms<2200;++ms) {
        mbx_model_advance_ms(&model,1);
        for(unsigned n=0;n<10 && ctrl_loop_service(&app.loop);++n) {}
    }
    EXPECT_EQ(allocations,MBX_N_IF);
    EXPECT_EQ(app.loop.stats.ticks,220u);
    bool sent[MBX_N_CH]{};
    for(unsigned n=0;n<model.tx_sent;++n) {
        const auto *f=mbx_model_tx_frame(&model,n);
        ASSERT_NE(f,nullptr); sent[f->channel]=true;
    }
    EXPECT_TRUE(sent[MBX_CH_ADP]);
    EXPECT_TRUE(sent[MBX_CH_MAAP]);
    EXPECT_TRUE(sent[MBX_CH_SRP]);
    srp_mbx_destroy(&adapter);
    maap_mbx_stop(&app.maap); adp_mbx_set_enable(&app.adp,false);
    EXPECT_EQ(ctrl_pool_in_use(&app.pool),0u);
    shlan_port_bind_pool(nullptr);
}
} // namespace

namespace {
// Isolate callback costs from loop/ring costs, using the same registered
// callbacks as production. The model counts every actual MMIO operation.
template<class Fn>
uint64_t srp_cost(mbx_model& model, Fn action) {
    const uint64_t before=model.reads+model.writes;
    action();
    return model.reads+model.writes-before;
}

TEST_F(Srp, EventReceiveAndTransmitPollFitTheirMeasuredBounds) {
    settle();
    auto cost=[&](auto action) { return srp_cost(model,action); };
    auto check=[](const char* label,uint64_t actual,unsigned limit) {
        std::printf("  %s: %u accesses, bound %u\n",label,static_cast<unsigned>(actual),limit);
        EXPECT_LE(actual,limit) << label;
    };
    mbx_event ev{}; ev.type=MBX_EV_TYPE_LINK; ev.interface=MBX_N_IF-1u; ev.link_up=true;
    const auto event=cost([&]{loop.sinks[0].fn(loop.sinks[0].ctx,&ev);});
    ASSERT_GT(event,0u);
    check("SRP event bound",event,SRP_MBX_EVENT_MAX);
    settle();
    const auto f=frame(4,{6,3,0,7},0);
    mbx_frame rx{};
    ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),MBX_N_IF-1u));
    ASSERT_EQ(mbx_rx_take(MBX_CH_SRP,&rx),MBX_STATUS_OK);
    calloc_before_failure=0;
    const auto receive=cost([&] {
        ASSERT_TRUE(loop.rx[MBX_CH_SRP].ready(&adapter));
        loop.rx[MBX_CH_SRP].fn(&adapter,&rx);
    });
    ASSERT_EQ(adapter.pending_rx.len,rx.len);
    check("SRP refused receive bound",receive,SRP_MBX_RX_MAX);
    const auto refused_poll=cost([&]{loop.polls[0].fn(loop.polls[0].ctx);});
    ASSERT_GT(refused_poll,MBX_N_IF);
    check("SRP retained receive poll bound",refused_poll,SRP_MBX_POLL_MAX);
    calloc_before_failure=-1; settle();
    // Mature the real Applicant's transmit opportunity without polling it.
    for (unsigned n=0;n<20u;++n) loop.ticks[0]();
    const auto sent=adapter.transmitted;
    const auto transmit_poll=cost([&]{loop.polls[0].fn(loop.polls[0].ctx);});
    ASSERT_GT(adapter.transmitted,sent);
    check("SRP transmitting poll bound",transmit_poll,SRP_MBX_POLL_MAX);
    // Per-frame bound independently measures the actual TX driver, at the
    // channel's maximum payload, so a one-access understatement is visible.
    std::vector<uint8_t> large(MBX_CH_SRP_MAX_FRAME_BYTES);
    const auto tx=cost([&]{ASSERT_EQ(mbx_tx_send(MBX_CH_SRP,0,large.data(),large.size()),MBX_STATUS_OK);});
    check("SRP maximum TX record bound",tx,SRP_MBX_TX_MAX);
    // Receive the maximum permitted wire record, through the real ring.
    // A valid empty MVRP PDU can carry Ethernet padding up to this ceiling.
    wire_put_be(large.data(),0x0180c2000021ull,6);
    wire_put_be(large.data()+6,0x020304010203ull,6);
    wire_put_be(large.data()+12,0x88f5u,2);
    ASSERT_TRUE(mbx_model_rx(&model,large.data(),large.size(),0));
    mbx_frame taken{};
    const auto record=cost([&]{ASSERT_EQ(mbx_rx_take(MBX_CH_SRP,&taken),MBX_STATUS_OK);});
    check("SRP maximum RX record bound",record,SRP_MBX_RX_RECORD_MAX);
    ASSERT_TRUE(mbx_model_rx(&model,large.data(),large.size(),0));
    const auto pass=cost([&]{ctrl_loop_service(&loop);});
    ASSERT_GT(pass,record);
    check("SRP complete pass bound",pass,SRP_MBX_PASS_MAX);
}
} // namespace
