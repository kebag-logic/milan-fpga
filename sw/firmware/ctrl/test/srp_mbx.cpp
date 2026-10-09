// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "srp_fixture.hpp"
FW_TALLY_LABEL("ctrl SRP mailbox");
namespace {
std::vector<uint8_t> talker_value(const msrp_stream_id &sid, const uint8_t da[6], uint16_t vid) {
    std::vector<uint8_t> value(25);
    std::copy(sid.bytes,sid.bytes+8,value.begin());
    std::copy(da,da+6,value.begin()+8);
    wire_put_be(value.data()+14,vid,2);
    wire_put_be(value.data()+16,224,2);
    wire_put_be(value.data()+18,1,2);
    value[20]=0x60;
    return value;
}

// ---- the publication block (lane F-INT; #665 comment 6088423771) -----------------

mbx_model_pub pub_of(const mbx_model &m, unsigned i) {
    mbx_model_pub v;
    mbx_model_pub_view(&m,i,&v);
    return v;
}

// The publication block as the fabric held it when each SRP record was
// committed: the trace sees a write before the model applies it, so the
// snapshot at a TX_HEAD write is what the datapath read while that frame left.
struct Commit {
    uint32_t frame;
    mbx_model_pub pub[MBX_N_IF];
};
std::vector<Commit> commits_seen;
const mbx_model *traced_model;

void commit_trace(void *, bool write, uint32_t off, uint32_t) {
    if (write && off==MBX_CH_BASE+MBX_CH_STRIDE*MBX_CH_SRP+MBX_CH_REG_TX_HEAD) {
        Commit c{traced_model->tx_sent,{}};
        for (unsigned i=0;i<MBX_N_IF;++i) mbx_model_pub_view(traced_model,i,&c.pub[i]);
        commits_seen.push_back(c);
    }
}

const Commit *commit_of(uint32_t frame) {
    for (const auto &c:commits_seen) if (c.frame==frame) return &c;
    return nullptr;
}

// Source 0, the one allocated, admitted at 1 Gb/s: (224 + 22 + 20) bytes, 8 bits,
// 8000 frames/s (srp_mbx.c's admission, Ethernet overhead included).
constexpr uint32_t kAdmittedBps=17024000u;

TEST_F(Srp, PubDomainPrecedesEveryDeclarationThatCarriesIt) {
    settle();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto v=pub_of(model,i);
        EXPECT_TRUE(!v.adopted && v.priority==3u && v.vid==2u)
            << "PUB the default Domain {priority 3, VID 2}, not adopted, from startup";
    }
    commits_seen.clear(); traced_model=&model; mbx_host_trace(commit_trace,nullptr);
    offer(frame(4,{6,4,0,3},0)); advance(200);
    mbx_model_set_link(&model,0,false); settle(); mbx_model_set_link(&model,0,true); settle();
    const uint32_t restarted=model.tx_sent;
    advance(200);
    mbx_host_trace(nullptr,nullptr);
    capture();
    unsigned adopted=0, restored=0;
    for (const auto &d:declarations) {
        if (d.interface!=0 || d.ethertype!=0x22ea || commit_of(d.frame)==nullptr) continue;
        const auto &p=commit_of(d.frame)->pub[0];
        const bool new_vid=d.value==std::vector<uint8_t>({6,4,0,3}) ||
                           (d.type==1 && wire_be16(d.value.data()+14)==3u);
        if (new_vid && d.frame<restarted) {
            ++adopted;
            EXPECT_TRUE(p.adopted && p.priority==4u && p.vid==3u)
                << "PUB an MRPDU carrying the adopted Domain or its VID left after SR_DOMAIN published it";
        }
        if (d.type==4 && d.value==std::vector<uint8_t>({6,3,0,2}) && d.frame>=restarted) {
            ++restored;
            EXPECT_TRUE(!p.adopted && p.priority==3u && p.vid==2u)
                << "PUB after a link restart, the default Domain is published before it is declared again";
        }
    }
    EXPECT_GT(adopted,0u) << "PUB the adopted Domain was declared";
    EXPECT_GT(restored,0u) << "PUB the default Domain was declared again after the restart";
    for (unsigned i=1;i<MBX_N_IF;++i) {
        const auto v=pub_of(model,i);
        EXPECT_TRUE(!v.adopted && v.priority==3u && v.vid==2u) << "PUB another interface keeps its own Domain";
    }
}

TEST_F(Srp, PubLicenceIsSetAndClearedBeforeEachChangeIsReported) {
    settle();
    unsigned seen=0xFFFFu;
    for (unsigned i=0;i<MBX_N_IF;++i) {
        auto look=[&,i](unsigned,unsigned,bool) { seen=pub_of(model,i).licence; };
        EXPECT_EQ(pub_of(model,i).licence,0u) << "PUB no licence before a Listener Ready";
        EXPECT_CALL(licence,Change(i,0,true)).WillOnce(look); offer(frame(3,identity(i),1,2),i);
        EXPECT_EQ(seen,1u) << "PUB LICENCE holds source 0's bit before the licence is reported";
        EXPECT_CALL(licence,Change(i,0,false)).WillOnce(look); offer(frame(3,identity(i),5,2),i);
        EXPECT_EQ(seen,0u) << "PUB LICENCE clears source 0's bit before the revocation is reported";
        EXPECT_CALL(licence,Change(i,0,true)).WillOnce(look); offer(frame(3,identity(i),1,2),i);
        EXPECT_CALL(licence,Change(i,0,false)).WillOnce(look);
        mbx_model_set_link(&model,i,false); settle();
        EXPECT_EQ(seen,0u) << "PUB a link loss clears LICENCE before the revocation is reported";
        mbx_model_set_link(&model,i,true); settle();
        ASSERT_TRUE(::testing::Mock::VerifyAndClearExpectations(&licence));
    }
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),1,2),i);
    }
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,false)).WillOnce([&,i](unsigned,unsigned,bool) {
            seen=pub_of(model,i).licence;
            EXPECT_EQ(seen,0u) << "PUB destroy clears LICENCE before any revocation is reported";
        });
    }
    srp_mbx_destroy(&adapter);
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
}

TEST_F(Srp, PubIdleSlopeIsPublishedBeforeTheDeclarationsItAdmits) {
    settle();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(pub_of(model,i).idle_slope,kAdmittedBps) << "PUB IDLE_SLOPE is the admitted bandwidth from startup";
    }
    const unsigned last=MBX_N_IF-1u;
    // a value the firmware did not write, then a link restart: the slope is
    // published again before the restart's first declaration leaves
    mbx_model_write(&model,MBX_PUB_BASE+MBX_PUB_STRIDE*last+MBX_PUB_REG_IDLE_SLOPE,0u,0xFu);
    ASSERT_EQ(pub_of(model,last).idle_slope,0u);
    commits_seen.clear(); traced_model=&model; mbx_host_trace(commit_trace,nullptr);
    const uint32_t first=model.tx_sent;
    mbx_model_set_link(&model,last,false); settle(); mbx_model_set_link(&model,last,true); settle();
    advance(200);
    mbx_host_trace(nullptr,nullptr);
    unsigned left=0;
    for (const auto &c:commits_seen) {
        const auto *f=mbx_model_tx_frame(&model,c.frame);
        if (c.frame<first || f==nullptr || f->interface!=last) continue;
        ++left;
        EXPECT_EQ(c.pub[last].idle_slope,kAdmittedBps)
            << "PUB every MRPDU of the restarted interface left with IDLE_SLOPE published again";
    }
    EXPECT_GT(left,0u) << "PUB the restarted interface declared again";
}

