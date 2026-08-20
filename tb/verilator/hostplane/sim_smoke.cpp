// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Host-plane cfg-sweep SMOKE (case e of the hostplane suite): the minimal
// case-A/B kernel - broadcast ARP + unicast-to-station + gPTP peer-multicast
// each MUST emerge on the host RX AXIS lane, and a PTP event frame MUST
// produce exactly one 2-beat ts record - re-run in OTHER parameterizations so
// shape-specific host-plane breaks surface:
//
//   small-1x-50MHz  : N_STREAMS=1,  MILAN_CLK_FREQ_HZ=50e6  (cfg_arty family)
//   mid-4x-100MHz   : N_STREAMS=4,  MILAN_CLK_FREQ_HZ=100e6 (4x4 direction)
//   tdm8-8x-100MHz  : N_STREAMS=8,  AUDIO_IF_SLOTS_P=8      (TDM front-end)
//
// There is NO elaboration-level taps-off parameter (KL_aaf_latency_taps is
// always instantiated; its runtime knob is LTAP_CTRL[1]) - the runtime-off
// variant is exercised in the main harness case D instead.
//
// LTAP same-cycle staging fixed 2026-07-26 (cascade walk).

#include "Vmilan_datapath.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>
#include <deque>

#ifndef NSTREAMS_TB
#define NSTREAMS_TB 1
#endif
#ifndef MILAN_CLK_TB
#define MILAN_CLK_TB 100000000
#endif
#ifndef SHAPE_NAME
#define SHAPE_NAME "unnamed"
#endif

static Vmilan_datapath* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, unsigned long got, unsigned long exp) {
    bool ok = (got == exp);
    checks++; if (!ok) fails++;
    printf("  [%s] %-52s got=0x%lx exp=0x%lx\n", ok ? "PASS" : "FAIL", what, got, exp);
}

// ---- clock + pump (same little-lane conventions as sim_hostplane.cpp) ----
struct Collected { int user; std::vector<uint8_t> bytes; };
static std::deque<std::vector<uint8_t>> rxq;
static std::vector<uint8_t> rx_cur;
static size_t rx_beat = 0;
static std::vector<Collected> host_frames, pcm_frames;
static std::vector<uint64_t> ts_beats;
static bool host_open = false, pcm_open = false;
struct Pre { bool aw_acc, b_v, ar_acc, r_v; uint32_t r_d; };
static Pre g_pre;

