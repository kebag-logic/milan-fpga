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
