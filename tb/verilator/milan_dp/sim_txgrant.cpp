/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * sim_txgrant - the CPU DMA-TX lane under REGISTERED-CONTROLLER push load
 * (task #19, silicon 2026-08-06).
 *
 * WHY THIS EXECUTABLE EXISTS: an A/B on the AX7101 proved the 0x0024+
 * fabric starves the CPU DMA-TX lane minutes after an ATDECC controller
 * REGISTERs for unsolicited notifications - ssh/ARP die while the kernel,
 * RX, AAF streaming and the AECP control lane all stay healthy (bd-stage
 * b2 ~146us/frame, TX n~147 frames in 8 min). No sim in this suite had
 * ever REGISTERED a controller, so the Table 5.22 push machinery - the
 * only 0x0024 delta - had never once run against the TX trunk at desk.
 * This harness closes exactly that gap and it is a PERMANENT leg: the
 * push arms must never again be a wire-first code path.
 *
 * SHAPE OF THE DRILL:
 *   [1] streaming posture: talker 0 emits silence-filled AAF (the data
 *       lane's standing competitor) against a PACED MAC model (~1 GbE
 *       beat cadence + inter-frame gap) - a constantly-ready MAC would
 *       hide every stall-window interaction in adp_tx_arbiter;
 *   [2] baseline: continuous best-effort CPU frames (ARP-shaped, q0 -
 *       ssh's exact path) presented on s_axis_tx; measure accepted
 *       throughput and the worst inter-accept gap;
 *   [3] REGISTER a controller (the silicon trigger);
 *   [4] push storm: GM identity flips - each flip arms pend3 (interface
 *       GET_COUNTERS) and pend8 (GET_AS_PATH, deliberately unlimited)
 *       so every flip is a real push emission through the control lane;
 *       plus CONNECT_RX/DISCONNECT_RX churn on sink 0 for the pend6
 *       dwell path (16 ms settle at the real 1 kHz tick);
 *   [5] post-storm quiet window - the silicon death was MINUTES AFTER
 *       registration during ordinary traffic, i.e. a leak, not a burst;
 *   [6] verdicts: CPU accept rate in every measured window >= 85% of
 *       baseline, worst gap < 2^18 cycles, pushes actually egressed
 *       (the drill must prove it exercised the machinery), and the
 *       A_TXARB_DIAG 0x784 stickies name any arbiter that locked up.
 */

#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>

static Vmilan_datapath* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, unsigned long got, unsigned long exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-52s got=0x%lx exp=0x%lx\n", what, got, exp);
    } else {
        printf("  [ok]   %-52s = 0x%lx\n", what, got);
    }
}
static void ck_ge(const char* what, double got, double floor_v) {
    checks++;
    if (got < floor_v) {
        fails++;
        printf("  [FAIL] %-52s got=%.3f floor=%.3f\n", what, got, floor_v);
    } else {
        printf("  [ok]   %-52s = %.3f (floor %.3f)\n", what, got, floor_v);
    }
}

static void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->eval(); }
static void hi() { dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->eval(); }
static void step() { lo(); hi(); }

// ---- AXI4-Lite BFM (identical to the other milan_dp harnesses) ----
static void axi_write(uint16_t a, uint32_t d) {
    dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
    dut->s_axi_wdata = d;  dut->s_axi_wvalid = 1; dut->s_axi_wstrb = 0xF;
    dut->s_axi_bready = 1;
    for (int g = 0; g < 4096; ++g) {
        dut->eval();
        bool acc = dut->s_axi_awready && dut->s_axi_wready;
        step();
        if (acc) break;
    }
    dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
    for (int g = 0; g < 4096; ++g) { dut->eval(); if (dut->s_axi_bvalid) break; step(); }
    step();
    dut->s_axi_bready = 0;
}
static uint32_t axi_read(uint16_t a) {
    dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
    for (int g = 0; g < 4096; ++g) {
        dut->eval();
        bool acc = dut->s_axi_arready;
        step();
        if (acc) break;
    }
    dut->s_axi_arvalid = 0;
    uint32_t v = 0;
    for (int g = 0; g < 4096; ++g) { dut->eval(); if (dut->s_axi_rvalid) { v = dut->s_axi_rdata; break; } step(); }
    step();
    dut->s_axi_rready = 0;
    return v;
}

