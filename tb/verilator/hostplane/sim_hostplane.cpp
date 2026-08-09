// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Host-plane coverage harness: milan_datapath in the SILICON SHAPE (cfg_ax8x8
// -> N_STREAMS=8, MILAN_CLK_FREQ_HZ=100e6, I2S front-end, playback pruned,
// PB_PREFILL_C at its silicon default - see README.md for the derivation).
//
// The regression class this suite exists for (2026-07-25): silicon where the
// HOST plane is dead (zero frames on the host RX AXIS lane, zero ts records)
// while every fabric-autonomous path (AAF talker, CRF, SRP, ADP) runs
// perfectly - and the default-shape suites stay green. Every case here
// asserts on the real wiring path of a host-facing lane WITH stream traffic
// running concurrently, in the exact elaboration silicon ships.
//
//   [A] host-frame delivery : broadcast ARP + unicast-to-station + gPTP peer
//       multicast each enter MAC-RX and MUST emerge on the host RX AXIS lane
//       while bound-stream AAF RX traffic and the AAF talker run.
//   [B] ts-record production: one 2-beat record per PTP EVENT frame on TX and
//       on RX (record contract v2.1, docs/findings/PTP_TS_METADATA_FIX.md);
//       general messages produce none.
//   [C] filter correctness  : bound-stream AVTP never leaks to the host lane
//       (TCAM shield programmed exactly like the driver); host frames never
//       leak into the media path (ring/counters untouched).
//   [D] observer purity     : with the host lane backpressured for long
//       windows, latency taps + telemetry still update and NO stream data is
//       lost or reordered on release; the LTAP enable knob cannot perturb
//       stream data (runtime half - the structural half is
//       syn/yosys/check_tap_purity.sh).
//
// Lane convention: LITTLE-endian byte lanes everywhere (first wire byte in
// tdata[7:0]) - the MAC-side truth silicon-proven by adp_advertiser and the
// BIG_ENDIAN(0) ptp_ts_top instantiation (the milan_dp legacy harness's
// big-lane frames only pass because its paths are byte-transparent).

#include "Vmilan_datapath.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>
#include <deque>

#ifndef NSTREAMS_TB
#define NSTREAMS_TB 8
#endif
#ifndef MILAN_CLK_TB
#define MILAN_CLK_TB 100000000
#endif

static Vmilan_datapath* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, unsigned long got, unsigned long exp) {
    bool ok = (got == exp);
    checks++; if (!ok) fails++;
    printf("  [%s] %-52s got=0x%lx exp=0x%lx\n", ok ? "PASS" : "FAIL", what, got, exp);
}

// ======================= clock + universal bus pump =========================
// ONE tick() drives every AXIS master from its pending-frame queue and samples
// every AXIS sink pre-edge (post-edge monitors miss single-cycle beats at
// backpressure-release edges - the ptp_ts TB lesson). CSR accessors run on the
// same tick so no beat can ever be double-presented while a poll loop spins.

struct Collected { int user; std::vector<uint8_t> bytes; };

static std::deque<std::vector<uint8_t>> rxq;    // MAC-RX injection queue
static std::deque<std::vector<uint8_t>> txq;    // host-TX-DMA injection queue
static std::vector<uint8_t> rx_cur, tx_cur;     // in-flight frames
static size_t rx_beat = 0, tx_beat = 0;

static std::vector<Collected> host_frames;      // m_axis_rx (host RX lane)
static std::vector<Collected> mactx_frames;     // m_axis_mac_tx
static std::vector<Collected> pcm_frames;       // m_axis_pcm (PCM ring lane)
static std::vector<uint64_t>  ts_beats;         // m_axis_ts
static bool host_open = false, mactx_open = false, pcm_open = false;

static int  g_host_tready = 1;                  // case D backpressure lever

// pre-edge AXI-Lite samples for the CSR BFM
struct Pre { bool aw_acc, b_v, ar_acc, r_v; uint32_t r_d; };
static Pre g_pre;

