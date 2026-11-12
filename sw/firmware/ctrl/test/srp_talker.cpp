// SPDX-License-Identifier: CERN-OHL-W-2.0
// SRP's Talker declarations follow MAAP's allocation (#895): srp_mbx_allocation
// records each source's destination and THE TRANSMIT declares it. A source
// allocated and admitted declares Talker Advertise with base + n and its TSpec,
// and Talker Failed otherwise, code 2 without an allocation and 1 when its
// bandwidth does not fit (IEEE 802.1Q-2018 35.2.2.8.7, Table 35-6). MSRP does
// not support a changed FirstValue on a StreamID (35.2.2.8): a declared source
// whose destination moves (an allocation, a change, a loss) or whose type its
// admission changes withdraws, its TALKER_DECL bit cleared before the Leave
// leaves, and declares again no sooner than two LeaveAllTime periods after the
// Leave (Table 10-7). A reset of the participants holds a moved source as its
// Leave would. Run at 1x1/1if and 8x8/2if (test_ctrl_firmware.py).
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
// The fixture's configured destination of source n (srp_fixture.hpp).
constexpr uint64_t kConfigured=0x91e0f0000000ull;
// The withdrawal's hold-off in ms: two LeaveAllTime periods (Table 10-7, 1000 cs each), and the hold-off as
// srp_mbx.c counts it from the Leave's request, with a JoinTime and THE TRANSMIT's bound added.
constexpr uint32_t kTwoLeaveAllMs=20000u;
constexpr uint32_t kHoldOffMs=20220u;

bool declares(unsigned event) { return event==0u || event==1u || event==3u; }

class Talker : public Srp {
protected:
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
};

}  // namespace

// Allocate: a source declaring Talker Failed for want of a destination withdraws it once MAAP allocates one, and
// declares Talker Advertise with base + n and its TSpec no sooner than two LeaveAllTime periods after the Leave. No
// Talker of that StreamID is declared in between, and a source whose destination did not move is not declared again.
TEST_F(Talker, AllocationWithdrawsTheFailedThenAdvertisesTheDestination) {
    settle(); advance(400);
    const unsigned n=CTRL_SRP_SOURCES-1u;
    const uint64_t base=0x91e0f000aa00ull;
    const uint32_t all=(1u<<CTRL_SRP_SOURCES)-1u;
    trace();
    const uint32_t first=model.tx_sent;
    const uint32_t at=model.now_ms;
    ASSERT_TRUE(srp_mbx_allocation(&adapter,1u<<n,base,CTRL_SRP_SOURCES,true));
    advance(400);
    uint32_t withdrawn[MBX_N_IF]{};
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,n,first);
        const auto *lv=leave(ds,2);
        ASSERT_NE(lv,nullptr) << "an allocation withdraws the source's Talker Failed";
        EXPECT_LE(lv->time_ms,at+220u) << "an allocation withdraws the source's Talker Failed within a JoinTime";
        ASSERT_NE(commit_of(lv->frame),nullptr);
        EXPECT_EQ(commit_of(lv->frame)->pub[i].talker_decl,all&~(1u<<n))
            << "TALKER_DECL clears the withdrawn source before its Leave leaves";
        withdrawn[i]=lv->time_ms;
        const auto zero=talker(i,0,first);
        EXPECT_EQ(newly(zero,1),nullptr) << "a Talker whose destination did not move is not declared again";
    }
    advance_to(at+kTwoLeaveAllMs);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,n,first);
        EXPECT_EQ(declared(ds,1),nullptr) << "no Talker of a moved destination is declared before the hold-off ends";
        EXPECT_EQ(declared(ds,2),nullptr) << "no Talker of a moved destination is declared before the hold-off ends";
        EXPECT_EQ(pub_of(model,i).talker_decl,all&~(1u<<n)) << "TALKER_DECL holds the source withdrawn while it waits";
    }
    advance_to(at+kHoldOffMs+400u);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,n,first);
        const auto *adv=declared(ds,1);
        ASSERT_NE(adv,nullptr) << "declares Talker Advertise with the allocated destination once the hold-off ends";
        EXPECT_EQ(adv->event,0u) << "declares Talker Advertise with the allocated destination once the hold-off ends";
        EXPECT_EQ(dest(*adv),base+n) << "declares Talker Advertise with the allocated destination once the hold-off ends";
        EXPECT_EQ(wire_be16(adv->value.data()+14),2u) << "the Advertise carries the Domain's VID";
        EXPECT_EQ(wire_be16(adv->value.data()+16),224u) << "the Advertise carries the source's TSpec";
        EXPECT_EQ(wire_be16(adv->value.data()+18),1u) << "the Advertise carries the source's TSpec";
        EXPECT_GE(adv->time_ms,withdrawn[i]+kTwoLeaveAllMs)
            << "the Advertise comes no sooner than two LeaveAllTime periods after the Leave";
        EXPECT_EQ(declared(ds,2,withdrawn[i]),nullptr) << "and no Talker Failed is declared again";
        ASSERT_NE(commit_of(adv->frame),nullptr);
        EXPECT_EQ(commit_of(adv->frame)->pub[i].talker_decl,all) << "TALKER_DECL is set before the Advertise leaves";
        EXPECT_EQ(commit_of(adv->frame)->pub[i].idle_slope_bps,2u*kAdmittedBps)
            << "IDLE_SLOPE admits the source before its Advertise leaves";
    }
}

