// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Two RENDER interfaces on one clock domain, graded at their pins (#632):
// the synthetic shape of render_wrap.sv (TDM8 owner A and TDM4 B on one
// 24.576 MHz audio clock, B through a one-frame output hold, so its
// post-grid delay is a frame longer; one KL_render_queue reads both from the
// domain's one media event, each with its own derived out-lead; a 50 MHz
// datapath clock, the PHC the true time).
//
// The harness plays the depacketizer's read side: each PDU's header (tv and
// avtp_timestamp) and, PAY_LEAD cycles later, its 48 samples (6 events of 8
// channels) as 24 beats. Every sample carries its identity (stream, channel,
// event number), and its presentation time is the PDU's timestamp plus one
// period per event (IEEE 1722-2016 7.5). The timestamps sit on the domain's
// frame grid as the pins show it (A's sync instants), plus a phase phi:
// the grid a talker locked to the same media clock stamps (10.8).
//
// A slot-MSB pin decoder per interface (slot_msb_decoder.hpp) reads that
// interface's bclk, fsync and data pins and decodes every slot's 24 bits.
// The harness requires:
//   [render A|B] every slot of every frame carries its mapped stream and
//              channel or silence;
//   [render A|B] every sample's slot-MSB pin instant, less its slot offset, is
//              its presentation time inside +/-5 % of Ps (|phi| <= 4 % here);
//   [render A|B] ...and is the frame instant nearest its presentation time:
//              the pin instant less the slot offset is the presentation time
//              less phi, inside 100 ns, at every phi up to +/-0.45 Ps;
//   [render A|B] every sample a presented PDU carries reaches the pins, at
//              holds from 0.1 ms to 2.6 ms ahead of its presentation time
//              (the supported range), and the frames of the refused PDUs are
//              silence;
//   [render]   the late PDU (its timestamp 1.5 ms in the past at its
//              arrival), the too-early PDU (3.0 ms ahead) and the PDU without
//              tv, each sent in its place in its stream, are each counted
//              once and presented nowhere; slips_o counts every run of
//              presented frames that ends;
//   [render]   B's out-lead is at least a frame past A's.
// phase_mutants.py drops B's constant, reads the queue untimed, puts every
// PDU a frame late, and removes the late rule (and the early rule), each a
// named failure.

#include "Vrender_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include "slot_msb_decoder.hpp"

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <map>
#include <vector>

namespace {

constexpr double kPsNs = 1e9 / 48000.0;
constexpr double kBandNs = 0.05 * kPsNs;
constexpr double kAxisHz = 50e6;
//! the audio VCO 10.64 ppm under nominal, the shipping MMCM plan
constexpr double kPlan = 1.0 - 10.64e-6;
constexpr double kAudHz = 24.576e6 * kPlan;
constexpr double kHalfIFs = 0.5 * 1e15 / kAxisHz;
constexpr double kHalfAFs = 0.5 * 1e15 / kAudHz;
//! the domain's frame period as the pins run it: 512 audio cycles
constexpr double kPsActNs = 512.0 * 1e9 / kAudHz;
//! the nearest-frame grade: the pin instant against the timestamp less phi
constexpr double kSnapNs = 100.0;
constexpr int kPayLead = 16;      //!< render_wrap's PAY_LEAD_P
constexpr int kEvents = 6;
constexpr int kChans = 8;

//! one sample's identity: stream, channel, event number (never zero)
uint32_t ident(int s, int ch, long seq) {
    return (static_cast<uint32_t>(s) << 22) | (static_cast<uint32_t>(ch) << 19) |
           static_cast<uint32_t>(seq & 0x7FFFF);
}

//! one PDU the talker sends
struct Pdu {
    int stream = 0;
    long frame = 0;        //!< grid frame of its first event
    double phi = 0;        //!< its timestamp's offset from that frame, ns
    double ts_ns = 0;      //!< its avtp_timestamp, ns
    double send_ns = 0;    //!< when its header reaches the queue
    bool tv = true;
    enum Fate { PRESENTED, LATE, EARLY, UNTIMED } fate = PRESENTED;
    long seq0 = 0;         //!< its first event's number
};

class RenderHarness {
 public:
    RenderHarness(Vrender_wrap* dut, milan::tb::Checker& check) : dut_(dut), check_(check) {}

