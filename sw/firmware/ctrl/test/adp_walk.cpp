// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// adp_walk.cpp - the firmware ADP slice walked by the PROCESSOR's own ADP
// stimulus and expectations, through the mailbox model (#665 lanes F0 and FT;
// GoogleTest: one test per walked cell, and one per carried-over scenario).
//
// NOTHING HERE RESTATES THE PROCESSOR'S EXPECTATIONS. pp_adp_reuse.inc is cut
// by test_ctrl_firmware.py, at build time, out of the pinned submodule's
// tb/adp_engine/sim_main.cpp (the pin and the file's blob are proved first):
// its fixed entity configuration, its independent 82-byte ADPDU builder
// (`model_frame`, written from the processor's 04 section 3 field table) and
// its Milan v1.2 Table 5.51 transcription (`ADV[row][col]`, each cell's class,
// end state, draws, arms, cancel rule and frame). This file only drives the
// firmware into each cell's state through the mailbox, applies the row's
// event the way the fabric would deliver it, and compares what the firmware
// did with the cell.
//
// Column map. NOT STARTED, DOWN, WAITING and DELAY (timer armed) are walked.
// The processor's "DELAY, draw in flight" column has no firmware counterpart:
// the firmware draws and arms inside one call (adp.c enter_delay), so no
// event can reach the machine between the draw and the arm; its nine cells
// are reported as not applicable, with that reason, rather than walked.
//
// Mapping of the cell classes onto the mailbox: an 'S' stray is an expiry
// whose arm is no longer current, posted into the event ring with a tag the
// firmware did not issue; a 'C' cell checks the precondition that rules the
// event out (link level, enable level, or what the one timer holds).

#include <gtest/gtest.h>

#include <algorithm>
#include <cctype>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "ctrl_app.h"
#include "fw_gtest.hpp"
#include "mbx_model.h"
#include "mbx_wire.h"

namespace pp {
#include "pp_adp_reuse.inc"
}  // namespace pp

FW_TALLY_LABEL("ctrl ADP walk (processor stimulus, host model)");

namespace {

constexpr std::uint64_t kGm1 = 0x5150515051505150ull;
constexpr std::uint64_t kForeign = 0xF00DF00DF00DF00Dull;
constexpr unsigned kSlot = CTRL_APP_ADP_FIRST_SLOT;

//! What a cell window saw: timer operations on the ADP slot (and elsewhere),
//! frames sent, and the machine's counters.
struct Window {
    unsigned arms = 0;
    unsigned cancels = 0;
    unsigned foreign_ops = 0;
    std::uint32_t last_deadline = 0;
    std::uint32_t last_arm_now = 0;
    std::vector<std::vector<std::uint8_t>> frames;
};

class Walk {
 public:
    Walk() {
        entity_.entity_id = pp::EID;
        entity_.entity_model_id = pp::EMID;
        entity_.mac = pp::MAC;
        entity_.entity_capabilities = PP_ENTITY_CAPS;
        entity_.talker_stream_sources = pp::TKSRC;
        entity_.talker_capabilities = pp::TKCAP;
        entity_.listener_stream_sinks = pp::LSNK;
        entity_.listener_capabilities = pp::LSCAP;
        entity_.identify_control_index = pp::IDIX;
    }

    //! One cell of the table: driven into its column, the row's event applied, graded.
    void walk_cell(int row, int col);
    void check_boot_gate();
    void check_first_advert_and_cadence();
    void check_departing_and_restart();
    void check_config_index_bytes();

 private:
    mbx_model* m() { return model_.get(); }
    adp& machine() { return app_->adp.ifs[0].adp; }
    adp_mbx_if& adapter() { return app_->adp.ifs[0]; }

