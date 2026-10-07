// Reviewer probe (not part of the candidate): Listener withdrawal while the SRP
// pool is exhausted. Run unchanged against the old and new lwSRP pins.
#include "srp_fixture.hpp"
FW_TALLY_LABEL("reviewer exhaustion probe");
using ::testing::AtMost;
#ifndef FLOOD
#define FLOOD 60u
#endif
namespace {
struct Held {
    ctrl_pool *pool; std::vector<void*> blocks;
    explicit Held(ctrl_pool *p): pool(p) { while(void *b=ctrl_pool_alloc(pool,1)) blocks.push_back(b); }
    void release() { for(void *b:blocks) ctrl_pool_free(pool,b); blocks.clear(); }
    ~Held() { release(); }
};
TEST_F(Srp, ProbeRapidListenerLeaveWhilePoolExhausted) {
    settle();
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),1,2));
    ASSERT_TRUE(adapter.ifs[0].active[0]);
    Held held(&pool);
    const unsigned malformed=adapter.malformed, received=adapter.received;
    EXPECT_CALL(licence,Change(0,0,false)).Times(AtMost(1));
    offer(frame(3,identity(),5,2));                      // peer Listener Lv (Milan rapid leave)
    advance(100);
    std::printf("PROBE rapid-leave held=%zu malformed+%u received+%u active_after_lv=%d\n",
                held.blocks.size(),adapter.malformed-malformed,adapter.received-received,
                (int)adapter.ifs[0].active[0]);
    EXPECT_FALSE(adapter.ifs[0].active[0]) << "Listener Lv must revoke the Talker licence";
    held.release();
    unsigned waited=0;
    while(adapter.ifs[0].active[0] && waited<40000) { advance(100); waited+=100; }
    std::printf("PROBE rapid-leave after-release active=%d revoked_after_ms=%u\n",
                (int)adapter.ifs[0].active[0],waited);
    EXPECT_CALL(licence,Change(0,0,false)).Times(AtMost(1));
    mbx_model_set_link(&model,0,false); settle();
}
TEST_F(Srp, ProbeLeaveTimeDeadlineWhilePoolExhausted) {
    settle();
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),1,2));
    offer(frame(3,identity(),4,2,true));                 // peer LeaveAll: Registrar enters LV
    Held held(&pool);
    EXPECT_CALL(licence,Change(0,0,false)).Times(AtMost(1));
    advance(5100);                                        // past the original 5 s LeaveTime
    std::printf("PROBE leavetime held=%zu active_after_deadline=%d stops=%u\n",
                held.blocks.size(),(int)adapter.ifs[0].active[0],adapter.stops);
    EXPECT_FALSE(adapter.ifs[0].active[0]) << "LeaveTime expiry must revoke the Talker licence";
    held.release();
    advance(200);
    std::printf("PROBE leavetime after-release active=%d\n",(int)adapter.ifs[0].active[0]);
    mbx_model_set_link(&model,0,false); settle();
}
TEST_F(Srp, ProbeDomainFloodThenRapidListenerLeave) {
    // Wire-only: the peer registers many Class A Domain values (the receive
    // filter admits every class-6 VID), then withdraws its Ready Listener.
    // Bounded pumping replaces settle(): refused retries keep the loop busy.
    auto pump=[&](unsigned ms) { for(unsigned k=0;k<ms;++k) { mbx_model_advance_ms(&model,1);
        for(unsigned n=0;n<20;++n) ctrl_loop_service(&loop); } };
    auto push=[&](const std::vector<uint8_t> &f) { for(unsigned tries=0;tries<200;++tries) {
        if(mbx_model_rx(&model,f.data(),f.size(),0)) { pump(2); return true; } pump(1); } return false; };
    settle();
    EXPECT_CALL(licence,Change(0,0,true)); offer(frame(3,identity(),1,2));
    ASSERT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false)).Times(AtMost(1));
    EXPECT_CALL(licence,Change(0,0,true)).Times(AtMost(1));
    const unsigned refused_before=adapter.refused;
    unsigned pushed=0;
    for(unsigned v=3;v<3+FLOOD;++v) pushed+=push(frame(4,{6,3,uint8_t(v>>8),uint8_t(v)},1));
    pump(1500);   // the final Domain VID's MVRP Join commits; Ready re-enables the licence
    const unsigned malformed=adapter.malformed;
    std::printf("PROBE flood values=%u pushed=%u pool_refused=%u adapter_refused+%u domain_vid=%u active_before_lv=%d\n",
                (unsigned)FLOOD,pushed,(unsigned)pool.refused,adapter.refused-refused_before,
                (unsigned)adapter.ifs[0].domain.vid,(int)adapter.ifs[0].active[0]);
    const bool lv_pushed=push(frame(3,identity(),5,2)); pump(100);
    std::printf("PROBE flood lv_pushed=%d malformed+%u active_after_lv=%d\n",(int)lv_pushed,
                adapter.malformed-malformed,(int)adapter.ifs[0].active[0]);
    EXPECT_FALSE(adapter.ifs[0].active[0]) << "Listener Lv must revoke the Talker licence";
    pump(3000);
    std::printf("PROBE flood +3s active=%d\n",(int)adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false)).Times(AtMost(1));
    mbx_model_set_link(&model,0,false); pump(10);
}
} // namespace
