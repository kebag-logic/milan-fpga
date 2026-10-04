// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The media-clock plane and the two listener rings through a source change
// and through an INTERNAL aligner pull-in (#645, #647), on follow_ring_wrap.sv.
//
// THE BENCH IT REPEATS (docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md,
// lanes B7 and B8). The reference peer's media clock runs 11.02 ppm slow of
// gPTP time (the meter's and the CRF sink's +11.02 ppm, "positive means the
// talker's clock is slow"); the DUT's INTERNAL clock runs 5.1 ppm slow (the
// MMCM plan's -10.64 ppm plus its oscillator), so the DUT reads 5.92 ppm
// faster than the peer writes and its loopback ring slips one frame every
// 3.52 s at INTERNAL (B0's 342 dups in 600 s). The two boards' oscillators
// are 16.5 ppm apart. The peer's stream is 4 channels: two LOOP pairs, so
// one slipped frame is 2 on SLIP_LB.
//
// THE CLOCKS (one femtosecond wheel; nothing is time-compressed):
//   clk_i  CLK_HZ_TB (6.25 MHz): the axis clock. ptp_now_i is the wheel's
//          own time in ns: the gPTP plane is ideal;
//   audio  24.576 MHz / 32 at the DUT's INTERNAL offset, its edges moved by
//          the behavioral MMCM's fine phase steps (1 ns each, GAIN_NUM_P 1:
//          one step per 1 ms tick per ppm, the servo's design plant gain);
//   ps_clk 1 MHz, PSDONE 2 PSCLK cycles after PSEN (the servo waits for
//          PSDONE and never counts cycles; milan_dp_mclk's choice).
// The servo's windows, gains and lock rule, the meter's E8 estimator, the
// aligner's loop in sample units and every ring are therefore the shipping
// ones on real time: a 512 ms window is 512 ms of the wheel.
//
// WHAT IS MEASURED, PER PDU OF THE FOLLOWED STREAM:
//   ring margin m   the loopback ring's (pair 0) time from a PDU's first
//                   event landing in the queue to the pop that takes it, in
//                   media ticks. The ring's law gives it a range of (0, 3]
//                   ticks: below 0 a tick finds the queue empty (a dup, and
//                   m gains a tick), above 3 a push finds it full (a skip,
//                   and m loses a tick). The ring has no setpoint and nothing
//                   re-centres it.
//   render fill     the render stage's fill at the PDU end (#643's grading
//                   instant): the law is the setpoint plus the PDU, 14;
//   render delay    the PDU's first event from its end to its pop, in ticks:
//                   the law is (8, 9].
//
// Usage: Vfollow_ring [--case b8|pullin] [options]   (see usage())

#include "../../common/verilator_harness.hpp"
#include "../mmcm_servo/mmcm_model.h"
#include "Vfollow_ring_wrap.h"
#include "Vfollow_ring_wrap___024root.h"
#include "verilated.h"

#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <random>
#include <string>
#include <vector>