// Lose: an advertised source whose allocation is lost closes its licence, then withdraws its Advertise, TALKER_DECL
// and IDLE_SLOPE dropping it before the Leave leaves; no Advertise of it is declared again, LeaveAll included, and
// once the hold-off ends it declares Talker Failed, code 2, with no destination and the interface's MAC.
TEST_F(Talker, LossWithdrawsTheAdvertiseAndDeclaresFailedAfterTheHoldOff) {
    settle(); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,true)); offer(frame(3,identity(i),1,2),i);
    }
    ASSERT_TRUE(::testing::Mock::VerifyAndClearExpectations(&licence));
    const uint32_t all=(1u<<CTRL_SRP_SOURCES)-1u;
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
    ASSERT_TRUE(srp_mbx_allocation(&adapter,1u,kConfigured,CTRL_SRP_SOURCES,false));
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
            << "a loss closes LICENCE before TALKER_DECL drops the source";
        const auto ds=talker(i,0,first);
        const auto *lv=leave(ds,1);
        ASSERT_NE(lv,nullptr) << "a loss withdraws the source's Talker Advertise";
        ASSERT_NE(commit_of(lv->frame),nullptr);
        EXPECT_EQ(commit_of(lv->frame)->pub[i].talker_decl,all&~1u)
            << "TALKER_DECL clears the lost source before its Leave leaves";
        EXPECT_EQ(commit_of(lv->frame)->pub[i].idle_slope_bps,0u)
            << "IDLE_SLOPE drops the lost source before its Leave leaves";
        withdrawn[i]=lv->time_ms;
    }
    EXPECT_TRUE(::testing::Mock::VerifyAndClearExpectations(&licence)) << "a loss closes the source's licence";
    advance_to(at+kHoldOffMs+400u);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,0,first);
        EXPECT_EQ(declared(ds,1,withdrawn[i]),nullptr) << "no stale Talker Advertise remains after a loss";
        const auto *failed=declared(ds,2);
        ASSERT_NE(failed,nullptr) << "a lost source declares Talker Failed once the hold-off ends";
        EXPECT_GE(failed->time_ms,withdrawn[i]+kTwoLeaveAllMs)
            << "the Failed comes no sooner than two LeaveAllTime periods after the Leave";
        EXPECT_EQ(dest(*failed),0u) << "a lost source's Talker Failed carries no destination";
        ASSERT_EQ(failed->value.size(),34u);
        EXPECT_EQ(failed->value[33],2u) << "a lost source's Talker Failed carries code 2";
        uint64_t system=0;
        for (unsigned b=25;b<33;++b) system=system<<8|failed->value[b];
        EXPECT_EQ(system,config.mac[i]) << "the Talker Failed names the interface's MAC";
        EXPECT_EQ(pub_of(model,i).talker_decl,all) << "TALKER_DECL holds the Failed declaration";
    }
}

