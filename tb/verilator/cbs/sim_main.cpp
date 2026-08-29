/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for credit_based_shaper.sv (runtime-config).
 *
 * Checks, every cycle:
 *   (A) DUT.credit          == FixedPointRef.credit          (bit-exact)
 *   (B) DUT.allow_transmit  == FixedPointRef.allow_transmit
 *   (C) DUT.slope terms     == FixedPointRef slope terms
 *   (D) |DUT.credit - IdealRef.credit| <= PRECISION_TOL_BYTES (quantization)
 * plus directed behavioural assertions (idle saturation, transmit drain,
 * empty-queue reset, negative-credit recovery, strict-priority bypass,
 * back-pressure accrual, live reconfiguration) that encode the 802.1Qav intent.
 *
 * Exit code 0 = all checks pass, non-zero = failure (CI friendly).
 */

#include "Vcbs_ver_wrap.h"
#include "verilated.h"
#include "cbs_ref_model.h"

#include <cstdio>
#include <cstdint>
#include <cmath>
#include <random>
#include <string>

// Sign-extend a Verilator-packed 48-bit value to int64.
static int64_t sx48(uint64_t v) {
    v &= (((uint64_t)1 << 48) - 1);
    if (v & ((uint64_t)1 << 47)) v |= ~((((uint64_t)1 << 48) - 1));
    return (int64_t)v;
}

static const double PRECISION_TOL_BYTES = 1.0; // fixed-point error budget vs ideal

// Convenience: build a CbsInputs with status + config in one call.
static CbsInputs mk(bool resetn, bool qhd, bool istx, bool is1g, bool isg,
                    uint16_t bytes, bool shaped = true, int32_t idle = 500000000,
                    int32_t hi = 761, int32_t lo = -761, bool tlast = false) {
    CbsInputs in;
    in.resetn = resetn; in.queue_has_data = qhd; in.is_transmitting = istx;
    in.is_1g = is1g; in.is_granted = isg; in.bytes_sent = bytes;
    in.shaped = shaped; in.idle_slope_bps = idle; in.hi_credit_bytes = hi; in.lo_credit_bytes = lo;
    in.tlast = tlast;
    return in;
}

struct Harness {
    Vcbs_ver_wrap* dut;
    FixedPointRef  fref;
    IdealRef       iref;
    CbsConfig      cfg;

    long checks = 0, fails = 0;
    double max_ideal_err = 0.0;

    Harness(Vcbs_ver_wrap* d, const CbsConfig& c)
        : dut(d), fref(c), iref(c), cfg(c) {}

    void posedge() {
        dut->clk = 0; dut->eval();
        dut->clk = 1; dut->eval();
    }

    // Drive one cycle with the given inputs; advance refs; check.
    void cycle(const CbsInputs& in, const char* tag) {
        dut->resetn            = in.resetn;
        dut->queue_has_data_i  = in.queue_has_data;
        dut->is_transmitting_i = in.is_transmitting;
        dut->is_1g_i           = in.is_1g;
        dut->is_granted_i      = in.is_granted;
        dut->bytes_sent_i      = in.bytes_sent;
        dut->tlast_i           = in.tlast;
        dut->shaped_i          = in.shaped;
        dut->idle_slope_bps_i      = (uint32_t)in.idle_slope_bps;
        dut->hi_credit_bytes_i       = (uint32_t)in.hi_credit_bytes;
        dut->lo_credit_bytes_i       = (uint32_t)in.lo_credit_bytes;
        posedge();

        fref.step(in);
        iref.step(in);

        int64_t dut_credit = sx48(dut->dbg_credit);
        int64_t dut_isc    = sx48(dut->dbg_idle_slope_per_cycle);
        int64_t dut_ssb    = sx48(dut->dbg_send_slope_per_byte);

        // (C) slope registers must track the SlopeEngineRef mirror EVERY cycle,
        // including engine warm-up and reconfiguration transitions (this pins
        // the RTL engine cadence bit-for-bit, a stronger check than the old
        // instant-combinational compare).
        if (in.resetn) {
            expect_eq(dut_isc, fref.isc_reg(), tag, "idle_slope_per_cycle_r");
            expect_eq(dut_ssb, fref.ssb_reg(), tag, "send_slope_per_byte_r");
        }
        // (A) credit bit-exact
        expect_eq(dut_credit, fref.credit_q16(), tag, "credit");
        // (A') REQ-CBS-07 wire-time debt bit-exact, every cycle
        if (in.resetn)
            expect_eq((int64_t)dut->dbg_wire_debt, fref.wire_debt_q16(),
                      tag, "wire_debt");
        // (B) allow_transmit
        expect_eq((int64_t)(dut->allow_transmit_o & 1), (int64_t)fref.allow_transmit(), tag, "allow");
        // (D) precision vs ideal
        double err = std::fabs(fref.credit_bytes() - iref.credit_bytes());
        if (err > max_ideal_err) max_ideal_err = err;
        if (err > PRECISION_TOL_BYTES) {
            fail(tag, "precision", (int64_t)llround(err * 65536), 0);
        }
        checks++;
    }

