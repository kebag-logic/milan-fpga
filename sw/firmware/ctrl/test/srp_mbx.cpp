// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "srp_fixture.hpp"
#include <array>
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
    // a down interface sends nothing: every later frame of it is the restart's,
    // the first of them sent while the link comes back
    const uint32_t restarted=model.tx_sent;
    mbx_model_set_link(&model,0,false); settle(); mbx_model_set_link(&model,0,true); settle();
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
        EXPECT_EQ(pub_of(model,i).idle_slope_bps,kAdmittedBps) << "PUB IDLE_SLOPE is the admitted bandwidth from startup";
    }
    const unsigned last=MBX_N_IF-1u;
    // a value the firmware did not write, then a link restart: the slope is
    // published again before the restart's first declaration leaves
    mbx_model_write(&model,MBX_PUB_BASE+MBX_PUB_STRIDE*last+MBX_PUB_REG_IDLE_SLOPE,0u,0xFu);
    ASSERT_EQ(pub_of(model,last).idle_slope_bps,0u);
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
        EXPECT_EQ(c.pub[last].idle_slope_bps,kAdmittedBps)
            << "PUB every MRPDU of the restarted interface left with IDLE_SLOPE published again";
    }
    EXPECT_GT(left,0u) << "PUB the restarted interface declared again";
}

// TALKER_DECL (#665 comment 6092086337): every source's Talker attribute is
// declared, so its bit is set before any MRPDU carrying it leaves, and cleared
// before the participants holding it are destroyed: by a link restart, before
// the new participants declare again, and by destroy.
std::vector<std::pair<uint32_t,uint32_t>> pub_trace;
void pub_writes(void*, bool write, uint32_t off, uint32_t value) {
    if (write && off>=MBX_PUB_BASE && off<MBX_PUB_BASE+MBX_N_IF*MBX_PUB_STRIDE) pub_trace.emplace_back(off,value);
}

TEST_F(Srp, PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst) {
    const uint32_t all=(1u<<CTRL_SRP_SOURCES)-1u;
    settle();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(pub_of(model,i).talker_decl,all) << "PUB TALKER_DECL holds every declared source from startup";
        EXPECT_EQ(pub_of(model,i).licence,0u) << "PUB and is not the licence: no Listener is registered";
    }
    const unsigned last=MBX_N_IF-1u;
    const uint32_t block=MBX_PUB_BASE+MBX_PUB_STRIDE*last;
    // a value the firmware did not write, then a link restart: the
    // declarations are withdrawn, then published again before the restart's
    // first declaration leaves
    mbx_model_write(&model,block+MBX_PUB_REG_TALKER_DECL,0u,0xFu);
    pub_trace.clear(); mbx_host_trace(pub_writes,nullptr);
    mbx_model_set_link(&model,last,false); settle();
    mbx_host_trace(nullptr,nullptr);
    std::size_t withdrawn=SIZE_MAX, recreated=SIZE_MAX;
    for (std::size_t n=0;n<pub_trace.size();++n) {
        if (pub_trace[n].first==block+MBX_PUB_REG_TALKER_DECL && pub_trace[n].second==0u && withdrawn==SIZE_MAX)
            withdrawn=n;
        if (pub_trace[n].first==block+MBX_PUB_REG_SR_DOMAIN && recreated==SIZE_MAX) recreated=n;
    }
    EXPECT_TRUE(withdrawn!=SIZE_MAX && recreated!=SIZE_MAX && withdrawn<recreated)
        << "PUB a link restart withdraws TALKER_DECL before the new participants declare";
    EXPECT_EQ(pub_of(model,last).talker_decl,all) << "PUB and publishes it again as they declare";
    commits_seen.clear(); traced_model=&model; mbx_host_trace(commit_trace,nullptr);
    const uint32_t first=model.tx_sent;
    mbx_model_write(&model,block+MBX_PUB_REG_TALKER_DECL,0u,0xFu);
    mbx_model_set_link(&model,last,true); settle();
    advance(200);
    mbx_host_trace(nullptr,nullptr);
    capture();
    unsigned talkers=0;
    for (const auto &d:declarations) {
        if (d.interface!=last || d.ethertype!=0x22ea || d.frame<first || commit_of(d.frame)==nullptr) continue;
        if (d.type!=1 && d.type!=2) continue;
        ++talkers;
        EXPECT_EQ(commit_of(d.frame)->pub[last].talker_decl,all)
            << "PUB every MRPDU carrying a Talker declaration left with TALKER_DECL published again";
    }
    EXPECT_GT(talkers,0u) << "PUB the restarted interface declared its Talkers again";
    for (unsigned i=0;i+1u<MBX_N_IF;++i) {
        EXPECT_EQ(pub_of(model,i).talker_decl,all) << "PUB another interface keeps its own declarations";
    }
    srp_mbx_destroy(&adapter);
    for (unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_EQ(pub_of(model,i).talker_decl,0u) << "PUB destroy withdraws every declaration from the datapath";
    }
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
}

// TALKER_DECL across a Domain adoption (#665, comment 6095903333): the
// adoption declares every source again under the adopted VID, and
// declare_sources publishes TALKER_DECL again before those declarations
// leave. A value the firmware did not write stands in the register first, so
// an adoption that skips the publication shows too; it holds after.
TEST_F(Srp, PubTalkerDeclHoldsAcrossADomainAdoption) {
    const uint32_t all=(1u<<CTRL_SRP_SOURCES)-1u;
    settle();
    ASSERT_EQ(pub_of(model,0).talker_decl,all);
    mbx_model_write(&model,MBX_PUB_BASE+MBX_PUB_REG_TALKER_DECL,0u,0xFu);
    commits_seen.clear(); traced_model=&model; mbx_host_trace(commit_trace,nullptr);
    const uint32_t first=model.tx_sent;
    offer(frame(4,{6,4,0,3},0)); advance(200);
    mbx_host_trace(nullptr,nullptr);
    capture();
    unsigned talkers=0;
    for (const auto &d:declarations) {
        if (d.interface!=0 || d.ethertype!=0x22ea || d.frame<first || commit_of(d.frame)==nullptr) continue;
        if ((d.type!=1 && d.type!=2) || wire_be16(d.value.data()+14)!=3u) continue;
        ++talkers;
        EXPECT_EQ(commit_of(d.frame)->pub[0].talker_decl,all)
            << "PUB every Talker MRPDU under the adopted VID left with TALKER_DECL published again";
    }
    EXPECT_GT(talkers,0u) << "PUB the adoption declared the Talkers again under the adopted VID";
    EXPECT_EQ(pub_of(model,0).talker_decl,all) << "PUB TALKER_DECL holds every declared source after the adoption";
    for (unsigned i=1;i<MBX_N_IF;++i) {
        EXPECT_EQ(pub_of(model,i).talker_decl,all) << "PUB another interface keeps its own declarations";
    }
}

// A creation that fails declares nothing the block shows (srp_mbx.c,
// withdraw_declared; #665, comment 6095903333, R583-3-S1): declare_sources
// publishes TALKER_DECL only once every source joined. Each allocation of a
// link restart's re-creation is refused in turn, the sources' joins among
// them, so one refusal lands after the first source joined and before the
// last: no such re-creation writes TALKER_DECL nonzero, and it holds 0 after.
TEST_F(Srp, PubTalkerDeclIsNotPublishedByACreationThatFails) {
    settle();
    const unsigned last=MBX_N_IF-1u;
    const uint32_t reg=MBX_PUB_BASE+MBX_PUB_STRIDE*last+MBX_PUB_REG_TALKER_DECL;
    // the allocations a re-creation makes: what a successful one consumes, on the pass after the reset's
    calloc_before_failure=1000000;
    mbx_model_set_link(&model,last,false); ctrl_loop_service(&loop); ctrl_loop_service(&loop);
    const int made=1000000-calloc_before_failure;
    calloc_before_failure=-1;
    ASSERT_NE(adapter.ifs[last].msrp,nullptr);
    ASSERT_GT(made,static_cast<int>(CTRL_SRP_SOURCES)) << "PUB a re-creation allocates for each source's join";
    mbx_model_set_link(&model,last,true); settle();
    int failed=0;
    for (int failure=0;failure<made;++failure) {
        const unsigned refused=adapter.refused;
        pub_trace.clear(); mbx_host_trace(pub_writes,nullptr);
        calloc_before_failure=failure;
        mbx_model_set_link(&model,last,false); ctrl_loop_service(&loop); ctrl_loop_service(&loop);
        calloc_before_failure=-1;
        mbx_host_trace(nullptr,nullptr);
        ASSERT_GT(adapter.refused,refused) << "PUB the re-creation refused at allocation " << failure << " fails";
        ++failed;
        bool declared=false;
        for (const auto &w:pub_trace) declared=declared || (w.first==reg && w.second!=0u);
        EXPECT_FALSE(declared)
            << "PUB a re-creation refused at allocation " << failure << " publishes no Talker declaration";
        EXPECT_EQ(pub_of(model,last).talker_decl,0u)
            << "PUB TALKER_DECL holds 0 after a re-creation refused at allocation " << failure;
        settle();
        ASSERT_NE(adapter.ifs[last].msrp,nullptr);
        mbx_model_set_link(&model,last,true); settle();
    }
    EXPECT_EQ(failed,made) << "PUB every allocation of the re-creation was refused in turn";
    EXPECT_EQ(pub_of(model,last).talker_decl,(1u<<CTRL_SRP_SOURCES)-1u)
        << "PUB the retried creation declares every source";
}

// Every source of the compiled entity declares at startup (#895: the fixture's sources are valid from init): source 0,
// the one allocated, Talker Advertise, and each other one Talker Failed with code 2, unallocated (IEEE 802.1Q-2018
// 35.2.2.8.7, Table 35-6). Each is held by its own StreamID, so the 8x8 entity's eight unallocated sources are each
// held to New, New, JoinMt as the 1x1 entity's one is (#929).
TEST_F(Srp, StartupDeclaresTalkersDomainAndVlan) {
    settle();
    ASSERT_EQ(pool.refused,0u);
    EXPECT_EQ(adapter.transmitted,2u*MBX_N_IF);
    advance(400);
    EXPECT_EQ(adapter.transmitted,5u*MBX_N_IF);
    capture();
    const unsigned events[]={0,0,3};
    for(unsigned i=0;i<MBX_N_IF;++i) {
        unsigned count=0;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea && d.type==4) {
            ASSERT_LT(count,3u);
            EXPECT_EQ(d.event,events[count]); EXPECT_EQ(d.time_ms,10u*CTRL_LOOP_JOIN_CS*count); ++count;
            EXPECT_EQ(d.value,(std::vector<uint8_t>{6,3,0,2}));
        }
        EXPECT_EQ(count,3u) << "the Domain on interface " << i;
        unsigned talkers=0;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea && (d.type==1 || d.type==2)) ++talkers;
        EXPECT_EQ(talkers,3u*CTRL_SRP_SOURCES) << "each source's three Talker declarations and no other on interface "
                                               << i;
        for(unsigned n=0;n<CTRL_SRP_SOURCES;++n) {
            const unsigned type=sources[i][n].allocated ? 1u : 2u;
            const auto id=identity(i,n);
            count=0;
            for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea && (d.type==1 || d.type==2) &&
                                                  std::equal(d.value.begin(),d.value.begin()+8,id.begin())) {
                ASSERT_LT(count,3u) << "source " << n << " on interface " << i;
                EXPECT_EQ(d.type,type) << "source " << n << " on interface " << i;
                EXPECT_EQ(d.event,events[count]); EXPECT_EQ(d.time_ms,10u*CTRL_LOOP_JOIN_CS*count); ++count;
                EXPECT_EQ(wire_be16(d.value.data()+14),2u);
                EXPECT_EQ(wire_be16(d.value.data()+16),224u);
                EXPECT_EQ(wire_be16(d.value.data()+18),1u);
                EXPECT_EQ(d.value[20],0x60u);
                if(type==2) { EXPECT_EQ(d.value[33],2u) << "source " << n << "'s failure code"; }
            }
            EXPECT_EQ(count,3u) << "source " << n << " on interface " << i << " declares New, New, JoinMt";
        }
        count=0;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x88f5) {
            EXPECT_EQ(d.type,1u); EXPECT_EQ(d.event,3u); EXPECT_EQ(d.time_ms,10u*CTRL_LOOP_JOIN_CS*count);
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
    offer(frame(3,identity(),1,0));
    EXPECT_FALSE(adapter.ifs[0].listener_present[0]) << "Ignore occupies no registrar and supplies no demand";
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),1,2));
    EXPECT_TRUE(adapter.ifs[0].listener_present[0]) << "Listener Ready supplies declaration demand";
    EXPECT_CALL(licence,Change(0,0,false)); offer(frame(3,identity(),1,1));
    EXPECT_FALSE(adapter.ifs[0].active[0]);
    EXPECT_TRUE(adapter.ifs[0].listener_present[0]) << "Listener Asking Failed retains declaration demand";
    offer(frame(3,identity(),1,0));
    EXPECT_TRUE(adapter.ifs[0].listener_present[0]) << "Ignore leaves the registered Listener unchanged";
    offer(frame(3,identity(),1,1));
    EXPECT_TRUE(adapter.ifs[0].listener_present[0]);
    offer(frame(3,identity(),5,1));
    EXPECT_FALSE(adapter.ifs[0].listener_present[0]) << "last Listener leave removes declaration demand";
}
// The receive filter, the Listener indication and the registrar walk compare a
// StreamID (IEEE 802.1Q-2018 35.2.2.8.2) byte for byte (#665: srp_mbx.c's
// same): a Listener whose StreamID differs from a source's in its first byte
// alone, or in its last alone, is no source's, and the source's own is its.
TEST_F(Srp, AListenerIsASourcesOnlyForItsStreamIDByteForByte) {
    settle();
    for(unsigned at:{0u,7u}) {
        auto other=identity(0,0); other[at]^=0x40u;
        offer(frame(3,other,1,2));
        bool none=true;
        for(unsigned n=0;n<CTRL_SRP_SOURCES;++n) none=none&&!adapter.ifs[0].listener_present[n]&&!adapter.ifs[0].registered[n];
        EXPECT_TRUE(none)<<"a StreamID that differs from source 0's in byte "<<at<<" alone is no source's";
    }
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(0,0),1,2));
    EXPECT_TRUE(adapter.ifs[0].listener_present[0]&&adapter.ifs[0].registered[0])<<"source 0's own StreamID is its";
    EXPECT_CALL(licence,Change(0,0,false)); offer(frame(3,identity(0,0),5,2));
    EXPECT_FALSE(adapter.ifs[0].listener_present[0])<<"and its leave removes it";
}

