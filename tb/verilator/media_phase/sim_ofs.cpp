// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Several AAF outputs of one clock domain with different presentation
// offsets, and the domain's CRF output, each graded against the frame grid
// (#632): ofs_wrap.sv binds a four-talker KL_aaf_packetizer, KL_crf_tx and
// KL_mtt_round as milan_datapath binds them, on an exact 48 kHz frame grid of
// a 50 MHz datapath clock. Each frame instant is the instant the frame started
// at the media interface (the pins case grades that instant at the pins), and
// each talker is handed it with the frame, as the capture walk hands it.
//
// AN AAF TALKER APPLIES ITS OFFSET EXACTLY AS SET (Milan v1.2 5.4.2.9): every
// AAF timestamp must be a frame instant plus its row as set, to the ns, and
// GET_STREAM_INFO must read the row as set (5.4.2.10.2). An AAF timestamp is
// the low 32 bits of gPTP time (IEEE 1722-2016 4.4.4.9, Eq. 6), so it is
// graded on 32 bits. Against the CRF timing points an AAF output's phase is
// then its row as set less the CRF row as applied, modulo Ps: whole periods
// for an offset of whole periods, the offset's fraction otherwise.
//
// THE CRF OUTPUT ALONE ROUNDS, by IEEE 1722-2016 10.7 Equation (14): its row
// applied is graded against an independent Equation 14 result, all 33 bits,
// and every CRF timestamp, all 64 bits (10.4.13.1, Eq. 13), must be a frame
// instant plus that value and lie on the frame grid inside 10.8's +/-5 % of
// Ps. Rounding up can pass 2^32 - 1 ns (KL_mtt_round's banner), so
// GET_STREAM_INFO's 32-bit word reads such a row as 0xFFFFFFFF.
//
// THE OFFSETS (the #632 ruling's list): 0, 1, 20,833, 20,834, 62,500,
// 2,000,000, 2,010,000 and 0xFFFFFFFF ns, each on AAF rows and on the CRF
// row, and on the CRF row 4,294,958,333 and 4,294,958,334 besides (the
// largest whose rounding fits 32 bits, and the first whose does not). Each
// case either resets with its rows set (the CRF row's factory value,
// kCrfReset, graded in reset, all 33 bits) or moves them while the streams
// run (kCases).
//
// Mutants: phase_mutants.py plants the AAF rows rounded (round 2's binding),
// their readback rounded, the CRF row as set, and the carry dropped at the
// rounder's conversion, its reset load, its readback and the CRF output's sum.

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
//! the CRF row's factory value, as ofs_wrap's CRF_RESET_NS_P declares it
constexpr uint32_t kCrfReset = 0xFFFFFFFFu;
//! the frame instants are whole ns, so two of them lie whole periods apart
//! to within this
constexpr double kGridNs = 2.0;

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