    int run() {
        reset_and_map();
        // let the buses and the domain event run, then take the grid from A's pins
        run_ns(2e6);
        if (a_.frames.size() < 8) {
            check_.that("[render] interface A's frames are at its pins", false);
            return check_.report();
        }
        ref_sync_ = a_.frames.back().sync;
        plan();
        // run past the last PDU's last frame, so every presented run has ended
        run_ns(last_frame_ns() - now_ns() + 3e6);
        grade();
        return check_.report();
    }

 private:
    // ------------------------------------------------------------------ //
    void reset_and_map() {
        dut_->rst_n = 0;
        run_ns(2000);
        dut_->rst_n = 1;
        run_ns(200);
        // A: slots 0..5 <- stream 0 channels 0..5, slots 6..7 <- stream 2
        // channels 0..1; B: slots 0..1 <- stream 0 channels 0..1, slots 2..3
        // <- stream 1 channels 0..1. Entry {en, src 0, {s, ch}}
        for (int k = 0; k < 8; k++) {
            const auto [s, ch] = mapped(true, k);
            map_write(true, k, 0x80 | (s << 3) | ch);
        }
        map_write(false, 0, 0x80 | (0 << 3) | 0);
        map_write(false, 1, 0x80 | (0 << 3) | 1);
        map_write(false, 2, 0x80 | (1 << 3) | 0);
        map_write(false, 3, 0x80 | (1 << 3) | 1);
    }
    void map_write(bool a, int addr, int data) {
        if (a) {
            dut_->map_a_we_i = 1; dut_->map_a_addr_i = addr; dut_->map_a_data_i = data;
        } else {
            dut_->map_b_we_i = 1; dut_->map_b_addr_i = addr; dut_->map_b_data_i = data;
        }
        clk_cycle();
        dut_->map_a_we_i = 0;
        dut_->map_b_we_i = 0;
    }

    double grid_ns(long frame) const { return ref_sync_ + static_cast<double>(frame) * kPsActNs; }
    double now_ns() const { return t_fs_ / 1e6; }
    double last_frame_ns() const {
        double t = 0;
        for (const Pdu& p : pdus_) t = std::max(t, grid_ns(p.frame + kEvents));
        return t;
    }

    //! the domain event's pulse after its frame instant: A's marker latency,
    //! derived here as sim_pins.cpp derives it (to the closing pair's last
    //! bit, one write-clock cycle, 4.5 datapath cycles)
    static double ev_lat_ns() {
        const double bits = 2.0 * 4 * 32 + 1 - 1;
        return bits * 1e9 / (8 * 32 * 48000.0) + 1e9 / 24.576e6 + 4.5e9 / kAxisHz;
    }