    void boot(bool link_up) {
        mbx_model_reset(m());
        mbx_model_bind(m(), nullptr, nullptr);
        mbx_model_set_gm(m(), 0, pp::GM0, pp::DOM0);
        mbx_model_set_link(m(), 0, link_up);
        ctrl_app_config cfg{&entity_, pp::CFGIX, arena_.data(), arena_.size(), classes_, 1, nullptr, nullptr, nullptr, nullptr};
        EXPECT_TRUE(ctrl_app_start(app_.get(), &cfg)) << "boot: the app starts on the model";
        settle();
    }
    void settle() {
        while (ctrl_loop_service(&app_->loop) != 0u) {}
    }
    //! Advance the model to the deadline of the ADP slot's current arm and serve.
    void expire_current() {
        const std::uint32_t dl = machine_deadline();
        mbx_model_advance_ms(m(), dl - m()->now_ms);
        settle();
    }
    std::uint32_t machine_deadline() {
        for (std::uint32_t k = m()->tmr_ops; k > 0; --k) {
            const struct mbx_model_tmr_op* op = mbx_model_tmr_op(m(), k - 1u);
            if (op != nullptr && op->slot == kSlot) {
                return op->op == MBX_TMR_OP_ARM ? op->deadline_ms : m()->now_ms;
            }
        }
        return m()->now_ms;
    }
    void to_column(int col);
    void prepare(int col, int row);
    void apply(int col, int row);
    void inject_stray() {
        const std::uint32_t tag = static_cast<std::uint32_t>(adapter().tag_seq) + 0x100u;
        mbx_model_write(m(), MBX_REG_TMR_DEADLINE, m()->now_ms, 0xF);
        mbx_model_write(m(), MBX_REG_TMR_CMD,
                        (MBX_TMR_OP_ARM << MBX_TMR_CMD_OP_LSB) | ((tag & 0xFFFFu) << MBX_TMR_CMD_TAG_LSB) | kSlot, 0xF);
    }
    Window observe(std::uint32_t ops0, std::uint32_t sent0);
    void grade(int row, int col, const pp::AdvCell& c, const Window& w, std::uint32_t aidx0, std::uint32_t draws0,
               std::uint32_t gm0);
    bool impossible_holds(int row, int col);
    std::vector<std::uint8_t> expected(bool departing, std::uint64_t gm, std::uint32_t aidx, std::uint16_t cfg) {
        std::vector<std::uint8_t> f(pp::kAdpduBytes);
        pp::model_frame(f.data(), departing, gm, pp::DOM0, aidx, cfg);
        return f;
    }