TEST_F(Srp, StartupDeclaresTalkersDomainAndVlan) {
    settle();
    ASSERT_EQ(pool.refused,0u);
    EXPECT_EQ(adapter.transmitted,2u*MBX_N_IF);
    advance(400);
    EXPECT_EQ(adapter.transmitted,5u*MBX_N_IF);
    capture();
    for(unsigned i=0;i<MBX_N_IF;++i) {
        for(unsigned type=1;type<=4;++type) {
            if(type==3) continue;
            unsigned count=0;
            for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea && d.type==type) {
                ASSERT_LT(count,3u); const unsigned events[]={0,0,3};
                EXPECT_EQ(d.event,events[count]); EXPECT_EQ(d.time_ms,200*count); ++count;
                if(type==4) EXPECT_EQ(d.value,(std::vector<uint8_t>{6,3,0,2}));
                else {
                    const unsigned index=type==1 ? 0 : 1;
                    EXPECT_TRUE(std::equal(d.value.begin(),d.value.begin()+8,identity(i,index).begin()));
                    EXPECT_EQ(wire_be16(d.value.data()+14),2u);
                    EXPECT_EQ(wire_be16(d.value.data()+16),224u);
                    EXPECT_EQ(wire_be16(d.value.data()+18),1u);
                    EXPECT_EQ(d.value[20],0x60u);
                    if(type==2) { EXPECT_EQ(d.value[33],2u); }
                }
            }
            EXPECT_EQ(count,3u);
        }
        unsigned count=0;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x88f5) {
            EXPECT_EQ(d.type,1u); EXPECT_EQ(d.event,3u); EXPECT_EQ(d.time_ms,200*count);
            EXPECT_EQ(d.value,(std::vector<uint8_t>{0,2})); ++count;
        }
        EXPECT_EQ(count,2u);
    }
}
TEST_F(Srp, LeaveAfterLeaveAllStopsAtOriginalFiveSecondDeadline) {
    settle();
    EXPECT_CALL(licence,Change(0,0,true));
    offer(frame(3,identity(),0,2));
    offer(frame(3,identity(),4,2,true));
    advance(2000);
    offer(frame(3,identity(),5,2));
    advance(2990);
    EXPECT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false));
    advance(10);
    EXPECT_FALSE(adapter.ifs[0].active[0]);
    EXPECT_EQ(adapter.stops,1u);
    advance(1000);
    offer(frame(3,identity(),5,2));
    EXPECT_EQ(adapter.stops,1u);
}
TEST_F(Srp, RegisteredListenerSubtypeChangeRevokesPermission) {
    settle();
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),1,2));
    EXPECT_CALL(licence,Change(0,0,false)); offer(frame(3,identity(),1,1));
    EXPECT_FALSE(adapter.ifs[0].active[0]);
}
TEST_F(Srp, InterfaceStateDoesNotCross) {
    settle();
    for(unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),0,2),i);
    }
    for(unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,false));
        mbx_model_set_link(&model,i,false); settle();
        EXPECT_FALSE(adapter.ifs[i].active[0]);
        for(unsigned k=i+1;k<MBX_N_IF;++k) EXPECT_TRUE(adapter.ifs[k].active[0]);
        mbx_model_set_link(&model,i,true); settle();
        EXPECT_FALSE(adapter.ifs[i].active[0]);
    }
}

TEST_F(Srp, SinkPortUsesMatchingRegisteredTalkerAndRetainsLeaveTimer) {
    settle();
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const uint8_t da[]= {
        0x91,0xe0,0xf0,0,0,9
    };
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
    std::vector<uint8_t> talker(25);
    std::copy(sid.bytes,sid.bytes+8,talker.begin());
    std::copy(da,da+6,talker.begin()+8);
    wire_put_be(talker.data()+14,2,2);
    wire_put_be(talker.data()+16,224,2); wire_put_be(talker.data()+18,1,2); talker[20]=0x60;
    offer(frame(1,talker,0));
    advance(200); capture();
    bool ready=false;
    for(const auto &d:declarations) if(d.type==3 && d.ethertype==0x22ea) {
        EXPECT_EQ(d.subtype,2u); EXPECT_TRUE(std::equal(d.value.begin(),d.value.end(),sid.bytes)); ready=true;
    }
    EXPECT_TRUE(ready);
    auto failed=talker; failed.resize(34); failed[33]=1;
    offer(frame(2,failed,0)); advance(200); capture();
    EXPECT_EQ(adapter.ifs[0].sinks[0].declared,1u);
    bool asking=false;
    for(const auto &d:declarations) if(d.type==3 && d.subtype==1) asking=true;
    EXPECT_TRUE(asking);
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0));
    advance(200); capture();
    bool left=false;
    for(const auto &d:declarations) if(d.type==3 && d.event==5) left=true;
    EXPECT_TRUE(left);
}
TEST_F(Srp, DomainUsesPeerPriorityAndVlan) {
    settle();
    offer(frame(4,{6,4,0,3},0)); advance(200); capture();
    EXPECT_EQ(adapter.ifs[0].domain.priority,4u); EXPECT_EQ(adapter.ifs[0].domain.vid,3u);
    bool domain=false; bool talker=false; bool vlan=false;
    for(const auto &d:declarations) {
        if(d.ethertype==0x22ea && d.type==4 && d.value==std::vector<uint8_t>({6,4,0,3})) domain=true;
        if(d.ethertype==0x22ea && d.type==1 && wire_be16(d.value.data()+14)==3 && d.value[20]==0x80) talker=true;
        if(d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,3})) vlan=true;
    }
    EXPECT_TRUE(domain); EXPECT_TRUE(talker); EXPECT_TRUE(vlan);
}
TEST_F(Srp, RefusedMailboxRetainsOwedFrameAndDefersInput) {
    mbx_model_tx_pause(&model,true);
    std::vector<uint8_t> filler(60); wire_put_be(filler.data(),0x0180c200000eull,6);
    wire_put_be(filler.data()+12,0x22ea,2);
    while(mbx_tx_send(MBX_CH_SRP,0,filler.data(),filler.size())==MBX_STATUS_OK) {}
    ctrl_loop_service(&loop); ASSERT_GT(adapter.owed_len,0u);
    EXPECT_FALSE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0));
    std::vector<uint8_t> owed(adapter.owed_frame,adapter.owed_frame+adapter.owed_len);
    auto ready=frame(3,identity(),0,2);
    ASSERT_TRUE(mbx_model_rx(&model,ready.data(),ready.size(),0));
    mbx_model_advance_ms(&model,16000);
    for(unsigned n=0;n<200;++n) ctrl_loop_service(&loop);
    EXPECT_EQ(adapter.received,0u); EXPECT_FALSE(adapter.ifs[0].active[0]);
    EXPECT_EQ(owed,std::vector<uint8_t>(adapter.owed_frame,adapter.owed_frame+adapter.owed_len));
    EXPECT_CALL(licence,Change(0,0,true));
    mbx_model_tx_pause(&model,false); settle();
    EXPECT_EQ(adapter.received,1u); EXPECT_EQ(adapter.owed_len,0u);
    // The overdue MVRP LeaveAll may precede its Join-spaced membership.
    advance(200); EXPECT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false));
    mbx_model_set_link(&model,0,false); settle();
}
TEST_F(Srp, ExpiryBacklogPrecedesSamePassReceive) {
    settle(); EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),0,2));
    offer(frame(3,identity(),4,2,true));
    mbx_model_advance_ms(&model,5000);
    auto ready=frame(3,identity(),0,2);
    ASSERT_TRUE(mbx_model_rx(&model,ready.data(),ready.size(),0));
    EXPECT_CALL(licence,Change(0,0,false));
    EXPECT_CALL(licence,Change(0,0,true));
    settle();
    EXPECT_EQ(adapter.stops,1u);
    EXPECT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false)); mbx_model_set_link(&model,0,false); settle();
}

