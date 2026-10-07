// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_acmp_nvm.cpp - the listener's bindings on lane F1's saved-state store
// (#665 lane F3; GoogleTest):
//
//   N   the ACMP core and acmp_nvm on the store as it ships (nvm_store.c,
//       nvm_klj2.c), over the host flash model, at the shipping 1x1 shape:
//       a bind saved and brought back by a power cycle into PRB_W_AVAIL with
//       discovery running, and the fast connect it then makes on the
//       talker's ENTITY_AVAILABLE (Milan v1.2 5.5.3.5.2, 5.5.2.6); an unbind
//       saved as an unbound record; the started flags; a slot the boot
//       cannot read holding the writer, so a later bind is not saved and the
//       old binding comes back (ctrl_nvm/README.md, "Boot" item 9); a record
//       the core refuses; the roll-back; every other group forwarded.
//
// The boot runs as a platform runs it (acmp_nvm.h): the core composed, the
// store booted through acmp_nvm's port, then the core's inputs; the env's
// persist port calls nvm_store_changed(NVM_G_BIND, sink).

#include <gtest/gtest.h>

#include <cstdint>
#include <cstring>

#include "acmp.h"
#include "acmp_fake.hpp"
#include "acmp_nvm.h"
#include "fw_gtest.hpp"
#include "wire.h"

// The store's headers carry no extern "C" and assert with C11's _Static_assert
// (lane F1's nvm_c.hpp supplies both the same way, for these includes only).
#define _Static_assert static_assert
extern "C" {
#include "nvm_fmodel.h"
#include "nvm_klj2.h"
#include "nvm_smodel.h"
#include "nvm_store.h"
}
#undef _Static_assert

FW_TALLY_LABEL("ctrl ACMP bindings on the saved-state store (1x1 shape)");

using namespace acmp_test;

namespace {

constexpr std::uint64_t kLoopUs = 1000u;       // one store step per millisecond of model time
constexpr std::uint32_t kJournal = 2u * NVM_SLOT_BYTES;

unsigned persists;

void persist_to_store(void*, unsigned sink) {
    persists++;
    nvm_store_changed(NVM_G_BIND, sink);
}

const acmp_env kStoreEnv = {nullptr, f_locked, f_source, f_srp, persist_to_store, f_changed};

class AcmpStore : public ::testing::Test {
 protected:
    void SetUp() override {
        nvm_fmodel_blank();
        boot(MILAN_NVM_N_STREAM_IN);
    }

    // A power cycle: the media keeps its bytes, the core and the store start afresh.
    void boot(unsigned sinks) {
        fk = Fake{};
        persists = 0;
        nvm_fmodel_power_on();
        nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_A + kJournal);
        nvm_smodel_reset();
        acmp_config cfg{};
        cfg.entity_id = kOwn;
        cfg.n_interfaces = 1;
        cfg.mac[0] = kMac0;
        cfg.n_sinks = sinks;
        ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kStoreEnv));
        acmp_nvm_init(&glue, &a, NVM_G_BIND, &nvm_smodel_port);
        nvm_store_boot(&nvm_fmodel_port, &glue.port);
    }

    // Serve the store until nothing waits (or ms of model time pass).
    void serve(std::uint64_t ms = 20000u) {
        const std::uint64_t until = nvm_fmodel_now_us() + ms * 1000u;
        do {
            nvm_store_service();
            nvm_fmodel_advance_us(kLoopUs);
        } while (nvm_fmodel_now_us() < until && !settled());
    }
    static bool settled() {
        const nvm_status* s = nvm_store_status();
        return s->phase == NVM_P_HELD || (s->phase == NVM_P_IDLE && !s->dirty && !s->pending);
    }

    void command(std::uint8_t msg, unsigned sink, std::uint64_t talker, std::uint16_t flags = 0) {
        Pdu p;
        p.msg = msg;
        p.controller = kCtl1;
        p.talker = talker;
        p.listener = kOwn;
        p.talker_uid = 1;
        p.listener_uid = static_cast<std::uint16_t>(sink);
        p.flags = flags;
        auto f = acmpdu(p);
        acmp_rx(&a, 0, f.data(), f.size());
    }

    acmp a{};
    acmp_nvm glue{};
};