namespace {

constexpr double kClkHz = CLK_HZ_TB;
constexpr double kHalfClk = 0.5e15 / kClkHz;
constexpr double kAudioHz = 24.576e6 / 32.0;
constexpr double kHalfPs = 0.5e15 / 1e6;
constexpr double kTickFs = 1e15 / 48000.0;        //! one nominal media tick
constexpr double kPduNs = 125'000.0;              //! 6 samples at 48 kHz
constexpr double kCrfNs = 2'000'000.0;            //! 96 samples at 48 kHz
constexpr double kPresNs = 2'000'000.0;           //! presentation / max transit time
constexpr int kChans = 4;                         //! the peer's stream
constexpr int kBeats = 6 * kChans / 2;            //! 64-bit beats per PDU
//! the payload clone's beat spacing on silicon: 8 axis cycles at 50 MHz
//! (KL_chan_map_capture's banner), in this harness's cycles
constexpr int kBeatCycRaw = static_cast<int>(CLK_HZ_TB * 160e-9 + 0.5);
constexpr int kBeatCyc = kBeatCycRaw > 0 ? kBeatCycRaw : 1;
constexpr int kStateLocked = 4;
constexpr uint16_t kSrcInternal = 0;
constexpr uint16_t kSrcCrf = 1;
constexpr uint16_t kSrcAaf = 2;

struct Options {
    std::string scenario = "b8";
    double peer_ppm = -11.02;                     //! the peer against gPTP
    bool peer_given = false;                      //! --peer-ppm named on the command line
    double dut_ppm = -5.10;                       //! the DUT's INTERNAL clock against gPTP
    double latency_us = 200.0;                    //! the AAF PDU's wire-to-queue latency
    double start_s = 0.6;                         //! the talkers start, after the boot pull-in
    double jitter_us = 0.0;                       //! extra lateness, uniform in [0, J]
    //! rare queueing behind interfering frames: with probability P per PDU,
    //! a further lateness uniform in [0, T] (one 1,500-octet frame is 12 us
    //! at 1 Gb/s)
    double tail_us = 0.0;
    double tail_p = 0.0;
    uint64_t seed = 645;
    double dwell_s = 4.0;                         //! INTERNAL before the set
    double set_phase = 0.0;                       //! the set's place in one INTERNAL beat
    double hold_s = 60.0;                         //! after the INTERNAL-to-AAF set
    double switch_hold_s = 0.0;                   //! each stream-to-stream hold (0 = none)
    double hold_us = 52.0;                        //! pullin: the serial-clock hold
    //! a planted control: one harness recentre pulse into the render stage,
    //! this long after the hold (pullin) or after LOCKED (b8); < 0 = none
    double inject_s = -1.0;
    std::string trace;                            //! per-PDU CSV
    std::string servo_trace;                      //! per-window CSV
    std::string grid_trace;                       //! per-millisecond CSV: the aligner and the settle
};

void usage() {
    std::puts(
        "Vfollow_ring --case b8      INTERNAL dwell, the INTERNAL-to-AAF set, the hold, then\n"
        "                            (with --switch-hold) AAF to CRF and CRF to AAF\n"
        "Vfollow_ring --case pullin  INTERNAL, a talker on the DUT's own clock (unless\n"
        "                            --peer-ppm names another), one\n"
        "                            serial-clock hold, the render stage before and after\n"
        "  --peer-ppm P --dut-ppm D --latency-us L --jitter-us J --tail-us T --tail-p P\n"
        "  --seed N --start-s S\n"
        "  --dwell-s S --set-phase F (0..1 of one INTERNAL beat) --hold-s S\n"
        "  --switch-hold-s S --hold-us U --inject-recentre-s S (a planted control)\n"
        "  --trace FILE --servo-trace FILE --grid-trace FILE");
}

bool parse(int argc, char** argv, Options& o) {
    for (int i = 1; i < argc; ++i) {
        const std::string a = argv[i];
        const bool has = i + 1 < argc;
        auto num = [&](double& v) { v = std::strtod(argv[++i], nullptr); };
        if (a == "--case" && has) o.scenario = argv[++i];
        else if (a == "--peer-ppm" && has) {
            num(o.peer_ppm);
            o.peer_given = true;
        }
        else if (a == "--dut-ppm" && has) num(o.dut_ppm);
        else if (a == "--latency-us" && has) num(o.latency_us);
        else if (a == "--start-s" && has) num(o.start_s);
        else if (a == "--jitter-us" && has) num(o.jitter_us);
        else if (a == "--tail-us" && has) num(o.tail_us);
        else if (a == "--tail-p" && has) num(o.tail_p);
        else if (a == "--seed" && has) o.seed = std::strtoull(argv[++i], nullptr, 0);
        else if (a == "--dwell-s" && has) num(o.dwell_s);
        else if (a == "--set-phase" && has) num(o.set_phase);
        else if (a == "--hold-s" && has) num(o.hold_s);
        else if (a == "--switch-hold-s" && has) num(o.switch_hold_s);
        else if (a == "--hold-us" && has) num(o.hold_us);
        else if (a == "--inject-recentre-s" && has) num(o.inject_s);
        else if (a == "--trace" && has) o.trace = argv[++i];
        else if (a == "--servo-trace" && has) o.servo_trace = argv[++i];
        else if (a == "--grid-trace" && has) o.grid_trace = argv[++i];
        else if (a.rfind("+verilator", 0) == 0) continue;
        else return false;
    }
    return o.scenario == "b8" || o.scenario == "pullin";
}

//! One PDU of the followed stream, from its arrival to its two ring readings.
struct PduRec {
    uint64_t n = 0;
    double arrive_s = 0.0;
    double margin_ticks = NAN;                    //! the loopback ring's m
    int render_fill = -1;
    double render_delay_ticks = NAN;
};

class Bench {
 public:
    Bench(Vfollow_ring_wrap* d, const Options& o) : dut(d), opt(o), rng_(o.seed) {
        half_audio0_ = 0.5e15 / kAudioHz / (1.0 + opt.dut_ppm * 1e-6);
        next_audio_ = half_audio0_;
        base_audio_ = half_audio0_;
        aaf_space_ns_ = kPduNs / (1.0 + opt.peer_ppm * 1e-6);
        crf_space_ns_ = kCrfNs / (1.0 + opt.peer_ppm * 1e-6);
    }

    Vfollow_ring_wrap* dut;
    const Options& opt;
    MmcmModel mm{};
    std::vector<PduRec> pdus;