TEST_F(Srp, ReentryFromOutputIsRefusedAndCounted) {
    settle();
    EXPECT_CALL(licence,Change(0,0,true)).WillOnce([&](unsigned,unsigned,bool) {
        const unsigned before=adapter.reentries;
        const unsigned malformed=adapter.malformed;
        EXPECT_FALSE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0));
        EXPECT_FALSE(srp_mbx_bind(&adapter,MBX_N_IF,0,nullptr,nullptr,0));
        EXPECT_FALSE(srp_mbx_attach(&adapter,&loop));
        srp_mbx_destroy(&adapter);
        mbx_frame f{}; f.len=17; loop.rx[MBX_CH_SRP].fn(&adapter,&f);
        f.len=0; loop.rx[MBX_CH_SRP].fn(&adapter,&f);
        EXPECT_FALSE(loop.polls[loop.n_polls-1].fn(&adapter));
        loop.ticks[loop.n_ticks-1]();
        EXPECT_FALSE(srp_mbx_init(&adapter,&config));
        EXPECT_EQ(adapter.reentries,before+9);
        EXPECT_EQ(adapter.malformed,malformed);
    });
    offer(frame(3,identity(),0,2));
    EXPECT_TRUE(adapter.initialized); EXPECT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false)); srp_mbx_destroy(&adapter);
    EXPECT_FALSE(adapter.initialized); EXPECT_EQ(loop.n_ticks,0u); EXPECT_EQ(loop.n_polls,0u);
}
TEST_F(Srp, InvalidBindingsAndDuplicateBindingsPreserveState) {
    settle(); msrp_stream_id sid{{1,2,3,4,5,6,7,8}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,1};
    EXPECT_FALSE(srp_mbx_bind(&adapter,MBX_N_IF,0,&sid,da,2));
    EXPECT_FALSE(srp_mbx_bind(&adapter,0,CTRL_SRP_SINKS,&sid,da,2));
    EXPECT_FALSE(srp_mbx_bind(&adapter,0,0,&sid,nullptr,2));
    EXPECT_FALSE(srp_mbx_bind(&adapter,0,0,&sid,da,0));
    EXPECT_FALSE(srp_mbx_bind(&adapter,0,0,&sid,da,4095));
    EXPECT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
    const unsigned used=ctrl_pool_in_use(&pool);
    EXPECT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2)); EXPECT_EQ(ctrl_pool_in_use(&pool),used);
    sid.bytes[7]=9; EXPECT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
    da[5]=2; EXPECT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
    EXPECT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,3));
    EXPECT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0));
    srp_mbx_destroy(&adapter);
    EXPECT_FALSE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
}
TEST_F(Srp, ExhaustionDuringEachStartupStageReleasesEveryBlock) {
    srp_mbx_destroy(&adapter);
    alignas(std::max_align_t) uint8_t storage[40000];
    bool passed=false; bool refused=false;
    for(unsigned blocks=1;blocks<=40;++blocks) {
        ctrl_pool trial{}; ctrl_pool_class cls{512,static_cast<uint16_t>(blocks)};
        ASSERT_TRUE(ctrl_pool_init(&trial,storage,sizeof(storage),&cls,1)); shlan_port_bind_pool(&trial);
        srp_mbx candidate{};
        const bool ok=srp_mbx_init(&candidate,&config);
        if(ok) { passed=true; EXPECT_EQ(trial.refused,0u); }
        else { refused=true; EXPECT_GT(trial.refused,0u); EXPECT_FALSE(candidate.initialized); EXPECT_EQ(ctrl_pool_in_use(&trial),0u); }
        srp_mbx_destroy(&candidate); EXPECT_EQ(ctrl_pool_in_use(&trial),0u); EXPECT_EQ(trial.bad_frees,0u);
    }
    EXPECT_TRUE(passed); EXPECT_TRUE(refused); shlan_port_bind_pool(&pool);
}
TEST_F(Srp, MissingBootDependenciesRefuseBeforeAttachment) {
    srp_mbx_destroy(&adapter);
    srp_mbx candidate{}; auto cfg=config; cfg.licence=nullptr;
    EXPECT_FALSE(srp_mbx_init(&candidate,&cfg)); EXPECT_FALSE(srp_mbx_attach(&candidate,&loop));
    shlan_port_bind_pool(nullptr); EXPECT_FALSE(srp_mbx_init(&candidate,&config)); shlan_port_bind_pool(&pool);
    cfg=config; cfg.sources[0]=nullptr; EXPECT_FALSE(srp_mbx_init(&candidate,&cfg));
    EXPECT_EQ(ctrl_pool_in_use(&pool),0u);
}
TEST_F(Srp, AttachmentFailureIsAtomicAndDetachesAfterLoopReset) {
    settle(); EXPECT_FALSE(srp_mbx_attach(&adapter,&loop));
    EXPECT_FALSE(srp_mbx_init(&adapter,&config)); srp_mbx_destroy(&adapter);
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ctrl_loop_init(&loop); loop.n_ticks=CTRL_LOOP_MAX_TICKS;
    EXPECT_FALSE(srp_mbx_attach(&adapter,&loop)); EXPECT_EQ(loop.n_polls,0u);
    ctrl_loop_init(&loop); loop.n_polls=CTRL_LOOP_MAX_POLLS;
    EXPECT_FALSE(srp_mbx_attach(&adapter,&loop)); EXPECT_EQ(loop.n_ticks,0u);
    ctrl_loop_init(&loop); ctrl_loop_bind_rx(&loop,MBX_CH_SRP,[](void*,const mbx_frame*){},nullptr);
    EXPECT_FALSE(srp_mbx_attach(&adapter,&loop));
    ctrl_loop_init(&loop);
    ctrl_loop_add_tick(&loop,[](){}); ctrl_loop_add_poll(&loop,[](void*){return false;},nullptr);
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop)); srp_mbx_destroy(&adapter);
    EXPECT_EQ(loop.n_ticks,1u); EXPECT_EQ(loop.n_polls,1u);
    ASSERT_TRUE(srp_mbx_init(&adapter,&config)); ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    ctrl_loop_init(&loop); ctrl_loop_add_tick(&loop,[](){}); ctrl_loop_add_poll(&loop,[](void*){return false;},nullptr);
    srp_mbx_destroy(&adapter); EXPECT_EQ(loop.n_ticks,1u); EXPECT_EQ(loop.n_polls,1u);
    ctrl_loop_set_rx_ready(&loop,MBX_N_CH,[](void*){return false;});
}
TEST_F(Srp, InvalidFramesHaveNoReservationSideEffects) {
    settle(); const auto receive=loop.rx[MBX_CH_SRP].fn;
    mbx_frame f{}; f.interface=MBX_N_IF; receive(&adapter,&f);
    f.interface=0; f.len=16; receive(&adapter,&f);
    auto good=frame(3,identity(),0,2);
    std::copy(good.begin(),good.end(),f.bytes); f.len=good.size();
    f.bytes[12]=0x99; receive(&adapter,&f);
    f.bytes[12]=0x22; f.bytes[5]=9; receive(&adapter,&f);
    f.bytes[5]=0x0e; f.bytes[14+15]=216; receive(&adapter,&f);
    EXPECT_EQ(adapter.malformed,5u); EXPECT_EQ(adapter.received,0u); EXPECT_FALSE(adapter.ifs[0].active[0]);
}
TEST_F(Srp, ExhaustedPoolStillReusesOwnedBlocksOnLinkReset) {
    settle(); EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),0,2));
    std::vector<void*> held;
    while(void *p=ctrl_pool_alloc(&pool,1)) { held.push_back(p); }
    const unsigned refused=pool.refused;
    EXPECT_CALL(licence,Change(0,0,false)); mbx_model_set_link(&model,0,false); settle();
    EXPECT_FALSE(adapter.ifs[0].active[0]); EXPECT_EQ(adapter.refused,0u);
    mbx_model_set_link(&model,0,true); settle();
    EXPECT_EQ(pool.refused,refused); EXPECT_FALSE(adapter.ifs[0].active[0]);
    EXPECT_NE(adapter.ifs[0].msrp,nullptr); EXPECT_NE(adapter.ifs[0].mvrp,nullptr);
    for(void *p:held) { ctrl_pool_free(&pool,p); }
}

