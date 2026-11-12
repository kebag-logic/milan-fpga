// Reviewer probe P1 (disposable; inserted into a scratch copy of test_acmp_mbx.cpp before its
// closing namespace). acmp_mbx.h, THE KEPT COMMAND, states that apart from a kept BIND_RX that is
// only answered "a kept command's response leaves in pass n + 1 + f + r after the room returns".
// The port contract (tsn-c-stack docs/PORTING.md, "ACMP owed bound") names a second case for a port
// that offers fewer waiting frames after an accepting poll: "a frame that needs no answer".
// Arm WITH_GAP puts two such frames between two kept commands and lets one TMR_NO_RESP retry probe
// fall due in the pass after the gap; arm NO_GAP is the same run without them (control).

TEST_F(AcmpMailbox, ProbeP1LaterKeptCommandBehindNoAnswerFramesAndATimerProbe) {
    auto probe_p1_run = [&](bool with_gap, unsigned& first_pass, unsigned& second_pass, unsigned& probe_pass, unsigned& lost) {
        const unsigned i = acfg.sink_interface[1];
        const unsigned k2 = 0;                       // the timer probe's sink
        const unsigned i2 = acfg.sink_interface[k2];
        ASSERT_TRUE(offer(command(spec::MSG_BIND_RX_COMMAND, k2), spec::MULTICAST_MAC, i2));
        settle();
        ASSERT_EQ(core()->sinks[k2].state, ACMP_PRB_W_RESP) << "P1 the sink waits for its probe answer: k2 " << k2 << " if " << i << " n_sinks " << acfg.n_sinks << " state " << int(core()->sinks[k2].state);
        fill_owed();
        ASSERT_TRUE(offer(command(spec::MSG_GET_RX_STATE_COMMAND, 1, kCtl1, 0x7001),
                          spec::MULTICAST_MAC, i));
        if (with_gap) {
            for (unsigned n = 0; n < 2u; ++n) {
                // a PROBE_TX_RESPONSE for the unbound sink 1: taken, owes nothing
                Pdu r;
                r.msg = spec::MSG_PROBE_TX_RESPONSE;
                r.controller = kCtl1;
                r.talker = kTkA;
                r.listener = kOwn;
                r.talker_uid = 1;
                r.listener_uid = 1;
                r.seq = static_cast<std::uint16_t>(0x1230u + n);
                ASSERT_TRUE(offer(r, spec::MULTICAST_MAC, i));
            }
        }
        ASSERT_TRUE(offer(command(spec::MSG_GET_RX_STATE_COMMAND, 1, kCtl1, 0x7002),
                          spec::MULTICAST_MAC, i));
        for (unsigned p = 0; p < 20u; ++p) {
            static_cast<void>(pass());
        }
        const unsigned lost0 = core()->probes_lost;
        mbx_model_tx_pause(&model, false);
        std::uint32_t base = model.tx_sent;
        first_pass = second_pass = probe_pass = 0;
        for (unsigned p = 1; p <= ACMP_MBX_KEPT_PASSES + 6u; ++p) {
            if (p == 3u) {
                const mbx_model_timer& t = model.timers[slot(i2)];
                ASSERT_TRUE(t.armed);
                mbx_model_advance_ms(&model, t.deadline_ms - model.now_ms);   // TMR_NO_RESP of sink k2 falls due
            }
            static_cast<void>(pass());
            for (std::uint32_t j = base; j < model.tx_sent; ++j) {
                Pdu w = wire(j);
                if (w.msg == spec::MSG_GET_RX_STATE_RESPONSE && w.seq == 0x7001u && first_pass == 0u) {
                    first_pass = p;
                }
                if (w.msg == spec::MSG_GET_RX_STATE_RESPONSE && w.seq == 0x7002u && second_pass == 0u) {
                    second_pass = p;
                }
                if (w.msg == spec::MSG_PROBE_TX_COMMAND && probe_pass == 0u) {
                    probe_pass = p;
                }
            }
            base = model.tx_sent;
        }
        lost = core()->probes_lost - lost0;
    };
    unsigned a1 = 0, a2 = 0, ap = 0, al = 0;
    probe_p1_run(false, a1, a2, ap, al);
    std::printf("P1 NO_GAP   first %u second %u probe %u probes_lost %u (n + 1 + f = %u for the second)\n", a1, a2,
                ap, al, ACMP_OWED_MAX + 2u);
    SetUp();
    unsigned b1 = 0, b2 = 0, bp = 0, bl = 0;
    probe_p1_run(true, b1, b2, bp, bl);
    std::printf("P1 WITH_GAP first %u second %u probe %u probes_lost %u (n + 1 + f = %u for the second)\n", b1, b2,
                bp, bl, ACMP_OWED_MAX + 2u);
    EXPECT_EQ(a2, ACMP_OWED_MAX + 2u) << "P1 control: the second kept command leaves in pass n + 1 + f";
    EXPECT_EQ(b2, ACMP_OWED_MAX + 2u)
        << "P1 the header's bound for the second command with two no-answer frames between them";
}