    void expect_eq(int64_t got, int64_t exp, const char* tag, const char* what) {
        if (got != exp) fail(tag, what, got, exp);
    }
    void fail(const char* tag, const char* what, int64_t got, int64_t exp) {
        if (fails < 20)
            printf("  [FAIL] %-22s %-22s got=%lld exp=%lld\n", tag, what,
                   (long long)got, (long long)exp);
        fails++;
    }

    void do_reset(int n) {
        for (int i = 0; i < n; i++) cycle(mk(false,false,false,true,false,0), "reset");
    }
};

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    CbsConfig cfg;                       // only clk_freq_hz is a compile-time param now
    Vcbs_ver_wrap* dut = new Vcbs_ver_wrap;
    Harness h(dut, cfg);

    // The DUT carries no queue index: this is a SLOPE test, not a queue test.
    // 500 Mbit/s is 50 % of 1G - it was q0's share before the 0x0011->0x0014
    // renumbering made q0 best effort and SR class A q4 (450 Mbit/s). See
    // README.md "Configuration".
    printf("== CBS verification harness (runtime config; default slope "
           "@1G idleSlope=500Mbps HI=761 LO=-761 clk=%lldMHz) ==\n",
           (long long)(cfg.clk_freq_hz/1000000));

    h.do_reset(4);

    // ---- Scenario 1: idle accumulation to hiCredit ----
    {
        for (int i = 0; i < 3000; i++) h.cycle(mk(true,true,false,true,false,0), "idle_accum");
        double c = h.fref.credit_bytes();
        bool ok = std::fabs(c - 761.0) < 1.0 && dut->allow_transmit_o;
        printf("  [%s] idle saturates at HI: credit=%.3f (HI=761) allow=%d\n",
               ok ? "PASS" : "FAIL", c, dut->allow_transmit_o);
        if (!ok) h.fails++;
        // engine convergence: after a stable config the committed slope regs
        // must equal the SystemVerilog '/' results exactly
        h.expect_eq(h.fref.isc_reg(), h.fref.idle_slope_per_cycle(true, 500000000), "s1", "isc_converged");
        h.expect_eq(h.fref.ssb_reg(), h.fref.send_slope_per_byte(true, 500000000),  "s1", "ssb_converged");
    }

    // ---- Scenario 2: transmit drain to loCredit ----
    {
        for (int i = 0; i < 1000; i++) h.cycle(mk(true,true,true,true,true,8), "tx_drain");
        double c = h.fref.credit_bytes();
        bool ok = std::fabs(c - (-761.0)) < 1.0 && !dut->allow_transmit_o;
        printf("  [%s] tx drains to LO: credit=%.3f (LO=-761) allow=%d\n",
               ok ? "PASS" : "FAIL", c, dut->allow_transmit_o);
        if (!ok) h.fails++;
    }

    // ---- Scenario 3: empty-queue reset-to-zero ----
    {
        h.do_reset(4);
        for (int i = 0; i < 500; i++) h.cycle(mk(true,true,false,true,false,0), "pre_empty_accum");
        for (int i = 0; i < 5;   i++) h.cycle(mk(true,false,false,true,false,0), "empty_reset");
        double c = h.fref.credit_bytes();
        bool ok = std::fabs(c) < 1e-9;
        printf("  [%s] empty & credit>0 -> credit=%.3f (expect 0)\n", ok ? "PASS" : "FAIL", c);
        if (!ok) h.fails++;
    }

    // ---- Scenario 4: negative-credit recovery toward zero when empty ----
    {
        h.do_reset(4);
        for (int i = 0; i < 200; i++) h.cycle(mk(true,true,true,true,true,8), "pre_neg_tx");
        double c_neg = h.fref.credit_bytes();
        for (int i = 0; i < 4000; i++) h.cycle(mk(true,false,false,true,false,0), "neg_recover");
        double c = h.fref.credit_bytes();
        bool ok = c_neg < 0.0 && std::fabs(c) < 1e-9;
        printf("  [%s] negative(%.2f) recovers to credit=%.3f (expect 0)\n",
               ok ? "PASS" : "FAIL", c_neg, c);
        if (!ok) h.fails++;
    }

    // ---- Scenario 5: randomized stress (DUT must track FixedPointRef exactly) ----
    // Beats now carry random tlast marks too, so the REQ-CBS-07 frame byte
    // counter, the per-frame overhead charge and the min-frame pad all churn
    // against the model under the same randomness as the credit arms.
    {
        std::mt19937 rng(0xC0FFEE);
        std::uniform_int_distribution<int> bit(0, 1);
        std::uniform_int_distribution<int> bytes(0, 8);
        std::uniform_int_distribution<int> oct(0, 7);
        long start_fails = h.fails;
        for (int i = 0; i < 50000; i++) {
            bool qhd  = bit(rng);
            bool istx = bit(rng) && qhd;
            bool isg  = istx || bit(rng);
            uint16_t b = istx ? (uint16_t)bytes(rng) : 0;
            bool tl   = istx && (oct(rng) == 0);   // ~1 in 8 beats ends a frame
            h.cycle(mk(true, qhd, istx, true, isg, b, true, 500000000,
                       761, -761, tl), "random");
        }
        printf("  [%s] randomized 50000 cycles (frames + tlast): DUT tracks "
               "fixed-point ref exactly\n",
               (h.fails == start_fails) ? "PASS" : "FAIL");
    }

    // ---- Scenario 6: 100M link-rate config ----
    {
        h.do_reset(4);
        for (int i = 0; i < 20000; i++) h.cycle(mk(true,true,false,false,false,0,true,50000000), "idle_100m");
        h.expect_eq(h.fref.isc_reg(), h.fref.idle_slope_per_cycle(false, 50000000), "s6", "isc_converged_100m");
        h.expect_eq(h.fref.ssb_reg(), h.fref.send_slope_per_byte(false, 50000000),  "s6", "ssb_converged_100m");
        printf("  [INFO] 100M idle_slope_per_cycle=%lld send_slope_per_byte=%lld\n",
               (long long)h.fref.idle_slope_per_cycle(false, 50000000),
               (long long)h.fref.send_slope_per_byte(false, 50000000));
    }

    // ---- Scenario 7: strict-priority bypass (shaped=0, REQ-CBS-02) ----
    // Even while "transmitting" a lot, an unshaped queue must stay eligible and
    // keep credit parked at 0 (no shaping).
    {
        h.do_reset(4);
        long start_fails = h.fails;
        bool always_allow = true;
        for (int i = 0; i < 500; i++) {
            h.cycle(mk(true,true,true,true,true,8, /*shaped=*/false), "strict_prio");
            if (!(dut->allow_transmit_o & 1)) always_allow = false;
        }
        double c = h.fref.credit_bytes();
        bool ok = always_allow && std::fabs(c) < 1e-9 && (h.fails == start_fails);
        printf("  [%s] strict-priority (shaped=0): allow always high, credit=%.3f (expect 0)\n",
               ok ? "PASS" : "FAIL", c);
        if (!ok) h.fails++;
    }

    // ---- Scenario 8: back-pressure accrual (REQ-CBS-04) ----
    // Granted but downstream not ready (is_granted=1, is_transmitting=0): credit
    // must keep accruing at idleSlope up to hiCredit, not freeze.
    {
        h.do_reset(4);
        for (int i = 0; i < 3000; i++) h.cycle(mk(true,true,false,true,/*isg=*/true,0), "backpressure");
        double c = h.fref.credit_bytes();
        bool ok = std::fabs(c - 761.0) < 1.0;
        printf("  [%s] granted+backpressure accrues to HI: credit=%.3f (expect ~761)\n",
               ok ? "PASS" : "FAIL", c);
        if (!ok) h.fails++;
    }

    // ---- Scenario 9: live reconfiguration (REQ-CBS-01) ----
    // Reprogram idleSlope/hi/lo mid-run (as `tc cbs` would): DUT must track the
    // reference exactly across the change and saturate at the new hiCredit.
    {
        h.do_reset(4);
        long start_fails = h.fails;
        for (int i = 0; i < 2000; i++)                              // config A: 500M, HI 761
            h.cycle(mk(true,true,false,true,false,0,true,500000000,761,-761), "reconf_A");
        for (int i = 0; i < 3000; i++)                              // config B: 200M, HI 304
            h.cycle(mk(true,true,false,true,false,0,true,200000000,304,-1217), "reconf_B");
        double c = h.fref.credit_bytes();
        bool ok = std::fabs(c - 304.0) < 1.0 && (h.fails == start_fails);
        printf("  [%s] live reconfig 500M/HI761 -> 200M/HI304: credit=%.3f (expect ~304)\n",
               ok ? "PASS" : "FAIL", c);
        if (!ok) h.fails++;
        h.expect_eq(h.fref.isc_reg(), h.fref.idle_slope_per_cycle(true, 200000000), "s9", "isc_converged_reconf");
        h.expect_eq(h.fref.ssb_reg(), h.fref.send_slope_per_byte(true, 200000000),  "s9", "ssb_converged_reconf");
    }

    // ---- REQ-CBS-05: no stale allow_transmit into arbitration ----
    // 802.1Qav evaluates transmissionAllowed on the CURRENT credit. The old
    // RTL registered (credit >= 0) into a second flop, so the arbiter's view
    // lagged the credit by a cycle and could start a frame on a queue whose
    // credit had already crossed to negative. Two directed properties, driven
    // straight off the DUT (not via the reference model, so a model+RTL
    // change made together cannot hide the regression):
    //   P1 - while shaped, allow_transmit_o == (credit >= 0) EVERY cycle
    //   P2 - the deassert edge lands on the SAME cycle credit goes negative
    {
        long f0 = h.fails;
        h.do_reset(4);
        // build positive credit, then burn it down with a long transmission
        for (int i = 0; i < 400; i++)
            h.cycle(mk(true, true, false, true, true, 0), "cbs05 accrue");

        long p1_bad = 0, lag = -1, seen_neg = -1, seen_deassert = -1;
        int64_t prev_credit = sx48(h.dut->dbg_credit);
        for (int i = 0; i < 900; i++) {
            h.cycle(mk(true, true, true, true, true, 8), "cbs05 drain");
            int64_t c   = sx48(h.dut->dbg_credit);
            int      a  = h.dut->allow_transmit_o & 1;
            // P1: shaped has been high for many cycles, so the registered
            // `shaped` bit is 1 and the output is exactly the credit sign
            if (a != (c >= 0 ? 1 : 0)) p1_bad++;
            // P2: record the first cycle credit is negative and the first
            // cycle the output deasserts; they must be the same cycle
            if (seen_neg < 0 && c < 0)   seen_neg = i;
            if (seen_deassert < 0 && !a) seen_deassert = i;
            if (seen_neg >= 0 && seen_deassert >= 0) { lag = seen_deassert - seen_neg; break; }
            prev_credit = c;
        }
        (void)prev_credit;
        h.expect_eq(p1_bad, 0, "cbs05", "allow_transmit == credit sign every cycle");
        h.expect_eq((int64_t)lag, 0, "cbs05", "deassert lag cycles behind credit<0");
        if (seen_neg < 0) { printf("  [FAIL] cbs05: credit never went negative (test is vacuous)\n"); h.fails++; }
        printf("  [%s] REQ-CBS-05 allow_transmit is not stale (lag %ld cycle(s), %ld P1 misses)\n",
               (h.fails == f0) ? "PASS" : "FAIL", lag, p1_bad);
    }

    // ---- REQ-CBS-05 residual: the credit datapath input pipeline ----
    // The skew that REMAINS is 2 cycles from an accepted beat to its debit
    // (traffic_shaping_core registers is_transmitting/bytes_sent, stage1
    // registers send_delta). Pin the number so it cannot drift silently and a
    // future collapse has something to beat. Measured from the CBS port here,
    // which sees the second of those two registers, so the port-level lag is 1
    // and the datapath total is 2.
    {
        long f0 = h.fails;
        h.do_reset(4);
        for (int i = 0; i < 300; i++)
            h.cycle(mk(true, true, false, true, true, 0), "cbs05r settle");
        int64_t before = sx48(h.dut->dbg_credit);
        // exactly ONE transmitting beat, then idle-but-granted cycles
        h.cycle(mk(true, true, true, true, true, 8), "cbs05r beat");
        int64_t c1 = sx48(h.dut->dbg_credit);
        h.cycle(mk(true, true, false, true, true, 0), "cbs05r +1");
        int64_t c2 = sx48(h.dut->dbg_credit);
        // the send-slope debit must NOT have landed on the beat cycle itself
        h.expect_eq((int64_t)(c1 != before && c1 < before ? 1 : 0), 0,
                    "cbs05r", "debit must not land on the beat cycle (port lag 1)");
        // and it must have landed exactly one cycle later
        h.expect_eq((int64_t)(c2 < c1 ? 1 : 0), 1,
                    "cbs05r", "debit lands one cycle after the beat");
        printf("  [%s] REQ-CBS-05 residual input-pipeline lag pinned at 1 CBS-port cycle\n",
               (h.fails == f0) ? "PASS" : "FAIL");
    }

    // ---- REQ-CBS-06: slope fixed-point rounding + measured residual ----
    // The serial divider used to TRUNCATE toward zero. That is not a symmetric
    // error: idleSlope (positive) accrued slightly slow, which is harmless, but
    // sendSlope is NEGATIVE, so truncating its magnitude DOWN debited a
    // transmitting queue less than the standard says - it kept credit it had
    // spent. With idleSlope runtime-programmable (REQ-CBS-01) the residual
    // stopped being a compile-time constant, so the engine now rounds to
    // nearest (ties away from zero).
    {
        long f0 = h.fails;
        // A config where round and truncate DISAGREE on BOTH quotients, so the
        // check fails against the pre-2026-07-26 RTL rather than being vacuous:
        //   idleSlope 1007081 @ 100 MHz: idle_slope_per_cycle trunc 82 -> 83
        //                                send_slope_per_byte  trunc -65469 -> -65470
        const int32_t IDLE_R = 1007081;
        h.do_reset(4);
        for (int i = 0; i < 400; i++)   // > 2 engine passes so the config commits
            h.cycle(mk(true, false, false, true, false, 0, true, IDLE_R), "cbs06 warm");
        int64_t isc = sx48(h.dut->dbg_idle_slope_per_cycle);
        int64_t ssb = sx48(h.dut->dbg_send_slope_per_byte);
        h.expect_eq(isc,  83,     "cbs06", "idle_slope_per_cycle rounded (trunc gives 82)");
        h.expect_eq(ssb, -65470,  "cbs06", "send_slope_per_byte rounded (trunc gives -65469)");
        // and rounding must be to NEAREST, not "always up": a config whose
        // fraction is below 1/2 must still land on the truncated value
        h.do_reset(4);
        for (int i = 0; i < 400; i++)
            h.cycle(mk(true, false, false, true, false, 0, true, 1000000), "cbs06 warm2");
        int64_t isc2 = sx48(h.dut->dbg_idle_slope_per_cycle);
        //  1000000<<16 / 8e8 = 81.92 -> nearest 82
        h.expect_eq(isc2, 82, "cbs06", "fraction < 1/2 still rounds down");
        printf("  [%s] REQ-CBS-06 slope quotients round to nearest (both terms)\n",
               (h.fails == f0) ? "PASS" : "FAIL");
    }

    // ---- REQ-CBS-06: harness MEASURES the residual fixed-point error ----
    // The REQ asks for the number, not just the fix. Free-accrue below the
    // hiCredit clamp for a long run and report the fixed-point credit's drift
    // from the exact-rate ideal, in bytes and in ppm of the accrued value.
    // Two points: a deliberately awkward tiny slope (worst relative case) and a
    // realistic Class-A-sized one, so the number is interpretable.
    for (int mi = 0; mi < 2; mi++) {
        long f0 = h.fails;
        const int32_t IDLE_M = mi ? 490000000 : 1007081;  // 490 Mb/s frac .8 / 1 Mb/s frac .5+
        const int     N      = 20000;        // cycles of uninterrupted accrual
        h.do_reset(4);
        for (int i = 0; i < 300; i++)        // let the engine commit first
            h.cycle(mk(true, false, false, true, false, 0, true, IDLE_M, 1 << 20, -(1 << 20)), "cbs06m warm");
        double err0 = h.max_ideal_err;
        for (int i = 0; i < N; i++)          // queue has data, not transmitting -> pure accrual
            h.cycle(mk(true, true, false, true, true, 0, true, IDLE_M, 1 << 20, -(1 << 20)), "cbs06m accrue");
        // measure the DUT's own credit register, not the model's, so this
        // number is a hardware measurement and moves when the RTL moves
        double accrued = (double)sx48(h.dut->dbg_credit) / 65536.0;
        double ideal   = h.iref.credit_bytes();
        double drift   = std::fabs(accrued - ideal);
        double ppm     = (ideal != 0.0) ? (drift / std::fabs(ideal)) * 1e6 : 0.0;
        printf("  [INFO] REQ-CBS-06 residual over %d free-accrual cycles @ idleSlope %d:\n"
               "         fixed-point %.6f B, ideal %.6f B, drift %.6f B (%.2f ppm)\n",
               N, IDLE_M, accrued, ideal, drift, ppm);
        // the accrual must be non-trivial or the measurement means nothing
        if (ideal < 1.0) { printf("  [FAIL] cbs06m: accrual too small to measure\n"); h.fails++; }
        // and rounding must keep the drift inside half an LSB per cycle
        double bound = (double)N * 0.5 / 65536.0;
        if (drift > bound) {
            printf("  [FAIL] cbs06m: drift %.6f B exceeds the half-LSB-per-cycle bound %.6f B\n",
                   drift, bound);
            h.fails++;
        }
        printf("  [%s] REQ-CBS-06 residual measured and inside the half-LSB/cycle bound\n",
               (h.fails == f0) ? "PASS" : "FAIL");
        (void)err0;
    }

    // ---- REQ-CBS-07: the wire-time debt IS 8.6.8.2 (e) transmit ----------
    // Send ONE frame of L client bytes at full beat rate, then wait with
    // data queued. Three properties, each against an INDEPENDENT integer
    // oracle (not the reference model, so a model+RTL change made together
    // cannot hide a regression):
    //   (a) the debt window's LENGTH is the frame's real wire time: from the
    //       first nonzero-debt cycle to its return to zero takes
    //       ceil((L + V) * 65536 / 81920) cycles at 1G/100 MHz, where
    //       V = 24 + max(0, 60 - L) - the overhead + min-frame pad law;
    //   (b) while the debt is nonzero the credit HOLDS (no idleSlope
    //       accrual - the old law's 9.6/20.5 percent over-delivery was
    //       exactly this accrual running during wire time);
    //   (c) once the debt returns to zero the accrual resumes.
    for (int fi = 0; fi < 2; fi++) {
        long f0 = h.fails;
        const int L = fi ? 46 : 64;             // full frame / CRF-size runt
        const int V = 24 + (L < 60 ? 60 - L : 0);
        const int64_t DRAIN = 81920;            // 1.25 B/cyc in Q16 (1G/100MHz)
        const int64_t WQ16  = (int64_t)(L + V) << 16;
        const long exp_busy = (long)((WQ16 + DRAIN - 1) / DRAIN);  // ceil
        h.do_reset(4);
        for (int i = 0; i < 300; i++)           // engine commit + some credit
            h.cycle(mk(true, true, false, true, true, 0), "cbs07 warm");
        // the frame: full 8-byte beats, a short last beat for the runt
        long busy = 0; bool seen = false;
        int64_t hold_credit = 0; long hold_viol = 0;
        int rem = L;
        while (rem > 0) {
            int b = rem > 8 ? 8 : rem;
            rem -= b;
            h.cycle(mk(true, true, true, true, true, (uint16_t)b, true,
                       500000000, 761, -761, rem == 0), "cbs07 beat");
            if (dut->dbg_wire_debt != 0) { busy++; seen = true; }
        }
        // drain out: count the remaining busy cycles; credit must HOLD
        // (the last debit lands 1 cycle after the last beat - let it land,
        // then freeze-check until the debt clears)
        h.cycle(mk(true, true, false, true, true, 0), "cbs07 debit-lands");
        if (dut->dbg_wire_debt != 0) busy++;
        hold_credit = sx48(dut->dbg_credit);
        for (long g = 0; g < 4 * exp_busy && dut->dbg_wire_debt != 0; g++) {
            h.cycle(mk(true, true, false, true, true, 0), "cbs07 drain");
            if (dut->dbg_wire_debt != 0) {
                busy++;
                if (sx48(dut->dbg_credit) != hold_credit) hold_viol++;
            }
        }
        // (a) window length: +-1 cycle for the add/drain phase alignment
        bool len_ok = seen && (busy >= exp_busy - 1) && (busy <= exp_busy + 1);
        if (!len_ok) {
            printf("  [FAIL] cbs07 L=%d: debt busy %ld cycles, oracle %ld "
                   "(V=%d)\n", L, busy, exp_busy, V);
            h.fails++;
        }
        // (b) credit held through the post-frame wire time
        h.expect_eq(hold_viol, 0, "cbs07", "credit frozen while debt > 0");
        // (c) accrual resumes once the wire is ours again
        int64_t c0 = sx48(dut->dbg_credit);
        for (int i = 0; i < 50; i++)
            h.cycle(mk(true, true, false, true, true, 0), "cbs07 resume");
        h.expect_eq((int64_t)(sx48(dut->dbg_credit) > c0 ? 1 : 0), 1,
                    "cbs07", "accrual resumes at debt == 0");
        printf("  [%s] REQ-CBS-07 L=%d+V=%d: wire window %ld cyc (oracle %ld), "
               "credit frozen inside it, accrual resumes after\n",
               (h.fails == f0) ? "PASS" : "FAIL", L, V, busy, exp_busy);
    }

    printf("--------------------------------------------------------------\n");
    printf("cycle checks: %ld   mismatches: %ld   max |DUT-ideal|: %.4f bytes\n",
           h.checks, h.fails, h.max_ideal_err);
    printf("RESULT: %s\n", (h.fails == 0) ? "PASS" : "FAIL");

    dut->final();
    delete dut;
    return (h.fails == 0) ? 0 : 1;
}