TEST_F(Srp, ReadyFailedAndUninterestingStreamsAreSeparated) {
    settle(); offer(frame(3,identity(),1,1)); EXPECT_FALSE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),1,3));
    const unsigned before=ctrl_pool_in_use(&pool);
    offer(frame(3,{7,7,7,7,7,7,7,7},0,2));
    std::vector<uint8_t> unknown(25,0); unknown[7]=7;
    offer(frame(1,unknown,0)); EXPECT_EQ(ctrl_pool_in_use(&pool),before);
    EXPECT_CALL(licence,Change(0,0,false)); mbx_model_set_link(&model,0,false); settle();
}
TEST_F(Srp, DomainFilterAndDuplicateDoNotGrowDeclarations) {
    settle(); offer(frame(4,{6,3,0,2},0));
    const unsigned before=ctrl_pool_in_use(&pool);
    offer(frame(4,{5,2,0,2},0)); offer(frame(4,{6,3,0,0},0));
    offer(frame(4,{6,3,15,255},0)); offer(frame(4,{6,8,0,2},0));
    EXPECT_EQ(adapter.ifs[0].domain.priority,3u);
    EXPECT_FALSE(adapter.ifs[0].domain_owed); EXPECT_EQ(ctrl_pool_in_use(&pool),before);
}
TEST_F(Srp, MvrpAcceptsOnlyCurrentDomainVid) {
    settle();
    std::vector<uint8_t> f(26);
    wire_put_be(f.data(),0x0180c2000021ull,6); wire_put_be(f.data()+6,0x020304000009ull,6);
    wire_put_be(f.data()+12,0x88f5,2);
    const uint8_t pdu[]= {
        0,1,2,0,1,0,2,0,0,0,0,0
    };
    std::copy(pdu,pdu+12,f.begin()+14); offer(f);
    advance(1000); capture();
    bool joinin=false; for(const auto &d:declarations) if(d.ethertype==0x88f5 && d.event==1) joinin=true;
    EXPECT_TRUE(joinin);
    const unsigned count=ctrl_pool_in_use(&pool);
    f[20]=3; offer(f); EXPECT_EQ(ctrl_pool_in_use(&pool),count);
    mbx_frame invalid{}; invalid.len=f.size(); std::copy(f.begin(),f.end(),invalid.bytes);
    invalid.bytes[5]=0x22; loop.rx[MBX_CH_SRP].fn(&adapter,&invalid);
    EXPECT_EQ(adapter.malformed,1u);
}
TEST_F(Srp, WireMismatchesCannotAdmitBoundSinkAndLeaveExpiresIt) {
    settle();
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; msrp_stream_id other{{2,1,2,3,4,5,6,8}};
    uint8_t da[]= {
        0x91,0xe0,0xf0,0,0,1
    };
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&other,da,2));
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,&sid,da,2));
    std::vector<uint8_t> talker(25); std::copy(sid.bytes,sid.bytes+8,talker.begin());
    std::copy(da,da+6,talker.begin()+8); wire_put_be(talker.data()+14,2,2);
    wire_put_be(talker.data()+16,224,2); wire_put_be(talker.data()+18,1,2); talker[20]=0x60;
    talker[13]=2; offer(frame(1,talker,0)); EXPECT_EQ(adapter.ifs[0].sinks[1].declared,0u);
    talker[13]=1; talker[15]=3; offer(frame(1,talker,0)); EXPECT_EQ(adapter.ifs[0].sinks[1].declared,0u);
    talker[15]=2; offer(frame(1,talker,0)); EXPECT_EQ(adapter.ifs[0].sinks[1].declared,2u);
    offer(frame(1,talker,5)); advance(5000);
    EXPECT_EQ(adapter.ifs[0].sinks[1].declared,0u);
}
TEST_F(Srp, AdmissionUsesBandwidthAndEthernetMinimum) {
    srp_mbx_destroy(&adapter);
    config.link_rate_bps=1000000;
    sources[0][0].value.max_frame_size=1; sources[0][0].value.max_interval_frames=1;
    sources[0][1].allocated=true; sources[0][1].value.max_interval_frames=0;
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    EXPECT_FALSE(adapter.ifs[0].admitted[0]); EXPECT_FALSE(adapter.ifs[0].admitted[1]);
}
TEST_F(Srp, DomainExhaustionPreservesOldDeclarationUntilRetry) {
    settle(); advance(400);
    receive_before_poll(frame(4,{6,4,0,3},0));
    std::vector<void*> held; while(void *p=ctrl_pool_alloc(&pool,1)) { held.push_back(p); }
    ASSERT_GE(held.size(),2u);
    ctrl_loop_service(&loop);
    EXPECT_GT(adapter.refused,0u); EXPECT_EQ(adapter.ifs[0].domain.vid,2u);
    EXPECT_TRUE(adapter.ifs[0].domain_owed);
    ctrl_pool_free(&pool,held.back()); held.pop_back(); settle();
    EXPECT_EQ(adapter.ifs[0].domain.vid,3u); EXPECT_FALSE(adapter.ifs[0].domain_owed);
    for(void *p:held) { ctrl_pool_free(&pool,p); }
}
TEST_F(Srp, SinkDeclarationExhaustionRetriesWithoutLosingBinding) {
    settle(); advance(400);
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,1};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
    std::vector<uint8_t> talker(25); std::copy(sid.bytes,sid.bytes+8,talker.begin());
    std::copy(da,da+6,talker.begin()+8); wire_put_be(talker.data()+14,2,2);
    wire_put_be(talker.data()+16,224,2); wire_put_be(talker.data()+18,1,2); talker[20]=0x60;
    receive_before_poll(frame(1,talker,0));
    std::vector<void*> held; while(void *p=ctrl_pool_alloc(&pool,1)) { held.push_back(p); }
    ASSERT_GE(held.size(),2u);
    ctrl_loop_service(&loop);
    EXPECT_GT(adapter.refused,0u); EXPECT_EQ(adapter.ifs[0].sinks[0].declared,0u);
    EXPECT_TRUE(adapter.ifs[0].sinks[0].bound);
    ctrl_pool_free(&pool,held.back()); held.pop_back(); settle();
    EXPECT_EQ(adapter.ifs[0].sinks[0].declared,2u);
    for(void *p:held) { ctrl_pool_free(&pool,p); }
}
TEST_F(Srp, LinkLossCancelsItsOwedFrameOnly) {
    settle(); advance(400); mbx_model_tx_pause(&model,true);
    std::vector<uint8_t> filler(60); wire_put_be(filler.data(),0x0180c200000eull,6); wire_put_be(filler.data()+12,0x22ea,2);
    while(mbx_tx_send(MBX_CH_SRP,0,filler.data(),filler.size())==MBX_STATUS_OK) {}
    mbx_model_advance_ms(&model,600); for(unsigned n=0;n<100;++n) ctrl_loop_service(&loop);
    ASSERT_GT(adapter.owed_len,0u);
    const unsigned waiting=adapter.owed_if;
    if(MBX_N_IF>1) {
        const unsigned other=1-waiting;
        mbx_model_set_link(&model,other,false); mbx_model_set_link(&model,other,true);
        ctrl_loop_service(&loop);
        EXPECT_GT(adapter.owed_len,0u); EXPECT_EQ(adapter.owed_if,waiting);
        mbx_model_set_link(&model,other,false); ctrl_loop_service(&loop);
    }
    mbx_model_set_link(&model,waiting,false); ctrl_loop_service(&loop);
    EXPECT_EQ(adapter.owed_len,0u);
    mbx_model_tx_pause(&model,false); settle();
}

TEST_F(Srp, OneLoopOwnsTheGlobalCentisecondDispatch) {
    srp_mbx_destroy(&adapter);
    alignas(std::max_align_t) uint8_t storage[30000];
    ctrl_pool shared{}; ctrl_pool_class cls{512,50};
    ASSERT_TRUE(ctrl_pool_init(&shared,storage,sizeof(storage),&cls,1)); shlan_port_bind_pool(&shared);
    srp_mbx first{}; srp_mbx second{}; ctrl_loop first_loop{}; ctrl_loop second_loop{};
    ASSERT_TRUE(srp_mbx_init(&first,&config)); ASSERT_TRUE(srp_mbx_init(&second,&config));
    ASSERT_TRUE(srp_mbx_attach(&first,&first_loop)); EXPECT_FALSE(srp_mbx_attach(&second,&second_loop));
    EXPECT_EQ(second_loop.n_ticks,0u); EXPECT_EQ(second_loop.n_polls,0u);
    srp_mbx_destroy(&first); EXPECT_TRUE(srp_mbx_attach(&second,&second_loop));
    srp_mbx_destroy(&second); EXPECT_EQ(ctrl_pool_in_use(&shared),0u); shlan_port_bind_pool(&pool);
}

TEST_F(Srp, ListenerBeforeVlanCommitCannotStartTalker) {
    EXPECT_CALL(licence,Change(0,0,true)).WillOnce([&](unsigned,unsigned,bool) {
        bool joined=false;
        for(unsigned n=0;n<model.tx_sent;++n) {
            const auto *f=mbx_model_tx_frame(&model,n);
            if(f && f->interface==0 && wire_be16(f->bytes+12)==0x88f5) joined=true;
        }
        EXPECT_TRUE(joined)<<"MVRP Join must commit before the talker licence";
    });
    offer(frame(3,identity(),0,2));
    EXPECT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false)); mbx_model_set_link(&model,0,false); settle();
}

