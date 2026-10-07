// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// acmp_walk.cpp - the firmware's ACMP core walked by the PROCESSOR's own ACMP
// stimulus and expectations (#665 lane F3, the differential; GoogleTest: one
// test per walked cell, and one per carried-over scenario).
//
// NOTHING HERE RESTATES THE PROCESSOR'S EXPECTATIONS. test_ctrl_firmware.py
// cuts, at build time, out of the pinned submodule (the pin and each file's
// blob are proved first):
//
//   pp_acmp_reuse.inc   tb/acmp_listener/sim_main.cpp: the doc's constants,
//                       the 56-byte ACMPDU builder `mk_pdu`, the stimulus,
//                       and the independent F05.3 matrix model (`M`,
//                       `Model::predict`) of Milan v1.2 Table 5.30, which the
//                       processor's MTXW walk grades its RTL with;
//   pp_disc_reuse.inc   tb/adp_engine/sim_main.cpp: the Table 5.54
//                       transcription `DISC`, every guard of 5.6.4.5 its own
//                       row;
//   pp_talker_reuse.inc tb/acmp_talker/sim_main.cpp: the F05.11 constants.
//
// THE LISTENER WALK (LW) runs the model and the firmware in lock step: every
// cell of Table 5.30 is reached through legitimate stimulus only, the row's
// event applied to both, and everything the firmware did compared with what
// the model predicts: the frames byte for byte, the sink's timer (kind by
// state, deadline relative to the event), the record (state, probing and ACMP
// status, the binding, the sent probe, the settled stream, the talker's
// discovered and registered state), the SRP start and stop, the discovery
// start and stop, the store's mark, and the notification. The firmware draws
// TMR_DELAY from its own generator; before each event it is set to the state
// that draws the model's scripted 777 ms, so deadlines compare exactly.
//
// MAPPING. The model's abstract EVT_TK_DISCOVERED and EVT_TK_DEPARTED are the
// firmware's ENTITY_AVAILABLE and ENTITY_DEPARTING through its discovery
// machine, so the firmware raises them only on a discovery transition: a cell
// whose row needs the talker discovered first (EVT_TK_DEPARTED) is reached
// with an unchecked EVT_TK_DISCOVERED step in both. A timer row in a state
// whose own timer is another is impossible by construction in both (the
// state names its one timer) and is reported, not walked; in a state with no
// timer the processor injects a spurious expiry and so does this walk.
//
// THE DIFFERENCES, each asserted to be exactly what it is, field for field:
//   LD1  UNBIND_RX_RESPONSE: the processor echoes the command's
//        talker_entity_id and talker_unique_id; Milan v1.2 Table 5.36 gives
//        both 0, and the firmware sends 0;
//   LD2  TMR_RETRY with the talker discovered (5.5.3.5.30 step 2): the
//        processor's A12 sets the ACMP status to 0; step 2 sets none, so the
//        firmware keeps the status the retry was for (5.3.8.6: it reports the
//        last probe sequence's error while PROBING_ACTIVE);
//   LD3  CONTROLLER_NOT_AUTHORIZED: the processor sends status 13
//        (TALKER_MISBEHAVING in IEEE 1722.1-2021 Table 8-3); the firmware
//        sends 16, the table's CONTROLLER_NOT_AUTHORIZED;
//   TD1  DISCONNECT_TX of an unknown source: the processor answers SUCCESS;
//        Milan v1.2 5.5.4.2 step 1 and Table 5.44 answer TALKER_UNKNOWN_ID.
// Everything else agrees.
//
// THE DISCOVERY WALK (DW) drives every cell of the processor's Table 5.54
// transcription through the firmware's discovery machine with ADP frames,
// and grades the end state, the events raised to the connection machine (seen
// through it: in TK_NOT_DISCOVERED the sink waits in PRB_W_AVAIL, where
// EVT_TK_DISCOVERED starts TMR_DELAY; in TK_DISCOVERED it probes in
// PRB_W_RESP, where EVT_TK_DEPARTED returns it to PRB_W_AVAIL and the pair
// leaves it in PRB_W_DELAY), TMR_NO_ADP's arm or stop with the received
// valid_time, and the available_index noted.

#include <gtest/gtest.h>

#include <array>
#include <cctype>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include <tuple>
#include <vector>

#include "acmp.h"
#include "acmp_fake.hpp"
#include "fw_gtest.hpp"
#include "wire.h"

namespace pp_lsn {
#include "pp_acmp_reuse.inc"
}  // namespace pp_lsn

namespace pp_disc {
#include "pp_disc_reuse.inc"
}  // namespace pp_disc

namespace pp_tk {
#include "pp_talker_reuse.inc"
}  // namespace pp_tk

FW_TALLY_LABEL("ctrl ACMP walk (processor stimulus and models)");

using namespace acmp_test;

