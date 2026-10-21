// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The media-clock plane and the two listener paths through a source change
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
//   audio  48 kHz * FRAME_DIV_TB at the DUT's INTERNAL offset (64 by default,
//          resolving a hold to 1/64 sample), its edges moved by
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
//                   media ticks. The ring's law gives it a range of (0, 11]
//                   ticks: below 0 a tick finds the queue empty (a dup, and
//                   m gains a tick), above 11 a push finds it full (a skip,
//                   and m loses a tick). Only the settle recentre moves it
//                   otherwise, to its 11-event target: m in (5, 6] ticks;
//   full margin     time since a reused queue slot was freed, measured at
//                   each push; the least across each PDU is its early-side
//                   margin. Both margins must stay at least one tick;
//   presentation    the render presentation stage (#632) hands the TDM lane
//                   the frame its read names, K = 2 frames after the domain
//                   event it reads at; each event's sample names its ordinal,
//                   and its presentation time is its PDU's avtp_timestamp
//                   plus one talker period per event (IEEE 1722-2016 7.5).
//                   Each presentation is graded against the instant the
//                   domain event of its frame reports when it comes: the law
//                   is every event once, in order, at the frame nearest its
//                   presentation time (half a period, and the marker's two
//                   clk_i cycles of quantisation). The talker is not phased
//                   to the DUT's grid (the phase term is off here), so the
//                   tighter +/-5 % band is not this bench's.
//
// WHAT IS GRADED (#645 / #647, the ruling on #645's stage-1 STOP, and #632).
// The settle recentre is milan_datapath's own, copied by dp_glue.py: once per
// source change or aligner pull-in, after the servo has read LOCKED for 8
// windows (following) or the aligner has rested in its band (INTERNAL), to
// the loopback ring. From a switch to its settle recentre the ring may slip,
// up to the declared bound; after it the ring may not move: no loopback
// slip, the loopback ring centred. The presentation stage takes no recentre:
// it places every event by its timestamp, so after the settle it slips
// nothing and every event is on the presentation law.
//
// THE BIND CASE (#645, bench lane B17, PR #741). At INTERNAL, with the peer
// on the DUT's own clock (B17's delta was within 0.0017 ppm), each of B17's
// ten bind cycles is replayed: an unbind, then a bind whose first PDU lands
// at --bind-phase of a media tick, B17's delay after the bind, then B17's
// first burst over 20 us late, and a later burst at B17's largest later
// peak. B17's cycle 5 bounds the margin its bind primed: below 24.565 us,
// the peak of the burst that slipped it, and above 30.260 - 20.833 = 9.427
// us, since the dup moved the ring a tick off its empty edge and a 30.260 us
// burst after it slipped nothing. Graded per bind: one settle recentre,
// armed by the bind's first PDU and fired 2,048 ticks later (the INTERNAL
// rule), and no SLIP_LB change. At some
// first-PDU phases inside that window, finer than sweep-bind's 16, a bind
// takes a one-pair dup before the ring acts; dev's datapath takes it too,
// the arm does not remove it, and #743 owns it. --follow-binds then repeats
// the cycles under CRF following, where a bind must arm nothing.
//
// Usage: Vfollow_ring [--case b8|pullin|bind] [options]   (see usage())

#include "../../common/verilator_harness.hpp"
#include "../mmcm_servo/mmcm_model.h"
#include "Vfollow_ring_wrap.h"
#include "Vfollow_ring_wrap___024root.h"
#include "verilated.h"
#include "recovery_watch.hpp"

#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <map>
#include <random>
#include <string>
#include <vector>

