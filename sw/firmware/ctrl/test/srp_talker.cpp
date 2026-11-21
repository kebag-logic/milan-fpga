// SPDX-License-Identifier: CERN-OHL-W-2.0
// SRP's Talker declarations follow the validity of each source's SRP parameters (#895; Milan v1.2 4.3.3.1 and
// 5.3.7.4): srp_mbx_gate reports the sources whose destination MAAP allocated with no conflict and that a probe of the
// last 15 s or a registered Listener asks for (the MAAP adapter's DA gate). A valid source declares at once, Talker
// Advertise with base + n and its TSpec, or Talker Failed, code 1, when its bandwidth does not fit (IEEE 802.1Q-2018
// 35.2.2.8.7, Table 35-6); a source not valid declares nothing; a lapse withdraws, its licence and TALKER_DECL bit
// first. MSRP does not support a changed FirstValue on a StreamID (35.2.2.8): an unchanged destination may be declared
// again at once, a changed one reaches the wire within two nominal longest LeaveAll periods of the Leave's request,
// its JoinTime and THE TRANSMIT's terms counted inside them (10.7.4.3; #951, #956), a type swaps in place, and a reset
// holds a moved source as its Leave would. Run at 1x1/1if and 8x8/2if (test_ctrl_firmware.py).
#include "srp_fixture.hpp"
#include <algorithm>
FW_TALLY_LABEL("ctrl SRP Talker declarations");
namespace {

mbx_model_pub pub_of(const mbx_model &m, unsigned i) {
    mbx_model_pub v;
    mbx_model_pub_view(&m,i,&v);
    return v;
}

// The publication block as the fabric held it as each SRP record was committed.
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

// The order of the publication block's writes.
std::vector<std::pair<uint32_t,uint32_t>> pub_trace;
void pub_writes(void*, bool write, uint32_t off, uint32_t value) {
    if (write && off>=MBX_PUB_BASE && off<MBX_PUB_BASE+MBX_N_IF*MBX_PUB_STRIDE) pub_trace.emplace_back(off,value);
}

// One source admitted at 1 Gb/s: (224 + 22 + 20) bytes, 8 bits, 8000 frames/s (srp_mbx.c's admission).
constexpr uint32_t kAdmittedBps=17024000u;
// Two ranges MAAP may hold (IEEE 1722-2016 Table B.9's pool), base + n each source's destination.
constexpr uint64_t kBaseA=0x91e0f000aa00ull;
constexpr uint64_t kBaseB=0x91e0f000bb00ull;
// The withdrawal's hold-off in ms (#951, #956): two nominal longest LeaveAll periods, each 1.5 x LeaveAllTime (IEEE
// 802.1Q-2018 10.7.4.3 draws every leavealltimer below it) of 10 s (Table 10-7; Milan v1.2 Table 4.3), 30,000 ms, the
// latest a changed destination reaches the wire after its Leave's request. srp_mbx.c counts the hold-off from that
// request with a JoinTime and THE TRANSMIT's MRPDU by every source counted inside the two periods in whole
// centiseconds (ctrl_loop.h, CTRL_LOOP_JOIN_CS and CTRL_LOOP_TX_MS), the owner's decision of 2026-11-21: 29,770 ms at
// 1x1/1if, 29,730 at 8x8/1if and 29,700 at two interfaces. #951's added both terms past the two periods, 30,230 ms at
// 1x1/1if; two LeaveAllTime periods and both terms, 20,230 ms there, is the hold-off before #951.
constexpr uint32_t kLeaveAllTimeMs=10000u;
constexpr uint32_t kTwoLongestLeaveAllMs=2u*(kLeaveAllTimeMs+kLeaveAllTimeMs/2u);
constexpr uint32_t kHoldOffMs=kTwoLongestLeaveAllMs-10u*(CTRL_LOOP_JOIN_CS+(CTRL_LOOP_TX_MS+9u)/10u);
// The latest a declaration reaches the model's wire after the centisecond that owes it: lwSRP's join timer may hold it
// a JoinTime, and THE TRANSMIT commits its MRPDU within CTRL_LOOP_TX_MS of the centisecond that owes it (ctrl_loop.h).
constexpr uint32_t kLatestMs=10u*CTRL_LOOP_JOIN_CS+CTRL_LOOP_TX_MS;

bool declares(unsigned event) { return event==0u || event==1u || event==3u; }

class Talker : public Srp {
protected:
    // A composition's start (#895): no source valid and none allocated, so nothing is declared until srp_mbx_gate
    // reports a source's parameters valid.
    void SetUp() override {
        Srp::SetUp();
        srp_mbx_destroy(&adapter);
        config.sources_valid=false;
        for (unsigned i=0;i<MBX_N_IF;++i) {
            for (unsigned n=0;n<CTRL_SRP_SOURCES;++n) {
                sources[i][n].allocated=false;
                std::fill(sources[i][n].value.dest_mac,sources[i][n].value.dest_mac+6,0);
            }
        }
        ASSERT_TRUE(srp_mbx_init(&adapter,&config));
        ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    }
    // Every interface's gate: the sources in `valid` valid, at base.
    void gate(uint32_t valid, uint64_t base) {
        for (unsigned i=0;i<MBX_N_IF;++i) ASSERT_TRUE(srp_mbx_gate(&adapter,i,valid,base));
    }
    // Every SRP frame's declarations since the test began, decoded before the model's capture drops them.
    std::vector<Declaration> seen;
    uint32_t collected=0;
    void collect() {
        capture(collected);
        seen.insert(seen.end(),declarations.begin(),declarations.end());
        collected=model.tx_sent;
    }
    void trace() { commits_seen.clear(); traced_model=&model; mbx_host_trace(commit_trace,nullptr); }
    void untrace() { mbx_host_trace(nullptr,nullptr); }
    // Every Talker event of source n's StreamID on interface i in frames from `first`, in the order they left.
    std::vector<Declaration> talker(unsigned i, unsigned n, uint32_t first) {
        collect();
        std::vector<Declaration> out;
        const auto id=identity(i,n);
        for (const auto &d:seen) {
            if (d.interface==i && d.ethertype==0x22ea && (d.type==1 || d.type==2) && d.frame>=first &&
                std::equal(id.begin(),id.end(),d.value.begin())) out.push_back(d);
        }
        return out;
    }
    static uint64_t dest(const Declaration &d) {
        uint64_t v=0;
        for (unsigned b=8;b<14;++b) v=v<<8|d.value[b];
        return v;
    }
    // The first Leave of the Talker type of source n on interface i from `first`, or null.
    const Declaration *leave(const std::vector<Declaration> &ds, unsigned type) {
        for (const auto &d:ds) if (d.type==type && d.event==5u) return &d;
        return nullptr;
    }
    // The first declaring event (New, JoinIn, JoinMt) of the type after `after` ms, or null.
    const Declaration *declared(const std::vector<Declaration> &ds, unsigned type, uint32_t after=0) {
        for (const auto &d:ds) if (d.type==type && declares(d.event) && d.time_ms>=after) return &d;
        return nullptr;
    }
    // The first New of the type, or null: a Talker declared again with New (a periodic JoinIn is no new declaration).
    const Declaration *newly(const std::vector<Declaration> &ds, unsigned type) {
        for (const auto &d:ds) if (d.type==type && d.event==0u) return &d;
        return nullptr;
    }
    void advance_to(uint32_t ms) {
        while (model.now_ms<ms) {
            advance(1);
            if (model.now_ms%100u==0u) collect();
        }
    }
    // An MSRP frame of two Domain messages, each one value (IEEE 802.1Q-2018 10.8), the first with a LeaveAll if `la`.
    std::vector<uint8_t> domains(const std::vector<uint8_t> &a, unsigned ea, bool la,
                                 const std::vector<uint8_t> &b, unsigned eb) {
        auto f=frame(4,a,ea,0,la);
        const auto g=frame(4,b,eb);
        f.resize(f.size()-2);
        f.insert(f.end(),g.begin()+15,g.end());
        return f;
    }
    // SRP's transmit ring paused and filled with empty MRPDUs of interface 0, so the next frame it is given is
    // refused; how many it took.
    unsigned fill_ring() {
        mbx_model_tx_pause(&model,true);
        unsigned taken=0;
        for (unsigned len : {200u, 60u, 18u}) {
            std::vector<uint8_t> f(len);
            wire_put_be(f.data(),0x0180c200000eull,6);
            wire_put_be(f.data()+6,config.mac[0],6);
            wire_put_be(f.data()+12,0x22ea,2);
            while (mbx_tx_send(MBX_CH_SRP,0,f.data(),f.size())==MBX_STATUS_OK) ++taken;
        }
        return taken;
    }
    // Each interface's writes of one publication register in pub_trace.
    unsigned writes(unsigned i, uint32_t reg) const {
        unsigned n=0;
        for (const auto &w:pub_trace) n+=w.first==MBX_PUB_BASE+MBX_PUB_STRIDE*i+reg;
        return n;
    }
};

}  // namespace