    void reset() {
        mm.regs[0x08] = 0x0595;
        mm.regs[0x09] = 0x0080;
        mm.step_fs = 1e6;
        mm.ps_lat = 2;
        dut->rst_n = 0;
        dut->mmcm_locked_i = 1;
        dut->clk_src_idx_i = kSrcInternal;
        dut->pcm_chans_i = kChans;
        run_for(20e-6);
        dut->rst_n = 1;
        run_for(10e-6);
    }

    //! the peer's talkers start: the first PDU's media instant is `at_s`
    void start_talkers(double at_s) {
        t0_ns_ = at_s * 1e9;
        talking_ = true;
        aaf_n_ = 0;
        crf_n_ = 0;
        next_arrival_fs_ = arrival_fs(0);
        next_crf_fs_ = (t0_ns_ + opt.latency_us * 1e3) * 1e6;
    }

    void select(uint16_t src) {
        dut->clk_src_idx_i = src;
        std::printf("  info: t=%.6f s  CLOCK_SOURCE <- %u\n", now_s(), src);
    }

    void run_for(double s) { run_until(t_fs_ + s * 1e15); }
    void run_until(double until_fs) {
        while (t_fs_ < until_fs) step();
    }
    double now_s() const { return t_fs_ * 1e-15; }

    int servo_state() const { return static_cast<int>(dut->servo_status_o & 7); }
    double trim_ppm() const { return static_cast<int16_t>(dut->servo_status_o >> 16) / 16.0; }
    uint32_t dups() const { return dut->lb_dup_o; }
    uint32_t skips() const { return dut->lb_skip_o; }

    //! a planted control: one recentre pulse into the render stage
    void inject_recentre() {
        dut->tb_recentre_p_i = 1;
        run_until(t_fs_ + 2.0 * kHalfClk + 1.0);
        dut->tb_recentre_p_i = 0;
    }

    //! the serial-clock hold, from now
    void frame_hold(double us) {
        dut->frame_hold_i = 1;
        run_for(us * 1e-6);
        dut->frame_hold_i = 0;
    }

    // what the run saw
    double first_locked_s = -1.0;
    std::vector<double> dup_times;                //! one per slipped frame (pair 0)
    std::vector<double> recentre_times;
    uint32_t render_recentres() const { return dut->render_recentres_o; }

    //! the window and millisecond traces
    FILE* servo_trace = nullptr;
    FILE* grid_trace = nullptr;

 private:
    double t_fs_ = 0.0;
    double next_clk_ = kHalfClk;
    double next_ps_ = kHalfPs;
    double half_audio0_;
    double base_audio_;
    double next_audio_;
    std::mt19937_64 rng_;
    double aaf_space_ns_;
    double crf_space_ns_;

    // the peer
    bool talking_ = false;
    double t0_ns_ = 0.0;
    uint64_t aaf_n_ = 0;
    uint64_t crf_n_ = 0;
    double next_arrival_fs_ = 0.0;
    double next_crf_fs_ = 0.0;
    int beat_ = -1;                               //! the payload beat in flight
    int beat_gap_ = 0;
    uint64_t beat_pdu_ = 0;

    // the loopback ring's pair-0 queue, mirrored from its pointers
    struct Ev {
        double push_fs;
        uint64_t pdu;
        int event;
    };
    std::deque<Ev> q_;
    uint8_t q_wr_q_ = 0;
    uint8_t q_rd_q_ = 0;
    uint64_t push_count_ = 0;
    uint16_t dup_q_ = 0;
    uint16_t skip_q_ = 0;

    // the render stage
    bool pend_end_ = false;
    int end_wait_ = 0;
    uint64_t end_pdu_ = 0;
    double end_fs_ = 0.0;
    uint64_t end_pops_ = 0;
    uint64_t pop_total_ = 0;
    //! PDUs whose first event has not popped yet: (pdu, that pop's number, end)
    struct Want {
        uint64_t pdu;
        uint64_t pop;
        double end_fs;
    };
    std::deque<Want> wants_;
    uint16_t recentres_q_ = 0;

    // the servo windows
    uint8_t pp_seq_q_ = 0;
    bool locked_seen_ = false;

    double arrival_fs(uint64_t n) {
        const double tx = t0_ns_ + static_cast<double>(n) * aaf_space_ns_;
        double lat = opt.latency_us * 1e3;
        if (opt.jitter_us > 0.0) {
            std::uniform_real_distribution<double> u(0.0, opt.jitter_us * 1e3);
            lat += u(rng_);
        }
        if (opt.tail_p > 0.0) {
            std::uniform_real_distribution<double> c(0.0, 1.0);
            if (c(rng_) < opt.tail_p) {
                std::uniform_real_distribution<double> u(0.0, opt.tail_us * 1e3);
                lat += u(rng_);
            }
        }
        return (tx + lat) * 1e6;
    }

