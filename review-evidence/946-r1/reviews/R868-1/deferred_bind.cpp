// Additional integration probe: an ACMP bind during a deferred format change.
bool observing = false;
unsigned observed_input = 0;
unsigned stale_observations = 0;
void observe_bound_format() {
    if (!observing) return;
    const auto& s = ctrl_plat.app.acmp.acmp.sinks[observed_input];
    if (!s.published_bound || s.published_stream == 0u) return;
    const auto* core = &ctrl_plat.aecp.core;
    for (std::size_t k = 0; k < core->cfg.model->count; ++k) {
        const auto& d = core->cfg.model->descriptors[k];
        if (d.type != kStreamInput || d.index != observed_input || d.configuration != core->configuration)
            continue;
        const auto w = window(0, kOtherSelection);
        const auto current = be(d.value + kFormatAt, 8);
        if (w.holds(observed_input) && current != w.format(observed_input)) {
            if (stale_observations == 0u)
                std::printf("STALE: bound=1 published_sid=%016llx current=%016llx LCTX=%016llx\n",
                            static_cast<unsigned long long>(s.published_stream),
                            static_cast<unsigned long long>(current),
                            static_cast<unsigned long long>(w.format(observed_input)));
            ++stale_observations;
        }
    }
}

TEST_F(Sinks, DeferredFormatMustNotMoveAnAlreadySettledBinding) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    const unsigned n = contexts().back();
    const auto old_format = inputs().at(n).format;
    far.ack = false;
    std::vector<std::uint8_t> payload(12, 0);
    payload[1] = kStreamInput;
    payload[3] = static_cast<std::uint8_t>(n);
    for (unsigned k = 0; k < 8; ++k)
        payload[4+k] = static_cast<std::uint8_t>(kTwoChannels >> (8u * (7u-k)));
    ASSERT_TRUE(send(0x0008u, payload, 0x0501u));
    for (unsigned k = 0; k < 200u && statuses(0x0008u, 0x0501u).empty(); ++k) ctrl_plat_step();
    ASSERT_TRUE(ctrl_plat.aecp.core.waiting);
    ASSERT_EQ(inputs().at(n).format, old_format);

    acmp_test::Pdu bind;
    bind.msg = spec::MSG_BIND_RX_COMMAND;
    bind.controller = acmp_test::kCtl1;
    bind.talker = acmp_test::kTkA;
    bind.listener = ctrl_plat.config.entity->entity_id;
    bind.listener_uid = static_cast<std::uint16_t>(n);
    auto frame = acmp_test::acmpdu(bind);
    ASSERT_TRUE(mbx_model_rx(&fabric, frame.data(), frame.size(), 0));
    acmp_sink_view sink{};
    for (unsigned k = 0; k < 200u && !sink.bound; ++k) {
        ctrl_plat_step();
        ASSERT_TRUE(acmp_view(&ctrl_plat.app.acmp.acmp, n, &sink));
    }
    ASSERT_TRUE(sink.bound);
    steps(20);
    bool answered = false;
    for (std::uint32_t k = 0; k < fabric.tx_sent; ++k) {
        const auto* tx = mbx_model_tx_frame(&fabric, k);
        if (tx == nullptr || tx->len < 70u || tx->bytes[14] != 0xfcu || (tx->bytes[15] & 15u) != 0u)
            continue;
        acmp_test::Pdu response = bind;
        response.msg = spec::MSG_PROBE_TX_RESPONSE;
        response.seq = static_cast<std::uint16_t>(be(tx->bytes + 62, 2));
        response.stream_id = acmp_test::kSid;
        response.dest_mac = acmp_test::kDa;
        response.vlan = 2u;
        frame = acmp_test::acmpdu(response);
        ASSERT_TRUE(mbx_model_rx(&fabric, frame.data(), frame.size(), 0));
        answered = true;
        break;
    }
    ASSERT_TRUE(answered);
    for (unsigned k = 0; k < 200u && !sink.settled; ++k) {
        ctrl_plat_step();
        ASSERT_TRUE(acmp_view(&ctrl_plat.app.acmp.acmp, n, &sink));
    }
    ASSERT_TRUE(sink.settled);
    ASSERT_EQ(sink.stream.stream_id, acmp_test::kSid);
    ASSERT_TRUE(ctrl_plat.aecp.core.waiting);
    const std::size_t from = bus().log.size();
    observed_input = n;
    stale_observations = 0;
    observing = true;
    far.ack = true;
    mbx_model_face_ack(&fabric, 0);
    const int status = final_status(0x0008u, 0x0501u);
    steps(20);
    observing = false;
    ASSERT_TRUE(acmp_view(&ctrl_plat.app.acmp.acmp, n, &sink));
    ASSERT_TRUE(sink.bound && sink.settled);
    const auto written = window(from, kOtherSelection);
    std::printf("PROBE: input=%u bound=%u settled=%u final_status=%d old=%016llx current=%016llx window=%016llx\n",
                n, sink.bound, sink.settled, status,
                static_cast<unsigned long long>(old_format),
                static_cast<unsigned long long>(inputs().at(n).format),
                static_cast<unsigned long long>(written.holds(n) ? written.format(n) : old_format));
    EXPECT_EQ(stale_observations, 0u)
        << "A settled binding must not remain published while its current format differs from its LCTX format";
}