// The interface reset clears listener_present with the registrar it destroys
// (#665): delivery reads no Listener the new participants have not walked.
TEST_F(Srp, InterfaceResetClearsListenerPresent) {
    settle();
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),1,2));
    ASSERT_TRUE(adapter.ifs[0].listener_present[0]) << "(Listener Ready supplies declaration demand)";
    EXPECT_CALL(licence,Change(0,0,false));
    mbx_model_set_link(&model,0,false);
    ctrl_loop_service(&loop);
    EXPECT_FALSE(adapter.ifs[0].listener_present[0]) << "the interface reset clears listener_present";
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
// THE DRAIN's charge of the record at the head of SRP's ring (#977, its ruling of 2026-11-23, item 4): the unit, and a
// registration's stated cost for each Talker value its Talker Messages' vectors carry, at most CTRL_SRP_SINKS a vector,
// read with the record left in the ring: nothing for an MVRP record, a Listener's or one past the PDU's EndMark, a
// Message's AttributeListLength bounding it, and past eight Messages the rest by its length.
TEST_F(Srp, TheDrainChargesARecordTheTalkersItsVectorsCanRegister) {
    settle();
    ASSERT_TRUE(loop.drain_charge != nullptr);
    const auto record=[](uint16_t ethertype,const std::vector<uint8_t> &messages) {
        std::vector<uint8_t> f(14); wire_put_be(f.data(),ethertype==0x22ea ? 0x0180c200000eull : 0x0180c2000021ull,6);
        wire_put_be(f.data()+6,0x020304059900ull,6); wire_put_be(f.data()+12,ethertype,2);
        f.push_back(0); f.insert(f.end(),messages.begin(),messages.end());
        if (f.size()<60u) f.resize(60u);
        return f;
    };
    // a Message of `type` with one vector a count, each value its FirstValue of `alen` octets, the Message's EndMark in
    // its AttributeListLength unless `list` states another
    const auto message=[](uint8_t type,uint8_t alen,const std::vector<unsigned> &counts,int list=-1) {
        std::vector<uint8_t> v;
        for (unsigned n:counts) {
            v.push_back(uint8_t(n>>8)); v.push_back(uint8_t(n)); v.insert(v.end(),alen,0x11);
            v.insert(v.end(),(n+2u)/3u,0);
        }
        v.push_back(0); v.push_back(0);
        const unsigned length=list<0 ? unsigned(v.size()) : unsigned(list);
        std::vector<uint8_t> m={type,alen,uint8_t(length>>8),uint8_t(length)};
        m.insert(m.end(),v.begin(),v.end());
        return m;
    };
    const auto cat=[](std::vector<std::vector<uint8_t>> parts) {
        std::vector<uint8_t> out;
        for (auto &p:parts) out.insert(out.end(),p.begin(),p.end());
        return out;
    };
    const unsigned u=CTRL_LOOP_SRP_UNIT_US;
    const unsigned r=CTRL_LOOP_SRP_REG_US;
    const unsigned s=CTRL_SRP_SINKS;
    const std::vector<uint8_t> end={0,0};
    std::vector<uint8_t> listeners;
    for (unsigned k=0;k<9u;++k) {
        const auto m=message(3,8,{1});
        listeners.insert(listeners.end(),m.begin(),m.end());
    }
    const auto past=cat({listeners,message(1,25,{1})});
    // the ninth Message's offset: the ProtocolVersion's and eight Listener Messages of 17 octets each
    const unsigned rest=(unsigned(record(0x22ea,past).size())-(15u+8u*17u))/(2u+25u+1u);
    const struct { const char *what; std::vector<uint8_t> f; unsigned charge; } cases[]={
        {"an MVRP record",record(0x88f5,message(1,2,{1})),u},
        {"a Listener's",record(0x22ea,cat({message(3,8,{1}),end})),u},
        {"a Talker Advertise's two values",record(0x22ea,cat({message(1,25,{2}),end})),u+r*(2u<s?2u:s)},
        {"a Talker Failed's values past the sinks",record(0x22ea,cat({message(2,34,{s+3u}),end})),u+r*s},
        {"both kinds' one each",record(0x22ea,cat({message(1,25,{1}),message(2,34,{1}),end})),u+2u*r},
        {"a Talker past the EndMark",record(0x22ea,cat({end,end,message(1,25,{1})})),u},
        {"a Message whose length passes the record",record(0x22ea,message(1,25,{1},2000)),u+r},
        {"a Message whose length ends at its last vector",record(0x22ea,cat({message(1,25,{1},2+25+1),end})),u+r},
        {"past eight Messages, by its length",record(0x22ea,past),u+r*s*rest},
    };
    // the shortest record the filter passes, its ProtocolVersion and no Message: the unit
    std::vector<uint8_t> shortest(15); wire_put_be(shortest.data(),0x0180c200000eull,6);
    wire_put_be(shortest.data()+12,0x22ea,2);
    ASSERT_TRUE(mbx_model_rx(&model,shortest.data(),shortest.size(),0));
    EXPECT_EQ(loop.drain_charge(&adapter),u) << "a record that ends at its ProtocolVersion";
    settle();
    for (const auto &c:cases) {
        mbx_model_advance_ms(&model,100); settle();   // the channel's bucket refilled
        ASSERT_TRUE(mbx_model_rx(&model,c.f.data(),c.f.size(),0)) << c.what;
        EXPECT_EQ(loop.drain_charge(&adapter),c.charge) << c.what;
        EXPECT_EQ(loop.drain_charge(&adapter),c.charge) << c.what << ", the record left in the ring";
        settle();
    }
    srp_mbx_destroy(&adapter);
    EXPECT_TRUE(loop.drain_charge == nullptr) << "destroy unbinds the charge";
}
// The byte compares (#977): a StreamID whose last byte is a bound sink's and another byte not is no Talker of that sink,
// in the receive filter, the indication and the walk; and a Talker of a bound StreamID at another destination touches
// its sink with no change of its declaration, which the filter's pass over the touched sinks leaves as it was.
TEST_F(Srp, ATalkerIsASinksOnlyForItsStreamIDByteForByte) {
    settle();
    const msrp_stream_id a{{2,1,2,3,4,5,6,7}};
    const msrp_stream_id b{{3,1,2,3,4,5,6,7}};
    const uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    const uint8_t other[]={0x91,0xe0,0xf0,0,0,10};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&a,da,2));
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,&b,da,2));
    // one Message of two vectors: b's Talker at another destination, then a's
    const auto vb=talker_value(b,other,2);
    const auto va=talker_value(a,da,2);
    std::vector<uint8_t> f(14); wire_put_be(f.data(),0x0180c200000eull,6);
    wire_put_be(f.data()+6,0x020304010203ull,6); wire_put_be(f.data()+12,0x22ea,2);
    f.insert(f.end(),{0,1,25,0,2*(2+25+1)+2});
    for (const auto *v:{&vb,&va}) {
        f.insert(f.end(),{0,1}); f.insert(f.end(),v->begin(),v->end()); f.push_back(1*36);
    }
    f.insert(f.end(),{0,0,0,0});
    offer(f); advance(200); capture();
    EXPECT_EQ(adapter.ifs[0].sinks[0].registered_kinds,2u) << "a's Talker registers for its own sink";
    EXPECT_EQ(adapter.ifs[0].sinks[1].registered_kinds,0u) << "b's at another destination registers for none";
    EXPECT_EQ(adapter.ifs[0].sinks[0].declared,2u) << "a's sink declares Ready";
    EXPECT_EQ(adapter.ifs[0].sinks[1].declared,0u) << "b's sink declares nothing";
}
// The sink index (#977, srp_mbx.c index_sinks): a and c share a lane, c bound first and a ahead of it in the lane once
// bound, so c is its lane's second; each StreamID's Talker is found for its own sinks alone by the indication, the
// receive filter, the kept count and the walk, a second binding of c is found beside the first, and a binding's end
// leaves its lane.
TEST_F(Srp, EveryBindingInASinkLaneTakesItsOwnStreamsTalkersAlone) {
    settle();
    const msrp_stream_id a{{2,1,2,3,4,5,6,0x05}};
    const msrp_stream_id c{{2,1,2,3,4,5,6,0x15}};
    const uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_EQ(a.bytes[7]%SRP_SINK_LANES,c.bytes[7]%SRP_SINK_LANES) << "a and c share a lane";
    auto failed=talker_value(c,da,2);
    failed.insert(failed.end(),{0x80,0,0x0e,0x0e,0x0e,0x0e,0x0e,0x01,1});
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,&c,da,2));
    settle(); advance(200);
    offer(frame(1,talker_value(c,da,2),1)); advance(200);
    EXPECT_EQ(adapter.ifs[0].sinks[1].registered_kinds,2u) << "c's Advertise registers for its sink";
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&a,da,2));
    settle(); advance(200);
    offer(frame(1,talker_value(a,da,2),1)); advance(200);
    EXPECT_EQ(adapter.kept_count[0],0u) << "the count before a's receive keeps no Talker of a bound StreamID";
    EXPECT_EQ(adapter.ifs[0].sinks[0].registered_kinds,2u) << "a's Advertise registers for its sink";
    EXPECT_EQ(adapter.ifs[0].sinks[1].registered_kinds,2u) << "the walk finds c's Advertise for its lane's second";
    offer(frame(2,failed,1)); advance(200);
    EXPECT_EQ(adapter.ifs[0].sinks[1].registered_kinds,1u) << "c's Failed replaces its Advertise at its lane's second";
    EXPECT_EQ(adapter.ifs[0].sinks[0].registered_kinds,2u) << "and a's sink keeps a's Advertise";
    EXPECT_EQ(adapter.kept_count[0],0u) << "the filter keeps no Talker of a bound StreamID";
    EXPECT_EQ(adapter.ifs[0].sinks[1].declared,1u) << "c's sink declares Asking Failed";
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&c,da,2));
    settle(); advance(200);
    offer(frame(1,talker_value(c,da,2),1)); advance(200);
    EXPECT_EQ(adapter.ifs[0].sinks[0].registered_kinds,2u) << "c's Advertise registers for both of its bindings";
    EXPECT_EQ(adapter.ifs[0].sinks[1].registered_kinds,2u) << "the second of them too";
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,nullptr,nullptr,0));
    settle(); advance(200);
    offer(frame(2,failed,1)); advance(200);
    EXPECT_EQ(adapter.ifs[0].sinks[0].registered_kinds,1u) << "c's Failed registers for the binding left";
    EXPECT_EQ(adapter.ifs[0].sinks[1].registered_kinds,0u) << "and for no ended binding";
}
// lwSRP's build options by shape (#977; srp_entity.py, LWSRP_OPTIONS, the shape header every unit force-includes): the
// one-interface shapes build the lookup buckets, no MAP work at one port, the lean validation pass, no leave timer
// event for a replaced Talker the rapid leave took to MT, no copy past what is used and no tx! an Applicant keeps,
// 8x8/1if alone the merged Message build; every other shape lwSRP's defaults.
#ifdef LWSRP_ONE_PORT_MAP
#define SRP_TEST_ONE_PORT LWSRP_ONE_PORT_MAP
#else
#define SRP_TEST_ONE_PORT 0
#endif
#ifdef LWSRP_LEAN_VALIDATE
#define SRP_TEST_LEAN LWSRP_LEAN_VALIDATE
#else
#define SRP_TEST_LEAN 0
#endif
#ifdef LWSRP_ATTR_BUCKETS
#define SRP_TEST_BUCKETS LWSRP_ATTR_BUCKETS
#else
#define SRP_TEST_BUCKETS 0u
#endif
#ifdef LWSRP_TX_MERGE
#define SRP_TEST_MERGE LWSRP_TX_MERGE
#else
#define SRP_TEST_MERGE 0
#endif
#ifdef LWSRP_RAPID_REPLACE
#define SRP_TEST_RAPID LWSRP_RAPID_REPLACE
#else
#define SRP_TEST_RAPID 0
#endif
#ifdef LWSRP_LEAN_COPY
#define SRP_TEST_COPY LWSRP_LEAN_COPY
#else
#define SRP_TEST_COPY 0
#endif
#ifdef LWSRP_LEAN_TX
#define SRP_TEST_LEAN_TX LWSRP_LEAN_TX
#else
#define SRP_TEST_LEAN_TX 0
#endif
TEST_F(Srp, TheShapeHeaderSetsLwsrpsEndStationOptions) {
    const bool one=MBX_N_IF==1u;
    const bool eight=CTRL_SRP_SINKS==9u;
    EXPECT_EQ(SRP_TEST_ONE_PORT,one ? 1 : 0) << "no MAP work at one port at a one-interface shape";
    EXPECT_EQ(SRP_TEST_LEAN,one ? 1 : 0) << "the lean validation pass at a one-interface shape";
    EXPECT_EQ(SRP_TEST_BUCKETS,one ? 16u : 0u) << "the lookup buckets at a one-interface shape";
    EXPECT_EQ(SRP_TEST_MERGE,one && eight ? 1 : 0) << "the merged Message build at 8x8/1if alone";
    EXPECT_EQ(SRP_TEST_RAPID,one ? 1 : 0) << "no leave timer event for a rapid replacement at a one-interface shape";
    EXPECT_EQ(SRP_TEST_COPY,one ? 1 : 0) << "no copy past what is used at a one-interface shape";
    EXPECT_EQ(SRP_TEST_LEAN_TX,one ? 1 : 0) << "no tx! an Applicant keeps at a one-interface shape";
}
// THE TRANSMIT's re-declarations in a slice of their own (#977, its ruling of 2026-11-23, item 3; CTRL_LOOP_DECLARE_ALONE
// at 8x8/1if): a call whose declarations re-declared a Listener ends after them and the next call builds the MRPDU, no
// SRP record taken between; at every other shape one call declares and builds.
TEST_F(Srp, ARedeclarationBuildsItsMrpduInTheNextCallWhereTheShapeSaysSo) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
    settle(); advance(400);
    const auto f=frame(1,talker_value(sid,da,2),0);
    ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),0));
    for(unsigned n=0;n<20u && loop.drain_taken==0u;++n) ctrl_loop_service(&loop);
    ASSERT_NE(loop.drain_taken,0u) << "a pass took the registration";
    ASSERT_NE(adapter.tx_due,0u) << "its Listener declaration is owed THE TRANSMIT";
    const auto sent=adapter.transmitted;
    loop.transmit(loop.transmit_ctx,CTRL_LOOP_BUILD_MOST);
    EXPECT_NE(adapter.ifs[0].sinks[0].declared,0u) << "the call declares the Listener";
    if(CTRL_LOOP_DECLARE_ALONE) {
        EXPECT_EQ(adapter.transmitted,sent) << "the call that re-declared builds nothing";
        EXPECT_TRUE(adapter.declared_alone) << "its build owed to the next call";
        // a Listener of no source here, posted before the mark a pass's events read (THE DRAIN's order)
        const auto r=frame(3,{9,9,9,9,9,9,9,9},0,2);
        ASSERT_TRUE(mbx_model_rx(&model,r.data(),r.size(),0));
        loop.rx_order=mbx_rx_mark(MBX_CH_SRP);
        EXPECT_FALSE(loop.rx[MBX_CH_SRP].ready(&adapter)) << "no SRP record is taken before the build";
        loop.transmit(loop.transmit_ctx,CTRL_LOOP_BUILD_MOST);
        EXPECT_GT(adapter.transmitted,sent) << "the next call builds the MRPDU";
        EXPECT_FALSE(adapter.declared_alone);
        EXPECT_TRUE(loop.rx[MBX_CH_SRP].ready(&adapter)) << "and records are taken again";
    } else {
        EXPECT_GT(adapter.transmitted,sent) << "the call that declares builds the MRPDU";
        EXPECT_FALSE(adapter.declared_alone);
    }
    settle();
}
TEST_F(Srp, RefusedMailboxRetainsOwedFrameAndDefersInput) {
    mbx_model_tx_pause(&model,true);
    std::vector<uint8_t> filler(60); wire_put_be(filler.data(),0x0180c200000eull,6);
    wire_put_be(filler.data()+12,0x22ea,2);
    while(mbx_tx_send(MBX_CH_SRP,0,filler.data(),filler.size())==MBX_STATUS_OK) {}
    // THE TRANSMIT builds in the first pass that takes at most one event (ctrl_loop.h): at two interfaces the
    // first pass takes both LINK records; a slice holds CTRL_LOOP_BUILD_MOST of an interface's two MRPDUs, so its
    // startup build takes 2 / CTRL_LOOP_BUILD_MOST passes (THE TIERS)
    for(unsigned n=0;n<4u*2u/CTRL_LOOP_BUILD_MOST && !adapter.owed_len;++n) ctrl_loop_service(&loop);
    ASSERT_GT(adapter.owed_len,0u);
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
        loop.transmit(loop.transmit_ctx,CTRL_LOOP_BUILD_MOST);
        loop.ticks[loop.n_ticks-1]();
        EXPECT_FALSE(srp_mbx_init(&adapter,&config));
        EXPECT_EQ(adapter.reentries,before+10);
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
    ASSERT_TRUE(ctrl_loop_set_transmit(&loop,[](void*,unsigned){},[](void*){return false;},nullptr));
    EXPECT_FALSE(srp_mbx_attach(&adapter,&loop))<<"a loop whose THE TRANSMIT client is bound is refused";
    EXPECT_EQ(loop.n_polls,0u);
    ctrl_loop_init(&loop);
    ctrl_loop_add_tick(&loop,[](){}); ctrl_loop_add_poll(&loop,[](void*){return false;},nullptr);
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop)); srp_mbx_destroy(&adapter);
    EXPECT_EQ(loop.n_ticks,1u); EXPECT_EQ(loop.n_polls,1u);
    EXPECT_EQ(loop.transmit,nullptr)<<"destroy detaches THE TRANSMIT's client";
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
    EXPECT_EQ(ctrl_pool_in_use(&pool),before)<<"a Listener of no source takes no block";
    // a Talker of a StreamID no binding holds is kept for a binding made later, one block (#969, keep_talker)
    std::vector<uint8_t> unknown(25,0); unknown[7]=7;
    offer(frame(1,unknown,0)); EXPECT_EQ(ctrl_pool_in_use(&pool),before+1u)<<"a Talker no binding holds is kept";
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
    adapter.join_left[0]=0;
    ctrl_loop_service(&loop);
    EXPECT_GT(adapter.refused,0u); EXPECT_EQ(adapter.ifs[0].domain.vid,2u);
    EXPECT_TRUE(adapter.ifs[0].domain_owed);
    EXPECT_NE(adapter.join_left[0],0u)<<"a refused declaration is tried again when the join count ends";
    ctrl_pool_free(&pool,held.back()); held.pop_back(); advance(200); // one JoinTime
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
    ctrl_pool_free(&pool,held.back()); held.pop_back(); advance(200); // one JoinTime
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