// Allocate: a source whose SRP parameters are not valid declares nothing; once they are (MAAP's allocation and a probe
// or a Listener: the DA gate), it declares Talker Advertise at once, with base + n and its TSpec, TALKER_DECL and
// IDLE_SLOPE published before it leaves. A source whose parameters did not change is not declared again.
TEST_F(Talker, ValidSourceDeclaresAtOnceAndNothingBefore) {
    settle(); advance(1200);
    trace();
    uint32_t first=0;
    for (unsigned i=0;i<MBX_N_IF;++i) {
        for (unsigned n=0;n<CTRL_SRP_SOURCES;++n) {
            const auto ds=talker(i,n,0);
            EXPECT_EQ(declared(ds,1),nullptr) << "a source whose SRP parameters are not valid declares nothing";
            EXPECT_EQ(declared(ds,2),nullptr) << "a source whose SRP parameters are not valid declares nothing";
        }
        EXPECT_EQ(pub_of(model,i).talker_decl,0u) << "TALKER_DECL holds no undeclared source";
    }
    first=model.tx_sent;
    const uint32_t at=model.now_ms;
    gate(1u,kBaseA);
    advance(400);
    gate(1u,kBaseA);
    const unsigned n=CTRL_SRP_SOURCES-1u;
    gate(1u|1u<<n,kBaseA);
    advance(400);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,0,first);
        const auto *adv=declared(ds,1);
        ASSERT_NE(adv,nullptr) << "a valid source declares Talker Advertise at once";
        EXPECT_EQ(adv->event,0u) << "a valid source declares Talker Advertise at once";
        EXPECT_LE(adv->time_ms,at+220u) << "a valid source declares Talker Advertise at once";
        EXPECT_EQ(dest(*adv),kBaseA) << "the Advertise carries base + n";
        EXPECT_EQ(wire_be16(adv->value.data()+14),2u) << "the Advertise carries the Domain's VID";
        EXPECT_EQ(wire_be16(adv->value.data()+16),224u) << "the Advertise carries the source's TSpec";
        EXPECT_EQ(wire_be16(adv->value.data()+18),1u) << "the Advertise carries the source's TSpec";
        ASSERT_NE(commit_of(adv->frame),nullptr);
        EXPECT_EQ(commit_of(adv->frame)->pub[i].talker_decl&1u,1u) << "TALKER_DECL is set before the Advertise leaves";
        EXPECT_EQ(commit_of(adv->frame)->pub[i].idle_slope_bps,kAdmittedBps)
            << "IDLE_SLOPE admits the source before its Advertise leaves";
        // MRP sends a new declaration's New twice (its Applicant's VN and AN states, IEEE 802.1Q-2018 Table 10-3)
        unsigned news=0;
        for (const auto &d:ds) news+=d.type==1 && d.event==0u;
        EXPECT_LE(news,2u) << "a Talker whose parameters did not change is not declared again";
        if (n!=0u) {
            const auto others=talker(i,n,first);
            const auto *other=declared(others,1);
            ASSERT_NE(other,nullptr) << "a valid source declares Talker Advertise at once";
            EXPECT_EQ(dest(*other),kBaseA+n) << "the Advertise carries base + n";
        }
        EXPECT_EQ(pub_of(model,i).talker_decl,n!=0u ? 1u|1u<<n : 1u) << "TALKER_DECL holds the valid sources";
    }
}

