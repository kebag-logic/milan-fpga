// Independent round R533-1 behavior probes. No production edits.
#include "srp_fixture.hpp"
FW_TALLY_LABEL("R533 independent SRP probes");
namespace {
TEST_F(Srp, R533_MilanWithdrawalInINIsImmediate) {
    settle(); EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),0,2));
    ASSERT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false));
    offer(frame(3,identity(),5,2));
    EXPECT_FALSE(adapter.ifs[0].active[0]) << "Milan 4.2.7.2.2: IN plus rLv must stop in this service pass";
    std::printf("R533 IN/rLv active_after_receive=%u time_ms=%u\n",adapter.ifs[0].active[0],model.now_ms);
    if(adapter.ifs[0].active[0]) advance(5000);
    std::printf("R533 IN/rLv active_after_5000ms=%u time_ms=%u\n",adapter.ifs[0].active[0],model.now_ms);
}
TEST_F(Srp, R533_LVWithdrawalKeepsOriginalDeadline) {
    settle(); EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),0,2));
    offer(frame(3,identity(),4,2,true)); advance(2000); offer(frame(3,identity(),5,2));
    advance(2990); EXPECT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false)); advance(10); EXPECT_FALSE(adapter.ifs[0].active[0]);
}
TEST_F(Srp, R533_LinkCycleCannotReuseOldQueuedRegistration) {
    settle();
    auto f=frame(3,identity(),0,2);
    for(unsigned k=0;k<CTRL_LOOP_RX_PER_PASS+1;++k)
        ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),0));
    mbx_model_set_link(&model,0,false); settle();
    EXPECT_FALSE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,true)).Times(0);
    mbx_model_set_link(&model,0,true); settle();
    EXPECT_FALSE(adapter.ifs[0].active[0]) << "Only pre-link-loss Ready frames were offered";
    if(adapter.ifs[0].active[0]) { EXPECT_CALL(licence,Change(0,0,false)); }
}
TEST_F(Srp, R533_LinkPulseResetsDomainFromQueuedEvents) {
    settle(); offer(frame(4,{6,4,0,3},0)); advance(400);
    ASSERT_EQ(adapter.ifs[0].domain.vid,3u);
    mbx_model_set_link(&model,0,false);
    mbx_model_set_link(&model,0,true);
    settle();
    std::printf("R533 link pulse domain_vid=%u priority=%u\n",adapter.ifs[0].domain.vid,adapter.ifs[0].domain.priority);
    EXPECT_EQ(adapter.ifs[0].domain.vid,2u) << "Milan 4.2.7.2.1: link up restores default Domain";
    EXPECT_EQ(adapter.ifs[0].domain.priority,3u);
}
TEST_F(Srp, R533_SharedIdentityRetainsAnEligibleBinding) {
    settle(); advance(400);
    msrp_stream_id sid{{2,1,2,3,4,5,6,7}}; uint8_t da0[]={0x91,0xe0,0xf0,0,0,9};
    uint8_t da1[]={0x91,0xe0,0xf0,0,0,10};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da0,2));
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,1,&sid,da1,2));
    std::vector<uint8_t> t(25); std::copy(sid.bytes,sid.bytes+8,t.begin());
    std::copy(da1,da1+6,t.begin()+8); wire_put_be(t.data()+14,2,2);
    wire_put_be(t.data()+16,224,2); wire_put_be(t.data()+18,1,2); t[20]=0x60;
    offer(frame(1,t,0)); advance(600);
    ASSERT_EQ(adapter.ifs[0].sinks[1].declared,2u);
    const unsigned change_at=model.now_ms;
    std::copy(da0,da0+6,t.begin()+8); offer(frame(1,t,0)); advance(1800); capture();
    EXPECT_EQ(adapter.ifs[0].sinks[0].declared,2u);
    bool withdrew=false; unsigned last_event=99;
    for(const auto& d:declarations) if(d.time_ms>=change_at && d.ethertype==0x22ea && d.type==3 && d.value==std::vector<uint8_t>(sid.bytes,sid.bytes+8)) {
        std::printf("R533 shared SID listener time_ms=%u event=%u subtype=%u\n",d.time_ms,d.event,d.subtype);
        withdrew |= d.event==5; last_event=d.event;
    }
    EXPECT_FALSE(withdrew) << "one matching bound sink still needs Listener Ready";
    EXPECT_NE(last_event,5u) << "No later redeclaration repairs the final Lv";
}
}