static void tick() {
    // move, not copy: the queue entry is popped on the next statement anyway
    if (rx_cur.empty() && !rxq.empty()) { rx_cur = std::move(rxq.front()); rxq.pop_front(); rx_beat = 0; }
    if (!rx_cur.empty()) {
        size_t nbeats = (rx_cur.size() + 7) / 8;
        uint64_t d = 0; uint8_t k = 0;
        for (int j = 0; j < 8; j++) {
            size_t i = rx_beat * 8 + j;
            if (i < rx_cur.size()) { d |= (uint64_t)rx_cur[i] << (8 * j); k |= (uint8_t)(1u << j); }
        }
        dut->s_axis_mac_rx_tdata = d; dut->s_axis_mac_rx_tkeep = k;
        dut->s_axis_mac_rx_tvalid = 1; dut->s_axis_mac_rx_tlast = (rx_beat == nbeats - 1);
    } else {
        dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
    }
    dut->m_axis_rx_tready = 1; dut->m_axis_ts_tready = 1;
    dut->m_axis_pcm_tready = 1; dut->m_axis_mac_tx_tready = 1;

    // clk_tdm_i: the item-4 TDM MASTER's serial-domain clock. Driven on
    // EVERY shape - the port exists unconditionally (a port's direction
    // cannot be parameterized in SystemVerilog) and an undriven clock on
    // the master shape would make the front-end sit silent, which is the
    // exact failure this lane exists to eliminate. Toggled with the others:
    // the smoke test proves the datapath ELABORATES and runs, not the
    // 98.304/100 MHz ratio, which tb/verilator/tdm measures directly.
    dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->i_ps_clk = 0;
    dut->clk_tdm_i = 0;
    dut->eval();
    bool rx_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
    bool ho_acc = dut->m_axis_rx_tvalid && dut->m_axis_rx_tready;
    uint64_t ho_d = dut->m_axis_rx_tdata; uint8_t ho_k = dut->m_axis_rx_tkeep;
    bool ho_l = dut->m_axis_rx_tlast;
    bool pc_acc = dut->m_axis_pcm_tvalid && dut->m_axis_pcm_tready;
    uint64_t pc_d = dut->m_axis_pcm_tdata; uint8_t pc_k = dut->m_axis_pcm_tkeep;
    bool pc_l = dut->m_axis_pcm_tlast; int pc_u = dut->m_axis_pcm_tuser;
    bool tsx = dut->m_axis_ts_tvalid && dut->m_axis_ts_tready;
    uint64_t ts_d = dut->m_axis_ts_tdata;
    g_pre.aw_acc = dut->s_axi_awready && dut->s_axi_wready;
    g_pre.b_v = dut->s_axi_bvalid;
    g_pre.ar_acc = dut->s_axi_arready;
    g_pre.r_v = dut->s_axi_rvalid; g_pre.r_d = dut->s_axi_rdata;
    dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->i_ps_clk = 1;
    dut->clk_tdm_i = 1;
    dut->eval();
    if (rx_acc) { if (++rx_beat >= (rx_cur.size() + 7) / 8) { rx_cur.clear(); rx_beat = 0; } }
    auto collect = [](std::vector<Collected>& sink, bool& open, uint64_t data,
                      uint8_t keep, bool last, int user) {
        if (!open) { sink.push_back({user, {}}); open = true; }
        for (int j = 0; j < 8; j++)
            if (keep & (1u << j)) sink.back().bytes.push_back((uint8_t)(data >> (8 * j)));
        if (last) open = false;
    };
    if (ho_acc) collect(host_frames, host_open, ho_d, ho_k, ho_l, 0);
    if (pc_acc) collect(pcm_frames, pcm_open, pc_d, pc_k, pc_l, pc_u);
    if (tsx) ts_beats.push_back(ts_d);
}

static void run(int cycles) { for (int c = 0; c < cycles; c++) tick(); }
static void drain(int settle = 200, int guard = 40000) {
    for (int c = 0; c < guard && (!rx_cur.empty() || !rxq.empty()); c++) tick();
    run(settle);
}

static void axi_write(uint16_t a, uint32_t d) {
    dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
    dut->s_axi_wdata = d; dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
    dut->s_axi_bready = 1;
    for (int g = 0; g < 4096; g++) { tick(); if (g_pre.aw_acc) break; }
    dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
    for (int g = 0; g < 4096; g++) { tick(); if (g_pre.b_v) break; }
    dut->s_axi_bready = 0;
}

static uint32_t axi_read(uint16_t a) {
    dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
    for (int g = 0; g < 4096; g++) { tick(); if (g_pre.ar_acc) break; }
    dut->s_axi_arvalid = 0;
    uint32_t d = 0;
    for (int g = 0; g < 4096; g++) { tick(); if (g_pre.r_v) { d = g_pre.r_d; break; } }
    dut->s_axi_rready = 0;
    return d;
}

enum {
    A_ID = 0x000, A_MAC_ALO = 0x108, A_MAC_AHI = 0x10C,
    A_PTP_CTRL = 0x500, A_PTP_INCR = 0x504,
    A_TCAM_KEY_LO = 0x704, A_TCAM_KEY_HI = 0x708,
    A_TCAM_MASK_LO = 0x70C, A_TCAM_MASK_HI = 0x710, A_TCAM_ACTION = 0x714,
    A_TCAM_CMD = 0x718,
    A_STRM_SEL = 0x800, A_SW_CTRL = 0x810,
    A_SW_SID_LO = 0x814, A_SW_SID_HI = 0x818,
    A_SW_FMT_LO = 0x824, A_SW_FMT_HI = 0x828,
    // gh #64: the gPTP control-plane words. Both groups are SHAPE-FREE -
    // they describe the port's time-aware neighbour, not the stream shape -
    // so every shape this file elaborates must answer them identically.
    A_CLKV_CTRL = 0x778, A_CLKV_STAT = 0x77C,
    A_ASP_LO = 0x7DC, A_ASP_HI = 0x7E0, A_ASP_CMD = 0x7E4,
};

static const uint8_t STATION[6] = {0x02, 0x00, 0x00, 0x00, 0x00, 0x01};