    void step() {
        if (next_clk_ <= next_ps_ && next_clk_ <= next_audio_) {
            t_fs_ = next_clk_;
            next_clk_ += kHalfClk;
            dut->clk_i ^= 1;
            if (dut->clk_i) before_rise();
            dut->eval();
            if (dut->clk_i) after_rise();
        } else if (next_ps_ <= next_audio_) {
            t_fs_ = next_ps_;
            next_ps_ += kHalfPs;
            dut->ps_clk_i ^= 1;
            dut->eval();
            if (dut->ps_clk_i) {
                mm.psclk_edge(dut->ps_en_o, dut->ps_incdec_o, dut->mmcm_rst_o);
                dut->ps_done_i = mm.psdone;
            }
        } else {
            t_fs_ = next_audio_;
            base_audio_ += half_audio0_;
            next_audio_ = base_audio_ + mm.audio_adj_fs;
            if (next_audio_ <= t_fs_) next_audio_ = t_fs_ + 1e3;
            dut->clk_audio_i ^= 1;
            dut->eval();
        }
    }

    //! the inputs for this rising edge
    void before_rise() {
        dut->ptp_now_i = static_cast<uint64_t>(t_fs_ / 1e6);
        dut->aaf_match_p_i = 0;
        dut->crf_frame_p_i = 0;
        dut->pcm_tvalid_i = 0;
        dut->pcm_tlast_i = 0;
        if (!talking_) return;
        if (beat_ < 0 && t_fs_ >= next_arrival_fs_) {
            const uint64_t n = aaf_n_++;
            const double tx = t0_ns_ + static_cast<double>(n) * aaf_space_ns_;
            dut->aaf_match_p_i = 1;
            dut->aaf_seq_i = static_cast<uint8_t>(n & 0xFF);
            dut->aaf_ts_i = static_cast<uint32_t>(static_cast<uint64_t>(std::floor(tx + kPresNs)));
            dut->aaf_mr_i = 0;
            PduRec r;
            r.n = n;
            r.arrive_s = t_fs_ * 1e-15;
            pdus.push_back(r);
            beat_ = 0;
            beat_gap_ = kBeatCyc;
            beat_pdu_ = n;
            next_arrival_fs_ = arrival_fs(aaf_n_);
            if (next_arrival_fs_ <= t_fs_) next_arrival_fs_ = t_fs_ + 1.0;
        } else if (beat_ >= 0) {
            if (--beat_gap_ <= 0) {
                //! sample (pdu, event, channel) carries a ramp the loop keeps
                uint64_t d = 0;
                for (int s = 0; s < 2; ++s) {
                    const int k = beat_ * 2 + s;
                    const uint32_t v = static_cast<uint32_t>((beat_pdu_ * 6 + k / kChans) & 0xFFFFF) << 4 |
                                       static_cast<uint32_t>(k % kChans);
                    const uint32_t be = (v & 0xFF) << 16 | ((v >> 8) & 0xFF) << 8 | ((v >> 16) & 0xFF);
                    d |= static_cast<uint64_t>(be) << (32 * s);
                }
                dut->pcm_tdata_i = d;
                dut->pcm_tvalid_i = 1;
                dut->pcm_tlast_i = (beat_ == kBeats - 1);
                if (beat_ == kBeats - 1) {
                    pend_end_ = true;
                    end_wait_ = 2;
                    end_pdu_ = beat_pdu_;
                    end_fs_ = t_fs_;
                    end_pops_ = pop_total_;
                    beat_ = -1;
                } else {
                    ++beat_;
                    beat_gap_ = kBeatCyc;
                }
            }
        }
        if (t_fs_ >= next_crf_fs_) {
            const uint64_t m = crf_n_++;
            const double tx = t0_ns_ + static_cast<double>(m) * crf_space_ns_;
            dut->crf_frame_p_i = 1;
            dut->crf_seq_i = static_cast<uint8_t>(m & 0xFF);
            dut->crf_ts_i = static_cast<uint64_t>(std::floor(tx + kPresNs));
            dut->crf_mr_i = 0;
            next_crf_fs_ = (t0_ns_ + static_cast<double>(crf_n_) * crf_space_ns_ +
                            opt.latency_us * 1e3) * 1e6;
        }
    }

    void after_rise() {
        mm.dclk_edge(dut->drp_addr_o, dut->drp_en_o, dut->drp_we_o, dut->drp_di_o,
                     dut->mmcm_rst_o);
        dut->drp_do_i = mm.dout;
        dut->drp_rdy_i = mm.drdy;
        dut->mmcm_locked_i = mm.locked;
        watch_ring();
        watch_render();
        watch_servo();
        watch_grid();
    }

