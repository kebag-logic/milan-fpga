// R529-1 independent public-contract probes. Included fixture is the exact-head standing test.
#include "test_maap_mbx.cpp"

TEST(ReviewApp, AcceptedMaapMustWakeIdleLoop) {
    mbx_model model{}; mbx_model_reset(&model); mbx_model_bind(&model, nullptr, nullptr);
    std::array<std::uint8_t, 1024> arena{};
    const ctrl_pool_class classes[] = {{64, 4}};
    adp_entity entity{}; entity.mac=kMac; entity.entity_id=1; entity.talker_stream_sources=8;
    ctrl_app_config config{&entity,0,arena.data(),arena.size(),classes,1,nullptr,nullptr};
    ctrl_app app{};
    for (unsigned k=0;k<MBX_N_IF;++k) mbx_model_set_link(&model,k,true);
    ASSERT_TRUE(ctrl_app_start_maap(&app,&config,[](void*,unsigned,std::uint64_t,std::uint16_t,bool){},nullptr,kBase));
    for (unsigned n=0;n<8 && ctrl_loop_service(&app.loop);++n) {}
    ASSERT_FALSE(mbx_model_irq(&model));
    auto f=incoming(1);
    ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),0));
    std::printf("APP WAKE interfaces=%u filter=0x%x irq_enable=0x%x maap_rx_words=%u irq=%u\n",
        MBX_N_IF, model.filter_en,model.irq_enable,
        model.ch[MBX_CH_MAAP].rx_head-model.ch[MBX_CH_MAAP].rx_tail,mbx_model_irq(&model));
    EXPECT_TRUE(mbx_model_irq(&model)) << "accepted MAAP RX must wake the sleeping event loop";
    // Runtime positive control, outside source: adding precisely the missing channel bit raises IRQ.
    mbx_irq_enable(model.irq_enable | (1u << (MBX_IRQ_ENABLE_RX_LSB + MBX_CH_MAAP)));
    EXPECT_TRUE(mbx_model_irq(&model)) << "positive control with MAAP interrupt enabled";
    ctrl_loop_service(&app.loop);
    EXPECT_EQ(app.maap.ifs[0].core.conflicts,1u) << "the published input is otherwise serviceable";
    maap_mbx_stop(&app.maap);
}