enum {
    A_VERSION = 0x004, A_MAC_ALO = 0x108, A_MAC_AHI = 0x10C,
    A_ADP_CTRL = 0x600, A_ADP_EIDLO = 0x604, A_ADP_EIDHI = 0x608,
    A_ADP_GMLO = 0x624, A_ADP_GMHI = 0x628,
    A_AAF_CTRL = 0x654, A_AAF_FRAMES = 0x660, A_LWSRP_CTRL = 0x680,
    A_TXARB_DIAG = 0x784,
};

// ======================================================================
// background traffic engines. These run INSIDE every measured window and
// every helper that burns cycles, so the DUT never sees an idle bench.
// ======================================================================

// ---- paced MAC model: ~1 GbE on a 64-bit AXIS. In-frame: one beat per
//      7 cycles (8 B per 64 ns wire vs the axis clock); between frames:
//      30 idle cycles (preamble+IFG+slack). The stall windows this
//      creates are the conditions adp_tx_arbiter's accept-locking and
//      its documented mutate-under-stall deviation live in.
static int  mac_pace_cnt = 0;
static int  mac_gap_cnt  = 0;
static long eg_cpu_frames = 0, eg_aaf_frames = 0, eg_aecp_frames = 0;
static long eg_other_frames = 0;
static std::vector<uint8_t> eg_cur;

static void mac_model_pre() {   // call BEFORE lo() each cycle
    bool ready = false;
    if (mac_gap_cnt > 0)            { mac_gap_cnt--; }
    else if (mac_pace_cnt > 0)      { mac_pace_cnt--; }
    else                            { ready = true; }
    dut->m_axis_mac_tx_tready = ready ? 1 : 0;
}
static void mac_model_post() {  // call AFTER hi() (sampled accepted beat)
    if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
        for (int l = 0; l < 8; l++)
            if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                eg_cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
        if (dut->m_axis_mac_tx_tlast) {
            if (eg_cur.size() > 14) {
                if (eg_cur[12] == 0x08 && eg_cur[13] == 0x06) eg_cpu_frames++;
                else if (eg_cur[12] == 0x81 && eg_cur.size() > 18 &&
                         eg_cur[16] == 0x22 && eg_cur[17] == 0xF0 &&
                         eg_cur[18] == 0x02) eg_aaf_frames++;
                else if (eg_cur[12] == 0x22 && eg_cur[13] == 0xF0 &&
                         eg_cur[14] == 0xFB) eg_aecp_frames++;
                else eg_other_frames++;
            } else eg_other_frames++;
            eg_cur.clear();
            mac_gap_cnt = 30;
        } else {
            mac_pace_cnt = 6;
        }
    }
}

// ---- continuous CPU TX injector: 60-byte ARP-shaped best-effort frames
//      (broadcast dst, ethertype 0x0806 -> untagged, not in the control
//      DMAC table -> CLS_DEFAULT_PCP -> q0: ssh/ARP's exact lane).
static int      cpu_beat = -1;      // -1 = between frames
static int      cpu_gap  = 0;
static long     cpu_accepted_frames = 0;
static long     cpu_gap_worst = 0;  // cycles between frame accepts
static long     cpu_gap_cur = 0;
static uint64_t cpu_frame_beats[8];

static void cpu_frame_init() {
    uint8_t f[64]; memset(f, 0, sizeof f);
    memset(f, 0xFF, 6);                              // broadcast
    const uint8_t src[6] = {0x02,0x00,0x00,0x00,0x00,0x01};
    memcpy(f+6, src, 6);
    f[12]=0x08; f[13]=0x06;                          // ARP
    f[14]=0x00; f[15]=0x01; f[16]=0x08; f[17]=0x00;  // htype/ptype
    for (int b = 0; b < 8; b++) {
        uint64_t v = 0;
        for (int j = 0; j < 8; j++) v |= (uint64_t)f[b*8+j] << (8*j);
        cpu_frame_beats[b] = v;
    }
}
static void cpu_inj_pre() {     // BEFORE lo()
    if (cpu_beat < 0) {
        if (cpu_gap > 0) { cpu_gap--; dut->s_axis_tx_tvalid = 0; dut->s_axis_tx_tlast = 0; return; }
        cpu_beat = 0;
    }
    dut->s_axis_tx_tdata  = cpu_frame_beats[cpu_beat];
    dut->s_axis_tx_tkeep  = 0xFF;
    dut->s_axis_tx_tvalid = 1;
    dut->s_axis_tx_tlast  = (cpu_beat == 7);
}
static void cpu_inj_post() {    // AFTER hi()
    cpu_gap_cur++;
    if (dut->s_axis_tx_tvalid && dut->s_axis_tx_tready && cpu_beat >= 0) {
        if (cpu_beat == 7) {
            cpu_beat = -1; cpu_gap = 2;
            cpu_accepted_frames++;
            if (cpu_gap_cur > cpu_gap_worst) cpu_gap_worst = cpu_gap_cur;
            cpu_gap_cur = 0;
        } else cpu_beat++;
    }
}