    //! the talker's schedule. Streams 0 and 1 run every 6 frames, in order,
    //! through phases of hold (decreasing, as a talker's sends stay in order)
    //! and of phase. Stream 2 sends lone PDUs, each with nothing of its stream
    //! within a queue's depth: one presented, one whose first two events are
    //! late and one whose last two are beyond the queue (each sent half a
    //! frame after a domain event, so the frame each event names is not
    //! near a rounding), one wholly late, one wholly too early, one untimed.
    void plan() {
        const double start = now_ns();
        // the first PDU presents 130 frames (2.7 ms) after now
        const long f0 = 130;
        //! hold: the PDU's first event's lead at its arrival; its last event
        //! is held five periods longer
        const double last = (kEvents - 1) * kPsNs;
        struct Phase { int pdus; double hold_ns; double phi_ps; };
        const std::array<Phase, 7> phases = {{
            {16, 2.6e6 - last, 0.0},    // last event 2.6 ms ahead: the long end
            {24, 2.0e6, 0.0},           // the 2 ms default
            {16, 2.0e6, 0.04},          // a timestamp 4 % of Ps after its frame
            {16, 2.0e6, -0.04},         // ...and before it
            {12, 2.0e6, 0.45},          // nearly half a period off: still its frame
            {12, 2.0e6, -0.45},
            {16, 0.1e6, 0.0},           // first event 0.1 ms ahead: the short end
        }};
        long frame = f0;
        long seq[3] = {1, 1, 1};
        double sent[2] = {start, start};
        for (const Phase& ph : phases) {
            for (int j = 0; j < ph.pdus; j++) {
                for (int s = 0; s < 2; s++) {
                    Pdu p;
                    p.stream = s;
                    p.frame = frame;
                    p.phi = ph.phi_ps * kPsNs;
                    p.ts_ns = grid_ns(frame) + p.phi;
                    p.seq0 = seq[s];
                    seq[s] += kEvents;
                    //! a stream's PDUs leave in order, a microsecond apart at
                    //! least, stream 1 three microseconds after stream 0
                    p.send_ns = std::max(p.ts_ns - ph.hold_ns + 3.0e3 * s, sent[s] + 1e3);
                    sent[s] = p.send_ns;
                    pdus_.push_back(p);
                    for (int k = 0; k < kEvents; k++) {
                        if (s == 0) exp_a_[{s, frame + k}] = p.seq0 + k;
                        exp_b_[{s, frame + k}] = p.seq0 + k;
                    }
                }
                frame += kEvents;
            }
        }
        last_frame_ = frame - 1;
        // stream 2: one lone PDU per 150 frames, sent half a frame after the
        // domain event of grid frame m (its pulse comes ev_lat after m's
        // instant), its timestamp on grid frame m + delta. At that instant
        // the latest event is m's and every interface has consumed frame
        // m + K_A = m + 2, so event k names frame m + delta + k
        const double mid = ev_lat_ns() + 0.5 * kPsNs;
        struct Lone { Pdu::Fate fate; long delta; int first_a; };
        const std::array<Lone, 7> lone = {{
            {Pdu::PRESENTED, 50, 0},    // 1 ms ahead: all six at A
            //! the first event half a frame past at its arrival: it names
            //! m + 1, the second m + 2, both consumed (late, dropped, counted
            //! once); the rest are written, and A, reading two frames ahead
            //! from event m + 1 on, shows them
            {Pdu::LATE, 1, 2},
            //! the first event 2.59 ms ahead, naming m + 126: events 4 and 5
            //! name m + 130 and m + 131, 128 rows past the consumed m + 2
            //! (early, dropped, counted once)
            {Pdu::EARLY, 126, -2},
            {Pdu::LATE, -48, 6},        // a timestamp 1 ms past: wholly late
            {Pdu::EARLY, 145, 6},       // 3 ms ahead: wholly too early
            {Pdu::UNTIMED, 50, 6},      // no tv
            {Pdu::PRESENTED, 6, 0},     // 94 us ahead: all six at A
        }};
        long m = f0 + 10;
        for (const Lone& l : lone) {
            Pdu p;
            p.stream = 2;
            p.fate = l.fate;
            p.send_ns = grid_ns(m) + mid;
            p.ts_ns = grid_ns(m + l.delta);
            p.tv = l.fate != Pdu::UNTIMED;
            p.frame = m + l.delta;
            p.seq0 = seq[2];
            seq[2] += kEvents;
            pdus_.push_back(p);
            // which of its events A shows: from first_a on (a negative count
            // keeps that many from the end out), none for 6
            for (int k = 0; k < kEvents; k++) {
                const bool shown = l.first_a >= 0 ? k >= l.first_a : k < kEvents + l.first_a;
                if (shown) exp_a_[{2, p.frame + k}] = p.seq0 + k;
            }
            refused_late_ += l.fate == Pdu::LATE;
            refused_early_ += l.fate == Pdu::EARLY;
            refused_untimed_ += l.fate == Pdu::UNTIMED;
            m += 150;
        }
        last_frame_ = std::max(last_frame_, m);
        std::stable_sort(pdus_.begin(), pdus_.end(),
                         [](const Pdu& x, const Pdu& y) { return x.send_ns < y.send_ns; });
        // every sample's presentation time is its PDU's timestamp plus one
        // period per event
        for (const Pdu& p : pdus_) {
            for (int k = 0; k < kEvents; k++) {
                pt_[{p.stream, p.seq0 + k}] = p.ts_ns + k * kPsActNs;
                phi_[{p.stream, p.seq0 + k}] = p.phi;
            }
        }
        first_frame_ = f0;
        std::printf("  info: %zu PDUs, frames %ld..%ld, A out-lead %d, B out-lead %d\n", pdus_.size(),
                    first_frame_, last_frame_, dut_->a_lead_o, dut_->b_lead_o);
    }

