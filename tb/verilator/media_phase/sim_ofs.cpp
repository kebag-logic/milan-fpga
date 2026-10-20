// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Several AAF outputs of one clock domain with different presentation
// offsets, graded against the domain's CRF timing points (#632, R678-1-F2):
// ofs_wrap.sv binds KL_mtt_round, a four-talker KL_aaf_packetizer and
// KL_crf_tx as milan_datapath binds them, on an exact 48 kHz frame grid of a
// 50 MHz datapath clock. IEEE 1722-2016 4.3.5 and 10.8 Eq. 15: every output
// stamps whole periods from the grid, so each AAF timestamp must lie within
// +/-5 % of Ps of the CRF timing points modulo Ps; a raw 2,010,000 ns offset
// would sit 10,000 ns (0.48 Ps) off them. Each row must also read back as
// applied, and every timestamp be a frame instant plus its row as read back.
//
//   A  talkers 2,000,000 / 2,010,000 / 0 / 20,833 ns, the CRF row 2,010,000
//   B  talkers 1 / 20,834 / 62,500 / 4,294,958,333 ns (the largest under
//      2^32 once rounded), the CRF row 2,000,000
//   C  at run time talker 1 moves to 1,999,999 ns and talker 3 to
//      0xFFFFFFFF (rounded past 2^32: read back and stamped modulo 2^32)
//   D  the CRF row at 0xFFFFFFFF beside talkers 2,000,000 / 2,010,000 / 0 / 1
//
// The phase is graded for rows under 2^31, where the 32-bit AVTP timestamp
// differences are unambiguous, so not at all in D, whose CRF reference lies
// 4.29 s ahead; the larger rows are graded by readback and by their stamps.
// Mutants: phase_mutants.py plants the raw offset.

#include "Vofs_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"

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

    void reset() {
        d_->rst_n = 0;
        d_->ev_p_i = 0; d_->pair_valid_i = 0; d_->tctx_wr_en_i = 0;
        for (int i = 0; i < 8; i++) edge();
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
        // the readback: every row as applied
        bool rb = true;
        for (int k = 0; k <= kN; k++) {
            const uint32_t want = static_cast<uint32_t>(rounded(rows_[k]));
            const uint32_t got = d_->applied_ns_o[k];
            std::printf("  info: [ofs %s] row %d set %u ns, applied %u ns (%.4f periods)\n", tag, k, rows_[k], got,
                        static_cast<double>(rounded(rows_[k])) / kPsNs);
            if (got != want) rb = false;
        }
        std::snprintf(what, sizeof what, "[ofs %s] every row reads back as applied, rounded up to whole periods", tag);
        c_.that(what, rb);
        // every AAF stamp is a frame instant plus its row as read back
        std::set<uint32_t> low;
        for (uint64_t f : frames_) low.insert(static_cast<uint32_t>(f));
        bool on = true;
        int graded[kN] = {0, 0, 0, 0};
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
        // the CRF timing points: frame instants plus the CRF row as read back
        bool con = true;
        int ncrf = 0;
        for (const auto& c : crf_) {
            if (c.at < from) continue;
            ncrf++;
            if (!low.count(static_cast<uint32_t>(c.ts) - d_->applied_ns_o[kN])) con = false;
        }
        std::snprintf(what, sizeof what, "[ofs %s] every CRF timing point is a frame instant plus the CRF row as read back (%d)",
                      tag, ncrf);
        c_.that(what, con && ncrf >= 2);
        // the phase: each AAF output against the CRF timing points, mod Ps
        if (rows_[kN] >= 0x80000000u) {
            std::printf("  info: [ofs %s] the CRF row lies past 2^31: phase not graded (readback and stamps only)\n", tag);
            return;
        }
        double worst = 0;
        int worst_t = -1;
        for (const auto& a : aaf_) {
            if (a.at < from || rows_[a.t] >= 0x80000000u) continue;
            for (const auto& c : crf_) {
                if (c.at < from) continue;
                const double dd = static_cast<double>(static_cast<int32_t>(a.ts - static_cast<uint32_t>(c.ts)));
                const double p = std::fabs(fold(dd));
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
    reset();
    frames(400);
    grade("A", 12);

    set_rows({1, 20834, 62500, 4294958333u, 2000000});
    reset();
    frames(400);
    grade("B", 12);

    // run time: the rows move while the streams run
    long at = frame_n_;
    set_rows({1, 1999999, 62500, 0xFFFFFFFFu, 2000000});
    frames(400);
    grade("C", at + 12);

    set_rows({2000000, 2010000, 0, 1, 0xFFFFFFFFu});
    reset();
    frames(400);
    grade("D", 12);
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
