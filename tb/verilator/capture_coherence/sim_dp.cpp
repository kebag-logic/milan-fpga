// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_dp - AAF column coherence through the WHOLE milan_datapath (#617).
//
// WHY THIS LEG EXISTS BESIDE sim_main.cpp. The junction harness binds the
// front end, the grid and the crossbar in a wrapper that restates
// milan_datapath's wiring, which is what makes a whole beat of the true plan
// affordable - and is also why it cannot see that wiring. Two facts live only
// in the datapath: which frame length the crossbar is told
// (CMAP_TDM_FRAME_PAIRS_C, derived from the front end's per-frame supply) and
// how the stored clock source reaches the grid. This leg elaborates the
// shipping AX7101 1x1 TDM8 shape (sw/litex/build.sh cfg_ax7101's parameters,
// the 50 MHz milan clock of configs/endstation_ax7101_1x1_tdm8.yaml) and
// reads the talker's frames where a listener would: the MAC transmit port.
//
// THE STIMULUS. The same bench as the junction leg (coherence_bench.hpp): the
// SoC shifts the #451 pattern into tdm_data_i off tdm_bclk_o/tdm_fsync_o, and
// the oscillator runs the TDM clock (clk_tdm_i, which is clk_audio_i on this
// shape) on a chosen plan against the 50 MHz axis clock. The talker is set up
// the way the #451 bench set it up, through the CSR face: eight identity
// mappings on the capture map (CHMAP_SEL/CHMAP_WORD with CHMAP_CTRL armed;
// the shape's dynamic STREAM_PORT_OUTPUT map already puts the crossbar in
// circuit) and AAF_CTRL's enable with the diagnostic bypass, so no ACMP or
// SRP exchange is needed to see the frames.
//
// INTERNAL AND CRF. INTERNAL is the power-on selection. CRF is selected by
// poking the processor's stored CLOCK_SOURCE row, the documented
// public_flat_rw tap tb/verilator/milan_dp/sim_aclk.cpp uses one hop
// upstream of the command chain sim_nxn's AECP-FACE arms prove; the leg then
// requires the root's resolved verdict and the aligner's engagement to
// follow it. The INTERNAL scenarios run over two beats on +/-1000 ppm plans.
// The CRF ones, all on the true plan, 1,500 columns each:
//   DP-CRF-0..7   eight TDM-clock offsets an eighth of a frame apart, so most
//                 of them lock in a region the pre-#617 crossbar tore;
//   DP-band-true  the aligner's engagement close PLACED (coherence_bench's
//                 calibration) every 2 cycles from -20 to +4 cycles of the
//                 capture walk's crossing: the band where milan_datapath's
//                 aligner binding decides whether a lock repeats and skips
//                 frames (#617 round 2). This leg is the only one that sees
//                 that binding - the marker, the delayed tick, the keep-off.
//
// THE CHECKS are the column bench's ([A], [C], [V]; under CRF the CRF law:
// slips only in an engagement's first columns, netting zero), plus, from the
// pins and the root's public taps: the INTERNAL drift visited every
// tick-to-fsync phase bin; under CRF the root saw the selection, the aligner
// engaged, a placed engagement landed where it was placed, the second half
// of the run held its phase with no slip, and SLIP_TDM counted exactly the
// repeats and skips the columns show.

#include "coherence_bench.hpp"
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"

#include <cstdlib>
#include <map>

