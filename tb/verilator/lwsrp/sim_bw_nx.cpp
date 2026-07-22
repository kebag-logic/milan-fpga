// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_lwsrp_bw_gate Σ-slope harness at N=4 (docs/NXN_ARCHITECTURE.md §2.4 /
// §3.4, phase P5 matrix row "Σ-slope bw_gate + per-stream gates"):
//   - idleSlope(queue) = Σ granted per-stream slopes
//   - greedy index-order admission against the 75 % ceiling (over_limit on
//     refusal; lower-indexed grants never displaced)
//   - per-stream stream_gate: a torn-down stream stops instantly, others
//     keep their slots; freed budget re-admits a refused stream
//   - slope-then-gate / gate-then-slope ordering per stream
// 100 Mb/s port (limit = 75 Mb/s). slope = interval*(max_frame+42)*64000.
#include "VKL_lwsrp_bw_gate.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>

static VKL_lwsrp_bw_gate* dut;
static long checks=0, fails=0;
static void ck(const char* t, long got, long exp){
    checks++; if(got!=exp){ fails++; printf("  [FAIL] %-46s got=%ld exp=%ld\n",t,got,exp);}
    else printf("  [ ok ] %-46s = %ld\n",t,got); }

static void cyc(int n=1){ for(int i=0;i<n;i++){ dut->clk_i=0; dut->eval();
                                                dut->clk_i=1; dut->eval(); } }

static void set_tspec(int t, uint16_t mf, uint16_t iv){
    // packed [16N] inputs: 64-bit wide at N=4
    dut->max_frame_i       &= ~(0xFFFFULL<<(16*t));
    dut->max_frame_i       |= ((uint64_t)mf)<<(16*t);
    dut->interval_frames_i &= ~(0xFFFFULL<<(16*t));
    dut->interval_frames_i |= ((uint64_t)iv)<<(16*t);
}

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    dut=new VKL_lwsrp_bw_gate;

    dut->rst_n=0; dut->enable_i=1; dut->domain_ok_i=1; dut->is_1g_i=0;
    dut->talker_declared_i=0; dut->listener_ready_i=0;
    dut->max_frame_i=0; dut->interval_frames_i=0;
    cyc(4); dut->rst_n=1;

    printf("== KL_lwsrp_bw_gate Σ-slope harness (N=4, NXN P5) ==\n");

    // s0: (224+42)*1*64000 = 17.024 Mb/s
    // s1: (224+42)*2*64000 = 34.048 Mb/s
    // s2: (300+42)*2*64000 = 43.776 Mb/s
    set_tspec(0, 224, 1);
    set_tspec(1, 224, 2);
    set_tspec(2, 300, 2);
    cyc(16);                            // slope compute walk settles

    printf("\n[S1] two admitted streams: Σ slopes, both gates open\n");
    dut->talker_declared_i=0x3; dut->listener_ready_i=0x3; cyc(40);
    ck("gate s0 open", (dut->stream_gate_o>>0)&1, 1);
    ck("gate s1 open", (dut->stream_gate_o>>1)&1, 1);
    ck("slope_en", dut->slope_en_o, 1);
    ck("idleSlope = Σ(17.024M + 34.048M)", dut->idle_slope_o, 51072000);
    ck("no over_limit", dut->over_limit_o, 0);
    ck("res_active = s0|s1", dut->res_active_o, 0x3);

    printf("\n[S2] third stream refused by the Σ-ceiling (greedy order)\n");
    dut->talker_declared_i=0x7; dut->listener_ready_i=0x7; cyc(40);
    ck("over_limit on Σ refusal", dut->over_limit_o, 1);
    ck("s2 gate stays closed", (dut->stream_gate_o>>2)&1, 0);
    ck("lower-indexed grants keep their slots", dut->stream_gate_o & 0x3, 0x3);
    ck("idleSlope unchanged by the refusal", dut->idle_slope_o, 51072000);
    ck("res_active excludes s2", dut->res_active_o, 0x3);

    printf("\n[S3] per-stream teardown: s1 stops instantly, s0 untouched\n");
    dut->listener_ready_i=0x5;          // s1 loses READY (s0+s2 still ask)
    cyc(2);
    ck("s1 gate closes immediately", (dut->stream_gate_o>>1)&1, 0);
    ck("s0 gate still open", (dut->stream_gate_o>>0)&1, 1);
    cyc(80);                            // holds + re-admission round
    ck("freed budget re-admits s2", (dut->stream_gate_o>>2)&1, 1);
    ck("over_limit clears", dut->over_limit_o, 0);
    ck("idleSlope = Σ(17.024M + 43.776M)", dut->idle_slope_o, 60800000);

    printf("\n[S4] slope-before-gate ordering on (re)activation\n");
    dut->listener_ready_i=0x1; dut->talker_declared_i=0x1; cyc(80);
    ck("only s0 active", dut->res_active_o, 0x1);
    ck("Σ back to s0 alone", dut->idle_slope_o, 17024000);
    // re-admit s1 and watch slope join Σ before its gate opens
    dut->talker_declared_i=0x3; dut->listener_ready_i=0x3;
    long saw_slope_first=0;
    for(int i=0;i<80;i++){ cyc();
        if(dut->idle_slope_o==51072000 && !((dut->stream_gate_o>>1)&1))
            saw_slope_first=1;
        if((dut->stream_gate_o>>1)&1) break;
    }
    ck("s1 slope joined Σ before its gate opened", saw_slope_first, 1);
    ck("s1 gate finally open", (dut->stream_gate_o>>1)&1, 1);

    printf("\n[S5] global disable closes every gate\n");
    dut->enable_i=0; cyc(2);
    ck("all gates closed", dut->stream_gate_o, 0);
    cyc(40);
    ck("slope releases after the hold", dut->slope_en_o, 0);

    printf("--------------------------------------------------------------\n");
    printf("bw_gate NxN: %ld checks, %ld failures\nRESULT: %s\n",
           checks, fails, fails?"FAIL":"PASS");
    dut->final(); delete dut;
    return fails?1:0;
}