TEST_F(Srp, SharedBindingsRetainTheListenerAndVlanUntilTheLastUnbind) {
    settle(); advance(400);
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    std::vector<uint8_t> talker(25); std::copy(sid.bytes,sid.bytes+8,talker.begin());
    std::copy(da,da+6,talker.begin()+8); wire_put_be(talker.data()+14,7,2);
    wire_put_be(talker.data()+16,224,2); wire_put_be(talker.data()+18,1,2); talker[20]=0x60;
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,7)); offer(frame(1,talker,0));
    advance(200); EXPECT_EQ(adapter.ifs[0].sinks[0].declared,2u);
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,&sid,da,7)); settle();
    EXPECT_EQ(adapter.ifs[0].sinks[1].declared,2u);
    advance(200); const unsigned first=model.tx_sent;
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0)); advance(200); capture();
    for(const auto &d:declarations) if(d.time_ms>=1000 && d.ethertype==0x22ea && d.type==3) {
        EXPECT_NE(d.event,5u)<<"one remaining binding retains the Listener";
    }
    EXPECT_TRUE(adapter.ifs[0].sinks[1].vlan_sent);
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,nullptr,nullptr,0)); advance(200); capture();
    bool vlan_left=false; bool listener_left=false;
    for(const auto &d:declarations) if(d.event==5 && d.time_ms>=1000) {
        vlan_left|=d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,7});
        listener_left|=d.ethertype==0x22ea && d.type==3;
    }
    EXPECT_GT(model.tx_sent,first); EXPECT_TRUE(vlan_left); EXPECT_TRUE(listener_left);
}
TEST_F(Srp, BoundOldDomainVlanSurvivesDomainChange) {
    settle(); msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
    offer(frame(4,{6,4,0,3},0)); advance(200); capture();
    for(const auto &d:declarations) if(d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,2})) {
        EXPECT_NE(d.event,5u)<<"a bound sink retains the old Domain VID";
    }
}

TEST_F(Srp, PriorityOnlyDomainChangeKeepsVlanMembership) {
    settle(); offer(frame(4,{6,4,0,2},0)); advance(200); capture();
    EXPECT_EQ(adapter.ifs[0].domain.priority,4u);
    EXPECT_TRUE(adapter.ifs[0].vlan_sent);
    for(const auto &d:declarations) if(d.ethertype==0x88f5) {
        EXPECT_NE(d.event,5u)<<"priority-only change must not withdraw the current VID";
    }
}
TEST_F(Srp, SinkVlanExhaustionRetriesAndDistinctMembershipsRemainIndependent) {
    // Bound sinks on distinct VIDs exercise the explicit 35.1.2.2 ordering.
    settle(); advance(400);
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,7));
    std::vector<uint8_t> talker(25); std::copy(sid.bytes,sid.bytes+8,talker.begin());
    std::copy(da,da+6,talker.begin()+8); wire_put_be(talker.data()+14,7,2);
    wire_put_be(talker.data()+16,224,2); wire_put_be(talker.data()+18,1,2); talker[20]=0x60;
    receive_before_poll(frame(1,talker,0));
    std::vector<void*> held; while(void *p=ctrl_pool_alloc(&pool,1)) held.push_back(p);
    ASSERT_GE(held.size(),3u);
    ctrl_loop_service(&loop);
    EXPECT_FALSE(adapter.ifs[0].sinks[0].vlan_requested); EXPECT_GT(adapter.refused,0u);
    for(void *p:held) ctrl_pool_free(&pool,p);
    settle(); advance(200); EXPECT_EQ(adapter.ifs[0].sinks[0].declared,2u);
    sid.bytes[7]=8; talker[7]=8; talker[15]=8;
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,&sid,da,8)); offer(frame(1,talker,0)); advance(400);
    EXPECT_TRUE(adapter.ifs[0].sinks[1].vlan_sent);
    std::vector<uint8_t> vlan(26); wire_put_be(vlan.data(),0x0180c2000021ull,6); wire_put_be(vlan.data()+12,0x88f5,2);
    const uint8_t pdu[]={0,1,2,0,1,0,8,0,0,0,0,0}; std::copy(pdu,pdu+12,vlan.begin()+14);
    offer(vlan); advance(1000); capture(); bool joined8=false;
    for(const auto &d:declarations) if(d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,8}) && d.event==1) joined8=true;
    EXPECT_TRUE(joined8);
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0)); advance(200); capture();
    bool left7=false;
    for(const auto &d:declarations) if(d.ethertype==0x88f5 && d.event==5) {
        EXPECT_NE(d.value,std::vector<uint8_t>({0,8})); left7|=d.value==std::vector<uint8_t>({0,7});
    }
    EXPECT_TRUE(left7); EXPECT_TRUE(adapter.ifs[0].sinks[1].vlan_sent);
}

TEST_F(Srp, SinkMembershipCommitsBeforeReadyAtStartup) {
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
    std::vector<uint8_t> talker(25); std::copy(sid.bytes,sid.bytes+8,talker.begin());
    std::copy(da,da+6,talker.begin()+8); wire_put_be(talker.data()+14,2,2);
    wire_put_be(talker.data()+16,224,2); wire_put_be(talker.data()+18,1,2); talker[20]=0x60;
    offer(frame(1,talker,0)); advance(200); capture();
    bool joined=false; bool ready=false;
    for(const auto &d:declarations) {
        if(d.ethertype==0x88f5 && (d.event==1 || d.event==3)) joined=true;
        if(d.ethertype==0x22ea && d.type==3 && d.subtype==2) {
            EXPECT_TRUE(joined)<<"VLAN membership commit precedes Listener Ready"; ready=true;
        }
    }
    EXPECT_TRUE(ready);
}

TEST_F(Srp, InListenerWithdrawalRevokesLicenceImmediately) {
    settle();
    for(unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),1,2),i);
        EXPECT_CALL(licence,Change(i,0,false)); offer(frame(3,identity(i),5,2),i);
        EXPECT_FALSE(adapter.ifs[i].active[0]);
    }
    EXPECT_EQ(adapter.stops,MBX_N_IF);
    advance(5000); EXPECT_EQ(adapter.stops,MBX_N_IF);
}
TEST_F(Srp, InTalkerWithdrawalImmediatelyWithdrawsListener) {
    settle();
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    uint8_t da[]={
        0x91,0xe0,0xf0,0,0,9
    };
    std::vector<uint8_t> talker(25);
    std::copy(sid.bytes,sid.bytes+8,talker.begin());
    std::copy(da,da+6,talker.begin()+8); wire_put_be(talker.data()+14,2,2);
    for(unsigned i=0;i<MBX_N_IF;++i) {
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,&sid,da,2));
        offer(frame(1,talker,1),i); advance(200);
        ASSERT_EQ(adapter.ifs[i].sinks[0].declared,2u);
        const auto withdrew=model.now_ms;
        offer(frame(1,talker,5),i);
        EXPECT_EQ(adapter.ifs[i].sinks[0].declared,0u);
        advance(200); capture();
        bool left=false;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea &&
            d.type==3 && d.event==5 && d.time_ms>=withdrew && d.time_ms<=withdrew+200) left=true;
        EXPECT_TRUE(left);
    }
}
TEST_F(Srp, ReadyToReadyFailedNeverGlitchesAnActiveLicence) {
    settle();
    for(unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),1,2),i);
        ASSERT_TRUE(::testing::Mock::VerifyAndClearExpectations(&licence));
        offer(frame(3,identity(i),1,3),i);
        EXPECT_TRUE(adapter.ifs[i].active[0]); EXPECT_EQ(adapter.stops,0u);
    }
    for(unsigned i=0;i<MBX_N_IF;++i) EXPECT_CALL(licence,Change(i,0,false));
}
TEST_F(Srp, AdmissionStraddlesTheExactEthernetCeiling) {
    // 224 payload + 22 tagged header/FCS + 20 preamble/IFG, 8000 frames/s.
    // The independent on-wire charge is 17,024,000 bps.
    for(uint32_t rate : {22698667u,22698666u}) {
        srp_mbx_destroy(&adapter); config.link_rate_bps=rate;
        ASSERT_TRUE(srp_mbx_init(&adapter,&config));
        for(unsigned i=0;i<MBX_N_IF;++i) EXPECT_EQ(adapter.ifs[i].admitted[0],rate==22698667u);
    }
}
TEST_F(Srp, AdjacentLinkEdgesResetDomainAndAllPriorRegistrations) {
    settle();
    for(unsigned i=0;i<MBX_N_IF;++i) {
        offer(frame(4,{6,4,0,3},0),i); advance(200);
        EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),1,2),i);
    }
    for(unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,false));
        mbx_model_set_link(&model,i,false); mbx_model_set_link(&model,i,true); settle();
        EXPECT_EQ(adapter.ifs[i].domain.priority,3u); EXPECT_EQ(adapter.ifs[i].domain.vid,2u);
        EXPECT_FALSE(adapter.ifs[i].active[0]);
        for(unsigned other=i+1;other<MBX_N_IF;++other) EXPECT_TRUE(adapter.ifs[other].active[0]);
        advance(200); EXPECT_FALSE(adapter.ifs[i].active[0]);
    }
}
TEST_F(Srp, OldReceiveBacklogCannotRegisterAcrossLinkRestart) {
    settle(); advance(400);
    for(unsigned i=0;i<MBX_N_IF;++i) {
        auto ready=frame(3,identity(i),1,2);
        for(unsigned k=0;k<CTRL_LOOP_RX_PER_PASS+1;++k)
            ASSERT_TRUE(mbx_model_rx(&model,ready.data(),ready.size(),i));
        mbx_model_set_link(&model,i,false); mbx_model_set_link(&model,i,true);
        settle(); advance(200);
        EXPECT_FALSE(adapter.ifs[i].active[0]);
        EXPECT_CALL(licence,Change(i,0,true)); offer(ready,i);
        EXPECT_TRUE(adapter.ifs[i].active[0]);
        EXPECT_CALL(licence,Change(i,0,false));
        mbx_model_set_link(&model,i,false); settle();
        offer(ready,i); EXPECT_FALSE(adapter.ifs[i].registered[0]);
    }
}
TEST_F(Srp, SharedIdentityReconcilesBothBindingOrdersOnTheWire) {
    settle();
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    uint8_t da[2][6]={
        {0x91,0xe0,0xf0,0,0,8}, {0x91,0xe0,0xf0,0,0,9}
    };
    for(bool different_vlan : {false,true}) for(unsigned first : {0u,1u}) {
        // Preserve protocol state; start a fresh bounded capture window.
        capture(); model.tx_sent=0; declarations.clear();
        const uint16_t vid[2]={2,static_cast<uint16_t>(different_vlan ? 7 : 2)};
        for(unsigned k=0;k<2;++k) ASSERT_TRUE(srp_mbx_bind(&adapter,0,k,&sid,da[k],vid[k]));
        std::vector<uint8_t> talker(25); std::copy(sid.bytes,sid.bytes+8,talker.begin());
        wire_put_be(talker.data()+14,2,2);
        for(unsigned k : {first,1-first}) {
            std::copy(da[k],da[k]+6,talker.begin()+8); wire_put_be(talker.data()+14,vid[k],2);
            const unsigned start=model.now_ms;
            offer(frame(1,talker,1)); advance(1200); capture();
            unsigned last=99;
            for(const auto &d:declarations) if(d.ethertype==0x22ea && d.type==3 && d.time_ms>=start) {
                last=d.event; EXPECT_EQ(d.subtype,2u);
            }
            EXPECT_NE(last,99u); EXPECT_NE(last,5u);
        }
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,first,nullptr,nullptr,0));
        advance(200);
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,1-first,nullptr,nullptr,0));
        const unsigned start=model.now_ms; advance(200); capture();
        bool left=false;
        for(const auto &d:declarations) if(d.ethertype==0x22ea && d.type==3 && d.event==5 && d.time_ms>=start) left=true;
        EXPECT_TRUE(left);
    }
}

