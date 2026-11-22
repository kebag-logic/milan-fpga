// Reviewer probe (#973, not part of the tree): SRP reattached while interface 0's link is momentarily down and its
// DOWN record is held by a full event ring, the level recovering before the record posts, so the fabric owes no LINK
// record (KL_mbx_evt.sv: a record posts only when the level differs from the last one posted). Attach reads DOWN.
// The question: does SRP follow the link that is up, without another LINK record?
#include "srp_fixture.hpp"
FW_TALLY_LABEL("probe reattach with an elided DOWN");
namespace {

TEST_F(Srp, ProbeReattachWhileItsDownRecordIsElided) {
    settle(); advance(400);
    srp_mbx_destroy(&adapter);
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ctrl_loop_init(&loop);
    mbx_model_evt_pause(&model,true);
    model.link_up[0]=false;
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    ASSERT_TRUE(ctrl_loop_open(&loop,0x020304fffe050600ull,config.mac));
    ASSERT_FALSE(adapter.ifs[0].link) << "(attach read the DOWN)";
    model.link_up[0]=true;
    ASSERT_TRUE(model.posted_up[0]) << "(the last posted record is UP: no LINK record is owed)";
    mbx_model_evt_pause(&model,false);
    advance(1500);
    EXPECT_TRUE(adapter.ifs[0].link) << "PROBE: SRP does not follow a link that is up";
    EXPECT_NE(adapter.ifs[0].msrp, nullptr) << "PROBE: the interface has participants";
}

// The same with the link staying down across the reattach and coming up later: a record is owed and SRP follows it.
TEST_F(Srp, ProbeReattachThenALaterUpIsCarried) {
    settle(); advance(400);
    srp_mbx_destroy(&adapter);
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ctrl_loop_init(&loop);
    model.link_up[0]=false;
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    ASSERT_TRUE(ctrl_loop_open(&loop,0x020304fffe050600ull,config.mac));
    advance(100);
    ASSERT_FALSE(adapter.ifs[0].link);
    model.link_up[0]=true;
    advance(1500);
    EXPECT_TRUE(adapter.ifs[0].link) << "PROBE: a later UP is followed";
}

} // namespace
