// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "srp_fixture.hpp"
#include <array>
FW_TALLY_LABEL("ctrl SRP receive recovery");
namespace {
class SrpRetry : public Srp {
protected:
    std::vector<void*> held;
    void exhaust() {
        while(void *p=ctrl_pool_alloc(&pool,1)) held.push_back(p);
        ASSERT_FALSE(held.empty());
    }
    void recover() {
        for(void *p:held) ctrl_pool_free(&pool,p);
        held.clear(); calloc_before_failure=-1;
    }
    void TearDown() override { recover(); Srp::TearDown(); }
    std::vector<uint8_t> mixed(std::vector<uint8_t> first,const std::vector<uint8_t> &last) {
        first.resize(first.size()-2);
        first.insert(first.end(),last.begin()+15,last.end());
        return first;
    }
};

TEST_F(SrpRetry, RefusedMixedPayloadRetriesWithoutPeerRetransmission) {
    settle(); advance(400);
    const unsigned i=MBX_N_IF-1;
    EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),0,2),i);
    auto f=mixed(frame(3,identity(i),5,2),frame(4,{6,4,0,7},0));
    const auto before=adapter.received;
    exhaust(); offer(f,i);
    ASSERT_EQ(adapter.pending_rx.len,f.size());
    EXPECT_EQ(adapter.pending_rx.interface,i);
    EXPECT_EQ(adapter.pending_rx.arrival_ms,400u);
    EXPECT_EQ(std::memcmp(adapter.pending_rx.bytes,f.data(),f.size()),0);
    EXPECT_EQ(adapter.received,before);
    const auto refusals=adapter.refused;
    for(unsigned n=0;n<3;++n) ctrl_loop_service(&loop);
    EXPECT_GT(adapter.refused,refusals);
    EXPECT_EQ(adapter.malformed,0u);
    EXPECT_TRUE(adapter.ifs[i].active[0]);
    EXPECT_EQ(adapter.ifs[i].domain.vid,2u);
    EXPECT_FALSE(srp_mbx_bind(&adapter,i,0,nullptr,nullptr,0));
    // The shared receive buffer belongs to the loop, not the adapter.
    std::memset(&loop.frame,0xa5,sizeof(loop.frame));
    recover();
    EXPECT_CALL(licence,Change(i,0,false));
    ctrl_loop_service(&loop);
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_FALSE(adapter.ifs[i].active[0]);
    EXPECT_EQ(adapter.ifs[i].domain.vid,7u);
    EXPECT_EQ(adapter.received,before+1);
    EXPECT_EQ(adapter.stops,1u);
    EXPECT_EQ(adapter.malformed,0u);
    settle(); EXPECT_EQ(adapter.stops,1u);
}

TEST_F(SrpRetry, PartialPayloadKeepsLaterAttributesAndDoesNotRepeatStop) {
    settle(); advance(400);
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),0,2));
    auto f=mixed(frame(3,identity(),5,2),frame(4,{6,4,0,7},0));
    f=mixed(f,frame(4,{6,5,0,8},0));
    // Only the first Leave's propagation reservation succeeds.
    calloc_before_failure=1;
    EXPECT_CALL(licence,Change(0,0,false)); offer(f);
    EXPECT_EQ(adapter.stops,1u);
    ASSERT_EQ(adapter.pending_rx.len,f.size());
    EXPECT_EQ(adapter.ifs[0].domain.vid,2u);
    EXPECT_EQ(adapter.received,1u);
    for(unsigned n=0;n<3;++n) ctrl_loop_service(&loop);
    recover(); ctrl_loop_service(&loop);
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_EQ(adapter.ifs[0].domain.vid,8u);
    EXPECT_EQ(adapter.ifs[0].domain.priority,5u);
    EXPECT_EQ(adapter.received,2u);
    EXPECT_EQ(adapter.stops,1u);
    EXPECT_EQ(adapter.malformed,0u);
}

