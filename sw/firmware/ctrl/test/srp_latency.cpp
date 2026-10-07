// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "srp_fixture.hpp"
#include "mbx_wire.h"
#include <srp_latency_policy.hpp>
#include <cstdio>
FW_TALLY_LABEL("ctrl SRP service latency");
namespace {
// Desk envelope: 100 ns per mailbox access, plus 1 ms total CPU/preemption
// allowance per action and 100 ns observation uncertainty. This measures the
// actual access path; the allowance requires target validation before release.
class SrpLatency : public Srp {
protected:
    uint64_t now_ns=0; uint64_t accesses=0;
    std::vector<uint64_t> commits;
    static constexpr uint64_t ns_per_ms=1000000;
    static constexpr uint64_t service_limit=srp_service_limit_ns;
    static void trace(void *ctx,bool write,uint32_t offset,uint32_t) {
        auto &h=*static_cast<SrpLatency*>(ctx);
        h.now_ns+=100; ++h.accesses;
        if(write && offset==(MBX_CH_BASE + MBX_CH_SRP * MBX_CH_STRIDE + MBX_CH_REG_TX_HEAD)) h.commits.push_back(h.now_ns);
    }
    void SetUp() override { Srp::SetUp(); mbx_host_trace(trace,this); }
    void TearDown() override { mbx_host_trace(nullptr,nullptr); Srp::TearDown(); }
    void at(unsigned ms) {
        ASSERT_GE(ms,model.now_ms);
        mbx_model_advance_ms(&model,ms-model.now_ms);
        now_ns=std::max(now_ns,uint64_t(ms)*ns_per_ms);
        settle();
    }
    void bound(const char *path,uint64_t start,uint64_t end,uint64_t wait_ms=0) {
        ASSERT_GE(end,start);
        const uint64_t elapsed=end-start+ns_per_ms+100;
        std::printf("H-SRP if=%u path=%s elapsed_ns=%llu wait_ms=%llu service_ns=%llu accesses=%llu\n",
            MBX_N_IF,path,(unsigned long long)elapsed,(unsigned long long)wait_ms,
            (unsigned long long)(elapsed>wait_ms*ns_per_ms?elapsed-wait_ms*ns_per_ms:0),
            (unsigned long long)accesses);
        EXPECT_LE(elapsed,wait_ms*ns_per_ms+service_limit)<<path;
    }
};
TEST_F(SrpLatency, StartupJoinPeriodicAndLeaveAllCommitWithinOneBudget) {
    settle(); ASSERT_EQ(commits.size(),2u*MBX_N_IF);
    bound("startup",0,commits.back());
    auto count=commits.size(); at(200); ASSERT_GT(commits.size(),count);
    bound("JoinTime",200*ns_per_ms,commits.back());
    at(400); count=commits.size(); at(1000); ASSERT_GT(commits.size(),count);
    bound("periodic",1000*ns_per_ms,commits.back());
    // The selected random draw is an input to the timing verdict. Record
    // each application's first LA and allow only the outstanding Join wait.
    uint32_t seed[MBX_N_IF][2]{};
    unsigned due[MBX_N_IF][2]{}; bool seen[MBX_N_IF][2]{};
    for(unsigned i=0;i<MBX_N_IF;++i) for(unsigned p=0;p<2;++p) {
        seed[i][p]=uint32_t(config.mac[i])^(p?0x91u:0u);
        seed[i][p]=seed[i][p]*1664525u+1013904223u;
        due[i][p]=(1001u+seed[i][p]%499u)*10u;
        EXPECT_GT(due[i][p],10000u); EXPECT_LT(due[i][p],15000u);
    }
    unsigned last_ms[MBX_N_IF][2]{};
    for(unsigned k=0;k<model.tx_sent;++k) {
        const auto *previous=mbx_model_tx_frame(&model,k); ASSERT_NE(previous,nullptr);
        last_ms[previous->interface][wire_be16(previous->bytes+12)==0x88f5]=previous->now_ms;
    }
    for(unsigned ms=1010;ms<=15200;ms+=10) {
        const unsigned first=model.tx_sent; at(ms);
        for(unsigned k=first;k<model.tx_sent;++k) {
            const auto *f=mbx_model_tx_frame(&model,k); ASSERT_NE(f,nullptr);
            const bool mvrp=wire_be16(f->bytes+12)==0x88f5;
            const unsigned i=f->interface; const unsigned p=mvrp?1:0;
            bool la=false; unsigned off=15;
            while(off+2<f->len && (f->bytes[off] || f->bytes[off+1])) {
                unsigned width=f->bytes[off+1]; off+=2;
                unsigned end=f->len;
                if(!mvrp) { end=off+2+wire_be16(f->bytes+off); off+=2; }
                // LA appears on the first vector of each message.
                la=la || (f->bytes[off]&0x20u);
                if(!mvrp) off=end;
                else { const unsigned n=wire_be16(f->bytes+off)&8191u;
                       off+=2+width+(n+2)/3+2; }
            }
            if(la && !seen[i][p]) {
                seen[i][p]=true; EXPECT_GE(ms,due[i][p]);
                const unsigned last=last_ms[i][p];
                const unsigned wait=last+200>due[i][p] ? last+200-due[i][p] : 0;
                ASSERT_LE(wait,200u);
                bound(mvrp?"MVRP LeaveAll":"MSRP LeaveAll",due[i][p]*ns_per_ms,
                      commits.at(k),wait);
            }
            last_ms[i][p]=ms;
        }
    }
    for(auto &iface:seen) for(bool yes:iface) EXPECT_TRUE(yes);
}
TEST_F(SrpLatency, ReceiveStateMalformedDomainAndListenerPaths) {
    settle(); at(400);
    uint64_t begin=now_ns;
    EXPECT_CALL(licence,Change(0,0,true)).WillOnce([&](unsigned,unsigned,bool) {
        bound("RX to licence",begin,now_ns);
    });
    offer(frame(3,identity(),0,2));
    begin=now_ns; auto bad=frame(3,identity(),0,2); bad[29]=216;
    offer(bad); EXPECT_EQ(adapter.malformed,1u); bound("malformed discard",begin,now_ns);
    begin=now_ns;
    EXPECT_CALL(licence,Change(0,0,false));
    EXPECT_CALL(licence,Change(0,0,true));
    offer(frame(4,{6,4,0,3},0)); at(600);
    ASSERT_EQ(adapter.ifs[0].domain.vid,3u);
    bound("Domain to declarations",begin,commits.back(),200);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; const uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,3));
    std::vector<uint8_t> talker(25); std::copy(sid.bytes,sid.bytes+8,talker.begin());
    std::copy(da,da+6,talker.begin()+8); wire_put_be(talker.data()+14,3,2);
    wire_put_be(talker.data()+16,224,2); wire_put_be(talker.data()+18,1,2); talker[20]=0x80;
    begin=now_ns; offer(frame(1,talker,0)); at(800);
    ASSERT_EQ(adapter.ifs[0].sinks[0].declared,2u);
    bound("Talker RX to Listener",begin,commits.back(),200);
    begin=now_ns; ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0)); at(1000);
    bound("unbind to withdrawal",begin,commits.back(),200);
    EXPECT_CALL(licence,Change(0,0,false)); mbx_model_set_link(&model,0,false); settle();
}
TEST_F(SrpLatency, OriginalLeaveDeadlineSurvivesCoalescedBacklog) {
    settle(); EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),0,2));
    offer(frame(3,identity(),4,2,true));
    at(2000); offer(frame(3,identity(),5,1));
    at(4990); ASSERT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false)).WillOnce([&](unsigned,unsigned,bool) {
        bound("LeaveTime to stop",5000*ns_per_ms,now_ns);
    });
    at(5000); EXPECT_FALSE(adapter.ifs[0].active[0]);
    EXPECT_EQ(loop.stats.ticks,500u);
}
TEST_F(SrpLatency, FullRingRetainsOriginalOriginAndElevenMillisecondStallFails) {
    mbx_model_tx_pause(&model,true); std::vector<uint8_t> filler(60);
    while(mbx_tx_send(MBX_CH_SRP,0,filler.data(),filler.size())==MBX_STATUS_OK) {}
    commits.clear(); now_ns=0; ctrl_loop_service(&loop); ASSERT_GT(adapter.owed_len,0u);
    const uint64_t origin=0;
    mbx_model_advance_ms(&model,11); now_ns=11*ns_per_ms; ctrl_loop_service(&loop);
    EXPECT_TRUE(commits.empty());
    mbx_model_tx_pause(&model,false); settle(); ASSERT_FALSE(commits.empty());
    EXPECT_GT(commits.front()-origin+ns_per_ms+100,service_limit)
        <<"11 ms stall must fail the original event-to-commit budget";
}

