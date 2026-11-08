// SPDX-License-Identifier: MIT
// Reviewer probes for the ACMP owed bound. Appended inside the anonymous namespace of a disposable
// copy of tests/test_acmp.cpp so it can reuse the AcmpOwed port model. Never part of the reviewed tree.
class AcmpOwedProbe : public AcmpOwed {
 protected:
    void passes_after(std::uint32_t hold) {
        fk.now += hold;
        fk.room = true;
        for (unsigned n = 0; n < 4u * ACMP_OWED_MAX && (a.owed_count != 0u || !held.empty()); ++n) {
            pass();
        }
    }
    unsigned sent_of(std::uint8_t msg) const {
        unsigned n = 0;
        for (const Sent& s : fk.sent) {
            n += read(s.bytes.data()).msg == msg ? 1u : 0u;
        }
        return n;
    }
};

// A declined BIND_RX is answered after redelivery; record what happens to its first probe.
TEST_F(AcmpOwedProbe, BindDeclinedIsAnsweredAfterRedelivery) {
    fill(0x7700);
    fk.clear();
    const std::uint32_t arrival = fk.now;
    EXPECT_FALSE(deliver(command(spec::MSG_BIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7708)));
    EXPECT_EQ(a.sinks[1].state, ACMP_UNBOUND);
    release_after_hold();
    const Sent* s = answer(spec::MSG_BIND_RX_RESPONSE, 0x7708);
    ASSERT_TRUE(s != nullptr) << "PROBE: deferred BIND_RX unanswered";
    Pdu r = read(s->bytes.data());
    EXPECT_TRUE(r.status == spec::STATUS_SUCCESS && r.listener_uid == 1u && r.count == 1u && r.talker == kTkA);
    EXPECT_LE(s->at - arrival, kCommandTimeoutMs);
    std::printf("PROBE bind: answer_ms=%u probes_lost=%u probe_tx_sent=%u state=%d timer=%d bound=%d\n",
                static_cast<unsigned>(s->at - arrival), a.probes_lost, sent_of(spec::MSG_PROBE_TX_COMMAND),
                static_cast<int>(a.sinks[1].state), static_cast<int>(a.sinks[1].timer), a.sinks[1].bound ? 1 : 0);
    fk.now += ACMP_TMR_NO_RESP_MS;
    acmp_timer_expired(&a, 0);
    std::printf("PROBE bind: after NO_RESP expiry probe_tx_sent=%u state=%d\n", sent_of(spec::MSG_PROBE_TX_COMMAND),
                static_cast<int>(a.sinks[1].state));
}

// A declined GET_TX_STATE is answered after redelivery with the Milan Table 5.47 fields.
TEST_F(AcmpOwedProbe, GetTxStateDeclinedIsAnsweredAfterRedelivery) {
    fill(0x7800);
    fk.clear();
    Pdu t;
    t.msg = spec::MSG_GET_TX_STATE_COMMAND;
    t.controller = kCtl2;
    t.talker = kOwn;
    t.talker_uid = 0u;
    t.seq = 0x7808;
    const std::uint32_t arrival = fk.now;
    EXPECT_FALSE(deliver(t));
    release_after_hold();
    const Sent* s = answer(spec::MSG_GET_TX_STATE_RESPONSE, 0x7808);
    ASSERT_TRUE(s != nullptr) << "PROBE: deferred GET_TX_STATE unanswered";
    Pdu r = read(s->bytes.data());
    EXPECT_TRUE(r.status == spec::STATUS_SUCCESS && r.stream_id == kSid && r.dest_mac == kDa);
    EXPECT_LE(s->at - arrival, kCommandTimeoutMs);
    std::printf("PROBE get_tx_state: answer_ms=%u status=%u\n", static_cast<unsigned>(s->at - arrival),
                static_cast<unsigned>(r.status));
}

// A declined command for an unknown listener unique ID is answered LISTENER_UNKNOWN_ID after redelivery.
TEST_F(AcmpOwedProbe, UnknownSinkDeclinedIsAnsweredAfterRedelivery) {
    fill(0x7900);
    fk.clear();
    EXPECT_FALSE(deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 9, 0, 0, kCtl2, 0, 0x7908)));
    release_after_hold();
    const Sent* s = answer(spec::MSG_GET_RX_STATE_RESPONSE, 0x7908);
    ASSERT_TRUE(s != nullptr);
    std::printf("PROBE unknown sink: status=%u unknown_sink=%u\n", static_cast<unsigned>(read(s->bytes.data()).status),
                a.unknown_sink);
}

// Each declined offer counts; repeated offers change nothing else.
TEST_F(AcmpOwedProbe, RepeatedOffersEachCount) {
    fill(0x7A00);
    fk.clear();
    auto f = acmpdu(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, 0x7A08));
    for (int n = 0; n < 3; ++n) {
        EXPECT_FALSE(acmp_rx(&a, 0, f.data(), f.size()));
    }
    EXPECT_TRUE(a.busy_declined == 3u && a.owed_count == ACMP_OWED_MAX && fk.calls.empty());
    std::printf("PROBE repeat: busy_declined=%u calls=%zu\n", a.busy_declined, fk.calls.size());
}

// Byte-level image of a decline with no field masked: list every byte that changes.
TEST_F(AcmpOwedProbe, DeclineByteImage) {
    bind(1);
    fill(0x7B00);
    fk.clear();
    a.now_read = true;
    acmp before;
    std::memcpy(&before, &a, sizeof a);
    auto f = acmpdu(command(spec::MSG_UNBIND_RX_COMMAND, 1, kTkA, 1, kCtl1, 0, 0x7B08));
    EXPECT_FALSE(acmp_rx(&a, 0, f.data(), f.size()));
    const auto* x = reinterpret_cast<const unsigned char*>(&before);
    const auto* y = reinterpret_cast<const unsigned char*>(&a);
    const std::size_t busy = offsetof(acmp, busy_declined);
    const std::size_t nr = offsetof(acmp, now_read);
    unsigned other = 0;
    for (std::size_t i = 0; i < sizeof a; ++i) {
        if (x[i] != y[i]) {
            bool known = (i >= busy && i < busy + sizeof a.busy_declined) || i == nr;
            other += known ? 0u : 1u;
            std::printf("PROBE image: byte %zu changed (%s)\n", i,
                        i == nr ? "now_read" : (known ? "busy_declined" : "OTHER"));
        }
    }
    EXPECT_EQ(other, 0u);
    std::printf("PROBE image: other_bytes_changed=%u now_read_after=%d\n", other, a.now_read ? 1 : 0);
}

// Answer time against egress hold length, for a port polling once per 1 ms pass.
TEST_F(AcmpOwedProbe, HoldSweep) {
    for (std::uint32_t hold : {0u, 60u, 131u, 191u, 192u}) {
        SetUp();
        held.clear();
        fill(0x7C00);
        fk.clear();
        const std::uint32_t arrival = fk.now;
        EXPECT_FALSE(deliver(command(spec::MSG_GET_RX_STATE_COMMAND, 0, 0, 0, kCtl2, 0, 0x7C08)));
        passes_after(hold);
        const Sent* s = answer(spec::MSG_GET_RX_STATE_RESPONSE, 0x7C08);
        ASSERT_TRUE(s != nullptr);
        std::printf("PROBE sweep: hold_ms=%u answer_ms=%u within_200=%d\n", hold,
                    static_cast<unsigned>(s->at - arrival), (s->at - arrival) <= kCommandTimeoutMs ? 1 : 0);
    }
}