// ---- one bench cycle with every background engine live ----
static void bstep() {
    mac_model_pre();
    cpu_inj_pre();
    lo();
    hi();
    cpu_inj_post();
    mac_model_post();
}
static void brun(long n) { for (long i = 0; i < n; i++) bstep(); }

// measured window: returns accepted-CPU-frame count over n cycles
struct Win { long cpu; long worst_gap; long aaf; long aecp; };
static Win measure(long n, const char* label) {
    long c0 = cpu_accepted_frames, a0 = eg_aaf_frames, e0 = eg_aecp_frames;
    cpu_gap_worst = 0; cpu_gap_cur = 0;
    brun(n);
    Win w = { cpu_accepted_frames - c0, cpu_gap_worst,
              eg_aaf_frames - a0, eg_aecp_frames - e0 };
    printf("  [win]  %-24s %8ld cyc: cpu %6ld  worst-gap %7ld  aaf %5ld  aecp %4ld\n",
           label, n, w.cpu, w.worst_gap, w.aaf, w.aecp);
    return w;
}

// ---- wire-side injection (MAC RX) with the background engines live ----
static void inject(const uint8_t* f, size_t len, int drain = 3000) {
    std::vector<uint64_t> beats;
    for (size_t bt = 0; bt < (len + 7) / 8; bt++) {
        uint64_t v = 0;
        for (int j = 0; j < 8; j++)
            if (bt*8 + j < len) v |= (uint64_t)f[bt*8+j] << (8*j);
        beats.push_back(v);
    }
    size_t idx = 0;
    for (int c = 0; c < drain; c++) {
        if (idx < beats.size()) {
            dut->s_axis_mac_rx_tdata  = beats[idx];
            dut->s_axis_mac_rx_tkeep  = 0xFF;
            dut->s_axis_mac_rx_tvalid = 1;
            dut->s_axis_mac_rx_tlast  = (idx == beats.size()-1);
        } else {
            dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
        }
        mac_model_pre(); cpu_inj_pre();
        lo();
        bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
        hi();
        cpu_inj_post(); mac_model_post();
        if (in_acc) idx++;
    }
    dut->s_axis_mac_rx_tvalid = 0;
}

