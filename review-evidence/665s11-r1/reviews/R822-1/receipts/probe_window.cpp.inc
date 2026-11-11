
// ---- REVIEW PROBE (disposable; appended to test_plat_boot.cpp, then removed) ----
// Between the REBOOT's SUCCESS leaving the mailbox and the reset port's write,
// is an ACMP command taken, and does any non-ADP frame follow ENTITY_DEPARTING?
namespace {
TEST_F(Boot, ProbeAcmpBindBetweenSuccessAndPort) {
    env.reboot = kReboot;
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    for (unsigned k = 0; k < 50; ++k) pass_ms();
    const std::size_t from = frames.size();
    mbx_model_tx_pause(&fabric, true);
    aem(42, entity0(), kCtl, kCtlMac);
    for (unsigned k = 0; k < 50; ++k) pass_ms();
    // release the response; the mailbox then stops at ADP's next commit (its ENTITY_DEPARTING)
    hold_adp = true;
    mbx_model_tx_pause(&fabric, false);
    take_frames();
    for (unsigned k = 0; k < 50; ++k) pass_ms();
    ASSERT_EQ(aecp_frames(from, 42).size(), 1u) << "PROBE the SUCCESS has left";
    ASSERT_FALSE(hold_adp) << "PROBE the mailbox holds ENTITY_DEPARTING";
    ASSERT_TRUE(reboot_writes().empty()) << "PROBE the window: SUCCESS left, port not yet written";
    acmp_test::Pdu bind;
    bind.msg = spec::MSG_BIND_RX_COMMAND;
    bind.controller = acmp_test::kCtl1;
    bind.talker = acmp_test::kTkA;
    bind.listener = ctrl_plat.config.entity->entity_id;
    const auto frame = acmp_test::acmpdu(bind);
    ASSERT_TRUE(mbx_model_rx(&fabric, frame.data(), frame.size(), 0));
    for (unsigned k = 0; k < 50; ++k) pass_ms();
    acmp_sink_view sink{};
    ASSERT_TRUE(acmp_view(&ctrl_plat.app.acmp.acmp, 0, &sink));
    std::printf("PROBE sink.bound after a BIND_RX in the window: %d\n", sink.bound ? 1 : 0);
    mbx_model_tx_pause(&fabric, false);
    take_frames();
    for (unsigned k = 0; k < 500 && reboot_writes().empty(); ++k) pass_ms();
    const auto gone = departing(from);
    const auto writes = reboot_writes();
    std::size_t acmp_after_departing = 0, acmp_any = 0;
    for (std::size_t k = from; k < frames.size(); ++k) {
        if (frames[k].frame.channel != MBX_CH_ACMP) continue;
        ++acmp_any;
        if (!gone.empty() && frames[k].plat >= gone[0]->plat) ++acmp_after_departing;
    }
    std::printf("PROBE departing=%zu writes=%zu acmp_frames=%zu acmp_frames_at_or_after_first_departing=%zu\n",
                gone.size(), writes.size(), acmp_any, acmp_after_departing);
    for (std::size_t k = from; k < frames.size(); ++k) {
        std::printf("PROBE frame %zu channel %u plat %zu%s\n", k, static_cast<unsigned>(frames[k].frame.channel),
                    frames[k].plat, (!writes.empty() && frames[k].plat > writes[0]) ? " (after the port)" : "");
    }
    if (!writes.empty()) std::printf("PROBE port written at plat %zu\n", writes[0]);
    EXPECT_FALSE(sink.bound) << "PROBE a BIND_RX after the REBOOT's SUCCESS is not taken";
    EXPECT_EQ(acmp_any, 0u) << "PROBE a BIND_RX after the REBOOT's SUCCESS is not answered";
}
}  // namespace