    adp_entity entity_{};
    std::unique_ptr<mbx_model> model_ = std::make_unique<mbx_model>();
    std::unique_ptr<ctrl_app> app_ = std::make_unique<ctrl_app>();
    std::vector<std::uint8_t> arena_ = std::vector<std::uint8_t>(1024 + 64);
    const ctrl_pool_class classes_[1] = {{32u, 8u}};
    char label_[160] = {};
};

const char* fmt(char* buf, std::size_t n, const char* what, int row, int col) {
    std::snprintf(buf, n, "%s x %s: %s", pp::ARN[row], pp::ACN[col], what);
    return buf;
}

void Walk::to_column(int col) {
    if (col == pp::A_NS) {
        boot(false);
        adp_mbx_set_enable(&app_->adp, false);
        settle();
        return;
    }
    if (col == pp::A_DOWN) {
        boot(false);
        return;
    }
    boot(false);
    mbx_model_set_link(m(), 0, true);
    settle();
    if (col == pp::A_WAIT) {
        expire_current();
    }
}

void Walk::prepare(int col, int row) {
    if (col == pp::A_NS && row == pp::R_LDN) {
        mbx_model_set_link(m(), 0, true);
        settle();
    }
    if ((col == pp::A_NS || col == pp::A_DOWN) && (row == pp::R_TADV || row == pp::R_TDLY)) {
        inject_stray();
    }
}

void Walk::apply(int col, int row) {
    std::vector<std::uint8_t> f(pp::kAdpduBytes, 0);
    switch (row) {
        case pp::R_DISC0:
        case pp::R_DISCOWN:
        case pp::R_DISCFOR:
            pp::putbe(f.data(), 0x91E0F0010000ull, 6);
            pp::putbe(f.data() + 12, 0x22F0, 2);
            f[14] = 0xFA;
            f[15] = 2;
            pp::putbe(f.data() + 18, row == pp::R_DISC0 ? 0u : (row == pp::R_DISCOWN ? pp::EID : kForeign), 8);
            static_cast<void>(mbx_model_rx(m(), f.data(), f.size(), 0));
            break;
        case pp::R_TADV:
        case pp::R_TDLY:
            if (col == pp::A_WAIT || col == pp::A_DLY) {
                expire_current();
            }
            break;
        case pp::R_LUP:
            mbx_model_set_link(m(), 0, true);
            break;
        case pp::R_LDN:
            mbx_model_set_link(m(), 0, false);
            break;
        case pp::R_GM:
            mbx_model_gm_change(m(), 0, kGm1, pp::DOM0);
            break;
        default:
            adp_mbx_set_enable(&app_->adp, false);
            break;
    }
    settle();
}

Window Walk::observe(std::uint32_t ops0, std::uint32_t sent0) {
    Window w;
    for (std::uint32_t k = ops0; k < m()->tmr_ops; ++k) {
        const struct mbx_model_tmr_op* op = mbx_model_tmr_op(m(), k);
        if (op->slot != kSlot) {
            ++w.foreign_ops;
        } else if (op->op == MBX_TMR_OP_ARM) {
            ++w.arms;
            w.last_deadline = op->deadline_ms;
            w.last_arm_now = op->now_ms;
        } else {
            ++w.cancels;
        }
    }
    for (std::uint32_t k = sent0; k < m()->tx_sent; ++k) {
        const mbx_model_tx* t = mbx_model_tx_frame(m(), k);
        w.frames.emplace_back(t->bytes, t->bytes + t->len);
    }
    return w;
}

bool Walk::impossible_holds(int row, int col) {
    switch (row) {
        case pp::R_TADV:
            return machine().timer == ADP_TIMER_DELAY;
        case pp::R_TDLY:
            return machine().timer == ADP_TIMER_ADVERTISE;
        case pp::R_LUP:
            return m()->link_up[0] && machine().link_up;
        case pp::R_LDN:
            return !m()->link_up[0] && !machine().link_up;
        default:
            return col == pp::A_NS && !machine().enabled;
    }
}

}  // namespace