namespace {

// An xorshift32 state whose next TMR_DELAY draw is `ms` (the core's rule).
std::uint32_t state_drawing(std::uint32_t ms) {
    for (std::uint32_t s = 1;; ++s) {
        std::uint32_t x = s;
        x ^= x << 13;
        x ^= x >> 17;
        x ^= x << 5;
        if ((((x >> 16) * (spec::TMR_DELAY_MAX_MS + 1u)) >> 16) == ms) {
            return s;
        }
    }
}

const std::uint32_t kDraw777 = state_drawing(pp_lsn::DRAWVAL);

// ---- the listener walk ------------------------------------------------------------------

// The firmware's sink seen as the model's record.
struct Seen {
    int sm;
    int pbsta;
    int acmpsta;
    bool bound;
    bool started;
    bool sw;
    bool retried;
    bool tk_reg;
    bool tk_disc;
    int srp_decl;
    std::uint64_t talker_eid;
    std::uint64_t bind_ctlr;
    std::uint64_t sid;
    std::uint64_t da;
    std::uint16_t talker_uid;
    std::uint16_t probe_seq;
    std::uint16_t vlan;
};

Seen seen(const acmp& a, unsigned k) {
    const acmp_sink& s = a.sinks[k];
    acmp_sink_view v{};
    static_cast<void>(acmp_view(&a, k, &v));
    Seen r{};
    r.sm = s.state;
    r.pbsta = s.probing;
    r.acmpsta = s.acmp_status;
    r.bound = s.bound;
    r.started = s.started;
    r.sw = s.binding.streaming_wait;
    r.retried = s.probe_retried;
    r.tk_reg = v.talker_registered;
    r.tk_disc = s.discovered;
    r.srp_decl = (v.settled ? 1 : 0) | (v.registering_failed ? 2 : 0);   // settled: SRP listening
    r.talker_eid = s.binding.talker_entity_id;
    r.bind_ctlr = s.binding.controller_entity_id;
    r.sid = v.stream.stream_id;
    r.da = v.stream.dest_mac;
    r.vlan = v.stream.vlan_id;
    r.talker_uid = s.binding.talker_unique_id;
    r.probe_seq = s.probe_seq;
    return r;
}

// Table 5.22's STREAM_INPUT items of a model record: what a notification is due for.
struct Items {
    bool bound;
    bool started;
    int pbsta;
    int acmpsta;
    std::uint64_t sid;
    std::uint64_t da;
    std::uint16_t vlan;
    bool registered;
    bool failed;
    bool operator==(const Items& o) const {
        return bound == o.bound && started == o.started && pbsta == o.pbsta && acmpsta == o.acmpsta && sid == o.sid &&
               da == o.da && vlan == o.vlan && registered == o.registered && failed == o.failed;
    }
};

Items items(const pp_lsn::Rec& r) {
    bool settled = r.sm == pp_lsn::S_SNR || r.sm == pp_lsn::S_SOK;
    return Items{r.bound,     r.started,   r.pbsta, r.acmpsta, settled ? r.sid : 0u, settled ? r.da : 0u,
                 settled ? r.vlan : std::uint16_t{0}, r.sm == pp_lsn::S_SOK && r.tk_reg,
                 r.sm == pp_lsn::S_SOK && ((r.srp_decl >> 1) & 1) != 0};
}

class Lockstep {
 public:
    Lockstep() {
        fk = Fake{};
        fk.now = pp_lsn::NOW;
        cfg_.entity_id = pp_lsn::OUR_EID;
        cfg_.n_interfaces = 1;
        cfg_.mac[0] = kMac0;
        cfg_.n_sinks = pp_lsn::N_SINKS;
        EXPECT_TRUE(acmp_init(&a, &cfg_, &kPorts, &kEnv));
    }

    // One stimulus to sink k, both sides; returns the model's prediction.
    pp_lsn::Exp step(int k, const pp_lsn::Stim& s) {
        fk.clear();
        a.rng = kDraw777;
        a.seeded = true;
        t0 = fk.now;
        before = m.rec[k];
        if (s.k == pp_lsn::Stim::EXP) {
            armed_[k] = false;                           // an expiry consumes the timer it fires
        }
        pp_lsn::Exp e = m.predict(k, s);
        drive(k, s);
        return e;
    }

    void drive(int k, const pp_lsn::Stim& s) {
        if (s.k == pp_lsn::Stim::TXN) {
            pp_lsn::Pdu p = pp_lsn::mk_pdu(s.msg, s.status, s.sid, s.ctlr, s.tk_eid, s.target, s.tk_uid, s.uid, s.da,
                                           0, s.seq, s.flags, s.vlan);
            std::array<std::uint8_t, spec::FRAME_BYTES> f{};
            wire_put_be(f.data(), spec::MULTICAST_MAC, 6);
            wire_put_be(f.data() + 6, 0x0202DEADBEEFull, 6);
            wire_put_be(f.data() + 12, spec::ETHERTYPE, 2);
            std::memcpy(f.data() + spec::HEADER_BYTES, p.b, pp_lsn::PDU_BYTES);
            acmp_rx(&a, 0, f.data(), f.size());
        } else if (s.k == pp_lsn::Stim::EXP) {
            if (a.sinks[k].timer != ACMP_TIMER_NONE) {
                fk.now = a.sinks[k].timer_deadline;
            }
            t0 = fk.now;
            acmp_timer_expired(&a, 0);
        } else if (s.tk_kind == 0u) {                    // EVT_TK_DISCOVERED: a matching ENTITY_AVAILABLE
            Adp d;
            d.entity = a.sinks[k].binding.talker_entity_id;
            d.index = ++index_;
            auto f = adpdu(d);
            acmp_adp_rx(&a, 0, f.data(), f.size());
        } else if (s.tk_kind == 1u) {                    // EVT_TK_DEPARTED: its ENTITY_DEPARTING
            Adp d;
            d.msg = spec::ADPDU_ENTITY_DEPARTING;
            d.entity = a.sinks[k].binding.talker_entity_id;
            auto f = adpdu(d);
            acmp_adp_rx(&a, 0, f.data(), f.size());
        } else if (s.tk_kind == 2u) {
            acmp_tk_registered(&a, static_cast<unsigned>(k), s.tk_fail);
        } else {
            acmp_tk_unregistered(&a, static_cast<unsigned>(k));
        }
    }

