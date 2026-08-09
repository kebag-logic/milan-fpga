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

// ---- ACMP PROBE_TX sniffer: the listener matches a PROBE_TX_RESPONSE on
// controller+talker+tuid+sequence_id (Milan 5.5.3.5.18 step 1), so answers
// must echo the probe's OWN sequence_id — harvest it off the egress while
// inject() drains. A probe launches within the bind's drain window, and the
// 100 MHz TMR_NO_RESP (20M cycles) means no second draw can occur inside a
// leg, so the per-luid latch stays valid across the follow-up CSR reads.
static std::vector<uint8_t> acmp_sniff_fr;
static uint16_t probe_seq_by_luid[16];
static void acmp_sniff() {
    if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
        for (int l = 0; l < 8; l++)
            if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                acmp_sniff_fr.push_back(
                    (dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
        if (dut->m_axis_mac_tx_tlast) {
            if (acmp_sniff_fr.size() >= 70 && acmp_sniff_fr[12] == 0x22 &&
                acmp_sniff_fr[13] == 0xF0 && acmp_sniff_fr[14] == 0xFC &&
                (acmp_sniff_fr[15] & 0xF) == 0x0) {   // CONNECT_TX_COMMAND
                int luid = ((acmp_sniff_fr[52] << 8) | acmp_sniff_fr[53]) & 0xF;
                probe_seq_by_luid[luid] =
                    (uint16_t)((acmp_sniff_fr[62] << 8) | acmp_sniff_fr[63]);
            }
            acmp_sniff_fr.clear();
        }
    }
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
    acmp_sniff_fr.clear();   // a fragment drained elsewhere is not a frame
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
        acmp_sniff();
        hi();
        if (in_acc) idx++;
    }
    dut->s_axis_mac_rx_tvalid = 0;
}

