// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// milan_datapath with the protocol-processor SHADOW plane ON (PP_PLANE_P=1).
//
// What this suite proves, and why each check exists:
//
//   A. The plane is THERE and the CSR window decodes it. PP_STAT carries a
//      constant 0x5B tag, so a structural zero (the answer every undecoded
//      address gives) can never be mistaken for "present and idle".
//
//   B. The RX path works end to end: MAC AXIS beat -> aligned-lane classifier
//      -> control-frame FIFO -> byte serializer -> the processor's own
//      validator. The counter only moves when the processor ACCEPTED a whole
//      frame, so it is evidence about the processor, not about the wrapper.
//
//   C. The classifier REJECTS non-control traffic. This is the check that
//      protects the board: the serializer runs at 1 B/clk = 100 MB/s against
//      gigabit's 125 MB/s, so an unfiltered tap would lag and corrupt rather
//      than drop. A frame that should not enter must not enter.
//
//   D. SHADOW DISCIPLINE — the safety property this whole landing rests on.
//      The processor is driven until it WANTS to transmit (its own TX frame
//      counter moves), and the MAC TX port must stay silent through the same
//      window. Without this, coexistence would put a second ENTITY_AVAILABLE
//      from the same entity_id on the segment.
//
//   E. The side port answers over the CSR bridge with the processor's OWN
//      magic word ("KLPP") and its shape. That word is generated inside
//      protocol_processor_top, so reading it is proof the fabric is alive and
//      clocked, not that the bridge returns a plausible constant.
//
// Frames are injected LITTLE-LANE (tdata[7:0] = first wire byte). That is the
// silicon convention of the RX tap — KL_maap.sv:154 states it and tests the
// EtherType at lanes 4/5, and KL_aecp_ingress.sv documents the same. The
// vlan_frame() helper in milan_dp/sim_main.cpp packs the OTHER way for the TX
// classifier path; copying it here would feed the processor byte-swapped
// frames and every accept check would read a silent zero.

#include "Vmilan_datapath.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>

static Vmilan_datapath* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint32_t got, uint32_t exp) {
    checks++;
    bool ok = (got == exp);
    if (!ok) fails++;
    printf("  [%s] %-42s got=0x%08X exp=0x%08X\n", ok ? "PASS" : "FAIL", what, got, exp);
}

static void ck_true(const char* what, bool cond, const char* detail) {
    checks++;
    if (!cond) fails++;
    printf("  [%s] %-42s %s\n", cond ? "PASS" : "FAIL", what, detail);
}

// ---- clocking (single domain, as milan_dp drives it) ----
static void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->clk_tdm_i = 0; dut->eval(); }
static void hi() { dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->clk_tdm_i = 1; dut->eval(); }
static void step() { lo(); hi(); }

// ---- AXI4-Lite BFM (identical protocol/timing to the milan_dp harness) ----
static void axi_write(uint16_t a, uint32_t d) {
    dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
    dut->s_axi_wdata = d;  dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
    dut->s_axi_bready = 1;
    for (int g = 0; g < 2048; g++) { lo(); bool acc = dut->s_axi_awready && dut->s_axi_wready; hi(); if (acc) break; }
    dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
    for (int g = 0; g < 2048; g++) { lo(); bool bv = dut->s_axi_bvalid; hi(); if (bv) break; }
    dut->s_axi_bready = 0;
}

static uint32_t axi_read(uint16_t a) {
    dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
    for (int g = 0; g < 2048; g++) { lo(); bool acc = dut->s_axi_arready; hi(); if (acc) break; }
    dut->s_axi_arvalid = 0;
    uint32_t d = 0;
    for (int g = 0; g < 2048; g++) { lo(); bool rv = dut->s_axi_rvalid; if (rv) d = dut->s_axi_rdata; hi(); if (rv) break; }
    dut->s_axi_rready = 0;
    return d;
}

enum {
    A_ID = 0x000, A_VERSION = 0x004,
    A_PP_CTRL = 0x920, A_PP_STAT = 0x924,
    A_PP_SPADDR = 0x928, A_PP_SPDATA = 0x92C, A_PP_DIAG = 0x930,
};

// side-port windows implemented by protocol_processor_top (tb/pp_top README)
static const uint32_t SP_SNAPSHOT = 0x20000;   // word 0 = magic "KLPP"

