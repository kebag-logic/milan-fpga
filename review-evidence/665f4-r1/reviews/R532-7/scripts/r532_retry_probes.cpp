// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probes (R532-6): receive-time allocation refusal, retention and retry
// at the mailbox boundary. Built by r532_probe.py with the tree's own fixture.
#include "srp_fixture.hpp"
namespace fw_test { const char *tally_label() { return "R532-6 receive retry probes"; } }
namespace {
class R532 : public Srp {
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
    // RX and EVT are level causes (MAILBOX_CONTRACT IRQ_STATUS): the target
    // loop passes again while work is reported or a cause is still pending.
    void drain() {
        for(unsigned n=0;n<1000;++n) {
            if(ctrl_loop_service(&loop)==0 && !mbx_model_irq(&model)) return;
        }
        FAIL()<<"loop did not drain";
    }
    // Service like the target: a pass, then sleep unless work or a wake is pending.
    void target_ms(unsigned ms) {
        for(unsigned k=0;k<ms;++k) {
            mbx_model_advance_ms(&model,1);
            for(unsigned n=0;n<50;++n) {
                if(ctrl_loop_service(&loop)==0 && !mbx_model_irq(&model)) break;
            }
        }
    }
};

// Repeated refusal across many centiseconds: no partial loss, nothing counted
// malformed, and the original record applies once storage returns.
TEST_F(R532, RepeatedRefusalAcrossTicksAppliesOnceAfterRecovery) {
    settle(); advance(400);
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),0,2));
    ASSERT_TRUE(adapter.ifs[0].active[0]);
    const auto received=adapter.received;
    exhaust();
    auto leave=frame(3,identity(),5,2);
    ASSERT_TRUE(mbx_model_rx(&model,leave.data(),leave.size(),0));
    target_ms(60);
    std::cout << "exhausted: pending=" << adapter.pending_rx.len << " refused=" << adapter.refused
              << " received=" << adapter.received << " malformed=" << adapter.malformed << std::endl;
    EXPECT_EQ(adapter.pending_rx.len,leave.size());
    EXPECT_EQ(std::memcmp(adapter.pending_rx.bytes,leave.data(),leave.size()),0);
    EXPECT_GE(adapter.refused,3u);
    EXPECT_EQ(adapter.received,received);
    EXPECT_EQ(adapter.malformed,0u);
    EXPECT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false));
    recover();
    target_ms(10);
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_FALSE(adapter.ifs[0].active[0]);
    EXPECT_EQ(adapter.received,received+1);
    EXPECT_EQ(adapter.stops,1u);
    advance(2000);
    EXPECT_EQ(adapter.stops,1u);
    EXPECT_EQ(adapter.malformed,0u);
}

// A sleeping loop with a retained record wakes on the centisecond tick alone.
TEST_F(R532, SleepingLoopRetriesOnTickWithoutPeerInput) {
    settle(); advance(400);
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),0,2));
    exhaust(); offer(frame(3,identity(),5,2));
    ASSERT_NE(adapter.pending_rx.len,0u);
    recover();
    unsigned waited=0;
    EXPECT_CALL(licence,Change(0,0,false));
    while(adapter.pending_rx.len && waited<30) {
        mbx_model_advance_ms(&model,1); ++waited;
        while(mbx_model_irq(&model)) { if(ctrl_loop_service(&loop)==0) break; }
    }
    std::cout << "retry after recovery waited " << waited << " ms" << std::endl;
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_LE(waited,10u);
    EXPECT_FALSE(adapter.ifs[0].active[0]);
}

