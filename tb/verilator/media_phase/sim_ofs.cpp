// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Several AAF outputs of one clock domain with different presentation
// offsets, graded against the domain's CRF timing points (#632):
// ofs_wrap.sv binds KL_mtt_round, a four-talker KL_aaf_packetizer and
// KL_crf_tx as milan_datapath binds them, on an exact 48 kHz frame grid of a
// 50 MHz datapath clock. IEEE 1722-2016 4.3.5 and 10.8 Eq. 15: every output
// stamps whole periods from the grid, so each AAF timestamp must lie within
// +/-5 % of Ps of the CRF timing points modulo Ps; a raw 2,010,000 ns offset
// would sit 10,000 ns (0.48 Ps) off them. Each row must also read back as
// applied, and every timestamp be a frame instant plus its row as read back.
//
// Rounding up can pass 2^32 - 1 ns (KL_mtt_round's banner). An AAF timestamp
// is the low 32 bits of gPTP time (IEEE 1722-2016 4.4.4.9, Eq. 6), so it is
// graded on 32 bits; a CRF timestamp is all 64 (10.4.13.1, Eq. 13), so on 64,
// against an independent Equation 14 result and against the frame grid, and
// the AAF outputs against it on 64 bits too, each AAF stamp unwrapped about
// the grid (rows under 2^31, the AVTP timestamp's own range).
// GET_STREAM_INFO's readback is 32 bits: a row past 2^32 - 1 ns reads
// 0xFFFFFFFF.
//
//   A  talkers 2,000,000 / 2,010,000 / 0 / 20,833 ns, the CRF row 2,010,000
//   B  talkers 1 / 20,834 / 62,500 / 4,294,958,333 ns, the CRF row
//      4,294,958,333 (both the largest that rounds under 2^32)
//   C  at run time talker 1 moves to 1,999,999 ns, talker 3 to 0xFFFFFFFF and
//      the CRF row to 4,294,958,334 (the first that rounds past 2^32)
//   D  the CRF row at 0xFFFFFFFF beside talkers 2,000,000 / 2,010,000 / 0 / 1
//   E  every row its factory value (ofs_wrap's RESET_NS_P, kReset), as a
//      device no controller has set: graded in reset too, all 33 bits
//   F  at run time from E: the CRF row down to 2,000,000 (its carry clears)
//
// Mutants: phase_mutants.py plants the raw offset, the CRF row as set, and
// the carry dropped at the rounder's conversion, its reset load, its
// readback and the CRF output's sum.

#include "Vofs_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"

#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <map>
#include <set>
#include <string>
#include <vector>

namespace {

constexpr int kN = 4;                         //!< AAF talkers
constexpr double kPsNs = 1e9 / 48000.0;
constexpr double kBandNs = 0.05 * kPsNs;
constexpr uint64_t kT0Ns = 7000000000ULL;     //!< the PHC at the first cycle
constexpr int kClkNs = 20;
//! the factory rows, as ofs_wrap's RESET_NS_P declares them
const std::vector<uint32_t> kReset = {2000000u, 2010000u, 4294958333u, 4294958334u, 0xFFFFFFFFu};

double fold(double x) {
    double r = std::fmod(x, kPsNs);
    if (r < 0) r += kPsNs;
    if (r >= kPsNs / 2) r -= kPsNs;
    return r;
}

//! the rule (IEEE 1722-2016 10.7 Eq. 14 as KL_crf_tx applies it), exactly
uint64_t rounded(uint64_t t) {
    const uint64_t per = (t * 3 + 62499) / 62500;
    return (per * 62500 + 2) / 3;
}

class OfsHarness {
 public:
    OfsHarness(Vofs_wrap* d, milan::tb::Checker& c) : d_(d), c_(c) {}
    int run();

 private:
    uint64_t phc() const { return kT0Ns + cyc_ * kClkNs; }