    // ------------------------------------------------------------------ //
    // the depacketizer read side: a header, PAY_LEAD cycles, 24 beats. Run
    // after each rising edge, it sets what the next rising edge samples.
    void drive() {
        dut_->hdr_p_i = 0;
        dut_->s_tvalid_i = 0;
        dut_->s_tlast_i = 0;
        switch (state_) {
        case IDLE:
            if (next_pdu_ < pdus_.size() && now_ns() >= pdus_[next_pdu_].send_ns) {
                const Pdu& p = pdus_[next_pdu_];
                const double ts = p.ts_ns;
                dut_->hdr_p_i = 1;
                dut_->hdr_ts_i = static_cast<uint32_t>(static_cast<uint64_t>(std::llround(ts)));
                dut_->hdr_tv_i = p.tv ? 1 : 0;
                cur_ = next_pdu_++;
                lead_ = kPayLead - 1;
                state_ = LEAD;
            }
            break;
        case LEAD:
            if (lead_ > 0) {
                --lead_;
                break;
            }
            state_ = BEATS;
            beat_ = 0;
            [[fallthrough]];
        case BEATS: {
            const Pdu& p = pdus_[cur_];
            uint64_t d = 0;
            for (int h = 0; h < 2; h++) {
                const int i = 2 * beat_ + h;
                const uint32_t v = ident(p.stream, i % kChans, p.seq0 + i / kChans);
                d |= (static_cast<uint64_t>((v >> 16) & 0xFF) << (32 * h)) |
                     (static_cast<uint64_t>((v >> 8) & 0xFF) << (32 * h + 8)) |
                     (static_cast<uint64_t>(v & 0xFF) << (32 * h + 16));
            }
            dut_->s_tdata_i = d;
            dut_->s_tvalid_i = 1;
            dut_->s_tuser_i = static_cast<uint8_t>(p.stream);
            if (++beat_ == kEvents * kChans / 2) {
                dut_->s_tlast_i = 1;
                state_ = IDLE;
            }
            break;
        }
        }
    }

    // ------------------------------------------------------------------ //
    void tick_one() {
        const double next = std::min(next_i_, next_a_);
        t_fs_ = next;
        const double t_ns = t_fs_ / 1e6;
        if (next == next_i_) {
            next_i_ += kHalfIFs;
            dut_->clk_i ^= 1;
            if (dut_->clk_i) dut_->ptp_now_i = static_cast<uint64_t>(t_ns);
            dut_->eval();
            if (dut_->clk_i) drive();
        } else {
            next_a_ += kHalfAFs;
            dut_->clk_audio_i ^= 1;
            dut_->eval();
            a_.on_edge(dut_->a_bclk_o, dut_->a_fsync_o, dut_->a_dout_o, t_ns);
            b_.on_edge(dut_->b_bclk_o, dut_->b_fsync_o, dut_->b_dout_o, t_ns);
            collect(a_, true);
            collect(b_, false);
        }
    }
    void clk_cycle() {
        const double te = t_fs_ + 2 * kHalfIFs;
        while (t_fs_ < te) tick_one();
    }
    void run_ns(double ns) {
        const double te = t_fs_ + ns * 1e6;
        while (t_fs_ < te) tick_one();
    }

    //! a decoded frame of one interface, kept for the grade
    struct Seen {
        double sync;
        std::array<double, 32> msb;
        std::array<uint32_t, 32> value;
    };
    void collect(milan::tb::SlotMsbDecoder& dec, bool a) {
        while (!dec.done.empty()) {
            const auto& f = dec.done.front();
            (a ? seen_a_ : seen_b_).push_back(Seen{f.sync, f.msb, f.value});
            dec.done.pop_front();
        }
    }