// Change: an advertised source whose destination changes withdraws the old destination's Advertise and advertises the
// new one only once the hold-off ends; no Advertise carries the old destination after its Leave.
TEST_F(Talker, ChangeWithdrawsTheOldDestinationAndAdvertisesTheNew) {
    settle(); advance(400);
    const uint64_t base=0x91e0f000bb00ull;
    trace();
    const uint32_t first=model.tx_sent;
    const uint32_t at=model.now_ms;
    ASSERT_TRUE(srp_mbx_allocation(&adapter,1u,base,CTRL_SRP_SOURCES,true));
    advance_to(at+kHoldOffMs+400u);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,0,first);
        const auto *lv=leave(ds,1);
        ASSERT_NE(lv,nullptr) << "a changed destination withdraws the old destination's Advertise";
        EXPECT_EQ(dest(*lv),kConfigured) << "a changed destination withdraws the old destination's Advertise";
        const auto *adv=declared(ds,1,lv->time_ms);
        ASSERT_NE(adv,nullptr) << "a changed destination is advertised once the hold-off ends";
        EXPECT_EQ(dest(*adv),base) << "a changed destination is advertised once the hold-off ends";
        EXPECT_GE(adv->time_ms,lv->time_ms+kTwoLeaveAllMs)
            << "the new destination comes no sooner than two LeaveAllTime periods after the Leave";
        for (const auto &d:ds) {
            if (d.time_ms>lv->time_ms && declares(d.event)) {
                EXPECT_EQ(dest(d),base) << "no Talker carries the old destination after its Leave";
            }
        }
    }
}

// Re-allocate: a source allocated again while it waits declares the newest destination, still when the hold-off that
// began at its withdrawal ends: a report in the meantime neither declares nor restarts it.
TEST_F(Talker, ReallocationDuringTheHoldOffAdvertisesTheLatest) {
    settle(); advance(400);
    const uint64_t base=0x91e0f000cc00ull;
    trace();
    const uint32_t first=model.tx_sent;
    const uint32_t at=model.now_ms;
    ASSERT_TRUE(srp_mbx_allocation(&adapter,1u,kConfigured,CTRL_SRP_SOURCES,false));
    advance(5000);
    ASSERT_TRUE(srp_mbx_allocation(&adapter,1u,base,CTRL_SRP_SOURCES,true));
    advance_to(at+kHoldOffMs+400u);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,0,first);
        const auto *lv=leave(ds,1);
        ASSERT_NE(lv,nullptr) << "the loss withdraws the Advertise";
        EXPECT_EQ(declared(ds,2),nullptr) << "a source allocated again while it waits declares no Talker Failed";
        const auto *adv=declared(ds,1,lv->time_ms);
        ASSERT_NE(adv,nullptr) << "a re-allocated source advertises its newest destination when the hold-off ends";
        EXPECT_EQ(dest(*adv),base) << "a re-allocated source advertises its newest destination when the hold-off ends";
        EXPECT_GE(adv->time_ms,lv->time_ms+kTwoLeaveAllMs)
            << "the re-allocated destination comes no sooner than two LeaveAllTime periods after the Leave";
        EXPECT_LT(adv->time_ms,at+kHoldOffMs+400u)
            << "the hold-off runs from the withdrawal, not from the re-allocation";
    }
}

