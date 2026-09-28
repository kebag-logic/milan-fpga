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
// INTERNAL AND CRF. The clock-source verdict is the wrapper's sel_crf_i, the
// net milan_datapath resolves from the stored CLOCK_SOURCE. INTERNAL leaves
// the packet grid free-running, so the TDM frame drifts through it: the
// true-plan scenario runs a whole beat, the exaggerated ones several. CRF
// engages the aligner, which locks the packet grid where it found the frame
// marker; the CRF scenarios start the TDM clock at sixteen offsets across one
// frame, so a lock lands in every region the INTERNAL sweep crosses, on a
// TDM clock that runs off nominal (the true plan, and +/-50 ppm).
//
// THE CHECKS, per scenario:
//   [A] every AAF column after the first valid one carries its own channel
//       tags, and all eight channels one TDM frame (the acceptance check);
//   [W] every media-tick walk read one frame, and that frame is the newest
//       one whose last pair entered the crossbar at or before the tick (no
//       added sample of latency) and not one that entered after the walk's
//       first inject (the frame is fixed before the walk reads it);
//   [C] column continuity: each column's frame is the previous one's plus
//       one, or a slip cluster netting one frame in the drift's direction,
//       one cluster per beat crossing;
//   [V] vacuity: the front end captured the pattern it was sent, every
//       requested column was decoded, the INTERNAL drift swept the tick
//       through the whole frame, and a CRF lock held its phase slip-free.
// Each scenario prints its torn-state table in the #451 page's form (the
// frame offset of pairs 1, 2, 3 against pair 0) and, as information, the
// age of each pair's sample at the walk's tick.
//
// mutants.py rebuilds this harness against defective copies of the crossbar
// and requires the named checks to fail; the first of them is the ce550952
// law, per-pair holds read at slot time.

#include "coherence_bench.hpp"
#include "Vcoherence_wrap.h"
#include "verilated.h"

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
};

