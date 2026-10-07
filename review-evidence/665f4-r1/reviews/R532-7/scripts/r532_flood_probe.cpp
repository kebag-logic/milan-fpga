// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R532-6): the R532-5 wire-only Domain flood (60 separate frames,
// one Class A Domain value each), then a Listener Lv. How long until revocation,
// and is a record retained? Mock cardinality is left open (Domain changes toggle
// the licence); only the observable state is asserted.
#include "srp_fixture.hpp"
FW_TALLY_LABEL("R532-6 flood probe");
using ::testing::AnyNumber;
namespace {
TEST_F(Srp, FloodThenListenerLeaveRevocationTime) {
    auto pump=[&](unsigned ms) { for(unsigned k=0;k<ms;++k) { mbx_model_advance_ms(&model,1);
        for(unsigned n=0;n<20;++n) ctrl_loop_service(&loop); } };
    auto push=[&](const std::vector<uint8_t> &f) { for(unsigned tries=0;tries<200;++tries) {
        if(mbx_model_rx(&model,f.data(),f.size(),0)) { pump(2); return true; } pump(1); } return false; };
    EXPECT_CALL(licence,Change(0,0,::testing::_)).Times(AnyNumber());
    settle();
    offer(frame(3,identity(),1,2));
    ASSERT_TRUE(adapter.ifs[0].active[0]);
    unsigned pushed=0;
    for(unsigned v=3;v<63;++v) pushed+=push(frame(4,{6,3,uint8_t(v>>8),uint8_t(v)},1));
    pump(1500);
    std::printf("PROBE flood pushed=%u pending=%u refused=%u received=%u active=%d pool_in_use=%u\n",pushed,
                (unsigned)adapter.pending_rx.len,adapter.refused,adapter.received,(int)adapter.ifs[0].active[0],
                (unsigned)ctrl_pool_in_use(&pool));
    const unsigned received=adapter.received;
    ASSERT_TRUE(push(frame(3,identity(),5,2)));
    unsigned waited=0;
    while(adapter.ifs[0].active[0] && waited<60000) { pump(100); waited+=100; }
    std::printf("PROBE flood lv revoked_after_ms=%u active=%d pending=%u received+%u malformed=%u pool_in_use=%u\n",
                waited,(int)adapter.ifs[0].active[0],(unsigned)adapter.pending_rx.len,adapter.received-received,
                adapter.malformed,(unsigned)ctrl_pool_in_use(&pool));
    EXPECT_LT(waited,1000u) << "Listener Lv must revoke within the rapid-leave pass budget";
}
}