// Withdrawal: a source whose parameters lapse (no probe for 15 s and no Listener, or the allocation lost) closes its
// licence, then withdraws its Advertise, TALKER_DECL and IDLE_SLOPE dropping it before the Leave leaves; nothing of it
// is declared while its parameters are not valid, LeaveAll included: no stale Talker Advertise remains.
TEST_F(Talker, LapseWithdrawsTheAdvertiseAndDeclaresNothing) {
    settle(); gate(1u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),1,2),i);
    }
    ASSERT_TRUE(::testing::Mock::VerifyAndClearExpectations(&licence));
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,false));
    }
    pub_trace.clear();
    trace();
    mbx_host_trace([](void *ctx, bool write, uint32_t off, uint32_t value) {
        commit_trace(ctx,write,off,value); pub_writes(ctx,write,off,value);
    },nullptr);
    const uint32_t first=model.tx_sent;
    const uint32_t at=model.now_ms;
    gate(0u,kBaseA);
    advance(400);
    uint32_t withdrawn[MBX_N_IF]{};
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const uint32_t block=MBX_PUB_BASE+MBX_PUB_STRIDE*i;
        std::size_t closed=SIZE_MAX, undeclared=SIZE_MAX;
        for (std::size_t k=0;k<pub_trace.size();++k) {
            const auto &w=pub_trace[k];
            if (w.first==block+MBX_PUB_REG_LICENCE && (w.second&1u)==0u && closed==SIZE_MAX) closed=k;
            if (w.first==block+MBX_PUB_REG_TALKER_DECL && (w.second&1u)==0u && undeclared==SIZE_MAX) undeclared=k;
        }
        EXPECT_TRUE(closed!=SIZE_MAX && undeclared!=SIZE_MAX && closed<undeclared)
            << "a lapse closes LICENCE before TALKER_DECL drops the source";
        const auto ds=talker(i,0,first);
        const auto *lv=leave(ds,1);
        ASSERT_NE(lv,nullptr) << "a source whose parameters lapse withdraws its Talker";
        EXPECT_LE(lv->time_ms,at+220u) << "a source whose parameters lapse withdraws its Talker";
        ASSERT_NE(commit_of(lv->frame),nullptr);
        EXPECT_EQ(commit_of(lv->frame)->pub[i].talker_decl,0u)
            << "TALKER_DECL clears the withdrawn source before its Leave leaves";
        EXPECT_EQ(commit_of(lv->frame)->pub[i].idle_slope_bps,0u)
            << "IDLE_SLOPE drops the withdrawn source before its Leave leaves";
        withdrawn[i]=lv->time_ms;
    }
    EXPECT_TRUE(::testing::Mock::VerifyAndClearExpectations(&licence)) << "a lapse closes the source's licence";
    advance_to(at+25000u);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,0,first);
        EXPECT_EQ(declared(ds,1,withdrawn[i]),nullptr) << "no stale Talker Advertise remains after a lapse";
        EXPECT_EQ(declared(ds,2),nullptr) << "a source whose parameters lapse declares no Talker Failed";
        EXPECT_EQ(pub_of(model,i).talker_decl,0u) << "TALKER_DECL holds the source withdrawn";
    }
}

// Re-declaration: a source whose parameters are valid again with an unchanged destination declares at once (35.2.2.8:
// the same FirstValue may come back immediately).
TEST_F(Talker, UnchangedDestinationIsDeclaredAgainAtOnce) {
    settle(); gate(1u,kBaseA); advance(400);
    trace();
    const uint32_t first=model.tx_sent;
    gate(0u,kBaseA); advance(1000);
    const uint32_t again=model.now_ms;
    gate(1u,kBaseA); advance(400);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,0,first);
        const auto *lv=leave(ds,1);
        ASSERT_NE(lv,nullptr) << "the lapse withdraws the Advertise";
        const auto *adv=declared(ds,1,lv->time_ms+1u);
        ASSERT_NE(adv,nullptr) << "an unchanged destination is declared again at once";
        EXPECT_LE(adv->time_ms,again+220u) << "an unchanged destination is declared again at once";
        EXPECT_EQ(dest(*adv),kBaseA) << "an unchanged destination is declared again at once";
    }
}

// Change and re-allocation: a source valid again at another destination (MAAP's new range after a conflict) is held
// from its Leave's request for two of the longest LeaveAll periods less a JoinTime and THE TRANSMIT's MRPDU (#956):
// nothing of it is declared and TALKER_DECL holds it withdrawn until then, it is declared as the count ends, and it
// reaches the wire no later than the two periods after the request. Once the hold-off has passed, a further change is
// declared at once.
TEST_F(Talker, ChangedDestinationWaitsTwoLongestLeaveAllPeriods) {
    settle(); gate(1u,kBaseA); advance(400);
    while (model.tick_div!=0u) advance(1);
    trace();
    const uint32_t first=model.tx_sent;
    // the Leave's request on a centisecond, so the count ends on one, kHoldOffMs later
    const uint32_t at=model.now_ms;
    gate(0u,kBaseA); settle();
    advance(2000);
    gate(1u,kBaseB);
    advance_to(at+kHoldOffMs-1u);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,0,first);
        const auto *lv=leave(ds,1);
        ASSERT_NE(lv,nullptr) << "the lapse withdraws the Advertise";
        EXPECT_EQ(declared(ds,1,lv->time_ms+1u),nullptr)
            << "no Talker of a changed destination is declared before the hold-off ends";
        EXPECT_EQ(pub_of(model,i).talker_decl&1u,0u) << "TALKER_DECL holds a changed destination withdrawn while it waits";
    }
    advance_to(at+kHoldOffMs);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(pub_of(model,i).talker_decl&1u,1u)
            << "a changed destination is declared two of the longest LeaveAll periods less a JoinTime and THE "
               "TRANSMIT's term after its Leave's request";
    }
    advance_to(at+kTwoLongestLeaveAllMs+400u);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,0,first);
        const auto *lv=leave(ds,1);
        ASSERT_NE(lv,nullptr);
        const auto *adv=declared(ds,1,lv->time_ms+1u);
        ASSERT_NE(adv,nullptr) << "a changed destination is declared once the hold-off ends";
        EXPECT_EQ(dest(*adv),kBaseB) << "a changed destination is declared once the hold-off ends";
        EXPECT_GE(adv->time_ms,at+kHoldOffMs)
            << "the changed destination comes no sooner than two of the longest LeaveAll periods less a JoinTime and "
               "THE TRANSMIT's term after the withdrawal";
        EXPECT_LE(adv->time_ms,at+kTwoLongestLeaveAllMs)
            << "the changed destination reaches the wire no later than two of the longest LeaveAll periods after the "
               "withdrawal";
    }
    // a lapse, then a re-allocation more than the hold-off later: declared at once
    gate(0u,kBaseB); advance_to(model.now_ms+kHoldOffMs+1000u);
    const uint32_t later=model.now_ms;
    const uint32_t next=model.tx_sent;
    gate(1u,kBaseA); advance(400);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,0,next);
        const auto *adv=declared(ds,1);
        ASSERT_NE(adv,nullptr) << "a re-allocation after the hold-off is declared at once";
        EXPECT_LE(adv->time_ms,later+220u) << "a re-allocation after the hold-off is declared at once";
        EXPECT_EQ(dest(*adv),kBaseA) << "a re-allocation after the hold-off is declared at once";
    }
}

