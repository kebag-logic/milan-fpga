// SPDX-License-Identifier: CERN-OHL-W-2.0
// SRP's Talker declarations follow the MAAP adapter's DA gate through the composition (#895; Milan v1.2 4.3.3.1 and
// 5.3.7.4): a source declares nothing until MAAP holds its range and a PROBE_TX_COMMAND for it was answered in the last
// 15 s or a matching Listener is registered; then at once, on its own interface, at MAAP's base + n; it withdraws when
// neither holds or MAAP loses the range, a re-probe with the same destination declares it again at once, and the new
// range's destination waits two LeaveAllTime periods after the Leave (IEEE 802.1Q-2018 35.2.2.8).
namespace {

class SrpGate : public AcmpMailbox {
protected:
    unsigned source = 0;
    unsigned interface = 0;
    // The adapter is the file's own: destroyed after each test, so the next one can initialise it.
    void TearDown() override { srp_mbx_destroy(&srp_adapter); }
    // The composition with SRP, MAAP holding every interface's range.
    void compose() {
        mbx_model_reset(&model);
        for (unsigned i = 0; i < MBX_N_IF; ++i) mbx_model_set_link(&model, i, true);
        const ctrl_app_config cfg = three_way();
        ASSERT_TRUE(ctrl_app_start(&app, &cfg));
        attach_srp();
        run(2200u);
        source = core()->cfg.n_sources - 1u;
        ASSERT_LT(source, CTRL_SRP_SOURCES);
        interface = core()->cfg.source_interface[source];
        ASSERT_TRUE(app.maap.ifs[interface].core.valid);
    }
    void run(unsigned ms) {
        for (unsigned k = 0; k < ms; ++k) {
            mbx_model_advance_ms(&model, 1u);
            settle();
        }
    }
    void probe() {
        Pdu request;
        request.msg = 0u;
        request.talker = kOwn;
        request.talker_uid = static_cast<std::uint16_t>(source);
        ASSERT_TRUE(offer(request, spec::MULTICAST_MAC, interface));
        settle();
    }
    bool declared(unsigned i) const { return (srp_adapter.ifs[i].talkers >> source & 1u) != 0u; }
    std::uint32_t talker_decl(unsigned i) const {
        mbx_model_pub view{};
        mbx_model_pub_view(&model, i, &view);
        return view.talker_decl;
    }
    // The destination SRP declares for the source on its interface.
    std::uint64_t destination() const {
        std::uint64_t d = 0;
        for (unsigned b = 0; b < 6; ++b) d = d << 8 | srp_adapter.ifs[interface].sources[source].value.dest_mac[b];
        return d;
    }
    // An MSRP Listener vector for the source's stream: one value, Asking Failed, `event` (1 JoinIn, 5 Lv).
    void listener(unsigned event) {
        std::array<std::uint8_t, 60> frame{};
        wire_put_be(frame.data(), 0x0180c200000eull, 6);
        wire_put_be(frame.data() + 6, 0x020304010203ull, 6);
        wire_put_be(frame.data() + 12, 0x22ea, 2);
        auto* p = frame.data() + 14;
        p[1] = 3; p[2] = 8; p[4] = 14; p[6] = 1;
        std::memcpy(p + 7, srp_sources[interface][source].value.stream_id.bytes, 8);
        p[15] = static_cast<std::uint8_t>(event * 36u); p[16] = 64;
        ASSERT_TRUE(mbx_model_rx(&model, frame.data(), frame.size(), interface));
        settle();
    }
    // A peer ANNOUNCEs the interface's range from a MAC whose octet-wise reverse is below this entity's, so compare_MAC
    // is FALSE and MAAP restarts on a new range (IEEE 1722-2016 Table B.7, B.3.6.4).
    void conflict() {
        std::array<std::uint8_t, 60> frame{};
        wire_put_be(frame.data(), MAAP_MULTICAST, 6);
        wire_put_be(frame.data() + 6, 0x0e0000000000ull, 6);
        frame[12] = 0x22; frame[13] = 0xf0; frame[14] = 0xfe; frame[15] = 3; frame[16] = 8; frame[17] = 16;
        wire_put_be(frame.data() + 26, app.maap.ifs[interface].core.base, 6);
        wire_put_be(frame.data() + 32, app.maap.ifs[interface].core.count, 2);
        ASSERT_TRUE(mbx_model_rx(&model, frame.data(), frame.size(), interface));
        settle();
    }
};

TEST_F(SrpGate, F895AProbeDeclaresTheSourceAndItsExpiryWithdrawsIt) {
    compose();
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        EXPECT_EQ(srp_adapter.ifs[i].talkers, 0u) << "no Talker is declared before its destination is valid";
        EXPECT_EQ(talker_decl(i), 0u) << "no Talker is declared before its destination is valid";
    }
    probe();
    run(300u);
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        EXPECT_EQ(declared(i), i == interface) << "a probe declares the source's Talker on its own interface";
        EXPECT_EQ((talker_decl(i) >> source & 1u) != 0u, i == interface)
            << "a probe declares the source's Talker on its own interface";
    }
    EXPECT_EQ(destination(), app.maap.ifs[interface].core.base + source) << "with MAAP's base + n";
    run(14500u);
    EXPECT_TRUE(declared(interface)) << "the probe window holds the Talker for 15 s";
    run(500u);
    EXPECT_FALSE(declared(interface)) << "the probe's 15 s expiry withdraws the Talker";
    EXPECT_EQ(talker_decl(interface) >> source & 1u, 0u) << "the probe's 15 s expiry withdraws the Talker";
    probe();
    run(300u);
    EXPECT_TRUE(declared(interface)) << "a re-probe with the same destination declares it again at once";
    EXPECT_EQ(core()->reentries, 0u);
}