// ---- gh #58 D1 end-to-end: one AECP AEM transaction through the REAL RX
// path, the response fished off the MAC TX trunk (subtype 0xFB; the only
// 0xFB frames in this sim are our responses - nothing ever REGISTERs).
// dst MAC = the station MAC, which this harness leaves at its reset 0.
static std::vector<uint8_t> aecp_xact(uint16_t cmd, uint16_t sq,
                                      const std::vector<uint8_t>& pl,
                                      int cyc = 200000) {
    uint8_t f[80]; memset(f, 0, sizeof f);
    const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
    memcpy(f+6, csrc, 6);
    f[12]=0x22; f[13]=0xF0; f[14]=0xFB; f[15]=0x00;      // AECP AEM_COMMAND
    uint16_t cdl = (uint16_t)(12 + pl.size());
    f[16]=(uint8_t)((cdl >> 8) & 0x7); f[17]=(uint8_t)cdl;
    const uint8_t teid[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
    memcpy(f+18, teid, 8);                                // = A_ADP_EID
    const uint8_t ceid[8] = {0x68,0x05,0xCA,0xFF,0xFE,0x95,0xB2,0xD1};
    memcpy(f+26, ceid, 8);
    f[34]=(uint8_t)(sq >> 8); f[35]=(uint8_t)sq;
    f[36]=(uint8_t)((cmd >> 8) & 0x7F); f[37]=(uint8_t)cmd;
    for (size_t i = 0; i < pl.size() && 38 + i < sizeof f; i++) f[38+i] = pl[i];
    size_t flen = 38 + pl.size(); if (flen < 60) flen = 60;
    inject(f, flen, 40);
    std::vector<uint8_t> cur, resp;
    dut->m_axis_mac_tx_tready = 1;
    for (int c = 0; c < cyc && resp.empty(); c++) {
        lo();
        if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
            for (int l = 0; l < 8; l++)
                if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                    cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
            if (dut->m_axis_mac_tx_tlast) {
                if (cur.size() > 17 && cur[12] == 0x22 && cur[13] == 0xF0 &&
                    cur[14] == 0xFB)
                    resp = cur;
                cur.clear();
            }
        }
        hi();
    }
    return resp;
}
static long aecp_status(const std::vector<uint8_t>& b) {
    return b.size() > 16 ? (b[16] >> 3) & 0x1F : -1;
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
    ck("VERSION 0x0021 (the TSpec describes the frame this build emits)",
       axi_read(A_VERSION), 0x0001003D);

#ifdef AAF_PB_TB
    // ---- task #26 (0x002C): the BOOT SEED is CSR-visible before any ----
    //      software touch. This leg's shape compiles AEM_ODYNMAP, so the
    //      AECP builder must have walked the declared identity image into
    //      the capture map RAM within its post-reset IDLE cycles - key 0's
    //      declared template is RING ch0 ({en,src=3} = raw 0x1300), and
    //      0x900[0] has never been written (the crossbar is in-circuit by
    //      construction, there is no arm to poke). A zero or poison read
    //      here means the seeder never ran and every talker would wake
    //      streaming an EMPTY map's silence.
    {
        axi_write(0x904, 0x100);             // capture side, key 0
        axi_write(0x910, 1);
        uint32_t sv = 0;
        for (int g = 0; g < 64; g++) {
            sv = axi_read(0x910);
            if ((sv & 1) == 0) break;
        }
        uint32_t seed0 = axi_read(0x914);
        ck("0x002C seed: capture key 0 readback VALID (bit 26)",
           (seed0 >> 26) & 1, 1);
        ck("0x002C seed: key 0 carries the declared RING template 0x1300",
           seed0 & 0x1FFF, 0x1300);
    }
#endif

    printf("-- 5.5.2.7 SRP-only licence at t>0 STRAIGHT FROM RESET "
           "(2026-07-30 bite) --\n");
    // The silicon defect this bites: TCTX w0 CTRL[0] was an ENABLE with
    // reset 0 and NO board-software writer, so a shape-static build could
    // never egress any talker above 0 - measured on m001g, the soak's
    // t0.s0 leg fully green while t1/t2/t3 all failed with tx-interval 0
    // despite CONNECT SUCCESS, SRP rows declared, and tu=0. The fix flips
    // the lever to a DISARM (reset 0 = armed): a context the shape
    // elaborated streams by construction, like t0 under AAF_CTRL[0].
    // This case is the boot scenario verbatim - NO window op ever touches
    // t3 before or during it; a registered Listener Ready alone must open
    // its gate. Reverting the polarity (or restoring the tctx_en_r AND
    // term) reddens exactly the two opened/flowed checks below.
    {
        axi_write(A_AAF_CTRL, 0x00020001);   // AAF en + VID 2, bypass CLEAR
        // engine + TALKER-DECLARE + the LWSRP_CTRL[5] DECLARE bypass: this
        // case proves the fabric PROVISIONER (every row declares with no
        // window op), which since the 4.3.3.1 declaration gate needs a
        // probe/listener per row OR the bypass - the declared-at-boot
        // posture under test here is exactly what the bypass restores. The
        // gate itself (cold boot = NO TalkerAdvertise) is proven in its own
        // case below.
        axi_write(A_LWSRP_CTRL, 0x37);
        for (int c = 0; c < 512; c++) step();
        ck("t>0 reset licence: gate3 CLOSED with no listener",
           (tap_stream_en() >> 3) & 1, 0);
        // Listener Ready MRPDU for t3's DERIVED sid {station_mac, uid 3} -
        // the harness MAC is 0, so FirstValue = {0..0, 0x0003}. Same MRPDU
        // shape as the t0 SRP-only case further down.
        uint8_t lr[60]; memset(lr, 0, sizeof lr);
        const uint8_t msrp_da3[6] = {0x01,0x80,0xC2,0x00,0x00,0x0E};
        memcpy(lr, msrp_da3, 6);
        lr[6]=0x02; lr[7]=0xAA; lr[8]=0xBB; lr[9]=0xCC; lr[10]=0xDD;
        lr[11]=0x01;
        lr[12]=0x22; lr[13]=0xEA;
        lr[14]=0;                      // ProtocolVersion
        lr[15]=3; lr[16]=8;            // Listener (type 3), AttributeLength
        lr[17]=0; lr[18]=14;           // AttributeListLength
        lr[19]=0; lr[20]=1;            // VectorHeader: LeaveAll 0, NOV 1
        lr[28]=0x03;                   // FirstValue = {0..0, uid 0x0003}
        lr[29]=36;                     // ThreePacked JoinIn
        lr[30]=128;                    // FourPacked Ready
        dut->m_axis_rx_tready = 1;
        // ---- ONE TX SNIFFER, RUNNING FROM BEFORE THE GATE OPENS ---------
        // It has to start here rather than after the checks below, and the
        // reason is a measured timing fact: MRP declares the row ONCE
        // immediately on the join event and then only every JoinTime, which
        // lwsrp_pkg puts at 200 ms = 20,000,000 clocks at the harness's
        // 100 MHz (KL_lwsrp_timers TICK_DIV_C). A capture window opened after
        // the PDU poll misses the immediate declaration by ~3 ms and would
        // have to run fifty times longer to see the next one. Both the AAF
        // frame and the TalkerAdvertise are parsed out of the same beat
        // stream so the two numbers describe the same instant.
        std::vector<uint8_t> w3;
        int seen3 = 0, id3 = 0, vid3 = -1; uint64_t dm3 = 0;
        // TALKER 1 IS THE TSPEC SUBJECT, not t3, and that is a measured
        // constraint rather than a preference: MRP declares each attribute
        // once immediately and then per JoinTime, and lwsrp_pkg's JoinTime of
        // 200 ms is 20,000,000 clocks here - so within this block exactly ONE
        // TalkerAdvertise leaves the port, the first row the fabric arbiter
        // reaches, uid 1. Waiting for uid 3's would cost ~600 ms of sim. t1
        // is the same kind of witness: index > 0, fabric-provisioned, never
        // written through the TCTX window.
        int avt1 = -1, mf1 = -1;
        auto pump = [&]() {
            lo();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                for (int l = 0; l < 8; l++)
                    if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                        w3.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                if (dut->m_axis_mac_tx_tlast) {
                    size_t off = (w3.size() > 17 && w3[12] == 0x81
                                  && w3[13] == 0x00) ? 4 : 0;
                    if (w3.size() >= 86 + off && w3[12+off] == 0x22
                        && w3[13+off] == 0xF0 && w3[14+off] == 0x02) {
                        int uid = (w3[24+off] << 8) | w3[25+off];
                        if (uid == 3) {
                            seen3 = 1; id3 = uid;
                            dm3 = 0;
                            for (int b = 0; b < 6; b++)
                                dm3 = (dm3 << 8) | w3[b];
                            if (off) vid3 = ((w3[14] & 0x0F) << 8) | w3[15];
                        }
                        // the MSDU: L2 frame less DA/SA/EtherType and the
                        // C-TAG - exactly what 802.1Q 35.2.2.8.4 a) calls
                        // MaxFrameSize ("the maximum frame size that the
                        // Talker will produce")
                        if (uid == 1) avt1 = (int)w3.size() - 14 - (int)off;
                    }
                    // MSRP MRPDU (untagged, 0x22EA), first message
                    // TalkerAdvertise: v[0..1] VectorHeader, v[2..9] StreamID,
                    // v[10..15] DA, v[16..17] VID, v[18..19] MaxFrameSize -
                    // the same walk the per-row sweep further down uses
                    if (w3.size() >= 47 && w3[12] == 0x22 && w3[13] == 0xEA) {
                        size_t ll = ((size_t)w3[17] << 8) | w3[18];
                        for (size_t o = 0;
                             o + 28 <= ll - 2 && 19 + o + 28 <= w3.size();
                             o += 28) {
                            const uint8_t* v = &w3[19 + o];
                            if ((((int)v[8] << 8) | v[9]) == 1)
                                mf1 = ((int)v[18] << 8) | v[19];
                        }
                    }
                    w3.clear();
                }
            }
            hi();
        };
        dut->m_axis_mac_tx_tready = 1;
        for (int c = 0; c < 1000; c++) pump();
        inject(lr, 60, 2000);
        inject(lr, 60, 2000);          // bridges re-declare every JoinTime
        // ...and the same for uid 1, so the talker whose TalkerAdvertise this
        // block can actually catch also puts frames on the wire. Same MRPDU,
        // one byte different.
        lr[28] = 0x01;                 // FirstValue = {0..0, uid 0x0001}
        inject(lr, 60, 2000);
        inject(lr, 60, 2000);
        lr[28] = 0x03;
        int opened3 = 0;
        for (int g = 0; g < 400 && !opened3; g++) {
            for (int c = 0; c < 64; c++) pump();
            opened3 = (tap_stream_en() >> 3) & 1;
        }
        ck("t>0 reset licence: Ready(uid3) ALONE opens gate3 "
           "(no window write, no ACMP)", opened3, 1);
        ck("t>0 reset licence: t0 stayed dark (no Ready for uid0, no "
           "bypass)", tap_stream_en() & 1, 0);
        // FRAMES: the per-talker TCTX w5 counter through the window, POLLED.
        // NOT A_AAF_FRAMES (0x660) - that alias counts t0 only
        // (KL_aaf_packetizer frames_sent_o, `if (et_r == 0)`), so asserting
        // it here would be unsatisfiable beside the t0-is-dark check above.
        // Zero-fill emits ~1 PDU per 6*512 audio-clock ticks, so poll.
        int t3pdus = 0;
        for (int g = 0; g < 60 && t3pdus < 2; g++) {
            for (int c = 0; c < 3072; c++) pump();
            axi_write(A_STRM_SEL, 0x103);
            snap_and_wait();
            t3pdus = axi_read(A_SW_PDUS);
        }
        ck("t>0 reset licence: t3 PDUs flowed under the licence",
           t3pdus >= 2, 1);
        // ---- AND THE FRAMES CARRY t3's OWN IDENTITY (2026-07-30) --------
        // The bite that matters most. Nothing writes the talker window on a
        // real board, and the packetizer used to read dmac/vid/uid ONLY from
        // that window - so an armed t3 framed to dmac 00:00:00:00:00:00 on
        // VID 0 with stream_id {mac, uid 0}, colliding with t0 and reaching
        // no listener, while its own SRP row declared {mac, uid 3}. Frames
        // existing is NOT the property under test; frames carrying the
        // identity we advertised is. dmac must be the MAAP-block base + 3
        // (the same rule acmp_src_dmac_w answers and srp_fab_dmac_w
        // declares), vid the engine VID, uid16 = 3.
        const unsigned A_AAF_DML = 0x658, A_AAF_DMH = 0x65C;
        const uint64_t base3 = ((uint64_t)(axi_read(A_AAF_DMH) & 0xFFFF) << 32)
                             | (uint64_t)axi_read(A_AAF_DML);
        // top up only if the poll above happened to end between frames
        for (int c = 0; c < 200000 && !(seen3 && mf1 >= 0 && avt1 >= 0); c++)
            pump();
        ck("t>0 identity: a t3 PDU appeared on the wire", seen3, 1);
        ck("t>0 identity: stream_id uid16 == 3 (not t0's 0)", id3, 3);
        ck("t>0 identity: dmac == MAAP base + 3 (not all-zeros)",
           dm3 == base3 + 3, 1);
        ck("t>0 identity: C-TAG VID == the engine VID 2 (not 0)", vid3, 2);
        // MILAN v1.2 4.3.3.2 Table 4.4. MaxFrameSize is the MSDU the Talker
        // "will produce" plus the table's one mandated headroom octet, so
        // declared == emitted + 1 is the clause itself, and it holds at ANY
        // elaborated width - 2, 4 or 8 channels - because neither side is a
        // literal. THE DEFECT IT BITES: milan_datapath's tctx_chans_r reset
        // to 4'd2 while KL_aaf_packetizer reset its chans_r to the elaborated
        // WIRE_CHANS_C, so a 4-channel build emitted a 120-octet AVTPDU and
        // declared 73 - reserving 7.36 Mb/s for a stream occupying 10.368,
        // and the bridge grants CBS credit against the DECLARATION. Slot 0
        // hid it (the fabric mux starts at s=1 and slot 0 keeps
        // cfg_lwsrp_max_frame), the same index-0-works signature as 0x001F.
        // Reverting the reset to 4'd2 reddens exactly the two checks below.
        ck("t>0 TSpec: uid 1 both declared a TalkerAdvertise and framed",
           (mf1 >= 0 && avt1 >= 0) ? 1 : 0, 1);
        ck("t>0 TSpec: declared MaxFrameSize == emitted MSDU + Table 4.4's "
           "one octet (reservation matches the wire at the elaborated width)",
           mf1, avt1 + 1);
        // Restore the legacy flow posture. NO TCTX w0 writes: the per-context
        // lever is gone, so there is nothing to restore there - and writing
        // it would leave residue the flow reads back later ("talker 2 CTRL
        // reads 0"). Engine off withdraws the rows (shape-derived want);
        // AAF_CTRL back to its TRUE reset value 0x00020000 (VID 2, en 0,
        // bypass 0) - writing plain 0 would clear the VID field and set up
        // the VID-0 clobber the rest of the flow assumes away.
        axi_write(A_LWSRP_CTRL, 0x10);
        axi_write(A_AAF_CTRL, 0x00020000);
        for (int c = 0; c < 256; c++) step();
    }

    // ==================================================================
    //  THE 4.3.3.1 TALKER-ADVERTISE DECLARATION GATE (gh #63 I2).
    //  Milan 5.3.7.2 obliges the TalkerAdvertise "as soon as it has VALID
    //  SRP parameters" and 4.3.3.1 defines valid: MAAP-allocated DMAC AND
    //  (a PROBE_TX within 15 s OR a registered Listener attribute). The
    //  clause's own Note kills always-declare. So on a COLD BOOT with the
    //  engine + talker knob on and NO bypass, the wire must carry the
    //  Domain+MVRP pair but NO TalkerAdvertise and no fabric row; a
    //  CONNECT_TX (the Milan probe - the fast-connect path arms the same
    //  window) opens the declaration promptly; and losing the last
    //  interest withdraws it with a talker LV.
    // ==================================================================
    printf("-- 4.3.3.1 declaration gate: cold boot silent, probe opens, "
           "lapse withdraws --\n");
    {
        enum { A_ADP_CTRL_L = 0x600, A_ACMP_LOBS_L = 0x670,
               A_LWSRP_STATUS_L = 0x694, A_SW_SRP_L = 0x85C };
        const uint32_t adp_was = axi_read(A_ADP_CTRL_L);
        const uint32_t eidlo_was = axi_read(0x604);
        const uint32_t eidhi_was = axi_read(0x608);
        axi_write(A_ADP_CTRL_L, 0x1);        // the ACMP responder's gate
        //! the responder matches the probe's talker_entity_id against the
        //! ADP_EID registers - name the entity the probe below carries
        axi_write(0x608, 0x020000FF);
        axi_write(0x604, 0xFE000001);
        //! hold the MAC port CLOSED across the enabling writes so the
        //! one-shot prompt declare pair parks against tready and the
        //! sniffer below captures it whole (MRP re-declares only per
        //! JoinTime = 20M cycles here - a missed first pair never repeats
        //! inside this case's budget)
        dut->m_axis_mac_tx_tready = 0;
        axi_write(A_AAF_CTRL, 0x00020001);   // AAF en, bypass CLEAR
        axi_write(A_LWSRP_CTRL, 0x17);       // engine + talker, NO [5] bypass
        // ---- (a) cold boot: Domain+MVRP declare, NO TalkerAdvertise ----
        int n_dom = 0, n_ta = 0, n_lv = 0;
        std::vector<uint8_t> sn;
        auto sniff = [&](int cycles) {
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < cycles; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            sn.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        if (sn.size() >= 30 && sn[12] == 0x22 && sn[13] == 0xEA) {
                            if (sn[15] == 4) n_dom++;
                            //! a TalkerAdvertise anywhere: row 0 carries it
                            //! as message 2 (byte 28), ctx rows as message 1
                            if (sn[15] == 1) n_ta++;
                            if (sn[28] == 1) {
                                n_ta++;
                                if (sn.size() >= 60 && sn[59] == 5*36) n_lv++;
                            }
                        }
                        sn.clear();
                    }
                }
                hi();
            }
        };
        sniff(40000);
        ck("4.3.3.1: cold boot declares the Domain", n_dom >= 1, 1);
        ck("4.3.3.1: cold boot carries NO TalkerAdvertise", n_ta, 0);
        ck("4.3.3.1: talker_declared (0x694[4]) clear",
           (axi_read(A_LWSRP_STATUS_L) >> 4) & 1, 0);
        axi_write(A_STRM_SEL, 0x101);
        ck("4.3.3.1: fabric row idx1 NOT provisioned",
           (axi_read(A_SW_SRP_L) >> 15) & 1, 0);
        // ---- (b) CONNECT_TX (Milan PROBE_TX) for uid 1 opens row 1 -----
        {
            uint8_t f[70]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            f[6]=0x68; f[7]=0x05; f[8]=0xCA; f[9]=0x95; f[10]=0xB2; f[11]=0xD1;
            f[12]=0x22; f[13]=0xF0;
            f[14]=0xFC; f[15]=0x00;              // CONNECT_TX_COMMAND
            f[16]=0x00; f[17]=44;
            f[34]=0x02; f[35]=0x00; f[36]=0x00; f[37]=0xFF;  // our entity_id
            f[38]=0xFE; f[39]=0x00; f[40]=0x00; f[41]=0x01;
            f[50]=0x00; f[51]=0x01;              // talker_unique_id 1
            //! SHORT drain: inject() forces tready=1, and the row's one
            //! immediate TalkerAdvertise must land inside the SNIFFER
            //! below, not inject()'s own drain (the ingest takes ~10
            //! cycles; classification + provisioning + the declare all
            //! happen after)
            inject(f, 70, 80);
        }
        n_dom = n_ta = n_lv = 0;
        //! park the MAC port for the whole poll phase: the row's ONE
        //! immediate TalkerAdvertise stalls against tready and the sniffer
        //! afterwards captures it whole (a CSR poll's own cycles would
        //! otherwise drain it unseen - the one-shot never repeats inside
        //! this budget)
        dut->m_axis_mac_tx_tready = 0;
        uint32_t srp1 = 0;
        for (int g = 0; g < 400 && !((srp1 >> 15) & 1); g++) {
            for (int c = 0; c < 64; c++) step();
            srp1 = axi_read(A_SW_SRP_L);         // A_STRM_SEL still 0x101
        }
        ck("4.3.3.1: PROBE_TX(uid 1) provisions row 1", (srp1 >> 15) & 1, 1);
        sniff(20000);
        ck("4.3.3.1: ...and its TalkerAdvertise reaches the wire",
           n_ta >= 1, 1);
        ck("4.3.3.1: row 0 still undeclared (uid 0 never probed)",
           (axi_read(A_LWSRP_STATUS_L) >> 4) & 1, 0);
        // ---- (c) a registered listener view via the LOBS socket opens
        //      row 0; dropping the last interest WITHDRAWS with an LV ----
        axi_write(A_ACMP_LOBS_L, 0x1);
        for (int g = 0; g < 200; g++) {
            if ((axi_read(A_LWSRP_STATUS_L) >> 4) & 1) break;
            for (int c = 0; c < 64; c++) step();
        }
        ck("4.3.3.1: listener interest opens row 0 (0x694[4])",
           (axi_read(A_LWSRP_STATUS_L) >> 4) & 1, 1);
        n_dom = n_ta = n_lv = 0;
        dut->m_axis_mac_tx_tready = 0;           // park the LV for the sniffer
        axi_write(A_ACMP_LOBS_L, 0x0);           // the last interest lapses
        sniff(40000);
        ck("4.3.3.1: lapse withdraws - row-0 TalkerAdvertise LV on the wire",
           n_lv >= 1, 1);
        ck("4.3.3.1: talker_declared falls on the lapse",
           (axi_read(A_LWSRP_STATUS_L) >> 4) & 1, 0);
        // restore the flow posture exactly as the block above left it
        axi_write(A_LWSRP_CTRL, 0x10);
        axi_write(A_AAF_CTRL, 0x00020000);
        axi_write(A_ADP_CTRL_L, adp_was);
        axi_write(0x604, eidlo_was);
        axi_write(0x608, eidhi_was);
        for (int c = 0; c < 256; c++) step();
    }

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
    // 2026-07-30: the per-context TCTX CTRL[0] arming lever is GONE - it
    // reset to 0 with no board-software writer, so it held every talker
    // above 0 dark forever, and Milan v1.2 5.3.7.3 / 5.4.2.19 / 5.4.2.20 /
    // 5.5.4.1 leave no room for a per-stream software enable on a Stream
    // Output at all. So AAF_CTRL[0] is now the ONE enable for every talker,
    // exactly as it always was for t0: with it clear, bypass alone must NOT
    // light t1 (this check used to assert the opposite).
    axi_write(A_AAF_CTRL, 0x00020002);   // bypass on, flat enable still 0
    ck("AAF_CTRL.en=0 holds t1 too (one flat enable, no per-context lever)",
       (tap_stream_en() >> 1) & 1, 0);
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
        int t1f = 0, t1sil = 0, t1chans = -1, t1dlen = -1, foreign = 0,
            sibling = 0;
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
                        } else if (uid >= 2 && uid < NSTREAMS_TB) {
                            // 2026-07-30: t2/t3 are ELABORATED contexts and
                            // this posture has bypass on, so they are
                            // licensed and MUST also be framing silence
                            // (Milan 5.3.7.3). They are counted, not
                            // condemned - and the count is only reachable
                            // at all because their identity is now derived
                            // (they used to emit uid 0, i.e. they were
                            // silently booked as t0 and this classifier was
                            // blind to them). The bound is the ELABORATED
                            // shape, not a hard 4: at N=8 talkers 4..7 are
                            // just as real, and hardcoding 4x4 here made the
                            // 8x8 leg call them foreign.
                            sibling++;
                        } else if (uid != 0) {
                            foreign++;      // an uid we never elaborated
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
        // no PDU may carry an unique_id this shape never elaborated
        ck("silence fill: no PDU from an unelaborated uid", foreign, 0);
        // ...and the sibling contexts ARE streaming under the same licence,
        // each under its OWN derived stream_id (they emitted uid 0 before
        // the identity fix, which is exactly what made this test blind)
        ck("silence fill: sibling talkers t2/t3 frame too (5.3.7.3)",
           sibling > 0, 1);
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
        //! 4.3.3.1 (gh #63 I2): with no probe, no bypass and no listener,
        //! the talker knob alone declares NOTHING - the TalkerAdvertise
        //! waits for the Listener registration this case injects, which is
        //! exactly clause condition 2's second arm
        ck("SRP-only: TalkerAdvertise NOT declared yet (0x694[4], 4.3.3.1)",
           (axi_read(0x694) >> 4) & 1, 0);
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
        int opened = 0;
        for (int g = 0; g < 400 && !opened; g++) {
            for (int c = 0; c < 64; c++) step();
            opened = tap_stream_en() & 1;
        }
        ck("SRP-only: Listener Ready ALONE opens the licence (no ACMP ever "
           "sent for t0)", opened, 1);
        // the bench-predicted bound status (8.3.6): 0x37E once the
        // registration lands, vs 0x30 declaring-unbound. Since the 4.3.3.1
        // round the registration ALSO opens the TalkerAdvertise ([4] - the
        // listener-registration arm of the declaration gate), so the whole
        // word settles only after the declare + gate walk; read it settled.
        ck("SRP-only: LWSRP_STATUS reads the BOUND value 0x37E",
           axi_read(0x694), 0x37E);
        ck("SRP-only: the registration OPENED the TalkerAdvertise (0x694[4])",
           (axi_read(0x694) >> 4) & 1, 1);
        // continuity: the gate holds while the registration stands
        uint32_t f0 = axi_read(A_AAF_FRAMES);
        bool held = true;
        for (int g = 0; g < 40; g++) {
            for (int c = 0; c < 128; c++) step();
            if (!(tap_stream_en() & 1)) held = false;
        }
        ck("SRP-only: licence HELD (no STREAMING_WAIT, 5.3.7.3)",
           held ? 1 : 0, 1);
        //! 0x002C: the crossbar lane paces pairs on the 48 kHz media tick
        //! (~2083 cycles/pair, 6-pair PDUs -> ~12.5k cycles between t0
        //! PDUs, and t0 is the ONLY licensed talker here). The old
        //! 5120-cycle window fit the faster bring-up zf grid only; give
        //! the licensed stream two full PDU intervals to show itself.
        for (int c = 0; c < 30000; c++) step();
        ck("SRP-only: frames flowed under it", axi_read(A_AAF_FRAMES) > f0, 1);
        // restore the flow's posture: engine back to the no-talker 0x15,
        // bypass back on (no row was ever touched - pure SRP case)
        axi_write(A_LWSRP_CTRL, 0x15);
        axi_write(A_AAF_CTRL, 0x00020003);
        for (int c = 0; c < 64; c++) step();
    }

    // ==================================================================
    //  MILAN 4.2.7.2.1 DOMAIN ADOPT AT THE DATAPATH (gh #63 I4): a class-A
    //  Domain declaration with a different VID moves LWSRP_DOM (0x788),
    //  the AAF C-TAG on the wire and the CRF talker's 0x750 tag word all
    //  at once - the reservation and the frames are one pair - and the
    //  adoption REVERTS on the engine-enable fall.
    // ==================================================================
    printf("-- 4.2.7.2.1 Domain adopt: 0x788 + the AAF/CRF tag words --\n");
    {
        enum { A_LWSRP_DOM_L = 0x788, A_CRFT_CTRL_L = 0x750,
               A_LINK_CTRL_L = 0x71C };
        // entry state: LWSRP_CTRL 0x15 (engine on), AAF_CTRL 0x00020003
        // (en + bypass) - t0 is emitting tagged AAF zero-fill PDUs.
        // Adoption reverts on link-down, and eff_link rides the LINK GUARD's
        // establishment window - park the guard disabled (LINK_CTRL[2]) so
        // eff_link = i_link_up = 1 deterministically for this case.
        const uint32_t link_was = axi_read(A_LINK_CTRL_L);
        axi_write(A_LINK_CTRL_L, link_was | 0x4);
        for (int c = 0; c < 64; c++) step();
        ck("adopt-dp: defaults in force (0x788 = {prio 3, vid 2})",
           axi_read(A_LWSRP_DOM_L), 0x00030002);
        // ---- inject the bridge Domain {class A, prio 3, VID 5} ---------
        uint8_t dm[60]; memset(dm, 0, sizeof dm);
        const uint8_t msrp_da2[6] = {0x01,0x80,0xC2,0x00,0x00,0x0E};
        memcpy(dm, msrp_da2, 6);
        dm[6]=0x02; dm[7]=0xAA; dm[8]=0xBB; dm[9]=0xCC; dm[10]=0xDD;
        dm[11]=0x02;
        dm[12]=0x22; dm[13]=0xEA;
        dm[14]=0;                       // ProtocolVersion
        dm[15]=4; dm[16]=4;             // Domain (type 4), AttributeLength 4
        dm[17]=0; dm[18]=9;             // AttributeListLength
        dm[19]=0; dm[20]=1;             // VectorHeader: NOV 1
        dm[21]=6;                       // SRclassID = A
        dm[22]=3;                       // SRclassPriority = 3
        dm[23]=0; dm[24]=5;             // SRclassVID = 5
        dm[25]=36;                      // ThreePacked JoinIn
        inject(dm, 60, 2000);
        uint32_t domw = 0;
        for (int g = 0; g < 64 && domw != 0x01030005u; g++) {
            for (int c = 0; c < 64; c++) step();
            domw = axi_read(A_LWSRP_DOM_L);
        }
        ck("adopt-dp: 0x788 reads {adopted, prio 3, VID 5}",
           domw, 0x01030005u);
        // the adopt event latches the boundary until the (now-operational)
        // pair is re-declared - the same PDU again heals it
        inject(dm, 60, 2000);
        ck("adopt-dp: re-declaration of the adopted pair heals domain_ok",
           (axi_read(0x694) >> 5) & 1, 1);
        // ---- the AAF C-TAG follows: TCI = {PCP 3, DEI 0, VID 5} --------
        auto tag_of_next_aaf = [&]() -> int {
            std::vector<uint8_t> fr;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 60000; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            fr.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        if (fr.size() >= 20 && fr[12] == 0x81 && fr[13] == 0x00
                            && fr[16] == 0x22 && fr[17] == 0xF0
                            && fr[18] == 0x02) {
                            int tci = (fr[14] << 8) | fr[15];
                            hi();
                            return tci;
                        }
                        fr.clear();
                    }
                }
                hi();
            }
            return -1;
        };
        ck("adopt-dp: AAF C-TAG TCI = {PCP 3, VID 5} (0x6005)",
           (uint32_t)tag_of_next_aaf(), 0x6005);
        // ---- the CRF talker's tag word follows (0x750[22:8]) -----------
        axi_write(A_LWSRP_CTRL, 0x37);       // talker + declare bypass
        axi_write(A_CRFT_CTRL_L, 0x3);       // CRF en + class A
        uint32_t crfw = 0;
        for (int g = 0; g < 200 && (((crfw >> 8) & 0xFFF) != 5); g++) {
            for (int c = 0; c < 256; c++) step();
            crfw = axi_read(A_CRFT_CTRL_L);
        }
        ck("adopt-dp: CRF tag word VID (0x750[19:8]) = the ADOPTED 5",
           (crfw >> 8) & 0xFFF, 5);
        ck("adopt-dp: CRF tag word PCP (0x750[22:20]) = 3",
           (crfw >> 20) & 0x7, 3);
        // ---- REVERT on enable-fall (the 4.2.7.2.1 reset list) ----------
        axi_write(A_CRFT_CTRL_L, 0x0);
        axi_write(A_LWSRP_CTRL, 0x14);       // enable OFF
        for (int c = 0; c < 2048; c++) step();
        axi_write(A_LWSRP_CTRL, 0x15);       // back to the flow posture
        for (int c = 0; c < 256; c++) step();
        ck("adopt-dp: enable-fall REVERTS to the defaults",
           axi_read(A_LWSRP_DOM_L), 0x00030002);
        ck("adopt-dp: AAF C-TAG back to {PCP 3, VID 2} (0x6002)",
           (uint32_t)tag_of_next_aaf(), 0x6002);
        axi_write(A_LINK_CTRL_L, link_was);  // the guard's posture restored
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
    // TCTX w0 CTRL[0] IS NO LONGER AN EGRESS LEVER (2026-07-30). The word
    // still carries chans/VID and still lands in the packetizer's context
    // RAM, but nothing consults bit 0: a Stream Output the shape elaborated
    // streams when SRP licenses it (Milan 5.3.7.3's licence has no software
    // term, and 5.4.2.20 forbids STOP_STREAMING on a Stream Output). So a
    // w0 commit with bit 0 clear must leave egress exactly as it was - the
    // check that used to assert it "disarms t1", inverted into the property
    // that replaced it.
    axi_write(A_STRM_SEL, 0x101);
    axi_write(A_SW_CTRL, (2u << 5) | 0u);            // TCTX w0: vid=2, bit0=0
    for (int c = 0; c < 16; c++) step();
    ck("w0 CTRL[0]=0 does NOT stop t1 (no per-stream software enable)",
       (tap_stream_en() >> 1) & 1, 1);
    ck("t0 unaffected by the t1 w0 commit", tap_stream_en() & 1, 1);
    // ...and with bypass on (this posture) every ELABORATED talker is
    // licensed, so t2/t3 stream too - the 5.3.7.3 zero-fill truth the old
    // "never armed" expectation could only hold because the missing enable
    // kept them dark. Their identity is asserted on the wire in the
    // reset-licence case at the top of this file.
    ck("t2/t3 armed too (shape-static, reset-armed)",
       (tap_stream_en() >> 2) & 3, 3);
    printf("-- N-sink ACMP: ctx2 window bind end-to-end (0x800 tbl master) --\n");
    //! ONE definition of ctx2's two stream identities, referenced by the bind,
    //! the probe answer, the 0x800 window checks and the t21 lwSRP-row section
    //! below. They must never be restated: the whole point of task #64 is that
    //! the SRP row ends up on the SECOND one, so two literals that happened to
    //! agree would pin nothing.
    const uint8_t CTX2_FC_SID[8]    = {0xAA,0xBB,0xCC,0xDD,0xEE,0xFF,0x00,0x07};
    const uint8_t CTX2_RESP_SID[8]  = {0x03,0x00,0x00,0x00,0x00,0x03,0x00,0x01};
    const uint8_t CTX2_RESP_DMAC[6] = {0x91,0xE0,0xF0,0x00,0x3C,0x11};
    // enable the ACMP listener (ADP enable gates it) with our entity id
    axi_write(A_ADP_EIDHI, 0x020000FF);
    axi_write(A_ADP_EIDLO, 0xFE000001);
    axi_write(A_ADP_CTRL, 0x00001F01);               // enable, valid_time 31
    {
        // CONNECT_RX (BIND_RX) for listener_unique_id 2: a window context
        // that honours an explicit fast-connect stream_id (Milan 5.5.1.2) as
        // its PROVISIONAL sid and then runs the full 5.5.3 probe ladder like
        // every other sink (task #64).
        uint8_t f[72]; memset(f, 0, sizeof f);
        const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
        memcpy(f, mc, 6);
        const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
        memcpy(f+6, csrc, 6);
        f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x06;   // CONNECT_RX_COMMAND
        f[16]=0x00; f[17]=44;                             // cdl
        // explicit fast-connect stream_id (nonzero -> adopted by policy)
        memcpy(f+18, CTX2_FC_SID, 8);
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
        //! NOT the old 400-cycle drain: a bind now puts TWO frames on the
        //! control lane (BIND_RX_RESPONSE at 5.5.3.5.3 step 3, then
        //! PROBE_TX_COMMAND at step 5) and both must win a grant through the
        //! five cascaded adp_tx_arbiters. The listener's single front-end FSM
        //! is deaf while a frame waits for its grant (the property
        //! adp_tx_arbiter.sv:143 documents, bounded by its own 2^20-cycle
        //! TX-grant watchdog), so a command injected 400 cycles behind a bind
        //! lands inside that window and is dropped. Measured on this trunk:
        //! the walker stays busy ~1400 cycles per bind.
        inject(f, 70, 2000);
    }
    axi_write(A_STRM_SEL, 0x002);                    // dir=0 idx=2
    // the CSR polls the tbl port continuously; a couple of reads give the
    // grant time to land, then the snapshot is fresh
    (void)axi_read(A_SW_SID_LO);
    ck("ctx2 SID_LO = explicit bind sid", axi_read(A_SW_SID_LO), 0xEEFF0007);
    ck("ctx2 SID_HI", axi_read(A_SW_SID_HI), 0xAABBCCDD);
    //! Milan 5.5.2.6 step 1: the SRP parameters are CLEARED at bind and
    //! re-learned from the PROBE_TX_RESPONSE (5.5.3.5.18 step 4). The
    //! command's stream_dest_mac is not a source of truth for them - it never
    //! was for sink 0, and since task #64 it is not for a window sink either.
    ck("ctx2 DMAC cleared at bind (5.5.2.6 step 1)",
       axi_read(A_SW_DMAC_LO) | axi_read(A_SW_DMAC_HI), 0);
    snap_and_wait();
    uint32_t st2 = axi_read(A_SW_STATE);
    ck("ctx2 STATE lsm = PRB_W_RESP (3)", st2 & 0x7, 3);
    ck("ctx2 STATE probing = ACTIVE (2)", (st2 >> 3) & 0x3, 2);
    ck("ctx2 STATE acmp_status = 0", (st2 >> 5) & 0x1F, 0);
    // ...and the talker's answer is what the row is finally provisioned from:
    // a stream_id and dest_mac the BIND_RX_COMMAND never carried.
    {
        uint8_t f[72]; memset(f, 0, sizeof f);
        const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
        memcpy(f, mc, 6);
        const uint8_t tsrc[6] = {0x03,0x00,0x00,0x00,0x00,0x03};
        memcpy(f+6, tsrc, 6);
        f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x01;   // CONNECT_TX_RESPONSE
        f[16]=0x00; f[17]=44;                             // SUCCESS | cdl
        memcpy(f+18, CTX2_RESP_SID, 8);                   // the REAL stream_id
        for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;  // controller
        const uint8_t tk[8] = {0x03,0x00,0x00,0x00,0x00,0x03,0x00,0x01};
        memcpy(f+34, tk, 8);
        const uint8_t us[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
        memcpy(f+42, us, 8);                              // listener = us
        f[50]=0x00; f[51]=0x01;                           // talker_unique_id
        f[52]=0x00; f[53]=0x02;                           // listener_unique_id 2
        memcpy(f+54, CTX2_RESP_DMAC, 6);                  // the REAL dest_mac
        f[62]=(uint8_t)(probe_seq_by_luid[2] >> 8);       // echo the probe's
        f[63]=(uint8_t)(probe_seq_by_luid[2] & 0xFF);     //   sequence_id
        f[66]=0x00; f[67]=0x02;                           // stream_vlan_id 2
        inject(f, 70, 2000);
    }
    axi_write(A_STRM_SEL, 0x002);
    (void)axi_read(A_SW_SID_LO);
    ck("ctx2 SID_LO now the PROBE RESPONSE's (5.5.3.5.18 s4)",
       axi_read(A_SW_SID_LO), 0x00030001);
    ck("ctx2 SID_HI now the PROBE RESPONSE's", axi_read(A_SW_SID_HI),
       0x03000000);
    ck("ctx2 DMAC_LO learned from the response", axi_read(A_SW_DMAC_LO),
       0xF0003C11);
    ck("ctx2 DMAC_HI learned from the response", axi_read(A_SW_DMAC_HI),
       0x000091E0);
    snap_and_wait();
    st2 = axi_read(A_SW_STATE);
    ck("ctx2 STATE lsm = SETTLED_NO_RSV (6)", st2 & 0x7, 6);
    ck("ctx2 STATE probing = COMPLETED (3)", (st2 >> 3) & 0x3, 3);
    axi_write(A_STRM_SEL, 0x003);                    // unbound window ctx
    (void)axi_read(A_SW_SID_LO);
    ck("ctx3 SID reads 0 (unbound)", axi_read(A_SW_SID_LO) |
                                     axi_read(A_SW_SID_HI), 0);
    axi_write(A_STRM_SEL, 0x000);                    // media ctx untouched
    (void)axi_read(A_SW_SID_LO);
    ck("ctx0 SID reads 0 (bind left ctx0 alone)", axi_read(A_SW_SID_LO) |
                                                  axi_read(A_SW_SID_HI), 0);

    // ================================================================== //
    //  gh #58 D1 END-TO-END: the CONNECT_RX above left sink 2 BOUND       //
    //  (SETTLED_NO_RSV), and that LEVEL - acmpl_bound_v_w through          //
    //  KL_aecp_top's lstn_bound_v_i - must refuse SET_STREAM_FORMAT on    //
    //  EXACTLY that index with STREAM_IS_RUNNING, value-independent        //
    //  (Milan 5.4.2.6 / 5.3.8.2). This is the plumbing proof the aecp     //
    //  harness pins cannot give: the vector here comes from the REAL      //
    //  listener SM, not a TB port poke. The unbind half lives in the t21  //
    //  section below, right after ctx2's DISCONNECT_RX.                   //
    // ================================================================== //
    printf("-- gh #58 D1 e2e: BOUND sink 2 refuses SET_STREAM_FORMAT --\n");
    {
        std::vector<uint8_t> q2 = {0x00,0x05,0x00,0x02};      // STREAM_INPUT 2
        auto g2 = aecp_xact(9, 0x5810, q2);                   // GET_STREAM_FORMAT
        ck("D1-e2e: GET_FMT(in2) SUCCESS", aecp_status(g2), 0);
        ck("D1-e2e: response long enough", g2.size() >= 50 ? 1 : 0, 1);
        // SET the very same value: the refusal keys on the BIND alone
        std::vector<uint8_t> s2(q2);
        for (int i = 0; i < 8 && g2.size() >= 50; i++) s2.push_back(g2[42+i]);
        auto r2 = aecp_xact(8, 0x5811, s2);                   // SET_STREAM_FORMAT
        ck("D1-e2e: SET(in2) while ctx2 BOUND -> STREAM_IS_RUNNING",
           aecp_status(r2), 12);
        // the NEIGHBOUR sink was never ACMP-bound: the same-value SET
        // lands there - the gate is PER INDEX through the live vector
        std::vector<uint8_t> q1 = {0x00,0x05,0x00,0x01};
        auto g1 = aecp_xact(9, 0x5812, q1);
        ck("D1-e2e: GET_FMT(in1) SUCCESS", aecp_status(g1), 0);
        std::vector<uint8_t> s1(q1);
        for (int i = 0; i < 8 && g1.size() >= 50; i++) s1.push_back(g1[42+i]);
        auto r1 = aecp_xact(8, 0x5813, s1);
        ck("D1-e2e: SET(in1) unbound neighbour SUCCEEDS", aecp_status(r1), 0);
    }

    printf("-- E3 journal ingest end-to-end: a saved bind survives 'reboot' "
           "--\n");
    // Milan v1.2 5.3.8.2: "The current bound state shall be saved in a
    // non-volatile memory and restored after a power cycle." This is the
    // restore half through the REAL CSR plane: the image is pushed VERBATIM
    // over the 0x7B8 group exactly as the boot script lifts it out of the
    // flash slot, the journal verifies it whole (magic/ver/shape/entity/
    // CRC - the persist suite owns the rejection taxonomy) and replays a
    // Milan 5.5.3.5.2 entry record into sink 1's ACMP context. SRP params
    // are NOT restored (5.5.2.6 step 1 re-probes them - [J4] proves the
    // clearing), so the assertions here are state + the E2 read-back.
    {
        auto crc32b = [](const std::vector<uint8_t>& b) {
            uint32_t c = 0xFFFFFFFFu;
            for (uint8_t x : b) { c ^= x;
                for (int k = 0; k < 8; k++)
                    c = (c & 1) ? ((c >> 1) ^ 0xEDB88320u) : (c >> 1); }
            return c ^ 0xFFFFFFFFu;
        };
        const uint64_t ENT = 0x020000FFFE000001ULL;  // the A_ADP eid above
        const uint64_t TK  = 0x0011BBCCDDEE0042ULL;  // saved talker
        const uint64_t CT  = 0x00AA5511220000FFULL;  // saved controller
        std::vector<uint32_t> w = {
            0x314A4C4Bu, 0x00010000u, /*SEQ*/ 1u, (6u << 8) | 1u,
            (uint32_t)ENT, (uint32_t)(ENT >> 32),
            (uint32_t)TK, (uint32_t)(TK >> 32),
            /*{vlan 2, tuid 7}*/ (2u << 16) | 7u,
            (uint32_t)CT, (uint32_t)(CT >> 32),
            /*VALID + flags 0 + sink idx 0 - the ONE probe-SM sink this
             shape elaborates (PROBE_SM_EN_P default = bit 0; sinks 1..N-1
             are record-only, a per-sink SM gap the gaps doc owns)*/
            (1u << 30) | 0u };
        std::vector<uint8_t> b;
        for (uint32_t x : w) {
            b.push_back(x & 0xFF); b.push_back((x >> 8) & 0xFF);
            b.push_back((x >> 16) & 0xFF); b.push_back((x >> 24) & 0xFF);
        }
        w.push_back(crc32b(b));
        axi_write(0x7B8, 1);                       // start
        for (uint32_t x : w) axi_write(0x7BC, x);  // the image, verbatim
        axi_write(0x7B8, 2);                       // end
        for (int c = 0; c < 256; c++) step();
        ck("E3: verdict ACCEPT", (axi_read(0x7C0) >> 4) & 0xF, 1);
        ck("E3: SEQ watermark = the accepted image's", axi_read(0x7C4), 1);
        axi_write(A_STRM_SEL, 0x000);
        (void)axi_read(A_SW_SID_LO);
        snap_and_wait();
        uint32_t st = axi_read(A_SW_STATE);
        ck("E3: sink 0 = PRB_W_AVAIL (5.5.3.5.2 step 3)", st & 0x7, 1);
        ck("E3: E2 controller_entity_id lo", axi_read(0x860), (uint32_t)CT);
        ck("E3: E2 controller_entity_id hi", axi_read(0x864),
           (uint32_t)(CT >> 32));
        ck("E3: E2 tuid = the saved source index", axi_read(0x868) & 0xFFFF, 7);
        // exit clean: UNBIND from the SAVED controller (5.5.3.5.8 -
        // RCV_UNBIND_RX_CMD in a probing state -> UNBOUND, binding
        // parameters cleared per 5.3.8.3), so the flow's later sink-0
        // cases meet the state they were written against
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x08;  // DISCONNECT_RX
            f[16]=0x00; f[17]=44;
            const uint8_t ct[8] = {0x00,0xAA,0x55,0x11,0x22,0x00,0x00,0xFF};
            memcpy(f+26, ct, 8);                  // the SAVED controller
            const uint8_t tk[8] = {0x00,0x11,0xBB,0xCC,0xDD,0xEE,0x00,0x42};
            memcpy(f+34, tk, 8);
            const uint8_t us[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, us, 8);
            f[50]=0x00; f[51]=0x07;               // saved talker_unique_id
            f[52]=0x00; f[53]=0x00;               // listener_unique_id 0
            f[62]=0x77; f[63]=0x31;
            inject(f, 70, 400);
        }
        axi_write(A_STRM_SEL, 0x000);
        (void)axi_read(A_SW_SID_LO);
        snap_and_wait();
        ck("E3: unbind returns sink 0 to UNBOUND (5.5.3.5.8)",
           axi_read(A_SW_STATE) & 0x7, 0);
    }



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
        ck("talker idx1 TalkerAdvertise MaxFrameSize = 24*8 + 24 + 1 (Table 4.4)",
           (unsigned)mf1, 24*8 + 24 + 1);
        ck("talker idx2 TalkerAdvertise MaxFrameSize = 24*2 + 24 + 1 (Table 4.4)",
           (unsigned)mf2, 24*2 + 24 + 1);
        // NEGATIVE LEG: the two rows do NOT share one value, and neither
        // fell back to the shared LWSRP_TSPEC reset (0x00E0 = 224)
        ck("per-row TSpec: the two rows differ", mf1 == mf2 ? 1 : 0, 0);
        ck("per-row TSpec: neither is the shared LWSRP_TSPEC 224",
           (mf1 == 224 || mf2 == 224) ? 1 : 0, 0);

        axi_write(A_LWSRP_CTRL, 0x0);
    }

    // ==================================================================
    //  EVERY AAF TALKER ROW HAS A PROVISIONER  (2026-07-30)
    //
    //  The block above provisions rows THROUGH THE WINDOW, which is how
    //  every previous test reached them - and it hid the defect, because
    //  nothing on the board drives that window. Measured on silicon:
    //  A_STRMW_SRP read 0x0000_037E at talker idx 0 (a live alias of the
    //  legacy flat row, which is why idx-0-only tests looked healthy) and
    //  0x0000_0000 at idx 1/2/3 - the row's OWN valid bit clear. On the
    //  wire, with a licensed stream running, MSRP declared a Talker
    //  Advertise for exactly {02:00:00:00:00:02, uid 0} and {..., uid 4 =
    //  the CRF output} and NOTHING for uid 1/2/3: the two stream_ids on
    //  the wire were the two rows that had a provisioner. Milan v1.2
    //  5.3.7.3 conditions streaming on declaring a Talker Advertise AND
    //  receiving a Listener Ready, so no talker but 0 could be licensed.
    //
    //  So this case provisions NOTHING through the SRP staging path: it
    //  stages a ZERO stream_id for every row (the fabric owns a row no
    //  software has named - the CRFT_SID precedent per row) and asks only
    //  that the talker be ENABLED. Every index, because idx 0 is the
    //  alias/legacy path and the least representative one there is.
    //
    //  WHAT ACTUALLY BITES, measured by reverting the datapath hunk in a
    //  scratch copy of this tree (2026-07-30: 248 checks / 30 failures at
    //  4x4, 248/0 with the fix): NOT the valid bit. The window's own CTRL
    //  commit writes the row valid=1 as a side effect, so pre-fix all three
    //  rows read VALID and DECLARED - carrying the NULL stream_id, three
    //  rows declaring streamID 0 at once. The identity is the discriminator:
    //  the derived sid words read 0 and NO TalkerAdvertise for uid 1/2/3 is
    //  on the wire, which is exactly the ProfiShark symptom. Never read
    //  "valid == 1" here as proof that a row is usable.
    //
    //  It also runs the two STARVATION legs in their worst shape:
    //  A_STRM_SEL is parked on a talker row for the whole burst (that
    //  level-high poll is exactly what pinned the first fabric requester
    //  off forever), the CRF slot requests at the same time as all N-1 AAF
    //  slots, and a CSR WRITE is committed while every fabric slot has a
    //  request pending.
    // ==================================================================
    printf("-- lwSRP: EVERY AAF talker row declares on its own enable --\n");
    {
        enum { A_MAC_LO = 0x108, A_MAC_HI = 0x10C,
               A_AAF_DMLO = 0x658, A_AAF_DMHI = 0x65C,
               A_CRFT_CTRL = 0x750, A_LWSRP_STATUS = 0x694,
               A_SW_SRP = 0x85C };
        const uint32_t mac_lo0 = axi_read(A_MAC_LO);
        const uint32_t mac_hi0 = axi_read(A_MAC_HI);
        // THE BOARD'S MAC, so the derived stream_ids are the ones the
        // ProfiShark capture recorded: 02:00:00:00:00:02. Wire byte order is
        // {MAC_LO[7:0], [15:8], [23:16], [31:24], MAC_HI[7:0], [15:8]}, so
        // stream_id = {02,00,00,00,00,02, uid} -> HI 0x02000000,
        // LO 0x0002_0000 | uid.
        axi_write(A_MAC_LO, 0x00000002);
        axi_write(A_MAC_HI, 0x00000200);
        const uint32_t SID_HI_C = 0x02000000;
        const uint64_t dbase = ((uint64_t)(axi_read(A_AAF_DMHI) & 0xFFFF) << 32)
                             | (uint64_t)axi_read(A_AAF_DMLO);
        auto chans_of = [](int t) { return 2u * (1u + (unsigned)(t % 4)); };
        auto sid_lo_of = [&](int t) { return (uint32_t)(0x00020000u + t); };

        // enable + talker declare + the [5] DECLARE bypass (this case is
        // the declared-at-boot provisioner proof; the 4.3.3.1 gate has its
        // own case), queue 5
        axi_write(A_LWSRP_CTRL, 0x37);
        // the CRF slot wants its row at the same time as every AAF slot, so
        // the rotating arbiter is exercised with SRP_TALKERS_C-1 requesters
        axi_write(A_CRFT_CTRL, 0x3);     // CRF talker en + class A asked
        for (int c = 0; c < 256; c++) step();

        // ---- arm every talker t>0 in ONE burst, staging NO stream_id ----
        for (int t = 1; t < NSTREAMS_TB; t++) {
            const uint64_t dm = dbase + (uint64_t)t;
            axi_write(A_STRM_SEL, 0x100 + t);
            axi_write(A_SW_SID_LO, 0);     // stage NO sid -> fabric-owned row
            axi_write(A_SW_SID_HI, 0);
            axi_write(A_SW_DMAC_LO, (uint32_t)(dm & 0xFFFFFFFFu));   // TCTX w1
            axi_write(A_SW_DMAC_HI, ((uint32_t)t << 16) |
                                    (uint32_t)((dm >> 32) & 0xFFFFu)); // w2
            axi_write(A_SW_CTRL, (2u << 5) | (chans_of(t) << 1) | 1u);
        }
        // A_STRM_SEL is left on the LAST talker row from here on: the window
        // master polls it level-high for the rest of the case.

        // ---- what actually left the port ------------------------------
        int      ta_hit[NSTREAMS_TB + 1], ta_mf[NSTREAMS_TB + 1];
        int      ta_pr[NSTREAMS_TB + 1], ta_vid[NSTREAMS_TB + 1];
        uint64_t ta_dm[NSTREAMS_TB + 1];
        uint32_t ta_shi[NSTREAMS_TB + 1];
        for (int t = 0; t <= NSTREAMS_TB; t++) {
            ta_hit[t] = 0; ta_mf[t] = -1; ta_pr[t] = -1; ta_vid[t] = -1;
            ta_dm[t] = 0;  ta_shi[t] = 0;
        }
        {
            std::vector<uint8_t> cur;
            dut->m_axis_mac_tx_tready = 1;
            int want = 0;
            for (int c = 0; c < 600000; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        // MSRP MRPDU, first message TalkerAdvertise: eth 14 +
                        // ver 1 + msg hdr 4, then 28-octet single-value
                        // vectors (802.1Q 35.2.2.4 FirstValue is 25 octets
                        // behind a 2-octet VectorHeader)
                        if (cur.size() >= 47 && cur[12] == 0x22 &&
                            cur[13] == 0xEA && cur[15] == 1) {
                            size_t listlen = ((size_t)cur[17] << 8) | cur[18];
                            for (size_t o = 0;
                                 o + 28 <= listlen - 2 && 19 + o + 28 <= cur.size();
                                 o += 28) {
                                const uint8_t* v = &cur[19 + o];
                                uint32_t slo = ((uint32_t)v[6] << 24) |
                                               ((uint32_t)v[7] << 16) |
                                               ((uint32_t)v[8] << 8) | v[9];
                                int uid = -1;
                                for (int t = 1; t <= NSTREAMS_TB; t++)
                                    if (slo == sid_lo_of(t)) uid = t;
                                if (uid < 0) continue;
                                ta_shi[uid] = ((uint32_t)v[2] << 24) |
                                              ((uint32_t)v[3] << 16) |
                                              ((uint32_t)v[4] << 8) | v[5];
                                ta_dm[uid] = 0;
                                for (int i = 0; i < 6; i++)
                                    ta_dm[uid] = (ta_dm[uid] << 8) | v[10+i];
                                ta_vid[uid] = (v[16] << 8) | v[17];
                                ta_mf[uid]  = (v[18] << 8) | v[19];
                                ta_pr[uid]  = v[22];
                                ta_hit[uid] = 1;
                            }
                        }
                        cur.clear();
                    }
                }
                hi();
                want = 0;
                for (int t = 1; t < NSTREAMS_TB; t++) want += ta_hit[t];
                if (want == NSTREAMS_TB - 1) break;
            }
        }

        // ---- the per-index verdict, EVERY index -----------------------
        // Reading a non-zero SRP/SID word is itself the proof that the
        // window's POLL was served: milan_csr gates both behind srp_fresh_r,
        // which only a granted poll sets (and i_srp_ctx_stolen clears).
        for (int t = 1; t < NSTREAMS_TB; t++) {
            char nm[96];
            axi_write(A_STRM_SEL, 0x100 + t);
            uint32_t sl = axi_read(A_SW_SID_LO);
            for (int g = 0; g < 64 && sl != sid_lo_of(t); g++) {
                for (int c = 0; c < 512; c++) step();
                sl = axi_read(A_SW_SID_LO);
            }
            const uint32_t sh  = axi_read(A_SW_SID_HI);
            const uint32_t srp = axi_read(A_SW_SRP);
            snprintf(nm, sizeof nm, "talker idx%d: SRP row VALID, nothing staged", t);
            ck(nm, (srp >> 15) & 1, 1);
            snprintf(nm, sizeof nm, "talker idx%d: row dir = talker", t);
            ck(nm, (srp >> 14) & 1, 0);
            snprintf(nm, sizeof nm, "talker idx%d: row DECLARED (on the wire)", t);
            ck(nm, (srp >> 13) & 1, 1);
            snprintf(nm, sizeof nm, "talker idx%d: BACKED, not the 0xDEAD alias", t);
            ck(nm, (srp & 0xFFFF) == 0xDEAD ? 1 : 0, 0);
            snprintf(nm, sizeof nm, "talker idx%d: derived sid LO {MAC,uid}", t);
            ck(nm, sl, sid_lo_of(t));
            snprintf(nm, sizeof nm, "talker idx%d: derived sid HI = station MAC", t);
            ck(nm, sh, SID_HI_C);
            snprintf(nm, sizeof nm, "MSRP idx%d: a TalkerAdvertise IS on the wire", t);
            ck(nm, ta_hit[t], 1);
            snprintf(nm, sizeof nm, "MSRP idx%d: sid HI = the station MAC", t);
            ck(nm, ta_shi[t], SID_HI_C);
            snprintf(nm, sizeof nm, "MSRP idx%d: DMAC = MAAP block base+idx", t);
            ck(nm, ta_dm[t], dbase + (uint64_t)t);
            snprintf(nm, sizeof nm,
                     "MSRP idx%d: MaxFrameSize = 24*C + 24 + 1 (Table 4.4)", t);
            ck(nm, (unsigned)ta_mf[t], 24u * chans_of(t) + 24u + 1u);
            snprintf(nm, sizeof nm, "MSRP idx%d: PriorityAndRank 0x70", t);
            ck(nm, (unsigned)ta_pr[t], 0x70);
            snprintf(nm, sizeof nm, "MSRP idx%d: VID = the SR VID 2", t);
            ck(nm, (unsigned)ta_vid[t], 2);
        }
        // NEGATIVE LEGS: the rows are not one aliased row, and no row fell
        // back to the shared LWSRP_TSPEC MaxFrameSize (0x00E0 = 224)
        {
            int same = 1, shared = 0;
            for (int t = 2; t < NSTREAMS_TB; t++)
                if (ta_mf[t] != ta_mf[1]) same = 0;
            for (int t = 1; t < NSTREAMS_TB; t++)
                if (ta_mf[t] == 224) shared = 1;
            ck("per-row TSpec: the derived rows do NOT share one MaxFrameSize",
               same, 0);
            ck("per-row TSpec: none fell back to the shared LWSRP_TSPEC 224",
               shared, 0);
        }
        // the row map did not run off the end of the table (this is a
        // PROVISIONING fix, not a re-fix of the 0x0010 SIZING bug)
        ck("LWSRP_STATUS[11] ctx shortfall STILL clear",
           (axi_read(A_LWSRP_STATUS) >> 11) & 1, 0);
        // ...and the CRF slot was served in the same storm: no fabric slot
        // starves another (rotating grant, served slot -> lowest priority)
        ck("no fabric starvation: the CRF row is declared too (0x750[4])",
           (axi_read(A_CRFT_CTRL) >> 4) & 1, 1);

        // ---- SHAPE-STATIC: the per-context enable does NOT withdraw ---
        // (2026-07-30, USER "shape is STATIC, not a runtime poke") A declared
        // Stream Output advertises for the life of the entity; toggling the
        // per-context runtime enable A_STRMW_CTRL[0] must NOT pull the
        // TalkerAdvertise. The 0x001E fix gated the declaration on that bit,
        // so S50milan - which never writes the 0x800 window - declared
        // nothing for t>0 and only stream 0 could reserve (silicon +
        // ProfiShark). BITES the pre-shape RTL, where disabling the enable
        // withdrew the row.
        for (int t = 1; t < NSTREAMS_TB; t++) {
            axi_write(A_STRM_SEL, 0x100 + t);
            axi_write(A_SW_CTRL, (2u << 5) | (chans_of(t) << 1) | 0u);  // enable OFF
        }
        for (int c = 0; c < 4096; c++) step();
        for (int t = 1; t < NSTREAMS_TB; t++) {
            char nm[96];
            axi_write(A_STRM_SEL, 0x100 + t);
            uint32_t srp = axi_read(A_SW_SRP);
            snprintf(nm, sizeof nm,
                     "talker idx%d: per-context disable does NOT withdraw", t);
            ck(nm, (srp >> 15) & 1, 1);
        }

        // ---- WITHDRAWAL on ENGINE-OFF: the trigger that DOES pull it ---
        // Clearing cfg_lwsrp_talker_en (A_LWSRP_CTRL[1]) drops the want for
        // every AAF talker AND the CRF at once - the N-way simultaneous
        // withdrawal - and a LISTENER CSR WRITE committed in the same breath
        // must not be dropped under that burst.
        axi_write(A_LWSRP_CTRL, 0x35);         // talker declare OFF (bypass kept)
        axi_write(A_STRM_SEL, 0x002);          // listener idx 2 -> ctx row 2
        axi_write(A_SW_SID_LO, 0x00C0FFEE);
        axi_write(A_SW_SID_HI, 0x0000C0DE);
        axi_write(A_SW_CTRL, (RT_DMA << 1) | 1u);
        for (int c = 0; c < 4096; c++) step();
        {
            uint32_t l = axi_read(A_SW_SRP);
            for (int g = 0; g < 64 && ((l >> 15) & 1) == 0; g++) {
                for (int c = 0; c < 256; c++) step();
                l = axi_read(A_SW_SRP);
            }
            ck("no window starvation: the CSR WRITE landed under the withdrawal",
               (l >> 15) & 1, 1);
            ck("no window starvation: ...and it is the LISTENER direction",
               (l >> 14) & 1, 1);
        }
        for (int t = 1; t < NSTREAMS_TB; t++) {
            char nm[96];
            axi_write(A_STRM_SEL, 0x100 + t);
            uint32_t srp = axi_read(A_SW_SRP);
            for (int g = 0; g < 64 && ((srp >> 15) & 1); g++) {
                for (int c = 0; c < 512; c++) step();
                srp = axi_read(A_SW_SRP);
            }
            snprintf(nm, sizeof nm, "talker idx%d: engine-off WITHDREW the row", t);
            ck(nm, (srp >> 15) & 1, 0);
        }
        // ---- and it re-arms (a withdrawal is not a one-way latch) -----
        axi_write(A_LWSRP_CTRL, 0x37);         // talker declare back ON (bypass kept)
        for (int c = 0; c < 8192; c++) step();
        for (int t = 1; t < NSTREAMS_TB; t++) {
            char nm[96];
            axi_write(A_STRM_SEL, 0x100 + t);
            uint32_t srp = axi_read(A_SW_SRP);
            for (int g = 0; g < 64 && ((srp >> 15) & 1) == 0; g++) {
                for (int c = 0; c < 512; c++) step();
                srp = axi_read(A_SW_SRP);
            }
            snprintf(nm, sizeof nm, "talker idx%d: engine re-enable re-declares", t);
            ck(nm, (srp >> 15) & 1, 1);
        }

        // ---- SOFTWARE STILL WINS IF IT NAMES A STREAM_ID -------------
        // The CRFT_SID precedent, per row: a window commit carrying a
        // NON-ZERO staged sid takes the row outright and the fabric stands
        // down WITHOUT withdrawing it.
        {
            const uint32_t SWLO = 0x0000BEE1, SWHI = 0x0BADF00D;
            axi_write(A_STRM_SEL, 0x101);
            axi_write(A_SW_SID_LO, SWLO);
            axi_write(A_SW_SID_HI, SWHI);
            axi_write(A_SW_CTRL, (2u << 5) | (chans_of(1) << 1) | 1u);
            uint32_t sl = axi_read(A_SW_SID_LO);
            for (int g = 0; g < 64 && sl != SWLO; g++) {
                for (int c = 0; c < 512; c++) step();
                sl = axi_read(A_SW_SID_LO);
            }
            ck("software staging still WINS: idx1 keeps the named sid", sl, SWLO);
            ck("software staging still WINS: ...both halves", axi_read(A_SW_SID_HI),
               SWHI);
            ck("software staging still WINS: the row stays VALID",
               (axi_read(A_SW_SRP) >> 15) & 1, 1);
            // and it did not disturb its neighbour, which the fabric owns
            axi_write(A_STRM_SEL, 0x102);
            uint32_t s2 = axi_read(A_SW_SID_LO);
            for (int g = 0; g < 64 && s2 != sid_lo_of(2); g++) {
                for (int c = 0; c < 512; c++) step();
                s2 = axi_read(A_SW_SID_LO);
            }
            ck("software staging on idx1 leaves idx2 fabric-derived", s2,
               sid_lo_of(2));
            // RELEASE-TO-FABRIC: commit a ZERO sid and the fabric retakes it
            axi_write(A_STRM_SEL, 0x101);
            axi_write(A_SW_SID_LO, 0);
            axi_write(A_SW_SID_HI, 0);
            axi_write(A_SW_CTRL, (2u << 5) | (chans_of(1) << 1) | 1u);
            sl = axi_read(A_SW_SID_LO);
            for (int g = 0; g < 64 && sl != sid_lo_of(1); g++) {
                for (int c = 0; c < 512; c++) step();
                sl = axi_read(A_SW_SID_LO);
            }
            ck("release-to-fabric: a zero sid hands idx1 back", sl,
               sid_lo_of(1));
        }

        // leave the shape as the CRF case below expects it
        for (int t = 1; t < NSTREAMS_TB; t++) {
            axi_write(A_STRM_SEL, 0x100 + t);
            axi_write(A_SW_CTRL, (2u << 5) | (2u << 1) | 0u);
        }
        axi_write(A_STRM_SEL, 0x000);
        axi_write(A_CRFT_CTRL, 0x0);
        axi_write(A_LWSRP_CTRL, 0x0);
        axi_write(A_MAC_LO, mac_lo0);
        axi_write(A_MAC_HI, mac_hi0);
        for (int c = 0; c < 1024; c++) step();
    }

    // ==================================================================
    //  TASK-21 FABRIC HALF: a CONNECT_RX provisions the lwSRP LISTENER row
    //
    //  The 07-29 peer-device silicon finding: binding one of our STREAM_INPUTs
    //  staged the ACMP record but NOTHING in the fabric wrote the lwSRP
    //  LISTENER attribute row - ctx_dir_i was hardwired 0 on the fabric
    //  grant path, so the only listener-direction writer was the 0x800
    //  window (manual CSR staging). Milan v1.2 5.3.7.3 makes the remote
    //  talker's streaming licence conditional on receiving a Listener
    //  Ready/ReadyFailed, so an unstaged bind never pulled its stream.
    //
    //  The input here is the CONNECT_RX for listener_unique_id 2 injected
    //  in the N-sink ACMP case above (explicit sid AA:BB:CC:DD:EE:FF:00:07,
    //  still bound). This case only releases the window's software claim
    //  on the row (earlier flow staged sids through it, and software that
    //  NAMES a sid owns a row - the per-row CRFT_SID rule) and turns the
    //  engine on. Everything that follows must come from the BIND alone.
    // ==================================================================
    printf("-- t21: CONNECT_RX -> lwSRP LISTENER row (fabric, no staging) --\n");
    {
        enum { A_LWSRP_STATUS = 0x694, A_SW_SRP = 0x85C };
        //! TASK #64: the lwSRP LISTENER row for sink 2 is provisioned from
        //! the sink's SETTLED stream_id, and Milan 5.5.3.5.18 step 4 makes
        //! that the PROBE_TX_RESPONSE's - NOT the fast-connect sid the
        //! BIND_RX_COMMAND carried. Naming CTX2_RESP_SID here is the fabric
        //! half of the bite: before task #64 this row went out under the
        //! controller's guess.
        const uint8_t* SID2 = CTX2_RESP_SID;

        //! scan TX frames for an MSRP Listener vector carrying `sid`;
        //! returns the three-packed event + four-packed declaration octets.
        //! want_evt / want_par (-1 = any) filter the match: around an
        //! ownership hand-off several frames for the same sid can be in
        //! flight (refresh, NEW, LV) and the capture must name the one it
        //! is asserting, not whichever drains first.
        auto find_lstn = [&](const uint8_t sid[8], int want_evt, int want_par,
                             int cyc, int* evt_out, int* par_out) -> bool {
            std::vector<uint8_t> cur;
            bool found = false;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < cyc && !found; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        //! keep the probe-seq latch fresh: the l0 bind's
                        //! PROBE_TX launches DURING this scan (its inject
                        //! drain is deliberately short), and the answer
                        //! must echo its sequence_id (5.5.3.5.18 step 1)
                        if (cur.size() >= 70 && cur[12] == 0x22 &&
                            cur[13] == 0xF0 && cur[14] == 0xFC &&
                            (cur[15] & 0xF) == 0x0) {
                            int pl = ((cur[52] << 8) | cur[53]) & 0xF;
                            probe_seq_by_luid[pl] =
                                (uint16_t)((cur[62] << 8) | cur[63]);
                        }
                        if (cur.size() >= 21 && cur[12] == 0x22 && cur[13] == 0xEA) {
                            size_t p = 15;               // after ProtocolVersion
                            while (p + 4 <= cur.size() && cur[p] != 0) {
                                uint8_t at  = cur[p];
                                size_t  ll  = ((size_t)cur[p+2] << 8) | cur[p+3];
                                size_t  vp  = p + 4;
                                if (at == 3 && ll >= 14 && vp + ll <= cur.size() + 2) {
                                    for (size_t o = 0; o + 12 <= ll - 2 &&
                                                       vp + o + 12 <= cur.size(); o += 12) {
                                        const uint8_t* v = &cur[vp + o];
                                        if (!memcmp(v + 2, sid, 8) &&
                                            (want_evt < 0 || v[10] == want_evt) &&
                                            (want_par < 0 || v[11] == want_par)) {
                                            if (evt_out) *evt_out = v[10];
                                            if (par_out) *par_out = v[11];
                                            found = true;
                                        }
                                    }
                                }
                                p = vp + ll;
                            }
                        }
                        cur.clear();
                    }
                }
                hi();
            }
            return found;
        };

        // release the window's claim on listener row 2: stage the ZERO sid
        // FOR this index (staging is spendable-by-selection), commit en=0
        axi_write(A_STRM_SEL, 0x002);              // listener idx 2
        axi_write(A_SW_SID_LO, 0);
        axi_write(A_SW_SID_HI, 0);
        axi_write(A_SW_CTRL, 0x0);
        axi_write(A_LWSRP_CTRL, 0x15);             // engine ON, queue 5,
                                                   // NO talker declare
        // THE BITE: the fabric must now declare the Listener attribute for
        // the bound sid on its own - capture the NEW declaration going out
        int evt = -1, par = -1;
        bool got = find_lstn(SID2, -1, -1, 400000, &evt, &par);
        ck("t21 bind: Listener declaration for the BOUND sid on the wire",
           got ? 1 : 0, 1);
        ck("t21 bind: first declaration event = NEW", evt, 0);
        ck("t21 bind: four-pack ASKING-FAILED before any TA", par, 0x40);

        // ...and the row reads back VALID + LISTENER through the window
        // (onwire follows the frame's tx_done, one poll behind the capture)
        uint32_t srp = axi_read(A_SW_SRP);
        for (int g = 0; g < 64 && ((srp >> 13) & 0x7) != 0x7; g++) {
            for (int c = 0; c < 256; c++) step();
            srp = axi_read(A_SW_SRP);
        }
        ck("t21 bind: SRP row VALID from the CONNECT_RX alone",
           (srp >> 15) & 1, 1);
        ck("t21 bind: SRP row direction = LISTENER", (srp >> 14) & 1, 1);
        ck("t21 bind: row on wire (declared)", (srp >> 13) & 1, 1);
        ck("t21 bind: row backed (not the 0xDEAD sentinel)",
           (srp & 0xFFFF) == 0xDEAD ? 1 : 0, 0);

        // a TalkerAdvertise for the bound sid: Ready must follow it
        // (KL_lwsrp_ctx registrar; re-declared promptly on the edge).
        // B1d: the row's EXPECTED pair is the SETTLED record's — the
        // probe response's {..:3C:11, vlan 2} — so the TA must carry
        // exactly that (Table 5.29 three-parameter match). The old
        // stimulus carried dmac ..:2A:99, which the walker now lawfully
        // ignores; the mismatch leg below pins that verdict first.
        {
            uint8_t ta[64]; memset(ta, 0, sizeof ta);
            const uint8_t msrp_da[6] = {0x01,0x80,0xC2,0x00,0x00,0x0E};
            memcpy(ta, msrp_da, 6);
            ta[6]=0x02; ta[7]=0xAA; ta[8]=0xBB; ta[9]=0xCC; ta[10]=0xDD; ta[11]=0x01;
            ta[12]=0x22; ta[13]=0xEA;
            ta[14]=0;                    // ProtocolVersion
            ta[15]=1; ta[16]=25;         // TalkerAdvertise, AttributeLength 25
            ta[17]=0; ta[18]=30;         // AttributeListLength 2+25+1+2
            ta[19]=0; ta[20]=1;          // VectorHeader: LeaveAll 0, NOV 1
            memcpy(ta+21, SID2, 8);      // StreamID
            ta[29]=0x91; ta[30]=0xE0; ta[31]=0xF0; ta[32]=0x00;  // DFP DMAC
            ta[33]=0x3C; ta[34]=0x11;    // = CTX2_RESP_DMAC (the probed pair)
            ta[35]=0x00; ta[36]=0x05;    // vlan 5: WRONG on purpose first
            ta[37]=0x00; ta[38]=0x48;    // TSpec MaxFrameSize 72
            ta[39]=0x00; ta[40]=0x01;    // MaxIntervalFrames 1
            ta[41]=0x70;                 // PriorityAndRank
            // AccumulatedLatency 42..45 = 0
            ta[46]=36;                   // ThreePacked JoinIn
            // --- mismatch leg: sid matches, vlan differs -> IGNORED
            // (5.3.8.9), no registration, sink 2 must NOT settle RSV_OK
            inject(ta, 60, 4000);
            srp = axi_read(A_SW_SRP);
            ck("t21 B1d: wrong-vlan TA never registers (Tab 5.29)",
               (srp >> 12) & 1, 0);
            axi_write(A_STRM_SEL, 0x002);
            (void)axi_read(A_SW_SID_LO);
            snap_and_wait();
            ck("t21 B1d: sink 2 stays SETTLED_NO_RSV on the mismatch",
               axi_read(A_SW_STATE) & 0x7, 6);
            // --- the real TA: all three parameters match
            ta[35]=0x00; ta[36]=0x02;    // vlan 2 = the probed value
            inject(ta, 60, 40);
        }
        got = find_lstn(SID2, -1, 0x80, 400000, &evt, &par);
        ck("t21 TA: re-declared for the bound sid", got ? 1 : 0, 1);
        ck("t21 TA: four-pack READY once the TA is registered", par, 0x80);
        srp = axi_read(A_SW_SRP);
        ck("t21 TA: row shows TA REGISTERED", (srp >> 12) & 1, 1);
        ck("t21 TA: row shows READY", (srp >> 11) & 1, 1);
        //! TASK #64, the other half of the coupling: the row's registrar
        //! level is fed BACK to ACMP sink 2 (acmpl_ta_reg_v_w[2]), so the
        //! sink leaves SETTLED_NO_RSV for SETTLED_RSV_OK - Milan 5.5.3.5.42
        //! (SETTLED_NO_RSV / EVT_TK_REGISTERED). Before task #64 only sink 0
        //! had a registrar bit and every other sink would have sat in
        //! SETTLED_NO_RSV re-probing every TMR_NO_TK forever.
        axi_write(A_STRM_SEL, 0x002);
        (void)axi_read(A_SW_SID_LO);
        snap_and_wait();
        ck("t21 TA: ACMP sink 2 -> SETTLED_RSV_OK (5.5.3.5.42)",
           axi_read(A_SW_STATE) & 0x7, 7);
        // the reservation architecture guard: a LISTENER row must never
        // reach the bw-gate - our talker CBS stays untouched by it
        uint32_t ls = axi_read(A_LWSRP_STATUS);
        ck("t21 guard: no reservation-active from a listener row",
           (ls >> 6) & 1, 0);
        ck("t21 guard: talker stream gate still shut", (ls >> 8) & 1, 0);
        ck("t21 guard: CBS slope mux untouched", (ls >> 9) & 1, 0);
        ck("t21 guard: no ctx shortfall", (ls >> 11) & 1, 0);

        // software that NAMES a sid still wins the row (0x800 override)...
        const uint8_t SIDS[8] = {0x0B,0xAD,0x00,0x00,0xC0,0xDE,0x00,0x02};
        axi_write(A_STRM_SEL, 0x002);
        axi_write(A_SW_SID_LO, 0xC0DE0002);
        axi_write(A_SW_SID_HI, 0x0BAD0000);
        axi_write(A_SW_CTRL, 0x1);
        got = find_lstn(SIDS, -1, -1, 400000, &evt, &par);
        ck("t21 override: the window-named sid takes the row", got ? 1 : 0, 1);
        // ...and a zero-sid release hands it straight back to the fabric,
        // which re-declares the BIND identity (fresh row -> NEW again)
        axi_write(A_STRM_SEL, 0x002);
        axi_write(A_SW_SID_LO, 0);
        axi_write(A_SW_SID_HI, 0);
        axi_write(A_SW_CTRL, 0x0);
        got = find_lstn(SID2, -1, -1, 400000, &evt, &par);
        ck("t21 release: the fabric retakes the row with the bind sid",
           got ? 1 : 0, 1);

        // THE NEW LAW, end to end (B1a sid-zeroing + the |sid want guard):
        // the release handoff blips the row invalid for the fabric retake,
        // which drops the registrar level; the RSV_OK sink sees the
        // combined-attribute fall (EVT_TK_UNREGISTERED — the registration
        // really did fall) and exits settled with the FULL 5.3.8.9
        // parameter clear, sid included. The zero sid drops the fabric
        // want, so the freshly retaken row is withdrawn again until a new
        // probe response re-keys the record — exactly the clause's "return
        // to the probing state to get up-to-date information".
        axi_write(A_STRM_SEL, 0x002);
        (void)axi_read(A_SW_SID_LO);
        {
            uint32_t slz = axi_read(A_SW_SID_LO) | axi_read(A_SW_SID_HI);
            for (int g = 0; g < 64 && slz != 0; g++) {
                for (int c = 0; c < 256; c++) step();
                slz = axi_read(A_SW_SID_LO) | axi_read(A_SW_SID_HI);
            }
            ck("t21 release: registrar blip de-settles, sid zeroed (5.3.8.9)",
               slz, 0);
        }
        srp = axi_read(A_SW_SRP);
        for (int g = 0; g < 64 && ((srp >> 15) & 1); g++) {
            for (int c = 0; c < 256; c++) step();
            srp = axi_read(A_SW_SRP);
        }
        ck("t21 release: ...and the |sid guard withdraws the row",
           (srp >> 15) & 1, 0);

        // re-settle for the steady-state unbind proof below: a fresh
        // UNBIND + BIND draws an immediate probe (no discovery wait) and
        // the talker's answer re-keys the record on the same sid/dmac
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x08;  // UNBIND
            f[16]=0x00; f[17]=44;
            const uint8_t usx[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, usx, 8);
            f[52]=0x00; f[53]=0x02;                          // luid 2
            f[62]=0x72; f[63]=0x01;
            //! the capture is BLIND while a previous answer/probe holds
            //! RESPOND_S/PROBE_S, and the de-settle's row withdraw is
            //! still contending for the control TX trunk — inject with a
            //! generous drain and VERIFY the state took, retrying the
            //! (idempotent) frame if it was swallowed
            for (int at = 0; at < 4; at++) {
                inject(f, 70, 4000);
                axi_write(A_STRM_SEL, 0x002);
                (void)axi_read(A_SW_SID_LO);
                snap_and_wait();
                if ((axi_read(A_SW_STATE) & 7) == 0) break;
            }
            ck("t21 release: teardown for the re-probe took",
               axi_read(A_SW_STATE) & 7, 0);
            f[15]=0x06;                                      // CONNECT_RX
            for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;
            const uint8_t tkr[8] = {0x03,0x00,0x00,0x00,0x00,0x03,0x00,0x01};
            memcpy(f+34, tkr, 8);
            f[50]=0x00; f[51]=0x01;                          // tuid 1
            f[62]=0x72; f[63]=0x02;
            for (int at = 0; at < 4; at++) {
                inject(f, 70, 4000);
                axi_write(A_STRM_SEL, 0x002);
                (void)axi_read(A_SW_SID_LO);
                snap_and_wait();
                if ((axi_read(A_SW_STATE) & 7) == 3) break;
            }
            ck("t21 release: rebind probing (PRB_W_RESP)",
               axi_read(A_SW_STATE) & 7, 3);
        }
        got = find_lstn(SID2, -1, -1, 400000, &evt, &par);
        ck("t21 release: the rebind re-declares the row", got ? 1 : 0, 1);
        {
            // the talker answers (retry per probe, echoing the sniffed
            // sequence_id — the t21-l0 recipe)
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t tsrc[6] = {0x03,0x00,0x00,0x00,0x00,0x03};
            memcpy(f+6, tsrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x01;
            f[16]=0x00; f[17]=44;
            memcpy(f+18, CTX2_RESP_SID, 8);
            for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;
            const uint8_t tkr[8] = {0x03,0x00,0x00,0x00,0x00,0x03,0x00,0x01};
            memcpy(f+34, tkr, 8);
            const uint8_t usx[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, usx, 8);
            f[50]=0x00; f[51]=0x01;
            f[52]=0x00; f[53]=0x02;
            memcpy(f+54, CTX2_RESP_DMAC, 6);
            f[66]=0x00; f[67]=0x02;
            for (int at = 0; at < 8; at++) {
                f[62]=(uint8_t)(probe_seq_by_luid[2] >> 8);
                f[63]=(uint8_t)(probe_seq_by_luid[2] & 0xFF);
                inject(f, 70, 2000);
                axi_write(A_STRM_SEL, 0x002);
                (void)axi_read(A_SW_SID_LO);
                snap_and_wait();
                if ((axi_read(A_SW_STATE) & 7) == 6) break;
            }
            ck("t21 release: re-probed and re-settled (5.5.3.5.18 s4)",
               axi_read(A_SW_STATE) & 7, 6);
        }

        // quiesce to the declared steady state before the unbind: the
        // retake's own NEW frame can still be in flight behind the control
        // TX arbiter, and a row invalidated before its declaration's
        // tx_done is (correctly) treated as never-on-wire - no LV. The
        // contract under test is the STEADY-STATE withdraw, so wait for
        // valid+dir+onwire through the window and drain the stragglers.
        srp = axi_read(A_SW_SRP);
        for (int g = 0; g < 64 && ((srp >> 13) & 0x7) != 0x7; g++) {
            for (int c = 0; c < 256; c++) step();
            srp = axi_read(A_SW_SRP);
        }
        ck("t21 release: row back on wire (declared)", (srp >> 13) & 0x7, 0x7);
        while (find_lstn(SID2, -1, -1, 20000, nullptr, nullptr)) { }

        // UNBIND: the row must be withdrawn - one LV on the wire, then gone
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x08;  // DISCONNECT_RX
            f[16]=0x00; f[17]=44;
            const uint8_t tk[8] = {0x03,0x00,0x00,0x00,0x00,0x03,0x00,0x01};
            memcpy(f+34, tk, 8);
            const uint8_t us[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, us, 8);
            f[50]=0x00; f[51]=0x01;                      // talker_unique_id
            f[52]=0x00; f[53]=0x02;                      // listener_unique_id 2
            f[62]=0x77; f[63]=0x24;
            inject(f, 70, 40);
        }
        got = find_lstn(SID2, 5 * 36, -1, 400000, &evt, &par);
        ck("t21 unbind: the withdraw (LV) went out", got ? 1 : 0, 1);
        ck("t21 unbind: event = LV", evt, 5 * 36);
        srp = axi_read(A_SW_SRP);
        for (int g = 0; g < 64 && ((srp >> 15) & 1); g++) {
            for (int c = 0; c < 256; c++) step();
            srp = axi_read(A_SW_SRP);
        }
        ck("t21 unbind: SRP row withdrawn (invalid)", (srp >> 15) & 1, 0);

        // gh #58 D1 e2e, the unbind half: ctx2's bind level just FELL, so
        // the same-value SET the bound section saw refused with 12 now
        // lands - acmpl_bound_v_w -> lstn_bound_v_i proven in BOTH
        // directions through the real ACMP frames
        {
            std::vector<uint8_t> q2 = {0x00,0x05,0x00,0x02};
            auto g2 = aecp_xact(9, 0x5820, q2);
            ck("t21/gh58: GET_FMT(in2) SUCCESS after unbind",
               aecp_status(g2), 0);
            std::vector<uint8_t> s2(q2);
            for (int i = 0; i < 8 && g2.size() >= 50; i++)
                s2.push_back(g2[42+i]);
            auto r2 = aecp_xact(8, 0x5821, s2);
            ck("t21/gh58: SET(in2) after UNBIND -> SUCCESS (level fell)",
               aecp_status(r2), 0);
        }

        // ==== t21-l0: sink 0's DEDICATED listener row =====================
        // The ax-rv32-g return-leg fix, end to end: sink 0's Listener
        // attribute used to ride the software-owned legacy row 0 (stale
        // dmac, garbage sid - the talker-0 side's row), so the remote talker
        // was never licensed and every t0/l0 loop read FRAMES_RX 0. Sink 0
        // now provisions the DEDICATED row (SRP_LSN0_ROW_C) through the same
        // fabric slot machinery as sinks 1..N-1, and its ACMP registrar
        // feedback comes from THAT row - not the talker's.
        printf("-- t21-l0: sink 0 -> DEDICATED lwSRP listener row --\n");
        {
            const uint8_t L0_SID[8]  = {0x3C,0xC0,0xC6,0x01,0x02,0x03,0x00,0x00};
            const uint8_t L0_DMAC[6] = {0x91,0xE0,0xF0,0x00,0xBE,0xC6};
            axi_write(A_LWSRP_CTRL, 0x15);           // engine ON, no talker
            // CONNECT_RX luid 0, fast-connect sid ZERO (bind-now-probe-later,
            // the real peer's shape: its sid equals its entity id)
            {
                uint8_t f[72]; memset(f, 0, sizeof f);
                const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
                memcpy(f, mc, 6);
                const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
                memcpy(f+6, csrc, 6);
                f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x06;
                f[16]=0x00; f[17]=44;
                for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;
                const uint8_t tk0[8] = {0x3C,0xC0,0xC6,0x01,0x02,0x03,0x00,0x00};
                memcpy(f+34, tk0, 8);
                const uint8_t us0[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
                memcpy(f+42, us0, 8);
                f[52]=0x00; f[53]=0x00;               // listener_unique_id 0
                f[62]=0x69; f[63]=0x01;
                //! drain BARELY past delivery: the 4c shape's shorter walk
                //! cycle launches the declaration inside a 200-cycle drain,
                //! which scans nothing - hand the window to find_lstn
                inject(f, 70, 24);
            }
            // THE BITE, half one: the BIND alone declares sink 0's Listener
            // attribute on the DEDICATED row - previously impossible. The
            // derived sid ({talker EID, tuid 0}) equals the peer-shaped
            // response sid here, so this is also the only NEW declaration
            // the whole flow emits (the probe answer re-provisions the SAME
            // identity - a no-op for the wire).
            int evt0 = -1, par0 = -1;
            //! the declaration launches ~1.4k cycles post-bind on the 8x8
            //! leg but the 4c leg's slower join timer needs far more; the
            //! scan exits on first match, and the ladder walking into RETRY
            //! is harmless now that the answer below re-tries per probe
            //! (exactly the live peer's behaviour)
            bool got0 = find_lstn(L0_SID, -1, -1, 120000, &evt0, &par0);
            ck("t21-l0: Listener declaration for sink 0's sid on the wire",
               got0 ? 1 : 0, 1);
            // the probe answer: the authoritative sid + dmac (5.5.3.5.18 s4)
            {
                uint8_t f[72]; memset(f, 0, sizeof f);
                const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
                memcpy(f, mc, 6);
                const uint8_t tsrc[6] = {0x3C,0xC0,0xC6,0x01,0x02,0x03};
                memcpy(f+6, tsrc, 6);
                f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x01;
                f[16]=0x00; f[17]=44;
                memcpy(f+18, L0_SID, 8);
                for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;
                const uint8_t tk0[8] = {0x3C,0xC0,0xC6,0x01,0x02,0x03,0x00,0x00};
                memcpy(f+34, tk0, 8);
                const uint8_t us0[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
                memcpy(f+42, us0, 8);
                f[52]=0x00; f[53]=0x00;               // luid 0
                memcpy(f+54, L0_DMAC, 6);
                f[66]=0x00; f[67]=0x02;               // stream_vlan_id 2
                // the walker is DEAF in RESPOND_S/PROBE_S and the SM is in
                // ACTIVE re-probe - a single answer can land in a deaf beat
                // and vanish. The live peer answers EVERY probe (1.4 ms,
                // tap-proven), so retry until the SM leaves PRB_W_RESP —
                // each attempt echoing the LATEST sniffed probe seq
                // (5.5.3.5.18 step 1).
                for (int at = 0; at < 8; at++) {
                    f[62]=(uint8_t)(probe_seq_by_luid[0] >> 8);
                    f[63]=(uint8_t)(probe_seq_by_luid[0] & 0xFF);
                    inject(f, 70, 2000);
                    if ((axi_read(0x6A4) & 7) >= 4) break;
                }
            }
            // window view via the NEW A_STRM_SEL[9] select
            axi_write(A_STRM_SEL, 0x200);
            (void)axi_read(A_SW_SRP);
            uint32_t srp0 = axi_read(A_SW_SRP);
            for (int g = 0; g < 64 && ((srp0 >> 13) & 0x7) != 0x7; g++) {
                for (int c = 0; c < 256; c++) step();
                srp0 = axi_read(A_SW_SRP);
            }
            ck("t21-l0: row VALID via the [9] select", (srp0 >> 15) & 1, 1);
            ck("t21-l0: row direction = LISTENER", (srp0 >> 14) & 1, 1);
            ck("t21-l0: row backed (not 0xDEAD)",
               (srp0 & 0xFFFF) == 0xDEAD ? 1 : 0, 0);
            // a TalkerAdvertise for the sid: READY + the sink 0 feedback
            {
                uint8_t ta[64]; memset(ta, 0, sizeof ta);
                const uint8_t msrp_da[6] = {0x01,0x80,0xC2,0x00,0x00,0x0E};
                memcpy(ta, msrp_da, 6);
                ta[6]=0x3C; ta[7]=0xC0; ta[8]=0xC6; ta[9]=0x01; ta[10]=0x02; ta[11]=0x03;
                ta[12]=0x22; ta[13]=0xEA;
                ta[14]=0;
                ta[15]=1; ta[16]=25;
                ta[17]=0; ta[18]=30;
                ta[19]=0; ta[20]=1;
                memcpy(ta+21, L0_SID, 8);
                memcpy(ta+29, L0_DMAC, 6);
                ta[35]=0x00; ta[36]=0x02;
                ta[37]=0x00; ta[38]=0x48;
                ta[39]=0x00; ta[40]=0x01;
                ta[41]=0x70;
                ta[46]=36;
                inject(ta, 60, 40);
            }
            bool gotr = find_lstn(L0_SID, -1, 0x80, 400000, &evt0, &par0);
            ck("t21-l0: four-pack READY once the TA is registered",
               gotr ? 1 : 0, 1);
            // sink 0's SM promotes on the DEDICATED row's registrar - read
            // at the very register the silicon evidence used (ACMPL_STATE)
            {
                enum { A_ACMPL_STATE = 0x6A4 };
                uint32_t a0 = axi_read(A_ACMPL_STATE);
                for (int g = 0; g < 64 && (a0 & 0x7) != 7; g++) {
                    for (int c = 0; c < 256; c++) step();
                    a0 = axi_read(A_ACMPL_STATE);
                }
                ck("t21-l0: sink 0 SETTLED_RSV_OK from ITS OWN row (5.5.3.5.42)",
                   a0 & 0x7, 7);
            }
            // the legacy row-0 (talker side) must be UNTOUCHED by all of it
            uint32_t ls0 = axi_read(A_LWSRP_STATUS);
            ck("t21-l0: legacy row reservation-active still 0",
               (ls0 >> 6) & 1, 0);
            axi_write(A_STRM_SEL, 0x000);
        }

        // ==== t27: the CRF Media Clock Input sink's OWN listener row =====
        // MILAN_COMPLIANCE_GAPS.md 3, closed: the pinned-LAST sink
        // (listener_unique_id = N_STREAMS) provisions the appended
        // SRP_CRFSNK row from its ACMP bind exactly like every AAF sink,
        // so the walker declares its Listener attribute and a Milan CRF
        // talker gets the Ready it licences on. Silicon 08-07: DS20 CRF
        // bound + connect-tx OK, ONE PDU arrived, then silence - our
        // Ready structurally could not go out (no row existed).
        printf("-- t27: CRF sink -> appended lwSRP listener row --\n");
        {
            // derived provisional sid = {talker EID, tuid 2} (the peer's
            // CRF output is its SO[2], per the bench topology)
            const uint8_t CS_SID[8]  = {0x3C,0xC0,0xC6,0x01,0x02,0x03,0x00,0x02};
            const uint8_t CS_DMAC[6] = {0x91,0xE0,0xF0,0x00,0xBE,0xC7};
            axi_write(A_LWSRP_CTRL, 0x15);           // engine ON, no talker
            // CONNECT_RX luid N (the pinned CRF sink), fast-connect sid 0
            // (bind-now-probe-later, the real peer's shape)
            {
                uint8_t f[72]; memset(f, 0, sizeof f);
                const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
                memcpy(f, mc, 6);
                const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
                memcpy(f+6, csrc, 6);
                f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x06;
                f[16]=0x00; f[17]=44;
                for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;
                const uint8_t tkc[8] = {0x3C,0xC0,0xC6,0x01,0x02,0x03,0x00,0x00};
                memcpy(f+34, tkc, 8);
                const uint8_t usc[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
                memcpy(f+42, usc, 8);
                f[50]=0x00; f[51]=0x02;               // talker_unique_id 2
                f[52]=0x00; f[53]=(uint8_t)NSTREAMS_TB; // luid N = CRF sink
                f[62]=0x27; f[63]=0x01;
                inject(f, 70, 24);
            }
            // the bind level reaches the pinned-LAST compatibility view -
            // ACMPL_STATE[31] is acmpl1_bound, which task #27 re-aims from
            // the literal ctx 1 to the LAST ctx (identical on 2-sink
            // shapes, the WRONG AAF sink before on this very leg)
            {
                uint32_t a1 = axi_read(0x6A4);
                for (int g = 0; g < 64 && !((a1 >> 31) & 1); g++) {
                    for (int c = 0; c < 256; c++) step();
                    a1 = axi_read(0x6A4);
                }
                ck("t27: CRF-sink bind level on ACMPL_STATE[31] (pinned-LAST view)",
                   (a1 >> 31) & 1, 1);
            }
            // THE BITE: the fabric declares the CRF sink's Listener
            // attribute on the appended row - previously structurally
            // impossible. The derived {talker EID, tuid 2} sid equals the
            // authoritative one here, so this is the flow's one NEW.
            int evtc = -1, parc = -1;
            bool gotc = find_lstn(CS_SID, -1, -1, 400000, &evtc, &parc);
            ck("t27: Listener declaration for the CRF sid on the wire",
               gotc ? 1 : 0, 1);
            ck("t27: four-pack ASKING-FAILED before any TA", parc, 0x40);
            // a TalkerAdvertise for the CRF sid: READY must follow - this
            // is the exact frame the DS20 stood down waiting for
            {
                uint8_t ta[64]; memset(ta, 0, sizeof ta);
                const uint8_t msrp_da[6] = {0x01,0x80,0xC2,0x00,0x00,0x0E};
                memcpy(ta, msrp_da, 6);
                ta[6]=0x3C; ta[7]=0xC0; ta[8]=0xC6; ta[9]=0x01; ta[10]=0x02; ta[11]=0x03;
                ta[12]=0x22; ta[13]=0xEA;
                ta[14]=0;
                ta[15]=1; ta[16]=25;
                ta[17]=0; ta[18]=30;
                ta[19]=0; ta[20]=1;
                memcpy(ta+21, CS_SID, 8);
                memcpy(ta+29, CS_DMAC, 6);
                ta[35]=0x00; ta[36]=0x02;
                ta[37]=0x00; ta[38]=0x48;
                ta[39]=0x00; ta[40]=0x01;
                ta[41]=0x70;
                ta[46]=36;
                inject(ta, 60, 40);
            }
            bool gotcr = find_lstn(CS_SID, -1, 0x80, 400000, &evtc, &parc);
            ck("t27: four-pack READY once the CRF TA is registered",
               gotcr ? 1 : 0, 1);
        }

        axi_write(A_STRM_SEL, 0x000);
        axi_write(A_LWSRP_CTRL, 0x0);
        for (int c = 0; c < 512; c++) step();
    }

    // ==================================================================
    //  B1a/B1d companion — THE |sid WANT GUARD, end to end. A bound sink
    //  whose record sid is ZERO must never provision an lwSRP listener
    //  row: a Listener declaration for stream 0 is a reservation for a
    //  stream that cannot exist, and the settled exits now ZERO the sid
    //  per Milan 5.3.8.9 (a not-settled Stream Input records all-zero
    //  SRP parameters). The E1 bind-restore is the lawful way to hold
    //  bound + sid-0 at full clock rate (5.5.2.6 step 1 clears the
    //  parameters until the probe response re-learns them), so it drives
    //  the guard here; the sid-zeroing exits themselves are pinned at the
    //  scaled clock in tb/verilator/acmp_lstn ([7]/[14]/[B1]/[B1a]).
    // ==================================================================
    printf("-- b1d-guard: bound-with-sid-0 sink provisions NO row --\n");
    {
        enum { A_REST_TKLO = 0x7A0, A_REST_TKHI = 0x7A4,
               A_REST_META = 0x7A8, A_REST_CTLO = 0x7AC,
               A_REST_CTHI = 0x7B0, A_REST_CMD  = 0x7B4,
               A_SW_SRP = 0x85C };
        axi_write(A_LWSRP_CTRL, 0x15);        // engine ON, no talker declare
        // sink 0 carries the leg: its row is the DEDICATED listener-0 row,
        // reachable only through the A_STRM_SEL[9] select this flow never
        // COMMITS through — so its want term can never be masked by a
        // software claim (the N-wide routing case upstream owns every
        // window stream 1..N-1), and probing it disturbs no stream-table
        // entry a later section (the 8x8 loopback lane) still feeds.
        // unbind it first (t21-l0 left it settled RSV_OK; the restore
        // refuses an OCCUPIED context)
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x08;  // DISCONNECT_RX
            f[16]=0x00; f[17]=44;
            const uint8_t us1[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, us1, 8);
            f[52]=0x00; f[53]=0x00;                          // luid 0
            f[62]=0x71; f[63]=0x77;
            inject(f, 70, 4000);
        }
        // E1 restore into sink 0: talker {3C:C0:C6:01:02:03, uid CAFE},
        // tuid 0, controller pw0 — the 5.5.3.5.2 entry record parks
        // PRB_W_AVAIL with sid/dmac/vlan CLEARED
        axi_write(A_REST_TKLO, 0x0203CAFEu);
        axi_write(A_REST_TKHI, 0x3CC0C601u);
        axi_write(A_REST_META, 0x00000000u);                 // tuid 0
        axi_write(A_REST_CTLO, 0x95B2D1AAu);
        axi_write(A_REST_CTHI, 0x6805CAFFu);
        axi_write(A_REST_CMD,  0x80000000u);                 // commit, idx 0
        uint32_t rc = axi_read(A_REST_CMD);
        for (int g = 0; g < 64 && (rc >> 31); g++) {
            for (int c = 0; c < 64; c++) step();
            rc = axi_read(A_REST_CMD);
        }
        ck("b1d-guard: restore DONE", (rc >> 30) & 1, 1);
        ck("b1d-guard: restore status = injected", (rc >> 8) & 3, 0);
        // the ACMP view: bound with the 5.5.2.6 step 1 all-zero sid
        // (SEL[9] = the sink-0 / LSN0-row select, the t21-l0 surface)
        axi_write(A_STRM_SEL, 0x200);
        (void)axi_read(A_SW_SID_LO);
        ck("b1d-guard: restored record sid reads 0 (5.5.2.6 s1)",
           axi_read(A_SW_SID_LO) | axi_read(A_SW_SID_HI), 0);
        // the guard: bound level HIGH + sid ZERO -> the provisioner must
        // sit on its hands. Give it a generous window, then look.
        for (int c = 0; c < 8192; c++) step();
        uint32_t srp1 = axi_read(A_SW_SRP);
        srp1 = axi_read(A_SW_SRP);
        ck("b1d-guard: NO lwSRP row for a sid-0 binding (want &= |sid)",
           (srp1 >> 15) & 1, 0);
        // control: a real BIND on the same sink derives a NONZERO sid at
        // the record write itself -> the want rises -> the row appears
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x06;  // CONNECT_RX
            f[16]=0x00; f[17]=44;
            for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;
            const uint8_t tk1[8] = {0x3C,0xC0,0xC6,0x01,0x02,0x03,0x00,0x01};
            memcpy(f+34, tk1, 8);
            const uint8_t us1[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, us1, 8);
            f[50]=0x00; f[51]=0x01;                          // tuid 1
            f[52]=0x00; f[53]=0x00;                          // luid 0
            f[62]=0x71; f[63]=0x78;
            inject(f, 70, 4000);
        }
        axi_write(A_STRM_SEL, 0x200);
        (void)axi_read(A_SW_SID_LO);
        uint32_t sl1 = axi_read(A_SW_SID_LO);
        for (int g = 0; g < 64 && sl1 != 0x02030001u; g++) {
            for (int c = 0; c < 256; c++) step();
            sl1 = axi_read(A_SW_SID_LO);
        }
        ck("b1d-guard: bind derives a nonzero sid", sl1, 0x02030001u);
        srp1 = axi_read(A_SW_SRP);
        for (int g = 0; g < 64 && !((srp1 >> 15) & 1); g++) {
            for (int c = 0; c < 256; c++) step();
            srp1 = axi_read(A_SW_SRP);
        }
        ck("b1d-guard: the nonzero-sid bind DOES provision the row",
           (srp1 >> 15) & 1, 1);
        ck("b1d-guard: ...as a LISTENER row", (srp1 >> 14) & 1, 1);
        // tidy: unbind sink 0 (VERIFIED — a swallowed unbind would leave
        // its probe ladder resending into the next section's sniffers),
        // engine off — the flow's steady posture
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x08;
            f[16]=0x00; f[17]=44;
            const uint8_t us1[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, us1, 8);
            f[52]=0x00; f[53]=0x00;
            f[62]=0x71; f[63]=0x79;
            uint32_t slu = 1;
            for (int at = 0; at < 4 && slu != 0; at++) {
                inject(f, 70, 4000);
                axi_write(A_STRM_SEL, 0x200);
                (void)axi_read(A_SW_SID_LO);
                slu = axi_read(A_SW_SID_LO) | axi_read(A_SW_SID_HI);
            }
            ck("b1d-guard: tidy unbind landed (record cleared)", slu, 0);
        }
        axi_write(A_STRM_SEL, 0x000);
        axi_write(A_LWSRP_CTRL, 0x0);
        for (int c = 0; c < 8192; c++) step();
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
        axi_write(A_LWSRP_CTRL, 0x37);          // enable + talker + declare bypass
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
            axi_write(A_LWSRP_CTRL, 0x37);      // provisions the CRF row NOW
                                                // (declare bypass: no probe
                                                // or listener in this leg)
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
        // MILAN v1.2 4.3.3.2 Table 4.4 row "CRF, 1 ts/pdu": MaxFrameSize =
        // 28 + 1, and the clause makes the table's values a "shall use".
        // This used to declare the PADDED wire MSDU (42) because the bare
        // payload once left a 60-octet slot reserved for an 84-octet frame -
        // but the clause's own remedy for that is step 2 of the bandwidth
        // recipe, the 68-octet minimum-frame clamp, which the bw gate now
        // implements. With the clamp, 29 reserves 88 wire octets and covers
        // the real 84; without it, 42 reserved 5376 kbps where the table
        // mandates 5632.
        ck("MSRP: TSpec MaxFrameSize = Table 4.4 CRF 28 + 1", ta_mf, 29);
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