TEST_F(SrpRetry, LaterRecordsCannotOvertakeRetainedInterface) {
    settle(); advance(400);
    const unsigned i=MBX_N_IF-1;
    EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),0,2),i);
    exhaust(); offer(frame(3,identity(i),5,2),i);
    auto next=frame(3,identity(),0,2);
    ASSERT_TRUE(mbx_model_rx(&model,next.data(),next.size(),0));
    const auto records=loop.stats.rx_records;
    ctrl_loop_service(&loop);
    EXPECT_EQ(loop.stats.rx_records,records);
    EXPECT_EQ(adapter.received,1u);
    recover();
    ::testing::InSequence ordered;
    EXPECT_CALL(licence,Change(i,0,false));
    EXPECT_CALL(licence,Change(0,0,true));
    ctrl_loop_service(&loop);
    EXPECT_EQ(adapter.received,2u);
    EXPECT_FALSE(adapter.ifs[i].active[0]);
    settle();
    EXPECT_EQ(adapter.received,3u);
    EXPECT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false));
}

TEST_F(SrpRetry, LinkResetCancelsRetainedPayloadAndFencesLaterOldRecords) {
    settle(); advance(400);
    const unsigned i=MBX_N_IF-1;
    exhaust(); offer(frame(4,{6,4,0,7},0),i);
    auto stale=frame(3,identity(i),0,2);
    ASSERT_TRUE(mbx_model_rx(&model,stale.data(),stale.size(),i));
    ASSERT_NE(adapter.pending_rx.len,0u);
    recover();
    mbx_model_set_link(&model,i,false); mbx_model_set_link(&model,i,true);
    settle();
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_EQ(adapter.received,0u);
    EXPECT_EQ(adapter.ifs[i].domain.vid,2u);
    EXPECT_FALSE(adapter.ifs[i].active[0]);
    EXPECT_CALL(licence,Change(i,0,true)); offer(stale,i);
    EXPECT_CALL(licence,Change(i,0,false));
}

TEST_F(SrpRetry, OtherInterfaceResetPreservesRetainedPayload) {
#if MBX_N_IF > 1
    settle(); advance(400);
    exhaust(); offer(frame(4,{6,4,0,7},0),1);
    ASSERT_NE(adapter.pending_rx.len,0u);
    // Hold the allocator refusal across recreation of the unrelated port.
    calloc_before_failure=0;
    mbx_model_set_link(&model,0,false); mbx_model_set_link(&model,0,true);
    ctrl_loop_service(&loop);
    EXPECT_NE(adapter.pending_rx.len,0u);
    EXPECT_EQ(adapter.pending_rx.interface,1u);
    recover(); settle();
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_EQ(adapter.ifs[1].domain.vid,7u);
    EXPECT_EQ(adapter.ifs[0].domain.vid,2u);
    EXPECT_EQ(adapter.received,1u);
#endif
}

TEST_F(SrpRetry, DestroyCancelsRetainedPayloadBeforeReinitialization) {
    settle(); advance(400); exhaust(); offer(frame(4,{6,4,0,7},0));
    ASSERT_NE(adapter.pending_rx.len,0u);
    srp_mbx_destroy(&adapter);
    EXPECT_EQ(adapter.pending_rx.len,0u);
    recover();
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    settle();
    EXPECT_EQ(adapter.ifs[0].domain.vid,2u);
    EXPECT_EQ(adapter.received,0u);
}

TEST_F(SrpRetry, FailedParticipantRecreationRetainsFreshReceive) {
    settle(); advance(400);
    calloc_before_failure=0;
    mbx_model_set_link(&model,0,false); mbx_model_set_link(&model,0,true);
    ctrl_loop_service(&loop);
    ASSERT_EQ(adapter.ifs[0].msrp,nullptr);
    auto f=frame(3,identity(),0,2);
    ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),0));
    ctrl_loop_service(&loop);
    EXPECT_EQ(adapter.pending_rx.len,f.size());
    EXPECT_EQ(adapter.malformed,0u);
    recover();
    EXPECT_CALL(licence,Change(0,0,true)); settle();
    EXPECT_EQ(adapter.received,1u);
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_CALL(licence,Change(0,0,false));
}