TEST_F(Srp, RecreateAllocationFailureIsCountedAndRetried) {
    settle();
    for(int failure : {0,3,6}) {
        calloc_before_failure=failure;
        const unsigned refused=adapter.refused;
        mbx_model_set_link(&model,0,false);
        ctrl_loop_service(&loop);
        EXPECT_GT(adapter.refused,refused); EXPECT_EQ(adapter.ifs[0].msrp,nullptr);
        EXPECT_EQ(adapter.ifs[0].mvrp,nullptr);
        EXPECT_GT(ctrl_loop_service(&loop),0u);
        if(MBX_N_IF>1) {
            capture(); const auto start=model.now_ms;
            adapter.cursor=0;
            for(unsigned ms=0;ms<1200;++ms) {
                mbx_model_advance_ms(&model,1); ctrl_loop_service(&loop); capture();
            }
            bool other_sent=false;
            for(const auto &d:declarations) if(d.interface==1 && d.time_ms>start) other_sent=true;
            EXPECT_TRUE(other_sent)<<"a failed participant must not starve the other interface";
        }
        calloc_before_failure=-1; settle();
        ASSERT_NE(adapter.ifs[0].msrp,nullptr); ASSERT_NE(adapter.ifs[0].mvrp,nullptr);
        mbx_model_set_link(&model,0,true); settle();
        EXPECT_EQ(adapter.ifs[0].domain.vid,2u);
    }
}
TEST_F(Srp, LinkEventsDiscardOnlyTheirPublishedReceivePrefix) {
    settle();
    for(unsigned i=0;i<MBX_N_IF;++i) {
        auto ready=frame(3,identity(i),1,2);
        ASSERT_TRUE(mbx_model_rx(&model,ready.data(),ready.size(),i));
        mbx_model_set_link(&model,i,false); mbx_model_set_link(&model,i,true);
        settle(); EXPECT_FALSE(adapter.ifs[i].active[0]);
        EXPECT_CALL(licence,Change(i,0,true)); offer(ready,i);
        EXPECT_TRUE(adapter.ifs[i].active[0]);
        EXPECT_CALL(licence,Change(i,0,false));
    }
}
TEST_F(Srp, LinkLevelLossAndFirstDownEventAreFailClosed) {
    settle(); EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),1,2));
    EXPECT_CALL(licence,Change(0,0,false));
    // Simulate a level change while event publication is held by a full ring.
    model.link_up[0]=false; ctrl_loop_service(&loop);
    EXPECT_FALSE(adapter.ifs[0].active[0]); EXPECT_FALSE(adapter.ifs[0].link);
    adapter.ifs[0].link_seen=false;
    mbx_event event{}; event.type=MBX_EV_TYPE_LINK;
    const auto sink=loop.sinks[loop.n_sinks-1];
    sink.fn(sink.ctx,&event); EXPECT_TRUE(adapter.ifs[0].link_seen);
    event.interface=MBX_N_IF; sink.fn(sink.ctx,&event);
    EXPECT_EQ(adapter.ifs[0].domain.vid,2u);
}
TEST_F(Srp, EventReentryAndSinkCapacityAreGuarded) {
    settle();
    EXPECT_CALL(licence,Change(0,0,true)).WillOnce([&](unsigned,unsigned,bool) {
        mbx_event event{}; event.type=MBX_EV_TYPE_LINK;
        loop.sinks[loop.n_sinks-1].fn(&adapter,&event);
    });
    offer(frame(3,identity(),1,2)); EXPECT_EQ(adapter.reentries,1u);
    EXPECT_TRUE(adapter.ifs[0].link);
    EXPECT_CALL(licence,Change(0,0,false)); srp_mbx_destroy(&adapter);
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ctrl_loop_init(&loop); loop.n_sinks=CTRL_LOOP_MAX_SINKS;
    EXPECT_FALSE(srp_mbx_attach(&adapter,&loop)); EXPECT_EQ(loop.n_ticks,0u);
    ctrl_loop_init(&loop); ASSERT_TRUE(ctrl_loop_add_sink(&loop,[](void*,const mbx_event*){},nullptr));
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop)); srp_mbx_destroy(&adapter);
    EXPECT_EQ(loop.n_sinks,1u);
    EXPECT_EQ(mbx_rx_mark(MBX_N_CH),0u); EXPECT_FALSE(mbx_rx_before(MBX_N_CH,0));
}

TEST_F(Srp, ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord) {
    settle(); advance(400);
    srp_mbx_destroy(&adapter);
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ctrl_loop_init(&loop);
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    ASSERT_TRUE(ctrl_loop_open(&loop,0x020304fffe050600ull,config.mac));
    capture(); model.tx_sent=0;
    for(unsigned i=0;i<MBX_N_IF;++i) {
        ASSERT_TRUE(mbx_link_up(i));
        EXPECT_TRUE(adapter.ifs[i].link)<<"attach samples the current level";
        EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),1,2),i);
    }
    advance(400); capture();
    for(unsigned i=0;i<MBX_N_IF;++i) {
        bool talker=false; bool domain=false; bool vlan=false;
        for(const auto &d:declarations) if(d.interface==i) {
            talker|=d.ethertype==0x22ea && d.type==1;
            domain|=d.ethertype==0x22ea && d.type==4 && d.value==std::vector<uint8_t>({6,3,0,2});
            vlan|=d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,2});
        }
        EXPECT_TRUE(talker); EXPECT_TRUE(domain); EXPECT_TRUE(vlan);
        EXPECT_TRUE(adapter.ifs[i].active[0]);
        EXPECT_CALL(licence,Change(i,0,false));
    }
}

