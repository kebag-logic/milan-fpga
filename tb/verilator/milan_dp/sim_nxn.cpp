/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * P12 NxN integration harness: milan_datapath at N_STREAMS=4, CSR 0x800
 * window -> REAL engines end-to-end (NXN_ARCHITECTURE.md P12 gate):
 *
 *   1. provision listener streams 1..2 THROUGH the window (SID/FMT staged,
 *      CTRL commit -> LCTX CFG words + stream-table entry + route field),
 *      readback of the CFG words through the engine-arbitrated LCTX port B
 *      (the monitor context RAM, not a CSR shadow);
 *   2. feed tagged AAF frames of both streams + an unknown sid on the MAC
 *      RX AXIS: classification tuser rides parser -> monitor -> depkt ->
 *      route; stream 1 (route=DMA flag) lands on the PCM ring output with
 *      tuser=1, stream 2 (route=NULL) is counted but not forwarded;
 *   3. read ISOLATED per-stream counters back through the window with SNAP
 *      (Table 7-157 block from the live LCTX; stream 0 legacy aliases and
 *      idx 3 stay zero); a seq-gap on stream 1 moves ONLY stream 1;
 *   4. talker side: TCTX CFG words written and read back through the live
 *      KL_aaf_packetizer window port.
 *
 * P12 follow-up gates (route flags + talker t>0 arming):
 *   5. route FLAGS {bit1 RENDER, bit0 DMA}: RENDER|DMA renders AND rings
 *      (capture-while-rendering), RENDER-only renders without a ring copy,
 *      NULL suppresses both (render truth = the datapath render-tap valid,
 *      a verilator-public probe - the flat CSRs expose no per-stream tap);
 *   6. talker t>0 arming composition (aaf_stream_en_w, verilator-public):
 *      t1 arms via the window TCTX CTRL[0] commit; enabling lwSRP without
 *      a t1 reservation drops ONLY t1 (t0 rides its bypass, emission keeps
 *      running); the engine-wide MAAP term holds t0 AND t1 alike (mirrors
 *      t0 semantics, one claim engine); window CTRL[0]=0 disarms t1.
 *      t>0 WIRE emission stays structurally impossible at datapath level
 *      (KL_aaf_capture_i2s emits slot 0 only until the item-4 TDM
 *      front-end) - frame-level TCTX-identity emission + per-slot gate
 *      drop are proven in tb/verilator/aaf sim_main_nx [I2T]/[I2T4].
 *      KL_aaf_packetizer window port;
 *   5. N-sink ACMP round: a CONNECT_RX bind of listener context 2 (a
 *      window stream's record-only explicit-sid context) reads back
 *      END-TO-END through the window's ACMP table master (SID/DMAC live,
 *      STATE via SNAP); unbound idx 3 and ctx 0 stay honest zero.
 */

#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <vector>

static Vmilan_datapath* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, unsigned long got, unsigned long exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-46s got=0x%lx exp=0x%lx\n", what, got, exp);
    } else {
        printf("  [ok]   %-46s = 0x%lx\n", what, got);
    }
}

static void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->eval(); }
static void hi() { dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->eval(); }
static void step() { lo(); hi(); }

// ---- AXI4-Lite BFM (same protocol as the milan_dp legacy harness) ----
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
    A_ID = 0x000, A_VERSION = 0x004,
    A_AAF_CTRL = 0x654, A_AAF_FRAMES = 0x660, A_LWSRP_CTRL = 0x680,
    A_ADP_CTRL = 0x600, A_ADP_EIDLO = 0x604, A_ADP_EIDHI = 0x608,
    A_AVTPRX_STAT = 0x6B8, A_AVTPRX_FRX = 0x6BC, A_PCMRX_CNT = 0x6C4,
    A_MAAP_CTRL = 0x6CC,
    A_STRM_SEL = 0x800, A_STRM_SNAP = 0x804, A_SW_CTRL = 0x810,
    A_SW_SID_LO = 0x814, A_SW_SID_HI = 0x818, A_SW_DMAC_LO = 0x81C,
    A_SW_DMAC_HI = 0x820, A_SW_FMT_LO = 0x824, A_SW_FMT_HI = 0x828,
    A_SW_STATE = 0x82C, A_SW_CNT0 = 0x830, A_SW_PDUS = 0x858,
};