// Two adapters share one pool, two of the compiled entity's SRP pools (srp_mbx.h, from its shape), so both are made at
// every shape and the second's attachment is what the test holds (#929: a 1x1-sized pool refused the second
// srp_mbx_init at the 8x8 entity with two interfaces).
TEST_F(Srp, OneLoopOwnsTheGlobalCentisecondDispatch) {
    srp_mbx_destroy(&adapter);
    alignas(std::max_align_t) static uint8_t storage[2u*SRP_POOL_ARENA_BYTES];
    ctrl_pool shared{};
    ctrl_pool_class cls[SRP_POOL_N_CLASSES];
    for(unsigned k=0;k<SRP_POOL_N_CLASSES;++k) {
        cls[k]={srp_pool_classes[k].block_bytes,static_cast<uint16_t>(2u*srp_pool_classes[k].blocks)};
    }
    ASSERT_TRUE(ctrl_pool_init(&shared,storage,sizeof(storage),cls,SRP_POOL_N_CLASSES)); shlan_port_bind_pool(&shared);
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
    // what is declared after the first unbind, whatever the JoinTime's grid (CTRL_LOOP_JOIN_CS)
    const unsigned unbound=model.now_ms;
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0)); advance(200); capture();
    for(const auto &d:declarations) if(d.time_ms>unbound && d.ethertype==0x22ea && d.type==3) {
        EXPECT_NE(d.event,5u)<<"one remaining binding retains the Listener";
    }
    EXPECT_TRUE(adapter.ifs[0].sinks[1].vlan_sent);
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,nullptr,nullptr,0)); advance(200); capture();
    bool vlan_left=false; bool listener_left=false;
    for(const auto &d:declarations) if(d.event==5 && d.time_ms>unbound) {
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
        ctrl_loop_service(&loop); ctrl_loop_service(&loop);
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
// A link change rebuilds its interface a poll later, 850 us of polls at 8x8/2if, which THE DRAIN's limit does not count:
// records stop at their cap until it is built (ctrl_loop.h).
TEST_F(Srp, ALinkResetHoldsRecordsToTheirCapUntilItsInterfaceIsBuilt) {
    ctrl_loop_service(&loop);
    EXPECT_FALSE(loop.rx_held)<<"no rebuild owed";
    model.link_up[0]=false;
    for(unsigned n=0;n<4u&&!loop.rx_held;++n) ctrl_loop_service(&loop); // a pass given whole may come first
    EXPECT_TRUE(loop.rx_held)<<"a reset owes its interface's rebuild";
    for(unsigned n=0;n<8u&&loop.rx_held;++n) ctrl_loop_service(&loop);
    EXPECT_FALSE(loop.rx_held)<<"and the rebuild ends the hold";
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
        // The DOWN level is observed while its record is held, as a full event
        // ring holds it: the writes the level's reset makes, the publication
        // block's included, must not post it. The level returns to the last
        // posted UP, so no new LINK record is owed.
        mbx_model_evt_pause(&model,true);
        model.link_up[i]=false; ctrl_loop_service(&loop);
        ASSERT_FALSE(adapter.ifs[i].link);
        auto ready=frame(3,identity(i),1,2);
        for(unsigned n=0;n<CTRL_LOOP_RX_PER_PASS+1;++n)
            ASSERT_TRUE(mbx_model_rx(&model,ready.data(),ready.size(),i));
        model.link_up[i]=true;
        ASSERT_TRUE(model.posted_up[i])<<"the DOWN record stayed held";
        mbx_model_evt_pause(&model,false);
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
    // the old link's reset discards the owed Domain: once it is taken neither owed nor adopted, whatever build ran
    // before it, a build resumed across slices included (#894)
    mbx_model_set_link(&model,0,false); settle();
    EXPECT_TRUE(!adapter.ifs[0].domain_owed && adapter.ifs[0].domain.vid == 2u)
        <<"old link's refused Domain must be discarded at its reset";
    for(void *p:held) ctrl_pool_free(&pool,p);
    mbx_model_set_link(&model,0,true); settle(); advance(400);
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


// #665: snapshot walks the registrar only after it, an indication or a binding
// changed what the walk copies, and otherwise holds what a walk would copy. A
// walk of the registrar here, with registrations()'s rules, is the reference.
struct Walked {
    std::vector<int> registered;
    std::vector<int> present;
    std::vector<int> desired;
    std::vector<int> kinds;
    std::vector<int> streams;
    bool operator==(const Walked &) const = default;
};
Walked walk(const srp_interface &i) {
    Walked w{std::vector<int>(CTRL_SRP_SOURCES),std::vector<int>(CTRL_SRP_SOURCES),
             std::vector<int>(CTRL_SRP_SINKS),std::vector<int>(CTRL_SRP_SINKS),std::vector<int>(CTRL_SRP_SINKS)};
    struct Ctx { const srp_interface *i; Walked *w; } ctx{&i,&w};
    mrp_attr_visit(i.msrp,0,[](void *p,const mrp_attr_status *s) {
        auto &c=*static_cast<Ctx*>(p);
        if(s->reg==MRP_REG_STATE_MT) return;
        const auto *v=static_cast<const uint8_t*>(s->attr_val);
        if(s->attr_type==MSRP_ATTR_TYPE_LISTENER) {
            for(unsigned n=0;n<CTRL_SRP_SOURCES;++n) if(!std::memcmp(c.i->sources[n].value.stream_id.bytes,v,8)) {
                c.w->present[n]=1; c.w->registered[n]=v[8]==2 || v[8]==3;
            }
        } else if(s->attr_type==MSRP_ATTR_TYPE_TALKER_ADV || s->attr_type==MSRP_ATTR_TYPE_TALKER_FAILED) {
            const auto *t=static_cast<const msrp_talker_adv*>(s->attr_val);
            for(unsigned k=0;k<CTRL_SRP_SINKS;++k) {
                const auto &sink=c.i->sinks[k];
                const int kind=s->attr_type==MSRP_ATTR_TYPE_TALKER_FAILED ? 1 : 2;
                // the StreamID's kinds whatever their destination and VID, which a final unbinding reads (#925)
                if(sink.bound && !std::memcmp(sink.stream_id.bytes,t->stream_id.bytes,8)) c.w->streams[k]|=kind;
                if(sink.bound && !std::memcmp(sink.stream_id.bytes,t->stream_id.bytes,8) &&
                   !std::memcmp(sink.dest_mac,t->dest_mac,6) && sink.vid==t->vlan_id)
                    c.w->kinds[k]|=kind;
            }
        }
    },&ctx);
    for(unsigned k=0;k<CTRL_SRP_SINKS;++k) {
        // both kinds registered: the one registered latest, the ordering only indications carry (#925)
        const int latest=i.sinks[k].latest_kind;
        const int kinds=(w.kinds[k]&latest) ? latest : w.kinds[k];
        w.desired[k]=(kinds&1) ? 1 : (kinds&2);
    }
    return w;
}
Walked held(const srp_interface &i) {
    Walked w;
    for(unsigned n=0;n<CTRL_SRP_SOURCES;++n) { w.registered.push_back(i.registered[n]); w.present.push_back(i.listener_present[n]); }
    for(unsigned k=0;k<CTRL_SRP_SINKS;++k) {
        w.desired.push_back(i.sinks[k].desired); w.kinds.push_back(i.sinks[k].registered_kinds);
        w.streams.push_back(i.sinks[k].stream_kinds);
    }
    return w;
}
void expect_held(const srp_mbx &adapter, const char *step) {
    for(unsigned i=0;i<MBX_N_IF;++i) {
        if(!adapter.ifs[i].msrp) continue;
        EXPECT_FALSE(adapter.ifs[i].stale)<<step<<": a settled loop leaves no walk owed";
        EXPECT_FALSE(adapter.ifs[i].reclaim)<<step<<": a settled loop leaves nothing to reclaim";
        EXPECT_TRUE(held(adapter.ifs[i])==walk(adapter.ifs[i]))<<step<<": interface "<<i<<" holds what a walk copies";
    }
}

TEST_F(Srp, HeldRegistrationsAreWhatAWalkCopiesAfterEveryStep) {
    settle(); expect_held(adapter,"startup");
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const uint8_t da[]={
        0x91,0xe0,0xf0,0,0,9
    };
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2)); settle(); expect_held(adapter,"bind");
    EXPECT_CALL(licence,Change(0,0,true));
    offer(frame(3,identity(),1,2)); expect_held(adapter,"Listener Ready");
    offer(frame(3,identity(),1,2)); expect_held(adapter,"the same Listener Ready");
    offer(frame(1,talker_value(sid,da,2),1)); expect_held(adapter,"Talker Advertise");
    auto failed=talker_value(sid,da,2); failed.resize(34); failed[33]=1;
    offer(frame(2,failed,1)); expect_held(adapter,"Talker Failed");
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,&sid,da,2)); settle(); expect_held(adapter,"a second binding of a registered Talker");
    EXPECT_CALL(licence,Change(0,0,false));
    offer(frame(3,identity(),1,1)); expect_held(adapter,"Listener Asking Failed, the value changed in place");
    offer(frame(3,identity(),5,1)); expect_held(adapter,"Listener leave");
    advance(5100); expect_held(adapter,"the leave timers expired");
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0)); settle(); expect_held(adapter,"unbind");
    mbx_model_set_link(&model,0,false); settle(); expect_held(adapter,"link down");
    mbx_model_set_link(&model,0,true); settle(); expect_held(adapter,"link up");
}