static void drive_streams() {
    if (rx_cur.empty() && !rxq.empty()) { rx_cur = rxq.front(); rxq.pop_front(); rx_beat = 0; }
    if (tx_cur.empty() && !txq.empty()) { tx_cur = txq.front(); txq.pop_front(); tx_beat = 0; }

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

    if (!tx_cur.empty()) {
        size_t nbeats = (tx_cur.size() + 7) / 8;
        uint64_t d = 0;
        for (int j = 0; j < 8; j++) {
            size_t i = tx_beat * 8 + j;
            if (i < tx_cur.size()) d |= (uint64_t)tx_cur[i] << (8 * j);
        }
        dut->s_axis_tx_tdata = d; dut->s_axis_tx_tkeep = 0xFF;   // DMA reads full beats
        dut->s_axis_tx_tvalid = 1; dut->s_axis_tx_tlast = (tx_beat == nbeats - 1);
    } else {
        dut->s_axis_tx_tvalid = 0; dut->s_axis_tx_tlast = 0;
    }

    dut->m_axis_rx_tready     = g_host_tready;
    dut->m_axis_ts_tready     = 1;
    dut->m_axis_pcm_tready    = 1;
    dut->m_axis_mac_tx_tready = 1;
}

static void collect(std::vector<Collected>& sink, bool& open, uint64_t data,
                    uint8_t keep, bool last, int user) {
    if (!open) { sink.push_back({user, {}}); open = true; }
    for (int j = 0; j < 8; j++)
        if (keep & (1u << j)) sink.back().bytes.push_back((uint8_t)(data >> (8 * j)));
    if (last) open = false;
}

static void tick() {
    drive_streams();
    // low phase: combinational readys/valids settle - sample what THIS edge commits
    // clk_tdm_i (item-4 TDM master serial domain) is driven on every shape:
    // the port exists unconditionally, and an undriven clock is how a
    // front-end sits silent while every gate stays green.
    dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->i_ps_clk = 0;
    dut->clk_tdm_i = 0;
    dut->eval();
    bool rx_acc  = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
    bool tx_acc  = dut->s_axis_tx_tvalid && dut->s_axis_tx_tready;
    bool ho_acc  = dut->m_axis_rx_tvalid && dut->m_axis_rx_tready;
    uint64_t ho_d = dut->m_axis_rx_tdata;  uint8_t ho_k = dut->m_axis_rx_tkeep;
    bool ho_l = dut->m_axis_rx_tlast;
    bool mt_acc  = dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready;
    uint64_t mt_d = dut->m_axis_mac_tx_tdata; uint8_t mt_k = dut->m_axis_mac_tx_tkeep;
    bool mt_l = dut->m_axis_mac_tx_tlast;
    bool pc_acc  = dut->m_axis_pcm_tvalid && dut->m_axis_pcm_tready;
    uint64_t pc_d = dut->m_axis_pcm_tdata;  uint8_t pc_k = dut->m_axis_pcm_tkeep;
    bool pc_l = dut->m_axis_pcm_tlast;     int pc_u = dut->m_axis_pcm_tuser;
    bool tsx     = dut->m_axis_ts_tvalid && dut->m_axis_ts_tready;
    uint64_t ts_d = dut->m_axis_ts_tdata;
    g_pre.aw_acc = dut->s_axi_awready && dut->s_axi_wready;
    g_pre.b_v    = dut->s_axi_bvalid;
    g_pre.ar_acc = dut->s_axi_arready;
    g_pre.r_v    = dut->s_axi_rvalid;
    g_pre.r_d    = dut->s_axi_rdata;
    // high phase: commit
    dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->i_ps_clk = 1;
    dut->clk_tdm_i = 1;
    dut->eval();
    if (rx_acc) { if (++rx_beat >= (rx_cur.size() + 7) / 8) { rx_cur.clear(); rx_beat = 0; } }
    if (tx_acc) { if (++tx_beat >= (tx_cur.size() + 7) / 8) { tx_cur.clear(); tx_beat = 0; } }
    if (ho_acc) collect(host_frames, host_open, ho_d, ho_k, ho_l, 0);
    if (mt_acc) collect(mactx_frames, mactx_open, mt_d, mt_k, mt_l, 0);
    if (pc_acc) collect(pcm_frames, pcm_open, pc_d, pc_k, pc_l, pc_u);
    if (tsx)    ts_beats.push_back(ts_d);
}

static void run(int cycles) { for (int c = 0; c < cycles; c++) tick(); }

