// PROBE (not committed): the Domain's own leave and join on the same path.
TEST_F(Talker, ProbeDomainLeaveAndJoinOnTheRefusedPath) {
    settle(); gate(1u,kBaseA); advance(400);
    for (unsigned k=0;k<2000u && (adapter.join_left[0]!=0u || adapter.tx_due!=0u);++k) advance(1);
    ASSERT_EQ(adapter.join_left[0],0u);
    collect();
    const uint32_t first=model.tx_sent;
    receive_before_poll(domains({6,4,0,3},1,true,{6,4,0,5},4));
    ASSERT_TRUE(adapter.ifs[0].domain_owed);
    ASSERT_TRUE(srp_mbx_gate(&adapter,0,0u,kBaseA));
    std::vector<void*> held;
    while (void *p=ctrl_pool_alloc(&pool,1)) held.push_back(p);
    fill_ring();
    loop.transmit(loop.transmit_ctx);
    ASSERT_NE(adapter.owed_len,0u);
    ASSERT_EQ(adapter.ifs[0].domain.vid,3u);
    const uint32_t at=model.now_ms;
    for (void *p:held) ctrl_pool_free(&pool,p);
    mbx_model_tx_pause(&model,false);
    collect();
    advance_to(at+25000u);
    collect();
    unsigned v2_declared=0, v2_left=0, v3_declared=0, v3_left=0;
    uint32_t last_v2=0;
    for (const auto &d:seen) {
        if (d.interface!=0 || d.ethertype!=0x22ea || d.type!=4 || d.frame<first) continue;
        const unsigned vid=wire_be16(d.value.data()+2);
        std::cerr<<"PROBE domain t="<<d.time_ms<<" prio="<<unsigned(d.value[1])<<" vid="<<vid<<" event="<<d.event<<" la="<<d.leaveall<<"\n";
        if (vid==2) { if (declares(d.event)) { ++v2_declared; last_v2=d.time_ms; } if (d.event==5u) ++v2_left; }
        if (vid==3) { if (declares(d.event)) ++v3_declared; if (d.event==5u) ++v3_left; }
    }
    std::cerr<<"PROBE summary from t="<<at<<" to "<<model.now_ms<<": vid2 declared "<<v2_declared<<" (last "<<last_v2<<") left "<<v2_left<<"; vid3 declared "<<v3_declared<<" left "<<v3_left<<"; adapter domain vid "<<adapter.ifs[0].domain.vid<<" owed "<<adapter.ifs[0].domain_owed<<"\n";
    EXPECT_EQ(v3_declared,0u) << "PROBE: the adopted Domain is never declared";
    EXPECT_GT(v2_declared,0u) << "PROBE: the old Domain stays declared";
    EXPECT_EQ(v2_left,0u) << "PROBE: the old Domain is never withdrawn";
}