TEST_F(AcmpStore, N1ABindSurvivesAPowerCycleAndFastConnects) {
    EXPECT_EQ(nvm_store_status()->terminal, NVM_T_BLANK) << "N1 blank media boots BLANK";
    command(spec::MSG_BIND_RX_COMMAND, 0, kTkA);
    ASSERT_EQ(persists, 1u) << "N1 the bind marks its record (5.5.2.4)";
    unsigned ok = nvm_store_status()->commits_ok;
    serve();
    ASSERT_EQ(nvm_store_status()->commits_ok, ok + 1u) << "N1 the store commits it";
    boot(MILAN_NVM_N_STREAM_IN);
    EXPECT_EQ(nvm_store_status()->terminal, NVM_T_COMPLETE) << "N1 the next boot restores the container";
    const acmp_sink& s = a.sinks[0];
    EXPECT_TRUE(s.bound && s.binding.talker_entity_id == kTkA && s.binding.talker_unique_id == 1u &&
                s.binding.controller_entity_id == kCtl1 && s.started && !s.binding.streaming_wait)
        << "N1 the binding parameters come back (5.3.8.2, 5.3.8.3)";
    EXPECT_TRUE(s.state == ACMP_PRB_W_AVAIL && s.probing == ACMP_PROBING_PASSIVE && s.disc_running && !s.discovered)
        << "N1 into PRB_W_AVAIL, PROBING_PASSIVE, discovery running (5.5.3.5.2)";
    EXPECT_TRUE(!a.sinks[1].bound && a.sinks[1].state == ACMP_UNBOUND) << "N1 the sink never bound stays unbound";
    EXPECT_TRUE(persists == 0u && fk.calls.empty()) << "N1 a restore saves and reports nothing";
    auto avail = adpdu(Adp{});
    acmp_adp_rx(&a, 0, avail.data(), avail.size());
    fk.now = a.sinks[0].timer_deadline;
    acmp_timer_expired(&a, 0);
    ASSERT_FALSE(fk.sent.empty());
    Pdu probe = read(fk.sent.back().bytes.data());
    EXPECT_TRUE(probe.msg == spec::MSG_PROBE_TX_COMMAND && probe.talker == kTkA && probe.controller == kCtl1 &&
                probe.talker_uid == 1u && a.sinks[0].state == ACMP_PRB_W_RESP)
        << "N1 the talker's ENTITY_AVAILABLE starts the fast connect: TMR_DELAY, then its probe (5.5.2.6)";
    EXPECT_EQ(persists, 0u) << "N1 probing saves nothing";
}

TEST_F(AcmpStore, N2AnUnbindIsSavedAsAnUnboundRecord) {
    command(spec::MSG_BIND_RX_COMMAND, 0, kTkA);
    serve();
    boot(MILAN_NVM_N_STREAM_IN);
    ASSERT_TRUE(a.sinks[0].bound);
    command(spec::MSG_UNBIND_RX_COMMAND, 0, kTkA);
    ASSERT_EQ(persists, 1u) << "N2 the unbind marks the record (5.5.3.5.8 step 3)";
    serve();
    boot(MILAN_NVM_N_STREAM_IN);
    EXPECT_TRUE(!a.sinks[0].bound && a.sinks[0].state == ACMP_UNBOUND && nvm_store_status()->terminal == NVM_T_COMPLETE)
        << "N2 the next boot finds the sink unbound";
}

TEST_F(AcmpStore, N3EachSinksStartedStateIsSaved) {
    command(spec::MSG_BIND_RX_COMMAND, 0, kTkA, spec::FLAG_STREAMING_WAIT);
    command(spec::MSG_BIND_RX_COMMAND, 1, kTkB);
    serve();
    unsigned ok = nvm_store_status()->commits_ok;
    ASSERT_TRUE(acmp_set_started(&a, 1, false)) << "N3 STOP_STREAMING of sink 1";
    serve();
    EXPECT_EQ(nvm_store_status()->commits_ok, ok + 1u) << "N3 the started state alone is a change the store commits";
    boot(MILAN_NVM_N_STREAM_IN);
    EXPECT_TRUE(a.sinks[0].bound && !a.sinks[0].started && a.sinks[0].binding.streaming_wait && a.sinks[1].bound &&
                !a.sinks[1].started && !a.sinks[1].binding.streaming_wait && a.sinks[1].binding.talker_entity_id == kTkB)
        << "N3 each sink's started state and STREAMING_WAIT come back (5.3.8.7)";
}