static const uint8_t ST_MAC[6]  = {0x02,0x00,0x00,0x00,0x00,0x01};
static const uint8_t CTL_MAC[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
static const uint8_t ENT_EID[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};

// AECP AEM_COMMAND to our entity (unicast to the station MAC)
static void aecp_cmd(uint16_t cmd, uint16_t seq,
                     const std::vector<uint8_t>& pl = {}) {
    uint8_t f[80]; memset(f, 0, sizeof f);
    memcpy(f, ST_MAC, 6);
    memcpy(f+6, CTL_MAC, 6);
    f[12]=0x22; f[13]=0xF0;
    f[14]=0xFB; f[15]=0x00;                    // AECP, AEM_COMMAND
    uint16_t cdl = 12 + (uint16_t)pl.size();
    f[16]=(uint8_t)((cdl>>8)&0x7); f[17]=(uint8_t)cdl;
    memcpy(f+18, ENT_EID, 8);                  // target = us
    memcpy(f+26, CTL_MAC, 6);                  // controller eid = MAC<<16
    f[34]=(uint8_t)(seq>>8); f[35]=(uint8_t)seq;
    f[36]=(uint8_t)((cmd>>8)&0x7F); f[37]=(uint8_t)cmd;
    for (size_t i = 0; i < pl.size() && 38 + i < sizeof f; i++)
        f[38+i] = pl[i];
    size_t flen = 38 + pl.size(); if (flen < 60) flen = 60;
    inject(f, flen);
}

// the Hive posture: a registered controller POLLS while the entity
// pushes - GET_STREAM_INFO on STREAM_INPUT[0] round after round.
static uint16_t poll_seq = 0xA000;
static void hive_poll() {
    aecp_cmd(0x0026 /* GET_STREAM_INFO */, poll_seq++,
             {0x00,0x05, 0x00,0x00});          // STREAM_INPUT[0]
}

// ACMP CONNECT_RX / DISCONNECT_RX on sink 0 (fast-connect sid) - the
// pend6 signature source. Talker = a fictional peer; the probe ladder
// runs for real, which is the point (bench-faithful control traffic).
static void acmp_bind(bool connect, uint16_t seq) {
    uint8_t f[72]; memset(f, 0, sizeof f);
    const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
    memcpy(f, mc, 6);
    memcpy(f+6, CTL_MAC, 6);
    f[12]=0x22; f[13]=0xF0; f[14]=0xFC;
    f[15]= connect ? 0x06 : 0x08;              // CONNECT/DISCONNECT_RX_COMMAND
    f[16]=0x00; f[17]=44;
    const uint8_t fc_sid[8] = {0x3C,0xC0,0xC6,0x01,0x02,0x03,0x00,0x00};
    memcpy(f+18, fc_sid, 8);                   // fast-connect stream_id
    memcpy(f+26, CTL_MAC, 6);                  // controller
    const uint8_t tk[8] = {0x3C,0xC0,0xC6,0x01,0x02,0x03,0x00,0x00};
    memcpy(f+34, tk, 8);                       // talker entity id
    memcpy(f+42, ENT_EID, 8);                  // listener = us
    f[50]=0x00; f[51]=0x00;                    // talker_unique_id 0
    f[52]=0x00; f[53]=0x00;                    // listener_unique_id 0 (sink 0)
    const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x40};
    memcpy(f+54, dm, 6);
    f[62]=(uint8_t)(seq>>8); f[63]=(uint8_t)seq;
    inject(f, 70, 4000);
}