    // Track the model's timer ops into the sink's armed deadline (relative to NOW).
    void model_timer(const pp_lsn::Exp& e, int k) {
        for (const pp_lsn::TOp& op : e.tops) {
            armed_[k] = !op.cancel;
            rel_[k] = op.deadline - pp_lsn::NOW;
        }
    }

    // The unchecked steps that bring sink k to Table 5.30's column `st`, the
    // processor's goto_state with its EVT_TK_* mapped onto discovery.
    void goto_state(int k, int st, bool discovered) {
        using namespace pp_lsn;
        auto sync = [&](const Stim& s) {
            Exp e = step(k, s);
            model_timer(e, k);
            EXPECT_EQ(a.sinks[k].state, m.rec[k].sm) << "LW(setup) state sync";
        };
        if (st == S_UNB) {
            return;
        }
        sync(bind(k, TK_A, TKUID_A, CTL1, false));
        if (st == S_PWA || st == S_PWD) {
            sync(tk(0));
            sync(tk(1));
            if (st == S_PWD) {
                sync(tk(0));
            }
            return;
        }
        if (discovered) {
            sync(tk(0));                                 // noted in PRB_W_RESP
        }
        if (st == S_PW2) {
            sync(exp());
        } else if (st == S_PWT) {
            sync(probe(k, ST_NOBW));
        } else if (st == S_SNR || st == S_SOK) {
            sync(probe(k, ST_OK));
            if (st == S_SOK) {
                sync(tk(2));
            }
        }
    }

    static pp_lsn::Stim bind(int k, std::uint64_t tk, std::uint16_t tu, std::uint64_t ct, bool sw) {
        pp_lsn::Stim s;
        s.k = pp_lsn::Stim::TXN;
        s.msg = pp_lsn::M_BIND;
        s.tk_eid = tk;
        s.tk_uid = tu;
        s.ctlr = ct;
        s.flags = sw ? 0x0008 : 0;
        s.seq = 0x4100;
        s.uid = static_cast<std::uint16_t>(k);
        return s;
    }
    static pp_lsn::Stim unbind(int k) {
        pp_lsn::Stim s;
        s.k = pp_lsn::Stim::TXN;
        s.msg = pp_lsn::M_UNBIND;
        s.ctlr = pp_lsn::CTL1;
        s.tk_eid = pp_lsn::TK_A;
        s.tk_uid = pp_lsn::TKUID_A;
        s.seq = 0x4200;
        s.uid = static_cast<std::uint16_t>(k);
        return s;
    }
    static pp_lsn::Stim getrx(int k) {
        pp_lsn::Stim s;
        s.k = pp_lsn::Stim::TXN;
        s.msg = pp_lsn::M_GETRX;
        s.ctlr = pp_lsn::CTL2;
        s.seq = 0x4300;
        s.uid = static_cast<std::uint16_t>(k);
        return s;
    }
    pp_lsn::Stim probe(int k, std::uint8_t status) const {
        const pp_lsn::Rec& r = m.rec[k];
        pp_lsn::Stim s;
        s.k = pp_lsn::Stim::TXN;
        s.msg = pp_lsn::M_PROBE_RESP;
        s.status = status;
        s.ctlr = r.bind_ctlr;
        s.tk_eid = r.talker_eid;
        s.tk_uid = r.talker_uid;
        s.seq = r.probe_seq;
        s.sid = 0x5544332211002233ull + static_cast<std::uint64_t>(k);
        s.da = 0x91E0F0004455ull;
        s.vlan = 2;
        s.uid = static_cast<std::uint16_t>(k);
        return s;
    }
    static pp_lsn::Stim exp() {
        pp_lsn::Stim s;
        s.k = pp_lsn::Stim::EXP;
        return s;
    }
    static pp_lsn::Stim tk(std::uint8_t kind, bool fail = false) {
        pp_lsn::Stim s;
        s.k = pp_lsn::Stim::TK;
        s.tk_kind = kind;
        s.tk_fail = fail;
        return s;
    }

    acmp a{};
    pp_lsn::Model m;
    pp_lsn::Rec before;
    std::uint32_t t0 = 0;
    bool armed_[pp_lsn::N_SINKS] = {};
    std::uint32_t rel_[pp_lsn::N_SINKS] = {};

