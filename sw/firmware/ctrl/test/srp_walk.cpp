// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "srp_fixture.hpp"
#include "pp_srp_reuse.inc"
FW_TALLY_LABEL("ctrl SRP processor wire differential");
namespace {
namespace P=processor_wire;
class SrpWalk : public Srp {
protected:
    void input(const std::vector<P::Msg> &messages,unsigned i=0,bool msrp=true) {
        offer(P::mrpdu_frame(msrp,messages),i);
    }
    void expect_listener(unsigned subtype,unsigned event) {
        capture(); bool found=false;
        for(const auto &d:declarations) if(d.ethertype==0x22ea && d.type==3 &&
            d.subtype==subtype && d.event==event) found=true;
        EXPECT_TRUE(found)<<"processor wire stimulus produced the required Listener message";
    }
};
TEST_F(SrpWalk, CertifiedTwoClassDomainVectorAdoptsOnlyClassA) {
    // srp_top check_certified_domain_arrival_adopts_and_redeclares: the
    // switch's two-value {5,2,VID} vector, not a firmware-built attribute.
    settle(); input({P::Msg{4,4,false,{P::Vec{false,2,P::fv_domain(5,2,3),{1,1},{}}}}});
    advance(200); capture();
    EXPECT_EQ(adapter.ifs[0].domain.class_id,6u); EXPECT_EQ(adapter.ifs[0].domain.priority,3u);
    EXPECT_EQ(adapter.ifs[0].domain.vid,3u);
    bool seen=false;
    for(const auto &d:declarations) if(d.ethertype==0x22ea && d.type==4 &&
        d.value==std::vector<uint8_t>({6,3,0,3})) seen=true;
    EXPECT_TRUE(seen)<<"adopted Domain is re-declared on the wire";
}
TEST_F(SrpWalk, StreamMatcherNearMissSwapAndImmediateWithdrawal) {
    // srp_stream_fsms section E, including 35.2.6's in-place type swap.
    const uint64_t sid=0x02AABBCCDDEE0001ull; const uint64_t da=0x91E0F0001234ull;
    msrp_stream_id id{}; uint8_t dest[6]; wire_put_be(id.bytes,sid,8); wire_put_be(dest,da,6);
    settle(); ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&id,dest,2));
    for(unsigned miss=0;miss<3;++miss) {
        input({P::Msg{1,25,false,{P::Vec{false,1,P::fv_talker(sid+(miss==0),da+(miss==1),2+(miss==2),217,1,3,1,111),{3},{}}}}});
        EXPECT_EQ(adapter.ifs[0].sinks[0].declared,0u);
    }
    input({P::Msg{1,25,false,{P::Vec{false,1,P::fv_talker(sid,da,2,217,1,3,1,777),{0},{}}}}});
    advance(200); expect_listener(2,0);
    input({P::Msg{2,34,false,{P::Vec{false,1,P::fv_failed(sid,da,2,217,1,3,1,999,0xBBBB0000CCCCull,7),{1},{}}}}});
    advance(200); EXPECT_EQ(adapter.ifs[0].sinks[0].declared,1u); expect_listener(1,0);
    input({P::Msg{1,25,false,{P::Vec{false,1,P::fv_talker(sid,da,2,217,1,3,1,555),{3},{}}}}});
    advance(200); EXPECT_EQ(adapter.ifs[0].sinks[0].declared,2u); expect_listener(2,0);
    input({P::Msg{1,25,false,{P::Vec{false,1,P::fv_talker(sid,da,2,217,1,3,1,555),{5},{}}}}});
    // Milan 4.2.7.2.2 replaces IN/rLv with immediate MT for MSRP.
    EXPECT_EQ(adapter.ifs[0].sinks[0].declared,0u);
    advance(200); EXPECT_EQ(adapter.ifs[0].sinks[0].declared,0u); expect_listener(2,5); // D2: retain Ready; Ignore=0 would discard this Lv.
}
TEST_F(SrpWalk, RunBLeaveAllLanesPreserveTheRedeclaredListener) {
    // srp_stream_fsms I/J/K and srp_top's switch vector shape (#608/#134).
    settle(); const uint64_t sid=wire_be64(identity().data());
    EXPECT_CALL(licence,Change(0,0,true));
    input({P::Msg{3,8,true,{P::Vec{false,1,P::fv_sid(sid),{3},{2}}}}});
    input({P::Msg{3,8,true,{P::Vec{true,1,P::fv_sid(sid),{3},{2}}}},
           P::Msg{4,4,false,{P::Vec{true,2,P::fv_domain(5,2,2),{3,3},{}}}},
           P::la_only(1,25,false),P::la_only(2,34,false)});
    advance(5000); EXPECT_TRUE(adapter.ifs[0].active[0]);
    input({P::la_only(4,4,false)}); advance(5000); EXPECT_TRUE(adapter.ifs[0].active[0]);
    input({P::la_only(3,8,true)}); advance(2000);
    input({P::Msg{3,8,true,{P::Vec{false,1,P::fv_sid(sid),{5},{2}}}}});
    advance(2990); EXPECT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false)); advance(10); EXPECT_FALSE(adapter.ifs[0].active[0]);
}
TEST_F(SrpWalk, ProcessorApplicantTransmitAndReceivedRowsAgreeOnTheWire) {
    settle(); advance(400); capture();
    int state=P::VN;
    for(unsigned n=0;n<3;++n) {
        const int event=P::app_msg(state,false,false);
        for(unsigned i=0;i<MBX_N_IF;++i) {
            bool seen=false;
            for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea &&
                d.type==1 && d.time_ms==n*200) {
                EXPECT_EQ(d.event,unsigned(event)); seen=true;
            }
            EXPECT_TRUE(seen);
        }
        state=P::app_next(state,P::eTx,false,true);
    }
    EXPECT_EQ(state,P::QA);
    // QA + rJoinMt becomes AA and must request an opportunity within JoinTime.
    auto &source=sources[0][0].value;
    input({P::Msg{1,25,false,{P::Vec{false,1,
        P::fv_talker(wire_be64(source.stream_id.bytes),0x91e0f0000000ull,2,224,1,3,0,0),{3},{}}}}});
    // The end-station interest policy intentionally ignores a peer Talker
    // for an unbound sink; test the same applicant row through Domain.
    input({P::Msg{4,4,false,{P::Vec{false,1,P::fv_domain(6,3,2),{3},{}}}}});
    advance(200); capture(); bool domain_join=false;
    for(const auto &d:declarations) if(d.type==4 && d.ethertype==0x22ea && d.time_ms==600) {
        EXPECT_EQ(d.event,unsigned(P::app_msg(P::app_next(P::QA,P::eRJoinMt,false,true),false,true)));
        domain_join=true;
    }
    EXPECT_TRUE(domain_join)<<"received event requests a bounded transmit opportunity";
}
TEST_F(SrpWalk, PerInterfaceWireIdentityAndUnknownOrTruncatedInput) {
    settle();
    for(unsigned i=0;i<MBX_N_IF;++i) {
        auto sid=wire_be64(identity(i).data());
        EXPECT_CALL(licence,Change(i,0,true));
        input({P::Msg{3,8,true,{P::Vec{false,1,P::fv_sid(sid),{0},{3}}}}},i);
        auto invalid=P::mrpdu_frame(true,{P::Msg{3,8,true,{P::Vec{false,1,P::fv_sid(sid),{5},{3}}}}});
        invalid.resize(invalid.size()-5); offer(invalid,i);
        EXPECT_TRUE(adapter.ifs[i].active[0]);
    }
    EXPECT_EQ(adapter.malformed,MBX_N_IF);
    for(unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_CALL(licence,Change(i,0,false)); mbx_model_set_link(&model,i,false); settle();
    }
}
}
