// SPDX-License-Identifier: CERN-OHL-W-2.0
// SRP's Talker declarations follow the MAAP adapter's DA gate through the composition (#895; Milan v1.2 4.3.3.1 and
// 5.3.7.4): a source declares nothing until MAAP holds its range and a PROBE_TX_COMMAND for it was answered in the last
// 15 s or a matching Listener is registered; then at once, on its own interface, at MAAP's base + n; it withdraws when
// neither holds or MAAP loses the range, a re-probe with the same destination declares it again at once, and the new
// range's destination waits two LeaveAllTime periods after the Leave (IEEE 802.1Q-2018 35.2.2.8). The source's frames
// carry the stream_id its Talker declares (#905): the MAAP adapter, the DA gate's owner, writes each source's
// SRC_SID_HI:SRC_SID_LO while its DA_GATE bit is clear, at its start before the bit first opens, and again before each
// reopening, read from the source port (KL_mbx_pkg.sv SRC_SID_LO; Milan v1.2 5.3.7.5).
namespace {

// The publication block's writes from the model's reset, in order (#905).
struct SidWrite {
    std::uint32_t off;
    std::uint32_t value;
};
std::vector<SidWrite> sid_writes;
void sid_record(void*, bool write, std::uint32_t off, std::uint32_t value) {
    if (write && off >= MBX_PUB_BASE && off < MBX_PUB_BASE + MBX_N_IF * MBX_PUB_STRIDE) {
        sid_writes.push_back({off, value});
    }
}

class SrpGate : public AcmpMailbox {
protected:
    unsigned source = 0;
    unsigned interface = 0;
    // The adapter is the file's own: destroyed after each test, so the next one can initialise it.
    void TearDown() override {
        mbx_host_trace(nullptr, nullptr);
        srp_mbx_destroy(&srp_adapter);
    }
    // Source s's stream_id as the platform's source port reports it, the entity's MAC and the output's index
    // (ctrl_plat.c stream_id; IEEE 1722.1-2021 7.2.3), which attach_srp has SRP's Talker declare.
    static std::uint64_t stream_id(unsigned s) { return kEntity.mac << 16 | s; }
    // The composition with SRP, MAAP holding every interface's range, ACMP's source port reporting each source's
    // stream_id, and the publication block's writes recorded from the reset.
    void compose() {
        mbx_model_reset(&model);
        sid_writes.clear();
        mbx_host_trace(sid_record, nullptr);
        for (unsigned s = 0; s < ACMP_MAX_SOURCES; ++s) fk.source[s].stream.stream_id = stream_id(s);
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
    // Source s's SRC_SID_HI:SRC_SID_LO as the datapath reads it.
    std::uint64_t sid(unsigned s) const {
        mbx_model_pub view{};
        mbx_model_pub_view(&model, core()->cfg.source_interface[s], &view);
        return view.src_sid[s];
    }
    // The stream_id SRP's Talker declares for the source (attach_srp).
    std::uint64_t declared_id() const {
        std::uint64_t v = 0;
        for (unsigned b = 0; b < 8; ++b) v = v << 8 | srp_sources[interface][source].value.stream_id.bytes[b];
        return v;
    }
    // What the source's history of publication writes shows, its port having reported each `reported` stream_id
    // from that index of sid_writes on: each DA_GATE write that opens its bit, and whether its SRC_SID then held the
    // stream_id reported; whether a word was written while its bit was set; whether a reopening came before both words
    // were written again since the bit closed; and the last value written to each word.
    struct History {
        unsigned openings = 0;
        bool opened_stale = false;
        bool written_open = false;
        bool reopened_unwritten = false;
        std::uint32_t lo = 0;
        std::uint32_t hi = 0;
    };
    History history(const std::vector<std::pair<std::size_t, std::uint64_t>>& reported) const {
        const std::uint32_t block = MBX_PUB_BASE + MBX_PUB_STRIDE * interface;
        const std::uint32_t entry = block + MBX_PUB_SRC_BASE + MBX_PUB_SRC_STRIDE * source;
        History h;
        std::uint32_t gate = 0;
        bool closed = false;
        bool lo_again = false;
        bool hi_again = false;
        for (std::size_t n = 0; n < sid_writes.size(); ++n) {
            const SidWrite& w = sid_writes[n];
            const bool open = (gate >> source & 1u) != 0u;
            if (w.off == entry + MBX_PUB_SRC_REG_SRC_SID_LO || w.off == entry + MBX_PUB_SRC_REG_SRC_SID_HI) {
                const bool low = w.off == entry + MBX_PUB_SRC_REG_SRC_SID_LO;
                h.written_open = h.written_open || open;
                (low ? h.lo : h.hi) = w.value;
                (low ? lo_again : hi_again) = true;
            } else if (w.off == block + MBX_PUB_REG_DA_GATE) {
                const bool set = (w.value >> source & 1u) != 0u;
                if (!open && set) {
                    std::uint64_t want = 0;
                    for (const auto& r : reported) want = r.first <= n ? r.second : want;
                    ++h.openings;
                    h.opened_stale = h.opened_stale || (std::uint64_t{h.hi} << 32 | h.lo) != want;
                    h.reopened_unwritten = h.reopened_unwritten || (closed && !(lo_again && hi_again));
                }
                if (open && !set) {
                    closed = true;
                    lo_again = hi_again = false;
                }
                gate = w.value;
            }
        }
        return h;
    }
    // The checks every #905 test makes of the source's history, each by its own words.
    void sid_checks(const History& h, unsigned openings) {
        EXPECT_EQ(h.openings, openings) << "the source's DA_GATE bit opens once a probe or a Listener asks for it";
        EXPECT_FALSE(h.opened_stale) << "SRC_SID holds the source's stream_id when its DA_GATE bit opens";
        EXPECT_FALSE(h.written_open) << "SRC_SID is written only while the source's DA_GATE bit is clear";
        EXPECT_FALSE(h.reopened_unwritten)
            << "both SRC_SID words are written again between the bit's closing and its reopening";
    }
    // One service pass at a time until the source's DA_GATE bit reads `open`, at most `passes`.
    bool passes_until(bool open, unsigned passes) {
        for (unsigned n = 0; n < passes; ++n) {
            static_cast<void>(pass());
            mbx_model_pub view{};
            mbx_model_pub_view(&model, interface, &view);
            if (((view.da_gate >> source & 1u) != 0u) == open) return true;
        }
        return false;
    }
    // The source's Listener's MSRP vector (listener()) offered without a pass.
    void listener_frame(unsigned event) {
        std::array<std::uint8_t, 60> frame{};
        wire_put_be(frame.data(), 0x0180c200000eull, 6);
        wire_put_be(frame.data() + 6, 0x020304010203ull, 6);
        wire_put_be(frame.data() + 12, 0x22ea, 2);
        auto* p = frame.data() + 14;
        p[1] = 3; p[2] = 8; p[4] = 14; p[6] = 1;
        std::memcpy(p + 7, srp_sources[interface][source].value.stream_id.bytes, 8);
        p[15] = static_cast<std::uint8_t>(event * 36u); p[16] = 64;
        ASSERT_TRUE(mbx_model_rx(&model, frame.data(), frame.size(), interface));
    }
};

// #905: before any gate opens, every source's SRC_SID holds the stream_id its port reports, each word in its own
// register; a probe then opens the source's gate with its SRC_SID already holding the stream_id its Talker declares.
TEST_F(SrpGate, F905AEachSourceStreamIdIsWrittenBeforeItsGateOpens) {
    compose();
    for (unsigned s = 0; s < core()->cfg.n_sources; ++s) {
        EXPECT_EQ(sid(s), stream_id(s)) << "SRC_SID holds each source's stream_id before any DA_GATE bit opens";
    }
    EXPECT_EQ(stream_id(source), declared_id()) << "the source port reports the stream_id SRP's Talker declares";
    probe();
    run(300u);
    ASSERT_TRUE(declared(interface)) << "a probe declares the source's Talker";
    const History h = history({{0u, stream_id(source)}});
    sid_checks(h, 1u);
    EXPECT_EQ(h.lo, static_cast<std::uint32_t>(stream_id(source)))
        << "SRC_SID_LO holds the stream_id's low word and SRC_SID_HI its high word";
    EXPECT_EQ(h.hi, static_cast<std::uint32_t>(stream_id(source) >> 32))
        << "SRC_SID_LO holds the stream_id's low word and SRC_SID_HI its high word";
    EXPECT_EQ(sid(source), declared_id()) << "the source's frames carry the stream_id its Talker declares";
    EXPECT_EQ(core()->reentries, 0u);
}

// #905: a stream_id the source port changes while the gate is closed is written before the gate reopens, both its
// words changed, so the source's frames never carry the stale one.
TEST_F(SrpGate, F905AStreamIdChangedWhileClosedIsWrittenBeforeTheGateReopens) {
    compose();
    probe();
    run(300u);
    ASSERT_TRUE(declared(interface)) << "a probe declares the source's Talker";
    run(15000u);
    ASSERT_FALSE(declared(interface)) << "the probe's 15 s expiry withdraws the Talker";
    const std::uint64_t moved = stream_id(source) ^ 0x0000010000000100ull;
    const std::size_t at = sid_writes.size();
    fk.source[source].stream.stream_id = moved;
    run(100u);
    probe();
    run(300u);
    sid_checks(history({{0u, stream_id(source)}, {at, moved}}), 2u);
    EXPECT_EQ(sid(source), moved) << "SRC_SID holds the source's stream_id when its DA_GATE bit opens";
    EXPECT_EQ(core()->reentries, 0u);
}

// #905: a gate closed by its Listener's Leave and asked for again by the next JoinIn, a pass later, reopens only once
// both SRC_SID words are written again, each while the bit is clear.
TEST_F(SrpGate, F905AGateReopensOnlyOnceItsStreamIdIsWrittenAgain) {
    compose();
    listener(1u);
    run(300u);
    ASSERT_TRUE(declared(interface)) << "a registered Listener declares the source's Talker";
    listener_frame(5u);
    ASSERT_TRUE(passes_until(false, 8u)) << "the Listener's Leave closes the source's DA_GATE bit";
    listener_frame(1u);
    ASSERT_TRUE(passes_until(true, 8u)) << "the Listener's JoinIn reopens the source's DA_GATE bit";
    settle();
    sid_checks(history({{0u, stream_id(source)}}), 2u);
    EXPECT_EQ(sid(source), stream_id(source)) << "SRC_SID holds the source's stream_id when its DA_GATE bit opens";
    EXPECT_EQ(core()->reentries, 0u);
}

// #905: after a MAAP conflict the gate is closed until the new allocation (KL_mbx_pkg.sv SRC_SID_LO; Milan v1.2
// 5.5.4.1): the loss closes it, both SRC_SID words are written again while it is closed, and the new range reopens it.
TEST_F(SrpGate, F905ARangeLostClosesTheGateUntilItsStreamIdIsWrittenAgain) {
    compose();
    probe();
    run(300u);
    listener(1u);
    ASSERT_TRUE(declared(interface)) << "a probe declares the source's Talker";
    conflict();
    mbx_model_pub view{};
    mbx_model_pub_view(&model, interface, &view);
    EXPECT_EQ(view.da_gate >> source & 1u, 0u) << "a range lost closes the source's DA_GATE bit";
    for (unsigned s = 0; s < 4u; ++s) {
        run(1000u);
        listener(1u);
    }
    ASSERT_TRUE(app.maap.ifs[interface].core.valid) << "MAAP holds the new range";
    mbx_model_pub_view(&model, interface, &view);
    ASSERT_EQ(view.da_gate >> source & 1u, 1u) << "the new range reopens the source's DA_GATE bit";
    sid_checks(history({{0u, stream_id(source)}}), 2u);
    EXPECT_EQ(sid(source), stream_id(source)) << "SRC_SID holds the source's stream_id when its DA_GATE bit opens";
    EXPECT_EQ(core()->reentries, 0u);
}

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