static void print_txarb(const char* when) {
    uint32_t d = axi_read(A_TXARB_DIAG);
    printf("  [diag] TXARB %-18s = 0x%08X (stall %02X abort %02X locked %02X)\n",
           when, d, (d >> 16) & 0xFF, (d >> 8) & 0xFF, d & 0xFF);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vmilan_datapath;
    cpu_frame_init();

    printf("=== milan_datapath TX-grant under registered-controller pushes"
           " (task #19) ===\n");
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
    dut->s_axi_bready = dut->s_axi_rready = 0;
    dut->s_axis_tx_tvalid = 0; dut->s_axis_mac_rx_tvalid = 0;
    dut->m_axis_mac_tx_tready = 1; dut->m_axis_rx_tready = 1;
    dut->m_axis_ts_tready = 1; dut->m_axis_pcm_tready = 1;
    for (int i = 0; i < 16; i++) step();
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    for (int i = 0; i < 16; i++) step();

    ck("VERSION is the 0x0024+ push era",
       axi_read(A_VERSION) >= 0x00010024, 1);

    // [1] identity + streaming posture: station MAC, entity id, engine on,
    //     VID-2 licence bypass so talker 0 emits continuously (5.3.7.3
    //     silence fill) - the data lane has its standing competitor.
    axi_write(A_MAC_ALO, 0x00000002);
    axi_write(A_MAC_AHI, 0x00000100);          // wire 02:00:00:00:00:01
    axi_write(A_ADP_EIDHI, 0x020000FF);
    axi_write(A_ADP_EIDLO, 0xFE000001);
    axi_write(A_ADP_CTRL, 0x1);
    axi_write(A_LWSRP_CTRL, 0x0);
    axi_write(A_AAF_CTRL, 0x00020003);
    brun(50000);                               // let the talker spin up
    long aaf0 = eg_aaf_frames;
    brun(200000);
    ck("talker 0 emits AAF against the paced MAC", eg_aaf_frames > aaf0, 1);

    // [2] baseline CPU throughput (nobody registered)
    print_txarb("at baseline");
    Win base = measure(1000000, "baseline");
    ck("baseline moves real CPU traffic", base.cpu > 500, 1);

    // [3] REGISTER a controller - the silicon trigger
    long e0 = eg_aecp_frames;
    aecp_cmd(36, 0x9000);                      // REGISTER_UNSOL_NOTIFICATION
    brun(20000);
    ck("REGISTER_UNSOL answered on the control lane", eg_aecp_frames > e0, 1);

    Win reg = measure(1000000, "registered-quiet");
    ck_ge("registered-quiet rate vs baseline",
          (double)reg.cpu / (double)base.cpu, 0.85);

    // [4a] push storm: GM identity flips. Every flip arms pend3
    //      (AVB_INTERFACE GET_COUNTERS) and pend8 (GET_AS_PATH, no rate
    //      limiter by design) -> real push emissions through the trunk.
    long push0 = eg_aecp_frames;
    double worst_ratio = 1.0;
    for (int i = 0; i < 30; i++) {
        axi_write(A_ADP_GMLO, 0x00000200u + (uint32_t)(i & 1));
        axi_write(A_ADP_GMHI, 0x3CC0C6FFu);    // commit on HI (atomic pair)
        hive_poll();                           // Hive polls WHILE we push
        brun(15000);
        hive_poll();
        brun(15000);                           // let the pushes emit
        if ((i % 6) == 5) {
            char nm[32]; snprintf(nm, sizeof nm, "gm-storm %d", i + 1);
            Win w = measure(300000, nm);
            double r = (double)w.cpu / ((double)base.cpu * 0.3);
            if (r < worst_ratio) worst_ratio = r;
        }
    }
    long gm_pushes = eg_aecp_frames - push0;
    printf("  [info] GM storm emitted %ld AECP frames to the controller\n",
           gm_pushes);
    ck("GM flips really emitted pushes", gm_pushes >= 30, 1);
    ck_ge("worst storm-window rate vs baseline", worst_ratio, 0.85);
    print_txarb("after GM storm");

    // [4b] pend6: bind/unbind churn on sink 0. The 16 ms dwell is real
    //      (1 kHz tick at the elaborated clock), so give each edge
    //      1.7M cycles of live traffic to settle and emit.
    push0 = eg_aecp_frames;
    for (int i = 0; i < 2; i++) {
        acmp_bind(true,  (uint16_t)(0x7100 + i));
        for (int k = 0; k < 17; k++) { hive_poll(); brun(100000); }
        acmp_bind(false, (uint16_t)(0x7200 + i));
        for (int k = 0; k < 17; k++) { hive_poll(); brun(100000); }
    }
    long bind_pushes = eg_aecp_frames - push0;
    printf("  [info] bind churn emitted %ld AECP frames"
           " (responses + stream-info pushes)\n", bind_pushes);
    ck("bind churn produced control traffic", bind_pushes >= 4, 1);
    Win churn = measure(500000, "post-bind-churn");
    ck_ge("post-churn rate vs baseline",
          (double)churn.cpu / ((double)base.cpu * 0.5), 0.85);

    // [5] the leak window: quiet, registered, minutes-equivalent of
    //     ordinary traffic after the machinery has fired many times
    Win soak = measure(2000000, "post-storm soak");
    ck_ge("soak rate vs baseline",
          (double)soak.cpu / ((double)base.cpu * 2.0), 0.85);
    ck("soak worst inter-accept gap < 2^18 cycles",
       soak.worst_gap < (1L << 18), 1);

    // [6] arbiter verdicts: the data-lane muxes (5 aaf_final, 6 crf_dp,
    //     7 MAC boundary) must have latched neither abort nor stall
    uint32_t d = axi_read(A_TXARB_DIAG);
    print_txarb("final");
    ck("no ABORT sticky on the data-lane muxes", (d >> 8)  & 0xE0, 0);
    ck("no STALL sticky on the data-lane muxes", (d >> 16) & 0xE0, 0);
    ck("AAF never stopped (fabric health)", eg_aaf_frames > 1000, 1);

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