#ifdef AAF_PB_TB
    // ==================================================================
    //  TASK #31 - HOST PLAYBACK RING -> chmap RING bucket -> TALKER WIRE
    //  (AAF_PLAYBACK_P=1, the cfg_ax8x8 ship flip). The full playback
    //  path IN the datapath: a host-written PCM ring is fetched over the
    //  pb_mem word port, paced by KL_pcm_tx, latched by the capture
    //  crossbar's RING bucket, and framed by the packetizer - the ALSA
    //  aplay direction, ending at the MAC TX AXIS.
    //
    //  Placement decoupling is the point of the map: ring PAIR 0 (host
    //  channels 0/1) is mapped onto BOTH talker 0's and talker 1's wire
    //  slots - the mechanism that puts host stereo on the peer-facing
    //  stream channels of the USER's choice (ch2/3 in the 8ch target).
    //
    //  Underrun continuity (Milan 5.3.7.3): starving the ring must KEEP
    //  the talkers framing - payload goes digital-silence, cadence never
    //  stalls - and the starvation is CSR-observable (PBK_RAILS 0x8D0 +
    //  the pb_underrun_o rail).
    // ==================================================================
    printf("-- task #31: host ring -> RING bucket -> talker wire (pb) --\n");
    {
        enum { A_CHMAP_CTRL = 0x900, A_CHMAP_SEL = 0x904, A_CHMAP_WORD = 0x908,
               A_PBK_RAILS = 0x8D0 };
        const uint32_t PB_LEN    = 512;      // 64-word sub-ring
        const uint32_t PB_STRIDE = 4096;
        const int      PB_LEAD   = 32;       // words kept ahead of the reader

        // streaming posture (VID-2 rule + bypass licence), lwSRP off
        axi_write(A_AAF_CTRL, 0x00020003);
        axi_write(A_LWSRP_CTRL, 0x0);

        // capture map, PER-CHANNEL (0x0027): channels 0..3 <- RING pair 0,
        // halves L,R,L,R. Window word {en[15], src[14:12]=3 RING,
        // half[8], idxh[7:4]=0, idx[3:0]=0}. At 2 wire channels keys 2/3
        // are talker 1's pair (the same harmless extra coverage the old
        // slot-1 strobe gave); the 4-wire-channel shape NEEDS all four or
        // its talker-0 frame carries silence on ch2/ch3.
        axi_write(A_CHMAP_CTRL, 0x1);        // arm the fabric + the CSR port
        for (int k = 0; k < 4; k++) {
            axi_write(A_CHMAP_SEL, 0x100 | k);
            axi_write(A_CHMAP_WORD, 0xB000 | ((k & 1) << 8));
        }

        // playback engine: ring stream 0 only, silence-on-underrun
        dut->pb_ring_base_i   = 0;
        dut->pb_ring_len_i    = PB_LEN;
        dut->pb_ring_stride_i = PB_STRIDE;
        dut->pb_underrun_silence_i = 1;
        dut->pb_enable_i    = 1;
        dut->pb_stream_en_i = 0x01;

        // host ring model: ramp-tagged S32BE pairs, L=0x7A0000|j R=0x7B0000|j
        static uint8_t pbram[PB_STRIDE + PB_LEN + 64];
        uint32_t pb_committed = 0;           // words written
        auto pb_put = [&](uint32_t j) {
            uint32_t a = (j * 8) % PB_LEN;
            uint32_t L = 0x7A0000u | (j & 0xFFFF), R = 0x7B0000u | (j & 0xFFFF);
            pbram[a+0] = L >> 16; pbram[a+1] = L >> 8; pbram[a+2] = L; pbram[a+3] = 0;
            pbram[a+4] = R >> 16; pbram[a+5] = R >> 8; pbram[a+6] = R; pbram[a+7] = 0;
        };
        bool pb_feed = true;
        bool mem_pend = false; uint32_t mem_addr = 0;
        auto pb_service = [&](void) {        // call between lo() and hi()
            // 1-cycle-latency word port (the BRAM-ring timing)
            dut->pb_mem_valid_i = mem_pend ? 1 : 0;
            if (mem_pend) {
                uint64_t w = 0;
                for (int b = 0; b < 8; b++)
                    w |= (uint64_t)pbram[(mem_addr % (PB_STRIDE + PB_LEN)) + b] << (8*b);
                dut->pb_mem_data_i = w;
            }
            mem_pend = dut->pb_mem_rd_o; mem_addr = dut->pb_mem_addr_o;
            if (pb_feed) {
                uint32_t rdw = dut->pb_rd_ptr_o[0] / 8;
                while (pb_committed < rdw + PB_LEAD) pb_put(pb_committed++);
            }
            dut->pb_wr_ptr_i[0] = pb_committed * 8;
        };

        // AAF PDU capture with the ring-tag payload decode (t0 + t1)
        struct Pdu { int uid; std::vector<uint32_t> smp; bool zero; };
        auto collect = [&](int want_t0, int want_t1, int budget) {
            std::vector<Pdu> got;
            std::vector<uint8_t> cur;
            int n0 = 0, n1 = 0;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < budget && (n0 < want_t0 || n1 < want_t1); c++) {
                lo();
                pb_service();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        size_t off = (cur.size() > 17 && cur[12] == 0x81
                                      && cur[13] == 0x00) ? 4 : 0;
                        if (cur.size() >= 86 + off && cur[12+off] == 0x22
                            && cur[13+off] == 0xF0 && cur[14+off] == 0x02) {
                            Pdu p; p.uid = (cur[24+off] << 8) | cur[25+off];
                            p.zero = true;
                            for (int s = 0; s < 12; s++) {   // 6 events x 2ch
                                size_t o = 38 + off + 4*s;
                                uint32_t v = ((uint32_t)cur[o] << 16) |
                                             ((uint32_t)cur[o+1] << 8) | cur[o+2];
                                p.smp.push_back(v);
                                if (v) p.zero = false;
                            }
                            if (p.uid == 0) { n0++; got.push_back(p); }
                            else if (p.uid == 1) { n1++; got.push_back(p); }
                        }
                        cur.clear();
                    }
                }
                hi();
            }
            return got;
        };

        // ---- LEG 1: both talkers carry the ring pair, ramp-exact -------
        // settle: let the engine start fetching and the buckets fill
        for (int c = 0; c < 4096; c++) { lo(); pb_service(); hi(); }
        auto pdus = collect(3, 3, 200000);
        int t0n = 0, t1n = 0; bool tags_ok = true, ramp_ok = true, lr_ok = true;
        int started = 0;                     // per-uid bit: ring seen yet
        for (auto& p : pdus) {
            (p.uid ? t1n : t0n)++;
            int prev = -1;
            for (int s = 0; s < 12; s += 2) {
                uint32_t L = p.smp[s], R = p.smp[s+1];
                //! 0x002C: the crossbar frames from BOOT, so the first
                //! captured PDU may straddle the silence->ring start -
                //! leading digital-silence events are the stream's legal
                //! pre-start tail, never a tag or ramp defect. A zero
                //! event AFTER the ring started still fails both checks.
                if (!((started >> p.uid) & 1)) {
                    if (L == 0 && R == 0) continue;
                    started |= 1 << p.uid;
                }
                if ((L >> 16) != 0x7A || (R >> 16) != 0x7B) tags_ok = false;
                if ((L & 0xFFFF) != (R & 0xFFFF)) lr_ok = false;
                // consecutive sample events step the ramp by exactly 1
                // (same clk, same divisor: no repeats, no drops)
                if (prev >= 0 &&
                    (uint16_t)(p.smp[s] & 0xFFFF) !=
                    (uint16_t)((p.smp[prev] & 0xFFFF) + 1)) ramp_ok = false;
                prev = s;
            }
        }
        ck("pb: t0 frames the host ring (>= 3 PDUs)", t0n >= 3, 1);
        ck("pb: t1 frames the SAME ring pair (>= 3)", t1n >= 3, 1);
        ck("pb: every sample carries the ring tag (L=7A/R=7B)", tags_ok, 1);
        ck("pb: L/R of one ring word stay a pair", lr_ok, 1);
        ck("pb: ramp steps by 1 per sample event (no slip)", ramp_ok, 1);
        ck("pb: engine consumed the ring (rd_ptr advanced)",
           dut->pb_rd_ptr_o[0] > 0, 1);
        ck("pb: no underrun while fed", dut->pb_underrun_o[0] & 0xFFFF, 0);

        // ---- LEG 2: starvation = SILENCE payload, cadence NEVER stalls -
        pb_feed = false;                      // freeze the host write pointer
        // drain the PB_LEAD words still queued (one word per media sample
        // at CHANS=2: ~PB_LEAD x 2083 cycles) until the engine reports the
        // first real underrun - the rail IS the drain oracle
        { int dg = 0;
          while ((dut->pb_underrun_o[0] & 0xFFFF) == 0 && dg++ < 400000) {
              lo(); pb_service(); hi(); } }
        auto starved = collect(3, 0, 200000);
        int zt0 = 0;
        for (auto& p : starved) if (p.uid == 0 && p.zero) zt0++;
        ck("pb starve: t0 KEEPS framing (5.3.7.3 cadence)",
           starved.size() >= 3, 1);
        ck("pb starve: payload is digital silence", zt0 >= 2, 1);
        ck("pb starve: underruns counted on the rail",
           (dut->pb_underrun_o[0] & 0xFFFF) > 0, 1);
        uint32_t rails = axi_read(A_PBK_RAILS);
        ck("pb starve: PBK_RAILS 0x8D0 shows the underruns",
           (rails >> 16) > 0, 1);

        // ---- LEG 3: refeed = audio returns (session survives a gap) ----
        pb_feed = true;
        for (int c = 0; c < 4096; c++) { lo(); pb_service(); hi(); }
        auto back = collect(3, 0, 200000);
        bool alive = false;
        for (auto& p : back) if (p.uid == 0 && !p.zero &&
                                 (p.smp[0] >> 16) == 0x7A) alive = true;
        ck("pb refeed: ramp audio returns on the wire", alive, 1);

        // restore: engine off, map disarmed (the legacy bit-identical path)
        dut->pb_enable_i = 0; dut->pb_stream_en_i = 0;
        axi_write(A_CHMAP_CTRL, 0x0);
    }