    //! every millisecond: the aligner's error and trim, and the #386 settle's
    //! pending flag and in-band run (the recentre window)
    double next_grid_fs_ = 0.0;
    void watch_grid() {
        if (!grid_trace || t_fs_ < next_grid_fs_) return;
        next_grid_fs_ = t_fs_ + 1e12;
        auto* r = dut->rootp;
        std::fprintf(grid_trace, "%.6f,%d,%d,%d,%d,%d,%d\n", now_s(),
                     static_cast<int>(r->follow_ring_wrap__DOT__mga_engaged_w),
                     static_cast<int>(static_cast<int16_t>(r->follow_ring_wrap__DOT__mga_err_w)),
                     static_cast<int>(static_cast<int16_t>(r->follow_ring_wrap__DOT__mnco_servo_trim_w)),
                     static_cast<int>(r->follow_ring_wrap__DOT__src_pend_r),
                     static_cast<int>(r->follow_ring_wrap__DOT__src_band_ticks_r),
                     static_cast<int>(dut->render_fill_o));
    }

    //! The loopback ring's pair 0, from its own pointers: every write is one
    //! event landing, every read one pop or one drop-oldest.
    void watch_ring() {
        auto* r = dut->rootp;
        const uint8_t wr = r->follow_ring_wrap__DOT__chan_map_capture__DOT__q_wr_r[0];
        const uint8_t rd = r->follow_ring_wrap__DOT__chan_map_capture__DOT__q_rd_r[0];
        const uint16_t sk = dut->lb_skip_o;
        const uint16_t dp = dut->lb_dup_o;
        if (wr != q_wr_q_) {
            const uint64_t k = push_count_++;
            q_.push_back(Ev{t_fs_, k / 6, static_cast<int>(k % 6)});
        }
        if (rd != q_rd_q_ && !q_.empty()) {
            const Ev e = q_.front();
            q_.pop_front();
            if (sk == skip_q_ && e.event == 0 && e.pdu < pdus.size()) {
                pdus[e.pdu].margin_ticks = (t_fs_ - e.push_fs) / kTickFs;
            }
        }
        //! two dups per slipped frame (the stream's two pairs, a cycle or
        //! more apart in the pre-walk): the frame is counted at the first
        for (uint32_t i = dup_q_; i < dp; ++i) {
            if (i % 2 == 0) dup_times.push_back(now_s());
        }
        q_wr_q_ = wr;
        q_rd_q_ = rd;
        skip_q_ = sk;
        dup_q_ = dp;
    }

    //! The render stage at the PDU end (#643's grading instant, the beat
    //! with tlast): its fill there is the fill once the last row is in plus
    //! any pop since the end, and the PDU's first event is the pop that many
    //! pops, less the PDU's own six, after the end.
    void watch_render() {
        if (dut->render_pop_p_o) {
            ++pop_total_;
            while (!wants_.empty() && wants_.front().pop <= pop_total_) {
                const Want w = wants_.front();
                wants_.pop_front();
                if (w.pop == pop_total_ && w.pdu < pdus.size()) {
                    //! less the pop pulse's one-cycle register (#643's band)
                    pdus[w.pdu].render_delay_ticks = (t_fs_ - w.end_fs - 2.0 * kHalfClk) / kTickFs;
                }
            }
        }
        if (pend_end_ && --end_wait_ <= 0) {
            pend_end_ = false;
            const int fill = static_cast<int>(dut->render_fill_o) +
                             static_cast<int>(pop_total_ - end_pops_);
            if (end_pdu_ < pdus.size()) pdus[end_pdu_].render_fill = fill;
            const uint64_t first = end_pops_ + static_cast<uint64_t>(std::max(fill - 6, 0)) + 1;
            if (!dut->render_prefill_o && fill >= 6 && first > pop_total_)
                wants_.push_back(Want{end_pdu_, first, end_fs_});
        }
        //! a prefill drops what was queued: those pops never come
        if (dut->render_prefill_o) wants_.clear();
        const uint16_t rc = dut->render_recentres_o;
        if (rc != recentres_q_) recentre_times.push_back(now_s());
        recentres_q_ = rc;
    }

