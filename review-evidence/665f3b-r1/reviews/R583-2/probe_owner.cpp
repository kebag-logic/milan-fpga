TEST_F(AcmpMailbox, R583SourceOwnerInvalidityClosesThePublishedGate) {
    mbx_model_reset(&model);
    for (unsigned interface = 0; interface < MBX_N_IF; ++interface)
        mbx_model_set_link(&model, interface, true);
    const ctrl_app_config cfg = three_way();
    ASSERT_TRUE(ctrl_app_start(&app, &cfg));
    for (unsigned ms = 0; ms < 2200u; ++ms) {
        mbx_model_advance_ms(&model, 1u);
        settle();
    }
    ASSERT_TRUE(app.maap.ifs[0].core.valid);
    // Drive the documented source port: a live MAAP range does not override
    // the source owner's per-stream destination-valid flag.
    fk.source[0].dest_mac_valid = false;
    ASSERT_TRUE(acmp_listener_registered(core(), 0u, 0u, true));
    settle();
    mbx_model_pub view{};
    mbx_model_pub_view(&model, 0u, &view);
    const bool core_gate = acmp_declaring(core(), 0u);
    std::printf("R583 MAAP valid=%u source DA valid=%u Listener=%u core predicate=%u DA_GATE=%u\n",
                app.maap.ifs[0].core.valid, fk.source[0].dest_mac_valid,
                core()->sources[0].listener_registered, core_gate, view.da_gate);
    EXPECT_FALSE(core_gate);
    EXPECT_EQ(view.da_gate & 1u, 0u) << "invalid source destination must close published declaration";
    ASSERT_TRUE(acmp_listener_registered(core(), 0u, 0u, false));
    Pdu request;
    request.msg = 0u;
    request.talker = kOwn;
    request.talker_uid = 0u;
    ASSERT_TRUE(offer(request));
    settle();
    ASSERT_TRUE(core()->sources[0].answered);
    mbx_model_pub_view(&model, 0u, &view);
    std::printf("R583 answered probe=%u invalid source DA: core predicate=%u DA_GATE=%u\n",
                core()->sources[0].answered, acmp_declaring(core(), 0u), view.da_gate);
    EXPECT_FALSE(acmp_declaring(core(), 0u));
    EXPECT_EQ(view.da_gate & 1u, 0u) << "answered probe cannot override invalid source destination";
    fk.source[0].dest_mac_valid = true;
    settle();
    mbx_model_pub_view(&model, 0u, &view);
    EXPECT_TRUE(acmp_declaring(core(), 0u));
    EXPECT_EQ(view.da_gate & 1u, 1u) << "valid source destination and Listener must open declaration";
}