#endif

    // ==================================================================
    //  TASK #65 - rx -> talker LOOPBACK: the AEM's DECLARED source, made
    //  real in the fabric.
    //
    //  The entity advertises 8 "Loopback S<s> ch <c>" AUDIO_CLUSTERs on
    //  every talker STREAM_PORT_OUTPUT, and the POWER-ON dynamic map wakes
    //  pointing every talker stream channel AT them: generated
    //  AEM_ODMAP_INIT_C = {valid, cluster offset 9..16}, whose
    //  AEM_ODMAP_CSRC_C templates are src = 5 = SRC_LOOP, which the AECP
    //  seeder writes into this very map RAM as {en, src=5, idx} = 0xD0|k.
    //
    //  KL_chan_map_capture has carried that bucket since 2026-07-28, but
    //  its five lb_* inputs were never connected in milan_datapath, so they
    //  took their `= 0` port defaults: the hold bank could never be written
    //  and EVERY loopback cluster selected SILENCE. A booted, bound talker
    //  therefore streamed conformant digital silence on every channel while
    //  GET_AUDIO_MAP showed a fully-populated, entirely honest-looking map -
    //  the trap that cost a USER a listening session.
    //
    //  BITE: drop any one of the five lb_* connections in milan_datapath
    //  and the talker payload collapses to all-zero, which "carries the
    //  RECEIVED audio" below refuses. The zero-payload check alone is not
    //  enough - digital silence is a LEGAL payload (5.3.7.3 fill) - so the
    //  emitted samples are matched against the exact bytes that were
    //  received, and L/R against the wire pair they were de-interleaved
    //  from. Nothing but a working loopback lane can produce those.
    // ==================================================================
    printf("-- task #65: rx -> talker LOOPBACK (chmap src 5) --\n");
    {
        enum { A_CHMAP_CTRL = 0x900, A_CHMAP_SEL = 0x904,
               A_CHMAP_WORD = 0x908 };
        const uint8_t LB_PAY0 = 0xA0;     // mkaaf payload seed (no 8-bit wrap)
        const int     LB_SID  = 1;        // sidB is provisioned to stream 1

        // the 12 S32BE samples mkaaf lays down, as the 24 audio bits the
        // depacketizer forwards and the packetizer re-emits: wire byte j in
        // lane j, lanes 3/7 the S32 pad (KL_chan_map_capture lb_tdata_i
        // contract, and tb/verilator/chmap_capture's lb_beat()).
        auto lb_smp = [&](int j) {
            return ((uint32_t)(uint8_t)(LB_PAY0 + 4*j)     << 16)
                 | ((uint32_t)(uint8_t)(LB_PAY0 + 4*j + 1) <<  8)
                 |  (uint32_t)(uint8_t)(LB_PAY0 + 4*j + 2);
        };

        // streaming posture: VID-2 rule + the bypass licence, lwSRP off -
        // the same arming the host-ring leg above uses
        axi_write(A_AAF_CTRL, 0x00020003);
        axi_write(A_LWSRP_CTRL, 0x0);

        // capture map, PER-CHANNEL (0x0027): channels <- LOOP {stream 1,
        // pair 0}, halves L,R,L,R. CSR word = {en[15], src[14:12]=5 LOOP,
        // half[8], idxh[7:4]=stream, idx[3:0]=pair}. Four keys because the
        // harness runs three shapes: at TALKER_WIRE_CHANS_P=2 keys 2/3 are
        // talker 1 (harmless extra coverage), while the 4-wire-channel
        // shape needs talker 0's four channels armed before the packetizer
        // can assemble a 4-channel frame at all.
        axi_write(A_CHMAP_CTRL, 0x1);
        for (int k = 0; k < 4; k++) {
            axi_write(A_CHMAP_SEL, 0x100 | k);
            axi_write(A_CHMAP_WORD, (uint32_t)(0x8000 | (5 << 12)
                                               | ((k & 1) << 8)
                                               | (LB_SID << 4) | 0));
        }

        // feed the listener: three AAF PDUs of stream 1, 2 wire channels.
        // The bucket's holds free-run, so after the burst they retain the
        // last received pair and the talker keeps re-emitting it.
        for (uint8_t s = 0; s < 3; s++)
            inject(mkaaf(sidB, (uint8_t)(120 + s), 2, LB_PAY0), 2000);

        // collect talker 0's PDUs (uid 0), decoding the 6 events x 2 ch
        std::vector<std::vector<uint32_t>> lbp;
        {
            std::vector<uint8_t> cur;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 200000 && (int)lbp.size() < 3; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l))
                                          & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        size_t off = (cur.size() > 17 && cur[12] == 0x81
                                      && cur[13] == 0x00) ? 4 : 0;
                        if (cur.size() >= 86 + off && cur[12+off] == 0x22
                            && cur[13+off] == 0xF0 && cur[14+off] == 0x02
                            && ((cur[24+off] << 8) | cur[25+off]) == 0) {
                            std::vector<uint32_t> smp;
                            for (int s = 0; s < 12; s++) {
                                size_t o = 38 + off + 4*s;
                                smp.push_back(((uint32_t)cur[o]   << 16) |
                                              ((uint32_t)cur[o+1] <<  8) |
                                               (uint32_t)cur[o+2]);
                            }
                            lbp.push_back(smp);
                        }
                        cur.clear();
                    }
                }
                hi();
            }
        }
        ck("lb: talker 0 frames while the LOOP slot is mapped",
           lbp.size() >= 3, 1);

        // LOOPBACK_P is a paired flag: the Makefile passes -GLOOPBACK_P=1
        // together with -DLOOPBACK_TB, so this side always knows which
        // gateware it is talking to. BOTH states are pinned - ON must carry
        // the received audio, OFF must be silent BY CONSTRUCTION, and that
        // OFF row is the whole reason the builder's power-on map may not
        // point a talker channel at a loopback cluster in a build that did
        // not elaborate the lane.