TEST_F(Srp, CancelledLinkRecordRecoversFromLevelAndFencesOldReceive) {
    settle(); advance(400);
    for(unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),1,2),i);
    }
    for(unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,false));
        // The DOWN level is observed while its record is held. The level
        // returns to the last posted UP, so no new LINK record is owed.
        model.link_up[i]=false; ctrl_loop_service(&loop);
        ASSERT_FALSE(adapter.ifs[i].link);
        auto ready=frame(3,identity(i),1,2);
        for(unsigned n=0;n<CTRL_LOOP_RX_PER_PASS+1;++n)
            ASSERT_TRUE(mbx_model_rx(&model,ready.data(),ready.size(),i));
        model.link_up[i]=true;
        const unsigned start=model.now_ms;
        advance(1500); capture();
        EXPECT_TRUE(adapter.ifs[i].link);
        EXPECT_FALSE(adapter.ifs[i].active[0]);
        bool transmitted=false;
        for(const auto &d:declarations) if(d.interface==i && d.time_ms>start) transmitted=true;
        EXPECT_TRUE(transmitted)<<"level recovery resumes declarations";
        for(unsigned other=i+1;other<MBX_N_IF;++other) EXPECT_TRUE(adapter.ifs[other].active[0]);
        EXPECT_CALL(licence,Change(i,0,true)); offer(ready,i);
        EXPECT_TRUE(adapter.ifs[i].active[0]);
    }
    for(unsigned i=0;i<MBX_N_IF;++i) EXPECT_CALL(licence,Change(i,0,false));
}

TEST_F(Srp, SharedRebindKeepsOnlyTheRemainingEligibleRequest) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const uint8_t da[2][6]={
        {0x91,0xe0,0xf0,0,0,9},{0x91,0xe0,0xf0,0,0,10}
    };
    for(unsigned i=0;i<MBX_N_IF;++i) for(unsigned slot : {0u,1u})
        for(bool change_vid : {false,true}) for(bool retain_match : {false,true}) {
        SCOPED_TRACE(::testing::Message()<<i<<'/'<<slot<<'/'<<change_vid<<'/'<<retain_match);
        capture(); model.tx_sent=0;
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,slot,&sid,da[0],7));
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-slot,&sid,da[retain_match ? 0 : 1],7));
        offer(frame(1,talker_value(sid,da[0],7),1),i); advance(400);
        ASSERT_EQ(adapter.ifs[i].sinks[slot].declared,2u);
        ASSERT_EQ(adapter.ifs[i].sinks[1-slot].declared,2u);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,slot,&sid,da[change_vid ? 0 : 1],change_vid ? 8 : 7));
        capture(); model.tx_sent=0;
        advance(2200); capture();
        bool left=false; bool ready=false;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea && d.type==3) {
            left|=d.event==5;
            ready|=d.event!=5 && d.subtype==2;
        }
        EXPECT_EQ(left,!retain_match)<<"withdraw the last eligible shared request";
        EXPECT_EQ(ready,retain_match)<<"no stale Ready renewal after rebind";
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-slot,nullptr,nullptr,0));
        capture(); model.tx_sent=0;
        advance(1200); capture();
        left=false;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea && d.type==3) {
            left|=d.event==5;
            EXPECT_EQ(d.event,5u)<<"removing the eligible user leaves no Ready";
        }
        EXPECT_EQ(left,retain_match);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,slot,nullptr,nullptr,0)); advance(200);
    }
}

TEST_F(Srp, ConsecutiveSharedReplacementsKeepApplicantStateUntilReconciliation) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const msrp_stream_id other{{2,1,2,3,4,5,6,8}};
    const uint8_t da[2][6]={
        {0x91,0xe0,0xf0,0,0,9},{0x91,0xe0,0xf0,0,0,10}
    };
    for(unsigned i=0;i<MBX_N_IF;++i) for(unsigned first : {0u,1u}) {
        capture(); model.tx_sent=0;
        for(unsigned k=0;k<2;++k) ASSERT_TRUE(srp_mbx_bind(&adapter,i,k,&sid,da[0],7));
        offer(frame(1,talker_value(sid,da[0],7),1),i); advance(400);
        // Both replacements occur before poll. The representative cannot
        // forget the Applicant when the second cache is replaced too.
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,first,&sid,da[1],8));
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-first,&sid,da[1],8));
        capture(); model.tx_sent=0;
        advance(2200); capture();
        bool left=false; bool vlan_left=false;
        for(const auto &d:declarations) if(d.interface==i) {
            if(d.ethertype==0x22ea && d.type==3) {
                left|=d.event==5; EXPECT_EQ(d.event,5u)<<"no stale shared renewal";
            }
            if(d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,7})) {
                vlan_left|=d.event==5; EXPECT_EQ(d.event,5u);
            }
        }
        EXPECT_TRUE(left); EXPECT_TRUE(vlan_left);
        // Replacing the other StreamID must withdraw its last user while
        // preserving the newly shared StreamID's existing Ready Applicant.
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,first,&other,da[0],7));
        offer(frame(1,talker_value(other,da[0],7),1),i); advance(400);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-first,&other,da[0],7));
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,first,nullptr,nullptr,0));
        capture(); model.tx_sent=0; advance(1200); capture();
        bool ready=false;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea && d.type==3 &&
            d.value==std::vector<uint8_t>(other.bytes,other.bytes+8)) {
            EXPECT_NE(d.event,5u); ready|=d.subtype==2;
        }
        EXPECT_TRUE(ready);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-first,nullptr,nullptr,0)); advance(200);
    }
}

TEST_F(Srp, JoiningIneligibleBindingWithdrawsReadyWhenOriginalLeaves) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const std::vector<uint8_t> id(sid.bytes,sid.bytes+8);
    const uint8_t da[2][6]={
        {0x91,0xe0,0xf0,0,0,9},{0x91,0xe0,0xf0,0,0,10}
    };
    for(unsigned i=0;i<MBX_N_IF;++i) for(unsigned first : {0u,1u}) {
        SCOPED_TRACE(::testing::Message()<<i<<'/'<<first);
        capture(); model.tx_sent=0;
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,first,&sid,da[0],7));
        offer(frame(1,talker_value(sid,da[0],7),1),i); advance(400); capture();
        bool ready=false;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea &&
            d.type==3 && d.value==id && d.event!=5) { ready|=d.subtype==2; }
        ASSERT_TRUE(ready)<<"the original binding has declared Ready on the wire";
        // Join from the other slot only after Ready exists. No service pass
        // may repair its inherited Applicant before the eligible user leaves.
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-first,&sid,da[1],7));
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,first,nullptr,nullptr,0));
        capture(); model.tx_sent=0; advance(2200); capture();
        bool left=false;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea &&
            d.type==3 && d.value==id) {
            left|=d.event==5;
            EXPECT_EQ(d.event,5u)<<"no stale Ready renewal for the ineligible survivor";
        }
        EXPECT_TRUE(left)<<"the shared Ready must be withdrawn";
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-first,nullptr,nullptr,0)); advance(1200);
    }
}

TEST_F(Srp, ReboundStreamCannotInheritAnotherStreamsReady) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const msrp_stream_id other{{2,1,2,3,4,5,6,8}};
    const std::vector<uint8_t> id(sid.bytes,sid.bytes+8);
    const uint8_t da[]={
        0x91,0xe0,0xf0,0,0,9
    };
    for(unsigned i=0;i<MBX_N_IF;++i) for(unsigned slot : {0u,1u}) {
        SCOPED_TRACE(::testing::Message()<<i<<'/'<<slot);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,slot,&sid,da,7));
        offer(frame(1,talker_value(sid,da,7),1),i); advance(400);
        ASSERT_EQ(adapter.ifs[i].sinks[slot].declared,2u);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,slot,nullptr,nullptr,0));
        capture(); model.tx_sent=0; advance(400); capture();
        bool left=false;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea &&
            d.type==3 && d.value==id) { left|=d.event==5; }
        ASSERT_TRUE(left)<<"the previous Listener declaration has been withdrawn";
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-slot,&other,da,7));
        offer(frame(1,talker_value(other,da,7),1),i); advance(400);
        ASSERT_EQ(adapter.ifs[i].sinks[1-slot].declared,2u);
        capture(); model.tx_sent=0;
        // The first Talker is still registered. Rebind without another RX:
        // another StreamID's Ready cache must not suppress this declaration.
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,slot,&sid,da,7)); advance(400); capture();
        bool ready=false;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea &&
            d.type==3 && d.value==id && d.event!=5) { ready|=d.subtype==2; }
        EXPECT_TRUE(ready)<<"the rebound StreamID owes its own Ready declaration";
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,slot,nullptr,nullptr,0));
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-slot,nullptr,nullptr,0)); advance(1200);
    }
}

