// Reviewer probe (R532-1): disposable; not part of the PR.
#include "srp_fixture.hpp"
FW_TALLY_LABEL("R532 probe");
namespace {
using ::testing::_;
// Milan v1.2 4.2.7.2.2: for MSRP, IN / rLv! -> (Lv) -> MT immediately.
TEST_F(Srp, R532MilanListenerLeaveFromInStopsTalkerPromptly) {
    settle();
    EXPECT_CALL(licence,Change(0,0,true));
    offer(frame(3,identity(),1,2));          // rJoinIn Ready -> registrar IN
    advance(500);
    ASSERT_TRUE(adapter.ifs[0].active[0]);
    EXPECT_CALL(licence,Change(0,0,false));
    offer(frame(3,identity(),5,2));          // rLv while IN (no LeaveAll)
    unsigned ms=0;
    while (adapter.ifs[0].active[0] && ms<8000) { advance(10); ms+=10; }
    std::printf("R532 talker licence revoked %u ms after Listener Lv from IN\n", ms);
    EXPECT_LE(ms,10u) << "Milan 4.2.7.2.2 requires IN/rLv! -> MT without LeaveTime";
}
TEST_F(Srp, R532MilanTalkerLeaveFromInWithdrawsListenerPromptly) {
    settle();
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const uint8_t da[]={0x91,0xe0,0xf0,0,0,9};
    ASSERT_TRUE(srp_mbx_bind(&adapter,0,0,&sid,da,2));
    std::vector<uint8_t> talker(25);
    std::copy(sid.bytes,sid.bytes+8,talker.begin());
    std::copy(da,da+6,talker.begin()+8);
    wire_put_be(talker.data()+14,2,2);
    wire_put_be(talker.data()+16,224,2); wire_put_be(talker.data()+18,1,2); talker[20]=0x60;
    offer(frame(1,talker,1));               // rJoinIn Talker Advertise
    advance(500);
    ASSERT_EQ(adapter.ifs[0].sinks[0].declared,2u);
    offer(frame(1,talker,5));               // rLv while IN
    unsigned ms=0;
    while (adapter.ifs[0].sinks[0].declared!=0 && ms<8000) { advance(10); ms+=10; }
    std::printf("R532 listener declaration withdrawn %u ms after Talker Lv from IN\n", ms);
    EXPECT_LE(ms,10u) << "Milan 4.2.7.2.2 requires IN/rLv! -> MT without LeaveTime";
}
}