#ifdef LOOPBACK_TB
        const int LB_LANE = 1;
#else
        const int LB_LANE = 0;
#endif
        bool any_audio = false, all_from_rx = true, pairs_ok = true;
        for (auto& p : lbp) {
            for (size_t s = 0; s + 1 < p.size(); s += 2) {
                uint32_t L = p[s], R = p[s+1];
                if (L || R) any_audio = true;
                // L must be an EVEN-indexed received sample (wire ch 0) and
                // R the one that followed it (wire ch 1): the de-interleave
                int li = -1;
                for (int j = 0; j < 12; j += 2) if (lb_smp(j) == L) li = j;
                if (li < 0) all_from_rx = false;
                else if (R != lb_smp(li + 1)) pairs_ok = false;
            }
        }
        if (LB_LANE) {
            ck("lb: talker payload is NOT digital silence", any_audio, 1);
            ck("lb: every sample is one the LISTENER received",
               all_from_rx, 1);
            ck("lb: L/R stay the wire pair they arrived as", pairs_ok, 1);
        } else {
            // LOOPBACK_P=0: the bucket is elaborated at its minimum with the
            // feed tied off, so a mapped loopback slot can only ever be
            // silence. An entity that ADVERTISED this cluster here would be
            // describing a source the gateware does not contain.
            ck("lb (lane OFF): a loopback slot is silent by construction",
               any_audio, 0);
        }

        // An UNMAPPED loop slot stops carrying the received audio - the
        // bucket is selected BY THE MAP and never leaks into a slot that
        // did not ask for it. But it must stop carrying audio the way the
        // clause allows: by SENDING SILENCE, not by going off the wire.
        //
        // Milan v1.2 5.3.9.1 makes "not mapped" a legal state for a
        // channel of a Stream Output; 5.3.7.3 says the PAAD "shall be
        // streaming AVTP packets" while it declares Talker Advertise and
        // sees a Listener Ready, and forbids STREAMING_WAIT outright. So
        // unmapping a channel owes the wire silence INSIDE a frame that
        // still goes out.
        //
        // This is the integration-level half of the proof, and it needs
        // to live HERE rather than in tb/verilator/chmap_capture: the
        // reason the gap was reachable at all is the milan_datapath
        // pkt_pv_w bypass, which mutes KL_pair_zero_fill - the guard that
        // covers exactly this for the front-end path - for as long as
        // CHMAP is armed. Only a datapath leg has both halves in it.
        // Before the fix this loop collected ZERO talker-0 PDUs.
        for (int k = 0; k < 4; k++) {
            axi_write(A_CHMAP_SEL, 0x100 | k);
            axi_write(A_CHMAP_WORD, 0x0000);     // en = 0
        }
        for (int c = 0; c < 20000; c++) step();
        {
            std::vector<uint8_t> cur; int leaked = 0; int seen = 0;
            int nonzero = 0;
            for (int c = 0; c < 200000 && seen < 2; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l))
                                          & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        size_t off = (cur.size() > 17 && cur[12] == 0x81
                                      && cur[13] == 0x00) ? 4 : 0;
                        if (cur.size() >= 86 + off && cur[12+off] == 0x22
                            && cur[13+off] == 0xF0 && cur[14+off] == 0x02
                            && ((cur[24+off] << 8) | cur[25+off]) == 0) {
                            seen++;
                            for (int s = 0; s < 12; s++) {
                                size_t o = 38 + off + 4*s;
                                uint32_t v = ((uint32_t)cur[o]   << 16) |
                                             ((uint32_t)cur[o+1] <<  8) |
                                              (uint32_t)cur[o+2];
                                if (v) nonzero++;
                                for (int j = 0; j < 12; j++)
                                    if (v && lb_smp(j) == v) leaked++;
                            }
                        }
                        cur.clear();
                    }
                }
                hi();
            }
            printf("         (unmapped slot: %d talker-0 PDU(s) seen)\n", seen);
            ck("lb: an UNMAPPED loop slot carries no rx audio", leaked, 0);
            ck("lb: unmapping a slot never stops talker 0 framing", seen, 2);
            ck("lb: and what it frames instead is silence", nonzero, 0);
        }

        axi_write(A_CHMAP_CTRL, 0x0);            // restore the legacy path
    }