// route flags (KL_pcm_route / window CTRL[2:1]): bit0 = DMA, bit1 = RENDER
enum { RT_NULL = 0, RT_DMA = 1, RT_RENDER = 2, RT_RENDER_DMA = 3 };

// composed per-stream talker enables (milan_datapath aaf_stream_en_w)
static unsigned tap_stream_en() {
    return dut->rootp->milan_datapath__DOT__aaf_stream_en_w;
}

static void snap_and_wait() {
    axi_write(A_STRM_SNAP, 1);
    for (int g = 0; g < 256; ++g)
        if ((axi_read(A_STRM_SNAP) & 1) == 0) return;
}

// ---- PCM ring collection: {tuser, payload bytes} per AXIS frame ----
struct PcmFrame { int user; std::vector<uint8_t> bytes; };
static std::vector<PcmFrame> pcm_frames;
static bool pcm_open = false;
static long render_beats = 0;   // datapath render-tap beats (public probe)

static void pcm_sample() {
    if (dut->m_axis_pcm_tvalid) {
        if (!pcm_open) { pcm_frames.push_back({(int)dut->m_axis_pcm_tuser, {}}); pcm_open = true; }
        for (int l = 0; l < 8; l++)
            pcm_frames.back().bytes.push_back((dut->m_axis_pcm_tdata >> (8*l)) & 0xFF);
        if (dut->m_axis_pcm_tlast) pcm_open = false;
    }
    if (dut->rootp->milan_datapath__DOT__rend_pcm_tvalid_w) render_beats++;
}

// ---- inject one little-lane frame on the MAC RX port ----
static void inject(const uint8_t* f, size_t len, int drain = 1200) {
    std::vector<uint64_t> beats;
    for (size_t bt = 0; bt < (len + 7) / 8; bt++) {
        uint64_t v = 0;
        for (int j = 0; j < 8; j++)
            if (bt*8 + j < len) v |= (uint64_t)f[bt*8+j] << (8*j);
        beats.push_back(v);
    }
    size_t idx = 0;
    dut->m_axis_mac_tx_tready = 1;
    dut->m_axis_pcm_tready = 1;
    for (int c = 0; c < drain; c++) {
        if (idx < beats.size()) {
            dut->s_axis_mac_rx_tdata  = beats[idx];
            dut->s_axis_mac_rx_tkeep  = 0xFF;
            dut->s_axis_mac_rx_tvalid = 1;
            dut->s_axis_mac_rx_tlast  = (idx == beats.size()-1);
        } else {
            dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
        }
        lo();
        bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
        pcm_sample();
        hi();
        if (in_acc) idx++;
    }
    dut->s_axis_mac_rx_tvalid = 0;
}