namespace {

using namespace coherence;

//! AXI4-Lite handshake guard: cycles one beat may wait before the BFM gives
//! up rather than hanging the leg
constexpr int kAxiGuardCycles = 2048;
//! CSR byte offsets (docs/reference/REGISTER_MAP.md), plain integers because
//! each is handed straight to the BFM as an address
constexpr std::uint16_t kAafCtrl = 0x654;
constexpr std::uint16_t kChmapCtrl = 0x900;
constexpr std::uint16_t kChmapSel = 0x904;
constexpr std::uint16_t kChmapWord = 0x908;
//! AAF_CTRL: [0] enable, [1] diagnostic bypass, [27:16] VID 2
constexpr std::uint32_t kAafCtrlRun = 0x0002'0003;
//! the AX 1x1 shape's CRF CLOCK_SOURCE index (INTERNAL is 0)
constexpr std::uint16_t kCrfClksrcIx = 1;
//! phase bins for the sweep-coverage vacuity check
constexpr int kPhaseBins = 16;
constexpr std::uint32_t kFirstFrame = 0x0100;

//! One run from reset.
struct Scenario {
    std::string name;
    ClockPlan plan;
    bool crf = false;           //! the stored clock source poked to CRF
    long start_delay_steps = 0; //! TDM clock held this long after reset
    long frames = 0;            //! columns to decode
    bool sweep = false;         //! INTERNAL: the tick must cross the frame
    bool brief = false;         //! one [i] line unless a check fails
    long placed = kUnplaced;    //! engagement close offset from the crossing
};

//! The harness: the datapath, the oscillator, the SoC and the column bench.
class DatapathHarness {
 public:
    explicit DatapathHarness(Vmilan_datapath* model) : dut_(model) {}
    void run(const Scenario& sc);
    void run_sweep(const Sweep& sw);
    int report() { return check_.report(); }

 private:
    Vmilan_datapath* dut_;
    milan::tb::Checker check_{"capture_coherence_dp"};
    Oscillator osc_;
    SocTransmitter soc_;
    ColumnBench bench_;
    long cycle_ = 0;
    int drp_lat_ = 0;
    bool tail_ = false;
    int fsync_prev_ = 0;
    long last_fsync_ = -1;
    std::array<long, kPhaseBins> phase_hits_{};
    long lock_ref_ = 0;
    long lock_min_ = 0;
    long lock_max_ = 0;
    bool lock_seen_ = false;
    long last_tick_ = -1;
    std::uint64_t bank_prev_ = 0;   //! the crossbar's frame bank, pair 0
    long engage_offset_ = 0;        //! the engagement close, cycles after its tick
    bool engage_seen_ = false;
    std::vector<long> placed_landed_;
    std::map<std::string, long> unheld_;  //! calibrations, by plan name