#ifdef AAF_PB_TB
    // ==================================================================
    //  [T66] RUNTIME dynamic-output-map writes REACH THE CROSSBAR RAM
    //  (t532 silicon 2026-08-09). On the wire the capture crossbar kept
    //  framing its BOOT image byte-identically across three different
    //  store states: runtime ADD/REMOVE_AUDIO_MAPPINGS commits reached
    //  the AECP store (GET_AUDIO_MAP tracked every edit) but landed in
    //  the fabric RAM erratically or not at all. No desk leg ever read
    //  the RAM SIDE back after a runtime AECP edit - the seeder had
    //  coverage (the 0x002C boot check above), the command path had
    //  none. This leg is that pin, end to end and RAM-side:
    //    * N spaced ADD_AUDIO_MAPPINGS through the REAL RX path,
    //    * after EACH, the crossbar RAM word read back via the CSR
    //      0x910/0x914 window (the RAM's own read port - not the store),
    //    * the store agreeing via GET_AUDIO_MAP,
    //    * a REMOVE clearing exactly its key,
    //    * and a live-audio proof: remapping talker 0's two wire
    //      channels to the TONE cluster changes the emitted payload.
    //  DELIBERATELY run with CHMAP_CTRL[0] = 0: since 0x002C the AECP
    //  mirror is the canonical programmer and its write arm must not
    //  depend on the bring-up debug bit (the write-gate half of the
    //  always-live law; the READ-mux half is the boot check above).
    // ==================================================================
    printf("-- [T66] runtime ADD/REMOVE_AUDIO_MAPPINGS -> crossbar RAM --\n");
    {
        enum { CMD_GET_AUDIO_MAP = 43, CMD_ADD_AUDIO_MAPPINGS = 44,
               CMD_REMOVE_AUDIO_MAPPINGS = 45 };
        const uint16_t DT_SPO = 0x000F;      // STREAM_PORT_OUTPUT
        static uint16_t sq = 0x4100;

        // capture-side crossbar RAM readback (CSR 0x904/0x910/0x914 window,
        // the 0x002C boot-seed recipe): returns the 13-bit map entry
        auto cap_ram = [&](int key) -> uint32_t {
            axi_write(0x904, 0x100 | key);
            axi_write(0x910, 1);
            uint32_t sv = 0;
            for (int g = 0; g < 64; g++) {
                sv = axi_read(0x910);
                if ((sv & 1) == 0) break;
            }
            uint32_t v = axi_read(0x914);
            if (((v >> 26) & 1) == 0) return 0xFFFFFFFFu;   // readback dead
            return v & 0x1FFF;
        };
        // one ADD/REMOVE of n {si, sc, co} rows on output port 0
        auto dmap_cmd = [&](int cmd, int n, const int* sc, const int* co)
            -> long {
            std::vector<uint8_t> pl = {
                (uint8_t)(DT_SPO >> 8), (uint8_t)DT_SPO, 0x00, 0x00,
                0x00, (uint8_t)n, 0x00, 0x00 };
            for (int i = 0; i < n; i++) {
                uint8_t row[8] = {0,0, 0,(uint8_t)sc[i], 0,(uint8_t)co[i], 0,0};
                pl.insert(pl.end(), row, row + 8);
            }
            auto r = aecp_xact((uint16_t)cmd, sq++, pl);
            return aecp_status(r);
        };
        // the generated CSRC template the fabric word must equal after an
        // ADD of cluster co (ring pool co 0..7 on this shape): src=3 RING,
        // half = co&1, idx = co/2, en forced by the commit
        auto ring_tpl = [&](int co) -> uint32_t {
            return 0x1300u | ((co & 1) << 11) | (co >> 1);
        };

        // ---- N spaced runtime ADDs, RAM-side readback after each -------
        const int scs[4] = {4, 5, 6, 7};
        const int cos[4] = {6, 7, 4, 5};     // cross-swap: != the boot image
        long all_success = 1, all_landed = 1;
        for (int i = 0; i < 4; i++) {
            if (dmap_cmd(CMD_ADD_AUDIO_MAPPINGS, 1, &scs[i], &cos[i]) != 0)
                all_success = 0;
            for (int c = 0; c < 3000; c++) step();   // SPACED, not a burst
            if (cap_ram(scs[i]) != ring_tpl(cos[i])) all_landed = 0;
        }
        ck("T66: 4 spaced runtime ADDs answered SUCCESS", all_success, 1);
        ck("T66: ALL 4 landed in the crossbar RAM (RAM-side read)",
           all_landed, 1);

        // ---- the store agrees (GET_AUDIO_MAP serves the SAME edits) ----
        {
            std::vector<uint8_t> pl = {
                (uint8_t)(DT_SPO >> 8), (uint8_t)DT_SPO, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00 };            // map_index 0
            auto r = aecp_xact(CMD_GET_AUDIO_MAP, sq++, pl);
            ck("T66: GET_AUDIO_MAP SUCCESS", aecp_status(r), 0);
            // rows at 50+8i: {si, sc, co, cc}; find sc 4..7, check co
            long rows_ok = (r.size() >= 50) ? 1 : 0;
            int found = 0;
            if (rows_ok) {
                int n = (r.size() > 47) ? r[47] : 0;
                for (int i = 0; i < n && 50 + 8*i + 7 < (int)r.size(); i++) {
                    int rsc = (r[50+8*i+2] << 8) | r[50+8*i+3];
                    int rco = (r[50+8*i+4] << 8) | r[50+8*i+5];
                    for (int k = 0; k < 4; k++)
                        if (rsc == scs[k]) { found++;
                            if (rco != cos[k]) rows_ok = 0; }
                }
            }
            ck("T66: the store carries all 4 edited rows", found, 4);
            ck("T66: store rows match the RAM-side clusters", rows_ok, 1);
        }

        // ---- REMOVE clears exactly its key, RAM-side ------------------
        {
            const int rsc = 4, rco = 6;
            ck("T66: REMOVE answered SUCCESS",
               dmap_cmd(CMD_REMOVE_AUDIO_MAPPINGS, 1, &rsc, &rco), 0);
            for (int c = 0; c < 3000; c++) step();
            ck("T66: removed key 4 cleared in the RAM", cap_ram(4), 0);
            ck("T66: neighbour key 5 untouched by the REMOVE",
               cap_ram(5), ring_tpl(7));
        }

        // ---- live-audio proof: tone onto talker 0's wire pair ----------
        // (keys 0/1 are talker 0's two wire channels at WIRE_CHANS=2; the
        // TONE cluster is co 8, template 0x1400, same value on both halves)
        {
            const int tsc[2] = {0, 1}, tco[2] = {8, 8};
            ck("T66: ADD tone onto ch0+ch1 SUCCESS",
               dmap_cmd(CMD_ADD_AUDIO_MAPPINGS, 2, tsc, tco), 0);
            for (int c = 0; c < 3000; c++) step();
            ck("T66: tone landed at key 0 (RAM-side)", cap_ram(0), 0x1400);
            ck("T66: tone landed at key 1 (RAM-side)", cap_ram(1), 0x1400);
            axi_write(0x6DC, 0x1);           // TONE_CTRL[0] = pilot on
            for (int c = 0; c < 30000; c++) step();   // let the walk emit it
            // capture one talker-0 PDU: payload nonzero, L==R per event
            std::vector<uint8_t> cur; std::vector<uint32_t> smp;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 200000 && smp.empty(); c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l))
                                          & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        size_t off = (cur.size() > 17 && cur[12] == 0x81
                                      && cur[13] == 0x00) ? 4 : 0;
                        if (cur.size() >= 86 + off && cur[12+off] == 0x22
                            && cur[13+off] == 0xF0 && cur[14+off] == 0x02
                            && ((cur[24+off] << 8) | cur[25+off]) == 0)
                            for (int s = 0; s < 12; s++) {
                                size_t o = 38 + off + 4*s;
                                smp.push_back(((uint32_t)cur[o]   << 16) |
                                              ((uint32_t)cur[o+1] <<  8) |
                                               (uint32_t)cur[o+2]);
                            }
                        cur.clear();
                    }
                }
                hi();
            }
            int nz = 0; long lr_eq = 1;
            for (size_t s = 0; s + 1 < smp.size(); s += 2) {
                if (smp[s]) nz++;
                if (smp[s] != smp[s+1]) lr_eq = 0;
            }
            // 6 sample events; the 48-entry 1 kHz table crosses zero at
            // most once in any 6-consecutive-sample window
            ck("T66: runtime-mapped tone REACHES the wire (payload live)",
               (long)(smp.size() == 12 && nz >= 4), 1);
            ck("T66: tone pair carries L == R (the TONE contract)", lr_eq, 1);
        }
    }

    // ==================================================================
    //  [T67] MEDIA-GRID CADENCE + TIMESTAMP TRACKING at the datapath
    //  level (t532 silicon 2026-08-09). The wire showed 123750 ns between
    //  6-sample PDUs - 48000 x 100/99 - where Milan 7.4 owes 125000 ns
    //  within +-50 ppm; 123750 = 6 x 2062.5 cycles x 10 ns and 2062.5 =
    //  99e6/48000, a media divider parameterized 99 MHz on a 100 MHz
    //  fabric. NOTHING at desk asserted the absolute rate (that is how it
    //  shipped), so this leg measures the SHIPPING grid end to end:
    //    * PDU-to-PDU spacing in fabric cycles over 8 epochs must equal
    //      8 x MILAN_CLK_FREQ_HZ x 6/48000 within the 50 ppm class bound
    //      (this build: 8 x 12500 exactly);
    //    * avtp_timestamp deltas must TRACK the PHC: equal to the PHC ns
    //      elapsed over those cycles at the LIVE PTP_INCR rate (read from
    //      0x504, Q8.24 - an earlier leg set 20 ns/tick), and after
    //      PTP_INCR is CSR-rewritten the deltas move with it - the
    //      integration half of the aaf [TSL] latch-not-adder pin.
    //  Runs on the [T66] tone stream: talker 0 framing continuously.
    // ==================================================================
    printf("-- [T67] media-grid cadence + avtp_timestamp PHC tracking --\n");
    {
        // collect K consecutive talker-0 PDUs: end-cycle stamps + ts
        auto collect_t0 = [&](int want) {
            std::vector<std::pair<long, uint32_t>> got;   // {cycle, ts}
            std::vector<uint8_t> cur;
            long c = 0;
            dut->m_axis_mac_tx_tready = 1;
            for (c = 0; c < 400000 && (int)got.size() < want; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l))
                                          & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        size_t off = (cur.size() > 17 && cur[12] == 0x81
                                      && cur[13] == 0x00) ? 4 : 0;
                        if (cur.size() >= 86 + off && cur[12+off] == 0x22
                            && cur[13+off] == 0xF0 && cur[14+off] == 0x02
                            && ((cur[24+off] << 8) | cur[25+off]) == 0) {
                            // avtp_timestamp = AVTP hdr +12: frame 26+off
                            uint32_t ts =
                                ((uint32_t)cur[26+off] << 24) |
                                ((uint32_t)cur[27+off] << 16) |
                                ((uint32_t)cur[28+off] <<  8) |
                                 (uint32_t)cur[29+off];
                            got.push_back({c, ts});
                        }
                        cur.clear();
                    }
                }
                hi();
            }
            return got;
        };

        const long EPOCH_CYC = 12500;        // MILAN_CLK 100e6 x 6/48000
        // the LIVE PHC rate (Q8.24 integer-ns; the ptp leg set 20 ns/tick)
        uint32_t incr0 = axi_read(0x504);
        long ns_cyc0 = (long)(incr0 >> 24);
        ck("T67: PTP_INCR is a whole-ns rate (Q8.24 frac 0)",
           incr0 & 0xFFFFFF, 0);
        auto p = collect_t0(9);
        ck("T67: talker 0 delivered 9 consecutive PDUs", (long)p.size(), 9);
        if (p.size() == 9) {
            long span = p[8].first - p[0].first;
            long lim  = (8 * EPOCH_CYC) / 20000 + 1;     // the 50 ppm class
            long err  = span - 8 * EPOCH_CYC;
            if (err < 0) err = -err;
            printf("         span 8 epochs = %ld cycles (nominal %ld, err %ld)\n",
                   span, 8 * EPOCH_CYC, err);
            ck("T67: PDU cadence = 48 kHz on MILAN_CLK within 50 ppm",
               err <= lim, 1);
            long d_ok = 1;
            for (int i = 1; i < 9; i++) {
                long d = (long)(uint32_t)(p[i].second - p[i-1].second);
                if (d != EPOCH_CYC * ns_cyc0) d_ok = 0;
                if (d != EPOCH_CYC * ns_cyc0)
                    printf("         ts delta %d = %ld ns (owed %ld)\n",
                           i, d, EPOCH_CYC * ns_cyc0);
            }
            ck("T67: ts deltas = PHC elapsed per epoch (12500 x INCR ns)",
               d_ok, 1);
            ck("T67: and NOT the t532 wire constant 123750",
               (long)(uint32_t)(p[1].second - p[0].second) == 123750, 0);
        } else { for (int k = 0; k < 3; k++) ck("T67 (skipped)", 0, 1); }

        // PHC warp via the ARCHITECTED CSR: PTP_INCR 0x504 moved ->
        // the deltas move with it (latched from the live PHC, never
        // synthesized; a ts += CONST adder reddens exactly this check)
        axi_write(0x504, 0x10000000);        // 16.0 ns per PHC tick
        collect_t0(3);                       // flush epochs straddling it
        auto w = collect_t0(5);
        long w_ok = (w.size() == 5) ? 1 : 0;
        for (size_t i = 1; i < w.size(); i++) {
            long d = (long)(uint32_t)(w[i].second - w[i-1].second);
            if (d != EPOCH_CYC * 16) w_ok = 0;
            if (d != EPOCH_CYC * 16)
                printf("         warp ts delta %zu = %ld ns (owed %ld)\n",
                       i, d, EPOCH_CYC * 16);
        }
        ck("T67: PTP_INCR rewrite moves the ts deltas (latch tracks PHC)",
           w_ok, 1);
        axi_write(0x504, incr0);             // restore the leg-entry PHC rate

        // [T66]/[T67] cleanup: tone off, tone mappings REMOVEd (store AND
        // RAM back to the loop-leg parting state: keys 0/1 dark)
        axi_write(0x6DC, 0x0);
        {
            enum { CMD_REMOVE_AUDIO_MAPPINGS = 45 };
            const uint16_t DT_SPO = 0x000F;
            std::vector<uint8_t> pl = {
                (uint8_t)(DT_SPO >> 8), (uint8_t)DT_SPO, 0x00, 0x00,
                0x00, 0x02, 0x00, 0x00,
                0,0, 0,0, 0,8, 0,0,          // {si 0, sc 0, co 8, cc 0}
                0,0, 0,1, 0,8, 0,0 };        // {si 0, sc 1, co 8, cc 0}
            auto r = aecp_xact(45, 0x4180, pl);
            ck("T67: cleanup REMOVE of the tone rows SUCCESS",
               aecp_status(r), 0);
        }
    }