// #930: a Listener's change is copied where lwSRP reports it, so its record walks no registrar; a Talker's
// registration, which the walk copies to the sinks, is copied once, after its record.
TEST_F(Srp, ARecordThatChangesNoRegistrationCostsNoWalk) {
    settle();
    // No poll runs between these records (receive_before_poll), so no licence changes.
    const uint32_t first=adapter.walks;
    receive_before_poll(frame(3,identity(),1,2));
    EXPECT_EQ(adapter.walks,first)<<"a new Listener registration is copied with no walk";
    EXPECT_TRUE(adapter.ifs[0].registered[0]); EXPECT_TRUE(adapter.ifs[0].listener_present[0]);
    for(unsigned n=0;n<4;++n) {
        const uint32_t before=adapter.walks;
        receive_before_poll(frame(3,identity(),1,2));
        EXPECT_EQ(adapter.walks,before)<<"a record that changes nothing walks no registrar";
    }
    EXPECT_TRUE(adapter.ifs[0].registered[0]);
    uint32_t before=adapter.walks;
    receive_before_poll(frame(3,identity(),1,1));
    EXPECT_EQ(adapter.walks,before)<<"a Listener's declaration changed in place is copied with no walk";
    EXPECT_FALSE(adapter.ifs[0].registered[0]); EXPECT_TRUE(adapter.ifs[0].listener_present[0]);
    settle(); expect_held(adapter,"settled");
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const std::array<uint8_t,6> da{0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da.data(),2)); settle();
    before=adapter.walks;
    receive_before_poll(frame(1,talker_value(sid,da.data(),2),1));
    EXPECT_EQ(adapter.walks,before+1u)<<"a new Talker registration is copied once, after its record";
    settle(); expect_held(adapter,"a Talker registered");
}

// A Listener declaration of a StreamID no source talks shares its attribute with no registration the walk copies
// (#977, srp_mbx.c prepare_declarations): THE TRANSMIT's re-declaration after a registration owes no walk.
TEST_F(Srp, ADeclarationOfAStreamNoSourceTalksOwesNoWalk) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2)); settle(); advance(400);
    receive_before_poll(frame(1,talker_value(sid,da,2),1));
    ASSERT_EQ(adapter.ifs[0].sinks[0].desired,2u) << "the registration asks for a Ready declaration";
    const uint32_t before=adapter.walks;
    settle(); advance(400);
    EXPECT_EQ(adapter.ifs[0].sinks[0].declared,2u) << "THE TRANSMIT declared it";
    EXPECT_EQ(adapter.walks,before) << "a declaration of a StreamID no source talks owes no walk";
    expect_held(adapter,"declared Ready");
}

// A sink bound to the entity's own stream shares each attribute with a source:
// the adapter's own declarations then rewrite a value a registration holds,
// with no Registrar change and no indication.
TEST_F(Srp, OwnDeclarationsThatRewriteARegisteredValueAreCopied) {
    settle(); advance(400);
    const auto own=identity();
    msrp_stream_id sid; std::copy(own.begin(),own.end(),sid.bytes);
    const uint8_t *da=sources[0][0].value.dest_mac;
    offer(frame(3,own,1,1)); expect_held(adapter,"a remote Listener Asking Failed for the own stream");
    EXPECT_FALSE(adapter.ifs[0].registered[0]);
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2)); settle(); expect_held(adapter,"bound to the own stream");
    EXPECT_CALL(licence,Change(0,0,true));
    offer(frame(1,talker_value(sid,da,2),1)); advance(400);
    expect_held(adapter,"the own Listener Ready declaration rewrote the registered Listener");
    EXPECT_TRUE(adapter.ifs[0].registered[0]);
    EXPECT_EQ(adapter.ifs[0].sinks[0].registered_kinds,2u);
    EXPECT_CALL(licence,Change(0,0,false));
    offer(frame(4,{6,3,0,5},1)); advance(400);
    expect_held(adapter,"the adopted Domain's Talker declaration rewrote the registered Talker");
    EXPECT_EQ(adapter.ifs[0].sinks[0].registered_kinds,0u);
}

TEST_F(Srp, ReclaimWaitsWhileItsParticipantHoldsTheOwedFrame) {
    settle(); advance(400); mbx_model_tx_pause(&model,true);
    std::vector<uint8_t> filler(60); wire_put_be(filler.data(),0x0180c200000eull,6); wire_put_be(filler.data()+12,0x22ea,2);
    while(mbx_tx_send(MBX_CH_SRP,0,filler.data(),filler.size())==MBX_STATUS_OK) {}
    mbx_model_advance_ms(&model,600); for(unsigned n=0;n<100;++n) ctrl_loop_service(&loop);
    ASSERT_GT(adapter.owed_len,0u);
    const unsigned waiting=adapter.owed_if;
    adapter.ifs[waiting].reclaim=true;     // as a transition during the hold leaves it
    for(unsigned n=0;n<10;++n) ctrl_loop_service(&loop);
    ASSERT_GT(adapter.owed_len,0u);
    EXPECT_TRUE(adapter.ifs[waiting].reclaim)<<"a reclaim lwSRP refused for the held frame is owed after it";
    mbx_model_tx_pause(&model,false); settle();
    EXPECT_EQ(adapter.owed_len,0u); expect_held(adapter,"after the owed frame");
}

// A record SRP's receive takes and drops (shorter than an MRPDU header): the
// pass that takes it took a record and changed no registration.
std::vector<uint8_t> runt() {
    std::vector<uint8_t> f(16);
    wire_put_be(f.data(),0x0180c200000eull,6);
    wire_put_be(f.data()+6,0x020304010203ull,6);
    wire_put_be(f.data()+12,0x22ea,2);
    return f;
}

// THE TRANSMIT (ctrl_loop.h, #665): the poll builds no MRPDU, and an MRPDU a timer, a record or a declaration makes
// owed takes a pass of its own, in place of any input: both participants of the first interface that owes one. The
// join timer's end is the adapter's own count (tick), which restarts on what a build sent.
TEST_F(Srp, AnOwedMrpduTakesAPassOfItsOwn) {
    settle();
    EXPECT_EQ(adapter.tx_due,0u)<<"a settled adapter owes no MRPDU";
    // every participant now owes an MRPDU (Srp.PollTermsAreMeasuredSeparatelyThroughRealCallbacks)
    for (unsigned n=0;n+1u<CTRL_LOOP_JOIN_CS;++n) loop.ticks[0]();
    EXPECT_EQ(adapter.tx_due,0u)<<"no centisecond before a join timer's end owes one";
    loop.ticks[0]();
    EXPECT_NE(adapter.tx_due,0u)<<"the centisecond that ends a join timer owes its interface's MRPDUs";
    const uint32_t unbuilt=adapter.transmitted;
    EXPECT_TRUE(loop.polls[0].fn(loop.polls[0].ctx))<<"an owed MRPDU is reported owed";
    EXPECT_EQ(adapter.transmitted,unbuilt)<<"and no poll builds it";
    const auto f=runt();
    ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),0));
    const uint32_t sent=adapter.transmitted;
    const uint32_t rx=loop.stats.rx_records;
    const uint32_t passes=loop.stats.transmit_passes;
    EXPECT_NE(ctrl_loop_service(&loop),0u);
    EXPECT_EQ(loop.stats.transmit_passes,passes+1u)<<"the pass goes to the build";
    EXPECT_EQ(loop.stats.rx_records,rx)<<"it takes no record";
    EXPECT_EQ(adapter.transmitted,sent+CTRL_LOOP_BUILD_MOST)
        <<"and sends the MRPDUs its slice holds of the first interface that owes, both where it holds them";
    settle();
    EXPECT_EQ(adapter.transmitted,sent+2u*MBX_N_IF)<<"the next such pass the next interface's";
    EXPECT_EQ(loop.stats.rx_records,rx+1u)<<"and the pass after them takes the record";
    EXPECT_EQ(adapter.tx_due,0u)<<"nothing is owed once every interface has built";
    // a binding owes nothing itself: the walk that finds its declaration does, and an unbinding that withdraws one
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,&sid,da,2));
    std::vector<uint8_t> talker(25); std::copy(sid.bytes,sid.bytes+8,talker.begin());
    std::copy(da,da+6,talker.begin()+8); wire_put_be(talker.data()+14,2,2);
    wire_put_be(talker.data()+16,224,2); wire_put_be(talker.data()+18,1,2); talker[20]=0x60;
    offer(frame(1,talker,0)); advance(200);
    settle();
    adapter.tx_due=0u;
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
    EXPECT_EQ(adapter.tx_due,0u)<<"a binding owes no MRPDU itself";
    static_cast<void>(loop.polls[0].fn(loop.polls[0].ctx));
    EXPECT_NE(adapter.tx_due,0u)<<"the walk that finds its declaration owes the MRPDU that declares it";
    settle();
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0));
    adapter.tx_due=0u;
    ASSERT_NE(adapter.ifs[0].sinks[1].declared,0u);
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,nullptr,nullptr,0));
    EXPECT_NE(adapter.tx_due,0u)<<"an unbinding that withdraws a declaration owes the MRPDU that sends it";
    settle();
}

namespace {
ctrl_transmit_fn whole_transmit;
unsigned slice_most;   // the MRPDUs the test's slices hold
unsigned slice_calls, slice_frames, slice_widest;
mbx_model *slice_model;
void sliced_transmit(void *ctx, unsigned) {
    const unsigned before = slice_model->tx_sent;
    whole_transmit(ctx, slice_most);
    ++slice_calls;
    slice_frames = slice_model->tx_sent - before;
    slice_widest = slice_frames > slice_widest ? slice_frames : slice_widest;
}
ctrl_poll_fn gap_poll;   // SRP's poll, run in each gap a slice leaves between an adoption's MSRP and its MVRP
unsigned gap_slices;     // the slices that ended with a resume owed and interface 0's VLAN unsent
bool gap_licensed;       // whether interface 0's Talker was licensed in such a gap, after its poll
void gapped_transmit(void *ctx, unsigned) {
    whole_transmit(ctx, 1u);
    const auto *m = static_cast<const srp_mbx *>(ctx);
    if (m->tx_resume != 0u && !m->ifs[0].vlan_sent) {
        ++gap_slices;
        static_cast<void>(gap_poll(ctx));   // an ordinary pass's poll between the two slices
        gap_licensed = gap_licensed || m->ifs[0].active[0];
    }
}
}

// THE TIERS (#894): where a slice holds one MRPDU (CTRL_LOOP_BUILD_MOST 1, both points), a Domain that moves the VID,
// adopted in a build's first slice, goes out in its MSRP MRPDU and the MVRP MRPDU follows in the next slice, an
// ordinary pass's poll between the two; the Talker's licence waits for the MVRP commit (vlan_sent; Milan v1.2 4.3.2).
TEST_F(Srp, ASlicedAdoptionLicensesItsTalkerOnlyOnceItsVlanIsSent) {
    whole_transmit = loop.transmit;
    loop.transmit = gapped_transmit;
    gap_poll = nullptr;
    for (unsigned k = 0; k < loop.n_polls; ++k) {
        if (loop.polls[k].ctx == &adapter) {
            gap_poll = loop.polls[k].fn;
        }
    }
    ASSERT_NE(gap_poll, nullptr);
    gap_slices = 0u;
    gap_licensed = false;
    settle();
    EXPECT_CALL(licence, Change(0, 0, true));
    offer(frame(3, identity(0), 1, 2), 0);
    ASSERT_TRUE(::testing::Mock::VerifyAndClearExpectations(&licence));
    unsigned grants = 0u;
    EXPECT_CALL(licence, Change(::testing::_, ::testing::_, false)).Times(::testing::AnyNumber());
    EXPECT_CALL(licence, Change(::testing::_, ::testing::_, true))
        .WillRepeatedly([&](unsigned, unsigned, bool) {
            ++grants;
            EXPECT_TRUE(adapter.ifs[0].vlan_sent) << "the Talker's licence waits for the MVRP commit";
        });
    offer(frame(4, {6, 4, 0, 3}, 0));
    advance(400);
    EXPECT_EQ(adapter.ifs[0].domain.vid, 3u) << "(the Domain was adopted)";
    EXPECT_GE(gap_slices, 1u) << "a slice ends between the adoption's MSRP and its MVRP, a poll run there";
    EXPECT_FALSE(gap_licensed) << "no Talker is licensed there while its VLAN is unsent";
    EXPECT_EQ(grants, 1u) << "and the Talker is licensed again once its VLAN is sent";
    ::testing::Mock::VerifyAndClearExpectations(&licence);
    EXPECT_CALL(licence, Change(::testing::_, ::testing::_, ::testing::_)).Times(::testing::AnyNumber());
    loop.transmit = whole_transmit;
}

// THE TRANSMIT's build resumes across slices (THE TIERS; #665, the decision of 2026-11-09, item 2): the same SRP
// frames, in the same order, as the build made whole, each call making at most the MRPDUs its slice holds; a reset
// between two slices leaves the new participants a whole build.
TEST_F(Srp, ABuildResumedAcrossSlicesSendsTheFramesOfTheBuildMadeWhole) {
    const auto frames = [&](unsigned most) {
        TearDown();
        SetUp();
        whole_transmit = loop.transmit;
        slice_model = &model;
        slice_most = most;
        slice_calls = slice_widest = 0u;
        loop.transmit = sliced_transmit;
        settle();
        msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
        EXPECT_TRUE(srp_mbx_bind(&adapter,0,1,&sid,da,2));
        offer(frame(4,{6,5,0,3},0));   // a Domain to adopt
        for (unsigned n=0;n<20u;++n) loop.ticks[0]();
        settle();
        std::vector<std::vector<uint8_t>> out;
        for (unsigned k=0;k<model.tx_sent;++k) {
            const auto *f=mbx_model_tx_frame(&model,k);
            out.emplace_back(f->bytes,f->bytes+f->len);
        }
        loop.transmit = whole_transmit;
        return std::make_pair(out, slice_calls);
    };
    const auto whole = frames(2u);
    const auto sliced = frames(1u);
    EXPECT_GT(whole.first.size(),2u*MBX_N_IF)<<"(the scenario builds every participant's MRPDUs)";
    EXPECT_LE(slice_widest,1u)<<"a slice that holds one MRPDU makes one";
    EXPECT_GT(sliced.second,whole.second)<<"so the build takes more slices";
    EXPECT_EQ(sliced.first,whole.first)<<"a build resumed across slices sends the frames of the build made whole";
    // a reset between two slices: the interface's new participants build whole, MSRP's first, not from where the
    // build it was resuming stopped
    TearDown();
    SetUp();
    whole_transmit = loop.transmit;
    slice_model = &model;
    slice_most = 1u;
    loop.transmit = sliced_transmit;
    settle();
    adapter.tx_due = 1u;
    loop.transmit(loop.transmit_ctx, 1u);
    ASSERT_NE(adapter.tx_resume,0u)<<"(a build resuming at its next participant)";
    mbx_model_set_link(&model,0,false);
    mbx_model_set_link(&model,0,true);
    // the reset and the rebuild before THE TRANSMIT's next slice (one held off, as by tier 1's records)
    loop.transmit = [](void*,unsigned){};
    for (unsigned n=0;n<64u;++n) static_cast<void>(ctrl_loop_service(&loop));
    ASSERT_NE(adapter.ifs[0].msrp,nullptr)<<"(the interface rebuilt)";
    loop.transmit = sliced_transmit;
    adapter.tx_due |= 1u;
    const unsigned before = model.tx_sent;
    settle();
    unsigned first = 0u;
    for (unsigned k=before;k<model.tx_sent && first==0u;++k) {
        const auto *f=mbx_model_tx_frame(&model,k);
        if (f->interface==0u) first=wire_be16(f->bytes+12);
    }
    EXPECT_EQ(first,0x22eau)<<"a reset ends the build it was resuming: its new participants build whole, MSRP first";
    loop.transmit = whole_transmit;
}