TEST_F(SrpRetry, RetainedMvrpUsesItsOriginalParticipant) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const std::array<uint8_t,6> da{0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,MBX_N_IF-1,0,&sid,da.data(),7));
    std::vector<uint8_t> f(26);
    wire_put_be(f.data(),0x0180c2000021ull,6);
    wire_put_be(f.data()+12,0x88f5,2);
    f[15]=1; f[16]=2; f[18]=1; f[20]=7;
    exhaust(); offer(f,MBX_N_IF-1);
    EXPECT_EQ(adapter.pending_rx.len,f.size());
    recover(); ctrl_loop_service(&loop);
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_EQ(adapter.received,1u);
    EXPECT_EQ(adapter.malformed,0u);
    unsigned registered=0;
    auto visit=[](void *ctx,const mrp_attr_status *s) {
        if(s->reg==MRP_REG_STATE_IN) ++*static_cast<unsigned*>(ctx);
    };
    mrp_attr_visit(adapter.ifs[MBX_N_IF-1].mvrp,0,visit,&registered);
    EXPECT_EQ(registered,1u);
}

TEST_F(SrpRetry, RetainedReceiveWaitsForOwedTransmit) {
    settle(); advance(400); exhaust(); offer(frame(4,{6,4,0,7},0));
    mbx_model_tx_pause(&model,true);
    std::vector<uint8_t> filler(60);
    while(mbx_tx_send(MBX_CH_SRP,0,filler.data(),filler.size())==MBX_STATUS_OK) {}
    mbx_model_advance_ms(&model,600);
    for(unsigned n=0;n<10;++n) ctrl_loop_service(&loop);
    ASSERT_GT(adapter.owed_len,0u);
    recover(); ctrl_loop_service(&loop);
    EXPECT_NE(adapter.pending_rx.len,0u);
    EXPECT_EQ(adapter.ifs[0].domain.vid,2u);
    EXPECT_EQ(adapter.malformed,0u);
    mbx_model_tx_pause(&model,false); settle();
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_EQ(adapter.ifs[0].domain.vid,7u);
    EXPECT_EQ(adapter.received,1u);
}

TEST_F(SrpRetry, RetainedReceiveWaitsForTickAndLifecycleBacklogs) {
    settle(); advance(400); exhaust(); offer(frame(4,{6,4,0,7},0));
    recover(); mbx_model_advance_ms(&model,5000);
    // Drain the posted prefix until the coalesced centiseconds arrive.
    for(unsigned n=0;n<100 && loop.ticks_owed==0;++n) {
        ctrl_loop_service(&loop);
        EXPECT_EQ(adapter.received,0u);
    }
    ASSERT_GT(loop.ticks_owed,0u);
    EXPECT_NE(adapter.pending_rx.len,0u);
    EXPECT_EQ(adapter.received,0u);
    settle();
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_EQ(adapter.received,1u);
    settle(); advance(400);
    exhaust(); offer(frame(4,{6,5,0,8},0)); recover();
    for(unsigned n=0;n<CTRL_LOOP_EVENTS_PER_PASS+1;++n) mbx_model_gm_change(&model,0,n+1,0);
    mbx_model_set_link(&model,0,false); mbx_model_set_link(&model,0,true);
    ctrl_loop_service(&loop);
    EXPECT_NE(adapter.pending_rx.len,0u);
    EXPECT_EQ(adapter.received,1u);
    settle();
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_EQ(adapter.ifs[0].domain.vid,2u);
    EXPECT_EQ(adapter.received,1u);
}

TEST_F(SrpRetry, WholeInvalidPduIsMalformedAndFutureUnknownMessageIsSkipped) {
    settle(); advance(400);
    auto invalid=mixed(frame(3,identity(),0,2),frame(4,{6,8,0,2},0));
    offer(invalid);
    EXPECT_EQ(adapter.malformed,1u);
    EXPECT_EQ(adapter.received,0u);
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_FALSE(adapter.ifs[0].active[0]);
    auto future=frame(3,identity(),0,2);
    future[14]=1;
    future.insert(future.begin()+15,{99,1,0,3,250,255,1});
    EXPECT_CALL(licence,Change(0,0,true)); offer(future);
    EXPECT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_EQ(adapter.malformed,1u);
    EXPECT_EQ(adapter.received,1u);
    EXPECT_CALL(licence,Change(0,0,false));
}
} // namespace