// The hold-off counts from the Leave's request, so the two periods must hold the latest the declaration its end owes
// can leave: lwSRP's join timer runs out within a JoinTime of the centisecond the count ends in, and THE TRANSMIT
// commits its MRPDU within CTRL_LOOP_TX_MS of the centisecond that owes it (ctrl_loop.h). With the request on a
// centisecond and the loop held that long from the tick that ends the count, the changed destination still reaches the
// wire no later than two of the longest LeaveAll periods after the request (IEEE 802.1Q-2018 35.2.2.8, 10.7.4.3;
// #956); a hold-off that adds the terms (#951's), drops THE TRANSMIT's term or rounds it down reaches it later.
TEST_F(Talker, ChangedDestinationReachesTheWireWithinTwoLongestLeaveAllPeriodsAtTheLatest) {
    // the withdrawal 700 ms into a second of the participants' periodic transmissions, so the count ends with no MRPDU
    // of theirs in the JoinTime before it: lwSRP's join timer is idle there, and the held loop stands in for its wait
    settle(); gate(1u,kBaseA); advance(700);
    while (model.tick_div!=0u) advance(1);
    trace();
    const uint32_t first=model.tx_sent;
    const uint32_t at=model.now_ms;
    gate(0u,kBaseA); settle();
    advance(2000);
    gate(1u,kBaseB);
    // the loop runs to the centisecond before the one whose tick ends the count, then is held from that tick on
    advance_to(at+kHoldOffMs-100u);
    for (unsigned k=0;k<1000u && adapter.held_cs[0]>1u;++k) advance_to(model.now_ms+1u);
    ASSERT_EQ(adapter.held_cs[0],1u) << "the hold-off counts down a centisecond at a time";
    while (model.tick_div!=9u) advance(1);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        ASSERT_EQ(adapter.join_left[2u*i],0u) << "the join timer is idle as the count ends, so the hold stands in for it";
    }
    const uint32_t end=model.now_ms+1u;
    mbx_model_advance_ms(&model,1u+kLatestMs);
    settle();
    advance(400);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,0,first);
        const auto *lv=leave(ds,1);
        ASSERT_NE(lv,nullptr) << "the lapse withdraws the Advertise";
        const auto *adv=declared(ds,1,lv->time_ms+1u);
        ASSERT_NE(adv,nullptr) << "a changed destination is declared once the hold-off ends";
        EXPECT_EQ(dest(*adv),kBaseB) << "a changed destination is declared once the hold-off ends";
        EXPECT_EQ(adv->time_ms,end+kLatestMs)
            << "the changed destination leaves as late as a JoinTime and THE TRANSMIT's stated figure allow";
        EXPECT_LE(adv->time_ms,at+kTwoLongestLeaveAllMs)
            << "the changed destination reaches the wire no later than two of the longest LeaveAll periods after the "
               "withdrawal, at the latest";
    }
}

// A destination that changes while the source stays valid withdraws the old destination's Advertise and declares the
// new one only once the hold-off ends; no Talker carries the old destination after its Leave.
TEST_F(Talker, DestinationChangeWhileValidWithdrawsTheOld) {
    settle(); gate(1u,kBaseA); advance(400);
    while (model.tick_div!=0u) advance(1);
    trace();
    const uint32_t first=model.tx_sent;
    const uint32_t at=model.now_ms;
    gate(1u,kBaseB); settle();
    advance_to(at+kTwoLongestLeaveAllMs+400u);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,0,first);
        const auto *lv=leave(ds,1);
        ASSERT_NE(lv,nullptr) << "a changed destination withdraws the old destination's Advertise";
        EXPECT_EQ(dest(*lv),kBaseA) << "a changed destination withdraws the old destination's Advertise";
        const auto *adv=declared(ds,1,lv->time_ms+1u);
        ASSERT_NE(adv,nullptr) << "a changed destination is declared once the hold-off ends";
        EXPECT_EQ(dest(*adv),kBaseB) << "a changed destination is declared once the hold-off ends";
        EXPECT_GE(adv->time_ms,at+kHoldOffMs)
            << "the new destination comes no sooner than two of the longest LeaveAll periods less a JoinTime and THE "
               "TRANSMIT's term after the withdrawal";
        EXPECT_LE(adv->time_ms,at+kTwoLongestLeaveAllMs)
            << "the new destination reaches the wire no later than two of the longest LeaveAll periods after the "
               "withdrawal";
        for (const auto &d:ds) {
            if (d.time_ms>lv->time_ms && declares(d.event)) {
                EXPECT_EQ(dest(d),kBaseB) << "no Talker carries the old destination after its Leave";
            }
        }
    }
}