// A build that stops at a slice boundary stays owed until its next slice, THE TRANSMIT's due and the poll's report
// both, and what comes due between its two slices, a join timer's end among the centiseconds dispatched there, or a
// declaration another pass made owed, is owed again once the build ends, as it is after a build made whole: the pause
// takes its interface's due, so a due set again before the build ends is new (THE TIERS; #956). A build with nothing
// due between its slices ends owing nothing, what its own sends moved included, and one whose second slice's frame the
// ring refuses leaves its interface due, as a build made whole does (A3).
TEST_F(Srp, ABuildPausedBetweenSlicesStaysOwedAndKeepsWhatCameDue) {
    ctrl_poll_fn poll = nullptr;
    for (unsigned k = 0; k < loop.n_polls; ++k) {
        if (loop.polls[k].ctx == &adapter) {
            poll = loop.polls[k].fn;
        }
    }
    ASSERT_NE(poll, nullptr);
    // the start, served as far as it goes, so each check below is reached whatever the start left
    const auto serve = [&] {
        for (unsigned n = 0; n < 1000u && ctrl_loop_service(&loop) != 0u; ++n) {
        }
    };
    serve();
    EXPECT_EQ(adapter.tx_owed, 0u) << "(the start settles owing THE TRANSMIT nothing)";
    for (const bool again : {false, true}) {
        while (adapter.tx_resume != 0u) {
            loop.transmit(loop.transmit_ctx, 1u);
        }
        adapter.tx_due = 1u;
        loop.transmit(loop.transmit_ctx, 1u);
        ASSERT_NE(adapter.tx_resume, 0u) << "(a build resuming at its next participant)";
        // nothing else due: the paused build alone
        const uint8_t due = adapter.tx_due;
        adapter.tx_due = 0u;
        EXPECT_TRUE(loop.transmit_aged(loop.transmit_ctx)) << "a build resuming in the next slice is THE TRANSMIT's due";
        EXPECT_TRUE(poll(&adapter)) << "the poll reports a build resuming in the next slice owed";
        adapter.tx_due = (uint8_t)(adapter.tx_due | due);
        if (again) {
            adapter.tx_due |= 1u;   // as a join timer's end dispatched between the two slices owes it (tick)
        }
        loop.transmit(loop.transmit_ctx, 1u);
        ASSERT_EQ(adapter.tx_resume, 0u) << "(the build ended)";
        if (again) {
            EXPECT_NE(adapter.tx_due & 1u, 0u) << "a due set between a build's slices is owed once the build ends";
        } else {
            EXPECT_EQ(adapter.tx_due & 1u, 0u) << "a build with nothing due between its slices ends owing nothing";
        }
        serve();
    }
    // the ring refuses the second slice's frame, once a periodic MRPDU of each participant is owed: the frame stays the
    // poll's and the interface stays due (A3), its pause's due taken or not
    while (adapter.tx_resume != 0u) {
        loop.transmit(loop.transmit_ctx, 1u);
    }
    for (unsigned n = 0; n < 120u; ++n) {
        loop.ticks[0]();
    }
    adapter.tx_due = 1u;
    loop.transmit(loop.transmit_ctx, 1u);
    ASSERT_NE(adapter.tx_resume, 0u) << "(a build resuming at its next participant)";
    mbx_model_tx_pause(&model, true);
    std::vector<uint8_t> filler(60);
    wire_put_be(filler.data(), 0x0180c200000eull, 6);
    wire_put_be(filler.data() + 12, 0x22ea, 2);
    while (mbx_tx_send(MBX_CH_SRP, 0, filler.data(), filler.size()) == MBX_STATUS_OK) {
    }
    loop.transmit(loop.transmit_ctx, 1u);
    ASSERT_GT(adapter.owed_len, 0u) << "(the ring refuses the second slice's frame)";
    EXPECT_NE(adapter.tx_due & (1u << adapter.owed_if), 0u)
        << "a frame the ring refuses in a build's second slice leaves its interface due";
    mbx_model_tx_pause(&model, false);
    serve();
}

// A join timer restarts on what a build sent and on nothing else, so its count (tick) stays the participant's: a
// build of a participant that sends nothing leaves it, and an Applicant moved while it runs owes nothing before it
// ends. LeaveAll's timer owes its LeaveAll whatever the join timer's count (802.1Q Table 10-5).
TEST_F(Srp, TheJoinCountFollowsWhatABuildSent) {
    settle();
    for (unsigned n=0;n<CTRL_LOOP_JOIN_CS;++n) loop.ticks[0]();
    settle();
    const uint8_t left=adapter.join_left[0];
    EXPECT_EQ(left,CTRL_LOOP_JOIN_CS)<<"a sent MRPDU restarts its participant's count at the JoinTime";
    EXPECT_EQ(adapter.tx_due,0u);
    for (unsigned n=0;n<5u;++n) loop.ticks[0]();
    EXPECT_EQ(adapter.join_left[0],left-5u)<<"each centisecond takes one off it";
    EXPECT_EQ(adapter.tx_due,0u);
    adapter.tx_due=1u;
    settle();
    EXPECT_EQ(adapter.join_left[0],left-5u)<<"a build that sends nothing leaves the count";
    EXPECT_GT(adapter.transmitted,0u);
    bool active=false;
    for (unsigned n=0;n<1600u && !active;++n) {
        const uint32_t sent=adapter.transmitted;
        loop.ticks[0]();
        enum mrp_la_state la=MRP_LA_STATE_PASSIVE;
        (void)mrp_port_status(adapter.ifs[0].msrp,0,&la,nullptr);
        active=la==MRP_LA_STATE_ACTIVE;
        if (active) {
            EXPECT_NE(adapter.tx_due,0u)<<"a LeaveAll timer's end owes its LeaveAll";
            settle();
            EXPECT_GT(adapter.transmitted,sent)<<"which its pass sends";
        }
        settle();
    }
    EXPECT_TRUE(active)<<"LeaveAll's timer ran out within its 10 to 15 s";
}

// What THE RETRY's bound counts (aecp_mbx.h): while notices are queued, under records that move Applicants, an interface
// takes a pass given whole for a join timer's end and one for each participant moved with its join timer idle.
TEST_F(Srp, AJoinTimeOwesAnInterfaceAPass) {
    settle(); advance(1000);
    loop.retry_queued=true;
    const uint32_t passes=loop.stats.transmit_passes;
    for (unsigned n=0;n<20u;++n) {
        offer(frame(4,{6,static_cast<uint8_t>(3u+n%2u),0,static_cast<uint8_t>(2u+n%2u)},0)); advance(10);
    }
    loop.retry_queued=false;
    EXPECT_LE(loop.stats.transmit_passes-passes,2u*MBX_N_IF)<<"an interface's passes given whole, a JoinTime";
}

// An Applicant that moves owes a pass only with its own participant's join timer idle (THE TRANSMIT).
TEST_F(Srp, AnApplicantMovedOwesAPassWithItsOwnJoinTimerIdle) {
    settle(); advance(400);
    adapter.tx_due=0u; adapter.join_left[0]=0u; adapter.join_left[1]=10u;
    ASSERT_EQ(mvrp_declare(adapter.ifs[0].mvrp,0,9),0);
    EXPECT_EQ(adapter.tx_due,0u)<<"not while its own runs, the other's idle or not";
    adapter.join_left[1]=0u;
    ASSERT_EQ(mvrp_declare(adapter.ifs[0].mvrp,0,10),0);
    EXPECT_NE(adapter.tx_due,0u)<<"an Applicant moved with its own join timer idle owes a pass";
    settle();
}

// What a first VLAN send licenses is declared in the pass that sent it, not at the join timer's end after it.
TEST_F(Srp, AFirstVlanSendDeclaresWhatItLicensesInItsPass) {
    settle(); advance(400);
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,7));
    std::vector<uint8_t> talker(25); std::copy(sid.bytes,sid.bytes+8,talker.begin());
    std::copy(da,da+6,talker.begin()+8); wire_put_be(talker.data()+14,7,2);
    wire_put_be(talker.data()+16,224,2); wire_put_be(talker.data()+18,1,2); talker[20]=0x60;
    offer(frame(1,talker,0));
    for (unsigned n=0;n<400u && !adapter.ifs[0].sinks[0].vlan_sent;++n) {
        mbx_model_advance_ms(&model,1); ctrl_loop_service(&loop);
    }
    ASSERT_TRUE(adapter.ifs[0].sinks[0].vlan_sent);
    EXPECT_EQ(adapter.ifs[0].sinks[0].declared,2u)<<"the pass that sent it declares what it licensed";
}

// A frame a build left owed comes first (A3): while it is owed no pass is given to the build, and the interface stays
// due, so the pass after the poll sends it builds what is left.
TEST_F(Srp, AnOwedFrameComesBeforeTheBuild) {
    settle();
    for (unsigned n=0;n<20u;++n) loop.ticks[0]();
    mbx_model_tx_pause(&model,true);
    std::vector<uint8_t> filler(60); wire_put_be(filler.data(),0x0180c200000eull,6);
    wire_put_be(filler.data()+12,0x22ea,2);
    while(mbx_tx_send(MBX_CH_SRP,0,filler.data(),filler.size())==MBX_STATUS_OK) {}
    for (unsigned n=0;n<8u && !adapter.owed_len;++n) ctrl_loop_service(&loop);
    ASSERT_GT(adapter.owed_len,0u);
    const uint32_t whole=loop.stats.transmit_passes;
    for (unsigned n=0;n<8u;++n) {
        mbx_model_advance_ms(&model,MBX_TICK_MS);
        ctrl_loop_service(&loop);
    }
    ASSERT_GT(adapter.owed_len,0u);
    EXPECT_NE(adapter.tx_due&(1u<<adapter.owed_if),0u)<<"the interface stays due";
    EXPECT_EQ(loop.stats.transmit_passes,whole)<<"no pass goes to the build while a frame is owed";
    mbx_model_tx_pause(&model,false);
    const uint32_t sent=adapter.transmitted;
    EXPECT_NE(ctrl_loop_service(&loop),0u);
    EXPECT_EQ(adapter.owed_len,0u);
    EXPECT_EQ(adapter.transmitted,sent+1u)<<"the pass whose poll sends the owed frame builds no other";
    settle();
    EXPECT_EQ(adapter.tx_due,0u)<<"then the build takes what is left";
}

// ---- #925: Talker Advertise and Talker Failed for one stream -------------------------------------------
// A talker declares one of the two for a stream and moves directly between them (IEEE 802.1Q-2018 35.1.2.1). A
// received JoinIn or JoinMt of one replaces a registered other (35.2.6), but lwSRP registers a New beside it, where
// 35.2.6's informative NOTE would give the Failed precedence. Milan v1.2 5.3.8.5 and the ruling on #925 decide: the
// latest registered decides the Listener declaration for as long as both stay registered.
class SrpTalkerKinds : public Srp {
protected:
    static constexpr unsigned kJoinMs=CTRL_LOOP_JOIN_CS*10u;
    // the kinds as srp_mbx.c holds them, which are also the Listener declarations they ask for (35.2.2.7.2)
    static constexpr unsigned kFailed=1u;
    static constexpr unsigned kAdvertise=2u;
    static constexpr unsigned kNew=0u;
    static constexpr unsigned kJoinIn=1u;
    static constexpr unsigned kLv=5u;
    const msrp_stream_id sid[2]={{{2,1,2,3,4,5,6,7}},{{2,1,2,3,4,5,6,8}}};
    const uint8_t da[2][6]={
        {0x91,0xe0,0xf0,0,0,9}, {0x91,0xe0,0xf0,0,0,10}
    };
    struct Message {
        unsigned kind;
        unsigned event;
        unsigned stream;
    };
    // One MRPDU of these Talker messages in this order (802.1Q 10.8: a Message ends at its EndMark, then the next),
    // each of stream s to its own destination: MSRP type 1 Advertise, 2 Failed (Table 35-1).
    std::vector<uint8_t> mrpdu(std::initializer_list<Message> messages) {
        std::vector<uint8_t> f;
        for (const auto &m:messages) {
            auto v=talker_value(sid[m.stream],da[m.stream],2);
            if (m.kind==kFailed) { v.resize(34); v[33]=1; }
            const auto next=frame(m.kind==kAdvertise ? 1u : 2u,v,m.event);
            if (f.empty()) { f=next; continue; }
            f.resize(f.size()-2u);
            f.insert(f.end(),next.begin()+15,next.end());
        }
        return f;
    }
    std::vector<uint8_t> record(unsigned kind, unsigned event) { return mrpdu({{kind,event,0}}); }
    // The MRPDU f with the messages of MRPDU next after its own.
    static std::vector<uint8_t> then(std::vector<uint8_t> f, const std::vector<uint8_t> &next) {
        f.resize(f.size()-2u);
        f.insert(f.end(),next.begin()+15,next.end());
        return f;
    }
    void bind(unsigned k, unsigned s=0, unsigned d=0) {
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,k,&sid[s],da[d],2)); settle();
    }
    void unbind(unsigned k) { ASSERT_TRUE(srp_mbx_bind(&adapter,0,k,nullptr,nullptr,0)); settle(); }
    // Time passes until both of the interface's join timers are idle and it owes no MRPDU.
    void idle() {
        for (unsigned n=0; n<2000u && (adapter.join_left[0]!=0u || adapter.join_left[1]!=0u || adapter.tx_due!=0u); ++n)
            advance(1);
        ASSERT_EQ(adapter.join_left[0],0u); ASSERT_EQ(adapter.join_left[1],0u); ASSERT_EQ(adapter.tx_due,0u);
    }
    const srp_sink &sink(unsigned k) const { return adapter.ifs[0].sinks[k]; }
    // The Listener declarations of stream s sent from frame `from` on.
    std::vector<Declaration> listeners(uint32_t from, unsigned s=0) {
        capture(from);
        std::vector<Declaration> out;
        for (const auto &d:declarations)
            if (d.ethertype==0x22ea && d.type==3 && std::equal(d.value.begin(),d.value.end(),sid[s].bytes))
                out.push_back(d);
        return out;
    }
    // The record is offered and one JoinTime passes with no other talker MRPDU: the binding's Listener declaration
    // of stream s is `subtype` (0 withdrawn), and it was on the wire within that JoinTime.
    void expect_declared(const std::vector<uint8_t> &record, unsigned k, unsigned subtype, const char *words,
                         unsigned s=0) {
        const uint32_t from=model.tx_sent; const unsigned start=model.now_ms;
        offer(record); advance(kJoinMs);
        EXPECT_EQ(sink(k).desired,subtype)<<words;
        EXPECT_EQ(sink(k).declared,subtype)<<words;
        bool sent=false;
        for (const auto &d:listeners(from,s)) {
            const bool match=subtype ? d.event!=kLv && d.subtype==subtype : d.event==kLv;
            sent=sent || (match && d.time_ms<=start+kJoinMs);
        }
        EXPECT_TRUE(sent)<<words<<": on the wire within a JoinTime";
    }
};

