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
                    int32_t hi = 761, int32_t lo = -761) {
    CbsInputs in;
    in.resetn = resetn; in.queue_has_data = qhd; in.is_transmitting = istx;
    in.is_1g = is1g; in.is_granted = isg; in.bytes_sent = bytes;
    in.shaped = shaped; in.idle_slope = idle; in.hi_credit = hi; in.lo_credit = lo;
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
        dut->shaped_i          = in.shaped;
        dut->idle_slope_i      = (uint32_t)in.idle_slope;
        dut->hi_credit_i       = (uint32_t)in.hi_credit;
        dut->lo_credit_i       = (uint32_t)in.lo_credit;
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

    printf("== CBS verification harness (runtime config; default queue-0 Class-A "
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
    {
        std::mt19937 rng(0xC0FFEE);
        std::uniform_int_distribution<int> bit(0, 1);
        std::uniform_int_distribution<int> bytes(0, 8);
        long start_fails = h.fails;
        for (int i = 0; i < 50000; i++) {
            bool qhd  = bit(rng);
            bool istx = bit(rng) && qhd;
            bool isg  = istx || bit(rng);
            uint16_t b = istx ? (uint16_t)bytes(rng) : 0;
            h.cycle(mk(true, qhd, istx, true, isg, b), "random");
        }
        printf("  [%s] randomized 50000 cycles: DUT tracks fixed-point ref exactly\n",
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

    printf("--------------------------------------------------------------\n");
    printf("cycle checks: %ld   mismatches: %ld   max |DUT-ideal|: %.4f bytes\n",
           h.checks, h.fails, h.max_ideal_err);
    printf("RESULT: %s\n", (h.fails == 0) ? "PASS" : "FAIL");

    dut->final();
    delete dut;
    return (h.fails == 0) ? 0 : 1;
}