// Admission: an allocated source whose bandwidth does not fit declares Talker Failed, code 1, with its destination; a
// lapse before it frees the bandwidth, and its type swaps in place at once: Advertise joined, then Failed left, so a
// refused join keeps the Failed declared; no hold-off (its FirstValue's Talker part is unchanged).
TEST_F(Talker, AdmissionChangeSwapsTheTypeInPlace) {
    if (CTRL_SRP_SOURCES<2u) GTEST_SKIP();
    srp_mbx_destroy(&adapter);
    // three quarters of 30 Mb/s admit one source
    config.link_rate_bps=30000000u;
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    settle(); gate(3u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,1,0);
        const auto *failed=declared(ds,2);
        ASSERT_NE(failed,nullptr) << "an allocated source whose bandwidth does not fit declares Talker Failed, code 1";
        EXPECT_EQ(failed->value[33],1u)
            << "an allocated source whose bandwidth does not fit declares Talker Failed, code 1";
        EXPECT_EQ(dest(*failed),kBaseA+1u) << "its Talker Failed carries its destination";
        EXPECT_EQ(pub_of(model,i).idle_slope_bps,kAdmittedBps) << "one source fits three quarters of the link";
    }
    // a lapse withdraws a Talker Failed too, and its unchanged destination comes back at once
    uint32_t mark=model.tx_sent;
    gate(1u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_NE(leave(talker(i,1,mark),2),nullptr) << "a lapse withdraws a Talker Failed too";
        EXPECT_EQ(pub_of(model,i).talker_decl,1u) << "a lapse withdraws a Talker Failed too";
    }
    gate(3u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(pub_of(model,i).talker_decl,3u) << "a Talker Failed with an unchanged destination comes back at once";
    }
    trace();
    const uint32_t first=model.tx_sent;
    const uint32_t at=model.now_ms;
    // the swap's join refused (no storage): the declared type stays until the join succeeds
    calloc_before_failure=0;
    gate(2u,kBaseA);
    advance(20);
    calloc_before_failure=-1;
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(pub_of(model,i).talker_decl,2u) << "a swap whose join is refused keeps the declared type";
    }
    advance(400);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,1,first);
        const auto *adv=declared(ds,1);
        ASSERT_NE(adv,nullptr) << "an admission change swaps the type in place at once";
        EXPECT_LE(adv->time_ms,at+640u) << "an admission change swaps the type in place at once";
        EXPECT_EQ(dest(*adv),kBaseA+1u) << "an admission change swaps the type in place at once";
        EXPECT_NE(leave(ds,2),nullptr) << "the Failed leaves as the Advertise joins";
        EXPECT_EQ(pub_of(model,i).idle_slope_bps,kAdmittedBps)
            << "IDLE_SLOPE admits the source the lapse made room for";
        EXPECT_EQ(pub_of(model,i).talker_decl,2u) << "TALKER_DECL holds the swapped source";
    }
    // the source before it valid again takes the bandwidth: the Advertise swaps to Talker Failed, code 1, in place
    mark=model.tx_sent;
    gate(3u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,1,mark);
        const auto *failed=declared(ds,2);
        ASSERT_NE(failed,nullptr) << "an admission lost swaps the Advertise to Talker Failed in place";
        EXPECT_EQ(failed->value[33],1u) << "an admission lost swaps the Advertise to Talker Failed in place";
        EXPECT_NE(leave(ds,1),nullptr) << "an admission lost swaps the Advertise to Talker Failed in place";
        EXPECT_EQ(pub_of(model,i).talker_decl,3u) << "an admission lost swaps the Advertise to Talker Failed in place";
    }
}

// A reset destroys the participants with no Leave sent. An unchanged source declares again at once on the new ones; a
// source whose destination changed before the reset is held as its Leave would hold it.
TEST_F(Talker, ResetKeepsAnUnchangedSourceAndHoldsAMovedOne) {
    settle(); gate(1u,kBaseA); advance(400);
    const unsigned last=MBX_N_IF-1u;
    uint32_t first=model.tx_sent;
    mbx_model_set_link(&model,last,false); settle();
    mbx_model_set_link(&model,last,true); settle();
    advance(400);
    EXPECT_NE(newly(talker(last,0,first),1),nullptr) << "an unchanged source declares again at once after a reset";
    mbx_model_set_link(&model,last,false);
    ctrl_loop_service(&loop);
    ASSERT_EQ(adapter.ifs[last].msrp,nullptr) << "the link change reset the participants";
    const uint32_t at=model.now_ms;
    ASSERT_TRUE(srp_mbx_gate(&adapter,last,1u,kBaseB));
    settle();
    mbx_model_set_link(&model,last,true); settle();
    first=model.tx_sent;
    // the new participants' creation is the hold-off's start, in the centisecond `at` is in
    advance_to(at+kHoldOffMs-10u);
    EXPECT_EQ(declared(talker(last,0,first),1),nullptr)
        << "the new participants hold a source that moved before the reset";
    EXPECT_EQ(pub_of(model,last).talker_decl&1u,0u) << "TALKER_DECL holds it withdrawn while it waits";
    advance_to(at+kTwoLongestLeaveAllMs);
    const auto held=talker(last,0,first);
    const auto *adv=declared(held,1);
    ASSERT_NE(adv,nullptr) << "and declare it once the hold-off ends";
    EXPECT_EQ(dest(*adv),kBaseB) << "and declare it once the hold-off ends";
    EXPECT_LE(adv->time_ms,at+kTwoLongestLeaveAllMs)
        << "and the moved source reaches the wire no later than two of the longest LeaveAll periods after the reset";
}