    void edge() {
        d_->clk_i = 0;
        d_->eval();
        d_->clk_i = 1;
        d_->eval();
        cyc_++;
        observe();
    }

    void set_rows(const std::vector<uint32_t>& rows) {
        rows_ = rows;
        for (int k = 0; k <= kN; k++) d_->raw_ns_i[k] = rows[k];
    }

    //! the row as applied, all 33 bits
    uint64_t applied(int k) const {
        return (static_cast<uint64_t>((d_->applied_c_o >> k) & 1u) << 32) | d_->applied_ns_o[k];
    }

    //! GET_STREAM_INFO's word for a rounded value: 0xFFFFFFFF past 32 bits
    static uint32_t readback(uint64_t r) { return r > 0xFFFFFFFFull ? 0xFFFFFFFFu : static_cast<uint32_t>(r); }

    void reset(const char* tag) {
        d_->rst_n = 0;
        d_->ev_p_i = 0; d_->pair_valid_i = 0; d_->tctx_wr_en_i = 0;
        for (int i = 0; i < 8; i++) edge();
        // in reset every row holds its factory value, rounded, all 33 bits
        bool fac = true;
        for (int k = 0; k <= kN; k++) fac = fac && applied(k) == rounded(kReset[k]);
        char what[160];
        std::snprintf(what, sizeof what,
                      "[ofs %s] in reset every row reads its factory value rounded up to whole periods, all 33 bits", tag);
        c_.that(what, fac);
        d_->rst_n = 1;
        for (int i = 0; i < 8; i++) edge();
        // talkers 1..3: enabled, stereo, UID = talker index
        for (int t = 1; t < kN; t++) {
            tctx(t, 1, 0xF000FE02u);
            tctx(t, 2, (static_cast<uint32_t>(t) << 16) | 0x91E0u);
            tctx(t, 0, (2u << 5) | (2u << 1) | 1u);
        }
        frames_.clear();
        next_frame_ = static_cast<double>(phc()) + 40000.0;
        frame_n_ = 0;
        aaf_.clear();
        crf_.clear();
        bytes_.clear();
        cbytes_.clear();
        pending_pairs_ = 0;
    }

    void tctx(int t, int w, uint32_t v) {
        d_->tctx_wr_en_i = 1;
        d_->tctx_wr_addr_i = static_cast<uint8_t>((t << 4) | w);
        d_->tctx_wr_data_i = v;
        for (int i = 0; i < 64; i++) {
            const bool rdy = d_->tctx_wr_rdy_o;
            edge();
            if (rdy) break;
        }
        d_->tctx_wr_en_i = 0;
        edge();
    }

    //! one cycle of the frame grid: an event per frame with its instant,
    //! then one pair per talker a few cycles apart, the time base held at
    //! the frame's instant while they are injected
    void cycle() {
        d_->ev_p_i = 0;
        d_->pair_valid_i = 0;
        if (static_cast<double>(phc()) >= next_frame_) {
            const uint64_t f = static_cast<uint64_t>(std::llround(next_frame_));
            d_->ev_p_i = 1;
            d_->ev_ns_i = f;
            d_->tbase_ns_i = f;
            frames_.insert(f);
            frame_n_++;
            next_frame_ += kPsNs;
            pending_pairs_ = kN;
            pair_gap_ = 2;
        } else if (pending_pairs_ > 0 && --pair_gap_ == 0) {
            d_->pair_valid_i = 1;
            d_->pair_slot_i = static_cast<uint8_t>(kN - pending_pairs_);
            pending_pairs_--;
            pair_gap_ = 3;
        }
        edge();
    }