namespace {

constexpr double kClkHz = CLK_HZ_TB;
constexpr double kHalfClk = 0.5e15 / kClkHz;
constexpr double kAudioHz = 48000.0 * FRAME_DIV_TB;
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
//! THE SETTLE LAW UNDER TEST, stated here and never read back from the DUT:
//! under following, the settle recentre fires once the servo has read LOCKED
//! for 8 of its 512 ms windows running (the #645 ruling)...
constexpr double kSettleAfterLockS = 8 * 0.512;
//! ...give or take the tick the run is counted in and the pulse's register
constexpr double kSettleSlackS = 2e-3;
//! ...and the loopback ring takes it at the stream's next PDU: within a PDU
//! interval and a tick of the pulse
constexpr double kActS = 1e-3;
//! the loopback ring decides as the stream's first PDU after the pulse
//! starts, and that PDU's own beats, through the skid, are the last a slip
//! of the old phase can land in: from the arrival to its last commit
constexpr double kPduEndS = static_cast<double>((kBeats + 3) * kBeatCyc) / kClkHz;
//! the presentation law is graded from this long after the settle recentre
constexpr double kLawAfterS = 0.05;
//! THE PRESENTATION LAW UNDER TEST (#632), stated here, not read back: the
//! stage reads frame n + 2 at domain event n (the wrapper's out-lead) ...
constexpr uint64_t kRenderLeadFrames = 2;
//! ...each event at the frame nearest its presentation time: half a period,
//! and two clk_i cycles for the frame marker's crossing in this bench
constexpr double kNearestNs = 0.5e9 / 48000.0 + 2.0e9 / kClkHz;
//! a PDU's header reaches the stage this many clk_i cycles before its first
//! payload beat (the wrapper's FR_PAY_LEAD_C, the depacketizer's lead)
constexpr int kHdrLeadCyc = 16;
//! a PDU is graded once its last event's frame has come: its presentation
//! time, and a millisecond
constexpr double kPresentedAfterS = kPresNs * 1e-9 + 1e-3;
//! THE DECLARED TRANSIENT: frames the loopback ring may slip from a switch
//! from INTERNAL to its settle recentre, at the bench's 5.92 ppm offset
//! (MEDIA_CLOCK_FOLLOWING.md "The declared transient", measured across the
//! sweeps): up to 2 from the 1.4-tick walk, and one more where the rare
//! lateness tail meets the ring near its empty edge during the walk
constexpr int kPreSettleSlips = 3;
//! the loopback ring centred: the target leaves five events of the previous
//! PDU queued when a PDU's first event lands, so that event pops 5 to 6
//! ticks after it lands; a PDU less late than the one the recentre read
//! pops later, by up to the run's uniform lateness. The recentre decides at
//! the PDU's first beat and the margin is measured from its first event's
//! landing, a few axis cycles later, so a PDU that lands on a pop is read
//! up to those cycles short of a whole tick
constexpr double kLandTicks = 3.0 * 48000.0 / kClkHz;
constexpr double kCentredLo = 5.0 - kLandTicks;
constexpr double kCentredHi = 6.0;
constexpr int kLoopDepth = 16;                    //! depth ruled on #645 stage 2c
constexpr double kTickUs = 1e6 / 48000.0;
//! a stream-to-stream switch keeps the trim (W2), so it moves the ring's
//! phase by about 0.02 tick; W1 (through IDLE) moves it by tenths
constexpr double kW2DriftTicks = 0.1;

//! BENCH LANE B17, per bind cycle (PR #741's packet,
//! review-evidence/645-b17-r1/author/summary/cNN.json): the peer's first PDU
//! after the bind's CONNECT_RX command; the first PDU burst over 20 us late,
//! its time from that first PDU and its peak; and the largest later burst,
//! none of which slipped the ring again.
struct B17Cycle {
    int cycle;
    double first_pdu_ms;
    double burst_s;
    double burst_us;
    double later_us;
};
constexpr std::array<B17Cycle, 10> kB17 = {{
    {1, 163.485, 2.6534, 28.833, 28.691},
    {2, 93.536, 1.4650, 25.009, 28.365},
    {3, 156.762, 1.6719, 26.326, 28.713},
    {4, 52.750, 3.1446, 29.309, 30.071},
    {5, 7.854, 0.0938, 24.565, 30.260},
    {6, 131.486, 3.4974, 25.840, 28.475},
    {7, 54.945, 1.3014, 24.968, 29.140},
    {8, 28.539, 1.3102, 25.581, 27.575},
    {9, 161.240, 1.1185, 25.128, 29.528},
    {10, 101.128, 5.3246, 26.869, 27.813},
}};
//! a burst's consecutive PDUs each arrive this much less late: the mean
//! least-squares slope of B17's ten first bursts (1.468 to 1.664)
constexpr double kB17DecayUs = 1.538;
//! the margin B17's cycle 5 primed lies between these: its first burst
//! slipped the ring at a 24.565 us peak; the dup moved the ring one tick off
//! its empty edge, and its 30.260 us later burst then slipped nothing, so the
//! margin was above 30.260 - 20.833 = 9.427 us. (B17's reader lists only PDUs
//! over 10 us late; that none came before a first burst bounds nothing.)
constexpr double kB17MarginLoUs = kB17[4].later_us - kTickUs;
constexpr double kB17MarginHiUs = kB17[4].burst_us;
//! the INTERNAL rule: the aligner rested in its band for 2,048 media ticks
constexpr double kInternalSettleTicks = 2048.0;

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
    double after_s = 1.0;                         //! pullin: the run after the hold
    double second_after_action_s = -1.0;         //! two-pull case, from the first action
    double second_hold_us = 52.0;
    bool second_inside_recovery = false;         //! declared residual, otherwise require the law
    //! a planted control: one harness flush pulse into the presentation
    //! stage, this long after the hold (pullin) or after LOCKED (b8); < 0 = none
    double inject_s = -1.0;
    //! bind: the B17 cycles replayed (1..10), the first PDU's arrival in a
    //! media tick, the unbound dwell, the later burst after the first, the
    //! hold after it, and the cycles repeated under CRF following
    std::vector<int> b17_cycles{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    double bind_phase = 0.25;
    double unbound_s = 0.2;
    double later_after_s = 0.5;
    double bind_hold_s = 0.3;
    int follow_binds = 0;
    //! a phase sweep crosses phases B17's window excludes: report those, and
    //! their slips before the ring acts, not fail them
    bool any_phase = false;
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
        "                            serial-clock hold, the presentation before and after\n"
        "Vfollow_ring --case bind    INTERNAL, a talker on the DUT's own clock, bench lane\n"
        "                            B17's bind cycles (--b17-cycles 1,5,...), each graded\n"
        "  --bind-phase F (0..1 of a media tick) --unbound-s S --later-after-s S\n"
        "  --bind-hold-s S --follow-binds K (the first K cycles again under CRF)\n"
        "  --any-phase (a phase outside B17's primed window, and its slips before the ring\n"
        "              acts, are reported, not failed)\n"
        "  --peer-ppm P --dut-ppm D --latency-us L --jitter-us J --tail-us T --tail-p P\n"
        "  --seed N --start-s S\n"
        "  --dwell-s S --set-phase F (0..1 of one INTERNAL beat) --hold-s S\n"
        "  --switch-hold-s S --hold-us U --after-s S\n"
        "  --second-after-action-s S --second-hold-us U --second-inside-recovery\n"
        "  --inject-flush-s S (a planted control)\n"
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
        else if (a == "--after-s" && has) num(o.after_s);
        else if (a == "--second-after-action-s" && has) num(o.second_after_action_s);
        else if (a == "--second-hold-us" && has) num(o.second_hold_us);
        else if (a == "--second-inside-recovery") o.second_inside_recovery = true;
        else if (a == "--inject-flush-s" && has) num(o.inject_s);
        else if (a == "--b17-cycles" && has) {
            o.b17_cycles.clear();
            for (const char* p = argv[++i]; *p;) {
                char* end = nullptr;
                const long c = std::strtol(p, &end, 10);
                if (end == p || c < 1 || c > static_cast<long>(kB17.size())) return false;
                o.b17_cycles.push_back(static_cast<int>(c));
                p = (*end == ',') ? end + 1 : end;
                if (*end != ',' && *end != '\0') return false;
            }
        }
        else if (a == "--bind-phase" && has) num(o.bind_phase);
        else if (a == "--unbound-s" && has) num(o.unbound_s);
        else if (a == "--later-after-s" && has) num(o.later_after_s);
        else if (a == "--bind-hold-s" && has) num(o.bind_hold_s);
        else if (a == "--follow-binds" && has)
            o.follow_binds = static_cast<int>(std::strtol(argv[++i], nullptr, 10));
        else if (a == "--any-phase") o.any_phase = true;
        else if (a == "--trace" && has) o.trace = argv[++i];
        else if (a == "--servo-trace" && has) o.servo_trace = argv[++i];
        else if (a == "--grid-trace" && has) o.grid_trace = argv[++i];
        else if (a.rfind("+verilator", 0) == 0) continue;
        else return false;
    }
    return o.scenario == "b8" || o.scenario == "pullin" ||
           (o.scenario == "bind" && !o.b17_cycles.empty() && o.bind_phase >= 0.0 && o.bind_phase < 1.0 &&
            o.follow_binds >= 0 && o.follow_binds <= static_cast<int>(o.b17_cycles.size()));
}

//! One PDU of the followed stream, from its arrival to its ring reading and
//! its six presentations.
struct PduRec {
    uint64_t n = 0;
    double arrive_s = 0.0;
    double margin_ticks = NAN;                    //! the loopback ring's m
    double full_margin_ticks = NAN;               //! earliest safe push clearance
    double pt0_ns = 0.0;                          //! its avtp_timestamp, on the wheel
    double ev_space_ns = 0.0;                     //! one talker period per event
    int shown = 0;                                //! events handed to the TDM lane
    int resolved = 0;                             //! ...whose frame's instant came
    int next_event = 0;                           //! the event expected next
    bool disorder = false;                        //! an event out of its order
    double err_max_ns = 0.0;                      //! the largest |frame - presentation time|
};

class Bench {
 public:
    Bench(Vfollow_ring_wrap* d, const Options& o) : dut(d), opt(o), rng_(o.seed) {
        slot_freed_fs_.fill(NAN);
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
        aaf_on_ = true;
        aaf_base_ns_ = t0_ns_;
        aaf_base_n_ = 0;
        aaf_n_ = 0;
        crf_n_ = 0;
        next_arrival_fs_ = arrival_fs(0);
        next_crf_fs_ = (t0_ns_ + opt.latency_us * 1e3) * 1e6;
    }

    //! bind: the unbind, between two PDUs: the AAF talker's PDUs stop
    //! reaching the listener and the stream table's bind fall flushes its
    //! LOOP queues and the render stage (the CRF talker carries on)
    void unbind() {
        while (beat_ >= 0) run_for(1e-6);
        aaf_on_ = false;
        fall_req_ = true;
        run_for(1e-6);
    }

    //! bind: the bind's rise now, and its first PDU's media instant such
    //! that it arrives `phase` of a media tick after the first tick at least
    //! `delay_s` from now; its later PDUs follow at the peer's spacing
    void bind(double delay_s, double phase) {
        rise_req_ = true;
        run_for(delay_s - kTickFs * 1e-15);
        const double tick_fs = kTickFs / (1.0 + opt.dut_ppm * 1e-6);
        const uint64_t ticks0 = media_ticks_;
        while (media_ticks_ == ticks0) run_for(1e-7);
        const double first_fs = last_tick_fs_ + phase * tick_fs;
        aaf_base_n_ = aaf_n_;
        aaf_base_ns_ = first_fs * 1e-6 - opt.latency_us * 1e3;
        push_count_ = aaf_n_ * 6;
        bursts_.clear();
        aaf_on_ = true;
        next_arrival_fs_ = arrival_fs(aaf_n_);
        if (next_arrival_fs_ <= t_fs_) next_arrival_fs_ = t_fs_ + 1.0;
    }