    // ------------------------------------------------------------------ //
    //! the stream and channel interface a's or b's slot k is mapped to
    static std::pair<int, int> mapped(bool a, int k) {
        if (a) return k < 6 ? std::pair<int, int>{0, k} : std::pair<int, int>{2, k - 6};
        return k < 2 ? std::pair<int, int>{0, k} : std::pair<int, int>{1, k - 2};
    }

    struct Grade {
        long samples = 0, silent = 0, wrong_slot = 0, missing = 0, unexpected = 0;
        long in_band = 0;
        double max_err_small = 0;   //!< |err| at |phi| <= 4 %
        double max_snap = 0;        //!< |err + phi|, every phi
        double max_err_any = 0;     //!< |err|, every phi
    };

    Grade grade_one(bool a, const std::vector<Seen>& seen, const milan::tb::SlotMsbDecoder& dec) {
        Grade g;
        const auto& expect_ = a ? exp_a_ : exp_b_;
        const int slots = dec.slots;
        for (const Seen& f : seen) {
            // the grid frame this pin frame is: its instant against A's grid
            const long m = std::lround((f.sync - ref_sync_) / kPsActNs);
            if (m < first_frame_ - 2 || m > last_frame_ + 8) continue;
            for (int k = 0; k < slots; k++) {
                const auto [s, ch] = mapped(a, k);
                const uint32_t v = f.value[static_cast<size_t>(k)];
                const auto exp = expect_.find({s, m});
                if (v == 0) {
                    g.silent++;
                    if (exp != expect_.end()) g.missing++;
                    continue;
                }
                const int vs = static_cast<int>(v >> 22), vch = static_cast<int>((v >> 19) & 7);
                const long seq = static_cast<long>(v & 0x7FFFF);
                if (vs != s || vch != ch) { g.wrong_slot++; continue; }
                g.samples++;
                const auto pt = pt_.find({s, seq});
                if (pt == pt_.end()) { g.unexpected++; continue; }
                const double phi = phi_[{s, seq}];
                const double err = (f.msb[static_cast<size_t>(k)] - dec.slot_offset(k)) - pt->second;
                g.max_err_any = std::max(g.max_err_any, std::fabs(err));
                g.max_snap = std::max(g.max_snap, std::fabs(err + phi));
                if (std::fabs(phi) <= 0.041 * kPsNs) {
                    g.in_band++;
                    g.max_err_small = std::max(g.max_err_small, std::fabs(err));
                }
                if (exp == expect_.end() || exp->second != seq) g.unexpected++;
            }
        }
        return g;
    }

    void report(const char* n, const Grade& g, long expect_samples) {
        char what[260];
        std::printf("  info: [render %s] %ld samples (%ld at |phi| <= 4 %%), %ld silent slots, max |pin - PT| "
                    "%.1f ns at |phi| <= 4 %%, %.1f ns at any phi, max |pin - (PT - phi)| %.1f ns\n",
                    n, g.samples, g.in_band, g.silent, g.max_err_small, g.max_err_any, g.max_snap);
        std::snprintf(what, sizeof what,
                      "[render %s] every slot of every frame carries its mapped stream and channel or silence "
                      "(%ld misplaced)", n, g.wrong_slot);
        check_.that(what, g.wrong_slot == 0);
        std::snprintf(what, sizeof what,
                      "[render %s] every sample's slot-MSB pin instant, less its slot offset, is its "
                      "presentation time inside +/-5 %% of Ps (max %.1f ns over %ld samples)",
                      n, g.max_err_small, g.in_band);
        check_.that(what, g.in_band > 1000 && g.max_err_small < kBandNs);
        std::snprintf(what, sizeof what,
                      "[render %s] ...and is the frame instant nearest its presentation time at every phase "
                      "up to +/-0.45 Ps, inside %.0f ns (max %.1f ns)", n, kSnapNs, g.max_snap);
        check_.that(what, g.samples > 0 && g.max_snap <= kSnapNs);
        std::snprintf(what, sizeof what,
                      "[render %s] every sample a presented PDU carries reaches the pins, at holds of 0.1 to "
                      "2.6 ms, and nothing else does (%ld of %ld, %ld missing, %ld unexpected)",
                      n, g.samples, expect_samples, g.missing, g.unexpected);
        check_.that(what, g.missing == 0 && g.unexpected == 0 && g.samples == expect_samples);
    }