// #925: the talker replaces its Talker Failed with a Talker Advertise, New. The Listener is Ready within a
// JoinTime of it, as its first registration was declared, with the Failed still registered beside it.
TEST_F(SrpTalkerKinds, AnAdvertiseNewReplacesARegisteredFailedWithinAJoinTime) {
    settle(); advance(400); bind(0);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"a first registration declares within a JoinTime");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"an Advertise New replaces the registered Failed");
    EXPECT_EQ(sink(0).registered_kinds,3u)<<"the Failed is still registered beside the New";
}

// The reverse: a Talker Failed New over a registered Talker Advertise asks Failed at once, and again over an
// Advertise registered New beside the Failed, both kinds still registered.
TEST_F(SrpTalkerKinds, AFailedNewReplacesARegisteredAdvertiseWithinAJoinTime) {
    settle(); advance(400); bind(0);
    expect_declared(record(kAdvertise,kJoinIn),0,kAdvertise,"a first registration declares within a JoinTime");
    expect_declared(record(kFailed,kNew),0,kFailed,"a Failed New replaces the registered Advertise");
    EXPECT_EQ(sink(0).registered_kinds,3u)<<"the Advertise is still registered beside the New";
    expect_declared(record(kAdvertise,kLv),0,kFailed,"the Advertise leaves");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"an Advertise New beside the Failed");
    expect_declared(record(kFailed,kNew),0,kFailed,"a Failed New replaces the registered Advertise, both registered");
}

// Leave of either, in both orders: the latest leaving hands the declaration to the other, which then withdraws it;
// the older leaving changes nothing.
TEST_F(SrpTalkerKinds, LeaveOfEitherKindLeavesTheOtherDeciding) {
    settle(); advance(400); bind(0);
    for (unsigned latest : {kAdvertise,kFailed}) {
        const unsigned older=3u-latest;
        expect_declared(record(older,kJoinIn),0,older,"the older registration");
        expect_declared(record(latest,kNew),0,latest,"the latest registration");
        expect_declared(record(latest,kLv),0,older,"the latest leaves: the other decides");
        expect_declared(record(older,kLv),0,0,"the other leaves: withdrawn");
        expect_declared(record(older,kJoinIn),0,older,"the older again");
        expect_declared(record(latest,kNew),0,latest,"the latest again");
        const uint32_t from=model.tx_sent;
        offer(record(older,kLv)); advance(kJoinMs);
        EXPECT_EQ(sink(0).desired,latest)<<"the older leaves: the latest keeps deciding";
        EXPECT_EQ(sink(0).registered_kinds,latest);
        for (const auto &d:listeners(from)) {
            EXPECT_NE(d.event,kLv)<<"the older leaving withdraws nothing";
            EXPECT_EQ(d.subtype,latest)<<"the older leaving changes nothing";
        }
        expect_declared(record(latest,kLv),0,0,"the latest leaves last: withdrawn");
    }
}

// Coincident registrations, both in one MRPDU: lwSRP applies its messages in their order, so the later registration
// decides; and a replacement whose Leave of the old kind rides the same MRPDU as the New is continuous.
TEST_F(SrpTalkerKinds, CoincidentRegistrationsInOneMrpduFollowTheirOrder) {
    settle(); advance(400); bind(0,0,0); bind(1,1,1);
    expect_declared(mrpdu({{kFailed,kNew,0},{kAdvertise,kNew,0}}),0,kAdvertise,"Failed then Advertise in one MRPDU");
    expect_declared(mrpdu({{kAdvertise,kNew,1},{kFailed,kNew,1}}),1,kFailed,"Advertise then Failed in one MRPDU",1);
    EXPECT_EQ(sink(0).registered_kinds,3u);
    EXPECT_EQ(sink(1).registered_kinds,3u);
    expect_declared(mrpdu({{kAdvertise,kNew,1},{kFailed,kLv,1}}),1,kAdvertise,"an Advertise New beside the Failed's Leave",1);
    EXPECT_EQ(sink(1).registered_kinds,2u);
    EXPECT_FALSE(sink(1).withdrawn)<<"a replacement in one MRPDU is no withdrawal";
}

// A binding made while both are registered takes the StreamID's latest from any binding of it, whatever that one's
// destination: another binding of the same destination, then one of another; and the StreamID's only binding replaced
// in place by one of another destination carries it back to its own.
TEST_F(SrpTalkerKinds, ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream) {
    settle(); advance(400);
    for (unsigned other : {0u,1u}) {
        bind(0,0,other);
        offer(record(kFailed,kJoinIn)); offer(record(kAdvertise,kNew)); advance(kJoinMs);
        EXPECT_EQ(sink(0).desired,other ? 0u : kAdvertise);
        const uint32_t from=model.tx_sent;
        bind(1); advance(kJoinMs);
        EXPECT_EQ(sink(1).desired,kAdvertise)<<"a later binding takes the latest registration";
        EXPECT_EQ(sink(1).declared,kAdvertise)<<"the shared declaration stays Ready, not ReadyFailed";
        for (const auto &d:listeners(from)) EXPECT_EQ(d.subtype,kAdvertise)<<"the shared declaration stays Ready";
        // in place: the StreamID's only binding replaced by one of another destination, then by its own again
        unbind(0); bind(1,0,1); advance(kJoinMs);
        EXPECT_EQ(sink(1).desired,0u)<<"another destination matches neither registration";
        bind(1); advance(kJoinMs);
        EXPECT_EQ(sink(1).desired,kAdvertise)<<"a later binding takes the latest registration, one in place too";
        offer(record(kAdvertise,kLv)); offer(record(kFailed,kLv)); advance(kJoinMs);
        EXPECT_EQ(sink(1).registered_kinds,0u);
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,nullptr,nullptr,0));
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0));
        advance(kJoinMs);
    }
}

// The latest is the StreamID's for as long as both registrations stay, whatever its bindings do. Its last binding
// ends and the sink binds it again with no talker MRPDU between: the latest decides again, in the Listener
// declaration and in ACMP's copy. A binding of another StreamID in that sink's place, or made while it is held, takes
// none of it, and the StreamID's next binding still takes it.
TEST_F(SrpTalkerKinds, AFinalUnbindingKeepsTheLatestWhileBothStayRegistered) {
    for (unsigned latest : {kAdvertise,kFailed}) {
        settle(); advance(400); bind(0);
        offer(record(3u-latest,kJoinIn)); offer(record(latest,kNew)); advance(kJoinMs);
        ASSERT_EQ(sink(0).declared,latest);
        unbind(0); advance(kJoinMs);
        EXPECT_EQ(adapter.held_count,1u)<<"the StreamID none binds holds its latest";
        const uint32_t from=model.tx_sent;
        bind(0); advance(kJoinMs);
        EXPECT_EQ(sink(0).registered_kinds,3u);
        EXPECT_EQ(sink(0).desired,latest)<<"a final unbinding keeps the latest registration";
        EXPECT_EQ(sink(0).declared,latest)<<"a final unbinding keeps the latest registration";
        EXPECT_EQ(sink(0).feedback_kind,latest)<<"ACMP sees the latest registration";
        for (const auto &d:listeners(from)) EXPECT_EQ(d.subtype,latest)<<"the binding made again declares the latest";
        EXPECT_EQ(adapter.held_count,0u)<<"the binding took it";
        bind(0,1,1); advance(kJoinMs);
        EXPECT_EQ(adapter.held_count,1u)<<"a binding of another StreamID in its place holds it";
        bind(0); advance(kJoinMs);
        EXPECT_EQ(sink(0).desired,latest)<<"the StreamID's next binding still takes the latest";
        unbind(0); bind(0,1,1); advance(kJoinMs);
        EXPECT_EQ(sink(0).latest_kind,0u)<<"another StreamID takes none of it";
        EXPECT_EQ(adapter.held_count,1u)<<"another StreamID takes none of it";
        bind(0); advance(kJoinMs);
        EXPECT_EQ(sink(0).desired,latest)<<"the StreamID's next binding still takes the latest";
        expect_declared(record(latest,kLv),0,3u-latest,"the latest leaves: the other decides");
        EXPECT_EQ(adapter.held_count,0u);
        TearDown(); SetUp();
    }
}

// A StreamID none binds is held only while both registrations stay. Its registrations are kept while no binding has
// it (#969), so a JoinIn of one kind, which replaces the other (IEEE 802.1Q-2018 35.2.6), ends it; so does a LeaveAll
// of one kind the talker no longer answers, which lets that registration expire, or a reset of the interface; and a
// binding made later follows what is left.
TEST_F(SrpTalkerKinds, AHeldStreamEndsWithEitherRegistrationOrAReset) {
    for (unsigned ending : {kAdvertise,kFailed,0u}) {
        settle(); advance(400); bind(0);
        offer(record(kFailed,kJoinIn)); offer(record(kAdvertise,kNew)); advance(kJoinMs);
        unbind(0); advance(kJoinMs);
        ASSERT_EQ(adapter.held_count,1u);
        if (ending) {
            auto v=talker_value(sid[0],da[0],2);
            if (ending==kFailed) { v.resize(34); v[33]=1; }
            offer(frame(ending==kAdvertise ? 1u : 2u,v,4u,0,true)); advance(5100);
        } else {
            mbx_model_set_link(&model,0,false); settle(); mbx_model_set_link(&model,0,true); settle(); advance(400);
        }
        EXPECT_EQ(adapter.held_count,0u)<<"a registration's end or a reset ends the hold";
        bind(0); advance(kJoinMs);
        EXPECT_EQ(sink(0).registered_kinds,ending ? 3u-ending : 0u);
        EXPECT_EQ(sink(0).desired,ending ? 3u-ending : 0u)<<"the registration left decides";
        EXPECT_EQ(sink(0).latest_kind,0u)<<"nothing held is taken";
        unbind(0); advance(kJoinMs);
        EXPECT_EQ(adapter.held_count,0u)<<"one kind registered holds nothing";
        TearDown(); SetUp();
    }
}

// A StreamID is held for its own interface: one held on the last interface is taken by no binding of another and
// survives another's reset, and its own interface's binding takes it.
#if MBX_N_IF > 1
TEST_F(SrpTalkerKinds, AStreamIsHeldForItsOwnInterface) {
    const unsigned last=MBX_N_IF-1u;
    settle(); advance(400);
    ASSERT_TRUE(srp_mbx_bind(&adapter,last,0,&sid[0],da[0],2)); settle();
    offer(record(kFailed,kJoinIn),last); offer(record(kAdvertise,kNew),last); advance(kJoinMs);
    ASSERT_EQ(adapter.ifs[last].sinks[0].desired,kAdvertise);
    ASSERT_TRUE(srp_mbx_bind(&adapter,last,0,nullptr,nullptr,0)); settle();
    ASSERT_EQ(adapter.held_count,1u);
    bind(0); advance(kJoinMs);
    EXPECT_EQ(sink(0).latest_kind,0u)<<"another interface's binding takes none of it";
    EXPECT_EQ(adapter.held_count,1u)<<"another interface's binding takes none of it";
    mbx_model_set_link(&model,0,false); settle(); mbx_model_set_link(&model,0,true); settle(); advance(400);
    EXPECT_EQ(adapter.held_count,1u)<<"another interface's reset leaves it";
    ASSERT_TRUE(srp_mbx_bind(&adapter,last,0,&sid[0],da[0],2)); settle(); advance(kJoinMs);
    EXPECT_EQ(adapter.ifs[last].sinks[0].desired,kAdvertise)<<"its own interface's binding takes it";
    EXPECT_EQ(adapter.held_count,0u);
}
#endif

// Half the pool's medium and large blocks bound the StreamIDs held (srp_held), so the table does not fill. Were it
// full, a final unbinding would hold nothing, and a later binding of both kinds with no latest known take Failed.
TEST_F(SrpTalkerKinds, AFullHeldTableHoldsNothingMore) {
    settle(); advance(400); bind(0);
    offer(record(kFailed,kJoinIn)); offer(record(kAdvertise,kNew)); advance(kJoinMs);
    adapter.held_count=SRP_HELD_STREAMS; // every entry interface 0, StreamID 0, as init left them
    unbind(0); advance(kJoinMs);
    EXPECT_EQ(adapter.held_count,SRP_HELD_STREAMS)<<"a full table holds nothing more";
    bind(0); advance(kJoinMs);
    EXPECT_EQ(sink(0).latest_kind,0u);
    EXPECT_EQ(sink(0).desired,kFailed)<<"no latest known: Failed";
    adapter.held_count=0u;
}

// Each New in turn decides, also one of a kind registered beside the other: a talker that moves Failed, Advertise,
// Failed with both kinds still registered asks Failed again, and Ready after its next Advertise.
TEST_F(SrpTalkerKinds, EachNewInTurnDecidesWhileBothAreRegistered) {
    settle(); advance(400); bind(0);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"the Failed");
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"an Advertise New beside it");
    expect_declared(record(kFailed,kNew),0,kFailed,"a Failed New beside the Advertise decides again");
    EXPECT_EQ(sink(0).registered_kinds,3u);
    expect_declared(record(kAdvertise,kNew),0,kAdvertise,"an Advertise New beside the Failed decides again");
}