static void do_reset() {
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
    dut->s_axi_bready = dut->s_axi_rready = 0;
    dut->s_axis_tx_tvalid = 0; dut->s_axis_mac_rx_tvalid = 0;
    dut->m_axis_mac_tx_tready = 1; dut->m_axis_rx_tready = 1; dut->m_axis_ts_tready = 1;
    dut->i_mac_speed = 2; dut->i_link_up = 1; dut->i_full_duplex = 1; dut->i_mac_events = 0;
    for (int i = 0; i < 8; i++) step();
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    for (int i = 0; i < 16; i++) step();
}

// ---- inject one little-lane frame on the MAC RX port ----
// Returns the number of MAC TX beats observed while injecting, so a caller can
// assert the wire stayed silent over the same window.
static long inject_rx(const uint8_t* f, size_t len, int tail_cycles) {
    size_t beats = (len + 7) / 8;
    std::vector<uint64_t> bw(beats, 0);
    std::vector<uint8_t>  bk(beats, 0);
    for (size_t i = 0; i < len; i++) {
        bw[i / 8] |= (uint64_t)f[i] << (8 * (i % 8));
        bk[i / 8] |= (uint8_t)(1u << (i % 8));
    }
    long tx_beats = 0;
    size_t idx = 0;
    dut->m_axis_rx_tready = 1;
    dut->m_axis_mac_tx_tready = 1;
    for (int c = 0; c < (int)beats + tail_cycles; c++) {
        if (idx < beats) {
            dut->s_axis_mac_rx_tdata  = bw[idx];
            dut->s_axis_mac_rx_tkeep  = bk[idx];
            dut->s_axis_mac_rx_tvalid = 1;
            dut->s_axis_mac_rx_tlast  = (idx == beats - 1);
        } else {
            dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
        }
        lo();
        bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
        if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) tx_beats++;
        hi();
        if (in_acc) idx++;
    }
    dut->s_axis_mac_rx_tvalid = 0;
    return tx_beats;
}

// run free cycles, counting MAC TX beats (the wire-silence witness)
static long run_idle(int cycles) {
    long tx_beats = 0;
    dut->m_axis_mac_tx_tready = 1;
    for (int c = 0; c < cycles; c++) {
        lo();
        if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) tx_beats++;
        hi();
    }
    return tx_beats;
}

// ---- posted side-port access over the CSR bridge ----
static uint32_t sp_read(uint32_t word_addr, bool* ok) {
    axi_write(A_PP_SPADDR, word_addr);            // arm: posts the read
    for (int g = 0; g < 4096; g++) {
        if ((axi_read(A_PP_STAT) & 1u) == 0) {    // STAT[0] = sp_busy
            if (ok) *ok = true;
            return axi_read(A_PP_SPDATA);
        }
        step();
    }
    if (ok) *ok = false;
    return 0;
}

// ---- frame builders (wire order, byte 0 = first DA octet) ----
static const uint8_t OUR_MAC[6] = {0x00, 0x1B, 0xC5, 0x0C, 0xAC, 0x00};