 private:
    acmp_config cfg_{};
    std::uint32_t index_ = 0;
};

// Every row's stimulus, from the processor's own helpers' values.
pp_lsn::Stim row_stim(const Lockstep& w, int k, int row) {
    using namespace pp_lsn;
    switch (row) {
    case R_BIND_SAME: return Lockstep::bind(k, TK_A, TKUID_A, CTL1, false);
    case R_BIND_NEW: return Lockstep::bind(k, TK_B, TKUID_B, CTL2, true);
    case R_UNBIND: return Lockstep::unbind(k);
    case R_GETRX: return Lockstep::getrx(k);
    case R_PROBE_OK: return w.probe(k, ST_OK);
    case R_PROBE_FAIL: return w.probe(k, ST_NOBW);
    case R_TK_DISC: return Lockstep::tk(0);
    case R_TK_DEP: return Lockstep::tk(1);
    case R_TK_REG: return Lockstep::tk(2, true);
    case R_TK_UNREG: return Lockstep::tk(3);
    default: return Lockstep::exp();
    }
}

// The one timer row of each state (Table 5.29), or -1 for a state with none.
int own_timer_row(int st) {
    using namespace pp_lsn;
    switch (st) {
    case S_PWD: return R_TMR_DELAY;
    case S_PWR:
    case S_PW2: return R_TMR_CMD;
    case S_PWT: return R_TMR_RETRY;
    case S_SNR: return R_TMR_NOTK;
    default: return -1;
    }
}

bool timer_row(int row) {
    return row >= pp_lsn::R_TMR_DELAY && row <= pp_lsn::R_TMR_NOTK;
}

using LCell = std::tuple<int, int, bool>;   // row, state, talker discovered when the event comes

class ListenerWalk : public ::testing::TestWithParam<LCell> {};

TEST_P(ListenerWalk, Graded) {
    using namespace pp_lsn;
    const int row = std::get<0>(GetParam());
    const int st = std::get<1>(GetParam());
    const bool disc = std::get<2>(GetParam());
    const int k = 0;
    const std::string cell = std::string(RN[row]) + " x " + SN[st] + (disc ? " (talker discovered)" : "");
    Lockstep w;
    w.goto_state(k, st, disc || row == R_TK_DEP);
    ASSERT_EQ(w.a.sinks[k].state, w.m.rec[k].sm) << "LW " << cell << ": reached";
    if (timer_row(row) && own_timer_row(st) != row) {
        // a state with no timer gets a spurious expiry; any other row is the
        // state's own timer's alone, so its expiry cannot exist
        ASSERT_EQ(M[row][st].t, C_DASH) << "LW " << cell << ": the model marks the foreign expiry impossible";
        ASSERT_TRUE(own_timer_row(st) < 0 && row == R_TMR_CMD) << "LW " << cell << ": walked once per timerless state";
    }
    Exp e = w.step(k, row_stim(w, k, row));
    w.model_timer(e, k);

    // LD1: the processor echoes UNBIND_RX_RESPONSE's talker fields; Table 5.36 gives 0
    for (pp_lsn::Pdu& f : e.frames) {
        if ((f.b[1] & 0x0Fu) == M_UNBIND_R && (f.b[2] >> 3) == ST_OK) {
            bool echoed = wire_be64(f.b + 20) == TK_A && wire_be16(f.b + 36) == TKUID_A;
            EXPECT_TRUE(echoed) << "LD1 " << cell << ": the processor echoes the command's talker fields";
            std::memset(f.b + 20, 0, 8);
            std::memset(f.b + 36, 0, 2);
        }
    }
    // LD2: TMR_RETRY, talker discovered: the processor's A12 zeroes the ACMP status
    bool ld2 = row == R_TMR_RETRY && st == S_PWT && w.before.tk_disc;
    if (ld2) {
        EXPECT_TRUE(w.m.rec[k].acmpsta == 0 && w.before.acmpsta == ST_NOBW)
            << "LD2 " << cell << ": the processor zeroes the status the retry was for";
        w.m.rec[k].acmpsta = w.before.acmpsta;
    }

    ASSERT_EQ(fk.sent.size(), e.frames.size()) << "LW " << cell << ": frames";
    for (std::size_t i = 0; i < e.frames.size(); ++i) {
        EXPECT_EQ(std::memcmp(fk.sent[i].bytes.data() + spec::HEADER_BYTES, e.frames[i].b, PDU_BYTES), 0)
            << "LW " << cell << ": frame " << i << " byte for byte";
    }
    const acmp_sink& s = w.a.sinks[k];
    bool fw_armed = s.timer != ACMP_TIMER_NONE;
    EXPECT_EQ(fw_armed, w.armed_[k]) << "LW " << cell << ": the sink's timer armed or not";
    if (fw_armed && w.armed_[k]) {
        EXPECT_EQ(s.timer_deadline - w.t0, w.rel_[k]) << "LW " << cell << ": the timer's deadline";
    }
    const Rec& r = w.m.rec[k];
    Seen g = seen(w.a, k);
    EXPECT_TRUE(g.sm == r.sm && g.pbsta == r.pbsta && g.acmpsta == r.acmpsta)
        << "LW " << cell << ": state, probing and ACMP status " << SN[g.sm & 7] << " " << g.pbsta << " " << g.acmpsta
        << " want " << SN[r.sm & 7] << " " << unsigned(r.pbsta) << " " << unsigned(r.acmpsta);
    EXPECT_TRUE(g.bound == r.bound && g.started == r.started && g.sw == r.sw && g.talker_eid == r.talker_eid &&
                g.talker_uid == r.talker_uid && g.bind_ctlr == r.bind_ctlr)
        << "LW " << cell << ": the binding";
    EXPECT_TRUE(!r.bound || (g.probe_seq == r.probe_seq && g.retried == r.retried))
        << "LW " << cell << ": the sent probe's sequence_id and its duplicate";
    EXPECT_TRUE(g.sid == r.sid && g.da == r.da && g.vlan == r.vlan) << "LW " << cell << ": the settled stream";
    EXPECT_TRUE(g.tk_disc == r.tk_disc && g.tk_reg == (r.sm == S_SOK && r.tk_reg) &&
                g.srp_decl == (r.sm == S_SOK ? r.srp_decl : (r.srp_decl & 1)))
        << "LW " << cell << ": the talker's discovered and registered state";
    int srp = fk.position(Call::SRP);
    EXPECT_EQ(srp >= 0 && fk.calls[static_cast<unsigned>(srp)].flag, e.settle) << "LW " << cell << ": SRP started";
    if (e.settle && srp >= 0) {
        const acmp_stream& got = fk.calls[static_cast<unsigned>(srp)].stream;
        EXPECT_TRUE(got.stream_id == e.settle_sid && got.dest_mac == e.settle_da && got.vlan_id == e.settle_vlan)
            << "LW " << cell << ": with the response's stream";
    }
    EXPECT_EQ(srp >= 0 && !fk.calls[static_cast<unsigned>(srp)].flag, e.teardown) << "LW " << cell << ": SRP stopped";
    EXPECT_EQ(s.disc_running, r.bound) << "LW " << cell << ": discovery runs exactly while the sink is bound (A4, A9)";
    EXPECT_TRUE(!e.disc_arm || (s.disc_running && !s.discovered && !s.adp_armed))
        << "LW " << cell << ": an armed discovery starts with the talker not discovered";
    EXPECT_EQ(fk.count(Call::PERSIST) != 0u, e.nvm) << "LW " << cell << ": the store marked";
    EXPECT_EQ(fk.count(Call::CHANGED) != 0u, !(items(w.before) == items(r)))
        << "LW " << cell << ": notified exactly when a Table 5.22 item moved";
}

std::vector<LCell> listener_cells() {
    using namespace pp_lsn;
    std::vector<LCell> cells;
    for (int row = 0; row < N_ROWS; ++row) {
        for (int st = 0; st < N_STATES; ++st) {
            if (M[row][st].t == C_DASH && !timer_row(row) && row != R_TK_REG && row != R_TK_UNREG &&
                row != R_TK_DISC) {
                continue;                                // BIND_SAME x UNB, TK_DEP x UNB/PWA: no stimulus exists
            }
            if (timer_row(row) && own_timer_row(st) != row && !(own_timer_row(st) < 0 && row == R_TMR_CMD)) {
                continue;
            }
            cells.emplace_back(row, st, false);
        }
    }
    // the dagger cells' other arm: the talker discovered when the timer or event comes
    cells.emplace_back(R_TMR_RETRY, S_PWT, true);
    cells.emplace_back(R_TMR_NOTK, S_SNR, true);
    cells.emplace_back(R_TK_UNREG, S_SOK, true);
    return cells;
}

std::string lcell_name(const ::testing::TestParamInfo<LCell>& info) {
    std::string n = std::string(pp_lsn::RN[std::get<0>(info.param)]) + "_" + pp_lsn::SN[std::get<1>(info.param)] +
                    (std::get<2>(info.param) ? "_disc" : "");
    for (char& c : n) {
        c = std::isalnum(static_cast<unsigned char>(c)) != 0 ? c : '_';
    }
    return n;
}

INSTANTIATE_TEST_SUITE_P(Table530, ListenerWalk, ::testing::ValuesIn(listener_cells()), lcell_name);

// LD3: the lock's refusal, both ways.
TEST(ListenerScenario, LD3TheLockRefusalStatus) {
    using namespace pp_lsn;
    Lockstep w;
    w.m.lock_held = true;
    w.m.lock_eid = CTL2;
    fk.locked = true;
    fk.holder = CTL2;
    Exp e = w.step(0, Lockstep::bind(0, TK_A, TKUID_A, CTL1, false));
    ASSERT_TRUE(e.frames.size() == 1u && fk.sent.size() == 1u) << "LD3 one refusal each";
    EXPECT_EQ(e.frames[0].b[2] >> 3, ST_NOAUTH) << "LD3 the processor's status is its ST_NOAUTH";
    EXPECT_EQ(ST_NOAUTH, 13) << "LD3 which is 13, TALKER_MISBEHAVING in IEEE 1722.1-2021 Table 8-3";
    EXPECT_EQ(fk.sent[0].bytes[16] >> 3, spec::STATUS_CONTROLLER_NOT_AUTHORIZED)
        << "LD3 the firmware sends 16, CONTROLLER_NOT_AUTHORIZED";
    e.frames[0].b[2] = static_cast<std::uint8_t>((spec::STATUS_CONTROLLER_NOT_AUTHORIZED << 3) | (e.frames[0].b[2] & 7u));
    EXPECT_EQ(std::memcmp(fk.sent[0].bytes.data() + spec::HEADER_BYTES, e.frames[0].b, PDU_BYTES), 0)
        << "LD3 and every other byte agrees";
    EXPECT_TRUE(w.a.sinks[0].state == ACMP_UNBOUND && w.m.rec[0].sm == S_UNB) << "LD3 nothing bound on either side";
}

// The probe guard per term and an unknown sink, from the processor's B8, B13, B14.
TEST(ListenerScenario, LW2GuardsUnknownSinksAndForeignMessages) {
    using namespace pp_lsn;
    Lockstep w;
    w.goto_state(0, S_PWR, false);
    for (int term = 0; term < 4; ++term) {
        Stim p = w.probe(0, ST_OK);
        p.ctlr ^= term == 0 ? 1u : 0u;
        p.tk_eid ^= term == 1 ? 1u : 0u;
        p.tk_uid = static_cast<std::uint16_t>(p.tk_uid ^ (term == 2 ? 1u : 0u));
        p.seq = static_cast<std::uint16_t>(p.seq ^ (term == 3 ? 1u : 0u));
        Exp e = w.step(0, p);
        EXPECT_TRUE(e.frames.empty() && fk.sent.empty() && w.a.sinks[0].state == ACMP_PRB_W_RESP &&
                    w.m.rec[0].sm == S_PWR)
            << "LW2 a probe response wrong in guard term " << term << " is ignored on both sides";
    }
    Stim unknown = Lockstep::getrx(N_SINKS);
    Exp e = w.step(0, unknown);
    ASSERT_TRUE(e.frames.size() == 1u && fk.sent.size() == 1u);
    EXPECT_EQ(std::memcmp(fk.sent[0].bytes.data() + spec::HEADER_BYTES, e.frames[0].b, PDU_BYTES), 0)
        << "LW2 LISTENER_UNKNOWN_ID byte for byte";
    for (std::uint8_t msg : {3, 5, 7, 9, 11, 13, 14, 15}) {
        Stim f = w.probe(0, ST_OK);
        f.msg = msg;
        e = w.step(0, f);
        EXPECT_TRUE(e.frames.empty() && fk.sent.empty() && w.a.sinks[0].state == ACMP_PRB_W_RESP)
            << "LW2 message type " << unsigned(msg) << " shaped as the perfect answer is inert on both sides";
    }
}

// ---- the discovery walk -----------------------------------------------------------------

using DCell = std::tuple<int, int>;   // row, column

class DiscoveryWalk : public ::testing::TestWithParam<DCell> {};

TEST_P(DiscoveryWalk, Graded) {
    using namespace pp_disc;
    const int row = std::get<0>(GetParam());
    const int col = std::get<1>(GetParam());
    const DiscCell& c = DISC[row][col];
    const std::string cell = std::string(DRN[row]) + " x " + DCN[col];
    fk = Fake{};
    acmp a{};
    acmp_config cfg{};
    cfg.entity_id = kOwn;
    cfg.n_interfaces = 1;
    cfg.mac[0] = kMac0;
    cfg.n_sinks = 1;
    ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kEnv));
    a.rng = kDraw777;
    a.seeded = true;
    auto ingest = [&](const Adp& d) {
        auto f = adpdu(d);
        acmp_adp_rx(&a, 0, f.data(), f.size());
    };
    auto command = [&](std::uint8_t msg) {
        Pdu p;
        p.msg = msg;
        p.controller = kCtl1;
        p.talker = kTkA;
        p.listener = kOwn;
        p.talker_uid = 1;
        auto f = acmpdu(p);
        acmp_rx(&a, 0, f.data(), f.size());
    };
    // the column: unbound; TK_NOT_DISCOVERED waiting in PRB_W_AVAIL; TK_DISCOVERED
    // probing in PRB_W_RESP with DISC_LAST noted
    if (col == D_NOT) {
        std::uint8_t record[spec::BINDING_BYTES] = {0x01, 0, 0, 1};
        wire_put_be(record + 4, kTkA, 8);
        wire_put_be(record + 12, kCtl1, 8);
        ASSERT_EQ(acmp_restore_binding(&a, 0, record, sizeof record), ACMP_RESTORE_APPLIED);
    } else if (col == D_DISC) {
        command(spec::MSG_BIND_RX_COMMAND);
        Adp d;
        d.index = DISC_LAST;
        d.interface_index = 2;
        ingest(d);
        ASSERT_TRUE(a.sinks[0].discovered && a.sinks[0].state == ACMP_PRB_W_RESP);
    }
    const acmp_sink& s = a.sinks[0];
    const bool armed_before = s.adp_armed;
    const std::uint32_t deadline_before = s.adp_deadline;
    const acmp_sink_state state_before = s.state;
    if (c.cls == 'C') {
        // the binding is already so: the processor proves the precondition, and so does this walk
        EXPECT_EQ(s.bound, row == V_BIND) << "DW " << cell << ": impossible by construction";
        return;
    }
    fk.now += 1000;
    const std::uint32_t t = fk.now;
    Adp d;
    d.valid_time = 7;
    d.interface_index = 2;
    switch (row) {
    case V_FRESH: d.index = DISC_LAST + 1u; ingest(d); break;
    case V_STALE: d.index = DISC_LAST - 1u; ingest(d); break;
    case V_GMF: d.index = DISC_LAST + 1u; d.gm = kGm0 + 1u; ingest(d); break;
    case V_GMS: d.index = DISC_LAST - 1u; d.gm = kGm0 + 1u; ingest(d); break;
    case V_DOMS: d.index = DISC_LAST - 1u; d.domain = 5; ingest(d); break;
    case V_IFX: d.index = DISC_LAST + 1u; d.interface_index = 3; ingest(d); break;
    case V_DEP: d.msg = spec::ADPDU_ENTITY_DEPARTING; ingest(d); break;
    case V_DEPIFX: d.msg = spec::ADPDU_ENTITY_DEPARTING; d.interface_index = 3; ingest(d); break;
    case V_NOADP:
        if (s.adp_armed) {
            fk.now = s.adp_deadline;
        }
        acmp_timer_expired(&a, 0);                       // a stray where nothing is armed
        break;
    case V_UNBIND: command(spec::MSG_UNBIND_RX_COMMAND); break;
    default: command(spec::MSG_BIND_RX_COMMAND); break;  // V_BIND
    }
    const int to = !s.bound ? D_UNB : (s.discovered ? D_DISC : D_NOT);
    EXPECT_EQ(to, c.to) << "DW " << cell << ": the discovery state (" << c.milan << ")";
    // the events, seen through the connection machine (see the top of the file)
    int ev = EV_NONE;
    if (col == D_NOT && state_before == ACMP_PRB_W_AVAIL && s.state == ACMP_PRB_W_DELAY) {
        ev = EV_DISC;
    } else if (col == D_DISC && s.bound && state_before == ACMP_PRB_W_RESP && s.state == ACMP_PRB_W_AVAIL) {
        ev = EV_DEP;
    } else if (col == D_DISC && s.bound && state_before == ACMP_PRB_W_RESP && s.state == ACMP_PRB_W_DELAY) {
        ev = EV_PAIR;
    }
    EXPECT_EQ(ev, c.evs) << "DW " << cell << ": the events raised to the connection machine";
    if (c.tm == TM_ARM) {
        EXPECT_TRUE(s.adp_armed && s.adp_deadline == t + 7u * spec::VALID_TIME_UNIT_MS)
            << "DW " << cell << ": TMR_NO_ADP armed from the received valid_time (6.2.2.5)";
    } else if (c.tm == TM_CANCEL) {
        EXPECT_FALSE(s.adp_armed) << "DW " << cell << ": TMR_NO_ADP stopped";
    } else {
        EXPECT_TRUE(s.adp_armed == (armed_before && to == D_DISC) && (!s.adp_armed || s.adp_deadline == deadline_before))
            << "DW " << cell << ": TMR_NO_ADP untouched";
    }
    if (notes_index(row, col)) {
        EXPECT_EQ(s.disc_available_index, noted_index(row)) << "DW " << cell << ": the available_index noted";
    } else if (col == D_DISC && to == D_DISC) {
        EXPECT_EQ(s.disc_available_index, DISC_LAST) << "DW " << cell << ": the available_index kept";
    }
}