// The entry: a mask bit past the sources is no source, and before attach, after destroy, for an interface out of
// range and on reentry it refuses and records nothing.
TEST_F(Talker, GateEntryRecordsOnlyWhatChanged) {
    settle();
    ASSERT_TRUE(srp_mbx_gate(&adapter,0,~0u<<CTRL_SRP_SOURCES,kBaseA));
    EXPECT_FALSE(adapter.ifs[0].sources_owed) << "a mask bit past the sources is no source";
    EXPECT_FALSE(srp_mbx_gate(&adapter,MBX_N_IF,1u,kBaseA)) << "an interface out of range is refused";
    adapter.busy=true;
    const uint32_t reentries=adapter.reentries;
    EXPECT_FALSE(srp_mbx_gate(&adapter,0,1u,kBaseA)) << "reentry is refused";
    EXPECT_EQ(adapter.reentries,reentries+1u) << "reentry is refused and counted";
    adapter.busy=false;
    EXPECT_EQ(adapter.ifs[0].gate,0u) << "a refused report records nothing";
    srp_mbx_destroy(&adapter);
    EXPECT_FALSE(srp_mbx_gate(&adapter,0,1u,kBaseA)) << "refused after destroy";
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    EXPECT_FALSE(srp_mbx_gate(&adapter,0,1u,kBaseA)) << "refused before attach";
    EXPECT_EQ(adapter.ifs[0].gate,0u) << "refused before attach, and nothing is recorded";
}

// A refused join (no storage) is counted and declared again with THE TRANSMIT's next declarations, at the JoinTime's
// rate.
TEST_F(Talker, RefusedDeclarationIsDeclaredAgain) {
    settle(); advance(400);
    const unsigned refused=adapter.refused;
    calloc_before_failure=0;
    gate(1u,kBaseA);
    advance(20);
    calloc_before_failure=-1;
    EXPECT_GT(adapter.refused,refused) << "a refused declaration is counted";
    EXPECT_EQ(pub_of(model,0).talker_decl&1u,0u) << "a refused declaration declares nothing";
    trace();
    const uint32_t first=model.tx_sent;
    const uint32_t at=model.now_ms;
    advance(600);
    untrace();
    const auto again=talker(0,0,first);
    const auto *adv=declared(again,1);
    ASSERT_NE(adv,nullptr) << "a refused declaration is declared again";
    EXPECT_LT(adv->time_ms,at+600u) << "a refused declaration is declared again at the JoinTime's rate";
    EXPECT_EQ(pub_of(model,0).talker_decl&1u,1u) << "and TALKER_DECL holds it";
}

// THE TRANSMIT's call publishes an interface's declarations within srp_bounds.h's terms (#895): IDLE_SLOPE and
// TALKER_DECL at most once a declarations pass, so twice on the interface whose MRPDUs the call builds, whose
// declarations after the build repeat a join lwSRP refused, and once on each other; LICENCE once for the licence a
// withdrawal closes; SR_DOMAIN only for an adoption.
TEST_F(Talker, TransmitPublishesWithinItsTermsAfterARefusedJoin) {
    if (CTRL_SRP_SOURCES<2u) GTEST_SKIP();
    settle(); gate(1u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),1,2),i);
    }
    ASSERT_TRUE(::testing::Mock::VerifyAndClearExpectations(&licence));
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,false));
    }
    // source 0 lapses with its licence open, and source 1 is valid, its join refused (no storage)
    calloc_before_failure=0;
    gate(2u,kBaseA);
    ASSERT_TRUE(loop.transmit_aged(loop.transmit_ctx)) << "the declarations owe THE TRANSMIT's call";
    const unsigned built=(adapter.tx_due&1u)!=0u ? 0u : 1u;
    pub_trace.clear();
    mbx_host_trace(pub_writes,nullptr);
    // THE TRANSMIT's call as the loop makes it, and the slices that resume its build (THE TIERS, #894)
    do loop.transmit(loop.transmit_ctx,CTRL_LOOP_BUILD_MOST); while (adapter.tx_resume!=0u);
    untrace();
    calloc_before_failure=-1;
    EXPECT_TRUE(::testing::Mock::VerifyAndClearExpectations(&licence)) << "the withdrawal closes the licence";
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const unsigned passes=i==built ? 2u : 1u;
        EXPECT_EQ(writes(i,MBX_PUB_REG_TALKER_DECL),passes)
            << "THE TRANSMIT's call publishes TALKER_DECL at most once a declarations pass, twice on the interface "
               "it builds";
        EXPECT_EQ(writes(i,MBX_PUB_REG_IDLE_SLOPE),passes)
            << "THE TRANSMIT's call publishes IDLE_SLOPE at most once a declarations pass, twice on the interface "
               "it builds";
        EXPECT_EQ(writes(i,MBX_PUB_REG_LICENCE),1u) << "LICENCE once for the licence the withdrawal closes";
        EXPECT_EQ(writes(i,MBX_PUB_REG_SR_DOMAIN),0u) << "SR_DOMAIN only for an adoption";
        EXPECT_LE(writes(i,MBX_PUB_REG_TALKER_DECL)+writes(i,MBX_PUB_REG_IDLE_SLOPE)+writes(i,MBX_PUB_REG_LICENCE)+
                  writes(i,MBX_PUB_REG_SR_DOMAIN)+writes(i,MBX_PUB_REG_DA_GATE),5u+MBX_N_PUB_SOURCES)
            << "THE TRANSMIT's call publishes at most 5 + MBX_N_PUB_SOURCES writes an interface";
        EXPECT_EQ(pub_of(model,i).talker_decl,0u) << "a refused join declares nothing";
        EXPECT_TRUE(adapter.ifs[i].sources_owed) << "a refused join is owed again";
    }
}

