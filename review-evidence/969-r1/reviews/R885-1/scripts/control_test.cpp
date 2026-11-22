// Reviewer control probe (not part of the PR): UNBIND_RX then BIND_RX to the same stream, the issue's control order.
// Each input is bound, settles and declares for its stream; it is unbound while its talker stays quiet; bound again,
// its Listener is declared in THE TRANSMIT's next MRPDU once the probe is answered, with GET_STREAM_INFO's REGISTERING.
TEST_F(Early, ZControlUnbindThenBindToTheSameStreamDeclaresWithinOneTransmit) {
    ASSERT_TRUE(ready());
    const auto all = every_input();
    ASSERT_FALSE(all.empty());
    for (const unsigned n : all) {
        const std::uint32_t since = fabric.tx_sent;
        ASSERT_TRUE(bind(n, true)) << "control input " << n << " is bound";
        ASSERT_TRUE(answer_probe(n, since, n)) << "control input " << n << " settles";
        pass(12);
        const auto f = talker_declaration(n, false);
        ASSERT_TRUE(mbx_model_rx(&fabric, f.data(), f.size(), 0));
        pass(kJoinMs + 10u);
        ASSERT_EQ(ctrl_plat.srp.ifs[0].sinks[n].declared, 2u) << "control input " << n << " declares its stream";
    }
    for (const unsigned n : all) {
        ASSERT_TRUE(bind(n, false)) << "control UNBIND_RX of input " << n;
        pass(12);
    }
    pass(1000);
    for (const unsigned n : all) {
        ASSERT_TRUE(acmp(spec::MSG_BIND_RX_COMMAND, n)) << "control BIND_RX of input " << n;
        pass(6);
    }
    answer_every_probe(all, 0u, false, "control UNBIND_RX then BIND_RX to the same stream", 0x0f00u);
}

