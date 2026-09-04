/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for the open CDC primitives cdc_pulse.sv and
 * cdc_handshake.sv (Track 1.4 — replacing xpm_cdc_pulse / xpm_cdc_handshake).
 *
 * Drives two INDEPENDENT clocks (src half-period 2, dest half-period 3 => async)
 * and checks: every source pulse produces exactly one destination pulse; each
 * value handed to the handshake arrives byte-exact in the destination domain with
 * a dest_req pulse and the src_rcv acknowledge returns to the source.
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vcdc_tb_top.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdio>
#include <cstdint>

// two asynchronous clocks: src toggles every SRC_HP ticks, dest every DST_HP
constexpr int SRC_HP = 2;
constexpr int DST_HP = 3;

// harness timing budgets, counted in step() ticks unless stated otherwise
constexpr int kResetTicks = 40;             // reset held asserted
constexpr int kPostResetTicks = 20;         // settle after reset release
constexpr int kPulseGapHalfPeriods = 12;    // src half-periods between pulses
constexpr int kPulseDrainTicks = 60;        // final drain before the pulse tally
constexpr int kHandshakeTimeout = 400;      // loop guard for one transfer
constexpr int kHandshakeGapTicks = 12;      // gap before the next transfer

namespace {

//! The two CDC primitives, their two asynchronous clocks and the tally that
//! judges them, owned by one object (Core Guidelines I.2): the tick counter and
//! the two edge flags `step()` publishes are state of THIS run, not of the
//! translation unit.
class CdcPrimitiveHarness {
 public:
    int run() {
        const milan::tb::Model<Vcdc_tb_top> model;
        dut = model.get();

        reset_both_domains();

        printf("== cdc_pulse + cdc_handshake harness (async 2:3 clocks) ==\n");

        check_every_source_pulse_crosses_once();
        check_each_value_crosses_byte_exact();

        printf("--------------------------------------------------------------\n");
        printf("checks: %ld   failures: %ld\n", checks, fails);
        printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
        return fails ? 1 : 0;
    }

 private:
    void ck(const char* what, uint64_t got, uint64_t exp) {
        checks++;
        if (got != exp) {
            fails++;
            printf("  [FAIL] %-28s got=0x%llx exp=0x%llx\n", what,
                   static_cast<unsigned long long>(got), static_cast<unsigned long long>(exp));
        }
    }

    void step() {
        bool sp = dut->src_clk;
        bool dp = dut->dest_clk;
        T++;
        if (T % SRC_HP == 0) dut->src_clk = !dut->src_clk;
        if (T % DST_HP == 0) dut->dest_clk = !dut->dest_clk;
        dut->eval();
        src_rose  = (!sp && dut->src_clk);
        dest_rose = (!dp && dut->dest_clk);
    }

    void reset_both_domains() {
        dut->src_clk = 0; dut->dest_clk = 0;
        dut->src_rst_n = 0; dut->dest_rst_n = 0;
        dut->p_src_pulse = 0; dut->h_src_in = 0; dut->h_src_send = 0;
        for (int i = 0; i < kResetTicks; i++) step();
        dut->src_rst_n = 1; dut->dest_rst_n = 1;
        for (int i = 0; i < kPostResetTicks; i++) step();
    }

    // ---- pulse CDC: N source pulses -> N destination pulses ----
    void check_every_source_pulse_crosses_once() {
        constexpr int N = 12;
        int dest_pulses = 0;
        for (int n = 0; n < N; n++) {
            dut->p_src_pulse = 1;
            do { step(); if (dest_rose && dut->p_dest_pulse) dest_pulses++; } while (!src_rose);
            dut->p_src_pulse = 0;                       // exactly one src-cycle pulse
            for (int g = 0; g < kPulseGapHalfPeriods * SRC_HP; g++) { step(); if (dest_rose && dut->p_dest_pulse) dest_pulses++; }
        }
        for (int g = 0; g < kPulseDrainTicks; g++) { step(); if (dest_rose && dut->p_dest_pulse) dest_pulses++; }
        ck("dest pulse count == src", dest_pulses, N);
        printf("  [%s] pulse CDC: %d/%d pulses crossed\n", dest_pulses == N ? "PASS" : "FAIL", dest_pulses, N);
    }

    // ---- value CDC: each value crosses byte-exact with req + rcv ----
    void check_each_value_crosses_byte_exact() {
        constexpr uint64_t vals[] = { 0x1122334455667788ULL, 0xDEADBEEFCAFEF00DULL,
                                      0x0000000000000001ULL, 0xFFFFFFFFFFFFFFFFULL,
                                      0x0102030405060708ULL };
        for (uint64_t v : vals) {
            dut->h_src_in = v;
            dut->h_src_send = 1;                        // rising edge starts the transfer
            bool got_req = false;
            bool got_rcv = false;
            uint64_t out = 0;
            for (int c = 0; c < kHandshakeTimeout && !(got_req && got_rcv); c++) {
                step();
                if (dest_rose && dut->h_dest_req) { got_req = true; out = dut->h_dest_out; }
                if (src_rose  && dut->h_src_rcv)  got_rcv = true;
            }
            ck("handshake dest_req", got_req ? 1 : 0, 1);
            ck("handshake value",    out, v);
            ck("handshake src_rcv",  got_rcv ? 1 : 0, 1);
            dut->h_src_send = 0;                         // drop send; gap before next
            for (int g = 0; g < kHandshakeGapTicks; g++) step();
        }
    }

    Vcdc_tb_top* dut = nullptr;
    long checks = 0;
    long fails = 0;
    uint64_t T = 0;
    bool src_rose = false;
    bool dest_rose = false;
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    CdcPrimitiveHarness harness;
    return harness.run();
}