// A withdrawal's Leave lwSRP refuses keeps the source declared and owed (#895). lwSRP refuses a Leave while its
// participant holds the MRPDU the ring refused, which THE TRANSMIT's declarations after its build meet when a Domain
// adoption refused for storage before the build is made after it, the reclaim before the build having freed the room
// (srp_mbx.c, transmit). TALKER_DECL holds the source until lwSRP takes the Leave, with THE TRANSMIT's next
// declarations once the frame has gone, and the Leave goes on the wire.
TEST_F(Talker, RefusedWithdrawalIsWithdrawnOnceLwsrpTakesIt) {
    settle(); gate(1u,kBaseA); advance(400);
    // interface 0's MSRP join timer idle and nothing owed, so THE TRANSMIT's build makes the MRPDU the LeaveAll owes
    for (unsigned k=0;k<2000u && (adapter.join_left[0]!=0u || adapter.tx_due!=0u);++k) advance(1);
    ASSERT_EQ(adapter.join_left[0],0u);
    collect();
    const uint32_t first=model.tx_sent;
    // a peer's Domain, VID 3, owes interface 0 an adoption, and its LeaveAll owes the participant an MRPDU; a Domain
    // it declares empty leaves an attribute mrp_reclaim frees
    receive_before_poll(domains({6,4,0,3},1,true,{6,4,0,5},4));
    ASSERT_TRUE(adapter.ifs[0].domain_owed);
    ASSERT_TRUE(srp_mbx_gate(&adapter,0,0u,kBaseA));
    // every block taken, and given back however the test ends
    struct Held {
        ctrl_pool *pool;
        std::vector<void*> blocks;
        void give() { for (void *p:blocks) ctrl_pool_free(pool,p); blocks.clear(); }
        ~Held() { give(); }
    } held{&pool,{}};
    while (void *p=ctrl_pool_alloc(&pool,1)) held.blocks.push_back(p);
    const unsigned fillers=fill_ring();
    ASSERT_LT(fillers,MBX_MODEL_TX_CAPTURE/2u);
    ASSERT_TRUE(loop.transmit_aged(loop.transmit_ctx));
    ASSERT_EQ(adapter.tx_due&1u,1u) << "THE TRANSMIT's call builds interface 0's MRPDUs";
    trace();
    loop.transmit(loop.transmit_ctx,CTRL_LOOP_BUILD_MOST);
    ASSERT_NE(adapter.owed_len,0u) << "the ring refused the MRPDU built";
    ASSERT_EQ(adapter.ifs[0].domain.vid,3u) << "the adoption refused before the build is made after it";
    EXPECT_EQ(pub_of(model,0).talker_decl&1u,1u) << "a withdrawal lwSRP refused keeps the source declared";
    EXPECT_TRUE(adapter.ifs[0].sources_owed) << "a withdrawal lwSRP refused is owed again";
    EXPECT_EQ(adapter.held_cs[0],0u) << "no hold-off starts at a Leave lwSRP refused";
    held.give();
    mbx_model_tx_pause(&model,false);
    collect();
    advance(1000);
    untrace();
    const auto ds=talker(0,0,first);
    const auto *lv=leave(ds,1);
    ASSERT_NE(lv,nullptr) << "the refused withdrawal's Leave leaves once lwSRP takes it";
    ASSERT_NE(commit_of(lv->frame),nullptr);
    EXPECT_EQ(commit_of(lv->frame)->pub[0].talker_decl&1u,0u)
        << "TALKER_DECL clears the withdrawn source before its Leave leaves";
    EXPECT_EQ(declared(ds,1,lv->time_ms+1u),nullptr) << "no stale Talker Advertise remains after the Leave";
    EXPECT_EQ(pub_of(model,0).talker_decl&1u,0u) << "TALKER_DECL holds the source withdrawn";
    EXPECT_NE(adapter.held_cs[0],0u) << "the hold-off starts at the Leave lwSRP took";
    EXPECT_FALSE(adapter.ifs[0].sources_owed) << "nothing is owed once lwSRP takes the Leave";
}

// #936: a source's STREAM_OUTPUT shows its Talker declaration (Milan v1.2 5.4.2.10.2, Table 5.11), so each change of
// it is noticed, on the interface that declares it, for its GET_STREAM_INFO notice (Milan v1.2 5.4.5.2, Table 5.22;
// IEEE 1722.1-2021 7.5.2). A declaration and a withdrawal are each noticed once; a report that changes nothing, and
// the periodic declarations of a Talker already declared, notice nothing.
TEST_F(Talker, DeclarationAndWithdrawalAreNoticed) {
    settle(); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(adapter.ifs[i].noticed,0u) << "a source that declares nothing is not noticed";
    }
    gate(1u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(adapter.ifs[i].noticed,1u) << "a declaration is noticed";
        adapter.ifs[i].noticed=0u;
    }
    gate(1u,kBaseA); advance(1200);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(adapter.ifs[i].noticed,0u) << "a declaration that did not change is not noticed again";
    }
    gate(0u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(adapter.ifs[i].noticed,1u) << "a withdrawal is noticed";
        adapter.ifs[i].noticed=0u;
    }
    advance(1200);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(adapter.ifs[i].noticed,0u) << "a withdrawal is noticed once";
    }
}

// #936: a Talker Advertise and a Talker Failed show differently (Table 5.11's MSRP_FAILURE_VALID, the failure code and
// bridge ID), so a type its admission swaps in place is noticed, the swap that lwSRP refuses only once it is made, and
// a Talker Failed declared or withdrawn is noticed as an Advertise is.
TEST_F(Talker, TypeSwapIsNoticed) {
    if (CTRL_SRP_SOURCES<2u) GTEST_SKIP();
    srp_mbx_destroy(&adapter);
    // three quarters of 30 Mb/s admit one source
    config.link_rate_bps=30000000u;
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    settle(); gate(3u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        ASSERT_EQ(pub_of(model,i).talker_decl,3u);
        EXPECT_EQ(adapter.ifs[i].noticed,3u) << "a Talker Failed declared is noticed";
        adapter.ifs[i].noticed=0u;
    }
    gate(1u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(adapter.ifs[i].noticed,2u) << "a Talker Failed withdrawn is noticed";
        adapter.ifs[i].noticed=0u;
    }
    gate(3u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) adapter.ifs[i].noticed=0u;
    // source 0 lapses, and source 1's swap to Advertise is refused (no storage): only the withdrawal is noticed
    calloc_before_failure=0;
    gate(2u,kBaseA);
    advance(20);
    calloc_before_failure=-1;
    for (unsigned i=0;i<MBX_N_IF;++i) {
        ASSERT_EQ(pub_of(model,i).talker_decl,2u);
        EXPECT_EQ(adapter.ifs[i].noticed,1u) << "a swap lwSRP refuses is not noticed until it is made";
        adapter.ifs[i].noticed=0u;
    }
    advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        ASSERT_TRUE(adapter.ifs[i].admitted[1]) << "the swap is made";
        EXPECT_EQ(adapter.ifs[i].noticed,2u) << "a type swapped in place is noticed";
        adapter.ifs[i].noticed=0u;
    }
    gate(3u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        ASSERT_FALSE(adapter.ifs[i].admitted[1]) << "the Advertise swaps back to Talker Failed";
        EXPECT_EQ(adapter.ifs[i].noticed&2u,2u) << "a type swapped in place is noticed";
    }
}