TEST_F(SrpLatency, ReceiveRecoveryKeepsOriginalArrivalBudget) {
    settle(); at(400);
    for(unsigned delay : {1u,11u}) {
        EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),0,2));
        std::vector<void*> held;
        while(void *p=ctrl_pool_alloc(&pool,1)) held.push_back(p);
        const uint64_t origin=now_ns;
        offer(frame(3,identity(),5,2));
        ASSERT_NE(adapter.pending_rx.len,0u);
        const unsigned arrival=adapter.pending_rx.arrival_ms;
        at(model.now_ms+delay);
        EXPECT_EQ(adapter.pending_rx.arrival_ms,arrival);
        for(void *p:held) ctrl_pool_free(&pool,p);
        EXPECT_CALL(licence,Change(0,0,false)).WillOnce([&](unsigned,unsigned,bool) {
            if(delay==1u) {
                bound("RX storage recovery",origin,now_ns);
            } else {
                EXPECT_GT(now_ns-origin+ns_per_ms+100,service_limit)
                    <<"11 ms allocation stall must fail the original arrival budget";
            }
        });
        ctrl_loop_service(&loop);
        EXPECT_EQ(adapter.pending_rx.len,0u);
        EXPECT_FALSE(adapter.ifs[0].active[0]);
    }
    EXPECT_EQ(adapter.stops,2u);
}
} // namespace