namespace {

void Walk::grade(int row, int col, const pp::AdvCell& c, const Window& w, std::uint32_t aidx0, std::uint32_t draws0,
                 std::uint32_t gm0) {
    char b[sizeof label_];
    EXPECT_EQ(static_cast<std::uint64_t>(machine().state), static_cast<std::uint64_t>(c.to))
        << fmt(b, sizeof b, "advertise state after", row, col);
    EXPECT_EQ(static_cast<std::uint64_t>(machine().draws - draws0), static_cast<std::uint64_t>(c.draws))
        << fmt(b, sizeof b, "T-ADP-DELAY draws", row, col);
    if (c.draws > 0) {
        EXPECT_EQ(static_cast<std::uint64_t>(machine().last_draw), static_cast<std::uint64_t>(ADP_DRAW_DELAY))
            << fmt(b, sizeof b, "the draw is the 0..4 s kind", row, col);
    }
    EXPECT_EQ(static_cast<std::uint64_t>(w.arms), static_cast<std::uint64_t>(static_cast<unsigned>(c.arms)))
        << fmt(b, sizeof b, "arms of the shared slot", row, col);
    if (c.cancel_must) {
        EXPECT_TRUE(w.cancels >= 1u) << fmt(b, sizeof b, "the clause stops the timer: a cancel", row, col);
    }
    if (!c.cancel_may) {
        EXPECT_EQ(static_cast<std::uint64_t>(w.cancels), static_cast<std::uint64_t>(0))
            << fmt(b, sizeof b, "no cancel where the slot is untouched", row, col);
    }
    if (c.arms == 1 && w.arms == 1u) {
        const std::uint32_t want = c.draws == 1 ? machine().last_draw_ms : ADP_ADVERTISE_MS;
        EXPECT_EQ(static_cast<std::uint64_t>(w.last_deadline - w.last_arm_now), static_cast<std::uint64_t>(want))
            << fmt(b, sizeof b, "the arm is now + the draw, or + 5000 ms", row, col);
    }
    EXPECT_EQ(static_cast<std::uint64_t>(w.foreign_ops), static_cast<std::uint64_t>(0))
        << fmt(b, sizeof b, "no operation on any other slot", row, col);
    EXPECT_EQ(static_cast<std::uint64_t>(w.frames.size()), static_cast<std::uint64_t>(c.frame == 0 ? 0u : 1u))
        << fmt(b, sizeof b, "frames committed", row, col);
    if (c.frame != 0 && w.frames.size() == 1u) {
        EXPECT_TRUE(w.frames[0] == expected(c.frame == 2, pp::GM0, aidx0, pp::CFGIX))
            << fmt(b, sizeof b, "the frame is the processor's model_frame, byte for byte", row, col);
    }
    const std::uint32_t aidx = c.frame == 1 ? aidx0 + 1u : (c.frame == 2 ? 0u : aidx0);
    EXPECT_EQ(static_cast<std::uint64_t>(machine().available_index), static_cast<std::uint64_t>(aidx))
        << fmt(b, sizeof b, "available_index (+1, reset to 0, or unchanged)", row, col);
    EXPECT_EQ(static_cast<std::uint64_t>(machine().gm_changed - gm0),
              static_cast<std::uint64_t>(row == pp::R_GM ? 1u : 0u))
        << fmt(b, sizeof b, "GPTP_GM_CHANGED ticks on GM_CHANGE only", row, col);
}

void Walk::walk_cell(int row, int col) {
    const pp::AdvCell& c = pp::ADV[row][col];
    to_column(col);
    prepare(col, row);
    char b[sizeof label_];
    if (c.cls == 'C') {
        EXPECT_TRUE(impossible_holds(row, col)) << fmt(b, sizeof b, "cannot happen: its precondition holds", row, col);
        return;
    }
    const std::uint32_t ops0 = m()->tmr_ops;
    const std::uint32_t sent0 = m()->tx_sent;
    const std::uint32_t aidx0 = machine().available_index;
    const std::uint32_t draws0 = machine().draws;
    const std::uint32_t gm0 = machine().gm_changed;
    const std::uint32_t stale0 = adapter().stale_expiries;
    apply(col, row);
    grade(row, col, c, observe(ops0, sent0), aidx0, draws0, gm0);
    if (c.cls == 'S') {
        EXPECT_EQ(adapter().stale_expiries - stale0, 1u)
            << fmt(b, sizeof b, "the stray expiry is discarded by its tag", row, col);
    }
}

void Walk::check_boot_gate() {
    to_column(pp::A_NS);
    const std::uint32_t ops0 = m()->tmr_ops;
    const std::uint32_t sent0 = m()->tx_sent;
    mbx_model_set_link(m(), 0, true);
    for (unsigned k = 0; k < 4100u; ++k) {
        mbx_model_advance_ms(m(), 1);
        settle();
    }
    mbx_model_set_link(m(), 0, false);
    mbx_model_advance_ms(m(), 20);
    settle();
    mbx_model_set_link(m(), 0, true);
    for (unsigned k = 0; k < 4100u; ++k) {
        mbx_model_advance_ms(m(), 1);
        settle();
    }
    const Window w = observe(ops0, sent0);
    EXPECT_TRUE(w.arms == 0u && w.cancels == 0u && w.frames.empty() && machine().state == ADP_STATE_DOWN &&
                machine().draws == 0u)
        << "P12 boot gate: not started, 8.2 s of link up and a bounce move nothing (5.6.1)";
}

void Walk::check_first_advert_and_cadence() {
    boot(true);
    EXPECT_TRUE(machine().last_draw == ADP_DRAW_STARTUP && machine().last_draw_ms <= ADP_DELAY_STARTUP_MAX_MS)
        << "P1 startup with the link up draws the 0..2 s kind (5.6.3.5.2)";
    std::uint32_t sent0 = m()->tx_sent;
    expire_current();
    Window w = observe(m()->tmr_ops, sent0);
    EXPECT_TRUE(w.frames.size() == 1u && w.frames[0] == expected(false, pp::GM0, 0, pp::CFGIX))
        << "P2 the first ENTITY_AVAILABLE is the processor's model frame, index 0";
    for (std::uint32_t k = 1; k <= 3u; ++k) {
        const std::uint32_t before = m()->now_ms;
        expire_current();
        EXPECT_EQ(static_cast<std::uint64_t>(m()->now_ms - before), static_cast<std::uint64_t>(ADP_ADVERTISE_MS))
            << "P3 TMR_ADVERTISE fires 5000 ms after the send";
        EXPECT_TRUE(machine().state == ADP_STATE_DELAY && machine().last_draw == ADP_DRAW_DELAY &&
                    machine().last_draw_ms <= ADP_DELAY_MAX_MS)
            << "P3 into DELAY with a 0..4 s draw";
        sent0 = m()->tx_sent;
        expire_current();
        w = observe(m()->tmr_ops, sent0);
        EXPECT_TRUE(w.frames.size() == 1u && w.frames[0] == expected(false, pp::GM0, k, pp::CFGIX))
            << "P3 each cycle sends the model frame with the next index";
    }
    mbx_model_gm_change(m(), 0, kGm1, pp::DOM0);
    settle();
    sent0 = m()->tx_sent;
    expire_current();
    w = observe(m()->tmr_ops, sent0);
    EXPECT_TRUE(w.frames.size() == 1u && w.frames[0] == expected(false, kGm1, 4, pp::CFGIX))
        << "P5 GM_CHANGE re-advertises with the new grandmaster sampled at build (5.6.3.5.7)";
}

void Walk::check_departing_and_restart() {
    boot(true);
    expire_current();
    expire_current();
    expire_current();
    const std::uint32_t index = machine().available_index;
    std::uint32_t sent0 = m()->tx_sent;
    adp_mbx_set_enable(&app_->adp, false);
    settle();
    Window w = observe(m()->tmr_ops, sent0);
    EXPECT_TRUE(w.frames.size() == 1u && w.frames[0] == expected(true, pp::GM0, index, pp::CFGIX))
        << "P7 disable sends ENTITY_DEPARTING with the pre-reset index";
    adp_mbx_set_enable(&app_->adp, true);
    settle();
    sent0 = m()->tx_sent;
    expire_current();
    w = observe(m()->tmr_ops, sent0);
    EXPECT_TRUE(w.frames.size() == 1u && w.frames[0] == expected(false, pp::GM0, 0, pp::CFGIX))
        << "P7 the restart advertises from index 0";
}

void Walk::check_config_index_bytes() {
    boot(true);
    std::uint32_t sent0 = m()->tx_sent;
    expire_current();
    const Window a = observe(m()->tmr_ops, sent0);
    adp_set_current_configuration(&machine(), 0x0304);
    expire_current();
    sent0 = m()->tx_sent;
    expire_current();
    const Window b = observe(m()->tmr_ops, sent0);
    bool only = a.frames.size() == 1u && b.frames.size() == 1u;
    for (int i = 0; only && i < pp::kAdpduBytes; ++i) {
        const bool own = (i >= 50 && i <= 53) || i == 64 || i == 65;
        only = own || a.frames[0][static_cast<std::size_t>(i)] == b.frames[0][static_cast<std::size_t>(i)];
    }
    EXPECT_TRUE(only) << "P11 a configuration change moves only bytes 64..65 (and the index 50..53)";
    EXPECT_TRUE(b.frames.size() == 1u && b.frames[0] == expected(false, pp::GM0, 1, 0x0304))
        << "P11 and the frame is the model's at the new index";
}

//! Every cell of the table but the draw-in-flight column, which has no
//! firmware counterpart (see the top of this file).
std::vector<std::pair<int, int>> walked_cells() {
    std::vector<std::pair<int, int>> cells;
    for (int row = 0; row < pp::N_AROW; ++row) {
        for (int col = 0; col < pp::N_ACOL; ++col) {
            if (col != pp::A_DRAW) {
                cells.emplace_back(row, col);
            }
        }
    }
    return cells;
}

//! "ROW x COLUMN" as a test name: every run of other characters becomes one '_'.
std::string cell_name(const ::testing::TestParamInfo<std::pair<int, int>>& info) {
    const std::string text = std::string(pp::ARN[info.param.first]) + " x " + pp::ACN[info.param.second];
    std::string name;
    for (const char ch : text) {
        const bool keep = std::isalnum(static_cast<unsigned char>(ch)) != 0;
        if (keep) {
            name += ch;
        } else if (!name.empty() && name.back() != '_') {
            name += '_';
        }
    }
    while (!name.empty() && name.back() == '_') {
        name.pop_back();
    }
    return name;
}

class AdpWalkCell : public ::testing::TestWithParam<std::pair<int, int>> {};

TEST_P(AdpWalkCell, Graded) {
    Walk walk;
    walk.walk_cell(GetParam().first, GetParam().second);
}

INSTANTIATE_TEST_SUITE_P(Table551, AdpWalkCell, ::testing::ValuesIn(walked_cells()), cell_name);

TEST(AdpWalk, EveryCellOutsideTheDrawColumnIsWalked) {
    unsigned by_class[4] = {0, 0, 0, 0};
    constexpr const char* kClasses = "NISC";
    const std::vector<std::pair<int, int>> cells = walked_cells();
    unsigned excluded = 0;
    bool only_draw = true;
    for (int row = 0; row < pp::N_AROW; ++row) {
        for (int col = 0; col < pp::N_ACOL; ++col) {
            const bool walked = std::find(cells.begin(), cells.end(), std::make_pair(row, col)) != cells.end();
            excluded += walked ? 0u : 1u;
            only_draw = only_draw && (walked || col == pp::A_DRAW);
            for (int k = 0; k < 4 && walked; ++k) {
                by_class[k] += pp::ADV[row][col].cls == kClasses[k] ? 1u : 0u;
            }
        }
    }
    std::printf(
        "  walked %u cells of the processor's ADV table (N %u, I %u, S %u, C %u); %u draw-in-flight cells "
        "not applicable\n",
        static_cast<unsigned>(cells.size()), by_class[0], by_class[1], by_class[2], by_class[3], excluded);
    EXPECT_EQ(cells.size(), static_cast<std::size_t>(pp::N_AROW * (pp::N_ACOL - 1)))
        << "every cell outside the draw-in-flight column was walked";
    EXPECT_TRUE(excluded == static_cast<unsigned>(pp::N_AROW) && only_draw)
        << "the draw-in-flight column is the only one excluded";
}

TEST(AdpWalk, P12BootGate) {
    Walk().check_boot_gate();
}
TEST(AdpWalk, P1toP5FirstAdvertAndCadence) {
    Walk().check_first_advert_and_cadence();
}
TEST(AdpWalk, P7DepartingAndRestart) {
    Walk().check_departing_and_restart();
}
TEST(AdpWalk, P11ConfigurationIndexBytes) {
    Walk().check_config_index_bytes();
}

}  // namespace