#endif

#ifdef LOOPBACK_TB
    // ==================================================================
    //  [T68] LOOP SOURCE SEQUENCE FIDELITY - the stair-step measurement
    //  (user audio capture 2026-08-09: direct reception clean at ppm-
    //  class, loop reception 9895 glitches/s on the 6-sample PDU lattice
    //  with 8000 +/- 1000 Hz sidebands). Mechanism, in this RTL: the LOOP
    //  bucket is a LATEST-SAMPLE hold (lb_hold_r) - each received PDU
    //  bursts 6 samples per channel into it at wire speed, the media-tick
    //  walk then reads it 6 times before the next PDU, so the wire gets
    //  ~6 copies of each block's LAST sample and skips the other 5: a
    //  duplicate+skip stair on exactly the measured lattice. That WAS the
    //  documented slip policy doing what it says - correct for the
    //  once-per-sample front-end sources, WRONG for the bursty PDU
    //  source. VERSION 0x0036 landed the fix: a per-pair elastic queue
    //  (depth 8 = one PDU + margin) popped once per media tick - paced,
    //  in-order sequence replay with honest bounded slip (empty tick =
    //  repeat last + dup counted, full push = drop OLDEST + skip
    //  counted; both ZERO at lock). LB_SEQ_FIXED (the Makefile defines
    //  it for this leg) asserts that law; the pre-fix stair measured
    //  76 dup / 56 skip on this ramp.
    // ==================================================================
    printf("-- [T68] loop sequence fidelity vs a paced RAMP --\n");
    {
        enum { A_CHMAP_CTRL = 0x900, A_CHMAP_SEL = 0x904,
               A_CHMAP_WORD = 0x908 };
        const int LB_SID = 1;                // sidB is stream 1
        const int M = 10;                    // paced PDUs (60 ch0 samples)

        // talker 0's pair <- LOOP {stream 1, pair 0} via the debug window
        // (the AECP path is [T66]'s; this shape's generated LOOP templates
        // are en=0 = not-fabric-backed, so the canonical programmer rightly
        // refuses them and the bring-up window is the honest way in)
        axi_write(A_CHMAP_CTRL, 0x1);
        for (int k = 0; k < 2; k++) {
            axi_write(A_CHMAP_SEL, 0x100 | k);
            axi_write(A_CHMAP_WORD, (uint32_t)(0x8000 | (5 << 12)
                                               | ((k & 1) << 8)
                                               | (LB_SID << 4) | 0));
        }

        // paced RX: one 6-sample 2ch PDU per 12500 cycles (the media rate),
        // ch0 samples globally DISTINCT: PDU k sample s = tuple(48k + 4s)
        auto rx_pdu_beats = [&](uint8_t seq, uint8_t seed) {
            static std::vector<uint64_t> beats;
            const uint8_t* f = mkaaf(sidB, seq, 2, seed);
            beats.clear();
            for (size_t bt = 0; bt < (86 + 7) / 8; bt++) {
                uint64_t v = 0;
                for (int j = 0; j < 8; j++)
                    if (bt*8 + j < 86) v |= (uint64_t)f[bt*8+j] << (8*j);
                beats.push_back(v);
            }
            return beats;
        };

        // ACCEPTANCE WARM-UP, not graded: stream 1 has been dark since
        // task #65 (T66/T67 ran the tone), so the RX monitor's re-lock /
        // re-accept eats the first PDUs UPSTREAM of the crossbar - the
        // depacketizer forwards nothing and the queue honestly starves.
        // That behaviour belongs to the monitor's own legs and counters;
        // THIS leg grades the LOOP SOURCE's pacing, so it measures on a
        // stream the depacketizer is already forwarding. The warm-up
        // payload family is seed 0xE2 + 4j: every sample's top byte is
        // 2 mod 4, while every graded ramp value's is 0 mod 4 - residue
        // and ramp are distinguishable BY CONSTRUCTION for the stripper.
        {
            std::vector<uint64_t> beats; size_t bi = 0; int fed = 0;
            for (long c = 0; c < 6 * 12500L; c++) {
                if (c % 12500 == 0 && fed < 6) {
                    beats = rx_pdu_beats((uint8_t)(140 + fed),
                                         (uint8_t)(0xE2 + 4 * fed));
                    bi = 0; fed++;
                }
                //! WIRE-PACED beats (one 8-byte beat per 8 cycles, the GbE
                //! byte rate): the accept verdict is a multi-cycle serial
                //! walk and the depacketizer drops a frame whose verdict
                //! misses its tlast - real frames last >= 88 byte-times, a
                //! 1-beat-per-cycle firehose is 8x faster than any wire
                //! and starves the verdict window instead of the DUT
                if (bi < beats.size() && (c & 7) == 0) {
                    dut->s_axis_mac_rx_tdata  = beats[bi];
                    dut->s_axis_mac_rx_tkeep  = 0xFF;
                    dut->s_axis_mac_rx_tvalid = 1;
                    dut->s_axis_mac_rx_tlast  = (bi == beats.size()-1);
                } else {
                    dut->s_axis_mac_rx_tvalid = 0;
                    dut->s_axis_mac_rx_tlast  = 0;
                }
                lo();
                bool wacc = dut->s_axis_mac_rx_tvalid
                            && dut->s_axis_mac_rx_tready;
                hi();
                if (wacc) bi++;
            }
            dut->s_axis_mac_rx_tvalid = 0;
        }
        // the queue's own drop-oldest evidence, graded by DELTA over the
        // paced window below (dup stays un-graded here: OTHER fed pairs
        // starve legitimately while only stream 1 is fed)
        long lbq_skip0 =
            (long)dut->rootp->milan_datapath__DOT__lb_skip_cnt_w;
        auto tuple24 = [&](int b0) -> uint32_t {
            return ((uint32_t)(uint8_t)(b0)     << 16)
                 | ((uint32_t)(uint8_t)(b0 + 1) <<  8)
                 |  (uint32_t)(uint8_t)(b0 + 2);
        };
        // expected ch0 sequence: 6 per PDU (payload samples 0,2,..,10)
        std::vector<uint32_t> expect;
        for (int k = 0; k < M; k++)
            for (int s = 0; s < 12; s += 2)
                expect.push_back(tuple24(48*k + 4*s));

        // drive M paced PDUs while capturing talker-0 ch0 output
        std::vector<uint32_t> emitted;
        {
            std::vector<uint8_t> cur;
            std::vector<uint64_t> beats; size_t bi = 0; int fed = 0;
            dut->m_axis_mac_tx_tready = 1;
            for (long c = 0; c < (long)M * 12500 + 40000; c++) {
                if (c % 12500 == 0 && fed < M) {
                    // seq continues the warm-up run (146 onward): the graded
                    // window must not open on a seq-mismatch of its own
                    beats = rx_pdu_beats((uint8_t)(146 + fed),
                                         (uint8_t)(48 * fed));
                    fed++; bi = 0;
                }
                //! wire-paced beats - same rule as the warm-up loop above
                if (bi < beats.size() && (c & 7) == 0) {
                    dut->s_axis_mac_rx_tdata  = beats[bi];
                    dut->s_axis_mac_rx_tkeep  = 0xFF;
                    dut->s_axis_mac_rx_tvalid = 1;
                    dut->s_axis_mac_rx_tlast  = (bi == beats.size()-1);
                } else {
                    dut->s_axis_mac_rx_tvalid = 0;
                    dut->s_axis_mac_rx_tlast  = 0;
                }
                lo();
                bool in_acc = dut->s_axis_mac_rx_tvalid
                              && dut->s_axis_mac_rx_tready;
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l))
                                          & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        size_t off = (cur.size() > 17 && cur[12] == 0x81
                                      && cur[13] == 0x00) ? 4 : 0;
                        if (cur.size() >= 86 + off && cur[12+off] == 0x22
                            && cur[13+off] == 0xF0 && cur[14+off] == 0x02
                            && ((cur[24+off] << 8) | cur[25+off]) == 0)
                            for (int s = 0; s < 12; s += 2) {
                                size_t o = 38 + off + 4*s;
                                emitted.push_back(
                                    ((uint32_t)cur[o]   << 16) |
                                    ((uint32_t)cur[o+1] <<  8) |
                                     (uint32_t)cur[o+2]);
                            }
                        cur.clear();
                    }
                }
                hi();
                if (in_acc) bi++;
            }
            dut->s_axis_mac_rx_tvalid = 0;
        }

        // strip the pre-ramp residue: silence fill (legal 5.3.7.3) and the
        // warm-up family (top byte 2 mod 4, disjoint from the ramp's
        // 0 mod 4). FIFO order guarantees no warm-up sample can appear
        // after the first ramp sample, so a leading strip is exact.
        while (!emitted.empty() && (emitted.front() == 0
                || ((emitted.front() >> 16) & 3) == 2))
            emitted.erase(emitted.begin());
        ck("T68: loop output collected against the paced ramp",
           emitted.size() >= 24, 1);

        // walk the expected sequence: membership, order, dups, skips. The
        // graded window ends the moment the whole ramp has been matched:
        // the feed stopped there, so everything after it is the queue law's
        // honest starved tail - it must be a pure repeat of the LAST sample
        // (the bounded-slip rule), graded separately below.
        long dups = 0, skips = 0, alien = 0, order_ok = 1;
        long tail_bad = 0; size_t matched = 0;
        {
            size_t p = 0; long last = -1;
            for (uint32_t v : emitted) {
                if (p == expect.size()) {
                    if (v != expect.back()) tail_bad++;
                    continue;
                }
                size_t q = p;
                while (q < expect.size() && expect[q] != v) q++;
                if (q == expect.size()) {
                    if (last >= 0 && v == expect[last]) { dups++; continue; }
                    // not ahead of the cursor: behind it = reordering
                    bool behind = false; size_t b = 0;
                    for (; b < p; b++) if (expect[b] == v) { behind = true; break; }
                    if (behind) order_ok = 0; else alien++;
                    continue;
                }
                skips += (long)(q - p);
                last = (long)q; p = q + 1;
            }
            matched = p;
        }
        printf("         emitted %zu ch0 samples vs %zu sent: "
               "%ld dup, %ld skipped, %ld alien, %ld bad tail\n",
               emitted.size(), expect.size(), dups, skips, alien, tail_bad);
        ck("T68: every loop sample is one the listener received", alien, 0);
        ck("T68: received order is preserved (no reordering)", order_ok, 1);
