// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// NX-shape TX mux soak — the coverage hole the m001a-era silicon TX wedge
// exposed (2026-07-29): the frame-atomic 2:1 TX mux (g_txmux) and the
// KL_lwsrp_ctx_tx attribute engine only elaborate at N_CTX_P > 1 — the
// silicon shape — and no desk suite drove them at all, let alone under
// MAC-arbiter backpressure. Silicon signature this hunts: ALL TX dies
// ~40 s after engine enable (~90 sent PDUs), sent-counter frozen, RX fine,
// no recovery — one source stuck mid-frame holds the mux grant forever.
//
// Scenario: the silicon 4x4 shape (N_CTX_P=8 = L+T-1 with L=5,T=4-ish; we
// use 8), talker ctx rows provisioned like the fabric auto-provisioning
// does at boot, engine enabled, bridge traffic + LeaveAll turns of both
// applications, HOSTILE tready. Invariants: liveness (frames keep
// completing every JoinTime window), pre-edge AXIS stability, and the
// mux-lock detector (tvalid held without acceptance for > 10k cycles =
// the wedge).
#include "VKL_lwsrp_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static VKL_lwsrp_top* dut;
static long checks = 0, fails = 0;
static void ck(const char* t, long got, long exp) {
    checks++; if (got != exp) { fails++; printf("  [FAIL] %-52s got=%ld exp=%ld\n", t, got, exp); }
    else printf("  [ ok ] %-52s = %ld\n", t, got);
}

static long cyc = 0;
static unsigned lfsr = 0xBEEFu;
static long frames = 0, axis_viol = 0, stuck_max = 0, stuck_now = 0;
static int in_frame = 0;
static int in_stall = 0; static uint64_t sdata; static int slast, skeep;

static void step() {
    lfsr = (lfsr >> 1) ^ (-(lfsr & 1u) & 0xB400u);
    dut->m_axis_tready = ((lfsr & 3u) != 0);          // ~25% stall
    dut->clk_i = 0; dut->eval();
    // pre-edge checks (post-edge sampling races the legal beat advance)
    if (in_stall) {
        if (!dut->m_axis_tvalid || dut->m_axis_tdata != sdata ||
            (int)dut->m_axis_tlast != slast || (int)dut->m_axis_tkeep != skeep)
            axis_viol++;
    }
    if (dut->m_axis_tvalid && !dut->m_axis_tready) {
        in_stall = 1; sdata = dut->m_axis_tdata;
        slast = dut->m_axis_tlast; skeep = dut->m_axis_tkeep;
        stuck_now++;
        if (stuck_now > stuck_max) stuck_max = stuck_now;
    } else {
        in_stall = 0;
        if (dut->m_axis_tvalid && dut->m_axis_tready) {
            stuck_now = 0;
            in_frame = !dut->m_axis_tlast;
            if (dut->m_axis_tlast) frames++;
        } else if (!dut->m_axis_tvalid) {
            stuck_now = 0;
        }
    }
    dut->clk_i = 1; dut->eval();
    cyc++;
}
static void run(long n) { for (long i = 0; i < n; i++) step(); }