//! What the junction taps measured (the columns are the bench's).
struct JunctionTally {
    long frames_in = 0;         //! whole frames the front end delivered
    long frame_mismatch = 0;    //! front-end pairs not matching the pattern
    long walks = 0;             //! walks graded
    long walk_torn = 0;         //! walks reading two frames
    long late = 0;              //! walks older than the newest closed frame
    long early = 0;             //! walks reading a frame closed after inject
    std::array<long, kPhaseBins> phase_hits{};
    long lock_phase_ref = 0;    //! first tick-to-close phase of the CRF tail
    long lock_phase_min = 0;    //! its excursion either side of that, cycles
    long lock_phase_max = 0;
    bool lock_seen = false;
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
    long walk_emit_ = -1;
    std::array<long, kPairs> walk_frame_{};

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
    void observe_walk();
    void grade_walk();
    void note_ages();
    void grade(const Scenario& sc);
    void grade_sweep(const Scenario& sc, const std::string& n);
    void grade_lock(const std::string& n);
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
    walk_emit_ = -1;
    osc_.restart(sc.plan, 0);
    dut_->rst_n = 0;
    dut_->sel_crf_i = sc.crf ? 1 : 0;
    dut_->tdm_data_i = 1;
    dut_->map_wr_en_i = 0;
    dut_->stream_en_i = 0;
    cycle(16);
    dut_->rst_n = 1;
    osc_.restart(sc.plan, sc.start_delay_steps);
    soc_.restart(kFirstFrame, dut_->tdm_bclk_o);
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

void JunctionHarness::close_frame(long frame) {
    if (base_frame_ < 0) base_frame_ = frame;
    if (latest_frame_ >= 0 && frame != latest_frame_ + 1) t_.frame_mismatch++;
    const size_t idx = static_cast<size_t>(frame - base_frame_);
    if (close_cycle_.size() <= idx) close_cycle_.resize(idx + 1, -1);
    close_cycle_[idx] = cycle_;
    latest_frame_ = frame;
    t_.frames_in++;
}

//! The newest frame whose last pair entered at or before cycle `cyc`.
long JunctionHarness::newest_closed_by(long cyc) const {
    long f = latest_frame_;
    while (f >= base_frame_ && close_cycle_[static_cast<size_t>(f - base_frame_)] > cyc) --f;
    return f;
}

//! One crossbar inject. Slot 0 opens a walk; the talker's last slot grades it.
void JunctionHarness::observe_walk() {
    const int s = dut_->walk_slot_o;
    if (s >= kPairs) return;
    if (s == 0) {
        walk_tick_ = pending_tick_;
        walk_emit_ = cycle_;
    }
    const std::uint32_t l = dut_->walk_l_o;
    walk_frame_[static_cast<size_t>(s)] =
        (l >> 16) == static_cast<std::uint32_t>(2 * s + 1) ? unwrap(l & 0xFFFFu) : -1;
    if (s == kPairs - 1) grade_walk();
}

void JunctionHarness::grade_walk() {
    if (!bench_.live() || walk_tick_ < 0 || base_frame_ < 0) return;
    const long f = walk_frame_[0];
    if (f < base_frame_) return;
    t_.walks++;
    note_ages();
    for (int p = 1; p < kPairs; p++) {
        if (walk_frame_[static_cast<size_t>(p)] != f) {
            t_.walk_torn++;
            return;
        }
    }
    if (f < newest_closed_by(walk_tick_)) t_.late++;
    if (f > newest_closed_by(walk_emit_ - 1)) t_.early++;
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
    std::printf("\n[%s] %s, %s, TDM clock held %ld steps, %ld columns\n", sc.name.c_str(),
                sc.crf ? "CRF (aligner engaged)" : "INTERNAL (free-running grid)", sc.plan.name.c_str(),
                sc.start_delay_steps, sc.frames);
    restart(sc);
    program_the_map();
    //! a cycle guard, never a verdict: a scenario that stops producing
    //! columns fails its [V] column count
    const long guard = cycle_ + (sc.frames + 400) * 1100;
    while (bench_.tally().columns < sc.frames && cycle_ < guard) {
        tail_ = sc.crf && bench_.tally().columns >= sc.frames / 2;
        bench_.set_tail(tail_);
        cycle(1024);
    }
    bench_.finish();
    grade(sc);
    bench_.print_table();
    print_ages();
}

void JunctionHarness::grade(const Scenario& sc) {
    const std::string n = "[" + sc.name + "] ";
    std::printf("  [i]  front end: %ld whole frames captured, %ld not matching the pattern\n", t_.frames_in,
                t_.frame_mismatch);
    check_.dec((n + "[V] front-end pairs not matching the pattern sent").c_str(),
               static_cast<std::uint64_t>(t_.frame_mismatch), 0);
    check_.that((n + "[V] the front end captured a frame per column").c_str(), t_.frames_in >= sc.frames - 16);
    bench_.grade(check_, n, sc.frames, sc.plan.ppm);
    check_.that((n + "[W] walks graded").c_str(), t_.walks >= sc.frames - 16);
    check_.dec((n + "[W] walks reading two TDM frames").c_str(), static_cast<std::uint64_t>(t_.walk_torn), 0);
    check_.dec((n + "[W] walks older than the newest frame closed by the tick").c_str(),
               static_cast<std::uint64_t>(t_.late), 0);
    check_.dec((n + "[W] walks reading a frame closed after their first inject").c_str(),
               static_cast<std::uint64_t>(t_.early), 0);
    if (sc.sweep) grade_sweep(sc, n);
    if (sc.crf) grade_lock(n);
}

//! INTERNAL: the drift must have carried the tick through the whole frame,
//! and the slips must be the beat crossings the plan predicts.
void JunctionHarness::grade_sweep(const Scenario& sc, const std::string& n) {
    int hit = 0;
    for (const long h : t_.phase_hits) hit += h > 0 ? 1 : 0;
    check_.dec((n + "[V] tick-to-frame phase bins the drift visited").c_str(), static_cast<std::uint64_t>(hit),
               kPhaseBins);
    const double ppm = sc.plan.ppm < 0 ? -sc.plan.ppm : sc.plan.ppm;
    const double crossings = static_cast<double>(bench_.tally().columns) * ppm * 1e-6;
    const long clusters = bench_.tally().clusters;
    std::printf("  [i]  %.2f beat crossings predicted, %ld slip clusters seen\n", crossings, clusters);
    check_.that((n + "[C] one slip cluster per beat crossing").c_str(),
                clusters >= static_cast<long>(crossings) - 1 && clusters <= static_cast<long>(crossings) + 2);
}

//! CRF: the aligner must be engaged, and in the second half of the run the
//! packet grid must hold its phase on the frame with no slip.
void JunctionHarness::grade_lock(const std::string& n) {
    check_.that((n + "[V] the aligner engaged").c_str(), dut_->engaged_o != 0);
    const long spread = t_.lock_phase_max - t_.lock_phase_min;
    std::printf("  [i]  CRF tail: tick %ld cycles after the frame close, %+ld..%+ld (spread %ld)\n",
                t_.lock_phase_ref, t_.lock_phase_min, t_.lock_phase_max, spread);
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

//! The scenario list: INTERNAL drift sweeps, then CRF locks at sixteen
//! phases on the true plan and at four on an exaggerated one each way.
//! `quick` (the mutation arm's runs) leaves out the one long scenario, the
//! true plan's whole beat; the +/-1000 ppm sweeps cross the same phases.
std::vector<Scenario> scenarios(bool quick) {
    std::vector<Scenario> list;
    //! one beat of the true plan is 1 / 10.64e-6 = 93,990 frames
    if (!quick) list.push_back({"INT-true", true_plan(), false, 0, 96'000, true});
    list.push_back({"INT-slow", ppm_plan(-1000), false, 0, 3'200, true});
    list.push_back({"INT-fast", ppm_plan(+1000), false, 0, 3'200, true});
    //! a TDM frame is 512 x 2 x 1591/391 = 4166.7 steps: sixteen offsets
    for (int k = 0; k < 16; k++) {
        char name[24];
        std::snprintf(name, sizeof name, "CRF-true-%02d", k);
        list.push_back({name, true_plan(), true, k * 4167L / 16, 2'000, false});
    }
    for (const int ppm : {-50, +50}) {
        for (int k = 0; k < 4; k++) {
            char name[24];
            std::snprintf(name, sizeof name, "CRF%+d-%d", ppm, k);
            list.push_back({name, ppm_plan(ppm), true, k * 4167L / 4 + 130, 6'000, false});
        }
    }
    return list;
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vcoherence_wrap> model;
    JunctionHarness harness(model.get());
    const bool quick = argc > 1 && std::string(argv[1]) == "--quick";
    std::printf("=== TDM capture junction: AAF column coherence (#617)%s ===\n",
                quick ? ", --quick: the true plan's whole beat left out" : "");
    for (const Scenario& sc : scenarios(quick)) harness.run(sc);
    return harness.report();
}