TEST_F(AcmpStore, N4AnUnreadSlotRefusesPersistence) {
    command(spec::MSG_BIND_RX_COMMAND, 0, kTkA);
    serve();
    const int auth = nvm_store_status()->auth;
    ASSERT_TRUE(auth == 0 || auth == 1);
    const std::uint32_t other = auth == 0 ? NVM_SLOT_B : NVM_SLOT_A;
    fk = Fake{};
    persists = 0;
    nvm_fmodel_power_on();
    nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_A + kJournal);
    nvm_smodel_reset();
    nvm_fmodel_fault_at(other);
    nvm_fmodel_fault(NVM_F_READ_FAIL_AT, 1000u, 0u);
    acmp_config cfg = a.cfg;
    ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kStoreEnv));
    acmp_nvm_init(&glue, &a, NVM_G_BIND, &nvm_smodel_port);
    nvm_store_boot(&nvm_fmodel_port, &glue.port);
    EXPECT_TRUE(nvm_store_status()->phase == NVM_P_HELD && nvm_store_status()->unread != 0u)
        << "N4 a slot the boot cannot read holds the writer (F1 decision 2)";
    EXPECT_TRUE(a.sinks[0].bound && a.sinks[0].binding.talker_entity_id == kTkA && a.sinks[0].state == ACMP_PRB_W_AVAIL)
        << "N4 what the readable slot holds is still restored: the fast connect stands";
    unsigned ok = nvm_store_status()->commits_ok;
    command(spec::MSG_BIND_RX_COMMAND, 0, kTkB);
    EXPECT_TRUE(persists == 1u && a.sinks[0].binding.talker_entity_id == kTkB)
        << "N4 a new bind is answered and taken, and its record marked";
    serve(5000u);
    EXPECT_TRUE(nvm_store_status()->commits_ok == ok && nvm_store_status()->phase == NVM_P_HELD &&
                nvm_store_status()->dirty)
        << "N4 but nothing is written while the writer is held: persistence is refused";
    boot(MILAN_NVM_N_STREAM_IN);
    EXPECT_TRUE(a.sinks[0].bound && a.sinks[0].binding.talker_entity_id == kTkA)
        << "N4 a clean boot brings back the binding that was saved, not the refused one";
}

TEST_F(AcmpStore, N5ARecordTheCoreRefusesKeepsItsDefault) {
    command(spec::MSG_BIND_RX_COMMAND, MILAN_NVM_N_STREAM_IN - 1u, kTkA);
    serve();
    boot(MILAN_NVM_N_STREAM_IN - 1u);
    EXPECT_TRUE(nvm_store_status()->terminal == NVM_T_COMPLETE && nvm_store_status()->refused >= 1u)
        << "N5 a binding record of a sink the configuration lacks is refused (nvm_state.h REFUSED), the walk goes on";
}

TEST_F(AcmpStore, N6TheRollBackAndEveryOtherGroup) {
    std::uint8_t record[spec::BINDING_BYTES] = {0x01, 0, 0, 1};
    wire_put_be(record + 4, kTkA, 8);
    ASSERT_EQ(glue.port.apply(glue.port.ctx, NVM_G_BIND, 0, record, sizeof record), NVM_APPLIED)
        << "N6 a binding record applies through the port";
    EXPECT_EQ(glue.port.apply(glue.port.ctx, NVM_G_BIND, 0, record, sizeof record - 1u), NVM_REFUSED)
        << "N6 one of another length is refused";
    EXPECT_EQ(glue.port.rollback(glue.port.ctx, NVM_W_BIND), 0) << "N6 the binding walk's roll-back succeeds";
    EXPECT_FALSE(a.sinks[0].bound) << "N6 and drops what it applied";
    std::uint8_t payload[spec::BINDING_BYTES];
    EXPECT_EQ(glue.port.latch(glue.port.ctx, NVM_G_BIND, 0, payload, sizeof payload - 1u), 0)
        << "N6 a latch of another length gives nothing";
    EXPECT_EQ(glue.port.latch(glue.port.ctx, NVM_G_BIND, 0, payload, sizeof payload), 1) << "N6 the record's does";
    EXPECT_EQ(glue.port.latch(glue.port.ctx, NVM_G_BIND, MILAN_NVM_N_STREAM_IN, payload, sizeof payload), 0)
        << "N6 a latch of a sink the configuration lacks gives nothing: the staged bytes stand";
    nvm_smodel_ready(0);
    EXPECT_EQ(glue.port.model_ready(glue.port.ctx), 0) << "N6 the model's readiness is the other owners'";
    nvm_smodel_ready(1);
    const struct nvm_smodel_count before = *nvm_smodel_count();
    std::uint8_t cfgidx[NVM_PL_CFG] = {0, 0};
    static_cast<void>(glue.port.model_ready(glue.port.ctx));
    static_cast<void>(glue.port.apply(glue.port.ctx, NVM_G_CFG, 0, cfgidx, sizeof cfgidx));
    static_cast<void>(glue.port.settle(glue.port.ctx));
    static_cast<void>(glue.port.rollback(glue.port.ctx, NVM_W_D3));
    static_cast<void>(glue.port.latch(glue.port.ctx, NVM_G_CFG, 0, cfgidx, sizeof cfgidx));
    glue.port.release(glue.port.ctx);
    const struct nvm_smodel_count& after = *nvm_smodel_count();
    EXPECT_TRUE(after.applies == before.applies + 1u && after.settles == before.settles + 1u &&
                after.rollbacks == before.rollbacks + 1u && after.latches == before.latches + 1u &&
                after.releases == before.releases + 1u && after.unbinds == before.unbinds)
        << "N6 every other group, settle, the D3 roll-back and the release go to the other owners unchanged";
}

}  // namespace