TEST_F(Srp, FinalDomainVidUnbindKeepsSrClassMembership) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const std::vector<uint8_t> id(sid.bytes,sid.bytes+8);
    const uint8_t da[]={
        0x91,0xe0,0xf0,0,0,9
    };
    for(unsigned i=0;i<MBX_N_IF;++i) for(unsigned vid : {2u,7u})
        for(unsigned slot : {0u,1u}) {
        SCOPED_TRACE(::testing::Message()<<i<<'/'<<vid<<'/'<<slot);
        // Exercise the current Domain, including a peer-selected VID.
        offer(frame(4,{6,3,0,uint8_t(vid)},1),i); advance(400);
        ASSERT_EQ(adapter.ifs[i].domain.vid,vid);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,slot,&sid,da,vid));
        offer(frame(1,talker_value(sid,da,vid),1),i); advance(1200);
        ASSERT_EQ(adapter.ifs[i].sinks[slot].declared,2u);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,slot,nullptr,nullptr,0));
        capture(); model.tx_sent=0; advance(2200); capture();
        bool listener_left=false; bool vlan_renewed=false;
        for(const auto &d:declarations) if(d.interface==i) {
            if(d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,uint8_t(vid)})) {
                EXPECT_NE(d.event,5u)<<"final unbind must retain the Domain VID";
                vlan_renewed|=d.event!=5;
            }
            if(d.ethertype==0x22ea && d.type==3 && d.value==id) {
                listener_left|=d.event==5;
                EXPECT_EQ(d.event,5u)<<"the removed Listener must not renew Ready";
            }
        }
        EXPECT_TRUE(listener_left)<<"the final unbind was serviced";
        EXPECT_TRUE(vlan_renewed)<<"SR class membership still renews after unbind";
    }
}

TEST_F(Srp, LastNeverEligibleBindingWithdrawsTheSharedVidInEitherOrder) {
    settle(); advance(400);
    const msrp_stream_id eligible{{2,1,2,3,4,5,6,7}};
    const msrp_stream_id waiting{{2,1,2,3,4,5,6,8}};
    const uint8_t da[]={
        0x91,0xe0,0xf0,0,0,9
    };
    for(unsigned i=0;i<MBX_N_IF;++i) for(unsigned first : {0u,1u}) {
        capture(); model.tx_sent=0;
        // Bind the ineligible sink before the VID is requested. Ownership
        // cannot depend on the last sink's individual request history.
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1,&waiting,da,7));
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,&eligible,da,7));
        offer(frame(1,talker_value(eligible,da,7),1),i); advance(400);
        ASSERT_FALSE(adapter.ifs[i].sinks[1].vlan_requested);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,first,nullptr,nullptr,0));
        capture(); model.tx_sent=0; advance(1200); capture();
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x88f5 &&
            d.value==std::vector<uint8_t>({0,7})) { EXPECT_NE(d.event,5u); }
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-first,nullptr,nullptr,0));
        capture(); model.tx_sent=0; advance(2200); capture();
        bool vlan_left=false;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x88f5 &&
            d.value==std::vector<uint8_t>({0,7})) {
            vlan_left|=d.event==5; EXPECT_EQ(d.event,5u)<<"no VID renewal without a binding";
        }
        EXPECT_TRUE(vlan_left);
    }
}

TEST_F(Srp, RefusedPeerDomainDoesNotSurviveLinkRestart) {
    settle(); advance(400);
    receive_before_poll(frame(4,{6,4,0,3},0));
    std::vector<void*> held; while(void *p=ctrl_pool_alloc(&pool,1)) held.push_back(p);
    ASSERT_GE(held.size(),2u);
    ctrl_loop_service(&loop);
    ASSERT_TRUE(adapter.ifs[0].domain_owed);
    for(void *p:held) ctrl_pool_free(&pool,p);
    mbx_model_set_link(&model,0,false); mbx_model_set_link(&model,0,true); settle(); advance(400);
    EXPECT_EQ(adapter.ifs[0].domain.vid,2u)<<"old link's refused Domain must be discarded";
    EXPECT_EQ(adapter.ifs[0].domain.priority,3u);
}

TEST_F(Srp, SinkVlanRedeclaredBeforeReadyAfterLinkRestart) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const uint8_t da[]={
        0x91,0xe0,0xf0,0,0,9
    };
    for(unsigned i=0;i<MBX_N_IF;++i) {
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,&sid,da,7));
        offer(frame(1,talker_value(sid,da,7),1),i); advance(400);
        ASSERT_EQ(adapter.ifs[i].sinks[0].declared,2u);
        mbx_model_set_link(&model,i,false); mbx_model_set_link(&model,i,true); settle();
        capture(); model.tx_sent=0;
        offer(frame(1,talker_value(sid,da,7),1),i); advance(400); capture();
        bool vlan=false; bool ready=false;
        for(const auto &d:declarations) if(d.interface==i) {
            if(d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,7}) && (d.event==1 || d.event==3)) vlan=true;
            if(d.ethertype==0x22ea && d.type==3 && d.subtype==2 && d.event!=5) {
                EXPECT_TRUE(vlan)<<"new link's VLAN Join must precede Ready"; ready=true;
            }
        }
        EXPECT_TRUE(vlan); EXPECT_TRUE(ready);
    }
}

TEST_F(Srp, SharedReadyWaitsForTheMatchingBindingsOwnVlan) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const uint8_t da[2][6]={
        {0x91,0xe0,0xf0,0,0,8},{0x91,0xe0,0xf0,0,0,9}
    };
    for(unsigned i=0;i<MBX_N_IF;++i) {
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,&sid,da[0],2));
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1,&sid,da[1],7));
        advance(1200); ASSERT_TRUE(adapter.ifs[i].sinks[0].vlan_sent);
        capture(); model.tx_sent=0;
        offer(frame(1,talker_value(sid,da[1],7),1),i); advance(400); capture();
        bool vlan=false; bool ready=false;
        for(const auto &d:declarations) if(d.interface==i) {
            if(d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,7}) && (d.event==1 || d.event==3)) vlan=true;
            if(d.ethertype==0x22ea && d.type==3 && d.subtype==2 && d.event!=5) {
                EXPECT_TRUE(vlan)<<"matching binding's VLAN Join must precede Ready"; ready=true;
            }
        }
        EXPECT_TRUE(vlan); EXPECT_TRUE(ready);
    }
}

TEST_F(Srp, MilanMsrpOptionLeavesMvrpOnTheOriginalLeaveDeadline) {
    settle(); advance(400);
    for(unsigned i=0;i<MBX_N_IF;++i) {
        std::vector<uint8_t> vlan(26);
        wire_put_be(vlan.data(),0x0180c2000021ull,6);
        wire_put_be(vlan.data()+12,0x88f5,2);
        const uint8_t pdu[]={
            0,1,2,0,1,0,2,36,0,0,0,0
        };
        std::copy(pdu,pdu+12,vlan.begin()+14);
        const auto registered=[&]() {
            struct Status { int state=-1; } status;
            mrp_attr_visit(adapter.ifs[i].mvrp,0,[](void *ctx,const mrp_attr_status *s) {
                if(s->attr_type==1 && wire_be16(static_cast<const uint8_t*>(s->attr_val))==2)
                    static_cast<Status*>(ctx)->state=s->reg;
            },&status);
            return status.state;
        };
        offer(vlan,i); ASSERT_EQ(registered(),MRP_REG_STATE_IN);
        vlan[21]=5*36; offer(vlan,i);
        EXPECT_EQ(registered(),MRP_REG_STATE_LV)<<"MVRP must retain IEEE aging";
        advance(2000); offer(vlan,i);
        advance(2990); EXPECT_EQ(registered(),MRP_REG_STATE_LV);
        advance(10); EXPECT_EQ(registered(),MRP_REG_STATE_MT);
    }
}

}