// drain: run until both injection queues are empty + settle margin
static void drain(int settle = 200, int guard = 40000) {
    for (int c = 0; c < guard && (!rx_cur.empty() || !rxq.empty()
                                  || !tx_cur.empty() || !txq.empty()); c++) tick();
    run(settle);
}

// ============================ AXI4-Lite CSR BFM =============================
static void axi_write(uint16_t a, uint32_t d) {
    dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
    dut->s_axi_wdata = d;  dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
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

// ---- register offsets (docs/reference/REGISTER_MAP.md) ----
enum {
    A_ID = 0x000, A_VERSION = 0x004,
    A_MAC_ALO = 0x108, A_MAC_AHI = 0x10C,
    A_PTP_CTRL = 0x500, A_PTP_INCR = 0x504,
    A_AAF_CTRL = 0x654, A_AAF_FRAMES = 0x660,
    A_PCMRX_CNT = 0x6C4,
    A_TCAM_CTRL = 0x700, A_TCAM_KEY_LO = 0x704, A_TCAM_KEY_HI = 0x708,
    A_TCAM_MASK_LO = 0x70C, A_TCAM_MASK_HI = 0x710, A_TCAM_ACTION = 0x714,
    A_TCAM_CMD = 0x718,
    A_STRM_SEL = 0x800, A_STRM_SNAP = 0x804, A_SW_CTRL = 0x810,
    A_SW_SID_LO = 0x814, A_SW_SID_HI = 0x818,
    A_SW_FMT_LO = 0x824, A_SW_FMT_HI = 0x828, A_SW_CNT0 = 0x830, A_SW_PDUS = 0x858,
    A_ACMPL_DBG = 0x6E8,   //! {classify_cnt, fc_cnt, fc_flags, base_hits}
    A_LTAP_CTRL = 0x870, A_LTAP_RX_EPOCH = 0x894, A_LTAP_RX_INFO = 0x898,
};

static void snap_and_wait() {
    axi_write(A_STRM_SNAP, 1);
    for (int g = 0; g < 256; g++)
        if ((axi_read(A_STRM_SNAP) & 1) == 0) return;
}

// ============================ frame constructors ============================
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

// gPTP frame (peer multicast, 0x88F7). b14 = {majorSdoId nibble, msgType}:
// 0x12 pdelay_req (EVENT), 0x13 pdelay_resp (EVENT), 0x18 follow_up (general),
// 0x1B announce (general). Event <=> msgType[3] == 0.
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

// AAF PDU (same shape the milan_dp NxN harness silicon-matched): 120-byte
// frame, DMAC in the MAAP dynamic pool (91:E0:F0:00:...), 48-byte payload.
static std::vector<uint8_t> aaf_frame(const uint8_t sid[8], uint8_t seq, uint8_t pay0) {
    std::vector<uint8_t> f(120, 0);
    const uint8_t dmac[6] = {0x91, 0xE0, 0xF0, 0x00, 0x2A, 0x02};
    memcpy(f.data(), dmac, 6);
    memcpy(f.data() + 6, sid, 6);
    f[12] = 0x22; f[13] = 0xF0;
    f[14] = 0x02;                                // AAF
    f[15] = 0x81;                                // sv, tv
    f[16] = seq;
    memcpy(f.data() + 18, sid, 8);
    f[26] = 0x00; f[27] = 0x00; f[28] = 0x10; f[29] = 0x00;  // avtp_ts (not late/early)
    f[30] = 0x02;                                // format INT32
    f[31] = (uint8_t)(0x05 << 4);                // nsr 48 kHz
    f[32] = 2;                                   // channels_per_frame
    f[33] = 32;                                  // bit depth
    f[34] = 0x00; f[35] = 0x30;                  // data_len 48
    for (int i = 0; i < 48; i++) f[38 + i] = (uint8_t)(pay0 + i);
    return f;
}

static bool bytes_equal(const std::vector<uint8_t>& a, const std::vector<uint8_t>& b) {
    if (a.size() != b.size()) return false;
    return memcmp(a.data(), b.data(), a.size()) == 0;
}

// count MAC-TX frames whose ethertype is `et` starting at index `from`
static int mactx_count_et(size_t from, uint16_t et) {
    int n = 0;
    for (size_t i = from; i < mactx_frames.size(); i++) {
        const auto& b = mactx_frames[i].bytes;
        if (b.size() >= 14 && b[12] == (uint8_t)(et >> 8) && b[13] == (uint8_t)et) n++;
    }
    return n;
}

// =============================== the campaign ===============================
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vmilan_datapath;

    printf("=== hostplane: milan_datapath SILICON SHAPE (N=%d, %d MHz) ===\n",
           NSTREAMS_TB, MILAN_CLK_TB / 1000000);
    printf("LTAP same-cycle staging FIXED 2026-07-26 (cascade walk in KL_aaf_latency_taps).\n");

    // ---- reset with the SoC's stub levels (milan_soc.py ports dict) ----
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

    // ---- [S] silicon-flavored bring-up over the CSR plane ----
    printf("[S] bring-up: identity + station MAC + PTP + TCAM shield + binds\n");
    ck("ID == 'MILN'", axi_read(A_ID), 0x4D494C4E);
    ck("VERSION major 1", axi_read(A_VERSION) >> 16, 1);
    // station MAC exactly as kl-eth programs it (LSB-first packing)
    axi_write(A_MAC_ALO, 0x00000002);
    axi_write(A_MAC_AHI, 0x00000100);
    // PHC armed like the flash init: 8 ns/tick nominal, counter enabled
    axi_write(A_PTP_INCR, 8u << 24);
    axi_write(A_PTP_CTRL, 1);
    // TCAM shield entry 0 - the exact driver programming that keeps the AVTP
    // multicast flood off the CPU (blacklist the MAAP dynamic pool
    // 91:E0:F0:00:xx:xx) while default_pass=1 delivers everything else.
    axi_write(A_TCAM_KEY_LO,  0xF0000000);
    axi_write(A_TCAM_KEY_HI,  0x000091E0);
    axi_write(A_TCAM_MASK_LO, 0xFFFF0000);
    axi_write(A_TCAM_MASK_HI, 0x0000FFFF);
    axi_write(A_TCAM_ACTION,  0x1);              // drop on match
    axi_write(A_TCAM_CMD,     0x10100);          // commit | valid | idx 0
    ck("TCAM default_pass still 1", axi_read(A_TCAM_CTRL) & 1, 1);
    // bind listener stream 1 through the 0x800 window (stage SID, commit
    // CTRL = en | DMA-route - the window ABI, stage-before-CTRL)
    const uint8_t sidB[8] = {0x03, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x01};
    const uint32_t FMT_HI = 0x02050220, FMT_LO = 2u << 22;
    axi_write(A_STRM_SEL, 0x001);
    axi_write(A_SW_SID_LO, 0x00030001);
    axi_write(A_SW_SID_HI, 0x03000000);
    axi_write(A_SW_FMT_LO, FMT_LO);
    axi_write(A_SW_FMT_HI, FMT_HI);
    axi_write(A_SW_CTRL, (1u << 1) | 1u);        // en + DMA flag
    ck("stream 1 CTRL readback (engine port B)", axi_read(A_SW_CTRL), 0x3);
    // AAF talker t0 armed (VID-2 rule: bit-preserving 0x00020003) so a
    // fabric-autonomous TX stream runs under every case below
    axi_write(A_AAF_CTRL, 0x00020003);

    // ======================= [A] host-frame delivery =======================
    printf("[A] host RX delivery under concurrent AAF stream traffic\n");
    static const uint8_t BCAST[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
    auto arp = eth_frame(BCAST, 0x0806, 0x5A, 64);
    auto uni = eth_frame(STATION, 0x0800, 0xA5, 64);
    auto gen = gptp_frame(0x18, 0x0100);         // follow_up: general, no record
    size_t h0 = host_frames.size(), p0 = pcm_frames.size();
    rxq.push_back(aaf_frame(sidB, 10, 0x30));
    rxq.push_back(arp);
    rxq.push_back(aaf_frame(sidB, 11, 0x40));
    rxq.push_back(uni);
    rxq.push_back(aaf_frame(sidB, 12, 0x50));
    rxq.push_back(gen);
    rxq.push_back(aaf_frame(sidB, 13, 0x60));
    drain();
    ck("exactly 3 host frames delivered", host_frames.size() - h0, 3);
    if (host_frames.size() - h0 == 3) {
        ck("host[0] = broadcast ARP byte-exact", bytes_equal(host_frames[h0 + 0].bytes, arp), 1);
        ck("host[1] = unicast-to-station byte-exact", bytes_equal(host_frames[h0 + 1].bytes, uni), 1);
        ck("host[2] = gPTP peer-multicast byte-exact", bytes_equal(host_frames[h0 + 2].bytes, gen), 1);
    }
    ck("concurrent AAF landed on the PCM ring (4)", pcm_frames.size() - p0, 4);
    bool ring_ok = true;
    for (size_t i = p0; i < pcm_frames.size(); i++)
        if (pcm_frames[i].user != 1 || pcm_frames[i].bytes.size() != 48) ring_ok = false;
    ck("ring frames tuser=1, 48-byte payloads", ring_ok, 1);
    // fabric-autonomous talker is alive in this same shape (the regression's
    // control group: fabric TX fine while the host plane is dead)
    uint32_t fr0 = axi_read(A_AAF_FRAMES);
    for (int g = 0; g < 40 && axi_read(A_AAF_FRAMES) == fr0; g++) run(2048);
    ck("AAF talker t0 emitting concurrently", axi_read(A_AAF_FRAMES) > fr0, 1);

    // ======================= [B] ts-record production =======================
    printf("[B] ts-record production (record contract v2.1)\n");
    // B1: RX event (pdelay_req) with stream traffic in the same window
    size_t t0 = ts_beats.size();
    rxq.push_back(aaf_frame(sidB, 14, 0x70));
    rxq.push_back(gptp_frame(0x12, 0xBEEF));     // pdelay_req EVENT
    rxq.push_back(aaf_frame(sidB, 15, 0x80));
    drain();
    ck("RX event: exactly one 2-beat record", ts_beats.size() - t0, 2);
    if (ts_beats.size() - t0 == 2) {
        uint64_t w0 = ts_beats[t0], w1 = ts_beats[t0 + 1];
        ck("RX record ns nonzero", w0 != 0, 1);
        ck("RX record dir=RX",     (unsigned long)(w1 & 1), 0);
        ck("RX record marker=1",   (unsigned long)((w1 >> 1) & 1), 1);
        ck("RX record mtype=2",    (unsigned long)((w1 >> 4) & 0xF), 2);
        ck("RX record seq=0xBEEF", (unsigned long)((w1 >> 8) & 0xFFFF), 0xBEEF);
    }
    // B2: RX general (follow_up) -> no record
    t0 = ts_beats.size();
    rxq.push_back(gptp_frame(0x18, 0xD00D));
    drain();
    ck("RX general: no record", ts_beats.size() - t0, 0);
    // B3: TX event (pdelay_resp) through the host TX DMA port
    t0 = ts_beats.size();
    size_t m0 = mactx_frames.size();
    txq.push_back(gptp_frame(0x13, 0x1234, 72)); // full-beat padded TX frame
    drain();
    ck("TX event frame egressed on MAC port", mactx_count_et(m0, 0x88F7), 1);
    ck("TX event: exactly one 2-beat record", ts_beats.size() - t0, 2);
    if (ts_beats.size() - t0 == 2) {
        uint64_t w1 = ts_beats[t0 + 1];
        ck("TX record dir=TX",     (unsigned long)(w1 & 1), 1);
        ck("TX record marker=1",   (unsigned long)((w1 >> 1) & 1), 1);
        ck("TX record mtype=3",    (unsigned long)((w1 >> 4) & 0xF), 3);
        ck("TX record seq=0x1234", (unsigned long)((w1 >> 8) & 0xFFFF), 0x1234);
    }
    // B4: TX general (announce) -> frame egresses, no record
    t0 = ts_beats.size(); m0 = mactx_frames.size();
    txq.push_back(gptp_frame(0x1B, 0x4444, 72));
    drain();
    ck("TX general frame egressed on MAC port", mactx_count_et(m0, 0x88F7), 1);
    ck("TX general: no record", ts_beats.size() - t0, 0);

    // ======================= [C] filter correctness =========================
    printf("[C] no-leak both ways (TCAM shield / media isolation)\n");
    // C1: bound-stream AVTP must NOT reach the host lane (shield in force)
    size_t hc = host_frames.size(), pc = pcm_frames.size();
    uint32_t pcm_cnt0 = axi_read(A_PCMRX_CNT) & 0xFFFF;
    rxq.push_back(aaf_frame(sidB, 16, 0x11));
    rxq.push_back(aaf_frame(sidB, 17, 0x22));
    rxq.push_back(aaf_frame(sidB, 18, 0x33));
    drain();
    ck("bound AVTP: zero leak to host lane", host_frames.size() - hc, 0);
    ck("bound AVTP: fabric consumed all 3 (ring)", pcm_frames.size() - pc, 3);
    ck("bound AVTP: shared depkt count +3",
       (axi_read(A_PCMRX_CNT) & 0xFFFF) - pcm_cnt0, 3);
    // C2: host frames + unknown-sid AVTP must NOT reach the media path
    hc = host_frames.size(); pc = pcm_frames.size();
    pcm_cnt0 = axi_read(A_PCMRX_CNT) & 0xFFFF;
    const uint8_t sidX[8] = {0x05, 0x00, 0x00, 0x00, 0x00, 0x05, 0x00, 0x09};
    rxq.push_back(arp);
    rxq.push_back(uni);
    rxq.push_back(gen);
    rxq.push_back(aaf_frame(sidX, 99, 0x77));    // unknown sid: no table entry
    drain();
    ck("host frames: zero leak to PCM ring", pcm_frames.size() - pc, 0);
    ck("host frames: depkt count unchanged",
       (axi_read(A_PCMRX_CNT) & 0xFFFF) - pcm_cnt0, 0);
    ck("host frames delivered meanwhile (3)", host_frames.size() - hc, 3);
    axi_write(A_STRM_SEL, 0x001);
    snap_and_wait();
    //! Milan v1.2 Table 5.6: FRAMES_RX counts OBSERVATION INTERVALS with
    //! traffic (<= 1 s each; LDIAG_IVAL_CYC_P=1024 in this build), so the
    //! 9 frames of the A/B/C bursts read as 1..9 ticks depending on how
    //! bursts fall on the tick grid - never more than the frame total.
    //! The frame-accurate isolation proof is the depkt PDUS attribution,
    //! which stays per-frame by design.
    { unsigned long frx = axi_read(A_SW_CNT0 + 9 * 4);
      ck("stream1 FRAMES_RX interval ticks in 1..9",
         frx >= 1 && frx <= 9, 1); }
    ck("stream1 depkt PDUS total 9 (per-frame, isolated)",
       axi_read(A_SW_PDUS) & 0xFFFF, 9);
    // C3: WHITELIST mode (default_pass=0 + accept entries) - the kernel's
    // non-promisc posture. Station MAC + broadcast + gPTP peer multicast
    // accepted; an unknown unicast dropped; the bound stream keeps flowing
    // pre-filter (media path must not depend on the kernel filter config).
    axi_write(A_TCAM_KEY_LO, 0x00000001); axi_write(A_TCAM_KEY_HI, 0x0200);
    axi_write(A_TCAM_MASK_LO, 0xFFFFFFFF); axi_write(A_TCAM_MASK_HI, 0xFFFF);
    axi_write(A_TCAM_ACTION, 0x0); axi_write(A_TCAM_CMD, 0x10101);
    axi_write(A_TCAM_KEY_LO, 0xFFFFFFFF); axi_write(A_TCAM_KEY_HI, 0xFFFF);
    axi_write(A_TCAM_CMD, 0x10102);
    axi_write(A_TCAM_KEY_LO, 0xC200000E); axi_write(A_TCAM_KEY_HI, 0x0180);
    axi_write(A_TCAM_CMD, 0x10103);
    axi_write(A_TCAM_CTRL, 0x0);                 // whitelist: default DROP
    hc = host_frames.size(); pc = pcm_frames.size();
    static const uint8_t OTHER[6] = {0x02, 0x00, 0x00, 0x00, 0x00, 0x99};
    rxq.push_back(arp);
    rxq.push_back(eth_frame(OTHER, 0x0800, 0x3C, 64));  // not ours: dropped
    rxq.push_back(uni);
    rxq.push_back(aaf_frame(sidB, 19, 0x44));           // table miss, fabric eats
    rxq.push_back(gen);
    drain();
    ck("whitelist: exactly our 3 host frames", host_frames.size() - hc, 3);
    ck("whitelist: foreign unicast dropped",
       host_frames.size() - hc == 3
       && bytes_equal(host_frames[hc + 0].bytes, arp)
       && bytes_equal(host_frames[hc + 1].bytes, uni)
       && bytes_equal(host_frames[hc + 2].bytes, gen), 1);
    ck("whitelist: bound AAF still consumed pre-filter", pcm_frames.size() - pc, 1);
    // back to the blacklist shield posture for case D
    axi_write(A_TCAM_CMD, 0x10001);              // remove idx 1 (valid=0)
    axi_write(A_TCAM_CMD, 0x10002);
    axi_write(A_TCAM_CMD, 0x10003);
    axi_write(A_TCAM_CTRL, 0x1);

    // ================== [D] observer purity under stress ====================
    printf("[D] host-lane backpressure: taps/telemetry live, no stream loss\n");
    // D1: host lane STALLED; shield-dropped AAF traffic must keep flowing to
    // the ring and the latency taps must keep sampling (the exact silicon
    // situation: host RX dead, fabric perfect).
    g_host_tready = 0;
    uint32_t ltap_s0 = axi_read(A_LTAP_RX_INFO) & 0xFFFF;
    pc = pcm_frames.size();
    for (int i = 0; i < 6; i++) rxq.push_back(aaf_frame(sidB, (uint8_t)(20 + i), (uint8_t)(0x90 + 16 * i)));
    drain();
    ck("stalled host: 6 AAF frames reached the ring", pcm_frames.size() - pc, 6);
    bool order_ok = true;
    for (int i = 0; i < 6; i++) {
        const auto& b = pcm_frames[pc + i].bytes;
        if (b.size() != 48 || b[0] != (uint8_t)(0x90 + 16 * i)) order_ok = false;
    }
    ck("stalled host: ring payloads in order, byte-exact", order_ok, 1);
    uint32_t ltap_s1 = axi_read(A_LTAP_RX_INFO) & 0xFFFF;
    ck("stalled host: LTAP RX samples advanced", ltap_s1 > ltap_s0, 1);
    ck("stalled host: LTAP RX epoch latched nonzero", axi_read(A_LTAP_RX_EPOCH) != 0, 1);
    // D2: a host frame wedges at the filter while stalled; frames behind it
    // must come through IN ORDER with nothing lost once pressure releases.
    size_t hd = host_frames.size(); pc = pcm_frames.size();
    rxq.push_back(uni);                          // stalls at the filter output
    rxq.push_back(aaf_frame(sidB, 26, 0x21));    // queued behind the wedge
    rxq.push_back(aaf_frame(sidB, 27, 0x43));
    run(3000);                                   // long stall window
    ck("still stalled: no host beat escaped", host_frames.size() - hd, 0);
    g_host_tready = 1;                           // release
    drain();
    ck("release: wedged host frame delivered", host_frames.size() - hd, 1);
    if (host_frames.size() - hd == 1)
        ck("release: host frame byte-exact", bytes_equal(host_frames[hd].bytes, uni), 1);
    ck("release: both queued AAF frames on ring", pcm_frames.size() - pc, 2);
    if (pcm_frames.size() - pc == 2) {
        ck("release: ring order preserved (0x21 then 0x43)",
           pcm_frames[pc].bytes[0] == 0x21 && pcm_frames[pc + 1].bytes[0] == 0x43, 1);
    }
    // D3: the LTAP enable knob must not perturb stream data (runtime purity)
    axi_write(A_LTAP_CTRL, 0x0);                 // taps OFF
    pc = pcm_frames.size();
    rxq.push_back(aaf_frame(sidB, 28, 0x55));
    rxq.push_back(aaf_frame(sidB, 29, 0x66));
    drain();
    ck("taps off: stream data unaffected (2 ring frames)", pcm_frames.size() - pc, 2);
    if (pcm_frames.size() - pc == 2)     // guard: a miss must FAIL, not segfault
        ck("taps off: payload byte-exact", pcm_frames[pc].bytes[0] == 0x55
                                           && pcm_frames[pc + 1].bytes[0] == 0x66, 1);
    axi_write(A_LTAP_CTRL, 0x2);                 // taps back ON
    uint32_t ltap_r0 = axi_read(A_LTAP_RX_INFO) & 0xFFFF;
    pc = pcm_frames.size();
    rxq.push_back(aaf_frame(sidB, 30, 0x77));
    rxq.push_back(aaf_frame(sidB, 31, 0x88));
    drain();
    ck("taps re-enabled: sampling resumes", (axi_read(A_LTAP_RX_INFO) & 0xFFFF) > ltap_r0, 1);
    ck("taps re-enabled: stream data still clean", pcm_frames.size() - pc, 2);
    // D4: telemetry COMPLETENESS - a single AAF frame's RX token must
    // complete on its own (no successor frame, no timeout credit). Found
    // failing 2026-07-25: KL_pcm_route is fully combinational, so the DEPKT
    // and PCM_RING tap stages pulse on the SAME cycle and the chain (one
    // stage credit per cycle) strands the token awaiting RING - RX samples
    // only advance when the NEXT frame's ring edge arrives, so RX_D2
    // actually measures inter-frame gap and the last frame of any burst is
    // never sampled. LTAP_CTRL read shows {rx_active=1, awaited stage 3}.
    run(4000);                                   // let any pending token settle
    uint32_t d4_info0 = axi_read(A_LTAP_RX_INFO);
    rxq.push_back(aaf_frame(sidB, 32, 0x99));    // exactly ONE frame
    drain(2000);                                 // < TIMEOUT_C: no abort credit
    uint32_t d4_info1 = axi_read(A_LTAP_RX_INFO);
    ck("single-frame RX token completes (DEPKT/RING same-cycle)",
       (d4_info1 & 0xFFFF) - (d4_info0 & 0xFFFF), 1);
    ck("single-frame token: no timeout burned",
       (d4_info1 >> 16) - (d4_info0 >> 16), 0);
    printf("  info: LTAP_CTRL status after single frame = 0x%08x "
           "(bit12 rx_active, [15:13] awaited stage)\n", axi_read(A_LTAP_CTRL));

    // D5 (gh #65): PARKED-LANE PURITY. rx_axis_to_dma.tready IS the host
    // lane's ready, and the SRP/ACMP/AECP monitor taps all ride that lane.
    // With the host stalled the producer parks a beat with tvalid held: a
    // tap that samples tvalid alone consumes every parked cycle as a NEW
    // beat, so one wedged frame is seen many times. The ACMP listener's
    // classify counter is the witness - it must advance by EXACTLY one per
    // frame no matter how long the frame sat parked.
    printf("[D5] parked-lane purity: one wedged frame = one tap consumption\n");
    {
        // The tlast beat is the one that matters: KL_acmp_lstn_ctx enters
        // CLASSIFY_S on rxl_r (hdl 1566-1580) and bumps dbg_classify_r there
        // (hdl 1616), then falls straight back to COLLECT_S for a non-ACMP
        // frame. A tvalid-only tap therefore re-latches the SAME parked
        // tlast every other cycle and the counter runs away; a tap qualified
        // on tvalid && tready sees exactly one frame end. Parking beat 0
        // would prove nothing - tlast never parks there.
        g_host_tready = 1;
        uint32_t cls0 = (axi_read(A_ACMPL_DBG) >> 24) & 0xFF;
        size_t hd5 = host_frames.size();
        rxq.push_back(uni);
        // let every beat BUT the last through, then stall the host lane
        int guard = 4000;
        while (guard-- > 0) {
            tick();
            if (host_open && host_frames.back().bytes.size() >= uni.size() - 8)
                break;
        }
        g_host_tready = 0;
        ck("[D5] the frame is parked ON its tlast beat",
           (host_open && host_frames.back().bytes.size() == uni.size() - 8)
               ? 1 : 0, 1);
        run(4000);                               // ...parked for 4000 cycles
        ck("[D5] the tlast beat never escaped while parked",
           host_frames.back().bytes.size(), uni.size() - 8);
        g_host_tready = 1;
        drain();
        uint32_t cls1 = (axi_read(A_ACMPL_DBG) >> 24) & 0xFF;
        ck("[D5] the parked frame was consumed EXACTLY once by the tap",
           (uint8_t)(cls1 - cls0), 1);
        ck("[D5] and delivered to the host exactly once",
           host_frames.size() - hd5, 1);
        ck("[D5] delivered byte-exact",
           bytes_equal(host_frames[hd5].bytes, uni), 1);
    }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
