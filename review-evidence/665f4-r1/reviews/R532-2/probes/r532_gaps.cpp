// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer R532-2 discriminators for planted defects the lane suite misses.
#include "srp_fixture.hpp"
FW_TALLY_LABEL("R532 SRP gap probes");
namespace {
std::vector<uint8_t> talker_value(const msrp_stream_id &sid, const uint8_t da[6], uint16_t vid) {
    std::vector<uint8_t> t(25); std::copy(sid.bytes,sid.bytes+8,t.begin());
    std::copy(da,da+6,t.begin()+8); wire_put_be(t.data()+14,vid,2);
    wire_put_be(t.data()+16,224,2); wire_put_be(t.data()+18,1,2); t[20]=0x60; return t;
}
// G1 (kills L1): a peer Domain whose adoption was refused by exhaustion must
// not be adopted after a link restart (R533-1-F2: no stale Domain).
TEST_F(Srp, G1_RefusedPeerDomainDoesNotSurviveLinkRestart) {
    settle(); advance(400);
    std::vector<void*> held; while(void *p=ctrl_pool_alloc(&pool,1)) held.push_back(p);
    ASSERT_GE(held.size(),2u); ctrl_pool_free(&pool,held.back()); held.pop_back();
    auto f=frame(4,{6,4,0,3},0);
    ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),0)); ctrl_loop_service(&loop);
    ASSERT_TRUE(adapter.ifs[0].domain_owed);
    for(void *p:held) ctrl_pool_free(&pool,p);
    mbx_model_set_link(&model,0,false); mbx_model_set_link(&model,0,true); settle(); advance(400);
    EXPECT_EQ(adapter.ifs[0].domain.vid,2u) << "old link's peer Domain adopted after restart";
    EXPECT_EQ(adapter.ifs[0].domain.priority,3u);
}
// G2 (kills L3): a bound sink on a non-Domain VID re-declares that VLAN on the
// new link before its Listener Ready (Milan 4.3.2; 802.1Q 35.1.2.2).
TEST_F(Srp, G2_SinkVlanRedeclaredBeforeReadyAfterLinkRestart) {
    settle(); advance(400);
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,7));
    offer(frame(1,talker_value(sid,da,7),1)); advance(400);
    ASSERT_EQ(adapter.ifs[0].sinks[0].declared,2u);
    mbx_model_set_link(&model,0,false); mbx_model_set_link(&model,0,true); settle();
    capture(); const size_t base=declarations.size();   // wire order: everything before the new link's input
    offer(frame(1,talker_value(sid,da,7),1)); advance(400);
    capture();
    int vlan_at=-1, ready_at=-1;
    for(size_t n=base;n<declarations.size();++n) {
        const auto &d=declarations[n];
        if(d.interface!=0) continue;
        if(d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,7}) && (d.event==1||d.event==3) && vlan_at<0) vlan_at=(int)n;
        if(d.ethertype==0x22ea && d.type==3 && d.subtype==2 && ready_at<0) ready_at=(int)n;
    }
    EXPECT_GE(ready_at,0) << "Listener Ready never re-declared on the new link";
    EXPECT_GE(vlan_at,0) << "VID 7 never re-declared on the new link";
    if(vlan_at>=0 && ready_at>=0) { EXPECT_LT(vlan_at,ready_at) << "Ready precedes the VLAN Join on the new link"; }
}
// G3 (kills S2): a shared StreamID whose matching binding is on another VID
// waits for that binding's own VLAN commit, not the first binding's.
TEST_F(Srp, G3_SharedIdentityReadyWaitsForTheMatchingBindingsVlan) {
    settle(); advance(400);
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    uint8_t da0[]={0x91,0xe0,0xf0,0,0,8}, da1[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da0,2));
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,&sid,da1,7));
    advance(1200); ASSERT_TRUE(adapter.ifs[0].sinks[0].vlan_sent);
    capture(); const size_t base=declarations.size();
    offer(frame(1,talker_value(sid,da1,7),1)); advance(400);
    capture();
    int vlan_at=-1, ready_at=-1;
    for(size_t n=base;n<declarations.size();++n) {
        const auto &d=declarations[n];
        if(d.interface!=0) continue;
        if(d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,7}) && (d.event==1||d.event==3) && vlan_at<0) vlan_at=(int)n;
        if(d.ethertype==0x22ea && d.type==3 && d.subtype==2 && ready_at<0) ready_at=(int)n;
    }
    ASSERT_GE(ready_at,0); ASSERT_GE(vlan_at,0);
    EXPECT_LT(vlan_at,ready_at) << "Ready for VID 7 binding precedes its VLAN Join";
}
// G4 (kills L2 if not equivalent): after a restart the bound sink's Listener
// Ready is declared again once the Talker registers on the new link.
TEST_F(Srp, G4_ListenerRedeclaredOnNewLink) {
    settle(); advance(400);
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
    offer(frame(1,talker_value(sid,da,2),1)); advance(400);
    ASSERT_EQ(adapter.ifs[0].sinks[0].declared,2u);
    mbx_model_set_link(&model,0,false); mbx_model_set_link(&model,0,true); settle();
    const unsigned start=model.now_ms;
    offer(frame(1,talker_value(sid,da,2),1)); advance(1200); capture();
    bool ready=false;
    for(const auto &d:declarations) if(d.interface==0 && d.time_ms>=start && d.ethertype==0x22ea && d.type==3 && d.subtype==2 && d.event!=5) ready=true;
    EXPECT_TRUE(ready);
}
}
