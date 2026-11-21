// Independent regression probe: registration after participant recreation.
TEST_F(Talker, RegistrationAfterLinkResetIsNoticed) {
    EXPECT_CALL(licence,Change(::testing::_,::testing::_,::testing::_)).Times(::testing::AnyNumber());
    settle(); gate(1u,kBaseA); advance(400);
    const unsigned i=MBX_N_IF-1u;
    offer(frame(3,identity(i,0),1,2),i); advance(20);
    ASSERT_TRUE(adapter.ifs[i].listener_present[0]);
    ASSERT_EQ(adapter.ifs[i].declaration[0],2u);
    // A closed gate and a link reset need no Listener notice. After recovery
    // the first Ready is a new registration, even if its value matches the old.
    gate(0u,kBaseA); settle();
    mbx_model_set_link(&model,i,false); settle();
    mbx_model_set_link(&model,i,true); settle(); advance(400);
    gate(1u,kBaseA); advance(400);
    ASSERT_FALSE(adapter.ifs[i].listener_present[0]);
    ASSERT_NE(adapter.ifs[i].gate&1u,0u);
    adapter.ifs[i].noticed=0u;
    offer(frame(3,identity(i,0),1,2),i); advance(20);
    ASSERT_TRUE(adapter.ifs[i].listener_present[0]);
    EXPECT_EQ(adapter.ifs[i].noticed&1u,1u)
        << "new Listener registration after link reset must be noticed";
}