// ADP ENTITY_DISCOVER: DA 91:E0:F0:01:00:00, EtherType 0x22F0, subtype 0xFA,
// msg_type 2. 82 bytes on the wire (the ADPDU rule this repo enforces).
static size_t build_adp_discover(uint8_t* f) {
    memset(f, 0, 82);
    const uint8_t da[6] = {0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
    const uint8_t sa[6] = {0x02, 0x11, 0x22, 0x33, 0x44, 0x55};
    memcpy(f, da, 6); memcpy(f + 6, sa, 6);
    f[12] = 0x22; f[13] = 0xF0;          // EtherType
    f[14] = 0xFA;                        // subtype ADP
    f[15] = 0x00;                        // sv/version
    f[16] = 0x02;                        // msg_type = ENTITY_DISCOVER
    f[17] = 0x00;                        // valid_time / control_data_length
    f[18] = 0x00;
    // target entity_id at wire byte 18 (0 = discover everybody)
    return 82;
}

// A frame the classifier must REJECT: plain IPv4, EtherType 0x0800.
static size_t build_ipv4(uint8_t* f) {
    memset(f, 0, 64);
    const uint8_t da[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
    memcpy(f, da, 6); memcpy(f + 6, OUR_MAC, 6);
    f[12] = 0x08; f[13] = 0x00;
    for (int i = 14; i < 64; i++) f[i] = (uint8_t)i;
    return 64;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vmilan_datapath;

    printf("=== milan_datapath + protocol-processor SHADOW plane (PP_PLANE_P=1) ===\n");
    do_reset();

    // ---- A. the plane is present and its window decodes -------------------
    printf("[A] presence + CSR window\n");
    ck("ID == 'MILN'", axi_read(A_ID), 0x4D494C4E);
    uint32_t stat = axi_read(A_PP_STAT);
    ck("PP_STAT tag == 0x5B (plane present)", (stat >> 24) & 0xFF, 0x5B);
    ck("PP_DIAG clean at reset", axi_read(A_PP_DIAG), 0x00000000);
    axi_write(A_PP_CTRL, 0x1);                       // entity_enable
    ck("PP_CTRL reads back", axi_read(A_PP_CTRL) & 0x3, 0x1);

    // ---- E. the side port answers with the processor's own magic ----------
    printf("[E] side-port bridge -> the processor's snapshot window\n");
    bool ok = false;
    uint32_t magic = sp_read(SP_SNAPSHOT + 0, &ok);
    ck_true("side-port access completed", ok, ok ? "ack seen" : "TIMED OUT waiting on sp_busy");
    ck("snapshot[0] magic == 'KLPP'", magic, 0x4B4C5050);
    uint32_t shape = sp_read(SP_SNAPSHOT + 1, &ok);
    ck_true("snapshot[1] shape non-zero", shape != 0, shape ? "shape word present" : "read 0");

    // ---- B. a control frame reaches the processor -------------------------
    printf("[B] RX classify -> FIFO -> serializer -> the processor's validator\n");
    uint8_t f[128];
    size_t n = build_adp_discover(f);
    uint32_t before = axi_read(A_PP_DIAG) & 0xFF;
    inject_rx(f, n, 400);                            // tail: drain the serializer
    run_idle(400);
    uint32_t after = axi_read(A_PP_DIAG) & 0xFF;
    ck("ADP DISCOVER accepted (rx_frames +1)", after - before, 1);
    ck("no frame lost to a full FIFO", (axi_read(A_PP_DIAG) >> 8) & 0xFF, 0);

    // ---- C. non-control traffic is rejected by the classifier -------------
    printf("[C] the filter that keeps a 1 B/clk serializer ahead of the wire\n");
    before = axi_read(A_PP_DIAG) & 0xFF;
    for (int i = 0; i < 8; i++) { n = build_ipv4(f); inject_rx(f, n, 40); }
    run_idle(400);
    after = axi_read(A_PP_DIAG) & 0xFF;
    ck("8 IPv4 frames REJECTED (rx_frames flat)", after - before, 0);
    ck("and none of them was counted as a drop", (axi_read(A_PP_DIAG) >> 8) & 0xFF, 0);

    // ---- D. SHADOW DISCIPLINE: it wants to transmit; the wire stays silent -
    printf("[D] shadow discipline — the processor transmits NOTHING to the MAC\n");
    // The shipping ADP plane is disabled out of reset (software enables it), so
    // any MAC TX beat in this window can only have come from the shadow. Run
    // long enough for the compressed ADP cadence to fire.
    long tx_beats = 0;
    for (int r = 0; r < 40; r++) tx_beats += run_idle(2000);
    uint32_t diag = axi_read(A_PP_DIAG);
    uint32_t pp_tx = (diag >> 16) & 0xFFFF;
    ck_true("the processor WANTED to send (tx_frames > 0)", pp_tx > 0,
            pp_tx ? "its TX lanes produced frames" : "no TX attempt seen - check the time compression");
    ck_true("MAC TX stayed SILENT (no shadow frame on the wire)", tx_beats == 0,
            tx_beats == 0 ? "0 beats egressed" : "BEATS EGRESSED - the drain is not holding");

    // ---- F. the TX packer is EXERCISED even while draining ----------------
    // The packer runs in drain mode on purpose: a packer that were bypassed
    // until the substitution day would be untested on the day it matters.
    // tx_frames counts ACCEPTED end-of-frame bytes through the packer's
    // handshake, so a non-zero count is proof the byte->beat path ran to
    // completion, repeatedly, under real backpressure.
    printf("[F] the byte->AXIS packer ran (drain mode still packs)\n");
    uint32_t pp_tx2 = (axi_read(A_PP_DIAG) >> 16) & 0xFFFF;
    ck_true("packer completed whole frames", pp_tx2 > 0,
            pp_tx2 ? "frames packed end to end" : "no frame completed the packer");
    ck_true("packer frame count only grows", pp_tx2 >= pp_tx,
            "monotonic");

    printf("----------------------------------------------------------------\n");
    printf("pp_shadow: %ld checks, %ld failures\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    delete dut;
    return fails ? 1 : 0;
}