// Admission: an allocated source whose bandwidth does not fit declares Talker Failed, code 1, with its destination. A
// loss before it frees the bandwidth: its type would change, so it withdraws too and advertises once the hold-off
// ends, while the lost source declares Talker Failed, code 2.
TEST_F(Talker, AdmissionChangeWithdrawsAndAdvertisesAfterTheHoldOff) {
    srp_mbx_destroy(&adapter);
    // three quarters of 30 Mb/s admit one source
    config.link_rate_bps=30000000u;
    for (unsigned i=0;i<MBX_N_IF;++i) sources[i][1].allocated=true;
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    settle(); advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(pub_of(model,i).idle_slope_bps,kAdmittedBps) << "one source fits three quarters of the link";
    }
    trace();
    const uint32_t at=model.now_ms;
    advance(1100);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,1,0);
        const auto *failed=declared(ds,2);
        ASSERT_NE(failed,nullptr) << "an allocated source whose bandwidth does not fit declares Talker Failed, code 1";
        EXPECT_EQ(failed->value[33],1u) << "an allocated source whose bandwidth does not fit declares Talker Failed, code 1";
        EXPECT_EQ(dest(*failed),kConfigured+1u) << "its Talker Failed carries its destination";
    }
    const uint32_t first=model.tx_sent;
    ASSERT_TRUE(srp_mbx_allocation(&adapter,1u,kConfigured,CTRL_SRP_SOURCES,false));
    advance_to(at+1100u+kHoldOffMs+400u);
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=talker(i,1,first);
        const auto *lv=leave(ds,2);
        ASSERT_NE(lv,nullptr) << "a source whose admission changes withdraws its Talker Failed";
        const auto *adv=declared(ds,1);
        ASSERT_NE(adv,nullptr) << "and advertises its destination once the hold-off ends";
        EXPECT_EQ(dest(*adv),kConfigured+1u) << "and advertises its destination once the hold-off ends";
        EXPECT_GE(adv->time_ms,lv->time_ms+kTwoLeaveAllMs)
            << "the admitted source comes no sooner than two LeaveAllTime periods after its Leave";
        const auto zero=talker(i,0,first);
        const auto *lost=declared(zero,2);
        ASSERT_NE(lost,nullptr) << "the lost source declares Talker Failed, code 2";
        EXPECT_EQ(lost->value[33],2u) << "the lost source declares Talker Failed, code 2";
        EXPECT_EQ(pub_of(model,i).idle_slope_bps,kAdmittedBps) << "IDLE_SLOPE admits the source the loss made room for";
    }
}

// A reset after a move: the participants are destroyed with no Leave sent, and the new ones hold the moved source
// for the hold-off as its Leave would; a source whose destination did not move declares again at once.
TEST_F(Talker, MoveBeforeAResetIsHeldByTheNewParticipants) {
    settle(); advance(400);
    const unsigned last=MBX_N_IF-1u;
    const uint64_t base=0x91e0f000dd00ull;
    trace();
    mbx_model_set_link(&model,last,false);
    ctrl_loop_service(&loop);
    ASSERT_EQ(adapter.ifs[last].msrp,nullptr) << "the link change reset the participants";
    const uint32_t at=model.now_ms;
    ASSERT_TRUE(srp_mbx_allocation(&adapter,1u,base,CTRL_SRP_SOURCES,true));
    settle();
    mbx_model_set_link(&model,last,true); settle();
    const uint32_t first=model.tx_sent;
    advance(1000);
    if (CTRL_SRP_SOURCES>1u) {
        EXPECT_NE(declared(talker(last,1,first),2),nullptr) << "an unmoved source declares again at once after a reset";
    }
    advance_to(at+kTwoLeaveAllMs);
    EXPECT_EQ(declared(talker(last,0,first),1),nullptr) << "the new participants hold a source that moved before the reset";
    EXPECT_EQ(pub_of(model,last).talker_decl&1u,0u) << "TALKER_DECL holds it withdrawn while it waits";
    advance_to(at+kHoldOffMs+400u);
    untrace();
    const auto held=talker(last,0,first);
    const auto *adv=declared(held,1);
    ASSERT_NE(adv,nullptr) << "and advertise it once the hold-off ends";
    EXPECT_EQ(dest(*adv),base) << "and advertise it once the hold-off ends";
}