    void observe() {
        if (d_->aaf_tvalid_o) {
            for (int l = 0; l < 8; l++)
                if ((d_->aaf_tkeep_o >> l) & 1) bytes_.push_back(static_cast<uint8_t>(d_->aaf_tdata_o >> (8 * l)));
            if (d_->aaf_tlast_o) {
                const size_t tag = bytes_.size() > 18 && bytes_[12] == 0x81 ? 4 : 0;
                if (bytes_.size() >= 34 + tag) {
                    const unsigned uid = (bytes_[24 + tag] << 8) | bytes_[25 + tag];
                    uint32_t ts = 0;
                    for (size_t k = 26 + tag; k < 30 + tag; k++) ts = (ts << 8) | bytes_[k];
                    if (uid < kN) aaf_.push_back({uid, ts, frame_n_});
                }
                bytes_.clear();
            }
        }
        if (d_->crf_tvalid_o) {
            const uint64_t v = d_->crf_tdata_o;
            for (int l = 0; l < 8; l++) cbytes_.push_back(static_cast<uint8_t>(v >> (8 * l)));
            if (d_->crf_tlast_o) {
                if (cbytes_.size() >= 42) {
                    uint64_t ts = 0;
                    for (int k = 34; k < 42; k++) ts = (ts << 8) | cbytes_[k];
                    crf_.push_back({ts, frame_n_});
                }
                cbytes_.clear();
            }
        }
    }

    void frames(long n) {
        const long until = frame_n_ + n;
        while (frame_n_ < until) cycle();
    }

    struct Aaf { unsigned t; uint32_t ts; long at; };
    struct Crf { uint64_t ts; long at; };

    //! grade the PDUs emitted after frame `from`: readback, stamps, phase
    void grade(const char* tag, long from) {
        char what[240];
        // the rows as applied, all 33 bits, and GET_STREAM_INFO's word
        bool rb = true;
        bool gsi = true;
        for (int k = 0; k <= kN; k++) {
            const uint64_t want = rounded(rows_[k]);
            d_->rb_row_i = static_cast<uint8_t>(k);
            d_->eval();
            std::printf("  info: [ofs %s] row %d set %u ns, applied %llu ns (%.4f periods), GET_STREAM_INFO reads %u\n",
                        tag, k, rows_[k], static_cast<unsigned long long>(applied(k)),
                        static_cast<double>(want) / kPsNs, d_->rb_ns_o);
            if (applied(k) != want) rb = false;
            if (d_->rb_ns_o != readback(want)) gsi = false;
        }
        std::snprintf(what, sizeof what,
                      "[ofs %s] every row reads back as applied, rounded up to whole periods, all 33 bits", tag);
        c_.that(what, rb);
        std::snprintf(what, sizeof what,
                      "[ofs %s] GET_STREAM_INFO reads every row as applied, 0xFFFFFFFF past 32 bits", tag);
        c_.that(what, gsi);
        // every AAF stamp is a frame instant plus its row as read back
        std::set<uint32_t> low;
        for (uint64_t f : frames_) low.insert(static_cast<uint32_t>(f));
        bool on = true;
        std::array<int, kN> graded{};
        for (const auto& a : aaf_) {
            if (a.at < from) continue;
            const uint32_t f = a.ts - d_->applied_ns_o[a.t];
            if (!low.count(f)) on = false;
            graded[a.t]++;
        }
        bool enough = true;
        for (int t = 0; t < kN; t++) enough = enough && graded[t] >= 20;
        std::snprintf(what, sizeof what, "[ofs %s] every AAF timestamp is a frame instant plus its row as read back (%d %d %d %d PDUs)",
                      tag, graded[0], graded[1], graded[2], graded[3]);
        c_.that(what, on && enough);
        // the CRF timing points, all 64 bits: frame instants plus the CRF row
        // as read back, and plus the independent Equation 14 result
        bool con = true;
        bool eq14 = true;
        int ncrf = 0;
        const uint64_t f0 = *frames_.begin();
        double grid = 0;
        for (const auto& c : crf_) {
            if (c.at < from) continue;
            ncrf++;
            if (!frames_.count(c.ts - applied(kN))) con = false;
            if (!frames_.count(c.ts - rounded(rows_[kN]))) eq14 = false;
            grid = std::fmax(grid, std::fabs(fold(static_cast<double>(c.ts - f0))));
        }
        std::snprintf(what, sizeof what, "[ofs %s] every CRF timing point is a frame instant plus the CRF row as read back (%d)",
                      tag, ncrf);
        c_.that(what, con && ncrf >= 2);
        std::snprintf(what, sizeof what,
                      "[ofs %s] every CRF timestamp, all 64 bits, is a frame instant plus the CRF row rounded by Equation 14", tag);
        c_.that(what, eq14 && ncrf >= 2);
        std::snprintf(what, sizeof what,
                      "[ofs %s] every CRF timestamp lies on the frame grid modulo Ps, inside +/-5 %% of Ps (max %.2f ns)",
                      tag, grid);
        c_.that(what, grid < kBandNs && ncrf >= 2);
        // the phase: each AAF output against the CRF timing points, mod Ps,
        // on 64 bits. An AAF stamp is unwrapped about the first frame (its
        // row and the run lie well inside 2^31 ns of it)
        double worst = 0;
        int worst_t = -1;
        for (const auto& a : aaf_) {
            if (a.at < from || rows_[a.t] >= 0x80000000u) continue;
            const int64_t a64 = static_cast<int64_t>(f0)
                                + static_cast<int32_t>(a.ts - static_cast<uint32_t>(f0));
            for (const auto& c : crf_) {
                if (c.at < from) continue;
                const double p = std::fabs(fold(static_cast<double>(a64 - static_cast<int64_t>(c.ts))));
                if (p > worst) { worst = p; worst_t = static_cast<int>(a.t); }
            }
        }
        std::snprintf(what, sizeof what,
                      "[ofs %s] every AAF output stamps whole periods from the CRF timing points, inside +/-5 %% of Ps "
                      "(max %.2f ns, talker %d)", tag, worst, worst_t);
        c_.that(what, worst < kBandNs && ncrf >= 2);
    }