// #936: a declared Talker carries the Domain's VID, its STREAM_OUTPUT's stream_vlan_id (Table 5.11), so an adopted
// Domain that moves the VID notices every source it declares again, on its own interface only; one that keeps the VID
// (another priority) notices nothing, and neither notices a source not declared.
TEST_F(Talker, AdoptedDomainVidIsNoticed) {
    settle(); gate(1u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) adapter.ifs[i].noticed=0u;
    offer(frame(4,{6,4,0,3},0)); advance(400);
    ASSERT_EQ(adapter.ifs[0].domain.vid,3u);
    EXPECT_EQ(adapter.ifs[0].noticed,1u) << "a declared Talker carrying another VID is noticed";
    for (unsigned i=1;i<MBX_N_IF;++i) {
        EXPECT_EQ(adapter.ifs[i].noticed,0u) << "a Domain adopted on one interface notices that interface's sources";
    }
    adapter.ifs[0].noticed=0u;
    offer(frame(4,{6,5,0,3},0)); advance(400);
    ASSERT_EQ(adapter.ifs[0].domain.priority,5u);
    EXPECT_EQ(adapter.ifs[0].noticed,0u) << "a Domain that keeps the VID notices nothing";
}

// #936: a reset destroys the participants and declares an unchanged source again on the new ones, which its
// STREAM_OUTPUT shows as it did: nothing is noticed.
TEST_F(Talker, ResetNoticesNothingUnchanged) {
    settle(); gate(1u,kBaseA); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) adapter.ifs[i].noticed=0u;
    const unsigned last=MBX_N_IF-1u;
    const uint32_t first=model.tx_sent;
    mbx_model_set_link(&model,last,false); settle();
    mbx_model_set_link(&model,last,true); settle();
    advance(400);
    ASSERT_NE(newly(talker(last,0,first),1),nullptr) << "the reset declares the source again";
    EXPECT_EQ(adapter.ifs[last].noticed,0u) << "a source a reset declares again unchanged is not noticed";
}

// #957: a source's STREAM_OUTPUT shows the Listener registered for its stream on the interface (#943's REGISTERING and
// REGISTERING_FAILED), so each change of that registration, a Listener Ready, Ready Failed or Asking Failed appearing,
// replacing another or going, the registrar's reset with its link included, is noticed on that interface for the
// output's GET_STREAM_INFO notice (Milan v1.2 5.4.5.2, Table 5.22; IEEE 1722.1-2021 7.5.2). A Listener declared again
// unchanged, its registration kept over a LeaveAll and a reset with none registered notice nothing; another stream's
// Listener notices its own source; neither is a Talker's record.
TEST_F(Talker, ListenerRegistrationChangeIsNoticed) {
    settle(); advance(400);
    const unsigned n=CTRL_SRP_SOURCES-1u;
    // the record since it was last taken, taken as the composition takes it (ctrl_app_srp.c)
    auto taken=[&](unsigned i){
        const uint32_t r=adapter.ifs[i].registration_noticed;
        adapter.ifs[i].registration_noticed=0u;
        return r;
    };
    for (unsigned i=0;i<MBX_N_IF;++i) EXPECT_EQ(taken(i),0u) << "no Listener registered, nothing is noticed";
    for (unsigned i=0;i<MBX_N_IF;++i) {
        offer(frame(3,identity(i,n),1,2),i); advance(20);
        EXPECT_EQ(taken(i),1u<<n) << "a Listener Ready appearing is noticed";
        for (unsigned k=0;k<MBX_N_IF;++k) {
            if (k!=i) {
                EXPECT_EQ(taken(k),0u) << "a Listener is noticed on its own interface";
            }
        }
        offer(frame(3,identity(i,n),1,2),i); advance(20);
        EXPECT_EQ(taken(i),0u) << "a Listener declared again unchanged is not noticed";
        // a LeaveAll of the Listener attribute type with the Listener's JoinIn after it in its message (IEEE 802.1Q-2018
        // 10.8.2.2): its Registrar leaves IN and registers again
        offer(frame(3,identity(i,n),1,2,true),i); advance(1200);
        EXPECT_EQ(taken(i),0u) << "a Listener registered again after a LeaveAll is not noticed";
        offer(frame(3,identity(i,n),1,3),i); advance(20);
        EXPECT_EQ(taken(i),1u<<n) << "a Listener Ready Failed replacing a Ready is noticed";
        offer(frame(3,identity(i,n),1,1),i); advance(20);
        EXPECT_EQ(taken(i),1u<<n) << "a Listener Asking Failed replacing a Ready Failed is noticed";
        if (n!=0u) {
            offer(frame(3,identity(i,0),1,2),i); advance(20);
            EXPECT_EQ(taken(i),1u) << "another stream's Listener notices its own source";
            offer(frame(3,identity(i,0),5,2),i); advance(1200);
            EXPECT_EQ(taken(i),1u) << "another stream's Listener notices its own source";
        }
        offer(frame(3,identity(i,n),5,1),i); advance(1200);
        EXPECT_EQ(taken(i),1u<<n) << "a Listener going is noticed";
        EXPECT_EQ(adapter.ifs[i].noticed,0u) << "a Listener's registration is not a Talker's record";
    }
    const unsigned last=MBX_N_IF-1u;
    offer(frame(3,identity(last,n),1,1),last); advance(20);
    ASSERT_EQ(taken(last),1u<<n) << "a Listener Asking Failed appearing is noticed";
    mbx_model_set_link(&model,last,false); settle();
    EXPECT_EQ(taken(last),1u<<n) << "a reset with a Listener registered notices it going";
    mbx_model_set_link(&model,last,true); settle(); advance(400);
    EXPECT_EQ(taken(last),0u) << "a reset with no Listener registered notices nothing";
}