static std::vector<uint8_t> eth_frame(const uint8_t dst[6], uint16_t et,
                                      uint8_t marker, size_t len = 64) {
    std::vector<uint8_t> f(len, 0);
    memcpy(f.data(), dst, 6);
    const uint8_t src[6] = {0x66, 0x77, 0x88, 0x99, 0xAA, 0xBB};
    memcpy(f.data() + 6, src, 6);
    f[12] = (uint8_t)(et >> 8); f[13] = (uint8_t)et;
    for (size_t i = 14; i < len; i++) f[i] = (uint8_t)(marker ^ i);
    return f;
}

static std::vector<uint8_t> gptp_frame(uint8_t b14, uint16_t seq, size_t len = 68) {
    std::vector<uint8_t> f(len, 0);
    const uint8_t dst[6] = {0x01, 0x80, 0xC2, 0x00, 0x00, 0x0E};
    memcpy(f.data(), dst, 6);
    memcpy(f.data() + 6, STATION, 6);
    f[12] = 0x88; f[13] = 0xF7;
    f[14] = b14; f[15] = 0x02; f[16] = 0x00; f[17] = 54;
    f[44] = (uint8_t)(seq >> 8); f[45] = (uint8_t)seq;
    return f;
}

static std::vector<uint8_t> aaf_frame(const uint8_t sid[8], uint8_t seq, uint8_t pay0) {
    std::vector<uint8_t> f(120, 0);
    const uint8_t dmac[6] = {0x91, 0xE0, 0xF0, 0x00, 0x2A, 0x02};
    memcpy(f.data(), dmac, 6);
    memcpy(f.data() + 6, sid, 6);
    f[12] = 0x22; f[13] = 0xF0;
    f[14] = 0x02; f[15] = 0x81; f[16] = seq;
    memcpy(f.data() + 18, sid, 8);
    f[26] = 0x00; f[27] = 0x00; f[28] = 0x10; f[29] = 0x00;
    f[30] = 0x02; f[31] = (uint8_t)(0x05 << 4); f[32] = 2; f[33] = 32;
    f[34] = 0x00; f[35] = 0x30;
    for (int i = 0; i < 48; i++) f[38 + i] = (uint8_t)(pay0 + i);
    return f;
}