// AAF PDU: sid = 8 wire bytes, chans = wire channels_per_frame
static const uint8_t* mkaaf(const uint8_t sid[8], uint8_t seq, uint8_t chans,
                            uint8_t pay0) {
    static uint8_t f[120];
    memset(f, 0, sizeof f);
    const uint8_t dmac[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x02};
    memcpy(f, dmac, 6);
    memcpy(f+6, sid, 6);                       // src MAC = sid MAC half
    f[12]=0x22; f[13]=0xF0;
    f[14]=0x02;                                // AAF
    f[15]=0x81;                                // sv, tv
    f[16]=seq;
    memcpy(f+18, sid, 8);
    f[26]=0x00; f[27]=0x00; f[28]=0x10; f[29]=0x00;  // avtp_ts = 0x1000 (not late/early)
    f[30]=0x02;                                // format INT32
    f[31]=(uint8_t)(0x05 << 4);                // nsr = 48 kHz
    f[32]=chans;
    f[33]=32;                                  // bit depth
    f[34]=0x00; f[35]=0x30;                    // data_len 48
    for (int i = 0; i < 48; i++) f[38+i] = (uint8_t)(pay0 + i);
    return f;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vmilan_datapath;

    printf("=== milan_datapath NxN integration (N_STREAMS=4, P12) ===\n");
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
    dut->s_axi_bready = dut->s_axi_rready = 0;
    dut->s_axis_tx_tvalid = 0; dut->s_axis_mac_rx_tvalid = 0;
    dut->m_axis_mac_tx_tready = 1; dut->m_axis_rx_tready = 1;
    dut->m_axis_ts_tready = 1; dut->m_axis_pcm_tready = 1;
    dut->i_mac_speed = 2; dut->i_link_up = 1; dut->i_full_duplex = 1;
    dut->i_mac_events = 0;
    for (int i = 0; i < 8; i++) step();
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    for (int i = 0; i < 8; i++) step();

    ck("ID == 'MILN'", axi_read(A_ID), 0x4D494C4E);
    ck("VERSION 0x000A (E1 bind-restore + E2 window)", axi_read(A_VERSION), 0x0001000A);

    // stream_id wire bytes {03:00:00:00:00:03, uid 0x0001} / {04:.., uid 2}
    const uint8_t sidB[8] = {0x03,0x00,0x00,0x00,0x00,0x03,0x00,0x01};
    const uint8_t sidC[8] = {0x04,0x00,0x00,0x00,0x00,0x04,0x00,0x02};
    const uint8_t sidX[8] = {0x05,0x00,0x00,0x00,0x00,0x05,0x00,0x09};
    // AAF format u64 for {AAF, 48k, INT32, depth 32, up to 2 ch}
    const uint32_t FMT_HI = 0x02050220, FMT_LO = 2u << 22;

    printf("-- provision listener 1 (route=DMA flag) + 2 (route=NULL) via 0x800 --\n");
    axi_write(A_STRM_SEL, 0x001);                    // dir=0 idx=1
    axi_write(A_SW_SID_LO, 0x00030001);              // sidB[63:0] LSW
    axi_write(A_SW_SID_HI, 0x03000000);
    axi_write(A_SW_FMT_LO, FMT_LO);
    axi_write(A_SW_FMT_HI, FMT_HI);
    axi_write(A_SW_CTRL, (RT_DMA << 1) | 1u);        // en, DMA flag only
    // CFG readback through the ENGINE-ARBITRATED LCTX port B (real RAM)
    ck("LCTX w4 CTRL readback (port B)",  axi_read(A_SW_CTRL), 0x3);
    ck("LCTX w2 FMT_LO readback (port B)", axi_read(A_SW_FMT_LO), FMT_LO);
    ck("LCTX w3 FMT_HI readback (port B)", axi_read(A_SW_FMT_HI), FMT_HI);

    axi_write(A_STRM_SEL, 0x002);                    // dir=0 idx=2
    axi_write(A_SW_SID_LO, 0x00040002);
    axi_write(A_SW_SID_HI, 0x04000000);
    axi_write(A_SW_FMT_LO, FMT_LO);
    axi_write(A_SW_FMT_HI, FMT_HI);
    axi_write(A_SW_CTRL, 0x1);                       // en, route=NULL
    ck("stream 2 CTRL readback (port B)", axi_read(A_SW_CTRL), 0x1);

    printf("-- idx-0 alias protection: route-only CTRL commit (2026-07-23) --\n");
    {
        // a CTRL commit at idx 0 with NO staged sid must not arm the
        // stream-table override: before the fix it wrote {sid=0, en=1},
        // hijacking the live ACMP alias AND matching sid-0 frames
        axi_write(A_STRM_SEL, 0x000);                // dir=0 idx=0
        axi_write(A_SW_CTRL, (RT_DMA << 1) | 1u);    // en + DMA, sid NOT staged
        size_t before = pcm_frames.size();
        const uint8_t sid0[8] = {0,0,0,0,0,0,0,0};
        inject(mkaaf(sid0, 5, 2, 0x10), 120);        // sid 0 must NOT match
        ck("route-only idx0 commit: sid-0 frame ignored",
           pcm_frames.size(), before);
    }

    printf("-- tagged AAF frames: 3x stream1, 2x stream2, 1x unknown --\n");
    inject(mkaaf(sidB, 10, 2, 0x30), 120);
    inject(mkaaf(sidB, 11, 2, 0x40), 120);
    inject(mkaaf(sidB, 12, 2, 0x50), 120);
    inject(mkaaf(sidC, 77, 2, 0x60), 120);
    inject(mkaaf(sidC, 78, 2, 0x70), 120);
    inject(mkaaf(sidX, 99, 2, 0x00), 120);           // no table entry: ignored

    ck("PCM ring frames = 3 (stream 1 only)", pcm_frames.size(), 3);
    bool user_ok = true, pay_ok = true;
    for (auto& fr : pcm_frames) {
        if (fr.user != 1) user_ok = false;
        if (fr.bytes.size() != 48) pay_ok = false;
    }
    if (!pcm_frames.empty() && pay_ok)
        for (int i = 0; i < 48; i++)
            if (pcm_frames[0].bytes[i] != (uint8_t)(0x30+i)) pay_ok = false;
    ck("ring tuser == 1 on every frame", user_ok, 1);
    ck("48-byte payload, frame 0 byte-exact", pay_ok, 1);

    printf("-- SNAP isolation: per-stream Table 7-157 blocks --\n");
    axi_write(A_STRM_SEL, 0x001);
    snap_and_wait();
    ck("s1 CNT9 FRAMES_RX = 3", axi_read(A_SW_CNT0 + 9*4), 3);
    ck("s1 CNT0 MEDIA_LOCKED = 1", axi_read(A_SW_CNT0 + 0*4), 1);
    ck("s1 CNT3 SEQ_NUM_MISMATCH = 0", axi_read(A_SW_CNT0 + 3*4), 0);
    ck("s1 CNT6 UNSUPPORTED_FORMAT = 0", axi_read(A_SW_CNT0 + 6*4), 0);
    ck("s1 PDUS = {drops 0, pdus 3}", axi_read(A_SW_PDUS), 3);
    uint32_t st1 = axi_read(A_SW_STATE);
    ck("s1 STATE media_locked", (st1 >> 10) & 1, 1);
    ck("s1 STATE wire_chans = 2", (st1 >> 11) & 0xFF, 2);

    axi_write(A_STRM_SEL, 0x002);
    snap_and_wait();
    ck("s2 CNT9 FRAMES_RX = 2", axi_read(A_SW_CNT0 + 9*4), 2);
    ck("s2 PDUS = 2 (NULL still counted)", axi_read(A_SW_PDUS), 2);
    axi_write(A_STRM_SEL, 0x003);
    snap_and_wait();
    ck("s3 (unprovisioned) CNT9 = 0", axi_read(A_SW_CNT0 + 9*4), 0);
    // stream-0 legacy flat FRAMES_RX untouched by streams 1/2 traffic;
    // 0x6C4 is the SHARED depacketizer's global {drops,pdus} (all streams:
    // 3 + 2 = 5) - per-stream pdus live in the window PDUS word
    ck("legacy 0x6BC (s0 FRAMES_RX) = 0", axi_read(A_AVTPRX_FRX), 0);
    ck("legacy 0x6C4 = shared-depkt total 5", axi_read(A_PCMRX_CNT), 5);

    printf("-- seq gap on stream 1 moves ONLY stream 1 --\n");
    // drain the 8-PDU settle window first (mismatches are suppressed while
    // settle > 0, the flat-monitor rule): 6 more in-order PDUs = 9 total
    for (uint8_t s = 13; s <= 18; s++) inject(mkaaf(sidB, s, 2, 0x30), 120);
    inject(mkaaf(sidB, 21, 2, 0x30), 120);           // expected 19: lost 2
    axi_write(A_STRM_SEL, 0x001);
    snap_and_wait();
    ck("s1 CNT9 FRAMES_RX = 10", axi_read(A_SW_CNT0 + 9*4), 10);
    ck("s1 CNT3 SEQ_NUM_MISMATCH = 1", axi_read(A_SW_CNT0 + 3*4), 1);
    ck("s1 CNT2 STREAM_INTERRUPTED = 1", axi_read(A_SW_CNT0 + 2*4), 1);
    axi_write(A_STRM_SEL, 0x002);
    snap_and_wait();
    ck("s2 CNT3 still 0", axi_read(A_SW_CNT0 + 3*4), 0);
    ck("s2 CNT9 still 2", axi_read(A_SW_CNT0 + 9*4), 2);

    printf("-- TCTX: talker CFG words through the live packetizer port --\n");
    axi_write(A_STRM_SEL, 0x101);                    // dir=1 idx=1
    axi_write(A_SW_DMAC_LO, 0xF000AB01);
    axi_write(A_SW_DMAC_HI, 0x000591E0);             // uid 5 in [31:16]
    axi_write(A_SW_CTRL, (2u << 5) | 1u);            // TCTX w0: vid=2, en
    ck("TCTX w0 CTRL readback (port B)", axi_read(A_SW_CTRL), (2u << 5) | 1u);
    ck("TCTX w1 DMAC_LO readback", axi_read(A_SW_DMAC_LO), 0xF000AB01);
    ck("TCTX w2 DMAC_HI readback", axi_read(A_SW_DMAC_HI), 0x000591E0);
    axi_write(A_STRM_SEL, 0x102);                    // untouched talker ctx
    ck("talker 2 CTRL reads 0", axi_read(A_SW_CTRL), 0);

    printf("-- route flags: RENDER|DMA / RENDER-only / NULL (stream 1) --\n");
    // so far every injected frame belonged to s1 (DMA-only) or s2 (NULL)
    // while s0 held the reset RENDER|DMA claim: the render tap must have
    // stayed silent (RENDER-lowest-wins picks s0, which got no frames)
    ck("render tap silent while s0 owns RENDER", render_beats, 0);
    // demote s0 (window idx 0 commit: en=0 evicts the table override,
    // route=NULL drops its RENDER claim) so s1 wins the render pick
    axi_write(A_STRM_SEL, 0x000);
    axi_write(A_SW_CTRL, (RT_NULL << 1) | 0u);
    // RENDER|DMA = capture-while-rendering: ring copy AND render tap.
    // A CTRL commit re-writes the stream-table entry from the STAGED sid
    // registers (the window ABI: SEL, stage SID, commit CTRL) - re-stage
    // sidB before every s1 CTRL rewrite.
    axi_write(A_STRM_SEL, 0x001);
    axi_write(A_SW_SID_LO, 0x00030001);
    axi_write(A_SW_SID_HI, 0x03000000);
    axi_write(A_SW_CTRL, (RT_RENDER_DMA << 1) | 1u);
    ck("s1 CTRL = RENDER|DMA readback", axi_read(A_SW_CTRL), 0x7);
    size_t rb0 = pcm_frames.size(); long xb0 = render_beats;
    inject(mkaaf(sidB, 22, 2, 0x30), 120);
    inject(mkaaf(sidB, 23, 2, 0x40), 120);
    ck("RENDER|DMA: +2 ring frames", pcm_frames.size() - rb0, 2);
    ck("RENDER|DMA: ring tuser == 1", pcm_frames.back().user, 1);
    ck("RENDER|DMA: 12 render beats (2 x 6)", render_beats - xb0, 12);
    // RENDER-only: renders, NO ring copy
    axi_write(A_SW_SID_LO, 0x00030001);
    axi_write(A_SW_SID_HI, 0x03000000);
    axi_write(A_SW_CTRL, (RT_RENDER << 1) | 1u);
    rb0 = pcm_frames.size(); xb0 = render_beats;
    inject(mkaaf(sidB, 24, 2, 0x50), 120);
    inject(mkaaf(sidB, 25, 2, 0x60), 120);
    ck("RENDER-only: no ring frames", pcm_frames.size() - rb0, 0);
    ck("RENDER-only: 12 render beats", render_beats - xb0, 12);
    // NULL: neither sink; the monitor/depkt still count ([M-5.3.8.10])
    axi_write(A_SW_SID_LO, 0x00030001);
    axi_write(A_SW_SID_HI, 0x03000000);
    axi_write(A_SW_CTRL, (RT_NULL << 1) | 1u);
    rb0 = pcm_frames.size(); xb0 = render_beats;
    inject(mkaaf(sidB, 26, 2, 0x70), 120);
    inject(mkaaf(sidB, 27, 2, 0x80), 120);
    ck("NULL: no ring frames", pcm_frames.size() - rb0, 0);
    ck("NULL: no render beats", render_beats - xb0, 0);
    axi_write(A_STRM_SEL, 0x001);
    snap_and_wait();
    ck("NULL still counted: s1 FRAMES_RX = 16", axi_read(A_SW_CNT0 + 9*4), 16);

    printf("-- talker t>0 arming: window CTRL + per-stream gate terms --\n");
    // the [TCTX] section already committed t1 CTRL en=1 through the window;
    // MAAP + lwSRP are still at their disabled defaults
    ck("t1 armed by the window CTRL commit", (tap_stream_en() >> 1) & 1, 1);
    ck("t0 still down (AAF_CTRL.en = 0)", tap_stream_en() & 1, 0);
    // t0 up via the legacy flat path (VID 2 + bypass + en - the VID-2 rule)
    axi_write(A_AAF_CTRL, 0x00020003);
    ck("t0 up via AAF_CTRL", tap_stream_en() & 1, 1);
    // t0 EMITS on the wire while t1 is armed (capture slot 0 pairs flow
    // continuously; t>0 has no sample source at datapath level - see the
    // header note, aaf nx [I2T] proves t>0 frame identity)
    uint32_t fr0 = axi_read(A_AAF_FRAMES);
    for (int g = 0; g < 200 && axi_read(A_AAF_FRAMES) == fr0; g++)
        for (int c = 0; c < 512; c++) step();
    ck("t0 emission alive while t1 armed", axi_read(A_AAF_FRAMES) > fr0, 1);
    // lwSRP on without a t1 reservation: ONLY t1 drops (t0 rides bypass)
    axi_write(A_LWSRP_CTRL, 0xD);
    for (int c = 0; c < 64; c++) step();
    ck("lwSRP on: t1 gate drops", (tap_stream_en() >> 1) & 1, 0);
    ck("lwSRP on: t0 unaffected (bypass)", tap_stream_en() & 1, 1);
    fr0 = axi_read(A_AAF_FRAMES);
    for (int g = 0; g < 200 && axi_read(A_AAF_FRAMES) == fr0; g++)
        for (int c = 0; c < 512; c++) step();
    ck("t0 emission alive after t1 drop", axi_read(A_AAF_FRAMES) > fr0, 1);
    axi_write(A_LWSRP_CTRL, 0xC);
    for (int c = 0; c < 64; c++) step();
    ck("lwSRP off: t1 re-arms", (tap_stream_en() >> 1) & 1, 1);
    // MAAP enabled + unclaimed holds t0 AND t1 alike (the engine-wide
    // term - ONE claim engine; mirrors t0's composition, see the RTL note)
    axi_write(A_MAAP_CTRL, 0x0801);
    for (int c = 0; c < 16; c++) step();
    ck("MAAP unclaimed: t1 held", (tap_stream_en() >> 1) & 1, 0);
    ck("MAAP unclaimed: t0 held too", tap_stream_en() & 1, 0);
    axi_write(A_MAAP_CTRL, 0x0800);
    for (int c = 0; c < 16; c++) step();
    ck("MAAP off: both restored", tap_stream_en() & 3, 3);
    // window CTRL[0] = 0 disarms ONLY t1
    axi_write(A_STRM_SEL, 0x101);
    axi_write(A_SW_CTRL, (2u << 5) | 0u);            // TCTX w0: vid=2, en=0
    for (int c = 0; c < 16; c++) step();
    ck("window CTRL[0]=0 disarms t1", (tap_stream_en() >> 1) & 1, 0);
    ck("t0 unaffected by the t1 disarm", tap_stream_en() & 1, 1);
    ck("t2/t3 never armed", (tap_stream_en() >> 2) & 3, 0);
    printf("-- N-sink ACMP: ctx2 window bind end-to-end (0x800 tbl master) --\n");
    // enable the ACMP listener (ADP enable gates it) with our entity id
    axi_write(A_ADP_EIDHI, 0x020000FF);
    axi_write(A_ADP_EIDLO, 0xFE000001);
    axi_write(A_ADP_CTRL, 0x00001F01);               // enable, valid_time 31
    {
        // CONNECT_RX (BIND_RX) for listener_unique_id 2: the record-only
        // explicit-sid window context (per-context policy, Lane-C/§3.1)
        uint8_t f[72]; memset(f, 0, sizeof f);
        const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
        memcpy(f, mc, 6);
        const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
        memcpy(f+6, csrc, 6);
        f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x06;   // CONNECT_RX_COMMAND
        f[16]=0x00; f[17]=44;                             // cdl
        // explicit fast-connect stream_id (nonzero -> adopted by policy)
        const uint8_t sid[8] = {0xAA,0xBB,0xCC,0xDD,0xEE,0xFF,0x00,0x07};
        memcpy(f+18, sid, 8);
        for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;  // controller
        const uint8_t tk[8] = {0x03,0x00,0x00,0x00,0x00,0x03,0x00,0x01};
        memcpy(f+34, tk, 8);                              // talker eid
        const uint8_t us[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
        memcpy(f+42, us, 8);                              // listener = us
        f[50]=0x00; f[51]=0x01;                           // talker_unique_id
        f[52]=0x00; f[53]=0x02;                           // listener_unique_id 2
        const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x99};
        memcpy(f+54, dm, 6);                              // stream_dest_mac
        f[62]=0x77; f[63]=0x21;                           // sequence_id
        inject(f, 70, 400);                               // (response drains to TX)
    }
    axi_write(A_STRM_SEL, 0x002);                    // dir=0 idx=2
    // the CSR polls the tbl port continuously; a couple of reads give the
    // grant time to land, then the snapshot is fresh
    (void)axi_read(A_SW_SID_LO);
    ck("ctx2 SID_LO = explicit bind sid", axi_read(A_SW_SID_LO), 0xEEFF0007);
    ck("ctx2 SID_HI", axi_read(A_SW_SID_HI), 0xAABBCCDD);
    ck("ctx2 DMAC_LO = bind cmd dest_mac", axi_read(A_SW_DMAC_LO), 0xF0002A99);
    ck("ctx2 DMAC_HI", axi_read(A_SW_DMAC_HI), 0x000091E0);
    snap_and_wait();
    uint32_t st2 = axi_read(A_SW_STATE);
    ck("ctx2 STATE lsm = SETTLED_NO_RSV (6)", st2 & 0x7, 6);
    ck("ctx2 STATE probing/status = 0 (record-only)", (st2 >> 3) & 0x7F, 0);
    axi_write(A_STRM_SEL, 0x003);                    // unbound window ctx
    (void)axi_read(A_SW_SID_LO);
    ck("ctx3 SID reads 0 (unbound)", axi_read(A_SW_SID_LO) |
                                     axi_read(A_SW_SID_HI), 0);
    axi_write(A_STRM_SEL, 0x000);                    // media ctx untouched
    (void)axi_read(A_SW_SID_LO);
    ck("ctx0 SID reads 0 (bind left ctx0 alone)", axi_read(A_SW_SID_LO) |
                                                  axi_read(A_SW_SID_HI), 0);

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
