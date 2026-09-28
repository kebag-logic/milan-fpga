// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_main - AAF column coherence at the TDM capture junction (#617).
//
// THE PROPERTY. IEEE 1722-2016 7.3.5 carries an AAF payload as sample events
// in chronological order, one sample per channel per event: every channel of
// one event is one instant. The talker's events are the capture crossbar's
// media-tick walks, and its TDM source is a front end that delivers one TDM
// frame as four pair strobes spread across the frame. On the #451 bench,
// 67.5% of the talker's AAF columns mixed two adjacent TDM frames between
// channel pairs: pairs 1 to 3 one frame older than pair 0, in four states
// that cycled once per 1.958 s beat. This harness asserts the opposite, on
// every column the packetizer emits: all eight channels carry one TDM frame.
//
// WHAT IS REAL. coherence_wrap.sv binds, as milan_datapath binds them on the
// shipping AX7101 1x1 TDM8 shape, the TDM MASTER front end, the media NCO,
// the #74 grid aligner, the capture crossbar and the packetizer, on a 50 MHz
// axis clock (the shipping milan clock). coherence_bench.hpp is the SoC and
// the column bench: the #451 pattern shifted into the TDM data pin off the
// master's own bclk and fsync, the clocks off one 100 MHz oscillator (the
// TRUE 391/1591 plan, fsync -10.64 ppm against the NCO's exact 48 kHz, or an
// EXAGGERATED plan a chosen ppm off 24.576 MHz), and every AAF column graded.
// sim_dp.cpp runs the same bench against the whole milan_datapath.
//
// THE CROSSING. A walk reads the frame its media tick takes: the newest one
// closed (its last pair's strobe) before the tick cycle, or one closing on
// the tick cycle itself when no frame is pending - the #74 junction
// counters' coincidence law, which the crossbar's walk follows. That is the
// one instant where the TDM frame and the packet grid meet. Under CRF the
// grid aligner keys on the same close, sees the tick one cycle late so its
// lock-target split is that crossing, and holds the close 256 cycles clear
// of it: milan_datapath's MGA_KEEPOFF_CYC_C, which the wrapper elaborates
// from the datapath's own declaration (mga_keepoff.py), so every sweep here
// grades the keep-off the datapath ships.
//
// INTERNAL AND CRF, and exactly what is swept. The clock-source verdict is
// the wrapper's sel_crf_i, the net milan_datapath resolves from the stored
// CLOCK_SOURCE. INTERNAL leaves the packet grid free-running, so the TDM
// frame drifts through it: the true plan runs one whole beat, the +/-1000 ppm
// plans three each. CRF engages the aligner on the first frame close after
// reset. Holding the TDM clock D oscillator steps (a quarter of an axis
// cycle each) moves that close D/4 cycles against the tick grid, so the
// harness first CALIBRATES, per plan, where the engagement close lands with
// the clock unheld, and then places each swept CRF engagement at a chosen
// offset from the crossing (0 = on the tick cycle, positive = after it),
// graded by its own [V] check. The CRF scenarios:
//   CRF-true-00..15   the round-1 grid, 16 held-clock offsets a sixteenth of
//                     a frame apart, 2,000 columns each;
//   CRF-50/+50-0..3   four offsets a quarter frame apart, 9,000 columns, so
//                     the aligner's acquisition transient passes its peak;
//   CRF-band-true     every offset from -32 to +32 cycles, one cycle apart,
//                     2,000 columns: the band where a lock with the close on
//                     the snapshot repeats and skips (R394-1 / R395-1 F1);
//   CRF-frame-true    every 16th offset from -512 to +512 cycles, the whole
//                     frame, 2,000 columns;
//   CRF-band-50/+50   every 4th offset from -176 to +32 (-50 ppm) and from
//                     -32 to +176 (+50 ppm), 6,000 columns: the crossing and
//                     the offsets whose acquisition transient carries the
//                     close across it inside the tail, a band 40 cycles wide
//                     or more at +/-50 ppm, so ten or more land in it;
//   CRF-fine-50       -50 ppm, every offset from -1 to +1 cycle - the
//                     crossing and the side before it, where the aligner's
//                     trim updates land on the media NCO's terminal count -
//                     at each of four quarter-cycle holds and 64 sub-step
//                     phases of the TDM clock (768 engagements, 300
//                     columns): the NCO race of R395-2 F1 lost two ticks in
//                     nine of these engagements until the NCO's terminal
//                     compare was made monotone;
//   CRF-settle-80/+80, -100/+100  the settled lock past the envelope, two
//                     engagements each: on the crossing (0 cycles at the
//                     negative rates, +8 at the positive ones: the side the
//                     pull carries a close across) and 256 cycles further to
//                     that side, where past about 86 ppm the unpulled
//                     acquisition transient crosses it; 30,000 columns, so
//                     the acquisition's net-zero crossings end in the first
//                     half and the lock is graded after them.
// Each CRF scenario's tail is its second half, and never starts inside its
// engagement window (coherence_bench's engage_columns and tail_start).
//
// THE CHECKS, per scenario:
//   [A] every AAF column after the first valid one carries its own channel
//       tags, and all eight channels one TDM frame (the acceptance check);
//   [W] every media-tick walk read one frame, and exactly the frame its tick
//       takes (THE CROSSING above): not older (no added sample of latency),
//       not newer (the frame is fixed before the walk reads it);
//   [C] column continuity: each column's frame is the previous one's plus
//       one, or a slip cluster netting one frame in the drift's direction,
//       one cluster per beat crossing (INTERNAL); under CRF slips net zero,
//       only while the engagement acquires, none in the tail; and the
//       junction counters (SLIP_TDM) count each walk's own repeat and skip,
//       walk by walk;
//   [V] vacuity: the front end captured the pattern it was sent, every
//       requested column was decoded, the INTERNAL drift swept the tick
//       through the whole frame and gave the counters slips to count, a CRF
//       lock held its phase, and each placed engagement landed where it was
//       placed.
// Each scenario prints its torn-state table in the #451 page's form (the
// frame offset of pairs 1, 2, 3 against pair 0) and, as information, the
// age of each pair's sample at the walk's tick; a swept scenario prints one
// line unless one of its checks fails.
//
// The counters and the aligner marker used to be the slot-0 strobe against
// the tick, three pair periods from the walk's crossing; nothing here keys
// on slot 0 any more. mutants.py rebuilds this harness against defective
// copies of the crossbar, of the wrapper's aligner binding, of the media
// NCO and of milan_datapath's keep-off, and requires the named checks to
// fail; the first is the ce550952 law, per-pair holds read at slot time,
// the round-1 aligner binding must reproduce the band (`--band`), a keep-off
// of 128 cycles the +/-50 ppm bands (`--band50`), and the NCO's == terminal
// compare the sub-cycle sweep's lost ticks (`--fine`).