//! one case: the four AAF rows and the CRF row, and whether the device
//! resets with them (else they move while the streams run)
struct Case {
    const char* tag;
    bool reset;
    std::array<uint32_t, kN + 1> rows;
};
const std::vector<Case> kCases = {
    {"A", true,  {0u, 1u, 20833u, 20834u, 0u}},
    {"B", true,  {62500u, 2000000u, 2010000u, 0xFFFFFFFFu, 1u}},
    {"C", false, {2010000u, 0u, 1u, 20833u, 20833u}},
    {"D", true,  {20834u, 62500u, 0xFFFFFFFFu, 2000000u, 20834u}},
    {"E", false, {0xFFFFFFFFu, 20834u, 62500u, 0u, 62500u}},
    {"F", true,  {2000000u, 2010000u, 0u, 1u, 2000000u}},
    {"G", false, {1u, 0u, 2010000u, 62500u, 2010000u}},
    {"H", true,  {2000000u, 2010000u, 20833u, 0xFFFFFFFFu, 0xFFFFFFFFu}},
    {"I", false, {2010000u, 2000000u, 1u, 0u, 4294958333u}},
    {"J", false, {2010000u, 2000000u, 1u, 0u, 4294958334u}},
    {"K", false, {2000000u, 2010000u, 0u, 20833u, 2000000u}},
};

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

    void set_rows(const std::array<uint32_t, kN + 1>& rows) {
        rows_ = rows;
        for (int k = 0; k <= kN; k++) d_->raw_ns_i[k] = rows[static_cast<size_t>(k)];
    }

    uint32_t row(int k) const { return rows_[static_cast<size_t>(k)]; }

    //! the CRF row as applied, all 33 bits
    uint64_t applied() const {
        return (static_cast<uint64_t>(d_->crf_applied_c_o & 1u) << 32) | d_->crf_applied_ns_o;
    }

    //! GET_STREAM_INFO's word for a rounded value: 0xFFFFFFFF past 32 bits
    static uint32_t readback(uint64_t r) { return r > 0xFFFFFFFFull ? 0xFFFFFFFFu : static_cast<uint32_t>(r); }

    void reset(const char* tag) {
        d_->rst_n = 0;
        d_->ev_p_i = 0; d_->pair_valid_i = 0; d_->tctx_wr_en_i = 0;
        for (int i = 0; i < 8; i++) edge();
        // in reset the CRF row holds its factory value, rounded, all 33 bits
        char what[160];
        std::snprintf(what, sizeof what,
                      "[ofs %s] in reset the CRF row reads its factory value rounded up to whole periods, all 33 bits",
                      tag);
        c_.that(what, applied() == rounded(kCrfReset));
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

    void grade_readback(const char* tag);
    void grade_aaf(const char* tag, long from);
    int grade_crf(const char* tag, long from);
    void grade_phase(const char* tag, long from, int ncrf);

    //! grade the PDUs emitted after frame `from`: readback, stamps, phase
    void grade(const char* tag, long from) {
        grade_readback(tag);
        grade_aaf(tag, from);
        const int ncrf = grade_crf(tag, from);
        grade_phase(tag, from, ncrf);
    }

    Vofs_wrap* d_;
    milan::tb::Checker& c_;
    uint64_t cyc_ = 0;
    std::array<uint32_t, kN + 1> rows_{};
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

//! the CRF row as applied, all 33 bits, and GET_STREAM_INFO's word for
//! every row: an AAF row as set, the CRF row as applied
void OfsHarness::grade_readback(const char* tag) {
    char what[240];
    const uint64_t want = rounded(row(kN));
    bool aaf_rb = true;
    for (int k = 0; k <= kN; k++) {
        d_->rb_row_i = static_cast<uint8_t>(k);
        d_->eval();
        std::printf("  info: [ofs %s] row %d set %u ns, GET_STREAM_INFO reads %u", tag, k, row(k), d_->rb_ns_o);
        if (k < kN) {
            std::printf("\n");
            if (d_->rb_ns_o != row(k)) aaf_rb = false;
        } else {
            std::printf(", applied %llu ns (%.4f periods)\n", static_cast<unsigned long long>(applied()),
                        static_cast<double>(want) / kPsNs);
        }
    }
    std::snprintf(what, sizeof what, "[ofs %s] the CRF row reads back as applied, rounded up to whole periods by "
                  "Equation 14, all 33 bits", tag);
    c_.that(what, applied() == want);
    std::snprintf(what, sizeof what, "[ofs %s] GET_STREAM_INFO reads every AAF row as set", tag);
    c_.that(what, aaf_rb);
    d_->rb_row_i = static_cast<uint8_t>(kN);
    d_->eval();
    std::snprintf(what, sizeof what, "[ofs %s] GET_STREAM_INFO reads the CRF row as applied, 0xFFFFFFFF past 32 bits",
                  tag);
    c_.that(what, d_->rb_ns_o == readback(want));
}

//! every AAF stamp is a frame instant plus its row as set, to the ns
void OfsHarness::grade_aaf(const char* tag, long from) {
    char what[240];
    std::set<uint32_t> low;
    for (uint64_t f : frames_) low.insert(static_cast<uint32_t>(f));
    bool on = true;
    std::array<int, kN> graded{};
    for (const auto& a : aaf_) {
        if (a.at < from) continue;
        if (!low.count(a.ts - row(static_cast<int>(a.t)))) on = false;
        graded[a.t]++;
    }
    bool enough = true;
    for (int t = 0; t < kN; t++) enough = enough && graded[static_cast<size_t>(t)] >= 20;
    std::snprintf(what, sizeof what,
                  "[ofs %s] every AAF timestamp is a frame instant plus its row as set, to the ns (%d %d %d %d PDUs)",
                  tag, graded[0], graded[1], graded[2], graded[3]);
    c_.that(what, on && enough);
}

//! the CRF timing points, all 64 bits: frame instants plus the CRF row as
//! read back, and plus the independent Equation 14 result
int OfsHarness::grade_crf(const char* tag, long from) {
    char what[240];
    bool con = true;
    bool eq14 = true;
    int ncrf = 0;
    const uint64_t f0 = *frames_.begin();
    double grid = 0;
    for (const auto& c : crf_) {
        if (c.at < from) continue;
        ncrf++;
        if (!frames_.count(c.ts - applied())) con = false;
        if (!frames_.count(c.ts - rounded(row(kN)))) eq14 = false;
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
    return ncrf;
}

//! each AAF output against the CRF timing points, mod Ps, on 64 bits: its
//! row as set less the CRF row as applied. An AAF stamp is unwrapped about
//! the first frame (its row and the run lie well inside 2^31 ns of it), so
//! rows from 2^31 on are left out: an AAF stamp is 32 bits, and no
//! controller sets such a row (SET_STREAM_INFO refuses bit 31)
void OfsHarness::grade_phase(const char* tag, long from, int ncrf) {
    char what[240];
    const uint64_t f0 = *frames_.begin();
    double worst = 0;
    int worst_t = -1;
    int pairs = 0;
    for (const auto& a : aaf_) {
        if (a.at < from || row(static_cast<int>(a.t)) >= 0x80000000u) continue;
        const int64_t a64 = static_cast<int64_t>(f0)
                            + static_cast<int32_t>(a.ts - static_cast<uint32_t>(f0));
        const double want = static_cast<double>(row(static_cast<int>(a.t))) - static_cast<double>(applied());
        for (const auto& c : crf_) {
            if (c.at < from) continue;
            const double p = std::fabs(fold(static_cast<double>(a64 - static_cast<int64_t>(c.ts)) - want));
            pairs++;
            if (p > worst) { worst = p; worst_t = static_cast<int>(a.t); }
        }
    }
    std::snprintf(what, sizeof what,
                  "[ofs %s] every AAF output's phase against the CRF timing points is its row as set less the CRF row "
                  "as applied, modulo Ps (max %.2f ns, talker %d)", tag, worst, worst_t);
    c_.that(what, worst <= kGridNs && pairs > 0 && ncrf >= 2);
}

int OfsHarness::run() {
    std::printf("[ofs] four AAF outputs and the CRF output of one domain, each its own offset\n");
    for (const Case& k : kCases) {
        set_rows(k.rows);
        long at = 0;
        if (k.reset) {
            reset(k.tag);
        } else {
            at = frame_n_;
        }
        frames(400);
        grade(k.tag, at + 12);
    }
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