// A replacement New followed in its MRPDU by a message that changes nothing, an unchanged Domain JoinIn or a Talker
// of a StreamID no binding has, which the filter ignores: the receive filter's copy sees the change before the walk
// does, and the declaration is owed all the same, on the wire within a JoinTime of an idle join timer. A New and its
// own Leave in one MRPDU, then such a message, leave the declaration as it was: only the final state is declared.
TEST_F(SrpTalkerKinds, AReplacementBeforeAMessageThatChangesNothingIsDeclaredWithinAJoinTime) {
    const auto domain=frame(4,{6,3,0,2},1);
    const auto ignored=mrpdu({{kAdvertise,kJoinIn,1}});
    for (unsigned latest : {kAdvertise,kFailed}) {
        for (const auto *trailer : {&domain,&ignored}) {
            settle(); advance(400); bind(0);
            expect_declared(record(3u-latest,kJoinIn),0,3u-latest,"the older registration");
            idle();
            expect_declared(then(record(latest,kNew),*trailer),0,latest,"a New before a message that changes nothing");
            EXPECT_EQ(sink(0).feedback_kind,latest);
            TearDown(); SetUp();
        }
    }
    settle(); advance(400); bind(0);
    expect_declared(record(kFailed,kJoinIn),0,kFailed,"the Failed");
    idle();
    const uint32_t from=model.tx_sent;
    offer(then(mrpdu({{kAdvertise,kNew,0},{kAdvertise,kLv,0}}),domain)); advance(kJoinMs);
    EXPECT_EQ(sink(0).declared,kFailed)<<"an Advertise New and its Leave in one MRPDU leave the Failed deciding";
    EXPECT_FALSE(sink(0).withdrawn);
    for (const auto &d:listeners(from)) {
        EXPECT_NE(d.event,kLv)<<"no withdrawal on the wire";
        EXPECT_EQ(d.subtype,kFailed)<<"only the final state is declared";
    }
}

// ---- #969: a Talker registered before the binding that wants it ------------------------------------------------
// ACMP initiates the SRP reservation only once the talker answers its probe (Milan v1.2 5.5.3.5.18 step 4), after a
// power-on settle or a BIND_RX alike, and a talker's applicant declares once and is then quiet (QA) until a LeaveAll
// (IEEE 802.1Q-2018 Table 10-3). A settled Stream Input declares Listener Ready while a matching Talker Advertise is
// being received (Milan v1.2 5.3.8.5), so the registration the talker made first is the one its binding takes, and the
// declaration rides THE TRANSMIT's next MRPDU, as one made for a registration that follows the binding does.
class SrpEarlyTalker : public SrpTalkerKinds {
protected:
    static constexpr unsigned kMt=4u;
    // stream s, one for each STREAM_INPUT and one past them: its StreamID, destination and Talker record
    static msrp_stream_id stream(unsigned s) { return {{2,1,2,3,4,5,0x40,static_cast<uint8_t>(s)}}; }
    static std::array<uint8_t,6> dest(unsigned s) { return {0x91,0xe0,0xf0,0,1,static_cast<uint8_t>(s)}; }
    std::vector<uint8_t> talker(unsigned s, unsigned kind, unsigned event, bool la=false, uint32_t latency=0u) {
        const auto d=dest(s);
        auto v=talker_value(stream(s),d.data(),2);
        wire_put_be(v.data()+21,latency,4);
        if (kind==kFailed) { v.resize(34); v[33]=1; }
        return frame(kind==kAdvertise ? 1u : 2u,v,event,0,la);
    }
    void bind_stream(unsigned k, unsigned s) {
        const auto sid=stream(s); const auto d=dest(s);
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,k,&sid,d.data(),2));
    }
    // A block returned to the pool owes the count a pending one waits for (srp_mbx.c count_kept), as the MAP work's
    // reservation returned one with every indication; at a one-interface shape lwSRP makes none at one port
    // (LWSRP_ONE_PORT_MAP), so a test that needs that count returns a block of its own (#977).
    void return_block() { ctrl_pool_free(&pool,ctrl_pool_alloc(&pool,1u)); }
    // The Listener declarations of stream s in interface 0's first MSRP MRPDU sent from frame `from` on, and when it
    // left.
    std::vector<Declaration> first_mrpdu(uint32_t from, unsigned s, unsigned *at_ms) {
        capture(from);
        std::vector<Declaration> out;
        const auto sid=stream(s);
        uint32_t first=UINT32_MAX;
        for (const auto &d:declarations) {
            if (d.ethertype!=0x22ea || d.interface!=0u) continue;
            if (first==UINT32_MAX) { first=d.frame; *at_ms=d.time_ms; }
            if (d.frame==first && d.type==3 && std::equal(d.value.begin(),d.value.end(),sid.bytes)) out.push_back(d);
        }
        return out;
    }
    // Sink k binds stream s now: its Listener declaration is `kind` (2 Ready, 1 Asking Failed) in THE TRANSMIT's next
    // MRPDU, within a JoinTime, and ACMP's copy is that kind.
    void expect_bound_declares(unsigned k, unsigned s, unsigned kind, const std::string &words) {
        const uint32_t from=model.tx_sent; const unsigned start=model.now_ms;
        bind_stream(k,s); settle(); advance(kJoinMs);
        EXPECT_EQ(sink(k).desired,kind)<<words<<": input "<<k;
        EXPECT_EQ(sink(k).declared,kind)<<words<<": input "<<k;
        EXPECT_EQ(sink(k).feedback_kind,kind)<<words<<": ACMP is told, input "<<k;
        unsigned at=0;
        const auto first=first_mrpdu(from,s,&at);
        bool declared=false;
        for (const auto &d:first) declared=declared || (d.event!=kLv && d.subtype==kind);
        EXPECT_TRUE(declared)<<words<<": in THE TRANSMIT's next MRPDU, input "<<k;
        EXPECT_LE(at,start+kJoinMs)<<words<<": within a JoinTime, input "<<k;
    }
    // The time passes with no talker MRPDU: the talker's applicant is quiet.
    void quiet(unsigned ms) { advance(ms); }
    // One MRPDU declaring the Talker Advertise (JoinIn) of streams 0 .. CTRL_SRP_SINKS-1, as a bridge re-declares them
    // after a link flap: one vector of them, each value its predecessor's plus one (IEEE 802.1Q-2018 35.2.2.8.4), or
    // one message each.
    std::vector<uint8_t> every_input(bool vector) {
        auto f=talker(0,kAdvertise,kJoinIn);
        if (!vector) {
            for (unsigned k=1;k<CTRL_SRP_SINKS;++k) f=then(f,talker(k,kAdvertise,kJoinIn));
            return f;
        }
        const unsigned n=CTRL_SRP_SINKS;
        f.resize(46u);                          // the headers and the FirstValue
        wire_put_be(f.data()+19,n,2);           // NumberOfValues, no LeaveAll
        wire_put_be(f.data()+17,29u+(n+2u)/3u,2); // the AttributeListLength
        for (unsigned k=0;k<n;k+=3u) {
            f.push_back(static_cast<uint8_t>(kJoinIn*36u+(k+1u<n ? kJoinIn*6u : 0u)+(k+2u<n ? kJoinIn : 0u)));
        }
        f.insert(f.end(),{0,0,0,0});            // the list's EndMark and the MRPDU's
        return f;
    }
    // Every input bound now to its stream declares it: the receive kept each one's registration.
    void expect_every_input_declares(const std::string &words) {
        for (unsigned k=0;k<CTRL_SRP_SINKS;++k) expect_bound_declares(k,k,kAdvertise,words);
    }
};

// Registration, then binding: every STREAM_INPUT's Talker is declared shortly after power-on, the talker is then
// quiet, and each input's binding lands some seconds later (the probe's answer), within the DUT's first LeaveAll
// period; each declares in THE TRANSMIT's next MRPDU. Advertise asks Ready, Failed asks Asking Failed.
TEST_F(SrpEarlyTalker, ARegistrationMadeBeforeItsBindingIsDeclaredWithinOneTransmitOnEveryInput) {
    for (unsigned kind : {kAdvertise,kFailed}) {
        settle(); advance(400);
        for (unsigned k=0;k<CTRL_SRP_SINKS;++k) offer(talker(k,kind,kJoinIn));
        quiet(5000);
        for (unsigned k=0;k<CTRL_SRP_SINKS;++k) {
            expect_bound_declares(k,k,kind,kind==kAdvertise ? "an Advertise registered before its binding"
                                                            : "a Failed registered before its binding");
        }
        TearDown(); SetUp();
    }
}

// Binding, then registration, the order that always worked, at every input too: each declares within a JoinTime of
// its registration, also with the registrations kept for StreamIDs no binding has at their bound (streams past the
// inputs' own), as a binding's own Talker is taken whatever is kept.
TEST_F(SrpEarlyTalker, ABindingMadeBeforeItsRegistrationIsDeclaredWithinAJoinTimeOnEveryInput) {
    settle(); advance(400);
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) offer(talker(0x80u+k,kAdvertise,kJoinIn));
    quiet(400);
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) {
        bind_stream(k,k); settle();
        const uint32_t from=model.tx_sent; const unsigned start=model.now_ms;
        offer(talker(k,kAdvertise,kJoinIn)); advance(kJoinMs);
        EXPECT_EQ(sink(k).declared,kAdvertise)<<"a binding made before its registration: input "<<k;
        bool sent=false;
        capture(from);
        const auto sid=stream(k);
        for (const auto &d:declarations) {
            sent=sent || (d.ethertype==0x22ea && d.type==3 && d.subtype==kAdvertise && d.event!=kLv &&
                          d.time_ms<=start+kJoinMs && std::equal(d.value.begin(),d.value.end(),sid.bytes));
        }
        EXPECT_TRUE(sent)<<"a binding made before its registration: on the wire within a JoinTime, input "<<k;
    }
}

// BIND_RX while bound: each input is bound and declaring for one stream while another's Talker has been declared all
// along; re-bound to that one, it declares it in THE TRANSMIT's next MRPDU and withdraws the first.
TEST_F(SrpEarlyTalker, ARebindWhileBoundToAStreamDeclaredAllAlongIsDeclaredWithinOneTransmit) {
    settle(); advance(400);
    const unsigned other=CTRL_SRP_SINKS-1u;
    offer(talker(other,kAdvertise,kJoinIn));
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) {
        if (k==other) continue;
        bind_stream(k,k); settle();
        offer(talker(k,kAdvertise,kJoinIn)); advance(kJoinMs);
        ASSERT_EQ(sink(k).declared,kAdvertise)<<"input "<<k<<" declares its first stream";
        quiet(400);
        const uint32_t from=model.tx_sent;
        expect_bound_declares(k,other,kAdvertise,"a rebind to a stream declared all along");
        bool withdrawn=false;
        capture(from);
        const auto first=stream(k);
        for (const auto &d:declarations) {
            withdrawn=withdrawn || (d.ethertype==0x22ea && d.type==3 && d.event==kLv &&
                                    std::equal(d.value.begin(),d.value.end(),first.bytes));
        }
        EXPECT_TRUE(withdrawn)<<"the rebind withdraws the first stream's Listener: input "<<k;
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,k,nullptr,nullptr,0)); settle(); advance(kJoinMs);
    }
}

// The latest kind decides for a StreamID no binding has as it does for a bound one (#925): a Failed, then an Advertise
// New beside it, and the binding asks Ready; the reverse, Asking Failed.
TEST_F(SrpEarlyTalker, ABindingTakesTheLatestOfTwoKindsRegisteredBeforeIt) {
    for (unsigned latest : {kAdvertise,kFailed}) {
        settle(); advance(400);
        offer(talker(0,3u-latest,kJoinIn)); offer(talker(0,latest,kNew)); quiet(1000);
        expect_bound_declares(0,0,latest,"the latest of two kinds registered before the binding");
        EXPECT_EQ(sink(0).registered_kinds,3u)<<"both kinds are registered";
        TearDown(); SetUp();
    }
}

// A JoinIn of the other kind replaces a registration kept for a StreamID no binding has (IEEE 802.1Q-2018 35.2.6), as it
// does a bound one's: the binding made later takes the talker's current kind alone.
TEST_F(SrpEarlyTalker, AJoinInOfTheOtherKindReplacesARegistrationKeptBeforeTheBinding) {
    for (unsigned now : {kAdvertise,kFailed}) {
        settle(); advance(400);
        offer(talker(0,3u-now,kJoinIn)); offer(talker(0,now,kJoinIn)); quiet(1000);
        expect_bound_declares(0,0,now,"a JoinIn of the other kind replaces the kept registration");
        EXPECT_EQ(sink(0).registered_kinds,now)<<"the replaced kind is no longer registered";
        TearDown(); SetUp();
    }
}

// A kept registration that ends holds its block until mrp_reclaim frees it, so it is counted until then, by a walk made
// meanwhile too (a bound Talker's indication owes one) and by the count a returned block owes (return_block); once the
// block is freed, the walk its return owes counts it no more, and another StreamID's Talker is kept in its place.
TEST_F(SrpEarlyTalker, AKeptRegistrationThatLeftHoldsItsPlaceUntilItsBlockIsFreed) {
    settle(); advance(400);
    const unsigned past=CTRL_SRP_SINKS, bound=CTRL_SRP_SINKS+1u;
    bind_stream(0,bound); settle();
    offer(talker(bound,kAdvertise,kJoinIn)); advance(kJoinMs);
    ASSERT_EQ(sink(0).declared,kAdvertise);
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) offer(talker(k,kAdvertise,kJoinIn));
    quiet(400);
    const unsigned full=ctrl_pool_in_use(&pool);
    // stream 0's Talker leaves, and the bound one's registers a new accumulated latency, in one MRPDU: the walk the
    // bound indication owes runs before any poll reclaims, and the declaration it leaves as it was owes no transmit
    receive_before_poll(then(talker(0,kAdvertise,kLv),talker(bound,kAdvertise,kJoinIn,false,1000u)));
    ASSERT_EQ(sink(0).declared,kAdvertise);
    return_block();
    const unsigned left=ctrl_pool_in_use(&pool);
    receive_before_poll(talker(past,kAdvertise,kJoinIn));
    EXPECT_EQ(ctrl_pool_in_use(&pool),left)<<"a kept registration that left is counted until its block is freed";
    settle(); advance(kJoinMs);
    EXPECT_EQ(ctrl_pool_in_use(&pool),full-1u)<<"the left one's block is freed";
    offer(talker(past,kAdvertise,kJoinIn));
    expect_bound_declares(1,past,kAdvertise,"once its block is freed, another is kept");
}