#include "coherence_bench.hpp"
#include "Vcoherence_wrap.h"
#include "verilated.h"

#include <cstdlib>
#include <map>

namespace {

using namespace coherence;

//! phase bins for the sweep-coverage vacuity check
constexpr int kPhaseBins = 16;
//! the first frame the SoC sends: its ordinal wraps inside the long scenario
constexpr std::uint32_t kFirstFrame = 0x4A00;

//! One run from reset.
struct Scenario {
    std::string name;
    ClockPlan plan;
    bool crf = false;           //! the aligner engaged (the CRF selection)
    long start_delay_steps = 0; //! TDM clock held this long after reset
    long frames = 0;            //! columns to decode
    bool sweep = false;         //! INTERNAL: the tick must cross the frame
    bool brief = false;         //! one [i] line unless a check fails
    long placed = kUnplaced;    //! engagement close offset from the crossing
    long sub_phase = 0;         //! TDM clock sub-step phase, of kSubPhases
};

//! the aligner's u is in 1/16 ppm (KL_media_grid_align's servo units)
constexpr double kUPerPpm = 16.0;

//! What the junction taps measured (the columns are the bench's).
struct JunctionTally {
    long frames_in = 0;         //! whole frames the front end delivered
    long frame_mismatch = 0;    //! front-end pairs not matching the pattern
    long walks = 0;             //! walks graded
    long walk_torn = 0;         //! walks reading two frames
    long late = 0;              //! walks older than the frame the tick takes
    long early = 0;             //! walks newer than the frame the tick takes
    long counted = 0;           //! walks whose counter deltas were compared
    long miscounted = 0;        //! walks the junction counters miscounted
    long counter_events = 0;    //! dups plus skips the counters attributed
    std::array<long, kPhaseBins> phase_hits{};
    long lock_phase_ref = 0;    //! first tick-to-close phase of the CRF tail
    long lock_phase_min = 0;    //! its excursion either side of that, cycles
    long lock_phase_max = 0;
    bool lock_seen = false;
    long engage_offset = 0;     //! the first close, cycles after its tick
    bool engage_seen = false;
    long run_min = 0;           //! the close's movement over the whole run,
    long run_max = 0;           //! cycles, circular about engage_offset
    long run_far_col = 0;       //! the column at which it moved furthest
    //! per pair: the age of the sample a walk read, from the cycle the pair
    //! entered the crossbar to the walk's tick (information, not a verdict)
    std::array<long, kPairs> age_sum{};
    std::array<long, kPairs> age_n{};
    std::array<long, kPairs> age_min{};
    std::array<long, kPairs> age_max{};
};

//! The harness: the model, the oscillator, the SoC and the benches.
class JunctionHarness {
 public:
    explicit JunctionHarness(Vcoherence_wrap* model) : dut_(model) {}
    void run(const Scenario& sc);
    void run_sweep(const Sweep& sw);
    int report() { return check_.report(); }