    void restart(const Scenario& sc);
    void step();
    void cycle(long n);
    void observe();
    void note_tick();
    void axi_write(std::uint16_t addr, std::uint32_t data);
    void program_the_talker();
    void select_crf(const std::string& n);
    void grade(const Scenario& sc);
    void grade_crf(const Scenario& sc, const std::string& n);
    long calibrate(const ClockPlan& plan);
};

void DatapathHarness::restart(const Scenario& sc) {
    bench_.restart();
    tail_ = false;
    last_fsync_ = -1;
    phase_hits_.fill(0);
    lock_ref_ = lock_min_ = lock_max_ = 0;
    lock_seen_ = false;
    last_tick_ = -1;
    bank_prev_ = 0;
    engage_seen_ = false;
    osc_.restart(sc.plan, 0);
    dut_->axis_resetn = 0;
    dut_->gtx_resetn = 0;
    dut_->m_axis_mac_tx_tready = 1;
    dut_->i_mmcm_locked = 1;
    dut_->tdm_data_i = 1;
    cycle(64);
    dut_->axis_resetn = 1;
    dut_->gtx_resetn = 1;
    osc_.restart(sc.plan, sc.start_delay_steps);
    soc_.restart(kFirstFrame, dut_->tdm_bclk_o);
    fsync_prev_ = dut_->tdm_fsync_o;
    cycle(512);
}

//! One 5 ns step: evaluate only when a clock edge lands on it. gtx_clk is
//! axis_clk (the PHC contract); clk_audio_i is clk_tdm_i on this shape.
void DatapathHarness::step() {
    const Edges e = osc_.step();
    if (!e.axis && !e.tdm) return;
    dut_->axis_clk = osc_.axis();
    dut_->gtx_clk = osc_.axis();
    dut_->clk_tdm_i = osc_.tdm();
    dut_->clk_audio_i = osc_.tdm();
    dut_->eval();
    if (e.tdm && osc_.tdm()) dut_->tdm_data_i = soc_.on_tdm_edge(dut_->tdm_bclk_o, dut_->tdm_fsync_o);
    if (e.axis && osc_.axis()) {
        ++cycle_;
        observe();
    }
}

void DatapathHarness::cycle(long n) {
    const long until = cycle_ + n;
    while (cycle_ < until) step();
}

void DatapathHarness::observe() {
    //! the minimal MMCM DRP responder of sim_aclk: DRDY a few cycles after
    //! DEN, data 0 (the servo's full MMCM model is tb/verilator/mmcm_servo's)
    dut_->i_mmcm_drp_rdy = 0;
    if (drp_lat_ > 0 && --drp_lat_ == 0) dut_->i_mmcm_drp_rdy = 1;
    if (dut_->o_mmcm_drp_en) drp_lat_ = 3;
    dut_->i_mmcm_drp_do = 0;
    const int fsync = dut_->tdm_fsync_o;
    if (fsync && !fsync_prev_) last_fsync_ = cycle_;
    fsync_prev_ = fsync;
    if (dut_->rootp->milan_datapath__DOT__media_tick_p) {
        last_tick_ = cycle_;
        note_tick();
    }
    //! the engagement close: the first frame the crossbar publishes once the
    //! root resolves CRF, seen on its frame bank the cycle after the close.
    //! It is read off the crossbar, not off the aligner, so a placement does
    //! not depend on the aligner binding it is there to test.
    const std::uint64_t bank = dut_->rootp->milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_r[0];
    if (bank != bank_prev_ && !engage_seen_ && last_tick_ >= 0 &&
        dut_->rootp->milan_datapath__DOT__crf_clk_selected_r) {
        engage_offset_ = (cycle_ - 1) - last_tick_;
        engage_seen_ = true;
    }
    bank_prev_ = bank;
    if (dut_->m_axis_mac_tx_tvalid && dut_->m_axis_mac_tx_tready) {
        bench_.beat(dut_->m_axis_mac_tx_tdata, dut_->m_axis_mac_tx_tkeep, dut_->m_axis_mac_tx_tlast != 0);
    }
}

//! The tick's phase after the latest fsync edge at the pin: the sweep's bins
//! and, in the CRF tail, the lock's circular excursion.
void DatapathHarness::note_tick() {
    if (last_fsync_ < 0) return;
    const long frame_cyc = static_cast<long>(kTickCycles + 0.5);
    const long phase = (cycle_ - last_fsync_) % frame_cyc;
    phase_hits_[static_cast<size_t>(phase * kPhaseBins / frame_cyc) % kPhaseBins]++;
    if (!tail_) return;
    if (!lock_seen_) {
        lock_ref_ = phase;
        lock_seen_ = true;
    }
    long d = phase - lock_ref_;
    if (d >= frame_cyc / 2) d -= frame_cyc;
    if (d < -frame_cyc / 2) d += frame_cyc;
    lock_min_ = std::min(lock_min_, d);
    lock_max_ = std::max(lock_max_, d);
}

void DatapathHarness::axi_write(std::uint16_t addr, std::uint32_t data) {
    dut_->s_axi_awaddr = addr;
    dut_->s_axi_awvalid = 1;
    dut_->s_axi_wdata = data;
    dut_->s_axi_wstrb = 0xF;
    dut_->s_axi_wvalid = 1;
    dut_->s_axi_bready = 1;
    bool accepted = false;
    for (int g = 0; g < kAxiGuardCycles && !accepted; g++) {
        accepted = dut_->s_axi_awready && dut_->s_axi_wready;
        cycle(1);
    }
    dut_->s_axi_awvalid = 0;
    dut_->s_axi_wvalid = 0;
    bool responded = false;
    for (int g = 0; g < kAxiGuardCycles && !responded; g++) {
        responded = dut_->s_axi_bvalid;
        cycle(1);
    }
    dut_->s_axi_bready = 0;
    if (!accepted || !responded) check_.fail("[V] a CSR write was not accepted by the AXI4-Lite face");
}

//! The #451 routed DIN setup through the CSR face: stream channel c takes
//! TDM slot c ({EN, SRC=TDM, HALF=c&1, IDX_LO=c/2}), then the talker runs.
void DatapathHarness::program_the_talker() {
    axi_write(kChmapCtrl, 1);
    for (int c = 0; c < kChans; c++) {
        axi_write(kChmapSel, (1u << 8) | static_cast<std::uint32_t>(c));
        axi_write(kChmapWord, (1u << 15) | (2u << 12) | (static_cast<std::uint32_t>(c & 1) << 8) |
                                  static_cast<std::uint32_t>(c >> 1));
    }
    axi_write(kAafCtrl, kAafCtrlRun);
}

//! The stored CLOCK_SOURCE row, poked to this shape's CRF index.
void DatapathHarness::select_crf(const std::string& n) {
    dut_->rootp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r[0] =
        kCrfClksrcIx;
    cycle(8);
    check_.that((n + "[V] the root resolves the CRF selection").c_str(),
                dut_->rootp->milan_datapath__DOT__crf_clk_selected_r != 0);
}

void DatapathHarness::run(const Scenario& sc) {
    const std::string n = "[" + sc.name + "] ";
    if (!sc.brief) {
        std::printf("\n[%s] milan_datapath, %s, %s, TDM clock held %ld steps, %ld columns\n", sc.name.c_str(),
                    sc.crf ? "CRF selected" : "INTERNAL", sc.plan.name.c_str(), sc.start_delay_steps, sc.frames);
    }
    restart(sc);
    if (sc.crf) select_crf(n);
    program_the_talker();
    //! a cycle guard, never a verdict: a scenario that stops producing
    //! columns fails its [V] column count
    const long guard = cycle_ + (sc.frames + 400) * 1100;
    while (bench_.tally().columns < sc.frames && cycle_ < guard) {
        tail_ = sc.crf && bench_.tally().columns >= sc.frames / 2;
        bench_.set_tail(tail_);
        cycle(1024);
    }
    bench_.finish();
    const std::uint64_t fails_before = check_.failures();
    grade(sc);
    if (sc.brief && check_.failures() == fails_before) return;
    bench_.print_table();
}

//! Every CRF plan of this leg is the true one, inside the Milan bound, where
//! the engagement window is kEngageColumns whatever the aligner's pull (the
//! junction leg grades the rates past the bound).
void DatapathHarness::grade(const Scenario& sc) {
    const std::string n = "[" + sc.name + "] ";
    if (sc.crf) {
        check_.that((n + "[V] the CRF plan is inside the Milan bound this leg's engagement window assumes").c_str(),
                    std::fabs(sc.plan.ppm) <= kMilanPpm);
    }
    bench_.grade(check_, n, sc.frames, sc.plan.ppm, !sc.crf, kEngageColumns);
    if (!sc.crf) {
        check_.that((n + "[V] the root keeps the INTERNAL selection").c_str(),
                    dut_->rootp->milan_datapath__DOT__crf_clk_selected_r == 0);
    }
    if (sc.sweep) {
        int hit = 0;
        for (const long h : phase_hits_) hit += h > 0 ? 1 : 0;
        check_.dec((n + "[V] tick-to-fsync phase bins the drift visited").c_str(),
                   static_cast<std::uint64_t>(hit), kPhaseBins);
        check_.that((n + "[C] the drift crossed at least one beat").c_str(), bench_.tally().clusters >= 1);
    }
    if (sc.crf) grade_crf(sc, n);
}

//! CRF: the aligner engaged where it was placed, the tail held its phase
//! with no slip, and SLIP_TDM counted exactly what the columns show. Under
//! CRF no slip falls in the in-flight walks at the end of a run, so the
//! counters' totals since reset and the bench's are one count.
void DatapathHarness::grade_crf(const Scenario& sc, const std::string& n) {
    check_.that((n + "[V] the aligner engaged").c_str(), dut_->rootp->milan_datapath__DOT__mga_engaged_w != 0);
    const long spread = lock_max_ - lock_min_;
    const long landed = wrap_offset(static_cast<double>(engage_offset_));
    const long rtl_dups = dut_->rootp->milan_datapath__DOT__tdm_dup_cnt_w;
    const long rtl_skips = dut_->rootp->milan_datapath__DOT__tdm_skip_cnt_w;
    std::printf("  [i]  %s: engaged %+ld cycles from the crossing; tail: tick %ld cycles after the fsync edge, "
                "%+ld..%+ld (spread %ld); %ld repeats, %ld skips; SLIP_TDM %ld dups, %ld skips\n",
                sc.name.c_str(), landed, lock_ref_, lock_min_, lock_max_, spread, bench_.tally().dups,
                bench_.tally().skips, rtl_dups, rtl_skips);
    if (sc.placed != kUnplaced) {
        check_.that((n + "[V] the engagement close landed where the sweep placed it").c_str(),
                    engage_seen_ && std::labs(landed - sc.placed) <= kPlaceTolerance);
        placed_landed_.push_back(landed);
    }
    check_.that((n + "[V] the CRF lock held its phase (spread under a quarter frame)").c_str(),
                lock_seen_ && spread < static_cast<long>(kTickCycles / 4));
    check_.dec((n + "[C] slips while the CRF lock held").c_str(),
               static_cast<std::uint64_t>(bench_.tally().tail_slips), 0);
    check_.that((n + "[C] SLIP_TDM counted the columns' repeats and skips").c_str(),
                rtl_dups == bench_.tally().dups && rtl_skips == bench_.tally().skips);
}

//! Where the engagement close (the first after the CRF selection) lands
//! against its tick with the TDM clock unheld, once per plan: the origin
//! placed engagements are measured from (coherence_bench's PLACED CRF
//! ENGAGEMENTS).
long DatapathHarness::calibrate(const ClockPlan& plan) {
    const auto known = unheld_.find(plan.name);
    if (known != unheld_.end()) return known->second;
    const Scenario sc{"calibrate", plan, true, 0, 0, false, true, kUnplaced};
    restart(sc);
    select_crf("[calibrate] ");
    const long guard = cycle_ + 16 * 1100;
    while (!engage_seen_ && cycle_ < guard) cycle(1);
    check_.that(("[calibrate " + plan.name + "] [V] the engagement close was seen").c_str(), engage_seen_);
    std::printf("\n  [i]  calibration, %s: with the TDM clock unheld the first close under CRF lands %ld cycles "
                "after its tick\n", plan.name.c_str(), engage_offset_);
    unheld_[plan.name] = engage_offset_;
    return engage_offset_;
}

//! A placed sweep: calibrate its plan, run one brief scenario per offset,
//! then require the engagements to have covered the window.
void DatapathHarness::run_sweep(const Sweep& sw) {
    const long unheld = calibrate(sw.plan);
    std::printf("\n[%s] milan_datapath, CRF, %s, engagement placed every %ld cycles from %+ld to %+ld of the "
                "crossing, %ld columns each\n", sw.tag.c_str(), sw.plan.name.c_str(), sw.step, sw.lo, sw.hi,
                sw.frames);
    placed_landed_.clear();
    for (long off = sw.lo; off <= sw.hi; off += sw.step) {
        char name[40];
        std::snprintf(name, sizeof name, "%s%+ld", sw.tag.c_str(), off);
        run({name, sw.plan, true, delay_for(unheld, off), sw.frames, false, true, off});
    }
    grade_window(check_, sw, placed_landed_);
}

//! Over two beats each way at INTERNAL (a beat of a 1000 ppm plan is 1000
//! frames), then CRF locks an eighth of a frame apart.
std::vector<Scenario> scenarios() {
    std::vector<Scenario> list;
    list.push_back({"DP-INT-slow", ppm_plan(-1000), false, 0, 2'200, true, false, kUnplaced});
    list.push_back({"DP-INT-fast", ppm_plan(+1000), false, 0, 2'200, true, false, kUnplaced});
    for (int k = 0; k < 8; k++) {
        char name[24];
        std::snprintf(name, sizeof name, "DP-CRF-%d", k);
        list.push_back({name, true_plan(), true, k * 4167L / 8, 1'500, false, false, kUnplaced});
    }
    return list;
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vmilan_datapath> model;
    DatapathHarness harness(model.get());
    //! `--quick` runs the fixed scenarios alone and `--band` the placed sweep
    //! alone: the mutation arm's two datapath recipes
    const std::string arg = argc > 1 ? argv[1] : "";
    std::printf("=== milan_datapath 1x1 TDM8: AAF column coherence at the MAC (#617)%s ===\n",
                arg == "--quick" ? ", --quick: the placed sweep left out"
                : arg == "--band" ? ", --band: the placed sweep alone" : "");
    if (arg != "--band") {
        for (const Scenario& sc : scenarios()) harness.run(sc);
    }
    if (arg != "--quick") harness.run_sweep({"DP-band-true", true_plan(), -20, 4, 2, 1'500});
    return harness.report();
}