// An unbinding leaves its StreamID's registration kept (the issue's control: UNBIND_RX then BIND_RX declares at once),
// and counted against the bound from the next receive on; a binding made again takes it.
TEST_F(SrpEarlyTalker, AnUnboundRegistrationIsKeptAndCountedAgainstTheBound) {
    settle(); advance(400);
    const unsigned mine=CTRL_SRP_SINKS, past=CTRL_SRP_SINKS+1u;
    bind_stream(0,mine); settle();
    offer(talker(mine,kAdvertise,kJoinIn)); advance(kJoinMs);
    ASSERT_EQ(sink(0).declared,kAdvertise);
    for (unsigned k=1;k<CTRL_SRP_SINKS;++k) offer(talker(k,kAdvertise,kJoinIn));
    // a refresh of one kept: the count before it, owed by a block returned (return_block), sees every one kept
    // registered, so none is pending when the binding changes, and the unbinding alone owes the next count
    return_block();
    offer(talker(1,kAdvertise,kJoinIn)); quiet(400);
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0)); settle(); advance(kJoinMs);
    const unsigned full=ctrl_pool_in_use(&pool);
    offer(talker(past,kAdvertise,kJoinIn));
    EXPECT_EQ(ctrl_pool_in_use(&pool),full)<<"an unbound registration is kept and counted: the bound is reached";
    quiet(400);
    expect_bound_declares(1,mine,kAdvertise,"an unbound registration kept, bound again");
}

// An unbinding at the bound leaves one registration more than the bound kept: the count before the next receive counts
// it, and lists the bound's first, so a Talker of another StreamID is kept no more until one ends; the binding made
// again takes it.
TEST_F(SrpEarlyTalker, AnUnbindingAtTheBoundIsCountedPastIt) {
    settle(); advance(400);
    const unsigned mine=CTRL_SRP_SINKS, past=CTRL_SRP_SINKS+1u;
    bind_stream(0,mine); settle();
    offer(talker(mine,kAdvertise,kJoinIn)); advance(kJoinMs);
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) offer(talker(k,kAdvertise,kJoinIn));
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0)); settle(); advance(kJoinMs);
    const unsigned full=ctrl_pool_in_use(&pool);
    offer(talker(past,kAdvertise,kJoinIn));
    EXPECT_EQ(ctrl_pool_in_use(&pool),full)<<"one past the bound is counted: no other is kept";
    offer(talker(0,kAdvertise,kJoinIn));
    EXPECT_EQ(ctrl_pool_in_use(&pool),full)<<"a kept one refreshed takes no block";
    quiet(400);
    expect_bound_declares(1,mine,kAdvertise,"the registration an unbinding left past the bound, bound again");
}

// Past the held table's bound, a registration kept for a StreamID no binding has holds nothing: a binding made later
// of both kinds with no latest known takes Failed (#925's fallback, AFullHeldTableHoldsNothingMore).
TEST_F(SrpEarlyTalker, AFullHeldTableHoldsNoKeptRegistration) {
    settle(); advance(400);
    adapter.held_count=SRP_HELD_STREAMS; // every entry interface 0, StreamID 0, as init left them
    offer(talker(1,kFailed,kJoinIn)); offer(talker(1,kAdvertise,kNew)); quiet(1000);
    EXPECT_EQ(adapter.held_count,SRP_HELD_STREAMS)<<"a full table holds nothing more";
    expect_bound_declares(0,1,kFailed,"no latest known: Failed");
    adapter.held_count=0u;
}

// What the talker withdrew before the binding is not declared: a Leave, or a LeaveAll it no longer answers, ends the
// registration, and the binding declares nothing; nor does a registration a reset of the interface destroyed.
TEST_F(SrpEarlyTalker, ARegistrationThatEndedBeforeTheBindingDeclaresNothing) {
    for (unsigned ending : {kLv,kMt,0u}) {
        settle(); advance(400);
        offer(talker(0,kAdvertise,kJoinIn)); quiet(400);
        if (ending==kLv) {
            offer(talker(0,kAdvertise,kLv));
        } else if (ending==kMt) {
            offer(talker(0,kAdvertise,kMt,true));
        } else {
            mbx_model_set_link(&model,0,false); settle(); mbx_model_set_link(&model,0,true); settle();
        }
        // past a LeaveAll's leave timer, as AHeldStreamEndsWithEitherRegistrationOrAReset waits
        advance(5100);
        const char *how=ending==kLv ? "a Leave" : ending==kMt ? "a LeaveAll unanswered" : "a reset";
        bind_stream(0,0); settle(); advance(kJoinMs);
        EXPECT_EQ(sink(0).registered_kinds,0u)<<"a registration ended by "<<how<<" is not taken";
        EXPECT_EQ(sink(0).declared,0u)<<"a registration ended by "<<how<<" declares nothing";
        TearDown(); SetUp();
    }
}

// The registrations kept for StreamIDs no binding has are bounded: one for each STREAM_INPUT of the shape, each a pool
// block. One past them takes no block; bound later, it is declared with the talker's next declaration, as before.
TEST_F(SrpEarlyTalker, RegistrationsKeptBeforeABindingAreBoundedByTheInputs) {
    settle(); advance(400);
    const unsigned before=ctrl_pool_in_use(&pool);
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) offer(talker(k,kAdvertise,kJoinIn));
    EXPECT_EQ(ctrl_pool_in_use(&pool),before+CTRL_SRP_SINKS)<<"one block for each registration kept";
    const unsigned past=CTRL_SRP_SINKS;
    offer(talker(past,kAdvertise,kJoinIn));
    EXPECT_EQ(ctrl_pool_in_use(&pool),before+CTRL_SRP_SINKS)<<"a registration past the bound takes no block";
    // counted again (a binding owes the count, here one of a stream nobody declares), they are still kept
    bind_stream(CTRL_SRP_SINKS-1u,0x90u); settle(); advance(kJoinMs);
    offer(talker(past,kAdvertise,kJoinIn));
    EXPECT_EQ(ctrl_pool_in_use(&pool),before+CTRL_SRP_SINKS)<<"counted again, they are still kept";
    // a New of the other kind of a kept StreamID registers beside it (lwSRP, as srp_mbx.c's listener_kind notes): a
    // registration of its own, past the bound too
    offer(talker(1,kFailed,kNew));
    EXPECT_EQ(ctrl_pool_in_use(&pool),before+CTRL_SRP_SINKS)<<"the other kind of a kept StreamID, past the bound";
    quiet(400);
    bind_stream(0,past); settle(); advance(kJoinMs);
    EXPECT_EQ(sink(0).declared,0u)<<"past the bound, nothing is declared before the talker's next declaration";
    const uint32_t from=model.tx_sent; const unsigned start=model.now_ms;
    offer(talker(past,kAdvertise,kJoinIn)); advance(kJoinMs);
    EXPECT_EQ(sink(0).declared,kAdvertise)<<"past the bound, the talker's next declaration is declared";
    capture(from);
    const auto sid=stream(past);
    bool sent=false;
    for (const auto &d:declarations) {
        sent=sent || (d.ethertype==0x22ea && d.type==3 && d.subtype==kAdvertise && d.event!=kLv &&
                      d.time_ms<=start+kJoinMs && std::equal(d.value.begin(),d.value.end(),sid.bytes));
    }
    EXPECT_TRUE(sent)<<"past the bound, the talker's next declaration: on the wire within a JoinTime";
}

// One receive declaring every STREAM_INPUT's Talker, in one vector or one message each, is kept whole into a fresh
// registrar: the bound is one for each input.
TEST_F(SrpEarlyTalker, OneReceiveOfEveryInputIsKeptWholeIntoAFreshRegistrar) {
    for (bool vector : {true,false}) {
        settle(); advance(400);
        offer(every_input(vector)); quiet(400);
        expect_every_input_declares(vector ? "a fresh registrar keeps one vector of every input"
                                           : "a fresh registrar keeps one receive of every input");
        TearDown(); SetUp();
    }
}

// A reset destroys the participants and what they kept: the new ones keep nothing, so the count the next receive starts
// from holds none, and one receive of every input after it (a bridge re-declaring after a link flap) is kept whole
// (#969, create_participants).
TEST_F(SrpEarlyTalker, AResetLeavesNoKeptRegistrationCounted) {
    for (bool vector : {true,false}) {
        settle(); advance(400);
        offer(talker(0xe0u,kAdvertise,kJoinIn)); quiet(400);
        // a refresh: the count before it sees the kept one registered, so nothing is pending when the reset comes and
        // only the reset's own zeroing leaves the count it destroyed behind
        offer(talker(0xe0u,kAdvertise,kJoinIn)); quiet(400);
        ASSERT_EQ(adapter.kept_count[0],1u)<<"one registration kept, below the bound";
        mbx_model_set_link(&model,0,false); settle(); mbx_model_set_link(&model,0,true); settle(); advance(400);
        offer(every_input(vector)); quiet(400);
        expect_every_input_declares(vector ? "after a reset, one vector of every input is kept whole"
                                           : "after a reset, one receive of every input is kept whole");
        TearDown(); SetUp();
    }
}

// A kept registration that left holds its place until mrp_reclaim frees its block (AKeptRegistrationThatLeftHolds...),
// and below the bound as at it, the count after that return holds it no more: its end leaves the count pending, so one
// receive of every input after it is kept whole, a moment after the Leave as past the Leave's timer.
TEST_F(SrpEarlyTalker, AKeptRegistrationWhoseBlockIsFreedIsCountedNoMore) {
    for (unsigned wait : {400u,5100u}) {
        for (bool vector : {true,false}) {
            settle(); advance(400);
            offer(talker(0xe0u,kAdvertise,kJoinIn)); quiet(400);
            ASSERT_EQ(adapter.kept_count[0],1u)<<"one registration kept, below the bound";
            offer(talker(0xe0u,kAdvertise,kLv)); quiet(wait);
            offer(every_input(vector)); quiet(400);
            expect_every_input_declares(vector
                                            ? "a kept one freed below the bound: one vector of every input is kept"
                                            : "a kept one freed below the bound: one receive of every input is kept");
            TearDown(); SetUp();
        }
    }
}

// A Leave of a StreamID no registration had is kept too, and lwSRP creates its attribute with no registration, which
// mrp_reclaim frees with no indication: kept since the count, it leaves the count pending, so the count after the
// return holds it no more and one receive of every input after it is kept whole.
TEST_F(SrpEarlyTalker, AKeptLeaveOfAStreamNeverRegisteredIsCountedNoMoreOnceFreed) {
    settle(); advance(400);
    offer(talker(0xe1u,kAdvertise,kLv));
    ASSERT_EQ(adapter.kept_count[0],1u)<<"a Leave of a StreamID never registered is kept";
    quiet(400);
    offer(every_input(true)); quiet(400);
    expect_every_input_declares("a Leave kept for a StreamID never registered, freed: every input is kept");
}

// A kept registration refreshed is the one kept, counted once, within one receive as across receives: the talker's
// JoinIn again takes no more of the bound, and the rest of the inputs' Talkers are kept beside it.
TEST_F(SrpEarlyTalker, AKeptRegistrationRefreshedIsCountedOnce) {
    for (bool one_receive : {true,false}) {
        settle(); advance(400);
        if (one_receive) {
            auto f=then(talker(0,kAdvertise,kJoinIn),talker(0,kAdvertise,kJoinIn));
            for (unsigned k=1;k<CTRL_SRP_SINKS;++k) f=then(f,talker(k,kAdvertise,kJoinIn));
            offer(f);
        } else {
            offer(talker(0,kAdvertise,kJoinIn));
            for (unsigned n=0;n<3u;++n) receive_before_poll(talker(0,kAdvertise,kJoinIn));
            EXPECT_EQ(adapter.kept_count[0],1u)<<"a kept registration refreshed is counted once";
            for (unsigned k=1;k<CTRL_SRP_SINKS;++k) receive_before_poll(talker(k,kAdvertise,kJoinIn));
            settle();
        }
        quiet(400);
        expect_every_input_declares(one_receive
                                        ? "a kept registration refreshed in one receive, the rest kept beside it"
                                        : "a kept registration refreshed, the rest kept beside it");
        TearDown(); SetUp();
    }
}

// Unbound Talkers at the receive rate leave the bound StreamIDs their blocks: at most the bound is kept, nothing is
// refused, no walk is owed, and every input bound later declares its own Talker's registration.
TEST_F(SrpEarlyTalker, AFloodOfUnboundTalkersStarvesNoBoundInput) {
    settle(); advance(400);
    const auto before=ctrl_pool_in_use(&pool);
    const auto refused=adapter.refused;
    const auto walks=adapter.walks;
    for (unsigned k=0;k<1000u;++k) { offer(talker(0x40u+(k%128u),kAdvertise,kJoinIn)); advance(2); }
    EXPECT_LE(ctrl_pool_in_use(&pool),before+CTRL_SRP_SINKS)<<"a flood keeps at most the bound";
    EXPECT_EQ(adapter.refused,refused)<<"a flood is refused nothing";
    EXPECT_EQ(adapter.walks,walks)<<"unbound registrations owe no walk";
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) {
        bind_stream(k,k); settle();
        offer(talker(k,kAdvertise,kJoinIn)); advance(kJoinMs);
        EXPECT_EQ(sink(k).declared,kAdvertise)<<"a flood starves no bound input: input "<<k;
    }
}

// UNBIND_RX then BIND_RX to the same stream declares at once on every input (the issue's control).
TEST_F(SrpEarlyTalker, AnUnbindingThenABindingDeclaresAtOnceOnEveryInput) {
    settle(); advance(400);
    for (unsigned k=0;k<CTRL_SRP_SINKS;++k) {
        bind_stream(k,k); settle();
        offer(talker(k,kAdvertise,kJoinIn)); advance(kJoinMs);
        ASSERT_EQ(sink(k).declared,kAdvertise);
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,k,nullptr,nullptr,0)); settle(); advance(kJoinMs);
        expect_bound_declares(k,k,kAdvertise,"UNBIND_RX then BIND_RX declares at once");
    }
}

}