 private:
    Vcoherence_wrap* dut_;
    milan::tb::Checker check_{"capture_coherence"};
    Oscillator osc_;
    SocTransmitter soc_;
    ColumnBench bench_;
    JunctionTally t_{};
    long cycle_ = 0;
    bool tail_ = false;

    long base_frame_ = -1;             //! unwrapped frame of the first close
    long latest_frame_ = -1;           //! newest frame the front end closed
    std::vector<long> close_cycle_;    //! by frame - base_frame_
    std::vector<std::array<long, kPairs>> entry_cycle_;  //! by frame - base_frame_
    std::array<std::uint32_t, kPairs> pair_ord_{};
    long pending_tick_ = -1;
    long walk_tick_ = -1;
    std::array<long, kPairs> walk_frame_{};
    long prev_walk_frame_ = -1;        //! the frame the previous walk read
    std::uint16_t walk_dup_ = 0;       //! the counters at this walk's inject
    std::uint16_t walk_skip_ = 0;
    std::uint16_t prev_dup_ = 0;       //! ...and at the previous walk's
    std::uint16_t prev_skip_ = 0;
    std::vector<long> placed_landed_;  //! the running sweep's engagements
    std::map<std::string, long> unheld_;  //! calibrations, by plan name

    void restart(const Scenario& sc);
    void program_the_map();
    void step();
    void cycle(long n);
    void observe();
    void note_tick_phase();
    void observe_front_end();
    void note_entry(long frame, int p);
    void close_frame(long frame);
    long unwrap(std::uint32_t ord16) const;
    long newest_closed_by(long cyc) const;
    long frame_the_tick_takes() const;
    void observe_walk();
    void grade_walk();
    void count_walk(long f);
    void note_ages();
    void grade(const Scenario& sc);
    void grade_sweep(const Scenario& sc, const std::string& n);
    void grade_lock(const Scenario& sc, const std::string& n);
    long window(const Scenario& sc) const;
    long calibrate(const ClockPlan& plan, long sub_phase = 0);
    void grade_window(const Sweep& sw);
    void print_ages() const;
};

void JunctionHarness::restart(const Scenario& sc) {
    t_ = JunctionTally{};
    bench_.restart();
    tail_ = false;
    base_frame_ = -1;
    latest_frame_ = -1;
    close_cycle_.clear();
    entry_cycle_.clear();
    pending_tick_ = -1;
    walk_tick_ = -1;
    prev_walk_frame_ = -1;
    osc_.restart(sc.plan, 0);
    dut_->rst_n = 0;
    dut_->sel_crf_i = sc.crf ? 1 : 0;
    dut_->tdm_data_i = 1;
    dut_->map_wr_en_i = 0;
    dut_->stream_en_i = 0;
    cycle(16);
    dut_->rst_n = 1;
    prev_dup_ = 0;
    prev_skip_ = 0;
    osc_.restart(sc.plan, sc.start_delay_steps, sc.sub_phase);
    soc_.restart(kFirstFrame, dut_->tdm_bclk_o);
}

//! The scenario's engagement window (coherence_bench's engage_columns), at
//! the pull the wrapper's aligner applies at one keep-off of error.
long JunctionHarness::window(const Scenario& sc) const {
    return engage_columns(sc.plan.ppm, static_cast<double>(dut_->engage_u_o) / kUPerPpm);
}

//! identity routing: stream channel c takes TDM slot c, the #451 routed map
void JunctionHarness::program_the_map() {
    for (int c = 0; c < kChans; c++) {
        const std::uint32_t en = 1u << 12;
        const std::uint32_t half = static_cast<std::uint32_t>(c & 1) << 11;
        const std::uint32_t src_tdm = 2u << 8;
        dut_->map_wr_en_i = 1;
        dut_->map_wr_addr_i = static_cast<std::uint32_t>(c);
        dut_->map_wr_data_i = en | half | src_tdm | static_cast<std::uint32_t>(c >> 1);
        cycle(1);
    }
    dut_->map_wr_en_i = 0;
    dut_->stream_en_i = 1;
}

//! One 5 ns step: evaluate only when a clock edge lands on it.
void JunctionHarness::step() {
    const Edges e = osc_.step();
    if (!e.axis && !e.tdm) return;
    dut_->clk = osc_.axis();
    dut_->clk_tdm = osc_.tdm();
    dut_->eval();
    if (e.tdm && osc_.tdm()) dut_->tdm_data_i = soc_.on_tdm_edge(dut_->tdm_bclk_o, dut_->tdm_fsync_o);
    if (e.axis && osc_.axis()) {
        ++cycle_;
        if (dut_->rst_n) observe();
    }
}

//! Advance n axis cycles.
void JunctionHarness::cycle(long n) {
    const long until = cycle_ + n;
    while (cycle_ < until) step();
}

//! The tick is noted before a same-cycle close, so a close always knows the
//! tick it follows or coincides with.
void JunctionHarness::observe() {
    if (dut_->tick_o) {
        pending_tick_ = cycle_;
        note_tick_phase();
    }
    if (dut_->cap_pv_o) observe_front_end();
    if (dut_->walk_pv_o) observe_walk();
    if (dut_->tvalid_o) bench_.beat(dut_->tdata_o, dut_->tkeep_o, dut_->tlast_o != 0);
}

//! Where the tick lands after the newest closed frame: the sweep's bins and,
//! in the CRF tail, the lock's excursion, taken circularly about its first
//! value so a lock sitting on the frame boundary does not read as a sweep.
void JunctionHarness::note_tick_phase() {
    if (latest_frame_ < 0) return;
    const long frame_cyc = static_cast<long>(kTickCycles + 0.5);
    const long closed = close_cycle_[static_cast<size_t>(latest_frame_ - base_frame_)];
    const long phase = (cycle_ - closed) % frame_cyc;
    t_.phase_hits[static_cast<size_t>(phase * kPhaseBins / frame_cyc) % kPhaseBins]++;
    if (!tail_) return;
    if (!t_.lock_seen) {
        t_.lock_phase_ref = phase;
        t_.lock_seen = true;
    }
    long d = phase - t_.lock_phase_ref;
    if (d >= frame_cyc / 2) d -= frame_cyc;
    if (d < -frame_cyc / 2) d += frame_cyc;
    t_.lock_phase_min = std::min(t_.lock_phase_min, d);
    t_.lock_phase_max = std::max(t_.lock_phase_max, d);
}

//! the unwrapped frame of a 16-bit ordinal, taken nearest the newest frame
//! the front end closed (every tap is within a few frames of it)
long JunctionHarness::unwrap(std::uint32_t ord16) const {
    const long ref = latest_frame_ < 0 ? static_cast<long>(ord16) : latest_frame_;
    const long delta = static_cast<long>((ord16 - static_cast<std::uint32_t>(ref)) & 0xFFFFu);
    return ref + (delta >= 0x8000 ? delta - 0x10000 : delta);
}

//! A front-end pair entering the crossbar. The last pair closes the frame.
void JunctionHarness::observe_front_end() {
    const int p = dut_->cap_slot_o;
    const std::uint32_t l = dut_->cap_l_o;
    const std::uint32_t r = dut_->cap_r_o;
    const bool tags_ok = p < kPairs && (l >> 16) == static_cast<std::uint32_t>(2 * p + 1) &&
                         (r >> 16) == static_cast<std::uint32_t>(2 * p + 2) && (l & 0xFFFFu) == (r & 0xFFFFu);
    if (!tags_ok) {
        if (base_frame_ >= 0) t_.frame_mismatch++;
        return;
    }
    pair_ord_[static_cast<size_t>(p)] = l & 0xFFFFu;
    note_entry(unwrap(l & 0xFFFFu), p);
    if (p != kPairs - 1) return;
    for (int q = 1; q < kPairs; q++) {
        if (pair_ord_[static_cast<size_t>(q)] != pair_ord_[0] && base_frame_ >= 0) t_.frame_mismatch++;
    }
    close_frame(unwrap(pair_ord_[0]));
}

//! When pair p of `frame` entered the crossbar (the age measurement's origin).
void JunctionHarness::note_entry(long frame, int p) {
    if (base_frame_ < 0 || frame < base_frame_) return;
    const size_t idx = static_cast<size_t>(frame - base_frame_);
    if (entry_cycle_.size() <= idx) entry_cycle_.resize(idx + 1, {});
    entry_cycle_[idx][static_cast<size_t>(p)] = cycle_;
}

//! A frame closes. The first close is the one the aligner engages on; every
//! later one records how far the close has moved from it.
void JunctionHarness::close_frame(long frame) {
    if (base_frame_ < 0) base_frame_ = frame;
    if (latest_frame_ >= 0 && frame != latest_frame_ + 1) t_.frame_mismatch++;
    const size_t idx = static_cast<size_t>(frame - base_frame_);
    if (close_cycle_.size() <= idx) close_cycle_.resize(idx + 1, -1);
    close_cycle_[idx] = cycle_;
    latest_frame_ = frame;
    t_.frames_in++;
    if (pending_tick_ < 0) return;
    const long after_tick = cycle_ - pending_tick_;
    if (!t_.engage_seen) {
        t_.engage_offset = after_tick;
        t_.engage_seen = true;
        return;
    }
    const long moved = wrap_offset(static_cast<double>(after_tick - t_.engage_offset));
    if (std::labs(moved) > std::max(-t_.run_min, t_.run_max)) t_.run_far_col = bench_.tally().columns;
    t_.run_min = std::min(t_.run_min, moved);
    t_.run_max = std::max(t_.run_max, moved);
}

//! The newest frame whose last pair entered at or before cycle `cyc`.
long JunctionHarness::newest_closed_by(long cyc) const {
    long f = latest_frame_;
    while (f >= base_frame_ && close_cycle_[static_cast<size_t>(f - base_frame_)] > cyc) --f;
    return f;
}

//! The frame this walk's tick takes (THE CROSSING in the header): the newest
//! closed before the tick cycle, or one closing on it when none is pending,
//! pending meaning closed and not read by the previous walk.
long JunctionHarness::frame_the_tick_takes() const {
    const long before = newest_closed_by(walk_tick_ - 1);
    const long on = newest_closed_by(walk_tick_);
    const long last_read = prev_walk_frame_ < base_frame_ ? base_frame_ - 1 : prev_walk_frame_;
    const bool pending = before > last_read;
    return (on != before && !pending) ? on : before;
}

//! One crossbar inject. Slot 0 opens a walk and reads the junction counters
//! (the tick's snapshot is a few cycles behind it, the next close a frame
//! ahead); the talker's last slot grades the walk.
void JunctionHarness::observe_walk() {
    const int s = dut_->walk_slot_o;
    if (s >= kPairs) return;
    if (s == 0) {
        walk_tick_ = pending_tick_;
        walk_dup_ = dut_->tdm_dup_cnt_o;
        walk_skip_ = dut_->tdm_skip_cnt_o;
    }
    const std::uint32_t l = dut_->walk_l_o;
    walk_frame_[static_cast<size_t>(s)] =
        (l >> 16) == static_cast<std::uint32_t>(2 * s + 1) ? unwrap(l & 0xFFFFu) : -1;
    if (s == kPairs - 1) grade_walk();
}

//! Every walk once a frame has closed: the counters against its own step;
//! the live walks also for tearing, the handoff law and age.
void JunctionHarness::grade_walk() {
    if (walk_tick_ < 0 || base_frame_ < 0) return;
    const long f = walk_frame_[0];
    const long expect = frame_the_tick_takes();
    count_walk(f);
    prev_walk_frame_ = f;
    if (!bench_.live() || f < base_frame_) return;
    t_.walks++;
    note_ages();
    for (int p = 1; p < kPairs; p++) {
        if (walk_frame_[static_cast<size_t>(p)] != f) {
            t_.walk_torn++;
            return;
        }
    }
    if (f < expect) t_.late++;
    if (f > expect) t_.early++;
}

//! The junction counters' movement since the previous walk's inject against
//! this walk's step: one dup for a repeat, step - 1 skips for a step over
//! frames, nothing for +1. The first walk with a frame only sets the base.
void JunctionHarness::count_walk(long f) {
    const auto dups = static_cast<long>(static_cast<std::uint16_t>(walk_dup_ - prev_dup_));
    const auto skips = static_cast<long>(static_cast<std::uint16_t>(walk_skip_ - prev_skip_));
    prev_dup_ = walk_dup_;
    prev_skip_ = walk_skip_;
    if (f < base_frame_ || prev_walk_frame_ < base_frame_) return;
    const long step = f - prev_walk_frame_;
    const long want_dups = step == 0 ? 1 : 0;
    const long want_skips = step > 1 ? step - 1 : 0;
    t_.counted++;
    t_.counter_events += dups + skips;
    if (dups != want_dups || skips != want_skips) t_.miscounted++;
}

//! Each pair's sample age at the walk's tick, from its own entry cycle.
void JunctionHarness::note_ages() {
    for (int p = 0; p < kPairs; p++) {
        const auto i = static_cast<size_t>(p);
        const long fp = walk_frame_[i];
        if (fp < base_frame_ || fp - base_frame_ >= static_cast<long>(entry_cycle_.size())) continue;
        const long age = walk_tick_ - entry_cycle_[static_cast<size_t>(fp - base_frame_)][i];
        if (t_.age_n[i] == 0 || age < t_.age_min[i]) t_.age_min[i] = age;
        if (t_.age_n[i] == 0 || age > t_.age_max[i]) t_.age_max[i] = age;
        t_.age_sum[i] += age;
        t_.age_n[i]++;
    }
}

//! One scenario from reset: run it, then grade and print what it measured.
void JunctionHarness::run(const Scenario& sc) {
    if (!sc.brief) {
        std::printf("\n[%s] %s, %s, TDM clock held %ld steps, %ld columns\n", sc.name.c_str(),
                    sc.crf ? "CRF (aligner engaged)" : "INTERNAL (free-running grid)", sc.plan.name.c_str(),
                    sc.start_delay_steps, sc.frames);
    }
    restart(sc);
    program_the_map();
    //! a cycle guard, never a verdict: a scenario that stops producing
    //! columns fails its [V] column count
    const long guard = cycle_ + (sc.frames + 400) * 1100;
    const long tail_from = tail_start(sc.frames, window(sc));
    while (bench_.tally().columns < sc.frames && cycle_ < guard) {
        tail_ = sc.crf && bench_.tally().columns >= tail_from;
        bench_.set_tail(tail_);
        cycle(1024);
    }
    bench_.finish();
    const std::uint64_t fails_before = check_.failures();
    grade(sc);
    if (sc.brief && check_.failures() == fails_before) return;
    bench_.print_table();
    print_ages();
}

//! Where the first close after reset lands against its tick with the TDM
//! clock unheld: the origin every placed CRF engagement is measured from,
//! once per plan and sub-step phase (a phase moves the TDM edges by up to a
//! cycle, so a placement is calibrated at its own).
long JunctionHarness::calibrate(const ClockPlan& plan, long sub_phase) {
    const std::string key = plan.name + "/" + std::to_string(sub_phase);
    const auto known = unheld_.find(key);
    if (known != unheld_.end()) return known->second;
    const Scenario sc{"calibrate", plan, true, 0, 0, false, true, kUnplaced, sub_phase};
    restart(sc);
    const long guard = cycle_ + 16 * 1100;
    while (!t_.engage_seen && cycle_ < guard) cycle(1);
    check_.that(("[calibrate " + plan.name + "] [V] the first close was seen").c_str(), t_.engage_seen);
    if (sub_phase == 0) {
        std::printf("\n  [i]  calibration, %s: with the TDM clock unheld the first close lands %ld cycles after its "
                    "tick\n", plan.name.c_str(), t_.engage_offset);
    }
    unheld_[key] = t_.engage_offset;
    return t_.engage_offset;
}

void JunctionHarness::grade(const Scenario& sc) {
    const std::string n = "[" + sc.name + "] ";
    if (!sc.brief) {
        std::printf("  [i]  front end: %ld whole frames captured, %ld not matching the pattern\n", t_.frames_in,
                    t_.frame_mismatch);
    }
    check_.dec((n + "[V] front-end pairs not matching the pattern sent").c_str(),
               static_cast<std::uint64_t>(t_.frame_mismatch), 0);
    check_.that((n + "[V] the front end captured a frame per column").c_str(), t_.frames_in >= sc.frames - 16);
    bench_.grade(check_, n, sc.frames, sc.plan.ppm, !sc.crf, window(sc));
    check_.that((n + "[W] walks graded").c_str(), t_.walks >= sc.frames - 16);
    check_.dec((n + "[W] walks reading two TDM frames").c_str(), static_cast<std::uint64_t>(t_.walk_torn), 0);
    check_.dec((n + "[W] walks older than the frame their tick takes").c_str(),
               static_cast<std::uint64_t>(t_.late), 0);
    check_.dec((n + "[W] walks newer than the frame their tick takes").c_str(),
               static_cast<std::uint64_t>(t_.early), 0);
    check_.that((n + "[V] the junction counters were compared on every walk").c_str(),
                t_.counted >= sc.frames - 16);
    check_.dec((n + "[C] walks whose repeat or skip the junction counters did not count").c_str(),
               static_cast<std::uint64_t>(t_.miscounted), 0);
    if (sc.sweep) grade_sweep(sc, n);
    if (sc.crf) grade_lock(sc, n);
}

//! INTERNAL: the drift must have carried the tick through the whole frame,
//! the slips must be the beat crossings the plan predicts, and the counters
//! must have had slips to count.
void JunctionHarness::grade_sweep(const Scenario& sc, const std::string& n) {
    int hit = 0;
    for (const long h : t_.phase_hits) hit += h > 0 ? 1 : 0;
    check_.dec((n + "[V] tick-to-frame phase bins the drift visited").c_str(), static_cast<std::uint64_t>(hit),
               kPhaseBins);
    const double ppm = sc.plan.ppm < 0 ? -sc.plan.ppm : sc.plan.ppm;
    const double crossings = static_cast<double>(bench_.tally().columns) * ppm * 1e-6;
    const long clusters = bench_.tally().clusters;
    std::printf("  [i]  %.2f beat crossings predicted, %ld slip clusters seen, %ld junction counter events\n",
                crossings, clusters, t_.counter_events);
    check_.that((n + "[C] one slip cluster per beat crossing").c_str(),
                clusters >= static_cast<long>(crossings) - 1 && clusters <= static_cast<long>(crossings) + 2);
    check_.that((n + "[V] the drift gave the junction counters slips to count").c_str(),
                clusters >= 1 && t_.counter_events >= clusters);
}

//! CRF: the aligner must be engaged, a placed engagement must have landed
//! where it was placed, and in the second half of the run the packet grid
//! must hold its phase on the frame with no slip.
void JunctionHarness::grade_lock(const Scenario& sc, const std::string& n) {
    check_.that((n + "[V] the aligner engaged").c_str(), dut_->engaged_o != 0);
    const long spread = t_.lock_phase_max - t_.lock_phase_min;
    const long landed = wrap_offset(static_cast<double>(t_.engage_offset));
    std::printf("  [i]  %s: engaged %+ld cycles from the crossing, the close then moved %+ld..%+ld (furthest "
                "at column %ld); tail: tick %ld cycles after the frame close, %+ld..%+ld (spread %ld); %ld repeats, "
                "%ld skips\n", sc.name.c_str(), landed, t_.run_min, t_.run_max, t_.run_far_col, t_.lock_phase_ref,
                t_.lock_phase_min, t_.lock_phase_max, spread, bench_.tally().dups, bench_.tally().skips);
    if (bench_.tally().dups + bench_.tally().skips > 0) {
        const long win = window(sc);
        std::printf("  [i]  %s: last slip at column %ld; engagement window %s columns\n", sc.name.c_str(),
                    bench_.tally().last_slip_col, win == kUnbounded ? "unbounded" : std::to_string(win).c_str());
    }
    if (sc.placed != kUnplaced) {
        check_.that((n + "[V] the engagement close landed where the sweep placed it").c_str(),
                    t_.engage_seen && std::labs(landed - sc.placed) <= kPlaceTolerance);
        placed_landed_.push_back(landed);
    }
    check_.that((n + "[V] the CRF lock held its phase (spread under a quarter frame)").c_str(),
                t_.lock_seen && spread < static_cast<long>(kTickCycles / 4));
    check_.dec((n + "[C] slips while the CRF lock held").c_str(),
               static_cast<std::uint64_t>(bench_.tally().tail_slips), 0);
}

void JunctionHarness::print_ages() const {
    for (int p = 0; p < kPairs; p++) {
        const auto i = static_cast<size_t>(p);
        if (t_.age_n[i] == 0) continue;
        std::printf("  [i]    pair %d sample age at the tick: min %ld  mean %.1f  max %ld axis cycles\n", p,
                    t_.age_min[i], static_cast<double>(t_.age_sum[i]) / static_cast<double>(t_.age_n[i]),
                    t_.age_max[i]);
    }
}

//! A placed sweep: calibrate its plan, run one brief scenario per offset,
//! then require the engagements to have covered the window.
void JunctionHarness::run_sweep(const Sweep& sw) {
    const long unheld = calibrate(sw.plan);
    std::printf("\n[%s] CRF, %s, engagement placed every %ld cycles from %+ld to %+ld of the crossing, "
                "%ld columns each\n", sw.tag.c_str(), sw.plan.name.c_str(), sw.step, sw.lo, sw.hi, sw.frames);
    if (sw.holds > 1 || sw.phases > 1) {
        std::printf("  [i]  each offset at %ld quarter-cycle holds x %ld sub-step phases of the TDM clock\n",
                    sw.holds, sw.phases);
    }
    placed_landed_.clear();
    for (long off = sw.lo; off <= sw.hi; off += sw.step) {
        for (long h = 0; h < sw.holds; h++) {
            for (long k = 0; k < sw.phases; k++) {
                char name[48];
                if (sw.holds > 1 || sw.phases > 1) {
                    std::snprintf(name, sizeof name, "%s%+ld.%ld/%ld", sw.tag.c_str(), off, h, k);
                } else {
                    std::snprintf(name, sizeof name, "%s%+ld", sw.tag.c_str(), off);
                }
                run({name, sw.plan, true, delay_for(k == 0 ? unheld : calibrate(sw.plan, k), off) + h, sw.frames,
                     false, true, off, k});
            }
        }
    }
    grade_window(sw);
}

//! The sweep's engagements must have covered its window (coherence_bench's
//! grade_window).
void JunctionHarness::grade_window(const Sweep& sw) {
    coherence::grade_window(check_, sw, placed_landed_);
}

//! What each run mode builds (the header's list). The mutation arm's modes:
//! `quick` leaves out the true plan's whole beat and every placed sweep;
//! `band` is the true plan's band alone (the guard mutants); `band50` the
//! +/-50 ppm bands at a 32-cycle step (the keep-off's value); `fine` the
//! sub-cycle sweep alone (the NCO's terminal compare).
enum class Mode { kAll, kQuick, kBand, kBand50, kFine };

//! the sub-cycle sweep's holds per offset: one quarter-cycle step each,
//! covering the cycle between two offsets
constexpr long kQuarterHolds = 4;

std::vector<Scenario> scenarios(Mode mode) {
    std::vector<Scenario> list;
    if (mode != Mode::kAll && mode != Mode::kQuick) return list;
    //! one beat of the true plan is 1 / 10.64e-6 = 93,990 frames
    if (mode == Mode::kAll) list.push_back({"INT-true", true_plan(), false, 0, 96'000, true, false, kUnplaced});
    list.push_back({"INT-slow", ppm_plan(-1000), false, 0, 3'200, true, false, kUnplaced});
    list.push_back({"INT-fast", ppm_plan(+1000), false, 0, 3'200, true, false, kUnplaced});
    //! a TDM frame is 512 x 2 x 1591/391 = 4166.7 steps: sixteen offsets
    for (int k = 0; k < 16; k++) {
        char name[24];
        std::snprintf(name, sizeof name, "CRF-true-%02d", k);
        list.push_back({name, true_plan(), true, k * 4167L / 16, 2'000, false, false, kUnplaced});
    }
    //! the full run follows the +/-50 ppm acquisition past its peak (about
    //! 7,800 frames); the mutation arm's quick runs stop at 6,000
    const long long_run = mode == Mode::kAll ? 9'000 : 6'000;
    for (const int ppm : {-50, +50}) {
        for (int k = 0; k < 4; k++) {
            char name[24];
            std::snprintf(name, sizeof name, "CRF%+d-%d", ppm, k);
            list.push_back({name, ppm_plan(ppm), true, k * 4167L / 4 + 130, long_run, false, false, kUnplaced});
        }
    }
    return list;
}

std::vector<Sweep> sweeps(Mode mode) {
    std::vector<Sweep> list;
    if (mode == Mode::kQuick) return list;
    if (mode == Mode::kBand50) {
        list.push_back({"CRF-band-50", ppm_plan(-50), -176, 32, 32, 6'000});
        list.push_back({"CRF-band+50", ppm_plan(+50), -32, 176, 32, 6'000});
        return list;
    }
    const Sweep fine{"CRF-fine-50", ppm_plan(-50), -1, 1, 1, 300, kQuarterHolds, kSubPhases};
    if (mode == Mode::kFine) return {fine};
    list.push_back({"CRF-band-true", true_plan(), -32, 32, 1, 2'000});
    if (mode == Mode::kBand) return list;
    list.push_back({"CRF-frame-true", true_plan(), -512, 512, 16, 2'000});
    list.push_back({"CRF-band-50", ppm_plan(-50), -176, 32, 4, 6'000});
    list.push_back({"CRF-band+50", ppm_plan(+50), -32, 176, 4, 6'000});
    list.push_back(fine);
    //! the settled lock past the envelope: the acquisition slips of 100 ppm
    //! end by column 13,100 (measured), inside the first half
    for (const int ppm : {-80, +80, -100, +100}) {
        char tag[24];
        std::snprintf(tag, sizeof tag, "CRF-settle%+d", ppm);
        const long near = ppm < 0 ? 0 : 8;
        const long far = ppm < 0 ? -256 : 8 + 256;
        list.push_back({tag, ppm_plan(ppm), std::min(near, far), std::max(near, far), 256, 30'000});
    }
    return list;
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vcoherence_wrap> model;
    JunctionHarness harness(model.get());
    const std::string arg = argc > 1 ? argv[1] : "";
    const Mode mode = arg == "--quick"    ? Mode::kQuick
                      : arg == "--band"   ? Mode::kBand
                      : arg == "--band50" ? Mode::kBand50
                      : arg == "--fine"   ? Mode::kFine
                                          : Mode::kAll;
    std::printf("=== TDM capture junction: AAF column coherence (#617)%s ===\n",
                mode == Mode::kQuick    ? ", --quick: the true plan's whole beat and the placed sweeps left out"
                : mode == Mode::kBand   ? ", --band: the true plan's band alone"
                : mode == Mode::kBand50 ? ", --band50: the +/-50 ppm bands every 32 cycles alone"
                : mode == Mode::kFine   ? ", --fine: the sub-cycle sweep alone"
                                        : "");
    model.get()->eval();
    std::printf("  [i]  aligner keep-off %u cycles (milan_datapath's MGA_KEEPOFF_CYC_C), engagement pull %.1f ppm\n",
                static_cast<unsigned>(model.get()->keepoff_cyc_o),
                static_cast<double>(model.get()->engage_u_o) / kUPerPpm);
    for (const Scenario& sc : scenarios(mode)) harness.run(sc);
    for (const Sweep& sw : sweeps(mode)) harness.run_sweep(sw);
    return harness.report();
}