std::vector<DCell> discovery_cells() {
    std::vector<DCell> cells;
    for (int row = 0; row < pp_disc::N_DROW; ++row) {
        for (int col = 0; col < pp_disc::N_DCOL; ++col) {
            cells.emplace_back(row, col);
        }
    }
    return cells;
}

std::string dcell_name(const ::testing::TestParamInfo<DCell>& info) {
    std::string n = std::string(pp_disc::DRN[std::get<0>(info.param)]) + "_" + pp_disc::DCN[std::get<1>(info.param)];
    std::string out;
    for (char ch : n) {
        out += std::isalnum(static_cast<unsigned char>(ch)) != 0 ? ch : '_';
    }
    return out;
}

INSTANTIATE_TEST_SUITE_P(Table554, DiscoveryWalk, ::testing::ValuesIn(discovery_cells()), dcell_name);

// ---- the talker, against the F05.11 constants ----------------------------------------------

class TalkerWalk : public ::testing::Test {
 protected:
    void SetUp() override {
        fk = Fake{};
        cfg.entity_id = pp_tk::OWN_EID;
        cfg.n_interfaces = 2;
        cfg.mac[0] = kMac0;
        cfg.mac[1] = kMac1;
        cfg.n_sources = pp_tk::N_SRC;
        cfg.source_interface[pp_tk::N_SRC - 1] = 1;
        for (int s = 0; s < pp_tk::N_SRC; ++s) {
            fk.source[s] = acmp_source_state{true, {pp_tk::sid_of(s), pp_tk::da_pool(s), pp_tk::VID}, false};
        }
        ASSERT_TRUE(acmp_init(&a, &cfg, &kPorts, &kEnv));
    }
    Pdu ask(int msg, int src, std::uint16_t flags, unsigned interface = 0) {
        Pdu p;
        p.msg = static_cast<std::uint8_t>(msg);
        p.controller = kCtl1;
        p.talker = pp_tk::OWN_EID;
        p.listener = kTkB;
        p.talker_uid = static_cast<std::uint16_t>(src);
        p.listener_uid = 4;
        p.seq = 0x2222;
        p.flags = flags;
        fk.clear();
        auto f = acmpdu(p);
        acmp_rx(&a, interface, f.data(), f.size());
        return fk.sent.empty() ? Pdu{} : read(fk.sent.back().bytes.data());
    }
    acmp a{};
    acmp_config cfg{};
};

