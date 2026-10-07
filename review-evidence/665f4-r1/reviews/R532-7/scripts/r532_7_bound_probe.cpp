// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R532-7): the 1000 ms original-arrival bound on retained SRP
// receive refusal, graded with millisecond timing at the mailbox boundary.
// Built by r532_probe.py with the tree's own fixture. Every timed case prints
// one PROBE line; asserts use Milan Table 4.3 LeaveTime (5000 ms) as the
// assignment's ceiling and the documented 1000 ms bound plus service slack.
#include "srp_fixture.hpp"
FW_TALLY_LABEL("R532-7 receive bound probe");
using ::testing::AnyNumber;
using ::testing::_;
namespace {
constexpr unsigned kLeaveTimeMs = 5000;
constexpr unsigned kBoundMs = 1000;
constexpr unsigned kSlackMs = 20;  // two centisecond service opportunities
class R5327 : public Srp {
protected:
    std::vector<uint8_t> domains(unsigned n, unsigned first) {
        std::vector<uint8_t> f(14);
        wire_put_be(f.data(),0x0180c200000eull,6);
        wire_put_be(f.data()+6,0x020304010203ull,6);
        wire_put_be(f.data()+12,0x22ea,2);
        f.push_back(0); f.push_back(4); f.push_back(4);
        const unsigned list=n*7+2;
        f.push_back(list>>8); f.push_back(list&255);
        for(unsigned k=0;k<n;++k) {
            const unsigned vid=first+k;
            f.insert(f.end(),{0,1,6,3,uint8_t(vid>>8),uint8_t(vid&255),36});
        }
        f.insert(f.end(),{0,0,0,0});
        return f;
    }
    unsigned now=0;
    void ms(unsigned count=1) {
        for(unsigned k=0;k<count;++k) {
            mbx_model_advance_ms(&model,1); ++now;
            for(unsigned n=0;n<50;++n) if(ctrl_loop_service(&loop)==0 && !mbx_model_irq(&model)) break;
        }
    }
    bool push(const std::vector<uint8_t> &f, unsigned i, unsigned *waited=nullptr) {
        for(unsigned t=0;t<5000;++t) {
            if(mbx_model_rx(&model,f.data(),f.size(),i)) { if(waited) *waited=t; return true; }
            ms();
        }
        return false;
    }
    unsigned last() const { return MBX_N_IF-1; }
    void listen() {
        EXPECT_CALL(licence,Change(_,_,_)).Times(AnyNumber());
        settle(); ms(400);
        auto ready=frame(3,identity(last()),0,2);
        ASSERT_TRUE(push(ready,last())); ms(5);
        ASSERT_TRUE(adapter.ifs[last()].active[0]);
    }
    // Milliseconds until the Listener's licence is revoked, from the Lv's mailbox acceptance.
    unsigned leave_latency(unsigned limit, unsigned *accept_wait) {
        auto lv=frame(3,identity(last()),5,2);
        EXPECT_TRUE(push(lv,last(),accept_wait));
        unsigned t=0;
        while(adapter.ifs[last()].active[0] && t<limit) { ms(); ++t; }
        return t;
    }
    void hol(unsigned n) {
        listen();
        auto big=domains(n,100);
        ASSERT_LE(big.size(),(size_t)MBX_FRAME_BYTES_MAX);
        ASSERT_TRUE(push(big,0));
        ms(5);
        const bool retained=adapter.pending_rx.len!=0;
        unsigned accept=0;
        const unsigned lat=leave_latency(10000,&accept);
        std::printf("PROBE hol N=%u ifs=%u retained=%d accept_wait=%u revoke_ms=%u discarded=%u refused=%u malformed=%u pending=%u\n",
                    n,(unsigned)MBX_N_IF,(int)retained,accept,lat,adapter.rx_discarded,adapter.refused,adapter.malformed,
                    (unsigned)adapter.pending_rx.len);
        EXPECT_FALSE(adapter.ifs[last()].active[0]);
        EXPECT_LT(lat,kLeaveTimeMs);
        EXPECT_LE(lat+accept,kBoundMs+kSlackMs);
        EXPECT_EQ(adapter.malformed,0u);
    }
};
TEST_F(R5327, TimedHolThirty) { hol(30); }
TEST_F(R5327, TimedHolOneFifty) { hol(150); }

// Lv arrives while separate one-Domain flood records are still being refused.
TEST_F(R5327, LeaveDuringDomainFlood) {
    listen();
    unsigned worst_accept=0;
    // Flood until a record is actually retained, then five more behind it.
    unsigned v=3, extra=0;
    for(;v<250 && extra<5;++v) {
        unsigned w=0; ASSERT_TRUE(push(frame(4,{6,3,0,uint8_t(v)},1),0,&w));
        worst_accept=std::max(worst_accept,w); ms(2);
        if(adapter.pending_rx.len) ++extra;
    }
    ASSERT_EQ(extra,5u) << "flood never exhausted the pool";
    const bool pending=adapter.pending_rx.len!=0;
    unsigned accept=0;
    const unsigned lat=leave_latency(10000,&accept);
    std::printf("PROBE flood-mid ifs=%u domains_sent=%u pending_at_lv=%d flood_accept_wait_max=%u lv_accept_wait=%u revoke_ms=%u discarded=%u refused=%u\n",
                (unsigned)MBX_N_IF,v-3,(int)pending,worst_accept,accept,lat,adapter.rx_discarded,adapter.refused);
    EXPECT_FALSE(adapter.ifs[last()].active[0]);
    EXPECT_LT(lat,kLeaveTimeMs);
    EXPECT_LE(lat+accept,kBoundMs+kSlackMs);
}

// The peer retransmits the oversized PDU every periodic interval; each later
// record is still bounded by its own arrival, never by the queue ahead of it.
TEST_F(R5327, RepeatedOversizedRetransmission) {
    listen();
    auto big=domains(150,100);
    unsigned lat=0, accept=0;
    for(unsigned s=0;s<8;++s) {
        ASSERT_TRUE(push(big,0));
        if(s==2) { ms(500); lat=leave_latency(10000,&accept); ms(500-std::min(500u,lat)); }
        else ms(1000);
    }
    std::printf("PROBE repeat ifs=%u lv_accept_wait=%u revoke_ms=%u discarded=%u refused=%u received=%u malformed=%u\n",
                (unsigned)MBX_N_IF,accept,lat,adapter.rx_discarded,adapter.refused,adapter.received,adapter.malformed);
    EXPECT_FALSE(adapter.ifs[last()].active[0]);
    EXPECT_LE(lat+accept,kBoundMs+kSlackMs);
    EXPECT_GE(adapter.rx_discarded,1u);
    EXPECT_EQ(adapter.malformed,0u);
}

// The binding port refuses while a record is retained; it must succeed by the bound.
TEST_F(R5327, BindingProgressByTheBound) {
    listen();
    auto big=domains(150,100);
    ASSERT_TRUE(push(big,0)); ms(2);
    ASSERT_NE(adapter.pending_rx.len,0u);
    unsigned t=0;
    while(!srp_mbx_bind(&adapter,last(),0,nullptr,nullptr,0) && t<10000) { ms(); ++t; }
    std::printf("PROBE bind ifs=%u bind_after_ms=%u discarded=%u\n",(unsigned)MBX_N_IF,t,adapter.rx_discarded);
    EXPECT_LE(t,kBoundMs+kSlackMs);
    EXPECT_EQ(adapter.rx_discarded,1u);
}

// Information: after the discard, does a fresh Talker Advertise on the last
// interface still find storage, or did the oversized prefix exhaust it?
TEST_F(R5327, StorageAfterDiscardInformation) {
    listen();
    auto big=domains(150,100);
    ASSERT_TRUE(push(big,0)); ms(1100);
    const unsigned refused=adapter.refused, discarded=adapter.rx_discarded, received=adapter.received;
    std::vector<uint8_t> ta(25,0);
    wire_put_be(ta.data(),0x0a0b0c0d0e0f0001ull,8);
    wire_put_be(ta.data()+8,0x91e0f0001234ull,6);
    wire_put_be(ta.data()+14,2,2);
    ASSERT_TRUE(push(frame(1,ta,1),last())); ms(1100);
    std::printf("PROBE storage ifs=%u in_use=%u refused+%u discarded+%u received+%u pending=%u\n",(unsigned)MBX_N_IF,
                (unsigned)ctrl_pool_in_use(&pool),adapter.refused-refused,adapter.rx_discarded-discarded,
                adapter.received-received,(unsigned)adapter.pending_rx.len);
    EXPECT_EQ(adapter.malformed,0u);
}
}