    void grade() {
        long exp_a = 0, exp_b = 0;
        for (const auto& [key, seq] : exp_a_) {
            (void)seq;
            exp_a += key.first == 0 ? 6 : 2;
        }
        exp_b = 2 * static_cast<long>(exp_b_.size());
        const Grade ga = grade_one(true, seen_a_, a_);
        const Grade gb = grade_one(false, seen_b_, b_);
        report("A", ga, exp_a);
        report("B", gb, exp_b);
        // a run of frames interface 0 (A) presents ends where the next has
        // none: streams 0 and 2 as A shows them, stream 1 as written
        long runs = 0;
        for (int s = 0; s < 3; s++) {
            const auto& e = s == 1 ? exp_b_ : exp_a_;
            for (long f = first_frame_; f <= last_frame_ + 8; f++)
                if (e.count({s, f}) && !e.count({s, f + 1})) runs++;
        }
        char what[220];
        std::printf("  info: [render] late %u, early %u, untimed %u, slips %u (runs %ld)\n",
                    dut_->late_o, dut_->early_o, dut_->untimed_o, dut_->slips_o, runs);
        std::snprintf(what, sizeof what,
                      "[render late] each late PDU (its first two events consumed; its timestamp 1 ms past) "
                      "is counted once (%u of %ld)", dut_->late_o, refused_late_);
        check_.that(what, static_cast<long>(dut_->late_o) == refused_late_);
        std::snprintf(what, sizeof what,
                      "[render early] each too-early PDU (its last two events past the queue; 3 ms ahead) "
                      "is counted once (%u of %ld)", dut_->early_o, refused_early_);
        check_.that(what, static_cast<long>(dut_->early_o) == refused_early_);
        std::snprintf(what, sizeof what, "[render untimed] the PDU without tv is counted once (%u of %ld)",
                      dut_->untimed_o, refused_untimed_);
        check_.that(what, static_cast<long>(dut_->untimed_o) == refused_untimed_);
        std::snprintf(what, sizeof what,
                      "[render] slips_o counts every run of presented frames that ends (%u of %ld)",
                      dut_->slips_o, runs);
        check_.that(what, static_cast<long>(dut_->slips_o) == runs);
        std::snprintf(what, sizeof what,
                      "[render] B's out-lead (%d) is at least a frame past A's (%d): post-grid delays a frame apart",
                      dut_->b_lead_o, dut_->a_lead_o);
        check_.that(what, dut_->b_lead_o >= dut_->a_lead_o + 1 && dut_->a_lead_o >= 1);
    }

    Vrender_wrap* dut_;
    milan::tb::Checker& check_;
    double t_fs_ = 0;
    double next_i_ = kHalfIFs;
    double next_a_ = kHalfAFs;
    milan::tb::SlotMsbDecoder a_{8, 1, 8 * 32 * 48000.0};
    milan::tb::SlotMsbDecoder b_{4, 1, 4 * 32 * 48000.0};
    double ref_sync_ = 0;
    std::vector<Pdu> pdus_;
    size_t next_pdu_ = 0;
    size_t cur_ = 0;
    enum { IDLE, LEAD, BEATS } state_ = IDLE;
    int lead_ = 0;
    int beat_ = 0;
    //! what each interface must show: (stream, frame) -> the sample number
    std::map<std::pair<int, long>, long> exp_a_;
    std::map<std::pair<int, long>, long> exp_b_;
    long refused_late_ = 0, refused_early_ = 0, refused_untimed_ = 0;
    std::map<std::pair<int, long>, double> pt_;
    std::map<std::pair<int, long>, double> phi_;
    long first_frame_ = 0;
    long last_frame_ = 0;
    std::vector<Seen> seen_a_;
    std::vector<Seen> seen_b_;
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vrender_wrap> model;
    milan::tb::Checker check{"media_phase render"};
    check.echo_passes();
    std::printf("[render] two render interfaces on one clock domain, post-grid delays a frame apart, graded at "
                "their pins\n");
    RenderHarness harness(model.get(), check);
    return harness.run();
}