// A later record on the same interface re-declares: the retained Leave must
// apply first, then the later Ready, in arrival order.
TEST_F(R532, RetainedLeaveThenQueuedReadyApplyInArrivalOrder) {
    settle(); advance(400);
    const unsigned i=MBX_N_IF-1;
    EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),0,2),i);
    exhaust(); offer(frame(3,identity(i),5,2),i);
    ASSERT_NE(adapter.pending_rx.len,0u);
    auto ready=frame(3,identity(i),1,2);
    ASSERT_TRUE(mbx_model_rx(&model,ready.data(),ready.size(),i));
    ctrl_loop_service(&loop);
    EXPECT_EQ(adapter.received,1u);
    ::testing::InSequence order;
    EXPECT_CALL(licence,Change(i,0,false));
    EXPECT_CALL(licence,Change(i,0,true));
    recover(); drain();
    EXPECT_EQ(adapter.pending_rx.len,0u);
    EXPECT_EQ(adapter.received,3u);
    EXPECT_TRUE(adapter.ifs[i].active[0]);
    EXPECT_EQ(adapter.stops,1u);
    EXPECT_EQ(adapter.malformed,0u);
    EXPECT_CALL(licence,Change(i,0,false));
}

// Cross-interface order: a retained interface-0 withdrawal precedes a queued
// interface-1 registration (the inverse direction of the lane's own case).
TEST_F(R532, RetainedFirstInterfacePrecedesLaterInterface) {
#if MBX_N_IF > 1
    settle(); advance(400);
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(0),0,2),0);
    exhaust(); offer(frame(3,identity(0),5,2),0);
    ASSERT_NE(adapter.pending_rx.len,0u);
    auto other=frame(3,identity(1),0,2);
    ASSERT_TRUE(mbx_model_rx(&model,other.data(),other.size(),1));
    ctrl_loop_service(&loop);
    EXPECT_FALSE(adapter.ifs[1].active[0]);
    ::testing::InSequence order;
    EXPECT_CALL(licence,Change(0,0,false));
    EXPECT_CALL(licence,Change(1,0,true));
    recover(); drain();
    EXPECT_FALSE(adapter.ifs[0].active[0]);
    EXPECT_TRUE(adapter.ifs[1].active[0]);
    EXPECT_EQ(adapter.received,3u);
    EXPECT_CALL(licence,Change(1,0,false));
#endif
}

// Link reset while the pool is still exhausted: the retained record is
// cancelled, the failed recreate is retried, and the stale Domain never applies.
TEST_F(R532, LinkResetDuringExhaustionCancelsAndRecreatesCleanly) {
    settle(); advance(400);
    const unsigned i=MBX_N_IF-1;
    exhaust(); offer(frame(4,{6,4,0,7},0),i);
    ASSERT_EQ(adapter.pending_rx.interface,i);
    ASSERT_NE(adapter.pending_rx.len,0u);
    mbx_model_set_link(&model,i,false);
    ctrl_loop_service(&loop);
    EXPECT_EQ(adapter.pending_rx.len,0u);
    calloc_before_failure=0; // reset frees blocks; refuse the recreate itself
    mbx_model_set_link(&model,i,true);
    for(unsigned n=0;n<5;++n) ctrl_loop_service(&loop);
    EXPECT_EQ(adapter.ifs[i].msrp,nullptr);
    recover(); settle(); advance(50);
    EXPECT_NE(adapter.ifs[i].msrp,nullptr);
    EXPECT_EQ(adapter.ifs[i].domain.vid,2u);
    EXPECT_EQ(adapter.received,0u);
    EXPECT_EQ(adapter.malformed,0u);
    EXPECT_EQ(adapter.pending_rx.len,0u);
}

// A truly malformed record after recovery is still counted once, and a
// refused one never is.
TEST_F(R532, OnlyMalformedInputCountsMalformed) {
    settle(); advance(400);
    exhaust(); offer(frame(4,{6,4,0,7},0));
    for(unsigned n=0;n<5;++n) ctrl_loop_service(&loop);
    EXPECT_EQ(adapter.malformed,0u);
    recover(); settle();
    EXPECT_EQ(adapter.ifs[0].domain.vid,7u);
    auto bad=frame(4,{6,4,0,9},0);
    bad[16]=3; // Domain AttributeLength 3 is invalid (35.2.2.8.1)
    offer(bad);
    EXPECT_EQ(adapter.malformed,1u);
    EXPECT_EQ(adapter.ifs[0].domain.vid,7u);
}
} // namespace