#ifdef LB_SEQ_FIXED
        // the paced-replay law (0x0036 queue rework): every received sample
        // exactly once, in order, and the post-feed tail repeats the final
        // sample only. The pre-rework latest-sample hold measured 76 dup /
        // 56 skip on this very ramp (the audible defect C stair).
        ck("T68: ZERO duplicated samples through the loop", dups, 0);
        ck("T68: ZERO skipped samples through the loop", skips, 0);
        ck("T68: the WHOLE ramp came through", (long)matched,
           (long)expect.size());
        ck("T68: post-feed tail = the final sample repeated (bounded slip)",
           tail_bad, 0);
        //! the module's own drop evidence agrees: rate-matched pacing never
        //! filled a queue, so drop-oldest never fired anywhere
        ck("T68: queue skip counter delta 0 over the paced window",
           (long)dut->rootp->milan_datapath__DOT__lb_skip_cnt_w - lbq_skip0,
           0);
#endif

        // parting state = the loop leg's: keys dark, window disarmed
        for (int k = 0; k < 2; k++) {
            axi_write(A_CHMAP_SEL, 0x100 | k);
            axi_write(A_CHMAP_WORD, 0x0000);
        }
        axi_write(A_CHMAP_CTRL, 0x0);
    }
#endif

    // ==================================================================
    //  THE SRP FABRIC LAUNCH STAGE CYCLE CONTRACT  (2026-08-02)
    //
    //  Timing closure moved the ctx write one register behind the arbiter:
    //  the LAUNCH beat captures the granted slot's record and retires the
    //  requester; the KL_lwsrp_ctx row write lands on the q's own service
    //  beat, >= 1 cycle later. This block pins that contract at CYCLE
    //  resolution (the ms-scale suites above cannot see a one-cycle skew):
    //
    //   (a) +1 LANDING: on the very beat a requester retires, the ctx row
    //       is NOT yet written; it lands within 4 cycles. Reverting to the
    //       same-cycle combinational feed makes the row appear ON the
    //       retire beat, which this check refuses.
    //   (b) FRESH COHERENCE: row_fresh rises on the SAME edge as the row
    //       write (both live inside KL_lwsrp_ctx), never on the retire
    //       beat and never a cycle apart from the write.
    //   (c) NO DOUBLE-GRANT / NOTHING LOST: over the whole burst the count
    //       of fabric ctx write beats (srp_fab_own_r pulses) EQUALS the
    //       count of requester retire edges - each retire buys exactly one
    //       write. Breaking the q hold (recapture over an in-flight
    //       record) makes writes outnumber retires.
    //   (d) SERIALIZATION: back-to-back requesters (every talker armed by
    //       ONE enable commit) drain one per q turnaround - two writes
    //       never land on adjacent beats.
    //
    //  The probes are FLOPS (Verilator keeps them): requester req_r
    //  vectors, srp_fab_own_r, and the ctx valid_r/row_fresh state.
    // ==================================================================
    printf("-- SRP fabric launch stage: cycle contract (+1, coherent) --\n");
    {
        enum { A_CRFT_CTRL = 0x750 };
        auto* rp = dut->rootp;
        // quiesce: engine off (rows clear, requesters settle), CRF want
        // off, window poll parked OFF so the port timing is bare
        axi_write(A_LWSRP_CTRL, 0x0);
        axi_write(A_CRFT_CTRL, 0x0);
        axi_write(A_STRM_SEL, 0);
        for (int c = 0; c < 4000; c++) step();
        ck("launch: talker requesters idle before the trigger",
           rp->milan_datapath__DOT__aafsrp_req_r, 0);
        ck("launch: no captured record in flight",
           rp->milan_datapath__DOT__srp_fab_qv_r, 0);
        ck("launch: every ctx row invalid",
           (unsigned)rp->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r,
           0);

        // trigger: ONE commit arms every talker requester at once. The
        // commit lands DURING the write's own AXI cycles, so the handshake
        // is stepped RAW and the per-cycle probe runs across it.
        // [5] = the declare bypass: this white-box case is about the LAUNCH
        // PIPELINE arming every requester on one commit, so it runs the
        // declared-at-boot posture the 4.3.3.1 gate otherwise forbids.
        dut->s_axi_awaddr = A_LWSRP_CTRL; dut->s_axi_awvalid = 1;
        dut->s_axi_wdata = 0x37; dut->s_axi_wvalid = 1;
        dut->s_axi_wstrb = 0xF; dut->s_axi_bready = 1;

        const int W = 1500;
        int  t_ret[NSTREAMS_TB], t_wr[NSTREAMS_TB], ret_edges[NSTREAMS_TB];
        int  val_at_ret[NSTREAMS_TB], fresh_rose_with_wr[NSTREAMS_TB];
        for (int t = 0; t < NSTREAMS_TB; t++) {
            t_ret[t] = -1; t_wr[t] = -1; ret_edges[t] = 0;
            val_at_ret[t] = -1; fresh_rose_with_wr[t] = -1;
        }
        long own_pulses = 0, total_retires = 0;
        int  own_adjacent = 0, own_prev = 0;
        unsigned prev_aaf = rp->milan_datapath__DOT__aafsrp_req_r;
        unsigned prev_lsn = rp->milan_datapath__DOT__lsnsrp_req_r;
        unsigned prev_crf = rp->milan_datapath__DOT__crf_srp_req_r;
        unsigned prev_val =
            (unsigned)rp->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r;
        unsigned prev_fr =
            (unsigned)rp->milan_datapath__DOT__lwsrp__DOT__row_fresh_w;
        bool aw_done = false, b_done = false;
        for (int c = 0; c < W; c++) {
            if (!aw_done) {
                dut->eval();
                if (dut->s_axi_awready && dut->s_axi_wready) aw_done = true;
            }
            step();
            if (aw_done && dut->s_axi_awvalid) {
                dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
            }
            if (aw_done && !b_done && dut->s_axi_bvalid) b_done = true;

            unsigned aaf = rp->milan_datapath__DOT__aafsrp_req_r;
            unsigned lsn = rp->milan_datapath__DOT__lsnsrp_req_r;
            unsigned crf = rp->milan_datapath__DOT__crf_srp_req_r;
            unsigned val = (unsigned)
                rp->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r;
            unsigned fr  = (unsigned)
                rp->milan_datapath__DOT__lwsrp__DOT__row_fresh_w;
            int own = rp->milan_datapath__DOT__srp_fab_own_r;

            if (own) { own_pulses++; if (own_prev) own_adjacent++; }
            own_prev = own;
            for (int b = 0; b < NSTREAMS_TB; b++) {
                if ((prev_aaf >> b) & 1 && !((aaf >> b) & 1)) total_retires++;
            }
            //! the listener requester carries one lane per ACMP sink INCL
            //! the appended CRF sink (task #27) - its earlier bind is still
            //! standing, so the engine re-arm rewrites its row too and the
            //! grant/retire ledger must count that lane or 5 != 4
            for (int b = 0; b < NSTREAMS_TB + 1; b++) {
                if ((prev_lsn >> b) & 1 && !((lsn >> b) & 1)) total_retires++;
            }
            if ((prev_crf & 1) && !(crf & 1)) total_retires++;

            for (int t = 1; t < NSTREAMS_TB; t++) {
                const int lane = (NSTREAMS_TB - 1) + t - 1;
                if (((prev_aaf >> t) & 1) && !((aaf >> t) & 1)) {
                    ret_edges[t]++;
                    if (t_ret[t] < 0) {
                        t_ret[t] = c;
                        val_at_ret[t] = (val >> lane) & 1;
                    }
                }
                if (t_wr[t] < 0 && !((prev_val >> lane) & 1) &&
                    ((val >> lane) & 1)) {
                    t_wr[t] = c;
                    fresh_rose_with_wr[t] =
                        !((prev_fr >> lane) & 1) && ((fr >> lane) & 1);
                }
            }
            prev_aaf = aaf; prev_lsn = lsn; prev_crf = crf;
            prev_val = val; prev_fr = fr;
        }
        dut->s_axi_bready = 0;

        char nm[96];
        for (int t = 1; t < NSTREAMS_TB; t++) {
            snprintf(nm, sizeof nm, "launch t%d: retired exactly once", t);
            ck(nm, ret_edges[t], 1);
            snprintf(nm, sizeof nm,
                     "launch t%d: row NOT yet written on the retire beat", t);
            ck(nm, val_at_ret[t], 0);
            snprintf(nm, sizeof nm,
                     "launch t%d: write landed 1..4 beats after retire", t);
            ck(nm, t_wr[t] > t_ret[t] && t_wr[t] - t_ret[t] <= 4, 1);
            snprintf(nm, sizeof nm,
                     "launch t%d: row_fresh rose WITH the write beat", t);
            ck(nm, fresh_rose_with_wr[t], 1);
        }
        ck("launch: one ctx write per retire (no double-grant, none lost)",
           own_pulses, total_retires);
        ck("launch: retires happened at all", total_retires >= NSTREAMS_TB - 1,
           1);
        ck("launch: writes never land on adjacent beats", own_adjacent, 0);
        ck("launch: all talker requesters drained",
           rp->milan_datapath__DOT__aafsrp_req_r, 0);
        ck("launch: pick stage idle after the burst",
           rp->milan_datapath__DOT__srp_fab_pv_r, 0);
        // the identity-root shadow latches on the CAPTURE beat from the
        // same wires the record mux samples - so it must equal the MAC
        // half of what the rows were actually written with
        {
            const int lane1 = NSTREAMS_TB - 1;         // talker 1's lane
            uint64_t sid1 = (uint64_t)
                rp->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                    [2 * lane1] |
                ((uint64_t)
                 rp->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                     [2 * lane1 + 1] << 32);
            ck("launch: root shadow == the row's MAC half (same-edge latch)",
               (uint64_t)rp->milan_datapath__DOT__aafsrp_mac_r ==
                   (sid1 >> 16), 1);
        }

        // ---- SOFTWARE WINS OVER AN IN-FLIGHT CAPTURE (the qkill) -------
        // The one-cycle overlap - a 0x800 window WRITE serviced while the
        // fabric's captured record for the SAME row is in flight - cannot
        // be staged through the sequential AXI BFM (its commits are >= 3
        // cycles apart), so the overlap is FAULT-INJECTED at the flops:
        // re-arm talker 1's requester directly, then land a window write
        // commit (the CSR master's own staged-commit flops) d cycles
        // later. Raw pokes become visible to the cached combinational
        // regions one eval late, so d is SWEPT until the true overlap is
        // hit. Detection is flop-based and latency-immune:
        //   pick     = a srp_fab_pv_r rising edge (the retire beat)
        //   write    = a srp_fab_own_r pulse (only fabric ctx writes)
        //   KILL     = a pick with NO write - a squash at either stage
        //              (pkill in the pick stage, qkill in the capture q).
        // The invariant holds at EVERY phase: software's sid is what the
        // row carries once the dust settles; and at least one phase must
        // actually exercise a squash.
        {
            const int      T    = 1;
            const int      LANE = (NSTREAMS_TB - 1) + T - 1;
            const uint64_t SWSID = 0x1122334455667788ULL;
            auto lane_sid = [&]() -> uint64_t {
                return (uint64_t)
                    rp->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                        [2 * LANE] |
                    ((uint64_t)
                     rp->milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                         [2 * LANE + 1] << 32);
            };
            const uint64_t fab_sid = lane_sid();   // the derived {mac, uid}
            ck("qkill: row starts fabric-owned (derived sid)",
               fab_sid != 0 && fab_sid != SWSID, 1);
            int kills = 0, sid_wins = 0, retakes = 0;
            const int SWEEP = 5;
            for (int d = 0; d < SWEEP; d++) {
                // re-arm the requester (flop poke = a want re-declare)
                rp->milan_datapath__DOT__aafsrp_req_r |= (1u << T);
                for (int c = 0; c < d; c++) step();
                // ...and the window write commit for the SAME row
                rp->milan_datapath__DOT__csr__DOT__srp_wr_pend_r  = 1;
                rp->milan_datapath__DOT__csr__DOT__srp_wr_row_r   =
                    (NSTREAMS_TB - 1) + T;
                rp->milan_datapath__DOT__csr__DOT__srp_wr_dir_r   = 0;
                rp->milan_datapath__DOT__csr__DOT__srp_wr_valid_r = 1;
                rp->milan_datapath__DOT__csr__DOT__srp_wr_sid_r   = SWSID;
                rp->milan_datapath__DOT__csr__DOT__srp_wr_dmac_r  = 0;
                int picks = 0, wrs = 0, pv_prev =
                    rp->milan_datapath__DOT__srp_fab_pv_r;
                for (int c = 0; c < 40; c++) {
                    step();
                    int pv = rp->milan_datapath__DOT__srp_fab_pv_r;
                    if (pv && !pv_prev) picks++;
                    pv_prev = pv;
                    if (rp->milan_datapath__DOT__srp_fab_own_r) wrs++;
                }
                if (picks > wrs) kills++;
                if (lane_sid() == SWSID) sid_wins++;
                // release: a commit naming NO sid hands the row back
                axi_write(A_STRM_SEL, 0x100 + T);
                axi_write(A_SW_SID_LO, 0);
                axi_write(A_SW_SID_HI, 0);
                axi_write(A_SW_CTRL, (2u << 5) | (4u << 1) | 1u);
                axi_write(A_STRM_SEL, 0);
                for (int c = 0; c < 200; c++) step();
                if (lane_sid() == fab_sid) retakes++;
            }
            ck("qkill: SOFTWARE's sid wins at EVERY overlap phase",
               sid_wins, SWEEP);
            ck("qkill: the in-flight squash was exercised (>= 1 phase)",
               kills >= 1, 1);
            ck("qkill: the fabric retook the row after every release",
               retakes, SWEEP);
        }

        axi_write(A_LWSRP_CTRL, 0x0);
        for (int c = 0; c < 512; c++) step();
    }


    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