// The entry: a repeated report changes no declaration, a source past the reported count has no destination, a mask
// bit past the sources is no source, and before attach, after destroy and on reentry it refuses and records nothing.
TEST_F(Talker, AllocationEntryRecordsOnlyWhatChanged) {
    settle(); advance(400);
    trace();
    const uint32_t first=model.tx_sent;
    ASSERT_TRUE(srp_mbx_allocation(&adapter,1u,kConfigured,CTRL_SRP_SOURCES,true));
    ASSERT_TRUE(srp_mbx_allocation(&adapter,~0u<<CTRL_SRP_SOURCES,0x91e0f000ee00ull,CTRL_SRP_SOURCES,true));
    EXPECT_EQ(adapter.reported,1u) << "a mask bit past the sources is no source";
    advance(400);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(leave(talker(i,0,first),1),nullptr) << "a repeated allocation changes no declaration";
    }
    ASSERT_TRUE(srp_mbx_allocation(&adapter,3u,0x91e0f000ee00ull,1,true));
    EXPECT_EQ(adapter.allocated&3u,1u) << "a source past the reported count has no destination";
    settle();
    untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_TRUE(adapter.ifs[i].sources[0].allocated) << "a source within the reported count holds base + n";
        uint64_t d=0;
        for (unsigned b=0;b<6;++b) d=d<<8|adapter.ifs[i].sources[0].value.dest_mac[b];
        EXPECT_EQ(d,0x91e0f000ee00ull) << "a source within the reported count holds base + n";
        if (CTRL_SRP_SOURCES>1u) {
            EXPECT_FALSE(adapter.ifs[i].sources[1].allocated) << "a source past the reported count has no destination";
            for (unsigned b=0;b<6;++b) {
                EXPECT_EQ(adapter.ifs[i].sources[1].value.dest_mac[b],0u)
                    << "a source past the reported count has no destination";
            }
        }
    }
    adapter.busy=true;
    const uint32_t reentries=adapter.reentries;
    EXPECT_FALSE(srp_mbx_allocation(&adapter,1u,0x91e0f000ff00ull,CTRL_SRP_SOURCES,true)) << "reentry is refused";
    EXPECT_EQ(adapter.reentries,reentries+1u) << "reentry is refused and counted";
    adapter.busy=false;
    EXPECT_EQ(adapter.dest[0],0x91e0f000ee00ull) << "a refused report records nothing";
    srp_mbx_destroy(&adapter);
    EXPECT_FALSE(srp_mbx_allocation(&adapter,1u,0x91e0f000ff00ull,CTRL_SRP_SOURCES,true)) << "refused after destroy";
    EXPECT_EQ(adapter.dest[0],0x91e0f000ee00ull) << "refused after destroy, and nothing is recorded";
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    EXPECT_FALSE(srp_mbx_allocation(&adapter,1u,0x91e0f000ff00ull,CTRL_SRP_SOURCES,true)) << "refused before attach";
    EXPECT_EQ(adapter.reported,0u) << "refused before attach, and nothing is recorded";
}

// A refused join of a source whose hold-off ended (no storage) is counted and declared again with THE TRANSMIT's
// next declarations, at the JoinTime's rate.
TEST_F(Talker, RefusedRedeclarationIsDeclaredAgain) {
    settle(); advance(400);
    const unsigned n=CTRL_SRP_SOURCES-1u;
    const uint32_t at=model.now_ms;
    ASSERT_TRUE(srp_mbx_allocation(&adapter,1u<<n,0x91e0f000aa00ull,CTRL_SRP_SOURCES,true));
    advance(400);
    ASSERT_NE(adapter.ifs[0].held_cs[n],0u) << "the allocation withdrew the source";
    while (adapter.ifs[0].held_cs[n]>1u) advance(1);
    collected=model.tx_sent;
    const unsigned refused=adapter.refused;
    calloc_before_failure=0;
    advance(20);
    calloc_before_failure=-1;
    EXPECT_GT(adapter.refused,refused) << "a refused re-declaration is counted";
    EXPECT_EQ(pub_of(model,0).talker_decl>>n&1u,0u) << "a refused re-declaration declares nothing";
    trace();
    const uint32_t first=model.tx_sent;
    advance(600);
    untrace();
    const auto again=talker(0,n,first);
    const auto *adv=declared(again,1);
    ASSERT_NE(adv,nullptr) << "a refused re-declaration is declared again";
    EXPECT_LT(adv->time_ms,at+kHoldOffMs+1200u) << "a refused re-declaration is declared again at the JoinTime's rate";
    EXPECT_EQ(pub_of(model,0).talker_decl>>n&1u,1u) << "and TALKER_DECL holds it";
}