// bridge-side MSRP/MVRP PDU feed (minimal: LeaveAll-only vectors)
static void feed(const std::vector<uint8_t>& f) {
    for (size_t off = 0; off < f.size(); off += 8) {
        uint64_t d = 0; int k = 0;
        for (int l = 0; l < 8 && off + l < f.size(); l++) { d |= (uint64_t)f[off+l] << (8*l); k++; }
        dut->rx_tvalid_i = 1; dut->rx_tdata_i = d;
        dut->rx_tkeep_i = (k == 8) ? 0xFF : ((1u << k) - 1);
        dut->rx_tlast_i = (off + 8 >= f.size());
        step();
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; run(20);
}

static std::vector<uint8_t> mrp_leaveall(bool mvrp) {
    std::vector<uint8_t> f(64, 0x00);
    // DA
    if (mvrp) { f[0]=0x01;f[1]=0x80;f[2]=0xC2;f[3]=0x00;f[4]=0x00;f[5]=0x21; }
    else      { f[0]=0x01;f[1]=0x80;f[2]=0xC2;f[3]=0x00;f[4]=0x00;f[5]=0x0E; }
    for (int i = 0; i < 6; i++) f[6+i] = 0x3C;            // bridge SA
    if (mvrp) { f[12]=0x88; f[13]=0xF5; } else { f[12]=0x22; f[13]=0xEA; }
    f[14]=0x00;                                            // proto ver
    if (mvrp) {
        f[15]=0x01; f[16]=0x02;                            // VID attr, len 2
        f[17]=0x20; f[18]=0x01;                            // LeaveAll, 1 val
        f[19]=0x00; f[20]=0x02; f[21]=0x00;                // vid 2, event 0
    } else {
        f[15]=0x04; f[16]=0x04;                            // Domain, len 4
        f[17]=0x00; f[18]=0x09;
        f[19]=0x20; f[20]=0x01;                            // LeaveAll, 1 val
        f[21]=0x06; f[22]=0x03; f[23]=0x00; f[24]=0x02; f[25]=0x00;
    }
    return f;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new VKL_lwsrp_top;

    dut->rst_n = 0; dut->enable_i = 0; dut->m_axis_tready = 1;
    dut->rx_tvalid_i = 0; dut->talker_en_i = 0; dut->lstn_declare_i = 0;
    dut->lstn_bound_i = 0; dut->is_1g_i = 0;
    dut->station_mac_i = 0x020000000002ULL; dut->unique_id_i = 0;
    dut->vid_i = 2; dut->dest_mac_i = 0x91E0F000FE01ULL;
    dut->max_frame_i = 224; dut->interval_frames_i = 1; dut->latency_i = 500000;
    dut->ctx_req_i = 0;
    run(8);
    dut->rst_n = 1; run(8);

    printf("== NX TX mux soak (N_CTX=8: g_txmux + ctx_tx under hostile tready) ==\n");

    // ---- provision 4 talker ctx rows like the fabric auto-provisioning ----
    for (int t = 0; t < 4; t++) {
        dut->ctx_req_i = 1; dut->ctx_we_i = 1;
        dut->ctx_idx_i = 4 + t;            // talker rows above the listeners
        dut->ctx_valid_i = 1; dut->ctx_dir_i = 0;
        dut->ctx_sid_i = 0x020000000002ULL << 16 | t;
        dut->ctx_dmac_i = 0x91E0F00060A1ULL + t;
        dut->ctx_prio_rank_i = 0x70; dut->ctx_max_frame_i = 120;
        dut->ctx_interval_i = 1; dut->ctx_latency_i = 500000;
        for (int w = 0; w < 20 && !dut->ctx_gnt_o; w++) step();
        step();
        dut->ctx_req_i = 0; run(5);
    }
    dut->enable_i = 1; dut->talker_en_i = 1; run(50);

    // ---- the soak: 12 LeaveAll turns' worth of cycles + bridge LeaveAlls --
    long f0 = frames, live_fail = 0;
    for (int turn = 0; turn < 12; turn++) {
        long before = frames;
        run(40000);
        if (turn % 2 == 0) feed(mrp_leaveall(false));   // MSRP LeaveAll
        run(30000);
        if (turn % 3 == 0) feed(mrp_leaveall(true));    // MVRP LeaveAll
        run(30000);
        if (frames == before) {
            live_fail++;
            printf("   [turn %d] NO completed frames (stuck_max=%ld)\n",
                   turn, stuck_max);
        }
    }
    ck("liveness: frames completed in every turn", live_fail, 0);
    ck("frames grew over the soak", frames > f0 ? 1 : 0, 1);
    ck("pre-edge AXIS stability violations", axis_viol, 0);
    // the wedge detector: a source holding tvalid > 10k cycles unaccepted
    ck("no mux lock (max consecutive stall cycles < 10000)",
       stuck_max < 10000 ? 1 : 0, 1);
    printf("   (frames=%ld stuck_max=%ld)\n", frames, stuck_max);

    printf("== %ld checks, %ld failures ==\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
