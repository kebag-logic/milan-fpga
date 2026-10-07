// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer R532-2 probes against the exact head; uses the lane's fixture.
#include "srp_fixture.hpp"
FW_TALLY_LABEL("R532 SRP probes");
namespace {
std::vector<uint8_t> talker_value(const msrp_stream_id &sid, const uint8_t da[6], uint16_t vid) {
    std::vector<uint8_t> t(25); std::copy(sid.bytes,sid.bytes+8,t.begin());
    std::copy(da,da+6,t.begin()+8); wire_put_be(t.data()+14,vid,2);
    wire_put_be(t.data()+16,224,2); wire_put_be(t.data()+18,1,2); t[20]=0x60; return t;
}
// P1: the documented destroy/re-init path while the physical link is
// already up. The fabric posts LINK only on a level change, so no record
// follows; Milan 5.5.2.7 still requires the Talker declaration.
TEST_F(Srp, P1_ReinitWithLinkAlreadyUpStillDeclares) {
    settle(); advance(400);
    ASSERT_TRUE(mbx_link_up(0));
    srp_mbx_destroy(&adapter);
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ctrl_loop_init(&loop);
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    ASSERT_TRUE(ctrl_loop_open(&loop,0x020304fffe050600ull,config.mac));
    const unsigned before=adapter.transmitted;
    advance(1500);
    EXPECT_GT(adapter.transmitted,before) << "no Talker/Domain/VLAN declaration after re-init with link up";
    EXPECT_TRUE(adapter.ifs[0].link);
}
// P2: link level drops while the event record is held (full ring), then
// returns before the fabric posts; the coalesced source posts nothing.
TEST_F(Srp, P2_LevelLossThenLevelReturnWithoutRecordRecovers) {
    settle(); advance(400);
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),1,2));
    EXPECT_CALL(licence,Change(0,0,false)).Times(::testing::Between(1,2)); // loss, and teardown if re-licensed
    model.link_up[0]=false; ctrl_loop_service(&loop);
    ASSERT_FALSE(adapter.ifs[0].link);
    model.link_up[0]=true;
    advance(1500);
    const unsigned before=adapter.transmitted;
    advance(1500);
    EXPECT_GT(adapter.transmitted,before) << "interface 0 never resumes MRP transmission";
    EXPECT_TRUE(adapter.ifs[0].link);
    // A fresh peer Listener Ready can no longer register either.
    EXPECT_CALL(licence,Change(0,0,true)).Times(::testing::AtMost(1));
    offer(frame(3,identity(),1,2));
    EXPECT_TRUE(adapter.ifs[0].registered[0]) << "receive is dropped while i->link stays false";
}
// P3: two bindings on one VID; only the first was eligible and requested
// the VLAN. Unbinding it first, then the never-requesting one, must still
// withdraw the VID that no binding needs any more.
TEST_F(Srp, P3_SharedVidWithdrawnAfterBothUnbindsInEitherOrder) {
    settle(); advance(400);
    msrp_stream_id a{{2,1,2,3,4,5,6,7}}, b{{2,1,2,3,4,5,6,8}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&a,da,7)); offer(frame(1,talker_value(a,da,7),0)); advance(400);
    ASSERT_TRUE(adapter.ifs[0].sinks[0].vlan_requested);
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,&b,da,7)); settle(); // no Talker for b: never eligible
    ASSERT_FALSE(adapter.ifs[0].sinks[1].vlan_requested);
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0)); advance(200);
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,nullptr,nullptr,0));
    const unsigned start=model.now_ms; advance(3000); capture();
    bool left=false, still_joined=false;
    for(const auto &d:declarations) if(d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,7}) && d.time_ms>=start) {
        left|=d.event==5; still_joined|=d.event==1 || d.event==3;
    }
    EXPECT_TRUE(left) << "VID 7 is never withdrawn";
    EXPECT_FALSE(still_joined && !left) << "VID 7 is still declared with no binding";
}
// P4: Milan applies only IN/rLv; a Talker Leave in LV (after LeaveAll)
// keeps the original LeaveTime deadline, so the Listener withdraws at 5 s.
TEST_F(Srp, P4_TalkerLeaveInLvKeepsOriginalDeadline) {
    settle(); advance(400);
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
    offer(frame(1,talker_value(sid,da,2),1)); advance(400);
    ASSERT_EQ(adapter.ifs[0].sinks[0].declared,2u);
    offer(frame(1,talker_value(sid,da,2),4,0,true));   // rLA: IN -> LV, timer starts
    advance(2000);
    offer(frame(1,talker_value(sid,da,2),5));          // rLv in LV: no restart, no immediate MT
    EXPECT_EQ(adapter.ifs[0].sinks[0].declared,2u) << "LV/rLv must not withdraw immediately";
    advance(2900);
    EXPECT_EQ(adapter.ifs[0].sinks[0].declared,2u);
    advance(200);
    EXPECT_EQ(adapter.ifs[0].sinks[0].declared,0u) << "original deadline must expire at 5 s";
}
// P5: MVRP keeps Table 10-4: a peer VLAN Lv in IN enters LV (aging), not MT,
// while an MSRP Domain Lv in IN enters MT at once (Milan 4.2.7.2.2).
int reg_of(mrp_app *app, uint8_t type, const std::vector<uint8_t> &val) {
    struct C { uint8_t type; std::vector<uint8_t> val; size_t len; int reg; } c{type,val,val.size(),-1};
    mrp_attr_visit(app,0,[](void *ctx,const mrp_attr_status *st){
        auto *c=static_cast<C*>(ctx);
        if(st->attr_type==c->type && std::memcmp(st->attr_val,c->val.data(),c->len)==0) c->reg=st->reg;
    },&c);
    return c.reg;
}
TEST_F(Srp, P5_MvrpLeaveInInAgesButMsrpLeaveIsImmediate) {
    settle(); advance(400);
    std::vector<uint8_t> v(26); wire_put_be(v.data(),0x0180c2000021ull,6); wire_put_be(v.data()+12,0x88f5,2);
    uint8_t join[]={0,1,2,0,1,0,2,1*36,0,0,0,0}; std::copy(join,join+12,v.begin()+14); offer(v);
    ASSERT_EQ(reg_of(adapter.ifs[0].mvrp,1,{0,2}),(int)MRP_REG_STATE_IN);
    uint8_t lv[]={0,1,2,0,1,0,2,5*36,0,0,0,0}; std::copy(lv,lv+12,v.begin()+14); offer(v);
    EXPECT_EQ(reg_of(adapter.ifs[0].mvrp,1,{0,2}),(int)MRP_REG_STATE_LV) << "MVRP must keep Table 10-4 aging";
    offer(frame(4,{6,3,0,2},1));
    ASSERT_EQ(reg_of(adapter.ifs[0].msrp,4,{6,3,2,0}),(int)MRP_REG_STATE_IN);
    offer(frame(4,{6,3,0,2},5));
    const int r=reg_of(adapter.ifs[0].msrp,4,{6,3,2,0});
    EXPECT_TRUE(r==(int)MRP_REG_STATE_MT || r==-1) << "MSRP IN/rLv must enter MT at once, got " << r;
}
}
