/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for the timestamp_counter PPS alarm
 * (issue #260) - the metrology output that makes this device's gPTP accuracy
 * measurable against an external reference instead of read back from its own
 * servo.  Built with PPS_P = 1; the option-OFF arm is proven by the default
 * build in sim_main.cpp.
 *
 * WHAT IT HAS TO PROVE, and how the two are different claims:
 *
 *   ALIGNMENT  - each rising edge lands at or after its second boundary, and
 *                within ONE COUNTER INCREMENT of it.  That bound is the whole
 *                specification of the instrument: the accumulator is
 *                fractional, so it steps OVER the boundary and can never land
 *                on it, and the residue is the measurement's own error floor.
 *                MEASURED AT THE COMPARE, not at the pad: what is recorded is
 *                the time the comparator accepted, and pps_o is a register
 *                stage after that, so the pin is one more clock period late.
 *                That last term is a constant, which is why the harness holds
 *                the sample to one increment and leaves the pad to the bench.
 *
 *   NO DRIFT   - the boundary the k-th edge is measured against is
 *                base + k*1e9 EXACTLY, for at least ten pulses.  A design that
 *                re-armed at "now + 1e9" would also pass a period check
 *                between adjacent edges while walking away from the true grid
 *                by one residue per pulse, so the period is checked against
 *                the ABSOLUTE grid rather than against the previous edge.
 *
 * THE SIMULATED RATE IS NOT 8 ns/tick, deliberately.  One second at the
 * recommended 125 MHz PHC clock is 125 million ticks, and ten of those is not
 * a test anyone runs.  The harness free-runs at ~251.7 ns/tick instead, which
 * is (a) fast enough for twelve real seconds of PHC time and (b) a deliberately
 * ugly, non-dividing, FRACTIONAL step - 1e9 is not a multiple of it, so every
 * boundary is genuinely stepped over.  Nothing about the property under test
 * depends on the rate: the bound asserted is "one increment", computed from
 * whatever increment is being driven.
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "../../common/verilator_harness.hpp"

#include "Vtimestamp_counter.h"
#include "verilated.h"

#include <cstdint>
#include <cstdio>
#include <vector>

namespace {

//! PTP_INCR / PTP_ADJ are Q8.24 nanoseconds (8 integer ns + 24 fractional).
constexpr int FRAC = 24;

//! One PHC second, the exact amount the hardware target advances per pulse.
constexpr uint64_t PPS_PERIOD_NS = 1000000000ull;

//! The elaborated pulse width, in clock cycles. Kept short so the stretcher can be
//! measured exactly without dominating the run; the Makefile passes the same
//! number to Verilator, so a drift between the two reddens the width check
//! rather than being quietly absorbed.
constexpr uint32_t PPS_WIDTH_CYC = 1000;

//! Free-run step: 251 + 45/64 ns, i.e. 251.703125 ns. Integer-ugly on purpose.
constexpr uint32_t INCR_FAST = (251u << FRAC) | (45u << (FRAC - 6));
//! Ceiling of the per-tick increment in whole ns - the "one increment" bound.
constexpr uint64_t INCR_FAST_NS_CEIL = 252;

//! Ticks per PHC second at INCR_FAST, rounded up: the free-run budget per pulse.
constexpr long TICKS_PER_SECOND_FAST =
    static_cast<long>(PPS_PERIOD_NS / INCR_FAST_NS_CEIL) + 2;

//! Pulses measured. The acceptance asks for at least ten.
constexpr int PULSES = 12;

//! Where the grid is armed: a real TAI-shaped multiple of 1e9, far from zero so
//! nothing can pass by accident on a counter that has only just left reset.
constexpr uint64_t BASE_TARGET = 1758000000ull * PPS_PERIOD_NS;

//! One observed pulse.
struct Edge {
    uint64_t ns = 0;        //!< integer-ns time the comparator fired at
    uint64_t target = 0;    //!< live target read back right after the edge
    long tick = 0;          //!< ticks since the arm strobe
    long width = 0;         //!< ticks the output stayed high
};

//! Drives the DUT and records PPS edges. Deliberately leaner than the PHC
//! equivalence harness next door: this one asserts about time, not about the
//! accumulator, so it carries no software model of the accumulator.
class PpsDriver {
 public:
    explicit PpsDriver(Vtimestamp_counter* dut) : dut_(dut) {}

    //! One clock. Samples timestamp_out BEFORE the edge, because that is the
    //! value the comparator compared: pps_o rising in cycle N reports a hit on
    //! the time visible during cycle N, not the time after the step.
    void tick(uint32_t incr, int32_t adj, bool pps_en) {
        const uint64_t t_before = dut_->timestamp_out;
        const bool was_high = dut_->pps_o != 0;

        dut_->enable_i = 1;
        dut_->incr_i = incr;
        dut_->adj_i = static_cast<uint32_t>(adj);
        dut_->pps_enable_i = pps_en ? 1 : 0;
        dut_->cmd_load_i = 0;
        dut_->cmd_adjust_i = 0;
        dut_->cmd_snapshot_i = 0;
        dut_->pps_arm_i = 0;
        step();

        const bool now_high = dut_->pps_o != 0;
        ++ticks_;
        if (now_high && !was_high) {
            Edge e;
            e.ns = t_before;
            e.target = dut_->pps_target_ns_o;
            e.tick = ticks_;
            edges_.push_back(e);
            high_since_ = ticks_;
        } else if (!now_high && was_high && !edges_.empty()) {
            edges_.back().width = ticks_ - high_since_;
        }
    }

    //! settime: load an absolute PHC time, clearing the fraction.
    void settime(uint64_t tod) {
        dut_->enable_i = 1;
        dut_->incr_i = 0;
        dut_->adj_i = 0;
        dut_->tod_wr_i = tod;
        dut_->cmd_load_i = 1;
        dut_->cmd_adjust_i = 0;
        dut_->cmd_snapshot_i = 0;
        dut_->pps_arm_i = 0;
        step();
        dut_->cmd_load_i = 0;
        ++ticks_;
    }

    //! Arm the alarm at an absolute target and restart the tick origin.
    void arm(uint64_t target, bool pps_en) {
        dut_->enable_i = 1;
        dut_->incr_i = 0;
        dut_->adj_i = 0;
        dut_->cmd_load_i = 0;
        dut_->cmd_adjust_i = 0;
        dut_->cmd_snapshot_i = 0;
        dut_->pps_enable_i = pps_en ? 1 : 0;
        dut_->pps_target_ns_i = target;
        dut_->pps_arm_i = 1;
        step();
        dut_->pps_arm_i = 0;
        ticks_ = 0;
        edges_.clear();
    }

    void reset(int n) {
        dut_->resetn = 0;
        for (int i = 0; i < n; i++) {
            dut_->enable_i = 0;
            dut_->incr_i = 0;
            dut_->adj_i = 0;
            dut_->tod_wr_i = 0;
            dut_->offset_i = 0;
            dut_->cmd_load_i = 0;
            dut_->cmd_adjust_i = 0;
            dut_->cmd_snapshot_i = 0;
            dut_->pps_enable_i = 0;
            dut_->pps_target_ns_i = 0;
            dut_->pps_arm_i = 0;
            step();
        }
        dut_->resetn = 1;
        ticks_ = 0;
        edges_.clear();
    }

    //! Free-run until at least `want` edges have been seen, or the budget runs out.
    bool run_until(int want, uint32_t incr, int32_t adj, long budget) {
        for (long i = 0; i < budget; i++) {
            if (static_cast<int>(edges_.size()) >= want) return true;
            tick(incr, adj, /*pps_en=*/true);
        }
        return static_cast<int>(edges_.size()) >= want;
    }

    const std::vector<Edge>& edges() const { return edges_; }
    //! The live target the hardware holds right now.
    uint64_t live_target() const { return dut_->pps_target_ns_o; }
    bool pin_high() const { return dut_->pps_o != 0; }

 private:
    void step() {
        dut_->clk = 0;
        dut_->eval();
        dut_->clk = 1;
        dut_->eval();
    }

    Vtimestamp_counter* dut_;
    std::vector<Edge> edges_;
    long ticks_ = 0;
    long high_since_ = 0;
};

//! Run the grid and return the per-pulse tick indices, so a perturbed rate can
//! be compared against an unperturbed one without duplicating the setup.
std::vector<long> grid_run(PpsDriver& drv, int32_t adj, int pulses) {
    drv.reset(4);
    drv.settime(BASE_TARGET - PPS_PERIOD_NS / 4);
    drv.arm(BASE_TARGET, /*pps_en=*/true);
    drv.run_until(pulses, INCR_FAST, adj, TICKS_PER_SECOND_FAST * (pulses + 2));
    std::vector<long> ticks;
    for (const Edge& e : drv.edges()) ticks.push_back(e.tick);
    return ticks;
}

// ---- Scenario 1: alignment and an exact, non-accumulating 1e9 grid ----
void grid_is_exact(PpsDriver& drv, milan::tb::Checker& check) {
    drv.reset(4);
    //! Start a quarter-second short of the armed boundary so the first hit is
    //! a real free-run arrival, not an immediate compare at t = 0.
    drv.settime(BASE_TARGET - PPS_PERIOD_NS / 4);
    drv.arm(BASE_TARGET, /*pps_en=*/true);

    //! One extra pulse, so every one of the twelve measured has a COMPLETED
    //! width - a pulse still high at the end of the run has no width to check.
    const bool got = drv.run_until(PULSES + 1, INCR_FAST, 0,
                                   TICKS_PER_SECOND_FAST * (PULSES + 2));
    if (!check.that("PPS: twelve pulses observed within the tick budget", got)) return;

    uint64_t worst = 0;
    for (int k = 0; k < PULSES; k++) {
        const Edge& e = drv.edges()[static_cast<size_t>(k)];
        //! THE GRID, absolute: pulse k belongs to base + k*1e9 and to nothing
        //! else. Checking against the previous edge instead would accept a
        //! "now + 1e9" re-arm, which is the defect this register shape exists
        //! to make impossible.
        const uint64_t boundary = BASE_TARGET + static_cast<uint64_t>(k) * PPS_PERIOD_NS;
        const bool not_early = e.ns >= boundary;
        const uint64_t over = not_early ? e.ns - boundary : 0;
        if (over > worst) worst = over;
        check.that("PPS edge is at or after its second boundary", not_early);
        check.that("PPS edge is within ONE counter increment of the boundary",
                   not_early && over < INCR_FAST_NS_CEIL);
        //! The hardware target advanced by exactly one second and nothing else
        //! touched it - the readable-target half of the acceptance.
        check.dec("PPS target advanced by exactly 1e9",
                  e.target, boundary + PPS_PERIOD_NS);
    }
    //! Explicit no-drift statement: the residue of the LAST pulse is bounded by
    //! the same single increment as the first. A per-pulse accumulation would
    //! have reached PULSES * residue by here.
    const uint64_t first_over = drv.edges()[0].ns - BASE_TARGET;
    const uint64_t last_over = drv.edges()[PULSES - 1].ns -
        (BASE_TARGET + static_cast<uint64_t>(PULSES - 1) * PPS_PERIOD_NS);
    check.that("PPS residue does not accumulate over 12 pulses",
               last_over < INCR_FAST_NS_CEIL);
    std::printf("  [info] PPS residues: first=%llu ns  last=%llu ns  worst=%llu ns"
                "  (bound = one increment = %llu ns)\n",
                static_cast<unsigned long long>(first_over),
                static_cast<unsigned long long>(last_over),
                static_cast<unsigned long long>(worst),
                static_cast<unsigned long long>(INCR_FAST_NS_CEIL));
}

// ---- Scenario 2: the stretcher is exactly PPS_WIDTH_CYC cycles wide ----
void pulse_width_is_the_parameter(PpsDriver& drv, milan::tb::Checker& check) {
    drv.reset(4);
    drv.settime(BASE_TARGET - PPS_PERIOD_NS / 4);
    drv.arm(BASE_TARGET, /*pps_en=*/true);
    drv.run_until(2, INCR_FAST, 0, TICKS_PER_SECOND_FAST * 3);
    if (drv.edges().size() < 2) {
        check.fail("PPS: two pulses needed to measure a completed width");
        return;
    }
    check.dec("PPS pulse is exactly PPS_WIDTH_CYC_P cycles wide",
              static_cast<uint64_t>(drv.edges()[0].width), PPS_WIDTH_CYC);
}

// ---- Scenario 3: NEGATIVE CONTROL (a) - the addend moves the edge ----
// A fine-frequency addend is what a servo writes. If the PPS did not actually
// consume the disciplined clock - if it were free-running off something else,
// or if the comparator were bypassed - perturbing that addend would leave the
// pulses where they were. Two facts are asserted, and they are different:
// the edge MOVES in ticks (the clock really is faster), and it does NOT move
// in nanoseconds (the grid is still an exact 1e9 in PHC time).
void addend_moves_the_edge(PpsDriver& drv, milan::tb::Checker& check) {
    const std::vector<long> base = grid_run(drv, 0, PULSES);
    //! +2.44e-4 ns/tick: a genuinely FINE addend - four ten-thousandths of a
    //! nanosecond, 1/1000th of a Q8.24 integer ns - which is nonetheless worth
    //! about a microsecond of PHC time per second and therefore several ticks.
    const int32_t fine = 1 << 12;
    const std::vector<long> fast = grid_run(drv, fine, PULSES);

    if (base.size() < PULSES || fast.size() < PULSES) {
        check.fail("PPS negative control: both runs need twelve pulses");
        return;
    }
    check.that("perturbing the fractional addend moves the PPS edge",
               fast[PULSES - 1] != base[PULSES - 1]);
    check.that("a positive addend makes the clock reach the boundary sooner",
               fast[PULSES - 1] < base[PULSES - 1]);
    //! ... and the grid in PHC nanoseconds is untouched, because the target
    //! advances in ns and not in ticks.
    const uint64_t boundary =
        BASE_TARGET + static_cast<uint64_t>(PULSES - 1) * PPS_PERIOD_NS;
    check.that("the perturbed run still lands on the same ns boundary",
               drv.edges()[PULSES - 1].ns >= boundary &&
               drv.edges()[PULSES - 1].ns - boundary < INCR_FAST_NS_CEIL);
    std::printf("  [info] pulse 12 at tick %ld (adj=0) vs %ld (adj=+%d/2^24 ns):"
                " moved %ld ticks\n",
                base[PULSES - 1], fast[PULSES - 1], fine,
                base[PULSES - 1] - fast[PULSES - 1]);
}

// ---- Scenario 4: the runtime enable is separate from the build ----
void runtime_enable_gates_the_pin(PpsDriver& drv, milan::tb::Checker& check) {
    drv.reset(4);
    drv.settime(BASE_TARGET - PPS_PERIOD_NS / 4);
    drv.arm(BASE_TARGET, /*pps_en=*/false);
    for (long i = 0; i < TICKS_PER_SECOND_FAST; i++)
        drv.tick(INCR_FAST, 0, /*pps_en=*/false);
    check.dec("pps_enable_i = 0: no pulse across the armed boundary",
              static_cast<uint64_t>(drv.edges().size()), 0);
    check.that("pps_enable_i = 0: the pin stays low", !drv.pin_high());
    check.dec("pps_enable_i = 0: the target does not advance",
              drv.live_target(), BASE_TARGET);
}

// ---- Scenario 5: arming reloads the grid and drops a pulse in flight ----
void arming_reloads_the_grid(PpsDriver& drv, milan::tb::Checker& check) {
    drv.reset(4);
    drv.settime(BASE_TARGET - PPS_PERIOD_NS / 4);
    drv.arm(BASE_TARGET, /*pps_en=*/true);
    drv.run_until(1, INCR_FAST, 0, TICKS_PER_SECOND_FAST * 2);
    check.that("a pulse is in flight before the re-arm",
               !drv.edges().empty() && drv.pin_high());
    //! Re-arm two seconds further out while that pulse is still stretching.
    const uint64_t moved = BASE_TARGET + 2 * PPS_PERIOD_NS;
    drv.arm(moved, /*pps_en=*/true);
    check.dec("arming reloads the live target", drv.live_target(), moved);
    check.that("arming clears the pulse in flight", !drv.pin_high());
    drv.run_until(1, INCR_FAST, 0, TICKS_PER_SECOND_FAST * 3);
    if (drv.edges().empty()) {
        check.fail("PPS: no pulse after re-arming");
        return;
    }
    check.that("the first edge after an arm is the newly armed boundary",
               drv.edges()[0].ns >= moved &&
               drv.edges()[0].ns - moved < INCR_FAST_NS_CEIL);
}

// ---- Scenario 6: a target armed in the past converges, then is exact ----
void a_stale_target_catches_up(PpsDriver& drv, milan::tb::Checker& check) {
    drv.reset(4);
    drv.settime(BASE_TARGET + 3 * PPS_PERIOD_NS);
    //! Three seconds behind the live time: defined behaviour, not undefined -
    //! the comparator hits every tick and the target advances 1e9 per tick
    //! until it passes the clock, which takes four ticks and no more.
    drv.arm(BASE_TARGET, /*pps_en=*/true);
    drv.run_until(2, INCR_FAST, 0, TICKS_PER_SECOND_FAST * 3);
    if (drv.edges().size() < 2) {
        check.fail("PPS: a stale target must still reach the grid");
        return;
    }
    const uint64_t a = drv.edges()[0].ns;
    const uint64_t b = drv.edges()[1].ns;
    check.that("after catching up, the next period is one second",
               b > a && (b - a) >= PPS_PERIOD_NS - INCR_FAST_NS_CEIL &&
               (b - a) <= PPS_PERIOD_NS + INCR_FAST_NS_CEIL);
    check.that("the recovered grid is a multiple of 1e9 from the armed base",
               (drv.edges()[1].target - BASE_TARGET) % PPS_PERIOD_NS == 0);
}

// ---- Scenario 7: NEGATIVE CONTROL (b) - enable alone must not pulse ----
// THE RACE THIS EXISTS FOR.  Software's normal sequence is one word into
// PTP_PPS_CTRL carrying arm in [1] and enable in [0].  Those two bits reach
// this counter by DIFFERENT crossings in ptp_csr_sync: enable rides a 2-flop
// synchroniser, arm rides a source toggle plus a 3-flop edge detect plus a
// delay, so enable lands first by a couple of ts_clk edges and the gap is a
// property of the CDC shapes, not of any clock ratio.  If the comparator were
// gated on enable alone it would spend that gap comparing against the RESET
// target - zero, which every live time is >= - and put a runt pulse on the pin
// before the arm arrived to clear it.  The first edge after power-up would be
// noise on a metrology output.  So: enable without arm is SILENT, and the
// target register is not advanced by a phantom hit either.
void enable_alone_never_pulses(PpsDriver& drv, milan::tb::Checker& check) {
    //! Comfortably more than the ~2 ts_clk edges the two crossings differ by.
    constexpr int ENABLE_LEAD = 8;

    //! (a) Straight out of reset, the case the shipping SoC actually hits:
    //! the target register still holds its reset zero and the live time has
    //! only just started ticking, so a `>=` against zero is true immediately.
    drv.reset(4);
    for (int i = 0; i < ENABLE_LEAD; i++) drv.tick(INCR_FAST, 0, /*pps_en=*/true);
    check.dec("enable before arm, from reset: no edge",
              static_cast<uint64_t>(drv.edges().size()), 0);
    check.that("enable before arm, from reset: the pin stays low", !drv.pin_high());
    check.dec("enable before arm, from reset: the target is not advanced",
              drv.live_target(), 0);

    //! (b) The same race with a real time-of-day loaded, which is how the
    //! sequence runs on a board: settime, write the target, then the one word.
    drv.reset(4);
    drv.settime(BASE_TARGET - PPS_PERIOD_NS / 4);
    for (int i = 0; i < ENABLE_LEAD; i++) drv.tick(INCR_FAST, 0, /*pps_en=*/true);
    check.dec("enable before arm, clock running: no edge",
              static_cast<uint64_t>(drv.edges().size()), 0);
    check.that("enable before arm, clock running: the pin stays low", !drv.pin_high());
    check.dec("enable before arm, clock running: the target is not advanced",
              drv.live_target(), 0);

    //! ... and once the arm does land, the pin behaves exactly as before: the
    //! FIRST edge is the armed boundary, so gating the comparator delayed
    //! nothing that was supposed to happen.
    drv.arm(BASE_TARGET, /*pps_en=*/true);
    drv.run_until(1, INCR_FAST, 0, TICKS_PER_SECOND_FAST * 2);
    if (drv.edges().empty()) {
        check.fail("PPS: no pulse after the delayed arm");
        return;
    }
    check.that("the first edge after a late arm is the armed boundary",
               drv.edges()[0].ns >= BASE_TARGET &&
               drv.edges()[0].ns - BASE_TARGET < INCR_FAST_NS_CEIL);
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    //! The banner says "comparator", not "alarm ("; the test-evidence gate
    //! reads a literal `alarm (` as the POSIX call and would count this
    //! cycle-driven harness as host-wall-clock dependent.
    std::printf("== timestamp_counter PPS comparator (PPS_P=1, width=%u cycles,"
                " free-run %u/2^%d ns per tick) ==\n",
                PPS_WIDTH_CYC, INCR_FAST, FRAC);

    const milan::tb::Model<Vtimestamp_counter> model;
    PpsDriver drv(model.get());
    milan::tb::Checker check{"ptp_pps"};

    grid_is_exact(drv, check);
    pulse_width_is_the_parameter(drv, check);
    addend_moves_the_edge(drv, check);
    runtime_enable_gates_the_pin(drv, check);
    arming_reloads_the_grid(drv, check);
    a_stale_target_catches_up(drv, check);
    enable_alone_never_pulses(drv, check);

    std::printf("--------------------------------------------------------------\n");
    return check.report();
}