TEST_F(SrpGate, F895AListenerKeepsTheSourceDeclaredPastTheProbeWindow) {
    compose();
    probe();
    run(300u);
    ASSERT_TRUE(declared(interface)) << "a probe declares the source's Talker";
    // the peer keeps its Listener declared, re-joining as after every LeaveAll (IEEE 802.1Q-2018 10.7.4.3)
    for (unsigned s = 0; s < 16u; ++s) {
        listener(1u);
        run(1000u);
    }
    EXPECT_TRUE(declared(interface)) << "a registered Listener keeps the Talker past the probe window";
    listener(5u);
    run(300u);
    EXPECT_FALSE(declared(interface)) << "with neither a probe nor a Listener, the Talker withdraws";
    EXPECT_EQ(core()->reentries, 0u);
}

TEST_F(SrpGate, F895ARangeLostWithdrawsAndTheNewRangeWaitsTheHoldOff) {
    compose();
    probe();
    run(300u);
    listener(1u);
    ASSERT_TRUE(declared(interface)) << "a probe declares the source's Talker";
    const std::uint64_t first = app.maap.ifs[interface].core.base;
    conflict();
    EXPECT_NE(app.maap.ifs[interface].core.base, first) << "MAAP restarts on a new range";
    EXPECT_FALSE(declared(interface)) << "a range lost withdraws the Talker";
    EXPECT_EQ(talker_decl(interface) >> source & 1u, 0u) << "a range lost withdraws the Talker";
    // the peer keeps its Listener, so the source is valid again once MAAP holds the new range (Milan v1.2 4.3.3.1)
    for (unsigned s = 0; s < 19u; ++s) {
        run(1000u);
        listener(1u);
    }
    EXPECT_TRUE(app.maap.ifs[interface].core.valid) << "MAAP holds the new range";
    EXPECT_FALSE(declared(interface)) << "a changed destination waits two LeaveAllTime periods after the Leave";
    for (unsigned s = 0; s < 2u; ++s) {
        run(1000u);
        listener(1u);
    }
    EXPECT_TRUE(declared(interface)) << "the new range's destination is declared once the hold-off ends";
    EXPECT_EQ(destination(), app.maap.ifs[interface].core.base + source) << "with the new range's base + n";
    EXPECT_EQ(core()->reentries, 0u);
}

}  // namespace