    Vofs_wrap* d_;
    milan::tb::Checker& c_;
    uint64_t cyc_ = 0;
    std::vector<uint32_t> rows_;
    std::set<uint64_t> frames_;
    double next_frame_ = 0;
    long frame_n_ = 0;
    int pending_pairs_ = 0;
    int pair_gap_ = 0;
    std::vector<uint8_t> bytes_;
    std::vector<uint8_t> cbytes_;
    std::vector<Aaf> aaf_;
    std::vector<Crf> crf_;
};

int OfsHarness::run() {
    std::printf("[ofs] four AAF outputs and the CRF output of one domain, each its own offset\n");
    set_rows({2000000, 2010000, 0, 20833, 2010000});
    reset("A");
    frames(400);
    grade("A", 12);

    set_rows({1, 20834, 62500, 4294958333u, 4294958333u});
    reset("B");
    frames(400);
    grade("B", 12);

    // run time: the rows move while the streams run, the CRF row past 2^32
    long at = frame_n_;
    set_rows({1, 1999999, 62500, 0xFFFFFFFFu, 4294958334u});
    frames(400);
    grade("C", at + 12);

    set_rows({2000000, 2010000, 0, 1, 0xFFFFFFFFu});
    reset("D");
    frames(400);
    grade("D", 12);

    // power-on: no controller has set a row, every output its factory value
    set_rows(kReset);
    reset("E");
    frames(400);
    grade("E", 12);

    // ...and at run time the CRF row comes down under 2^32 again
    at = frame_n_;
    set_rows({2000000, 2010000, 0, 20833, 2000000});
    frames(400);
    grade("F", at + 12);
    return c_.report();
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vofs_wrap> model;
    milan::tb::Checker check{"media_phase ofs"};
    check.echo_passes();
    OfsHarness harness(model.get(), check);
    return harness.run();
}