TEST_F(TalkerWalk, TW1ProbeTheFlagLawAndTheSource) {
    Pdu r = ask(pp_tk::MT_PROBE, 2, 0xFFFFu);
    EXPECT_TRUE(r.msg == pp_tk::MT_PROBE + 1 && r.status == pp_tk::ST_OK &&
                r.flags == (pp_tk::FL_FC | pp_tk::FL_SW) && r.count == 0u && r.stream_id == pp_tk::sid_of(2) &&
                r.dest_mac == pp_tk::da_pool(2) && r.vlan == pp_tk::VID && r.listener == kTkB && r.listener_uid == 4u)
        << "TW1 PROBE_TX: SUCCESS, FAST_CONNECT and STREAMING_WAIT echoed, REGISTERING_FAILED forced 0, the source's "
           "stream (F05.11; Milan v1.2 Table 5.43)";
    fk.source[2].dest_mac_valid = false;
    r = ask(pp_tk::MT_PROBE, 2, 0);
    EXPECT_EQ(r.status, pp_tk::ST_DMAC_FAIL) << "TW1 no destination MAC: TALKER_DEST_MAC_FAILED (Table 5.42)";
    r = ask(pp_tk::MT_PROBE, pp_tk::N_SRC, 0);
    EXPECT_EQ(r.status, pp_tk::ST_TK_UNKNOWN) << "TW1 an unknown source: TALKER_UNKNOWN_ID (Table 5.40)";
}