static bool bytes_equal(const std::vector<uint8_t>& a, const std::vector<uint8_t>& b) {
    return a.size() == b.size() && memcmp(a.data(), b.data(), a.size()) == 0;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vmilan_datapath;

    printf("=== hostplane SMOKE shape %s (N=%d, %d MHz) ===\n",
           SHAPE_NAME, NSTREAMS_TB, MILAN_CLK_TB / 1000000);
    printf("LTAP same-cycle staging fixed 2026-07-26 (cascade walk)\n");

    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
    dut->s_axi_bready = dut->s_axi_rready = 0;
    dut->i_mac_speed = 2; dut->i_link_up = 1; dut->i_full_duplex = 1;
    dut->i_mac_events = 0;
    dut->i_ethrx_tgl = 0; dut->i_ethtx_tgl = 0; dut->i_ethact_tgl = 0;
    dut->i_mmcm_locked = 1; dut->i_mmcm_drp_do = 0; dut->i_mmcm_drp_rdy = 0;
    dut->i_mmcm_ps_done = 0;
    for (int i = 0; i < 8; i++) tick();
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    for (int i = 0; i < 8; i++) tick();

    ck("ID == 'MILN'", axi_read(A_ID), 0x4D494C4E);
    // gh #64 J3/J4: the gPTP plane is the SAME at every shape. A stream
    // count cannot change what the neighbour port is capable of, nor how
    // many bridges an Announce traversed - so if either group ever became
    // shape-dependent, these two lines are where it would show.
    axi_write(A_CLKV_CTRL, 0x00000FF5);        // SYNC_OK | AS_CAPABLE | lease
#ifdef FABRIC_GPTP_TB
    // #116: the fabric publication bank owns live health in product shapes.
    // Retained software writes remain ABI-safe but cannot forge asCapable.
    ck("J3 fabric owner rejects software asCapable", (axi_read(A_CLKV_STAT) >> 16) & 1, 0);
#else
    ck("J3 software asCapable leased at this shape", (axi_read(A_CLKV_STAT) >> 16) & 1, 1);
#endif
    axi_write(A_ASP_LO, 0xFFFE0210); axi_write(A_ASP_HI, 0x3CC0C6FF);
    axi_write(A_ASP_CMD, 0x80000100);          // commit -> slot 1
    axi_write(A_ASP_CMD, 0x40000002);          // publish GM + 1 bridge
    ck("J4 AS_PATH publish at this shape", axi_read(A_ASP_CMD), 0x00000012);
    axi_write(A_ASP_CMD, 0x40000000);          // back to the legacy arm
    axi_write(A_MAC_ALO, 0x00000002);
    axi_write(A_MAC_AHI, 0x00000100);
    axi_write(A_PTP_INCR, 8u << 24);
    axi_write(A_PTP_CTRL, 1);
    // driver-style TCAM shield (MAAP dynamic pool blacklisted)
    axi_write(A_TCAM_KEY_LO,  0xF0000000);
    axi_write(A_TCAM_KEY_HI,  0x000091E0);
    axi_write(A_TCAM_MASK_LO, 0xFFFF0000);
    axi_write(A_TCAM_MASK_HI, 0x0000FFFF);
    axi_write(A_TCAM_ACTION,  0x1);
    axi_write(A_TCAM_CMD,     0x10100);

    const uint8_t sidB[8] = {0x03, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x01};
#if NSTREAMS_TB > 1
    // bind stream 1 so a shield-dropped AAF stream runs alongside (N>1 only:
    // window idx 0 is the live ACMP alias - never override it from a TB)
    axi_write(A_STRM_SEL, 0x001);
    axi_write(A_SW_SID_LO, 0x00030001);
    axi_write(A_SW_SID_HI, 0x03000000);
    axi_write(A_SW_FMT_LO, 2u << 22);
    axi_write(A_SW_FMT_HI, 0x02050220);
    axi_write(A_SW_CTRL, (1u << 1) | 1u);
    // engine-backed commit barrier: the LCTX port-B readback stalls until
    // the context engine has applied the staged CFG words (window ABI) -
    // traffic injected before that races the bind
    ck("stream 1 CTRL readback (engine port B)", axi_read(A_SW_CTRL), 0x3);
#endif

    static const uint8_t BCAST[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
    auto arp = eth_frame(BCAST, 0x0806, 0x5A, 64);
    auto uni = eth_frame(STATION, 0x0800, 0xA5, 64);
    auto evt = gptp_frame(0x12, 0xBEEF);         // pdelay_req EVENT

    size_t h0 = host_frames.size(), t0 = ts_beats.size(), p0 = pcm_frames.size();
#if NSTREAMS_TB > 1
    rxq.push_back(aaf_frame(sidB, 10, 0x30));
#else
    (void)sidB; (void)aaf_frame;
#endif
    rxq.push_back(arp);
    rxq.push_back(uni);
    rxq.push_back(evt);
#if NSTREAMS_TB > 1
    rxq.push_back(aaf_frame(sidB, 11, 0x40));
#endif
    drain();

    ck("exactly 3 host frames delivered", host_frames.size() - h0, 3);
    if (host_frames.size() - h0 == 3) {
        ck("host[0] broadcast ARP byte-exact", bytes_equal(host_frames[h0 + 0].bytes, arp), 1);
        ck("host[1] unicast-to-station byte-exact", bytes_equal(host_frames[h0 + 1].bytes, uni), 1);
        ck("host[2] gPTP peer-multicast byte-exact", bytes_equal(host_frames[h0 + 2].bytes, evt), 1);
    }
    ck("RX event: exactly one 2-beat ts record", ts_beats.size() - t0, 2);
    if (ts_beats.size() - t0 == 2) {
        ck("record seq=0xBEEF dir=RX",
           (unsigned long)(((ts_beats[t0 + 1] >> 8) & 0xFFFF) | (ts_beats[t0 + 1] & 1)), 0xBEEF);
    }
#if NSTREAMS_TB > 1
    ck("bound AAF consumed by fabric (2 ring frames)", pcm_frames.size() - p0, 2);
#else
    ck("no ring traffic in unbound shape", pcm_frames.size() - p0, 0);
#endif

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld   shape: %s\n", checks, fails, SHAPE_NAME);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