    void watch_servo() {
        auto* r = dut->rootp;
        const int st = servo_state();
        if (st == kStateLocked && !locked_seen_) {
            locked_seen_ = true;
            if (first_locked_s < 0.0) first_locked_s = now_s();
        }
        if (st != kStateLocked) locked_seen_ = false;
        const uint8_t seq = r->follow_ring_wrap__DOT__mmcm_servo__DOT__pp_seq_r;
        if (seq == 0 && pp_seq_q_ == 7 && servo_trace) {
            std::fprintf(servo_trace, "%.6f,%d,%d,%d,%d,%.4f,%d,%d,%d\n", now_s(), st,
                         static_cast<int>(r->follow_ring_wrap__DOT__mmcm_servo__DOT__pp_run_r),
                         static_cast<int>(r->follow_ring_wrap__DOT__mmcm_servo__DOT__ew_r),
                         static_cast<int>(r->follow_ring_wrap__DOT__mmcm_servo__DOT__integ_r),
                         trim_ppm(), static_cast<int>(r->follow_ring_wrap__DOT__aafm_rate_w),
                         static_cast<int>(r->follow_ring_wrap__DOT__aafm_rate_valid_w),
                         static_cast<int>(static_cast<int16_t>(r->follow_ring_wrap__DOT__mga_err_w)));
        }
        pp_seq_q_ = seq;
    }
};

void write_trace(const Bench& b, const std::string& path) {
    if (path.empty()) return;
    FILE* f = std::fopen(path.c_str(), "w");
    if (!f) return;
    std::fprintf(f, "pdu,arrive_s,ring_margin_ticks,render_fill,render_delay_ticks\n");
    for (const auto& p : b.pdus) {
        std::fprintf(f, "%llu,%.7f,%.4f,%d,%.4f\n", static_cast<unsigned long long>(p.n),
                     p.arrive_s, p.margin_ticks, p.render_fill, p.render_delay_ticks);
    }
    std::fclose(f);
}

//! A value range over a window of PDUs.
struct Range {
    double lo = 1e9;
    double hi = -1e9;
    void take(double v) {
        lo = std::min(lo, v);
        hi = std::max(hi, v);
    }
};

//! the ring margin's range over PDUs arriving in [a, e) seconds
Range margin_range(const Bench& b, double a, double e) {
    Range r;
    for (const auto& p : b.pdus) {
        if (p.arrive_s < a || p.arrive_s >= e || std::isnan(p.margin_ticks)) continue;
        r.take(p.margin_ticks);
    }
    return r;
}

int count_in(const std::vector<double>& v, double a, double e) {
    int n = 0;
    for (const double t : v) n += (t >= a && t < e) ? 1 : 0;
    return n;
}

//! #643's ambiguity window, in this harness's cycles: a PDU end whose nearest
//! pop is closer than this reads its fill on either side of that pop, so a
//! window holding one is not gradable
constexpr double kAmbigTicks = 3.0 * 48000.0 / kClkHz;

//! The render law over a window: fill 14 and delay (8, 9]. `clear` is the
//! least distance from a PDU end to its nearest pop, in ticks: below
//! kAmbigTicks the window is not gradable.
struct Law {
    int n = 0;
    int off_fill = 0;
    int off_band = 0;
    Range delay;
    Range fill;
    double clear = 1e9;
    bool gradable() const { return clear >= kAmbigTicks; }
    bool on_law() const { return n > 0 && off_fill == 0 && off_band == 0; }
};

Law render_law(const Bench& b, double a, double e) {
    Law w;
    for (const auto& p : b.pdus) {
        if (p.arrive_s < a || p.arrive_s >= e || p.render_fill < 0 || std::isnan(p.render_delay_ticks))
            continue;
        ++w.n;
        w.off_fill += (p.render_fill != 14) ? 1 : 0;
        w.off_band += (p.render_delay_ticks <= 8.0 || p.render_delay_ticks > 9.0) ? 1 : 0;
        w.delay.take(p.render_delay_ticks);
        w.fill.take(static_cast<double>(p.render_fill));
        const double off = p.render_delay_ticks - static_cast<double>(p.render_fill - 6);
        w.clear = std::min(w.clear, std::min(std::fabs(off), std::fabs(1.0 - off)));
    }
    return w;
}

void print_window(const Bench& b, const char* name, double a, double e) {
    const Range m = margin_range(b, a, e);
    const Law w = render_law(b, a, e);
    std::printf("  info: %-26s [%8.3f, %8.3f) s: ring slips %d, margin %+.3f..%+.3f ticks; "
                "render n %d fill %.0f..%.0f (off-law %d), delay %.3f..%.3f (out of band %d), "
                "end-to-pop clearance %.3f ticks%s\n",
                name, a, e, count_in(b.dup_times, a, e), m.lo, m.hi, w.n, w.fill.lo, w.fill.hi, w.off_fill,
                w.delay.lo, w.delay.hi, w.off_band, w.clear, w.gradable() ? "" : " NOT GRADABLE");
}

//! b8: the set at a chosen place in one INTERNAL beat: the next slip, then
//! that fraction of a beat later, so the ring's margin at the set runs from
//! about one tick (phase 0) down to its edge (phase 1). A peer on the DUT's
//! own clock (the control) has no beat: the set is immediate.
void wait_for_the_set(Bench& b, const Options& o, double beat_s) {
    if (std::fabs(o.dut_ppm - o.peer_ppm) <= 0.05) return;
    const size_t slips0 = b.dup_times.size();
    const double guard = (b.now_s() + 2.0 * beat_s) * 1e15;
    while (b.dup_times.size() == slips0 && b.now_s() * 1e15 < guard) b.run_for(1e-3);
    if (b.dup_times.size() > slips0) b.run_until((b.dup_times.back() + o.set_phase * beat_s) * 1e15);
}

//! b8: every slip and render recentre from the set on, against LOCKED
void print_events(const Bench& b, double t_set, double t_lock) {
    for (const double t : b.dup_times) {
        if (t >= t_set) {
            std::printf("  info: slip at %.4f s after the set, %+.4f s from LOCKED\n", t - t_set, t - t_lock);
        }
    }
    for (const double t : b.recentre_times) {
        if (t >= t_set) {
            std::printf("  info: render recentre at %.4f s after the set, %+.4f s from LOCKED\n", t - t_set,
                        t - t_lock);
        }
    }
}

//! b8: AAF to CRF and CRF to AAF, each held, graded as lane B8 graded them
void run_switches(Bench& b, const Options& o, milan::tb::Checker& ck) {
    const uint32_t d0 = b.dups();
    b.first_locked_s = -1.0;
    b.select(kSrcCrf);
    const double t1 = b.now_s();
    b.run_for(o.switch_hold_s);
    const double l1 = b.first_locked_s;
    const uint32_t d1 = b.dups();
    b.first_locked_s = -1.0;
    b.select(kSrcAaf);
    const double t2 = b.now_s();
    b.run_for(o.switch_hold_s);
    const double l2 = b.first_locked_s;
    const uint32_t d2 = b.dups();
    std::printf("  info: AAF to CRF: LOCKED %.3f s after, ring slips %u; CRF to AAF: LOCKED %.3f s "
                "after, ring slips %u\n",
                l1 - t1, (d1 - d0) / 2, l2 - t2, (d2 - d1) / 2);
    print_window(b, "AAF to CRF hold", t1, t2);
    print_window(b, "CRF to AAF hold", t2, b.now_s());
    ck.that("[SW] AAF to CRF re-locks", l1 > 0.0);
    ck.that("[SW] CRF to AAF re-locks", l2 > 0.0);
    ck.dec("[SW] no ring slip across the AAF to CRF switch", (d1 - d0) / 2, 0);
    ck.dec("[SW] no ring slip across the CRF to AAF switch", (d2 - d1) / 2, 0);
}

int run_b8(Bench& b, const Options& o, milan::tb::Checker& ck) {
    const double beat_s = 1.0 / (48000.0 * std::fabs(o.dut_ppm - o.peer_ppm) * 1e-6);
    b.start_talkers(o.start_s);
    b.run_until((o.start_s + o.dwell_s) * 1e15);
    wait_for_the_set(b, o, beat_s);
    const double t_int_end = b.now_s();
    const Range at_set = margin_range(b, t_int_end - 0.25, t_int_end);
    std::printf("  info: INTERNAL: %zu slips in %.3f s (beat %.3f s); margin at the set %+.3f..%+.3f ticks\n",
                b.dup_times.size(), t_int_end, beat_s, at_set.lo, at_set.hi);
    b.first_locked_s = -1.0;
    b.select(kSrcAaf);
    const double t_set = b.now_s();
    if (o.inject_s >= 0.0) {
        while (b.first_locked_s < 0.0 && b.now_s() < t_set + o.hold_s) b.run_for(1e-3);
        if (b.first_locked_s > 0.0) b.run_until((b.first_locked_s + o.inject_s) * 1e15);
        b.inject_recentre();
    }
    b.run_until((t_set + o.hold_s) * 1e15);
    const double t_lock = b.first_locked_s;
    const double t_end = b.now_s();
    std::printf("  info: INTERNAL-to-AAF: LOCKED %.3f s after the set; trim %+.3f ppm at the end\n",
                t_lock - t_set, b.trim_ppm());
    print_events(b, t_set, t_lock);
    print_window(b, "INTERNAL, last second", t_set - 1.0, t_set);
    print_window(b, "set to LOCKED", t_set, t_lock);
    print_window(b, "LOCKED to the hold's end", t_lock, t_end);
    print_window(b, "the hold's last 10 s", t_end - 10.0, t_end);
    const Range at_lock = margin_range(b, t_lock, t_lock + 0.5);
    const Law last = render_law(b, t_end - 10.0, t_end);
    double last_after = -1.0;
    for (const double t : b.dup_times) {
        if (t >= t_lock && t < t_end) last_after = t - t_lock;
    }
    std::printf("RESULT-645: phase %.4f jitter %.1f us tail %.1f us p %.0e: slips set-to-LOCKED %d, "
                "after LOCKED %d (last %+.2f s), margin at LOCKED %+.3f..%+.3f ticks, LOCKED %.2f s, "
                "render at the end fill %.0f..%.0f delay %.3f..%.3f%s\n",
                o.set_phase, o.jitter_us, o.tail_us, o.tail_p, count_in(b.dup_times, t_set, t_lock),
                count_in(b.dup_times, t_lock, t_end), last_after, at_lock.lo, at_lock.hi, t_lock - t_set,
                last.fill.lo, last.fill.hi, last.delay.lo, last.delay.hi,
                !last.gradable() ? " (not gradable)" : last.on_law() ? " (on the law)" : " (off the law)");
    ck.that("[B8] the servo read LOCKED within 15 s of the INTERNAL-to-AAF set",
            t_lock > 0.0 && t_lock - t_set <= 15.0);
    if (o.switch_hold_s > 0.0) run_switches(b, o, ck);
    return 0;
}

int run_pullin(Bench& b, const Options& o, milan::tb::Checker& ck) {
    b.start_talkers(o.start_s);
    b.run_until((o.start_s + o.dwell_s) * 1e15);
    const double t_hold = b.now_s();
    const uint32_t rc0 = b.render_recentres();
    print_window(b, "before the hold, last 0.5 s", t_hold - 0.5, t_hold);
    b.frame_hold(o.hold_us);
    if (o.inject_s >= 0.0) {
        b.run_for(o.inject_s);
        b.inject_recentre();
        b.run_until((t_hold + 1.0) * 1e15);
    } else {
        b.run_for(1.0);
    }
    const double t_end = b.now_s();
    print_window(b, "the pull, first 0.2 s", t_hold, t_hold + 0.2);
    print_window(b, "after the pull, 0.5..1 s", t_hold + 0.5, t_end);
    const uint32_t rc1 = b.render_recentres();
    const Law w0 = render_law(b, t_hold - 0.5, t_hold);
    const Law w1 = render_law(b, t_hold + 0.5, t_end);
    const char* verdict = !w0.gradable() ? "BEFORE NOT GRADABLE"
                        : !w0.on_law()   ? "OFF-LAW BEFORE"
                        : !w1.gradable() ? "AFTER NOT GRADABLE"
                        : !w1.on_law()   ? "LEFT THE LAW" : "ON THE LAW";
    std::printf("RESULT-647: latency %.2f us hold %.1f us: delay %.3f..%.3f -> %.3f..%.3f ticks "
                "(shift %+.3f), fill %.0f..%.0f -> %.0f..%.0f, clearance %.3f -> %.3f ticks, recentres %u: %s\n",
                o.latency_us, o.hold_us, w0.delay.lo, w0.delay.hi, w1.delay.lo, w1.delay.hi,
                0.5 * (w1.delay.lo + w1.delay.hi - w0.delay.lo - w0.delay.hi), w0.fill.lo, w0.fill.hi, w1.fill.lo,
                w1.fill.hi, w0.clear, w1.clear, rc1 - rc0, verdict);
    ck.that("[PULLIN] the stream was on the render law, or not gradable, before the hold",
            w0.n > 0 && (!w0.gradable() || w0.on_law()));
    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Options o;
    if (!parse(argc, argv, o)) {
        usage();
        return 2;
    }
    //! the pull-in case grades a stream that does not drift: unless named,
    //! its talker runs on the DUT's own INTERNAL clock
    if (o.scenario == "pullin" && !o.peer_given) o.peer_ppm = o.dut_ppm;
    const milan::tb::Model<Vfollow_ring_wrap> model;
    milan::tb::Checker ck{"follow_ring"};
    Bench b{model.get(), o};
    FILE* st = nullptr;
    if (!o.servo_trace.empty()) {
        st = std::fopen(o.servo_trace.c_str(), "w");
        if (st) std::fprintf(st, "t_s,state,pi_run,ew_ns,integ,trim_ppm,meter_rate,meter_valid,mga_err\n");
    }
    b.servo_trace = st;
    FILE* gt = nullptr;
    if (!o.grid_trace.empty()) {
        gt = std::fopen(o.grid_trace.c_str(), "w");
        if (gt) {
            std::fprintf(gt, "t_s,mga_engaged,mga_err_cyc,mga_trim_16th_ppm,settle_pend,settle_band_ticks,"
                             "render_fill\n");
        }
    }
    b.grid_trace = gt;
    b.reset();
    if (o.scenario == "pullin") run_pullin(b, o, ck);
    else run_b8(b, o, ck);
    if (st) std::fclose(st);
    if (gt) std::fclose(gt);
    write_trace(b, o.trace);
    return ck.report();
}