TEST_F(TalkerWalk, TW2GetTxStateReadsRegisteringFailedLive) {
    fk.source[3].asking_failed = true;
    Pdu r = ask(pp_tk::MT_GTXS, 3, 0xFFFFu);
    EXPECT_TRUE(r.status == pp_tk::ST_OK && r.flags == pp_tk::FL_RF && r.listener == 0u && r.listener_uid == 0u &&
                r.stream_id == pp_tk::sid_of(3) && r.vlan == pp_tk::VID)
        << "TW2 GET_TX_STATE: listener fields 0, REGISTERING_FAILED live from Asking Failed (Table 5.47)";
    fk.source[3].asking_failed = false;
    r = ask(pp_tk::MT_GTXS, 3, 0);
    EXPECT_EQ(r.flags, 0u) << "TW2 and clear without it";
    r = ask(pp_tk::MT_GTXS, pp_tk::N_SRC, 0);
    EXPECT_EQ(r.status, pp_tk::ST_TK_UNKNOWN) << "TW2 an unknown source: TALKER_UNKNOWN_ID (Table 5.46)";
}

TEST_F(TalkerWalk, TW3DisconnectAndGetTxConnection) {
    Pdu r = ask(pp_tk::MT_DISC, 1, 0xFFFFu);
    EXPECT_TRUE(r.status == pp_tk::ST_OK && r.flags == 0u && r.count == 0u && r.stream_id == 0u)
        << "TW3 DISCONNECT_TX: SUCCESS, nothing changes (Table 5.45)";
    r = ask(pp_tk::MT_DISC, pp_tk::N_SRC, 0);
    EXPECT_EQ(r.status, pp_tk::ST_TK_UNKNOWN)
        << "TD1 DISCONNECT_TX of an unknown source: TALKER_UNKNOWN_ID (Milan v1.2 5.5.4.2 step 1, Table 5.44); the "
           "processor answers SUCCESS";
    r = ask(pp_tk::MT_GTXC, 1, 0);
    EXPECT_EQ(r.status, pp_tk::ST_NSUPP) << "TW3 GET_TX_CONNECTION: NOT_SUPPORTED (Table 5.48)";
}

TEST_F(TalkerWalk, TW4TheInterfaceAndTheStatelessProperty) {
    Pdu r = ask(pp_tk::MT_PROBE, pp_tk::N_SRC - 1, 0, 0);
    EXPECT_EQ(r.status, spec::STATUS_INCOMPATIBLE_REQUEST)
        << "TW4 a probe from another interface than the source's is answered INCOMPATIBLE_REQUEST (Table 5.41), "
           "5.5.4.1 step 2's other choice than the processor's silence";
    Pdu first = ask(pp_tk::MT_GTXS, 5, 0);
    static_cast<void>(ask(pp_tk::MT_PROBE, 5, 0));
    static_cast<void>(ask(pp_tk::MT_DISC, 5, 0));
    Pdu again = ask(pp_tk::MT_GTXS, 5, 0);
    EXPECT_TRUE(same(first, again)) << "TW4 the same query around other traffic: the same answer (5.5.2.7)";
}

}  // namespace
