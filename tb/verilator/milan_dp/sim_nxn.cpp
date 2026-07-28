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
 *   6. talker t>0 arming composition (aaf_stream_en_w, verilator-public;
 *      2026-07-26 mirrored contract): t1 arms via the window TCTX CTRL[0]
 *      commit; the composition mirrors t0 TERM BY TERM - per-stream ACMP
 *      talker_active (N-context responder), cfg_aaf_bypass as the escape
 *      hatch for EVERY stream, per-stream lwSRP gate with the engine-off
 *      escape, and the engine-wide MAAP term (one claim engine, block of
 *      N addresses, stream j = base+j); window CTRL[0]=0 disarms t1.
 *      t>0 wire emission needs a sample source for its slots: the chmap
 *      capture crossbar (0x900/CMAP) feeds any of the 32 pair slots; the
 *      PHYSICAL I2S front-end alone still emits slot 0 only - frame-level
 *      TCTX-identity emission + per-slot gate drop are proven in
 *      tb/verilator/aaf sim_main_nx [I2T]/[I2T4].
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
#include <cstdio>

// Stream count the C++ side walks. Paired with the RTL -GN_STREAMS by the
// Makefile: the default obj_nxn build is N=4; the obj_nxn8 build passes
// -GN_STREAMS=8 AND -DNSTREAMS_TB=8 so the sweep below walks idx 3..7 (the
// AX 8x8 target - the top half of the index space only exists at N=8).
#ifndef NSTREAMS_TB
#define NSTREAMS_TB 4
#endif

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
    A_ADP_TALK = 0x618, A_ADP_LIST = 0x61C,
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

    printf("=== milan_datapath NxN integration (N_STREAMS=%d, P12) ===\n",
           NSTREAMS_TB);
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
    ck("VERSION 0x0017 (the channel-map RAMs are readable; 0x910/0x914)",
       axi_read(A_VERSION), 0x00010018);

    // ---- THE ADVERTISED SHAPE AT N > 1 (2026-07-27) --------------------
    // The CRF Media Clock Output lives at talker_unique_id = N_STREAMS and
    // the CRF sink at listener_unique_id = N_STREAMS, so the entity has
    // N+1 sources and N+1 sinks. Nothing is written here: 0x618/0x61C are
    // read-only words hardwired from milan_datapath's ACMP_SRC_C /
    // ACMP_SINKS_C. On silicon these came from a boot script frozen at the
    // 1x1 shape, so the 8x8 board advertised 1 source / 2 sinks and the CRF
    // source was OUTSIDE the advertised range - the probe test further down
    // proves uid N answers SUCCESS, and this proves a controller is ever
    // told to ask.

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
        // ...and it is now BLOCKED, not merely mis-aimed. The pre-2026-07-26
        // guard was `(|{wing_sid_hi_r, wing_sid_lo_r})` over a staging pair
        // that is GLOBAL, not per index: it still held listener 2's sid from
        // three writes earlier, so this route-only commit wrote the stream
        // table and armed entry 0 with SOMEBODY ELSE'S stream_id (armed count
        // 3). win_commit_glue now qualifies the staging with the index it was
        // staged for (`wing_stg_hit_w`), so a commit at idx 0 with nothing
        // staged FOR IDX 0 leaves the ACMP alias alone: 2 armed, not 3.
        ck("route-only idx0 commit leaves entry 0 on the ACMP alias",
           (axi_read(0x8C4) >> 16) & 0xFF, 2);
    }

    printf("-- tagged AAF frames: 3x stream1, 2x stream2, 1x unknown --\n");
    inject(mkaaf(sidB, 10, 2, 0x30), 120);
    inject(mkaaf(sidB, 11, 2, 0x40), 120);
    inject(mkaaf(sidB, 12, 2, 0x50), 120);
    inject(mkaaf(sidC, 77, 2, 0x60), 120);
    inject(mkaaf(sidC, 78, 2, 0x70), 120);
    inject(mkaaf(sidX, 99, 2, 0x00), 120);           // no table entry: ignored

    ck("PCM ring frames = 3 (stream 1 only)", pcm_frames.size(), 3);

    // ---- RX parser probe at width N (APRB 0x8B4) ------------------------
    // The last frame injected above carries sidX, which no table entry
    // holds: the probe must report it as PARSED-but-not-MATCHED and hand
    // back the stream_id it read off the wire. That pairing is what makes
    // the group usable on a listener that accepts nothing.
    {
        enum { A_APRB_PARSED = 0x8B4, A_APRB_MATCHED = 0x8B8,
               A_APRB_SIDLO = 0x8BC, A_APRB_SIDHI = 0x8C0,
               A_APRB_INFO = 0x8C4 };
        long parsed = axi_read(A_APRB_PARSED);
        long matched = axi_read(A_APRB_MATCHED);
        long info = axi_read(A_APRB_INFO);
        ck("APRB parsed > matched (unknown sid seen)", parsed > matched ? 1 : 0, 1);
        ck("APRB last frame did NOT match", (info >> 8) & 1, 0);
        ck("APRB last subtype = AAF", info & 0xFF, 0x02);
        uint64_t wire = ((uint64_t)axi_read(A_APRB_SIDHI) << 32)
                        | (uint32_t)axi_read(A_APRB_SIDLO);
        uint64_t want = 0;
        for (int i = 0; i < 8; i++) want = (want << 8) | sidX[i];
        ck("APRB last SID == the unmatched wire sid", wire == want ? 1 : 0, 1);
        // 2 = streams 1 and 2 provisioned above. Entry 0 is NOT counted: the
        // route-only commit no longer arms it, so it stays the ACMP alias.
        // The probe counts what is ARMED, which is exactly the distinction
        // that makes "armed but matching nothing" visible on silicon.
        ck("APRB armed entries = 2 (idx0 still the ACMP alias)",
           (info >> 16) & 0xFF, 2);
    }
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
    // MAAP + lwSRP are still at their disabled defaults.
    //
    // ASK FOR THE BYPASS EXPLICITLY. This case tests the TCTX ARMING PATH -
    // that a window CTRL commit reaches the per-stream enable - not the
    // admission POLICY. Until VERSION 0x0018 it passed without asking,
    // because AAF_CTRL reset to 0x0002_0002 and bit 1 (cfg_aaf_bypass) ORs
    // past both qualifying terms, so every talker streamed from power-on
    // whether or not a Listener Ready was ever registered. That reset value
    // was the defect (Milan v1.2 5.3.7.3 makes the licence to stream
    // conditional on RECEIVING a Listener Ready/Ready Failed), so the reset
    // is now 0x0002_0000 and this check was passing BECAUSE of it.
    axi_write(A_AAF_CTRL, 0x00020002);   // bypass on, talker enable still 0
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
    // lwSRP on without reservations (2026-07-26 mirrored contract): the
    // composition is term-by-term IDENTICAL for every stream now, so
    // cfg_aaf_bypass is the escape hatch for t>0 exactly as for t0 - the
    // old "only t1 drops" asymmetry WAS the honest gap this closes.
    axi_write(A_LWSRP_CTRL, 0x15);          // enable, class-A queue 5
    for (int c = 0; c < 64; c++) step();
    ck("lwSRP on + bypass: t1 rides bypass like t0", (tap_stream_en() >> 1) & 1, 1);
    ck("lwSRP on + bypass: t0 unaffected", tap_stream_en() & 1, 1);
    // bypass CLEAR: no reservation -> EVERY stream gates (FR-SRP-03 for all)
    axi_write(A_AAF_CTRL, 0x00020001);
    for (int c = 0; c < 64; c++) step();
    ck("bypass clear: t1 gates (no reservation)", (tap_stream_en() >> 1) & 1, 0);
    ck("bypass clear: t0 gates too (mirrored)", tap_stream_en() & 1, 0);
    axi_write(A_AAF_CTRL, 0x00020003);       // the VID-2 rule value restored
    for (int c = 0; c < 64; c++) step();
    fr0 = axi_read(A_AAF_FRAMES);
    for (int g = 0; g < 200 && axi_read(A_AAF_FRAMES) == fr0; g++)
        for (int c = 0; c < 512; c++) step();
    ck("t0 emission alive on bypass restore", axi_read(A_AAF_FRAMES) > fr0, 1);

    printf("-- 5.3.7.3 silence fill: an ARMED talker with no source FRAMES --\n");
    // Until 2026-07-28 t1 was armed exactly here and emitted NOTHING: no
    // pair slot had a source behind it (the W3 finding), so a listener that
    // bound it got ACMP SUCCESS and then no packets - the state Milan v1.2
    // 5.3.7.3's first sentence forbids ("...it shall be streaming AVTP
    // packets"). KL_pair_zero_fill now strobes every consumed pair slot at
    // clk_audio/512, silence where nothing feeds it, so an armed talker
    // frames at the media rate. Talkers are told apart by the sid uid16
    // (bytes 24-25): t0 = 0, t1 = 5 (staged into A_SW_DMAC_HI[31:16] in the
    // TCTX section above); anything else armed here would be a defect.
    {
        std::vector<uint8_t> cur;
        int t1f = 0, t1sil = 0, t1chans = -1, t1dlen = -1, foreign = 0;
        dut->m_axis_mac_tx_tready = 1;
        for (int c = 0; c < 60000 && t1f < 3; c++) {
            lo();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                for (int l = 0; l < 8; l++)
                    if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                        cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                if (dut->m_axis_mac_tx_tlast) {
                    // TX AAF rides the VID-2 C-TAG (the AAF_CTRL[27:16]
                    // rule), so allow for the 4-byte 802.1Q shim
                    size_t off = (cur.size() > 17 && cur[12] == 0x81
                                  && cur[13] == 0x00) ? 4 : 0;
                    if (cur.size() >= 86 + off && cur[12+off] == 0x22
                        && cur[13+off] == 0xF0 && cur[14+off] == 0x02) {
                        int uid = (cur[24+off] << 8) | cur[25+off];
                        if (uid == 5) {
                            t1f++;
                            t1chans = cur[32+off];
                            t1dlen  = (cur[34+off] << 8) | cur[35+off];
                            bool z = true;
                            for (size_t i = 38+off;
                                 i < 38 + off + 48 && i < cur.size(); i++)
                                if (cur[i]) z = false;
                            if (z) t1sil++;
                        } else if (uid != 0) {
                            foreign++;                 // t2/t3 must NOT stream
                        }
                    }
                    cur.clear();
                }
            }
            hi();
        }
        ck("silence fill: armed t1 EMITS AAF PDUs", t1f >= 3, 1);
        ck("silence fill: t1 channels_per_frame = wire width", t1chans, 2);
        ck("silence fill: t1 stream_data_length = 48", t1dlen, 48);
        ck("silence fill: t1 payload is DIGITAL SILENCE, every PDU",
           t1sil, t1f);
        ck("silence fill: unarmed talkers stayed silent", foreign, 0);
    }

    printf("-- 5.5.2.7 SRP-ONLY licence: a Listener Ready opens the gate "
           "with ZERO ACMP --\n");
    // Milan v1.2 5.5.2.7: "Talkers rely only on SRP (not ACMP) to determine
    // whether any Listeners are interested ... Talkers do not maintain any
    // internal state related to bound/settled Listeners." So the licence
    // must open on a REGISTERED LISTENER READY alone - no controller, no
    // BIND, no PROBE_TX ever sent toward t0 in this whole sim. The
    // composed gate already reads that way (KL_acmp_tlkr_ctx
    // talker_active = probe_armed | listener_observed, and
    // listener_observed IS the lwSRP registration hook - the ACMP-looking
    // term can never block an SRP-only listener); this case is the L2
    // proof through the real RX path. And 5.3.7.3's continuity: once open,
    // the gate must STAY open while the registration stands
    // (STREAMING_WAIT is excluded). The module-level term-by-term licence
    // (Ready opens, ReadyFailed opens, AskingFailed shuts) lives in
    // tb/verilator/lwsrp.
    {
        axi_write(A_AAF_CTRL, 0x00020001);   // en + VID 2, bypass CLEAR
        for (int c = 0; c < 64; c++) step();
        ck("SRP-only: gate CLOSED without a listener (no bypass)",
           tap_stream_en() & 1, 0);
        // Declare (LWSRP_CTRL 0x17 = enable + TALKER-DECLARE + queue 5; the
        // flow above ran 0x15, no talker bit - everything before this rode
        // the bypass). Row 0's matching StreamID is DERIVED by the walker:
        // {station_mac, unique_id} (KL_lwsrp_walker our_sid_w) - the
        // harness MAC is 0, so the Listener Ready must carry the all-zero
        // sid. No window op touches the row: the whole case is pure SRP.
        axi_write(A_LWSRP_CTRL, 0x17);
        for (int c = 0; c < 512; c++) step();
        uint8_t sid[8] = {0,0,0,0,0,0,0,0};
        ck("SRP-only: still CLOSED after declaring (no listener yet)",
           tap_stream_en() & 1, 0);
        // Listener Ready MRPDU for that StreamID: type 4, attrlen 8,
        // listlen 14 (VectorHeader 2 + StreamID 8 + 3-packed 1 + 4-packed 1
        // + EndMark 2), JoinIn(1)*36, FourPacked Ready(2)*64
        uint8_t lr[60]; memset(lr, 0, sizeof lr);
        const uint8_t msrp_da[6] = {0x01,0x80,0xC2,0x00,0x00,0x0E};
        memcpy(lr, msrp_da, 6);
        lr[6]=0x02; lr[7]=0xAA; lr[8]=0xBB; lr[9]=0xCC; lr[10]=0xDD; lr[11]=0x01;
        lr[12]=0x22; lr[13]=0xEA;
        lr[14]=0;                      // ProtocolVersion
        lr[15]=3; lr[16]=8;            // Listener (type 3), AttributeLength 8
        lr[17]=0; lr[18]=14;           // AttributeListLength
        lr[19]=0; lr[20]=1;            // VectorHeader: LeaveAll 0, NOV 1
        memcpy(lr+21, sid, 8);         // FirstValue = the captured StreamID
        lr[29]=36;                     // ThreePacked JoinIn
        lr[30]=128;                    // FourPacked Ready
        // the lwSRP tap rides rx_axis_to_dma, and earlier flow steps leave
        // frames PARKED against m_axis_rx_tready=0 - drain the lane so the
        // tap sees accepted beats
        dut->m_axis_rx_tready = 1;
        for (int c = 0; c < 4000; c++) step();
        // FEED, twice - a real bridge re-declares every JoinTime, so the
        // repeat is protocol-shaped. Both copies matter here empirically:
        // the first (true final keep 0x0F) resyncs the tap when the drain
        // left it mid-frame on a torn parked frame, and the REGISTERING
        // copy is inject()'s full-keep one (tkeep 0xFF = a 64 B min-size
        // frame). A keep-0x0F copy alone does not register - the rx
        // path's min-size/keep handling deserves a look in the lwsrp_rx
        // suite some round.
        {
            size_t idx = 0;
            std::vector<uint64_t> beats;
            for (size_t off = 0; off < 60; off += 8) {
                uint64_t d = 0;
                for (int j = 0; j < 8 && off + j < 60; j++)
                    d |= (uint64_t)lr[off + j] << (8*j);
                beats.push_back(d);
            }
            for (int c = 0; c < 3000; c++) {
                if (idx < beats.size()) {
                    dut->s_axis_mac_rx_tdata  = beats[idx];
                    dut->s_axis_mac_rx_tkeep  = (idx == beats.size()-1) ? 0x0F
                                                                        : 0xFF;
                    dut->s_axis_mac_rx_tvalid = 1;
                    dut->s_axis_mac_rx_tlast  = (idx == beats.size()-1);
                } else {
                    dut->s_axis_mac_rx_tvalid = 0;
                    dut->s_axis_mac_rx_tlast  = 0;
                }
                lo();
                bool acc = dut->s_axis_mac_rx_tvalid &&
                           dut->s_axis_mac_rx_tready;
                hi();
                if (acc) idx++;
            }
            dut->s_axis_mac_rx_tvalid = 0;
        }
        inject(lr, 60, 2000);
        // the bench-predicted bound status (8.3.6): 0x37E once the
        // registration lands, vs 0x30 declaring-unbound
        ck("SRP-only: LWSRP_STATUS reads the BOUND value 0x37E",
           axi_read(0x694), 0x37E);
        int opened = 0;
        for (int g = 0; g < 400 && !opened; g++) {
            for (int c = 0; c < 64; c++) step();
            opened = tap_stream_en() & 1;
        }
        ck("SRP-only: Listener Ready ALONE opens the licence (no ACMP ever "
           "sent for t0)", opened, 1);
        // continuity: the gate holds while the registration stands
        uint32_t f0 = axi_read(A_AAF_FRAMES);
        bool held = true;
        for (int g = 0; g < 40; g++) {
            for (int c = 0; c < 128; c++) step();
            if (!(tap_stream_en() & 1)) held = false;
        }
        ck("SRP-only: licence HELD (no STREAMING_WAIT, 5.3.7.3)",
           held ? 1 : 0, 1);
        ck("SRP-only: frames flowed under it", axi_read(A_AAF_FRAMES) > f0, 1);
        // restore the flow's posture: engine back to the no-talker 0x15,
        // bypass back on (no row was ever touched - pure SRP case)
        axi_write(A_LWSRP_CTRL, 0x15);
        axi_write(A_AAF_CTRL, 0x00020003);
        for (int c = 0; c < 64; c++) step();
    }

    axi_write(A_LWSRP_CTRL, 0x14);          // disable, class-A queue 5 kept
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

    // ======================================================================
    // item-5 (N x N, the AX 8x8 target): full-index routing sweep. The checks
    // above prove idx 1/2/3 at N=4; this proves EVERY fresh index 3..N-1 is
    // provisioned, live, and routed independently AT THE SAME TIME. Default
    // build (N=4) walks idx 3; the obj_nxn8 build (-GN_STREAMS=8) walks idx
    // 3..7 - the top half of the stream-index space that exists only at N=8,
    // so a PASS here IS the 8-stream routing proof the AX shape needs.
    printf("-- N-wide routing: fresh streams 3..%d live at once, by index --\n",
           NSTREAMS_TB - 1);
    // provision every fresh stream simultaneously, DMA route so each lands on
    // the PCM ring tagged with its own tuser. sid(s) = {0x30+s,0,0,0,0,
    // 0x30+s,0,s}: distinct from sidB/C/X and from each other.
    for (int s = 3; s < NSTREAMS_TB; s++) {
        uint32_t sid_hi = ((uint32_t)(0x30 + s) << 24);
        uint32_t sid_lo = ((uint32_t)(0x30 + s) << 16) | (uint32_t)s;
        axi_write(A_STRM_SEL, s & 0xF);                  // dir=0 idx=s
        axi_write(A_SW_SID_LO, sid_lo);
        axi_write(A_SW_SID_HI, sid_hi);
        axi_write(A_SW_FMT_LO, FMT_LO);
        axi_write(A_SW_FMT_HI, FMT_HI);
        axi_write(A_SW_CTRL, (RT_DMA << 1) | 1u);        // en, DMA flag
    }
    // CFG readback per stream through the ENGINE-ARBITRATED LCTX port B
    for (int s = 3; s < NSTREAMS_TB; s++) {
        axi_write(A_STRM_SEL, s & 0xF);
        char nm[56]; snprintf(nm, sizeof nm, "ctx%d CTRL readback (port B)", s);
        ck(nm, axi_read(A_SW_CTRL), 0x3);
    }
    // inject one uniquely-payloaded frame per stream, interleaved, ALL table
    // entries live: the classifier must tag each frame with the right index.
    size_t ring0 = pcm_frames.size();
    for (int s = 3; s < NSTREAMS_TB; s++) {
        uint8_t sid[8] = {(uint8_t)(0x30 + s), 0, 0, 0, 0,
                          (uint8_t)(0x30 + s), 0, (uint8_t)s};
        inject(mkaaf(sid, (uint8_t)(0x40 + s), 2, (uint8_t)(0xA0 + s)), 120);
    }
    ck("sweep: one ring frame per fresh stream",
       (unsigned)(pcm_frames.size() - ring0), (unsigned)(NSTREAMS_TB - 3));
    // each ring frame carries its own stream's tuser + byte-exact payload
    bool sweep_user_ok = true, sweep_pay_ok = true;
    for (int s = 3; s < NSTREAMS_TB; s++) {
        size_t k = ring0 + (size_t)(s - 3);
        if (k >= pcm_frames.size()) { sweep_user_ok = false; break; }
        if (pcm_frames[k].user != s) sweep_user_ok = false;
        if (pcm_frames[k].bytes.size() != 48) sweep_pay_ok = false;
        else for (int i = 0; i < 48; i++)
            if (pcm_frames[k].bytes[i] != (uint8_t)(0xA0 + s + i)) sweep_pay_ok = false;
    }
    ck("sweep: ring tuser == stream index for all", sweep_user_ok, 1);
    ck("sweep: 48-byte payload byte-exact for all", sweep_pay_ok, 1);
    // isolation: each fresh stream counted EXACTLY its own single frame (no
    // cross-count across the N simultaneously-live contexts) - Table 7-157.
    for (int s = 3; s < NSTREAMS_TB; s++) {
        axi_write(A_STRM_SEL, s & 0xF);
        snap_and_wait();
        char nm[64];
        snprintf(nm, sizeof nm, "ctx%d FRAMES_RX == 1 (isolated)", s);
        ck(nm, axi_read(A_SW_CNT0 + 9*4), 1);
        snprintf(nm, sizeof nm, "ctx%d PDUS == 1", s);
        ck(nm, axi_read(A_SW_PDUS), 1);
    }
    // an unknown sid (no table entry at any index) is still ignored at width N
    {
        const uint8_t sidU[8] = {0x5A, 0, 0, 0, 0, 0x5A, 0, 0x0F};
        size_t before = pcm_frames.size();
        inject(mkaaf(sidU, 50, 2, 0x11), 120);
        ck("sweep: unknown sid ignored (no ring frame)",
           (unsigned)pcm_frames.size(), (unsigned)before);
    }

    // ======================================================================
    // HOST-PLANE drill (silicon 0x1000B regression, 2026-07-25): the fabric
    // above is fully provisioned and N streams are live - exactly the state
    // the flashed ax8x8 build was in when host RX read dead. In THIS shape
    // (N=NSTREAMS_TB, single host RX lane) the host-facing lanes must work:
    //   [H1] a non-AVTP broadcast frame on the MAC RX AXIS emerges byte-exact
    //        on the host DMA RX port (MAC -> PTP-RX -> dest-MAC filter ->
    //        m_axis_rx = the RingDMAWriter's input);
    //   [H2] a gPTP pdelay_req (event) frame yields one 2-beat metadata
    //        record on m_axis_ts (= the dma-ts writer's input), with the
    //        host RX copy of the same frame still delivered.
    // sim_main proves both at N=1 only; this is the N>1 silicon-shape gate.
    // ======================================================================
    printf("-- host plane: MAC->host-RX + PTP ts record at N=%d --\n",
           NSTREAMS_TB);
    {
        // drain the host RX lane first: every earlier inject() left frames
        // parked against m_axis_rx_tready=0 (the fabric tests never drain it)
        dut->m_axis_rx_tready = 1;
        for (int c = 0; c < 4000; c++) step();

        // [H1] 64-byte broadcast ARP-ish frame, LE lanes like the real ingress
        uint8_t hf[64]; memset(hf, 0, sizeof hf);
        const uint8_t hh[14] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                0x02,0x11,0x22,0x33,0x44,0x55, 0x08,0x06};
        memcpy(hf, hh, 14);
        for (int i = 14; i < 64; i++) hf[i] = (uint8_t)(0xC0 + i);
        std::vector<uint64_t> hb, hout;
        for (int bt = 0; bt < 8; bt++) {
            uint64_t v = 0;
            for (int j = 0; j < 8; j++) v |= (uint64_t)hf[bt*8+j] << (8*j);
            hb.push_back(v);
        }
        size_t idx = 0;
        for (int c = 0; c < 800; c++) {
            if (idx < hb.size()) {
                dut->s_axis_mac_rx_tdata  = hb[idx];
                dut->s_axis_mac_rx_tkeep  = 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast  = (idx == hb.size()-1);
            } else {
                dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
            }
            lo();
            bool in_acc  = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
            bool out_acc = dut->m_axis_rx_tvalid && dut->m_axis_rx_tready;
            uint64_t od  = dut->m_axis_rx_tdata;
            hi();
            if (in_acc) idx++;
            if (out_acc) hout.push_back(od);
        }
        dut->s_axis_mac_rx_tvalid = 0;
        ck("host RX: broadcast frame beats delivered", hout.size(), hb.size());
        bool hexact = hout.size() == hb.size();
        if (hexact)
            for (size_t i = 0; i < hb.size(); i++)
                if (hout[i] != hb[i]) hexact = false;
        ck("host RX: broadcast frame byte-exact", hexact ? 1 : 0, 1);

        // [H2] PTP event frame -> exactly one 2-beat ts record + host RX copy
        enum { A_PTP_CTRL = 0x500, A_PTP_INCR = 0x504 };
        axi_write(A_PTP_INCR, 20u << 24);          // 20 ns/tick Q8.24
        axi_write(A_PTP_CTRL, 1);
        uint8_t g[68]; memset(g, 0, sizeof g);
        const uint8_t gh[14] = {0x01,0x80,0xC2,0,0,0x0E, 2,0,0,0,0,2, 0x88,0xF7};
        memcpy(g, gh, 14);
        g[14] = 0x12; g[15] = 0x02; g[17] = 54;    // pdelay_req, v2, len 54
        g[44] = 0xBE; g[45] = 0xEF;                // sequenceId
        std::vector<uint64_t> gb, ts;
        size_t hrx_beats = 0;
        for (int bt = 0; bt < 9; bt++) {
            uint64_t v = 0;
            for (int j = 0; j < 8 && bt*8+j < 68; j++)
                v |= (uint64_t)g[bt*8+j] << (8*j);
            gb.push_back(v);
        }
        idx = 0;
        dut->m_axis_ts_tready = 1;
        for (int c = 0; c < 800; c++) {
            if (idx < gb.size()) {
                dut->s_axis_mac_rx_tdata  = gb[idx];
                dut->s_axis_mac_rx_tkeep  = (idx == gb.size()-1) ? 0x0F : 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast  = (idx == gb.size()-1);
            } else {
                dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
            }
            lo();
            bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
            bool tsx    = dut->m_axis_ts_tvalid && dut->m_axis_ts_tready;
            uint64_t td = dut->m_axis_ts_tdata;
            bool hrx    = dut->m_axis_rx_tvalid && dut->m_axis_rx_tready;
            hi();
            if (in_acc) idx++;
            if (tsx) ts.push_back(td);
            if (hrx) hrx_beats++;
        }
        dut->s_axis_mac_rx_tvalid = 0;
        ck("ts record emitted (2 beats)", ts.size(), 2);
        if (ts.size() == 2) {
            ck("ts word1 dir=RX", (unsigned long)(ts[1] & 1), 0);
            ck("ts word1 mtype=2 (pdelay_req)",
               (unsigned long)((ts[1] >> 4) & 0xF), 2);
            ck("ts word1 seq=0xBEEF",
               (unsigned long)((ts[1] >> 8) & 0xFFFF), 0xBEEFUL);
        }
        ck("host RX: gPTP frame copy delivered (9 beats)", hrx_beats, 9);

        // [H3] silicon boot ordering: the dma-ts writer is NOT armed at boot
        // (m_axis_ts_tready = 0) while the LAN already carries gPTP event
        // frames (the switch runs 802.1AS). The ts record lane fills - and
        // MUST NOT wedge the shared RX pipeline: after a burst of un-drained
        // event frames, a host-destined frame still has to emerge on
        // m_axis_rx. This is the exact state the flashed ax8x8 build boots
        // into (rx_packets = 0 forever, fabric TX still perfect).
        dut->m_axis_ts_tready = 0;
        for (int burst = 0; burst < 40; burst++) {
            g[44] = (uint8_t)(burst >> 8); g[45] = (uint8_t)burst;
            idx = 0;
            for (int c = 0; c < 60; c++) {
                if (idx < gb.size()) {
                    dut->s_axis_mac_rx_tdata  = gb[idx];
                    dut->s_axis_mac_rx_tkeep  = (idx == gb.size()-1) ? 0x0F : 0xFF;
                    dut->s_axis_mac_rx_tvalid = 1;
                    dut->s_axis_mac_rx_tlast  = (idx == gb.size()-1);
                } else {
                    dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
                }
                lo();
                bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
                hi();
                if (in_acc) idx++;
            }
            dut->s_axis_mac_rx_tvalid = 0;
        }
        // now the host frame again, RX ring armed (tready=1), ts still unarmed
        std::vector<uint64_t> hout2;
        idx = 0;
        for (int c = 0; c < 800; c++) {
            if (idx < hb.size()) {
                dut->s_axis_mac_rx_tdata  = hb[idx];
                dut->s_axis_mac_rx_tkeep  = 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast  = (idx == hb.size()-1);
            } else {
                dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
            }
            lo();
            bool in_acc  = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
            bool out_acc = dut->m_axis_rx_tvalid && dut->m_axis_rx_tready;
            uint64_t od  = dut->m_axis_rx_tdata;
            hi();
            if (in_acc) idx++;
            if (out_acc) hout2.push_back(od);
        }
        dut->s_axis_mac_rx_tvalid = 0;
        ck("host RX alive under un-drained ts lane (8 beats)",
           hout2.size(), hb.size());
        bool h2exact = hout2.size() == hb.size();
        if (h2exact)
            for (size_t i = 0; i < hb.size(); i++)
                if (hout2[i] != hb[i]) h2exact = false;
        ck("host RX under ts backpressure byte-exact", h2exact ? 1 : 0, 1);
        dut->m_axis_ts_tready = 1;
        dut->m_axis_rx_tready = 0;
    }

    // ======================================================================
    // TRAP-1 END-TO-END — REGRESSION GUARD for the fabric-listener blocker
    // (found 2026-07-26, fixed the same day; this section asserts the FIX).
    //
    // The defect: any window CTRL write at index 0 detached the entry-0 ACMP
    // alias FOR GOOD, so a later ACMP bind of listener 0 was cosmetic - the
    // listener SM reported bound, the stream table never saw that stream_id,
    // the parser never matched. PARSED climbed, MATCHED did not: the 8x8
    // blocker's exact symptom, reached from a CSR write sequence a
    // provisioning daemon would make. Two RTL terms combined to allow it:
    //   * `(|{wing_sid_hi_r, wing_sid_lo_r})` was meant to mean "a sid was
    //     staged for this commit", but the staging pair is GLOBAL, not per
    //     index - any earlier stage for any OTHER listener satisfied it, so a
    //     route-flags-only CTRL write at idx 0 armed entry 0 with that other
    //     listener's stream_id;
    //   * `| ~csr_lctx_wr_data_w[0]` let an en=0 CTRL write through
    //     unconditionally, so even "clear this sink" reached the table -
    //     and KL_stream_table's ovr_armed_r[0] was set by ANY write and
    //     cleared only by RESET, so there was no way back to alias mode.
    //
    // The fix, asserted below:
    //   * win_commit_glue tags the staging set with the index it was staged
    //     for (`wing_stg_hit_w`), so a commit only overrides the table when a
    //     sid was staged FOR THAT INDEX, and an eviction with nothing staged
    //     commits the ZERO sid;
    //   * KL_stream_table treats {valid=0, sid=0} as RELEASE-TO-ALIAS and
    //     disarms ovr_armed_r[idx], so entry 0 returns to the ACMP alias at
    //     runtime.
    //
    // tb/verilator/avtp_parser/sim_tbl.cpp T6 covers the table-level
    // mechanism from a clean reset; this section proves the behaviour through
    // the real CSR window in the real datapath. Asserted through the 0x8B4
    // APRB probe group only - upstream of format, route and depacketizer
    // policy - so the verdict under test is the stream-table match itself and
    // nothing else. Runs last: it leaves listener 0 provisioned.
    printf("-- TRAP-1: entry-0 ACMP alias survives window writes (regression) --\n");
    {
        enum { A_APRB_PARSED = 0x8B4, A_APRB_MATCHED = 0x8B8,
               A_APRB_INFO = 0x8C4 };
        auto armed   = [&]{ return (axi_read(A_APRB_INFO) >> 16) & 0xFF; };
        auto matched = [&]{ return axi_read(A_APRB_MATCHED); };
        auto parsed  = [&]{ return axi_read(A_APRB_PARSED); };

        // the host-plane drill above deliberately left the DMA RX port
        // un-drained; the shared inject() never drives it, so frame tails
        // stall at the filter boundary and back-pressure the whole RX
        // pipeline - including the PRE-filter parser tap. Arm the port and
        // let the stalled tails flush before measuring anything.
        dut->m_axis_rx_tready = 1;
        for (int c = 0; c < 400; c++) step();

        // bind listener_unique_id 0 over ACMP with an explicit stream_id -
        // the entry-0 alias, exactly how the bench listener comes up
        const uint8_t sid0[8] = {0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x00};
        const unsigned long armed_pre = armed();
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x06;   // CONNECT_RX_COMMAND
            f[16]=0x00; f[17]=44;
            memcpy(f+18, sid0, 8);                            // explicit sid
            for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;
            const uint8_t tk[8] = {0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x00};
            memcpy(f+34, tk, 8);
            const uint8_t us[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, us, 8);
            f[50]=0x00; f[51]=0x00;                           // talker_unique_id
            f[52]=0x00; f[53]=0x00;                           // listener_unique_id 0
            const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x02};
            memcpy(f+54, dm, 6);
            f[62]=0x77; f[63]=0x22;
            inject(f, 70, 400);
        }
        unsigned long m0 = matched(), p0 = parsed();
        inject(mkaaf(sid0, 0x11, 2, 0xC0), 120);
        // THE REGRESSION GUARD: the listener is bound, both ends agree on the
        // sid, the frame reaches the parser - and the verdict is now OURS.
        // Before the fix this read MATCHED-static because entry 0 had stopped
        // being the ACMP alias hundreds of cycles earlier, when a route-flags
        // CTRL write landed on it.
        ck("TRAP-1 bound: PARSED climbs",  parsed()  - p0, 1);
        ck("TRAP-1 bound: MATCHED climbs (alias intact)", matched() - m0, 1);
        ck("TRAP-1 bound: INFO match flag set",
           (axi_read(A_APRB_INFO) >> 8) & 1, 1);
        ck("TRAP-1 bound: INFO index 0",
           (axi_read(A_APRB_INFO) >> 12) & 0xF, 0);
        // binding listener 0 ENABLES the alias entry, so the armed count rises
        // by exactly one - the alias is a live table entry again, not a ghost
        ck("TRAP-1 bound: the ACMP alias counts as one armed entry",
           armed() - armed_pre, 1);
        const unsigned long armed_bound = armed();

        // a route-flags-only CTRL write at idx 0 - the exact write that used
        // to detach the alias - must now leave it completely alone
        axi_write(A_STRM_SEL, 0x000);                 // dir=0 idx=0
        axi_write(A_SW_CTRL, (RT_DMA << 1) | 1u);     // en + DMA, sid NOT staged
        ck("TRAP-1 route-only CTRL at idx0 does not arm an override",
           armed(), armed_bound);
        m0 = matched(); p0 = parsed();
        inject(mkaaf(sid0, 0x12, 2, 0xC0), 120);
        ck("TRAP-1 route-only CTRL at idx0: STILL MATCHES", matched() - m0, 1);

        // the explicit-override path still works: stage the sid FOR idx 0,
        // then commit. This is the deliberate bench/daemon override.
        axi_write(A_STRM_SEL, 0x000);
        axi_write(A_SW_SID_LO, 0x00020000);
        axi_write(A_SW_SID_HI, 0x02000000);
        axi_write(A_SW_CTRL, (RT_DMA << 1) | 1u);
        m0 = matched(); p0 = parsed();
        inject(mkaaf(sid0, 0x13, 2, 0xC0), 120);
        ck("TRAP-1 explicit override at idx0: MATCH", matched() - m0, 1);
        ck("TRAP-1 explicit override: INFO index 0",
           (axi_read(A_APRB_INFO) >> 12) & 0xF, 0);

        // RELEASE-TO-ALIAS: "clear this sink" - en=0 with nothing staged for
        // idx 0 - commits the zero sid, which disarms the override and hands
        // entry 0 back to the ACMP alias. Before the fix this latched
        // ovr_armed_r[0] and the alias was gone until reset.
        axi_write(A_STRM_SEL, 0x000);                 // dir=0 idx=0
        axi_write(A_SW_CTRL, 0x0);                    // en=0, route=NULL
        m0 = matched(); p0 = parsed();
        inject(mkaaf(sid0, 0x14, 2, 0xC0), 120);
        ck("TRAP-1 release-to-alias: PARSED climbs", parsed() - p0, 1);
        ck("TRAP-1 release-to-alias: alias is back, MATCHED climbs",
           matched() - m0, 1);
        ck("TRAP-1 release-to-alias: INFO match flag set",
           (axi_read(A_APRB_INFO) >> 8) & 1, 1);

        // and an ACMP re-bind now lands on a live alias rather than a ghost
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x06;
            f[16]=0x00; f[17]=44;
            memcpy(f+18, sid0, 8);
            for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;
            const uint8_t tk[8] = {0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x00};
            memcpy(f+34, tk, 8);
            const uint8_t us[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, us, 8);
            f[52]=0x00; f[53]=0x00;
            const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x02};
            memcpy(f+54, dm, 6);
            f[62]=0x77; f[63]=0x23;
            inject(f, 70, 400);
        }
        m0 = matched(); p0 = parsed();
        inject(mkaaf(sid0, 0x15, 2, 0xC0), 120);
        ck("TRAP-1 ACMP re-bind still matches: PARSED climbs", parsed() - p0, 1);
        ck("TRAP-1 ACMP re-bind still matches: MATCHED climbs",
           matched() - m0, 1);

        // a NEGATIVE leg, so this is not a "matches everything" tautology: an
        // unrelated stream_id must still be parsed-but-not-matched with the
        // alias live
        {
            const uint8_t sidZ[8] = {0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,0x11,0x22};
            m0 = matched(); p0 = parsed();
            inject(mkaaf(sidZ, 0x16, 2, 0xC0), 120);
            ck("TRAP-1 negative: foreign sid PARSED", parsed() - p0, 1);
            ck("TRAP-1 negative: foreign sid NOT matched", matched() - m0, 0);
            ck("TRAP-1 negative: INFO match flag clear",
               (axi_read(A_APRB_INFO) >> 8) & 1, 0);
        }
    }

    // ==================================================================
    //  lwSRP attribute rows through the 0x800 window (2026-07-26)
    //
    //  The window maps listener k -> ctx row k and talker t -> ctx row
    //  (L-1)+t, so an LxT shape needs L+T-1 attribute rows. milan_datapath
    //  used to size the engine at N_STREAMS = max(L,T): at 4x4 every talker
    //  row (4,5,6) and at 8x8 rows 8..14 were >= N_CTX_P and KL_lwsrp_ctx
    //  refused them - silently, and the readback then ALIASED row 0, so the
    //  window reported the legacy pair's live status and the legacy sid for
    //  a row that had never been provisioned.
    //
    //  Plus: the ctx port carries a per-row TSpec but the window sources it
    //  from the shared LWSRP_TSPEC, so a 2ch and an 8ch talker reserved
    //  identically. The datapath now derives MaxFrameSize from the SAME
    //  TCTX w0 `chans` the packetizer frames with (MSDU = 24 + 24*C), so
    //  the reservation and the wire cannot disagree.
    // ==================================================================
    printf("-- lwSRP ctx rows via 0x800: row map, sid honesty, TSpec --\n");
    {
        enum { A_LWSRP_STATUS = 0x694, A_SW_SRP = 0x85C };
        // engine ON (enable + talker declare); the ctx port only grants
        // while the engine runs, so the window's SRP master needs this
        axi_write(A_LWSRP_CTRL, 0x17);      // enable + talker, class-A queue 5
        for (int c = 0; c < 256; c++) step();

        // ---- talker idx 1 -> ctx row (N-1)+1 -------------------------
        const uint32_t T1_LO = 0x0000A101, T1_HI = 0x0200BEEF;
        axi_write(A_STRM_SEL, 0x101);                 // dir=1 (talker) idx=1
        axi_write(A_SW_SID_LO, T1_LO);
        axi_write(A_SW_SID_HI, T1_HI);
        axi_write(A_SW_DMAC_LO, 0xF000FE11);
        axi_write(A_SW_DMAC_HI, 0x000091E0);
        // TCTX w0 = {en, chans=8, vid=2}: arms the stream AND (since the
        // per-row TSpec fix) sets this row's MaxFrameSize = 24 + 24*8 = 216
        axi_write(A_SW_CTRL, (2u << 5) | (8u << 1) | 1u);
        for (int c = 0; c < 512; c++) step();

        // the window's SRP words must now describe THIS row, not row 0's
        uint32_t sid_lo = axi_read(A_SW_SID_LO);
        uint32_t sid_hi = axi_read(A_SW_SID_HI);
        for (int g = 0; g < 32 && sid_lo != T1_LO; g++) {
            for (int c = 0; c < 64; c++) step();
            sid_lo = axi_read(A_SW_SID_LO); sid_hi = axi_read(A_SW_SID_HI);
        }
        ck("talker idx1: window SID_LO = the row we provisioned",
           sid_lo, T1_LO);
        ck("talker idx1: window SID_HI = the row we provisioned",
           sid_hi, T1_HI);
        // NEGATIVE LEG: it is NOT the legacy row-0 sid the refused row used
        // to alias ({station MAC, uid 0}; the harness MAC is 0 so row 0's
        // sid is 0 - a refused row read 0/0 here)
        ck("talker idx1: NOT the aliased legacy sid",
           (sid_lo == 0 && sid_hi == 0) ? 1 : 0, 0);

        uint32_t srp = axi_read(A_SW_SRP);
        ck("talker idx1: SRP row valid", (srp >> 15) & 1, 1);
        ck("talker idx1: SRP row dir = talker", (srp >> 14) & 1, 0);
        ck("talker idx1: SRP row is backed (not the 0xDEAD sentinel)",
           (srp & 0xFFFF) == 0xDEAD ? 1 : 0, 0);

        // ---- talker idx 2 -> ctx row (N-1)+2, a DIFFERENT geometry ----
        const uint32_t T2_LO = 0x0000A202, T2_HI = 0x0200BEEF;
        axi_write(A_STRM_SEL, 0x102);
        axi_write(A_SW_SID_LO, T2_LO);
        axi_write(A_SW_SID_HI, T2_HI);
        axi_write(A_SW_DMAC_LO, 0xF000FE12);
        axi_write(A_SW_DMAC_HI, 0x000091E0);
        axi_write(A_SW_CTRL, (2u << 5) | (2u << 1) | 1u);   // 2ch -> 72
        for (int c = 0; c < 512; c++) step();
        sid_lo = axi_read(A_SW_SID_LO);
        for (int g = 0; g < 32 && sid_lo != T2_LO; g++) {
            for (int c = 0; c < 64; c++) step();
            sid_lo = axi_read(A_SW_SID_LO);
        }
        ck("talker idx2: its own row, distinct from idx1", sid_lo, T2_LO);
        ck("talker idx2: SRP row valid", (axi_read(A_SW_SRP) >> 15) & 1, 1);
        // idx1 is untouched by idx2's provisioning (separate rows)
        axi_write(A_STRM_SEL, 0x101);
        sid_lo = axi_read(A_SW_SID_LO);
        for (int g = 0; g < 32 && sid_lo != T1_LO; g++) {
            for (int c = 0; c < 64; c++) step();
            sid_lo = axi_read(A_SW_SID_LO);
        }
        ck("talker idx1 still its own row after idx2", sid_lo, T1_LO);

        // ---- listener rows live BELOW the talker block ----------------
        // listener idx 1 is ctx row 1; provisioning it must not disturb
        // talker idx 1 (ctx row (N-1)+1). Pre-fix they were the SAME row.
        axi_write(A_STRM_SEL, 0x001);
        axi_write(A_SW_SID_LO, 0x00030001);
        axi_write(A_SW_SID_HI, 0x03000000);
        axi_write(A_SW_CTRL, (RT_DMA << 1) | 1u);
        for (int c = 0; c < 512; c++) step();
        uint32_t lsrp = axi_read(A_SW_SRP);
        ck("listener idx1: SRP row dir = listener", (lsrp >> 14) & 1, 1);
        axi_write(A_STRM_SEL, 0x101);
        sid_lo = axi_read(A_SW_SID_LO);
        for (int g = 0; g < 32 && sid_lo != T1_LO; g++) {
            for (int c = 0; c < 64; c++) step();
            sid_lo = axi_read(A_SW_SID_LO);
        }
        ck("talker idx1 survives a listener-row commit", sid_lo, T1_LO);

        // ---- the shortfall flag: 0 on a correctly-sized engine --------
        ck("LWSRP_STATUS[11] ctx shortfall clear",
           (axi_read(0x694) >> 11) & 1, 0);

        // ---- per-row TSpec ON THE WIRE --------------------------------
        // Re-declare both talker rows and read the MaxFrameSize each one
        // puts in its own TalkerAdvertise vector. 8ch -> 216, 2ch -> 72.
        int mf1 = -1, mf2 = -1;
        std::vector<uint8_t> cur;
        dut->m_axis_mac_tx_tready = 1;
        for (int c = 0; c < 240000 && (mf1 < 0 || mf2 < 0); c++) {
            lo();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                for (int l = 0; l < 8; l++)
                    if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                        cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                if (dut->m_axis_mac_tx_tlast) {
                    // MSRP MRPDU whose first message is TalkerAdvertise:
                    // eth 14 + ver 1 + msg hdr 4, then 28-byte vectors
                    if (cur.size() >= 47 && cur[12] == 0x22 && cur[13] == 0xEA
                        && cur[15] == 1) {
                        size_t listlen = ((size_t)cur[17] << 8) | cur[18];
                        for (size_t o = 0;
                             o + 28 <= listlen - 2 && 19 + o + 28 <= cur.size();
                             o += 28) {
                            const uint8_t* v = &cur[19 + o];
                            uint32_t slo = ((uint32_t)v[6] << 24) |
                                           ((uint32_t)v[7] << 16) |
                                           ((uint32_t)v[8] << 8) | v[9];
                            int mf = (v[18] << 8) | v[19];
                            if (slo == T1_LO) mf1 = mf;
                            if (slo == T2_LO) mf2 = mf;
                        }
                    }
                    cur.clear();
                }
            }
            hi();
        }
        ck("talker idx1 TalkerAdvertise MaxFrameSize = 24 + 24*8",
           (unsigned)mf1, 216);
        ck("talker idx2 TalkerAdvertise MaxFrameSize = 24 + 24*2",
           (unsigned)mf2, 72);
        // NEGATIVE LEG: the two rows do NOT share one value, and neither
        // fell back to the shared LWSRP_TSPEC reset (0x00E0 = 224)
        ck("per-row TSpec: the two rows differ", mf1 == mf2 ? 1 : 0, 0);
        ck("per-row TSpec: neither is the shared LWSRP_TSPEC 224",
           (mf1 == 224 || mf2 == 224) ? 1 : 0, 0);

        axi_write(A_LWSRP_CTRL, 0x0);
    }

    // ==================================================================
    //  CRF Media Clock Output as an ACMP talker source  (item 5, §3.5)
    //
    //  With N >= 2 AAF sinks the CRF output is mandatory, and a controller
    //  must be able to bind it with the SAME CONNECT_TX/PROBE_TX it uses
    //  for audio. milan_datapath gives KL_acmp_tlkr_ctx one more source
    //  context at talker_unique_id = N_STREAMS whose DMAC is the MAAP block
    //  slot base+N_STREAMS; KL_crf_tx then takes that same {sid, dmac} pair
    //  whenever CRFT_SID/CRFT_DMAC are left at 0, so the answer and the
    //  frames cannot disagree.
    // ==================================================================
    printf("-- CRF media-clock output: ACMP talker context at uid N --\n");
    {
        enum { A_CRFT_CTRL = 0x750,
               A_CRFT_SIDLO = 0x754, A_CRFT_SIDHI = 0x758,
               A_CRFT_DMLO = 0x75C, A_CRFT_DMHI = 0x760 };
        // the ACMP responder is gated by ADP enable
        axi_write(A_ADP_CTRL, 0x1);
        for (int c = 0; c < 64; c++) step();

        // a PROBE_TX (CONNECT_TX_COMMAND) for talker_unique_id = uid
        auto probe = [&](uint16_t uid, std::vector<uint8_t>& resp) {
            uint8_t f[70]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0;
            f[14]=0xFC; f[15]=0x00;              // CONNECT_TX_COMMAND
            f[16]=0x00; f[17]=44;
            // talker_entity_id (bytes 34..41) = ours (ADP_EIDHI/LO above)
            f[34]=0x02; f[35]=0x00; f[36]=0x00; f[37]=0xFF;
            f[38]=0xFE; f[39]=0x00; f[40]=0x00; f[41]=0x01;
            f[50]=(uint8_t)(uid >> 8); f[51]=(uint8_t)uid;   // talker_unique_id
            resp.clear();
            std::vector<uint64_t> beats;
            for (int bt = 0; bt < 9; bt++) {
                uint64_t v = 0;
                for (int j = 0; j < 8; j++)
                    if (bt*8+j < 70) v |= (uint64_t)f[bt*8+j] << (8*j);
                beats.push_back(v);
            }
            size_t idx = 0;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 3000; c++) {
                if (idx < beats.size()) {
                    dut->s_axis_mac_rx_tdata  = beats[idx];
                    dut->s_axis_mac_rx_tkeep  = 0xFF;
                    dut->s_axis_mac_rx_tvalid = 1;
                    dut->s_axis_mac_rx_tlast  = (idx == beats.size()-1);
                } else {
                    dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
                }
                lo();
                bool acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            resp.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        hi(); if (acc) idx++;
                        if (resp.size() >= 16 && resp[12] == 0x22 &&
                            resp[13] == 0xF0 && resp[14] == 0xFC) break;
                        resp.clear(); continue;
                    }
                }
                hi();
                if (acc) idx++;
            }
            dut->s_axis_mac_rx_tvalid = 0;
        };
        auto be = [](const std::vector<uint8_t>& v, size_t o, int n) {
            uint64_t r = 0; for (int i = 0; i < n; i++) r = (r<<8) | v[o+i];
            return r;
        };

        std::vector<uint8_t> r;
        probe((uint16_t)NSTREAMS_TB, r);
        ck("CRF probe: a 70-byte ACMP response came back", r.size(), 70);
        if (r.size() == 70) {
            ck("CRF probe: CONNECT_TX_RESPONSE(1)", r[15] & 0x0F, 1);
            ck("CRF probe: status SUCCESS", r[16] >> 3, 0);
            ck("CRF probe: talker_unique_id echoed = N",
               be(r, 50, 2), (unsigned)NSTREAMS_TB);
            // stream_id = {station MAC, uid}; the harness never sets MAC_ADDR
            // so the MAC half is 0 and the uid tail is what identifies it
            ck("CRF probe: stream_id tail = N", be(r, 24, 2),
               (unsigned)NSTREAMS_TB);
            // dest_mac = MAAP/AAF base + N (AAF_DMAC reset 0x91E0F000FE01)
            ck("CRF probe: stream_dest_mac = base + N", be(r, 54, 6),
               0x91E0F000FE01ULL + NSTREAMS_TB);
        }
        // NEGATIVE LEG: one uid past the CRF context is still unknown -
        // this is not a "everything succeeds" responder
        probe((uint16_t)(NSTREAMS_TB + 1), r);
        ck("CRF probe negative: uid N+1 -> TALKER_UNKNOWN_ID",
           r.size() == 70 ? (r[16] >> 3) : 0xFF, 2);
        // and a plain audio uid is untouched by the extra context
        probe(1, r);
        ck("audio uid 1 still SUCCESS", r.size() == 70 ? (r[16] >> 3) : 0xFF, 0);
        ck("audio uid 1 dest_mac = base + 1",
           r.size() == 70 ? be(r, 54, 6) : 0, 0x91E0F000FE01ULL + 1);

        // ---- KL_crf_tx takes the SAME pair when the CSR is left at 0 ----
        ck("CRFT_SID unset (auto)", axi_read(A_CRFT_SIDLO) |
                                    axi_read(A_CRFT_SIDHI), 0);
        ck("CRFT_DMAC unset (auto)", axi_read(A_CRFT_DMLO) |
                                     axi_read(A_CRFT_DMHI), 0);
        axi_write(A_CRFT_CTRL, 0x1);                  // enable the CRF talker
        std::vector<uint8_t> crf; std::vector<uint8_t> cur2;
        for (int c = 0; c < 400000 && crf.empty(); c++) {
            lo();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                for (int l = 0; l < 8; l++)
                    if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                        cur2.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                if (dut->m_axis_mac_tx_tlast) {
                    // AVTP subtype 0x04 = CRF
                    if (cur2.size() >= 26 && cur2[12] == 0x22 &&
                        cur2[13] == 0xF0 && cur2[14] == 0x04) crf = cur2;
                    cur2.clear();
                }
            }
            hi();
        }
        ck("CRF PDU on the wire", crf.empty() ? 0 : 1, 1);
        if (!crf.empty()) {
            ck("CRF PDU dmac = the ACMP answer (base + N)", be(crf, 0, 6),
               0x91E0F000FE01ULL + NSTREAMS_TB);
            ck("CRF PDU stream_id tail = N", be(crf, 24, 2),
               (unsigned)NSTREAMS_TB);
        }
        // NEGATIVE LEG: an explicit CRFT_DMAC still wins outright
        axi_write(A_CRFT_DMLO, 0xF000FEAA);
        axi_write(A_CRFT_DMHI, 0x000091E0);
        crf.clear(); cur2.clear();
        for (int c = 0; c < 400000 && crf.empty(); c++) {
            lo();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                for (int l = 0; l < 8; l++)
                    if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                        cur2.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                if (dut->m_axis_mac_tx_tlast) {
                    if (cur2.size() >= 26 && cur2[12] == 0x22 &&
                        cur2[13] == 0xF0 && cur2[14] == 0x04) crf = cur2;
                    cur2.clear();
                }
            }
            hi();
        }
        ck("explicit CRFT_DMAC overrides the auto pair",
           crf.empty() ? 0 : be(crf, 0, 6), 0x91E0F000FEAAULL);
        axi_write(A_CRFT_CTRL, 0x0);
    }

    // ==================================================================
    //  CRF MEDIA CLOCK OUTPUT AS AN SR CLASS A STREAM
    //  (Milan v1.2 7.3.3 "media clock stream carried under an SRP
    //   reservation of the specified class"; 802.1Q 9.5/9.6 C-TAG;
    //   802.1Q 34.5 / Table 34-1 SR class A = PCP 3; Milan 4.2.7.2.1
    //   {class A, priority 3, VID 2})
    //
    //  Three things had to land together and this block proves all three
    //  plus the interlock that keeps them together:
    //    (1) the 802.1Q C-TAG on the CRF frames,
    //    (2) the CRF PDUs on the DATA lane (they no longer pass the
    //        control min-IFG gasket - covered by the frame still arriving
    //        at the MAC in every leg below),
    //    (3) the MSRP Talker Advertise attribute row for the stream.
    //
    //  THE TRAP: a tagged stream with no declaration is not a class A
    //  stream, it is unshaped traffic squatting in the reserved SR VLAN.
    //  The tag is therefore DERIVED from the declaration in RTL, and the
    //  two negative legs below are the proof that it cannot be set alone.
    // ==================================================================
    printf("-- CRF media clock output: SR class A (Milan 7.3.3) --\n");
    {
        enum { A_CRFT_CTRL = 0x750, A_CRFT_DMLO = 0x75C, A_CRFT_DMHI = 0x760 };
        const uint64_t CRF_DMAC = 0x91E0F000FE01ULL + NSTREAMS_TB;
        const int      SR_VID   = 2;      // LWSRP_VID reset (Milan 4.2.7.2.1)
        const int      SR_PCP   = 3;      // 802.1Q 34.5 / Table 34-1
        auto be = [](const std::vector<uint8_t>& v, size_t o, int n) {
            uint64_t r = 0; for (int i = 0; i < n; i++) r = (r<<8) | v[o+i];
            return r;
        };

        // back to the AUTO {sid, dmac} pair - the shipping path, where the
        // declaration and the frames are derived from ONE source
        axi_write(A_CRFT_DMLO, 0x0);
        axi_write(A_CRFT_DMHI, 0x0);

        // grab the next CRF PDU in EITHER shape. The discriminator is the
        // ethertype position: untagged 0x22F0 at 12, tagged 0x8100 at 12
        // with 0x22F0 pushed to 16. subtype 0x04 = CRF either way.
        auto grab_crf = [&](std::vector<uint8_t>& out, int budget) -> bool {
            std::vector<uint8_t> cur3; out.clear();
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < budget; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur3.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        bool untag = cur3.size() >= 26 && cur3[12] == 0x22 &&
                                     cur3[13] == 0xF0 && cur3[14] == 0x04;
                        bool tag   = cur3.size() >= 30 && cur3[12] == 0x81 &&
                                     cur3[13] == 0x00 && cur3[16] == 0x22 &&
                                     cur3[17] == 0xF0 && cur3[18] == 0x04;
                        if (untag || tag) { out = cur3; hi(); return true; }
                        cur3.clear();
                    }
                }
                hi();
            }
            return false;
        };
        const int CRF_BUDGET = 160000;   // > 2 event periods (49152 each)

        // ---- LEG 1 (the DEFAULT BUILD): class A bit clear -------------
        // lwSRP fully running, CRF talker running, CRFT_CTRL[1] = 0.
        // This is what every existing bitstream does and it must not move.
        axi_write(A_LWSRP_CTRL, 0x17);          // enable + talker declare
        for (int c = 0; c < 256; c++) step();
        axi_write(A_CRFT_CTRL, 0x1);            // en=1, class_a=0
        std::vector<uint8_t> f1;
        ck("class A off: a CRF PDU still reaches the MAC",
           grab_crf(f1, CRF_BUDGET) ? 1 : 0, 1);
        if (!f1.empty()) {
            ck("class A off: UNTAGGED (ethertype 22F0 at 12)",
               (f1[12] << 8) | f1[13], 0x22F0);
            ck("class A off: 60-octet legacy frame", (long)f1.size(), 60);
            ck("class A off: dmac = the ACMP answer", be(f1, 0, 6), CRF_DMAC);
        }
        uint32_t st = axi_read(A_CRFT_CTRL);
        ck("class A off: 0x750[4] TA not declared", (st >> 4) & 1, 0);
        ck("class A off: 0x750[5] not tagged",      (st >> 5) & 1, 0);
        ck("class A off: 0x750[19:8] VID reads 0",  (st >> 8) & 0xFFF, 0);

        // ---- LEG 2 (NEGATIVE - THE TRAP): class A bit SET, lwSRP OFF --
        // Asking for the tag without an engine that can declare must NOT
        // produce a tagged frame. If this leg ever tags, the interlock is
        // gone and the board is emitting an unreserved stream on the SR
        // VLAN.
        axi_write(A_LWSRP_CTRL, 0x0);           // no engine -> no declaration
        axi_write(A_CRFT_CTRL, 0x3);            // en=1, class_a=1
        for (int c = 0; c < 2048; c++) step();
        std::vector<uint8_t> f2;
        ck("lwSRP off: a CRF PDU still reaches the MAC (Milan 5.3.7.3 - a"
           " Stream Output is never stopped)",
           grab_crf(f2, CRF_BUDGET) ? 1 : 0, 1);
        if (!f2.empty())
            ck("lwSRP off + class A asked: STILL UNTAGGED (the interlock)",
               (f2[12] << 8) | f2[13], 0x22F0);
        st = axi_read(A_CRFT_CTRL);
        ck("lwSRP off: 0x750[1] readback keeps what was written",
           (st >> 1) & 1, 1);
        ck("lwSRP off: 0x750[5] tag refused", (st >> 5) & 1, 0);

        // ---- LEG 3+4 (POSITIVE): declaration exists -> frames are tagged,
        // and the MSRP Talker Advertise that authorises them is on the wire.
        // ONE capture loop for both: the applicant declares on the
        // provisioning refresh, and the next periodic re-declare is a JoinTime
        // multiple away (millions of cycles) - a later window would miss it
        // and "no TalkerAdvertise" would be a TB artefact, not a defect.
        int      ta_hit = 0, ta_mf = -1, ta_iv = -1, ta_pr = -1, ta_vid = -1;
        uint64_t ta_dmac = 0;
        std::vector<uint8_t> f3;
        {
            std::vector<uint8_t> cur4;
            axi_write(A_LWSRP_CTRL, 0x17);      // provisions the CRF row NOW
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 500000 && (!ta_hit || f3.empty()); c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur4.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        // (a) the CRF PDU, in whichever shape it left
                        bool untag = cur4.size() >= 26 && cur4[12] == 0x22 &&
                                     cur4[13] == 0xF0 && cur4[14] == 0x04;
                        bool tag   = cur4.size() >= 30 && cur4[12] == 0x81 &&
                                     cur4[13] == 0x00 && cur4[16] == 0x22 &&
                                     cur4[17] == 0xF0 && cur4[18] == 0x04;
                        if ((untag || tag) && f3.empty()) f3 = cur4;
                        // (b) the MSRP MRPDU whose first message is a
                        // TalkerAdvertise (802.1Q 35.2.2.4): eth 14 + ver 1 +
                        // msg hdr 4, then 28-octet single-value vectors
                        if (!ta_hit && cur4.size() >= 47 && cur4[12] == 0x22 &&
                            cur4[13] == 0xEA && cur4[15] == 1) {
                            size_t listlen = ((size_t)cur4[17] << 8) | cur4[18];
                            for (size_t o = 0;
                                 o + 28 <= listlen - 2 && 19 + o + 28 <= cur4.size();
                                 o += 28) {
                                const uint8_t* v = &cur4[19 + o];
                                // FirstValue: StreamID(8) = {station MAC, uid};
                                // the harness never sets MAC_ADDR so the low
                                // 32 bits ARE the uid
                                uint32_t slo = ((uint32_t)v[6] << 24) |
                                               ((uint32_t)v[7] << 16) |
                                               ((uint32_t)v[8] << 8) | v[9];
                                if (slo != (uint32_t)NSTREAMS_TB) continue;
                                ta_dmac = 0;
                                for (int i = 0; i < 6; i++)
                                    ta_dmac = (ta_dmac << 8) | v[10+i];
                                ta_vid = (v[16] << 8) | v[17];
                                ta_mf  = (v[18] << 8) | v[19];
                                ta_iv  = (v[20] << 8) | v[21];
                                ta_pr  = v[22];
                                ta_hit = 1;
                            }
                        }
                        cur4.clear();
                    }
                }
                hi();
            }
        }
        ck("class A on: a CRF PDU reaches the MAC", f3.empty() ? 0 : 1, 1);
        if (f3.size() >= 46) {
            ck("class A on: TPID 0x8100 at 12 (802.1Q 9.5)",
               (f3[12] << 8) | f3[13], 0x8100);
            ck("class A on: TCI = PCP 3 | DEI 0 | VID 2 (802.1Q 9.6)",
               (f3[14] << 8) | f3[15], (SR_PCP << 13) | SR_VID);
            ck("class A on: ethertype 22F0 pushed to 16",
               (f3[16] << 8) | f3[17], 0x22F0);
            ck("class A on: AVTP subtype CRF at 18", f3[18], 0x04);
            ck("class A on: type CRF_AUDIO_SAMPLE at 21", f3[21], 0x01);
            // the whole AVTPDU shifts +4: stream_id 18..25 -> 22..29
            ck("class A on: stream_id tail still N", be(f3, 28, 2),
               (unsigned)NSTREAMS_TB);
            ck("class A on: base_frequency 48000 at 30",
               be(f3, 30, 4), 0xBB80ULL);
            ck("class A on: timestamp_interval 96 at 36", be(f3, 36, 2), 96);
            ck("class A on: dmac unchanged by tagging",
               be(f3, 0, 6), CRF_DMAC);
            // the tag REPLACES pad - the frame must not grow past the
            // 802.3 minimum, and everything after the AVTPDU stays zero
            ck("class A on: still a 60-octet frame", (long)f3.size(), 60);
            long tp = 1; for (size_t p = 46; p < f3.size(); p++) if (f3[p]) tp = 0;
            ck("class A on: zero pad 46..59", tp, 1);
        }
        st = axi_read(A_CRFT_CTRL);
        ck("class A on: 0x750[4] TA declared",  (st >> 4) & 1, 1);
        ck("class A on: 0x750[5] tagged",       (st >> 5) & 1, 1);
        ck("class A on: 0x750[19:8] VID = 2",   (st >> 8) & 0xFFF, SR_VID);
        ck("class A on: 0x750[22:20] PCP = 3",  (st >> 20) & 0x7, SR_PCP);
        ck("class A on: 0x750[1:0] RW bits still read back",
           st & 0x3, 0x3);

        // ---- LEG 4: the MSRP Talker Advertise for THIS stream ---------
        // 802.1Q 35.2.2.4 FirstValue(25) inside a 28-byte single-value
        // vector: StreamID(8) DataFrameParameters{DMAC(6) VID(2)}
        // TSpec{MaxFrameSize(2) MaxIntervalFrames(2)} PriorityAndRank(1)
        // AccumulatedLatency(4). Captured in the loop above.
        ck("MSRP: a TalkerAdvertise for the CRF stream is on the wire",
           ta_hit, 1);
        ck("MSRP: DataFrameParameters DMAC = the CRF stream's DMAC",
           ta_dmac, CRF_DMAC);
        ck("MSRP: DataFrameParameters VID = the VID on the frames",
           ta_vid, SR_VID);
        // MaxFrameSize is the MSDU: the 60-octet L2 frame minus the tagged
        // Ethernet header (14 + 4). NOT the 28-octet AVTPDU - the pad is on
        // the wire and the bridge has to budget for it.
        ck("MSRP: TSpec MaxFrameSize = padded MSDU 42", ta_mf, 42);
        // class A measurement interval is 125 us and CRF sends every 2 ms,
        // so 1 is the FLOOR a TSpec can express (16x over-provision, on
        // record; not to be "fixed" by weakening the class)
        ck("MSRP: TSpec MaxIntervalFrames = 1 (the floor)", ta_iv, 1);
        ck("MSRP: PriorityAndRank = priority 3, rank 1 (0x70)", ta_pr, 0x70);
        // NEGATIVE LEG: the CRF row did not just alias a neighbour - its
        // MaxFrameSize is none of the AAF talker values (216 / 72 / the
        // shared LWSRP_TSPEC 224)
        ck("MSRP: CRF TSpec is its own, not an AAF row's",
           (ta_mf == 216 || ta_mf == 72 || ta_mf == 224) ? 1 : 0, 0);

        // ---- LEG 5: withdrawing class A returns the untagged shape ----
        axi_write(A_CRFT_CTRL, 0x1);            // class_a back to 0
        for (int c = 0; c < 2048; c++) step();
        std::vector<uint8_t> f5;
        ck("class A withdrawn: CRF PDU still flows",
           grab_crf(f5, CRF_BUDGET) ? 1 : 0, 1);
        if (!f5.empty()) {
            ck("class A withdrawn: back to UNTAGGED",
               (f5[12] << 8) | f5[13], 0x22F0);
            ck("class A withdrawn: 60-octet legacy frame", (long)f5.size(), 60);
        }
        ck("class A withdrawn: 0x750[5] clear",
           (axi_read(A_CRFT_CTRL) >> 5) & 1, 0);

        axi_write(A_CRFT_CTRL, 0x0);
        axi_write(A_LWSRP_CTRL, 0x0);
    }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