    //! bind: a burst of late PDUs from the first one due at `at_s`: `peak_us`
    //! late, each next one `decay_us` less (B17's shape)
    void add_burst(double at_s, double peak_us, double decay_us) {
        bursts_.push_back(Burst{at_s * 1e9, peak_us * 1e3, decay_us * 1e3, 0, false});
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

    //! a planted control: one flush pulse into the presentation stage
    void inject_flush() {
        dut->tb_flush_p_i = 1;
        run_until(t_fs_ + 2.0 * kHalfClk + 1.0);
        dut->tb_flush_p_i = 0;
    }

    //! the serial-clock hold, from now
    void frame_hold(double us) {
        dut->frame_hold_i = 1;
        run_for(us * 1e-6);
        dut->frame_hold_i = 0;
    }

    //! One sample on every media tick, retaining the signed error, not an
    //! absolute peak or a millisecond subsample. Window selection is done by
    //! the stimulus and the declared settle instant, never by the error.
    struct GridSample { double time_s; int error_cyc; bool pending; };
    std::vector<GridSample> grid_samples;
    RecoveryWatch recovery;

    // what the run saw
    double first_locked_s = -1.0;
    std::vector<double> dup_times;                //! one per frame repeated (pair 0)
    std::vector<double> skip_times;               //! one per frame dropped (pair 0)
    std::vector<double> settle_times;             //! milan_datapath's settle recentre pulses
    std::vector<double> render_slip_times;        //! the presentation stage's slips
    uint64_t render_unknown = 0;                  //! presentations naming no PDU sent
    uint32_t render_refused() const { return dut->render_refused_o; }

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
    bool aaf_on_ = false;                         //! the AAF talker bound (bind case)
    double t0_ns_ = 0.0;
    double aaf_base_ns_ = 0.0;                    //! the media instant of PDU aaf_base_n_
    uint64_t aaf_base_n_ = 0;
    uint64_t aaf_n_ = 0;
    uint64_t crf_n_ = 0;
    struct Burst {
        double at_ns;
        double peak_ns;
        double decay_ns;
        uint64_t n0;
        bool started;
    };
    std::vector<Burst> bursts_;
    bool rise_req_ = false;                       //! a bind rise on the next edge
    bool fall_req_ = false;                       //! a bind fall on the next edge
    uint64_t media_ticks_ = 0;
    double last_tick_fs_ = 0.0;
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
    std::array<double, kLoopDepth> slot_freed_fs_; //! last read of each slot
    uint8_t q_wr_q_ = 0;
    uint8_t q_rd_q_ = 0;
    uint64_t push_count_ = 0;
    uint16_t dup_q_ = 0;
    uint16_t skip_q_ = 0;

    // the presentation stage
    uint64_t hdr_for_ = ~uint64_t{0};             //! the PDU whose header went out
    uint64_t dom_n_ = 0;                          //! domain events seen
    uint32_t rq_first_ = 0;                       //! lane 0 of the read's first beat
    bool rq_valid_q_ = false;
    uint64_t last_ord_ = 0;                       //! the last event ordinal presented
    uint16_t slips_q_ = 0;
    //! presentations waiting for their frame's instant: (frame, pdu, event)
    struct Pend {
        uint64_t frame;
        uint64_t pdu;
        int event;
    };
    std::deque<Pend> pend_;

    // the servo windows
    uint8_t pp_seq_q_ = 0;
    bool locked_seen_ = false;

    double tx_ns(uint64_t n) const {
        return aaf_base_ns_ + static_cast<double>(n - aaf_base_n_) * aaf_space_ns_;
    }

    double arrival_fs(uint64_t n) {
        const double tx = tx_ns(n);
        double lat = opt.latency_us * 1e3;
        for (auto& b : bursts_) {
            if (!b.started && tx + opt.latency_us * 1e3 >= b.at_ns) {
                b.started = true;
                b.n0 = n;
            }
            if (b.started) lat += std::max(0.0, b.peak_ns - static_cast<double>(n - b.n0) * b.decay_ns);
        }
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
    //! a PDU's avtp_timestamp: the talker's media instant plus the
    //! presentation offset, on the wheel's ns
    uint32_t stamp(uint64_t n) const {
        return static_cast<uint32_t>(static_cast<uint64_t>(std::floor(tx_ns(n) + kPresNs)));
    }

    void before_rise() {
        dut->ptp_now_i = static_cast<uint64_t>(t_fs_ / 1e6);
        dut->hdr_p_i = 0;
        dut->aaf_match_p_i = 0;
        dut->crf_frame_p_i = 0;
        dut->pcm_tvalid_i = 0;
        dut->pcm_tlast_i = 0;
        dut->bind_rise_i = rise_req_;
        dut->bind_fall_i = fall_req_;
        rise_req_ = false;
        fall_req_ = false;
        if (!talking_) return;
        //! the header, kHdrLeadCyc cycles ahead of the PDU's arrival: the
        //! depacketizer's read side parses it before the payload leaves
        const double lead_fs = 2.0 * kHalfClk * kHdrLeadCyc;
        if (aaf_on_ && hdr_for_ != aaf_n_ && t_fs_ + lead_fs >= next_arrival_fs_) {
            dut->hdr_p_i = 1;
            dut->hdr_ts_ns_i = stamp(aaf_n_);
            hdr_for_ = aaf_n_;
            if (next_arrival_fs_ < t_fs_ + lead_fs) next_arrival_fs_ = t_fs_ + lead_fs;
        } else if (aaf_on_ && beat_ < 0 && hdr_for_ == aaf_n_ && t_fs_ >= next_arrival_fs_) {
            const uint64_t n = aaf_n_++;
            dut->aaf_match_p_i = 1;
            dut->aaf_seq_i = static_cast<uint8_t>(n & 0xFF);
            dut->aaf_ts_i = stamp(n);
            dut->aaf_mr_i = 0;
            PduRec r;
            r.n = n;
            r.arrive_s = t_fs_ * 1e-15;
            //! the timestamp on the wheel's 64-bit ns: the wire carries its
            //! low 32 bits, the domain's instants are graded whole
            r.pt0_ns = std::floor(tx_ns(n) + kPresNs);
            r.ev_space_ns = aaf_space_ns_ / 6.0;
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
        auto* r = dut->rootp;
        if (r->follow_ring_wrap__DOT__media_tick_p) {
            ++media_ticks_;
            last_tick_fs_ = t_fs_;
        }
        if (r->follow_ring_wrap__DOT__media_tick_p && r->follow_ring_wrap__DOT__mga_engaged_w)
            grid_samples.push_back({now_s(), static_cast<int16_t>(r->follow_ring_wrap__DOT__mga_err_w),
                                    bool(r->follow_ring_wrap__DOT__settle_pend_r)});
        if (dut->rootp->follow_ring_wrap__DOT__settle_recentre_p_r) settle_times.push_back(now_s());
        recovery.sample(now_s(), static_cast<int16_t>(r->follow_ring_wrap__DOT__mga_err_w),
                        r->follow_ring_wrap__DOT__mga_engaged_w, r->follow_ring_wrap__DOT__media_tick_p,
                        r->follow_ring_wrap__DOT__settle_pend_r, r->follow_ring_wrap__DOT__settle_recover_r);
    }

    //! every millisecond: the aligner's error and trim, the #645 settle's
    //! pending flag and run (the recentre window), and the render slips
    double next_grid_fs_ = 0.0;
    void watch_grid() {
        if (!grid_trace || t_fs_ < next_grid_fs_) return;
        next_grid_fs_ = t_fs_ + 1e12;
        auto* r = dut->rootp;
        std::fprintf(grid_trace, "%.6f,%d,%d,%d,%d,%d,%d,%d\n", now_s(),
                     static_cast<int>(r->follow_ring_wrap__DOT__mga_engaged_w),
                     static_cast<int>(static_cast<int16_t>(r->follow_ring_wrap__DOT__mga_err_w)),
                     static_cast<int>(static_cast<int16_t>(r->follow_ring_wrap__DOT__mnco_servo_trim_w)),
                     static_cast<int>(r->follow_ring_wrap__DOT__settle_pend_r),
                     static_cast<int>(r->follow_ring_wrap__DOT__settle_run_ticks_r),
                     static_cast<int>(r->follow_ring_wrap__DOT__settle_recover_r),
                     static_cast<int>(dut->render_slips_o));
    }

    //! The loopback ring's pair 0, from its own pointers: every write is one
    //! event landing; a read is one pop, one drop-oldest at a full push, or
    //! (the settle recentre) a drop and a pop in one cycle, the read pointer
    //! moving by two.
    void watch_ring() {
        auto* r = dut->rootp;
        const uint8_t wr = r->follow_ring_wrap__DOT__chan_map_capture__DOT__q_wr_r[0];
        const uint8_t rd = r->follow_ring_wrap__DOT__chan_map_capture__DOT__q_rd_r[0];
        const uint16_t sk = dut->lb_skip_o;
        const uint16_t dp = dut->lb_dup_o;
        //! a bind fall on this edge emptied the queue and zeroed its pointers:
        //! what was queued is gone, not read
        if (dut->bind_fall_i) {
            q_.clear();
            slot_freed_fs_.fill(NAN);
            q_wr_q_ = wr;
            q_rd_q_ = rd;
        }
        //! Observe pop before push, as the queue composes a same-cycle pair.
        //! Every freed slot carries its actual read time, including a drop.
        const int reads = (rd - q_rd_q_) & (kLoopDepth - 1);
        for (int left = reads; left > 0 && !q_.empty(); --left) {
            slot_freed_fs_[(q_rd_q_ + reads - left) & (kLoopDepth - 1)] = t_fs_;
            const Ev e = q_.front();
            q_.pop_front();
            //! the last event read is the one popped; any before it dropped
            if (left == 1 && sk == skip_q_ && e.event == 0 && e.pdu < pdus.size()) {
                pdus[e.pdu].margin_ticks = (t_fs_ - e.push_fs) / kTickFs;
            }
        }
        if (wr != q_wr_q_) {
            const uint64_t k = push_count_++;
            q_.push_back(Ev{t_fs_, k / 6, static_cast<int>(k % 6)});
            const double freed = slot_freed_fs_[q_wr_q_];
            if (!std::isnan(freed) && k / 6 < pdus.size()) {
                double& margin = pdus[k / 6].full_margin_ticks;
                const double age = (t_fs_ - freed) / kTickFs;
                margin = std::isnan(margin) ? age : std::min(margin, age);
            }
        }
        //! two dups or skips per slipped frame (the stream's two pairs, a
        //! cycle or more apart): the frame is counted at the first
        for (uint32_t i = dup_q_; i < dp; ++i) {
            if (i % 2 == 0) dup_times.push_back(now_s());
        }
        for (uint32_t i = skip_q_; i < sk; ++i) {
            if (i % 2 == 0) skip_times.push_back(now_s());
        }
        q_wr_q_ = wr;
        q_rd_q_ = rd;
        skip_q_ = sk;
        dup_q_ = dp;
    }

    //! The presentation stage: every domain event's instant resolves the
    //! presentations the read K events earlier made of that frame; every
    //! read with a sample names, on lane 0, the ordinal of the event handed
    //! to the TDM lane (its sample is {ordinal[19:0], channel}).
    void watch_render() {
        if (dut->dom_ev_p_o) {
            ++dom_n_;
            const double e_ns = static_cast<double>(static_cast<int64_t>(dut->dom_ns_o));
            while (!pend_.empty() && pend_.front().frame <= dom_n_) {
                const Pend q = pend_.front();
                pend_.pop_front();
                if (q.frame != dom_n_ || q.pdu >= pdus.size()) continue;
                PduRec& r = pdus[q.pdu];
                const double pt = r.pt0_ns + q.event * r.ev_space_ns;
                r.err_max_ns = std::max(r.err_max_ns, std::fabs(pt - e_ns));
                ++r.resolved;
            }
        }
        const bool v = dut->render_tvalid_o;
        if (v && !rq_valid_q_) {
            const uint64_t d = dut->render_tdata_o;
            rq_first_ = static_cast<uint32_t>(((d & 0xFF) << 16) | (((d >> 8) & 0xFF) << 8) |
                                              ((d >> 16) & 0xFF));
        }
        rq_valid_q_ = v;
        if (dut->render_pop_p_o) presented(rq_first_ >> 4);
        const uint16_t sl = dut->render_slips_o;
        for (uint32_t i = slips_q_; i < sl; ++i) render_slip_times.push_back(now_s());
        slips_q_ = sl;
    }

    //! one event handed to the TDM lane, by its 20-bit ordinal, unwrapped
    //! against the last one
    void presented(uint32_t ord20) {
        uint64_t ord = (last_ord_ & ~uint64_t{0xFFFFF}) | ord20;
        if (ord + 0x80000 < last_ord_) ord += 0x100000;
        else if (ord > last_ord_ + 0x80000 && ord >= 0x100000) ord -= 0x100000;
        last_ord_ = ord;
        const uint64_t n = ord / 6;
        const int k = static_cast<int>(ord % 6);
        if (n >= pdus.size()) {
            ++render_unknown;
            return;
        }
        PduRec& r = pdus[n];
        ++r.shown;
        if (k != r.next_event) r.disorder = true;
        r.next_event = k + 1;
        pend_.push_back(Pend{dom_n_ + kRenderLeadFrames, n, k});
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
    //! Absolute event times come from the slip counters and the settle pulse,
    //! independently of PDU margin changes. A declared action is not a slip.
    for (const double t : b.dup_times) std::printf("RING-EVENT: dup %.9f\n", t);
    for (const double t : b.skip_times) std::printf("RING-EVENT: skip %.9f\n", t);
    for (const double t : b.settle_times) std::printf("RING-EVENT: recentre %.9f\n", t);
    std::printf("RING-EVENTS: complete through %.9f s\n", b.now_s());
    FILE* f = std::fopen(path.c_str(), "w");
    if (!f) return;
    std::fprintf(f, "pdu,arrive_s,ring_margin_ticks,full_margin_ticks,render_shown,render_err_max_ns\n");
    for (const auto& p : b.pdus) {
        std::fprintf(f, "%llu,%.7f,%.4f,%.4f,%d,%.1f\n", static_cast<unsigned long long>(p.n),
                     p.arrive_s, p.margin_ticks, p.full_margin_ticks, p.shown, p.err_max_ns);
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

//! the first instant of `v` at or after `a`, or -1
double first_at_or_after(const std::vector<double>& v, double a) {
    for (const double t : v) {
        if (t >= a) return t;
    }
    return -1.0;
}

//! The presentation law over the PDUs arriving in [a, e) whose last frame
//! has come: every event handed to the TDM lane once, in order, at the frame
//! nearest its presentation time; and the stage's slips in [a, e).
struct Law {
    int n = 0;
    int off = 0;                                  //! PDUs not on the law
    int slips = 0;
    double err_max_ns = 0.0;
    bool on_law() const { return n > 0 && off == 0 && slips == 0; }
    const char* verdict() const { return on_law() ? "on the law" : "OFF THE LAW"; }
};

Law render_law(const Bench& b, double a, double e) {
    Law w;
    const double ripe = b.now_s() - kPresentedAfterS;
    for (const auto& p : b.pdus) {
        if (p.arrive_s < a || p.arrive_s >= e || p.arrive_s >= ripe) continue;
        ++w.n;
        const bool ok = p.shown == 6 && p.resolved == 6 && !p.disorder && p.err_max_ns <= kNearestNs;
        w.off += ok ? 0 : 1;
        w.err_max_ns = std::max(w.err_max_ns, p.shown ? p.err_max_ns : 1e9);
    }
    w.slips = count_in(b.render_slip_times, a, e);
    return w;
}

//! Signed steady-error distribution at media-tick resolution. Every selected
//! sample is counted, including outliers; no error-based exclusion exists.
void print_errors(const Bench& b, const char* name, double a, double e,
                  milan::tb::Checker* steady = nullptr) {
    std::map<int, uint64_t> hist;
    uint64_t total = 0;
    uint64_t pending = 0;
    for (const auto& sample : b.grid_samples) {
        if (sample.time_s >= a && sample.time_s < e) {
            ++hist[sample.error_cyc];
            ++total;
            pending += sample.pending;
        }
    }
    std::printf("ERROR-DISTRIBUTION: %s window %.9f %.9f samples %llu axis_hz %.0f histogram",
                name, a, e, static_cast<unsigned long long>(total), kClkHz);
    for (const auto& [error, count] : hist)
        std::printf(" %d:%llu", error, static_cast<unsigned long long>(count));
    std::printf("\n");
    if (steady) {
        char label[200];
        std::snprintf(label, sizeof label, "[STEADY] %s has error samples", name);
        steady->that(label, total > 0);
        std::snprintf(label, sizeof label, "[STEADY] %s has no false settle pulse", name);
        steady->dec(label, count_in(b.settle_times, a, e), 0);
        std::snprintf(label, sizeof label, "[STEADY] %s has no excursion arm", name);
        steady->dec(label, count_in(b.recovery.arms, a, e), 0);
        std::snprintf(label, sizeof label, "[STEADY] %s has no pending settle", name);
        steady->dec(label, pending, 0);
    }
}

void print_window(const Bench& b, const char* name, double a, double e) {
    const Range m = margin_range(b, a, e);
    const Law w = render_law(b, a, e);
    std::printf("  info: %-26s [%8.3f, %8.3f) s: ring slips %d+%d, margin %+.3f..%+.3f ticks; "
                "presentation n %d (off-law %d), the largest |frame - presentation time| %.1f ns "
                "(nearest frame: %.1f ns), render slips %d\n",
                name, a, e, count_in(b.dup_times, a, e), count_in(b.skip_times, a, e), m.lo, m.hi, w.n,
                w.off, w.err_max_ns, kNearestNs, w.slips);
}

//! What one transient left, from its start to its settle recentre and after.
struct Settle {
    double t_start = 0.0;                         //! the switch or the hold
    double t_lock = -1.0;                         //! the servo's LOCKED (following)
    double t_settle = -1.0;                       //! the settle recentre's pulse
    double t_end = 0.0;
    int pulses = 0;                               //! settle pulses in [start, end)
    //! the end of the stream's first PDU after the pulse: the loopback ring
    //! has decided, so a slip from here on is the recentre's own
    double t_act = -1.0;
    int pre_slips = 0;                            //! frames slipped before the ring acts
    int post_slips = 0;                           //! ...and after it
    Range margin_after;
    Range full_margin_after;
    Law law_after;
    //! the PDUs queued across the pulse: where a recentre of the presentation
    //! stage, which it takes none of, would show
    Law law_across;
    //! the instant the rings have acted: the end of the PDU the loopback
    //! ring decided on, or (none fired) the one the law expected under
    //! following, so a missing recentre is graded on the window it should
    //! have cleaned up
    double acted() const {
        if (t_act > 0.0) return t_act;
        const double t = t_lock > 0.0 ? t_lock + kSettleAfterLockS : t_start;
        return t + kActS;
    }
};

Settle grade_settle(const Bench& b, double t_start, double t_lock, double t_end) {
    Settle s;
    s.t_start = t_start;
    s.t_lock = t_lock;
    s.t_end = t_end;
    s.pulses = count_in(b.settle_times, t_start, t_end);
    s.t_settle = first_at_or_after(b.settle_times, t_start);
    if (s.t_settle >= t_end) s.t_settle = -1.0;
    if (s.t_settle > 0.0) {
        for (const auto& p : b.pdus) {
            if (p.arrive_s > s.t_settle) {
                s.t_act = p.arrive_s + kPduEndS;
                break;
            }
        }
        if (s.t_act < 0.0) s.t_act = s.t_settle + kActS;
    }
    const double act = s.acted();
    s.pre_slips = count_in(b.dup_times, t_start, act) + count_in(b.skip_times, t_start, act);
    s.post_slips = count_in(b.dup_times, act, t_end) + count_in(b.skip_times, act, t_end);
    s.margin_after = margin_range(b, act, t_end);
    for (const auto& p : b.pdus) {
        if (p.arrive_s >= act && p.arrive_s < t_end && !std::isnan(p.full_margin_ticks))
            s.full_margin_after.take(p.full_margin_ticks);
    }
    //! with no pulse and no LOCKED to expect one from (a pull-in at
    //! INTERNAL), the law is graded on the run's last half second, long
    //! after the pull
    const bool timed = s.t_settle > 0.0 || s.t_lock > 0.0;
    s.law_after = render_law(b, timed ? act + kLawAfterS : t_end - 0.5, t_end);
    if (s.t_settle > 0.0) s.law_across = render_law(b, s.t_settle - kPresentedAfterS, act + kLawAfterS);
    return s;
}

void print_settle(const char* tag, const Settle& s) {
    std::printf("  info: %s: settle recentre %s (%d pulse(s)); "
                "slips before it %d, after it %d; after it the loopback margin %+.3f..%+.3f ticks, "
                "presentation n %d, largest error %.1f ns, render slips %d, %s\n",
                tag, s.t_settle > 0.0 ? "fired" : "DID NOT FIRE", s.pulses, s.pre_slips,
                s.post_slips, s.margin_after.lo, s.margin_after.hi, s.law_after.n, s.law_after.err_max_ns,
                s.law_after.slips, s.law_after.verdict());
    std::printf("MARGINS: %s empty %.6f full %.6f ticks\n", tag,
                s.margin_after.lo, s.full_margin_after.lo);
    if (s.t_settle > 0.0) {
        std::printf("  info: %s: settle recentre %.4f s after the start", tag, s.t_settle - s.t_start);
        if (s.t_lock > 0.0) std::printf(", %.4f s after LOCKED", s.t_settle - s.t_lock);
        std::printf("\n");
    }
}

//! The checks every settle recentre owes. `tag` names the transient; under
//! following it must come 8 servo windows after LOCKED.
void check_settle(milan::tb::Checker& ck, const char* tag, const Settle& s, const Options& o, bool following) {
    char w[200];
    std::snprintf(w, sizeof w, "%s exactly one settle recentre from the transient to the hold's end", tag);
    ck.dec(w, static_cast<uint64_t>(s.pulses), 1);
    if (following) {
        std::snprintf(w, sizeof w, "%s the settle recentre came 8 servo windows after LOCKED", tag);
        ck.that(w, s.t_settle > 0.0 && s.t_lock > 0.0 &&
                       std::fabs(s.t_settle - s.t_lock - kSettleAfterLockS) <= kSettleSlackS);
    }
    std::snprintf(w, sizeof w, "%s no loopback slip after the settle recentre", tag);
    ck.dec(w, static_cast<uint64_t>(s.post_slips), 0);
    std::snprintf(w, sizeof w, "%s the loopback ring is centred after the settle recentre (margin in (5, 6] ticks)",
                  tag);
    ck.that(w, s.margin_after.hi > kCentredLo &&
                   s.margin_after.hi <= kCentredHi + o.jitter_us / kTickUs + 0.005);
    std::snprintf(w, sizeof w, "%s empty-side margin at least one tick", tag);
    ck.that(w, s.margin_after.lo >= 1.0 && s.margin_after.lo < 1e9);
    std::snprintf(w, sizeof w, "%s full-side margin at least one tick", tag);
    ck.that(w, s.full_margin_after.lo >= 1.0 && s.full_margin_after.lo < 1e9);
    //! the presentation stage takes no recentre (#632): each PDU's timestamp
    //! places it, so arrival lateness inside the supported range moves no
    //! presentation and the law is graded on every run
    std::snprintf(w, sizeof w, "%s the presentation stage is on its law after the settle recentre", tag);
    ck.that(w, s.law_after.on_law());
    std::snprintf(w, sizeof w, "%s the presentation stage presented every PDU across the settle recentre", tag);
    ck.that(w, s.t_settle < 0.0 || s.law_across.on_law());
}

//! b8: the set at a chosen place in one INTERNAL beat: the next slip, then
//! that fraction of a beat later, so the ring's margin at the set runs from
//! about one tick (phase 0) down to its edge (phase 1). A peer on the DUT's
//! own clock (the control) has no beat: the set is immediate.
void wait_for_the_set(Bench& b, const Options& o, double beat_s) {
    if (std::fabs(o.dut_ppm - o.peer_ppm) <= 0.05) return;
    const auto& slips = o.dut_ppm > o.peer_ppm ? b.dup_times : b.skip_times;
    const size_t slips0 = slips.size();
    const double guard = (b.now_s() + 2.0 * beat_s) * 1e15;
    while (slips.size() == slips0 && b.now_s() * 1e15 < guard) b.run_for(1e-3);
    if (slips.size() > slips0) b.run_until((slips.back() + o.set_phase * beat_s) * 1e15);
}

//! b8: every slip and recentre from the set on, against LOCKED
void print_events(const Bench& b, double t_set, double t_lock) {
    for (const double t : b.dup_times) {
        if (t >= t_set) {
            std::printf("  info: slip (dup) at %.4f s after the set, %+.4f s from LOCKED\n", t - t_set, t - t_lock);
        }
    }
    for (const double t : b.skip_times) {
        if (t >= t_set) {
            std::printf("  info: slip (skip) at %.4f s after the set, %+.4f s from LOCKED\n", t - t_set, t - t_lock);
        }
    }
    for (const double t : b.render_slip_times) {
        if (t >= t_set) {
            std::printf("  info: render slip at %.4f s after the set, %+.4f s from LOCKED\n", t - t_set,
                        t - t_lock);
        }
    }
}

//! One stream-to-stream switch, held: W2 keeps the trim, so the switch moves
//! the ring's phase by hundredths of a tick until its settle recentre, then
//! the settle law as after the set.
void run_switch(Bench& b, const Options& o, milan::tb::Checker& ck, uint16_t to, const char* tag) {
    const Range before = margin_range(b, b.now_s() - 0.5, b.now_s());
    b.first_locked_s = -1.0;
    b.select(to);
    const double t_sw = b.now_s();
    b.run_for(o.switch_hold_s);
    const double t_lock = b.first_locked_s;
    const Settle s = grade_settle(b, t_sw, t_lock, b.now_s());
    const double t_pre = s.t_settle > 0.0 ? s.t_settle : s.acted();
    const Range ahead = margin_range(b, t_pre - 0.5, t_pre);
    char w[200];
    std::printf("  info: %s: LOCKED %.3f s after; ring slips %d; margin %+.3f before the switch, %+.3f before "
                "its settle recentre\n",
                tag, t_lock - t_sw, s.pre_slips + s.post_slips, before.hi, ahead.hi);
    print_window(b, tag, t_sw, b.now_s());
    print_settle(tag, s);
    print_errors(b, tag, s.acted(), b.now_s(), &ck);
    std::printf("RESULT-645-SW: %s phase %.4f jitter %.1f us tail %.1f us p %.0e: LOCKED %.2f s, slips %d, "
                "drift %+.3f ticks, settle %+.3f s after LOCKED, margin after %+.3f..%+.3f, presentation %s\n",
                tag, o.set_phase, o.jitter_us, o.tail_us, o.tail_p, t_lock - t_sw, s.pre_slips + s.post_slips,
                ahead.hi - before.hi, s.t_settle > 0.0 ? s.t_settle - t_lock : -1.0, s.margin_after.lo,
                s.margin_after.hi, s.law_after.verdict());
    std::snprintf(w, sizeof w, "%s re-locks", tag);
    ck.that(w, t_lock > 0.0);
    std::snprintf(w, sizeof w, "%s no ring slip across the switch", tag);
    ck.dec(w, static_cast<uint64_t>(s.pre_slips + s.post_slips), 0);
    std::snprintf(w, sizeof w, "%s the switch moved the loopback margin less than 0.1 tick before its settle", tag);
    ck.that(w, std::fabs(ahead.hi - before.hi) < kW2DriftTicks);
    check_settle(ck, tag, s, o, true);
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
        b.inject_flush();
    }
    b.run_until((t_set + o.hold_s) * 1e15);
    const double t_lock = b.first_locked_s;
    const double t_end = b.now_s();
    const Settle s = grade_settle(b, t_set, t_lock, t_end);
    std::printf("  info: INTERNAL-to-AAF: LOCKED %.3f s after the set; trim %+.3f ppm at the end\n",
                t_lock - t_set, b.trim_ppm());
    print_events(b, t_set, t_lock);
    print_window(b, "INTERNAL, last second", t_set - 1.0, t_set);
    print_window(b, "set to LOCKED", t_set, t_lock);
    print_window(b, "LOCKED to the settle", t_lock, s.acted());
    print_window(b, "settle to the hold's end", s.acted(), t_end);
    print_settle("[B8]", s);
    print_errors(b, "INTERNAL before switch", t_set - 0.5, t_set, &ck);
    print_errors(b, "AAF after settle", s.acted(), t_end, &ck);
    const Range at_lock = margin_range(b, t_lock, t_lock + 0.5);
    std::printf("RESULT-645: phase %.4f jitter %.1f us tail %.1f us p %.0e: slips set-to-settle %d (declared "
                "bound %d), after the settle %d, margin at LOCKED %+.3f..%+.3f, after the settle %+.3f..%+.3f "
                "ticks, LOCKED %.2f s, settle %+.3f s after LOCKED, presentation after the settle: largest "
                "error %.1f ns, render slips %d (%s)\n",
                o.set_phase, o.jitter_us, o.tail_us, o.tail_p, s.pre_slips, kPreSettleSlips, s.post_slips,
                at_lock.lo, at_lock.hi, s.margin_after.lo, s.margin_after.hi, t_lock - t_set,
                s.t_settle > 0.0 ? s.t_settle - t_lock : -1.0, s.law_after.err_max_ns, s.law_after.slips,
                s.law_after.verdict());
    ck.that("[B8] the servo read LOCKED within 15 s of the INTERNAL-to-AAF set",
            t_lock > 0.0 && t_lock - t_set <= 15.0);
    ck.that("[B8] the loopback ring slipped no more than the declared transient before the settle recentre",
            s.pre_slips <= kPreSettleSlips);
    check_settle(ck, "[B8]", s, o, true);
    if (o.switch_hold_s > 0.0) {
        run_switch(b, o, ck, kSrcCrf, "[SW] AAF to CRF:");
        run_switch(b, o, ck, kSrcAaf, "[SW] CRF to AAF:");
    }
    return 0;
}

//! Two independent pulls: the residual is restricted to a second pull that
//! starts while recovery is active. Outside it the ordinary settle law holds.
void run_second_pull(Bench& b, const Options& o, milan::tb::Checker& ck, double first_hold) {
    const double first_action = first_at_or_after(b.settle_times, first_hold);
    ck.that("[TWO-PULL] first hold produced an action", first_action > first_hold);
    if (first_action < first_hold) return;
    b.run_until((first_action + o.second_after_action_s) * 1e15);
    const double second_hold = b.now_s();
    const bool recovering = b.recovery.was_recovering;
    ck.that("[TWO-PULL] second hold starts on its declared side of recovery",
            recovering == o.second_inside_recovery);
    const Settle first = grade_settle(b, first_hold, -1.0, second_hold);
    print_settle("[FIRST-PULL]", first);
    check_settle(ck, "[FIRST-PULL]", first, o, false);
    b.frame_hold(o.second_hold_us);
    b.run_for(o.after_s);
    const Settle second = grade_settle(b, second_hold, -1.0, b.now_s());
    print_settle("[SECOND-PULL]", second);
    if (o.second_inside_recovery) {
        ck.dec("[RESIDUAL] second pull in recovery adds no action", second.pulses, 0);
        //! the residual is the loopback ring's alone: the presentation stage
        //! needs no recentre, so it is on its law after the second pull too
        ck.that("[RESIDUAL] the presentation stage is on its law after the second pull",
                second.law_after.on_law());
    } else {
        check_settle(ck, "[SECOND-PULL]", second, o, false);
    }
    b.recovery.check(ck, first_hold, b.now_s());
    std::printf("TWO-PULL: first %.9f action %.9f second %.9f inside_recovery %d "
                "second_actions %d final %s\n", first_hold, first_action, second_hold,
                recovering, second.pulses, second.law_after.verdict());
}

int run_pullin(Bench& b, const Options& o, milan::tb::Checker& ck) {
    b.start_talkers(o.start_s);
    b.run_until((o.start_s + o.dwell_s) * 1e15);
    const double t_hold = b.now_s();
    const uint32_t refused0 = b.render_refused();
    print_window(b, "before the hold, last 0.5 s", t_hold - 0.5, t_hold);
    b.frame_hold(o.hold_us);
    if (o.second_after_action_s >= 0.0) {
        while (first_at_or_after(b.settle_times, t_hold) < t_hold && b.now_s() < t_hold + o.after_s)
            b.run_for(1e-3);
        run_second_pull(b, o, ck, t_hold);
        return 0;
    }
    if (o.inject_s >= 0.0) {
        b.run_for(o.inject_s);
        b.inject_flush();
        b.run_until((t_hold + o.after_s) * 1e15);
    } else {
        b.run_for(o.after_s);
    }
    const double t_end = b.now_s();
    const Settle s = grade_settle(b, t_hold, -1.0, t_end);
    print_window(b, "the pull, first 0.2 s", t_hold, t_hold + 0.2);
    print_window(b, "after the settle", s.acted(), t_end);
    print_settle("[PULLIN]", s);
    print_errors(b, "INTERNAL before hold", t_hold - 0.5, t_hold, &ck);
    print_errors(b, "INTERNAL after hold", t_hold, t_end);
    if (s.t_settle > 0.0) print_errors(b, "INTERNAL after settle", s.acted(), t_end, &ck);
    //! the PDUs presented before the hold: the frames queued at it present
    //! the hold's length late, which is the hold's own transient
    const Law w0 = render_law(b, t_hold - 0.5, t_hold - kPresentedAfterS);
    const Law& w1 = s.law_after;
    const int hold_slips = count_in(b.render_slip_times, t_hold, s.acted() + kLawAfterS);
    const char* verdict = !w0.on_law() ? "OFF-LAW BEFORE" : !w1.on_law() ? "LEFT THE LAW" : "ON THE LAW";
    std::printf("RESULT-647: latency %.2f us hold %.1f us: largest |frame - presentation time| %.1f -> "
                "%.1f ns (nearest frame %.1f ns), render slips %d across the hold and %d after, refused %u, "
                "settle %+.3f s after the hold, loopback slips %d before the settle and %d after: %s\n",
                o.latency_us, o.hold_us, w0.err_max_ns, w1.err_max_ns, kNearestNs, hold_slips, w1.slips,
                b.render_refused() - refused0, s.t_settle > 0.0 ? s.t_settle - t_hold : -1.0,
                s.pre_slips, s.post_slips, verdict);
    ck.that("[PULLIN] the stream was on the presentation law before the hold", w0.on_law());
    ck.dec("[PULLIN] the presentation stage refused nothing across the hold",
           b.render_refused() - refused0, 0);
    if (o.hold_us == 0.0) {
        print_errors(b, "INTERNAL without a hold", t_hold, t_end, &ck);
        ck.that("[STEADY] the running stream stays on its presentation law", w1.on_law());
    } else {
        check_settle(ck, "[PULLIN]", s, o, false);
        b.recovery.check(ck, t_hold, t_end);
    }
    return 0;
}

//! What one bind cycle left, from its unbind to the next.
struct BindCycle {
    double t_bind = 0.0;
    double t_first = -1.0;                        //! the bind's first PDU's arrival
    double t_burst = -1.0;                        //! B17's first burst
    double t_end = 0.0;
    int arms = 0;                                 //! settle arms in [bind, end)
    double t_arm = -1.0;
    int pulses = 0;
    double t_settle = -1.0;
    int dups = 0;                                 //! SLIP_LB's two counters, raw
    int skips = 0;
    double t_act = -1.0;                          //! the loopback ring has acted
    //! slipped frames before the ring acts (from the bind) and after it; with
    //! no recentre, the instant the INTERNAL rule would have acted divides them
    int pre_slips = 0;
    int post_slips = 0;
    Range primed;                                 //! the margin the bind primed
    bool in_window = false;                       //! ...inside B17's
    Range after;
    Range full_after;
};

//! One bind cycle (B17's `c`): unbind, the unbound dwell, the bind with its
//! first PDU at `phase`, B17's first burst and the later one, the hold.
BindCycle run_bind_cycle(Bench& b, const Options& o, const B17Cycle& c) {
    BindCycle k;
    const unsigned dup0 = b.dut->lb_dup_o;
    const unsigned skip0 = b.dut->lb_skip_o;
    b.unbind();
    b.run_for(o.unbound_s);
    k.t_bind = b.now_s();
    const size_t first = b.pdus.size();
    b.bind(c.first_pdu_ms * 1e-3, o.bind_phase);
    while (b.pdus.size() == first) b.run_for(1e-6);
    k.t_first = b.pdus[first].arrive_s;
    k.t_burst = k.t_first + c.burst_s;
    b.add_burst(k.t_burst, c.burst_us, kB17DecayUs);
    b.add_burst(k.t_burst + o.later_after_s, c.later_us, kB17DecayUs);
    b.run_until((k.t_burst + o.later_after_s + o.bind_hold_s) * 1e15);
    k.t_end = b.now_s();
    k.arms = count_in(b.recovery.arms, k.t_bind, k.t_end);
    k.t_arm = first_at_or_after(b.recovery.arms, k.t_bind);
    k.pulses = count_in(b.settle_times, k.t_bind, k.t_end);
    k.t_settle = first_at_or_after(b.settle_times, k.t_bind);
    k.dups = static_cast<int>(b.dut->lb_dup_o - dup0);
    k.skips = static_cast<int>(b.dut->lb_skip_o - skip0);
    if (k.t_settle > 0.0 && k.t_settle < k.t_end) {
        for (const auto& p : b.pdus) {
            if (p.arrive_s > k.t_settle) {
                k.t_act = p.arrive_s + kPduEndS;
                break;
            }
        }
    }
    const double split = k.t_act > 0.0
        ? k.t_act : k.t_first + kPduEndS + (kInternalSettleTicks + 12.0) * kTickFs * 1e-15;
    k.pre_slips = count_in(b.dup_times, k.t_bind, split) + count_in(b.skip_times, k.t_bind, split);
    k.post_slips = count_in(b.dup_times, split, k.t_end) + count_in(b.skip_times, split, k.t_end);
    //! without a recentre the priming holds until the first burst; so it does
    //! when the pulse came before the first PDU, which an unprimed ring ignores
    const double primed_end = k.t_settle > k.t_first ? std::min(k.t_settle, k.t_burst) : k.t_burst;
    k.primed = margin_range(b, k.t_first, primed_end);
    if (k.t_act > 0.0) {
        k.after = margin_range(b, k.t_act, k.t_end);
        for (const auto& p : b.pdus) {
            if (p.arrive_s >= k.t_act && p.arrive_s < k.t_end && !std::isnan(p.full_margin_ticks))
                k.full_after.take(p.full_margin_ticks);
        }
    }
    k.in_window = k.primed.lo <= k.primed.hi && k.primed.lo * kTickUs > kB17MarginLoUs &&
                  k.primed.hi * kTickUs < kB17MarginHiUs;
    std::printf("RESULT-645-BIND: B17 cycle %d phase %.4f %s: first PDU %+.3f ms after the bind, primed margin "
                "%.3f..%.3f us (%s B17's window), arms %d (%+.3f ms after the first PDU), settle recentres %d "
                "(%.2f ticks after the arm), SLIP_LB %+d dups %+d skips, slipped frames "
                "%d before the ring acts and %d after, first burst %.3f us at %+.4f s, later %.3f us, "
                "margin after a recentre %+.3f..%+.3f ticks, full side %+.3f (1e9: no recentre)\n",
                c.cycle, o.bind_phase, b.dut->clk_src_idx_i != kSrcInternal ? "under CRF following" : "at INTERNAL",
                (k.t_first - k.t_bind) * 1e3, k.primed.lo * kTickUs, k.primed.hi * kTickUs,
                k.in_window ? "inside" : "OUTSIDE", k.arms, k.t_arm > 0.0 ? (k.t_arm - k.t_first) * 1e3 : -1.0,
                k.pulses, k.t_settle > 0.0 && k.t_arm > 0.0 ? (k.t_settle - k.t_arm) * 1e15 / kTickFs : -1.0,
                k.dups, k.skips, k.pre_slips, k.post_slips, c.burst_us, k.t_burst - k.t_first,
                c.later_us, k.after.lo, k.after.hi, k.full_after.lo);
    //! each slipped frame against the first burst, as B17 timed them
    for (const auto* v : {&b.dup_times, &b.skip_times}) {
        for (const double t : *v) {
            if (t >= k.t_bind && t < k.t_end) {
                std::printf("  info: B17 cycle %d: slip (%s) %+.6f s after the bind, %+.6f s from the first burst\n",
                            c.cycle, v == &b.dup_times ? "dup" : "skip", t - k.t_bind, t - k.t_burst);
            }
        }
    }
    return k;
}

int run_bind(Bench& b, const Options& o, milan::tb::Checker& ck) {
    b.start_talkers(o.start_s);
    b.run_until((o.start_s + o.dwell_s) * 1e15);
    char w[240];
    for (const int n : o.b17_cycles) {
        const B17Cycle& c = kB17[static_cast<size_t>(n - 1)];
        const BindCycle k = run_bind_cycle(b, o, c);
        char tag[80];
        std::snprintf(tag, sizeof tag, "[BIND] B17 cycle %d at INTERNAL:", c.cycle);
        if (!o.any_phase) {
            std::snprintf(w, sizeof w, "%s the bind primed the ring inside B17's window (%.3f to %.3f us)", tag,
                          kB17MarginLoUs, kB17MarginHiUs);
            ck.that(w, k.in_window);
        }
        std::snprintf(w, sizeof w, "%s its first PDU armed the settle recentre once", tag);
        ck.that(w, k.arms == 1 && k.t_arm >= k.t_first && k.t_arm <= k.t_first + kPduEndS);
        std::snprintf(w, sizeof w, "%s one settle recentre, 2,048 media ticks after the arming", tag);
        const double after_arm = (k.t_settle - k.t_arm) * 1e15 / kTickFs;
        ck.that(w, k.pulses == 1 && k.t_arm > 0.0 && after_arm > kInternalSettleTicks - 1.0 &&
                       after_arm <= kInternalSettleTicks + 1.0);
        //! the bind's stream is presented by its timestamps from its first
        //! PDU on, its bursts' lateness included (#632)
        const Law law = render_law(b, k.t_first, k.t_end);
        std::printf("  info: %s presentation n %d, off-law %d, largest error %.1f ns, render slips %d\n", tag,
                    law.n, law.off, law.err_max_ns, law.slips);
        std::snprintf(w, sizeof w, "%s the bind's stream is on the presentation law from its first PDU", tag);
        ck.that(w, law.on_law());
        //! a phase B17's window excludes primes the ring closer to its edge than
        //! B17 saw, so its slips before the ring acts are reported (--any-phase);
        //! inside the window none is allowed, and after the action none anywhere
        if (!o.any_phase || k.in_window) {
            std::snprintf(w, sizeof w, "%s no SLIP_LB change across the cycle", tag);
            ck.dec(w, static_cast<uint64_t>(k.dups + k.skips), 0);
        }
        std::snprintf(w, sizeof w, "%s no loopback slip after the ring acts", tag);
        ck.dec(w, static_cast<uint64_t>(k.post_slips), 0);
        std::snprintf(w, sizeof w, "%s the loopback ring is centred after the recentre (margin in (5, 6] ticks)",
                      tag);
        ck.that(w, k.after.hi > kCentredLo && k.after.hi <= kCentredHi + o.jitter_us / kTickUs + 0.005);
        std::snprintf(w, sizeof w, "%s empty-side margin at least one tick after the recentre", tag);
        ck.that(w, k.after.lo >= 1.0 && k.after.lo < 1e9);
        std::snprintf(w, sizeof w, "%s full-side margin at least one tick after the recentre", tag);
        ck.that(w, k.full_after.lo >= 1.0 && k.full_after.lo < 1e9);
    }
    if (o.follow_binds == 0) return 0;
    //! under following the switch rules alone arm: a bind arms nothing, and
    //! its ring keeps the phase its first PDU primed
    b.first_locked_s = -1.0;
    b.select(kSrcCrf);
    const double t_sw = b.now_s();
    while (first_at_or_after(b.settle_times, t_sw) < t_sw && b.now_s() < t_sw + 20.0) b.run_for(1e-3);
    const double t_sw_settle = first_at_or_after(b.settle_times, t_sw);
    std::printf("  info: [BIND-FOLLOW] CRF: LOCKED %.3f s, settle recentre %.3f s after the switch\n",
                b.first_locked_s - t_sw, t_sw_settle - t_sw);
    ck.that("[BIND-FOLLOW] the switch to CRF locked and settled before the binds",
            b.first_locked_s > t_sw && t_sw_settle > b.first_locked_s);
    b.run_for(0.1);
    for (int i = 0; i < o.follow_binds; ++i) {
        const B17Cycle& c = kB17[static_cast<size_t>(o.b17_cycles[static_cast<size_t>(i)] - 1)];
        const BindCycle k = run_bind_cycle(b, o, c);
        char tag[80];
        std::snprintf(tag, sizeof tag, "[BIND-FOLLOW] B17 cycle %d under CRF following:", c.cycle);
        std::snprintf(w, sizeof w, "%s the bind armed no settle recentre", tag);
        ck.dec(w, static_cast<uint64_t>(k.arms), 0);
        std::snprintf(w, sizeof w, "%s no settle recentre from the bind to the next unbind", tag);
        ck.dec(w, static_cast<uint64_t>(k.pulses), 0);
        std::printf("  info: %s SLIP_LB %+d dups %+d skips: the switch rules alone arm under following\n", tag,
                    k.dups, k.skips);
    }
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
    if ((o.scenario == "pullin" || o.scenario == "bind") && !o.peer_given) o.peer_ppm = o.dut_ppm;
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
            std::fprintf(gt, "t_s,mga_engaged,mga_err_cyc,mga_trim_16th_ppm,"
                             "settle_pend,settle_run_ticks,settle_recover,render_slips\n");
        }
    }
    b.grid_trace = gt;
    b.reset();
    if (o.scenario == "pullin") run_pullin(b, o, ck);
    else if (o.scenario == "bind") run_bind(b, o, ck);
    else run_b8(b, o, ck);
    if (st) std::fclose(st);
    if (gt) std::fclose(gt);
    write_trace(b, o.trace);
    return ck.report();
}
