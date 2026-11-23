// #973: an UP elided while the ring is full must not authorize a later UP.
// Append to the committed phase suite so its fixture and reset counter are reused.
namespace {
TEST_F(SrpLinkPass, AnElidedUpDoesNotAuthorizeAFreshUpInsideAPass) {
    srp_interface &i = adapter.ifs[0];
    mrp_app *const startup = i.msrp;
    ASSERT_NE(startup, nullptr);
    for (uint16_t type : {uint16_t{MBX_CTRCHG_STREAM_INPUT_TYPE}, uint16_t{MBX_CTRCHG_STREAM_OUTPUT_TYPE}}) {
        for (uint16_t n = 0; n < 16u; ++n) {
            mbx_model_face_event(&model, 0, MBX_MODEL_EV_COUNTERS, type, n);
        }
    }
    move_at(Phase::AfterTheEvents, true);
    ASSERT_TRUE(loop.events_left);
    ASSERT_FALSE(model.posted_up[0]);
    ASSERT_FALSE(i.link_seen);
    ASSERT_FALSE(i.link);
    // The first UP has no space to post; DOWN elides it before a take frees space.
    mbx_model_set_link(&model, 0, false);
    settle();
    ASSERT_FALSE(model.posted_up[0]);
    ASSERT_FALSE(loop.events_left);
    ASSERT_FALSE(i.link_seen);
    ASSERT_EQ(resets, 0u);
    ASSERT_EQ(i.msrp, startup);
    // This is the first UP record the fabric actually owes and dispatches.
    EXPECT_EQ(up_at(Phase::AfterTheEvents), 0u) << "the first dispatched UP must keep startup participants";
    EXPECT_EQ(i.msrp, startup);
}
}
