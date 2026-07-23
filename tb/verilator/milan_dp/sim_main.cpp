// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Integration harness for milan_datapath.sv — the PS-less §A.9 wrapper the LiteX
// SoC instantiates. Proves the whole wrapper is correctly assembled by driving it
// exactly the way the SoC will:
//   1. AXI4-Lite CSR slave: read ID="MILN" (0x4D494C4E), VERSION, CAPABILITIES
//      — this is migration deliverable M-A2 ("CPU reaches the CSR plane").
//   2. Program the classifier over the CSR (identity PCP->queue) — proves the
//      CSR -> datapath config wiring.
//   3. TX: push a VLAN frame into the TX DMA port -> collect on the MAC-facing TX
//      port; byte-exact through classifier -> CBS -> PTP -> ADP arbiter.
//   4. RX: push a frame into the MAC-facing RX port -> collect on the RX DMA port;
//      byte-exact through PTP-RX -> dest-MAC filter (default-pass).
//
// gtx_clk is tied to axis_clk (single clock) — the PTP CDC works identically.

#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "Vmilan_datapath_axi_stream_if__T40.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <vector>
#include <array>
#include <cstdint>

static Vmilan_datapath* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, unsigned long got, unsigned long exp) {
    bool ok = (got == exp);
    checks++; if (!ok) fails++;
    printf("  [%s] %-34s got=0x%08lx exp=0x%08lx\n", ok ? "PASS" : "FAIL", what, got, exp);
}

// ---- clocking: axis_clk and gtx_clk driven together (single domain) ----
static void eval() { dut->eval(); }
static void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; eval(); }
static void hi() { dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; eval(); }
static long g_step = 0;
static void step() { lo(); hi(); g_step++; }

// ---- AXI4-Lite BFM (same protocol/timing as the milan_csr harness): sample the
//      *ready when the clock is low (combinational), then pulse the rising edge to
//      commit the transfer. AW and W are held valid together until both readys
//      assert (milan_csr is a single-outstanding slave that accepts them jointly). ----
static void axi_write(uint16_t a, uint32_t d) {
    dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
    dut->s_axi_wdata = d;  dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
    dut->s_axi_bready = 1;
    for (int g = 0; g < 2048; g++) {
        lo(); bool acc = dut->s_axi_awready && dut->s_axi_wready; hi();
        if (acc) break;
    }
    dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
    for (int g = 0; g < 2048; g++) { lo(); bool bv = dut->s_axi_bvalid; hi(); if (bv) break; }
    dut->s_axi_bready = 0;
}

static uint32_t axi_read(uint16_t a) {
    dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
    for (int g = 0; g < 2048; g++) { lo(); bool acc = dut->s_axi_arready; hi(); if (acc) break; }
    dut->s_axi_arvalid = 0;
    uint32_t d = 0;
    for (int g = 0; g < 2048; g++) {
        lo(); bool rv = dut->s_axi_rvalid; if (rv) d = dut->s_axi_rdata; hi();
        if (rv) break;
    }
    dut->s_axi_rready = 0;
    return d;
}

// ---- register offsets (docs/reference/REGISTER_MAP.md) ----
enum {
    A_ID = 0x000, A_VERSION = 0x004, A_CAP = 0x008,
    A_CLS_CTRL = 0x300, A_CLS_MAP = 0x308, A_CLS_REGEN = 0x30C, A_CLS_TCQ = 0x310,
};

// ---- build a VLAN frame; PCP in TCI[7:5]; payload keyed by `marker` ----
// Beats are big-endian in the byte lane (tdata[63:56] = first wire byte), matching
// the datapath harness and BIG_ENDIAN=0 convention used inside the wrapper.
static std::vector<uint64_t> vlan_frame(int pcp, uint8_t marker, uint16_t ethertype = 0x0800) {
    uint8_t b[64]; memset(b, 0, sizeof b);
    const uint8_t dst[6] = {0x00,0x11,0x22,0x33,0x44,0x55};
    const uint8_t src[6] = {0x66,0x77,0x88,0x99,0xAA,0xBB};
    memcpy(b, dst, 6); memcpy(b+6, src, 6);
    b[12] = 0x81; b[13] = 0x00;                 // 802.1Q TPID
    b[14] = (uint8_t)((pcp & 7) << 5);          // TCI hi: PCP in [7:5]
    b[15] = 0x00;
    b[16] = (uint8_t)(ethertype >> 8); b[17] = (uint8_t)ethertype;
    for (int i = 18; i < 64; i++) b[i] = (uint8_t)(marker ^ i);
    std::vector<uint64_t> beats;
    for (int bt = 0; bt < 8; bt++) {
        uint64_t v = 0;
        for (int j = 0; j < 8; j++) v |= (uint64_t)b[bt*8+j] << (8*(7-j));
        beats.push_back(v);
    }
    return beats;
}

// ---- push a frame into an AXIS slave port, collect from an AXIS master port ----
// Templated on the port accessors via lambdas would be neat, but keep it explicit.
struct Res { std::vector<uint64_t> data; bool got = false; };

// TX: s_axis_tx_* in -> m_axis_mac_tx_* out
static Res run_tx(const std::vector<uint64_t>& beats, int cycles) {
    Res r; size_t idx = 0;
    dut->m_axis_mac_tx_tready = 1;
    for (int c = 0; c < cycles; c++) {
        if (idx < beats.size()) {
            dut->s_axis_tx_tdata = beats[idx];
            dut->s_axis_tx_tkeep = 0xFF;
            dut->s_axis_tx_tvalid = 1;
            dut->s_axis_tx_tlast = (idx == beats.size()-1);
        } else {
            dut->s_axis_tx_tvalid = 0; dut->s_axis_tx_tlast = 0;
        }
        step();
        if (dut->s_axis_tx_tvalid && dut->s_axis_tx_tready) idx++;
        if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
            r.data.push_back(dut->m_axis_mac_tx_tdata); r.got = true;
        }
    }
    dut->s_axis_tx_tvalid = 0;
    return r;
}

// RX: s_axis_mac_rx_* in -> m_axis_rx_* out
static Res run_rx(const std::vector<uint64_t>& beats, int cycles) {
    Res r; size_t idx = 0;
    dut->m_axis_rx_tready = 1;
    for (int c = 0; c < cycles; c++) {
        if (idx < beats.size()) {
            dut->s_axis_mac_rx_tdata = beats[idx];
            dut->s_axis_mac_rx_tkeep = 0xFF;
            dut->s_axis_mac_rx_tvalid = 1;
            dut->s_axis_mac_rx_tlast = (idx == beats.size()-1);
        } else {
            dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
        }
        // pre-edge sampling: read what this edge commits (post-edge reads
        // miss single-cycle final beats and catch upstream re-presents)
        lo();
        bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
        bool out_acc = dut->m_axis_rx_tvalid && dut->m_axis_rx_tready;
        uint64_t out_d = dut->m_axis_rx_tdata;
        hi();
        if (in_acc) idx++;
        if (out_acc) { r.data.push_back(out_d); r.got = true; }
    }
    dut->s_axis_mac_rx_tvalid = 0;
    return r;
}

static void do_reset() {
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
    dut->s_axi_bready = dut->s_axi_rready = 0;
    dut->s_axis_tx_tvalid = 0; dut->s_axis_mac_rx_tvalid = 0;
    dut->m_axis_mac_tx_tready = 0; dut->m_axis_rx_tready = 0; dut->m_axis_ts_tready = 1;
    dut->i_mac_speed = 2; dut->i_link_up = 1; dut->i_full_duplex = 1; dut->i_mac_events = 0;
    for (int i = 0; i < 8; i++) step();
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    for (int i = 0; i < 8; i++) step();
}

static bool frames_equal(const std::vector<uint64_t>& a, const std::vector<uint64_t>& b) {
    if (a.size() != b.size()) return false;
    for (size_t i = 0; i < a.size(); i++) if (a[i] != b[i]) return false;
    return true;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vmilan_datapath;

    printf("=== milan_datapath integration harness (§A.9 wrapper) ===\n");
    do_reset();

    // --- 1. CSR identity over AXI4-Lite (M-A2) ---
    printf("[CSR] identity + reset values\n");
    ck("ID == 'MILN'",  axi_read(A_ID),      0x4D494C4E);
    ck("VERSION",       axi_read(A_VERSION), 0x0001000A);
    // link guard: TB leaves the eth toggles static -> unarmed = inert
    // (alive/alive, RUN, no reinit) exactly like a no-PHY top
    ck("LINKG unarmed", axi_read(0x774), 0x00000003);
    uint32_t cap = axi_read(A_CAP);
    ck("CAP.ADP bit12",  (cap >> 12) & 1, 1);
    ck("CAP.TCAM bit13", (cap >> 13) & 1, 1);

    // --- 2. program the classifier over the CSR (identity PCP p -> queue p) ---
    printf("[CSR] program classifier (identity map)\n");
    axi_write(A_CLS_REGEN, 0x00FAC688);   // PCP -> regen PCP
    axi_write(A_CLS_MAP,   0x00FAC688);   // prio -> TC
    axi_write(A_CLS_TCQ,   0x000000E4);   // TC0..3 -> queue 0..3
    axi_write(A_CLS_CTRL,  0x1);          // use_pcp = 1
    ck("CLS_REGEN readback", axi_read(A_CLS_REGEN), 0x00FAC688);
    ck("CLS_TCQ   readback", axi_read(A_CLS_TCQ),   0x000000E4);

    // --- 3. TX datapath: DMA -> shaper -> PTP -> arbiter -> MAC ---
    // PCP=3 -> queue 3, which is strict-priority (unshaped) at reset, so no CBS
    // credit gating; proves the full TX assembly forwards byte-exact.
    printf("[TX] frame DMA-port -> MAC-port (PCP=3, unshaped queue)\n");
    auto txf = vlan_frame(/*pcp=*/3, /*marker=*/0x5A);
    Res tx = run_tx(txf, 400);
    ck("TX frame emerged on MAC port", tx.got ? 1 : 0, 1);
    ck("TX byte-exact (8 beats)", frames_equal(tx.data, txf) ? 1 : 0, 1);

    // --- 4. RX datapath: MAC -> PTP-RX -> dest-MAC filter (default-pass) -> DMA ---
    printf("[RX] frame MAC-port -> DMA-port (TCAM default-pass)\n");
    auto rxf = vlan_frame(/*pcp=*/1, /*marker=*/0xA5, /*ethertype=*/0x0806);
    Res rx = run_rx(rxf, 400);
    ck("RX frame emerged on DMA port", rx.got ? 1 : 0, 1);
    ck("RX byte-exact (8 beats)", frames_equal(rx.data, rxf) ? 1 : 0, 1);

    // --- 5. ADP enable-after-boot advertises (silicon bug 2026-07-11) ---
    // On the fully-FPGA SoC i_link_up is CONSTANT 1: its only edge pulses one
    // cycle after reset, while ADP is still disabled (CSR reset default). The
    // advertiser's available state needs link_up&&enable, so enabling ADP later
    // NEVER advertised (available_index stuck at 0, nothing on the wire  -
    // diagnosed live through the AVB switch). The wrapper now synthesizes the
    // link-up event on the ADP-enable rising edge while the link is up; this
    // replicates the exact silicon sequence: reset (enable=0, link=1), THEN
    // program identity + enable, and expects a spontaneous ENTITY_AVAILABLE on
    // the MAC port plus an available_index bump.
    printf("[ADP] enable-after-boot advertises (const-link integration fix)\n");
    enum { A_ADP_CTRL = 0x600, A_ADP_EIDLO = 0x604, A_ADP_EIDHI = 0x608,
           A_ADP_STATUS = 0x644, A_MAC_ALO = 0x108, A_MAC_AHI = 0x10C };
    // station MAC exactly as kl-eth programs it (platform LSB-first packing:
    // ALO/AHI hold 02:00:00:00:00:01 with [7:0] = first wire byte)
    axi_write(A_MAC_ALO, 0x00000002);
    axi_write(A_MAC_AHI, 0x00000100);
    axi_write(A_ADP_EIDHI, 0x020000FF);
    axi_write(A_ADP_EIDLO, 0xFE000001);
    uint32_t ai0 = axi_read(A_ADP_STATUS);
    axi_write(A_ADP_CTRL, 0x00001F01);           // enable=1, valid_time=31
    Res adp; dut->m_axis_mac_tx_tready = 1;
    for (int c = 0; c < 600; c++) {
        step();
        if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
            adp.data.push_back(dut->m_axis_mac_tx_tdata); adp.got = true;
        }
        if (adp.got && dut->m_axis_mac_tx_tlast) { step(); break; }
    }
    ck("ADP frame emerged on MAC port", adp.got ? 1 : 0, 1);
    // MAC-facing AXIS is little-endian in the byte lane (tdata[7:0] = first
    // wire byte): dst 91:e0:f0:01:00:00 = low 48 bits 0x000001f0e091. Beat 1
    // low half carries ethertype 22 f0 + AVTP subtype 0xFA in bytes 4..6.
    ck("ADP dst multicast 91:e0:f0:01:00:00",
       adp.data.empty() ? 0 : (unsigned long)(adp.data[0] & 0xFFFFFFFFFFFFUL),
       0x000001F0E091UL);
    ck("ADP ethertype 0x22F0 + subtype 0xFA",
       adp.data.size() < 2 ? 0 : (unsigned long)((adp.data[1] >> 32) & 0xFFFFFF),
       0xFAF022UL);
    // src MAC must egress 02:00:00:00:00:01 (byte-reverse at the instantiation:
    // a swapped src is 01:.. = MULTICAST SOURCE, which bridges MUST drop -
    // silicon-diagnosed through the AVB switch 2026-07-11). Bytes 6-7 sit in
    // beat0[63:48] (02 00), bytes 8-11 in beat1[31:0] (00 00 00 01).
    ck("ADP src bytes 6-7 = 02 00",
       adp.data.empty() ? 0 : (unsigned long)(adp.data[0] >> 48), 0x0002UL);
    ck("ADP src bytes 8-11 = 00 00 00 01",
       adp.data.size() < 2 ? 0 : (unsigned long)(adp.data[1] & 0xFFFFFFFFUL),
       0x01000000UL);
    ck("available_index bumped", axi_read(A_ADP_STATUS) > ai0 ? 1 : 0, 1);

    // --- 6b. ACMP GET_TX_STATE through the full datapath ---
    // The responder taps rx_axis_to_dma (little lane, like silicon); inject a
    // 70-byte GET_TX_STATE_COMMAND for our entity on the MAC RX port and
    // expect the GET_TX_STATE_RESPONSE (SUCCESS, count=0) on the MAC TX port.
    printf("[ACMP] GET_TX_STATE -> RESPONSE through datapath\n");
    {
        uint8_t f[72]; memset(f, 0, sizeof f);
        const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
        memcpy(f, mc, 6);
        const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
        memcpy(f+6, csrc, 6);
        f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x04;      // GET_TX_STATE_COMMAND
        f[16]=0x00; f[17]=44;                                // cdl
        // stream_id junk (18-25); controller (26-33)
        for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;
        // talker = 02:00:00:ff:fe:00:00:01 (the EID programmed in section 5)
        const uint8_t tk[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
        memcpy(f+34, tk, 8);
        f[62]=0x1A; f[63]=0x2B;                              // sequence_id
        std::vector<uint64_t> beats;
        for (int bt = 0; bt < 9; bt++) {
            uint64_t v = 0;
            for (int j = 0; j < 8; j++) v |= (uint64_t)f[bt*8+j] << (8*j);
            beats.push_back(v);
        }
        // inject and capture in ONE loop: the response can egress within a
        // few cycles of tlast, before a separate capture loop would start
        Res ac; size_t idx = 0;
        dut->m_axis_rx_tready = 1; dut->m_axis_mac_tx_tready = 1;
        for (int c = 0; c < 800; c++) {
            if (idx < beats.size()) {
                dut->s_axis_mac_rx_tdata  = beats[idx];
                dut->s_axis_mac_rx_tkeep  = 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast  = (idx == beats.size()-1);
            } else {
                dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
            }
            step();
            if (dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready) idx++;
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                ac.data.push_back(dut->m_axis_mac_tx_tdata); ac.got = true;
                if (dut->m_axis_mac_tx_tlast) { step(); break; }
            }
        }
        dut->s_axis_mac_rx_tvalid = 0;
        ck("ACMP response emerged on MAC port", ac.got ? 1 : 0, 1);
        ck("ACMP response is 9 beats", ac.data.size(), 9);
        if (ac.data.size() == 9) {
            ck("ACMP dst multicast", (unsigned long)(ac.data[0] & 0xFFFFFFFFFFFFUL),
               0x000001F0E091UL);
            ck("ACMP subtype 0xFC", (ac.data[1] >> 48) & 0xFF, 0xFC);
            ck("ACMP msg GET_TX_STATE_RESPONSE(5)", (ac.data[1] >> 56) & 0x0F, 5);
            ck("ACMP status SUCCESS + cdl 44",
               (unsigned)(ac.data[2] & 0xFFFF), (unsigned)((44 & 0xFF) << 8));
            ck("ACMP connection_count 0", (ac.data[7] >> 32) & 0xFFFF, 0);
            ck("ACMP sequence echoed", (ac.data[7] >> 48) & 0xFFFF, 0x2B1AUL);
        }
        enum { A_ACMP_STAT = 0x650 };
        ck("CSR 0x650 = {resp=1, cmd=1}", axi_read(A_ACMP_STAT), 0x00010001);
    }

    // --- 6. IRQ line is a defined level (no X) ---
    printf("[IRQ] o_irq_csr is driven\n");
    ck("o_irq_csr defined (0/1)", (dut->o_irq_csr <= 1) ? 1 : 0, 1);

    // --- 7. PTP ts record end-to-end through the REAL ingress (phase B) ---
    // A 0x88F7 frame at s_axis_mac_rx must yield one 2-beat metadata record on
    // m_axis_ts: {ns; {seq<<8 | dir}}. This is the check that would have caught
    // the BIG_ENDIAN(0)/F788 instantiation (extracted src-MAC bytes under the
    // BE-lane convention -> zero records on silicon while the unit TB agreed
    // with the wrong pair by driving LE lanes).
    {
        printf("[PTP-TS] gPTP RX -> metadata record\n");
        enum { A_PTP_CTRL = 0x500, A_PTP_INCR = 0x504 };
        axi_write(A_PTP_INCR, 20u << 24);       // 20 ns/tick Q8.24
        axi_write(A_PTP_CTRL, 1);
        uint8_t g[68]; memset(g, 0, sizeof g);
        const uint8_t gh[14] = {0x01,0x80,0xC2,0,0,0x0E, 2,0,0,0,0,2, 0x88,0xF7};
        memcpy(g, gh, 14);
        g[14] = 0x12; g[15] = 0x02; g[17] = 54;  // pdelay_req, v2, len 54
        g[44] = 0xBE; g[45] = 0xEF;              // sequenceId
        std::vector<uint64_t> gb;
        for (int bt = 0; bt < 9; bt++) {
            uint64_t v = 0;
            for (int j = 0; j < 8 && bt*8+j < 68; j++)
                v |= (uint64_t)g[bt*8+j] << (8*j);   // LE lanes = the real ingress
            gb.push_back(v);
        }
        std::vector<uint64_t> ts;
        size_t idx = 0;
        dut->m_axis_ts_tready = 1;
        for (int c = 0; c < 600; c++) {
            if (idx < gb.size()) {
                dut->s_axis_mac_rx_tdata = gb[idx];
                dut->s_axis_mac_rx_tkeep = (idx == gb.size()-1) ? 0x0F : 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast = (idx == gb.size()-1);
            } else {
                dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
            }
            lo();
            bool adv = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
            bool tsx = dut->m_axis_ts_tvalid && dut->m_axis_ts_tready;
            uint64_t td = dut->m_axis_ts_tdata;
            hi();
            if (adv) idx++;
            if (tsx) ts.push_back(td);
        }
        dut->s_axis_mac_rx_tvalid = 0;
        ck("ts record emitted (2 beats)", ts.size(), 2);
        if (ts.size() == 2) {
            ck("ts word0 (ns) nonzero", ts[0] != 0 ? 1 : 0, 1);
            ck("ts word1 dir=RX",       (unsigned long)(ts[1] & 1), 0);
            ck("ts word1 mtype=2 (pdelay_req)", (unsigned long)((ts[1] >> 4) & 0xF), 2);
            ck("ts word1 seq=0xBEEF",   (unsigned long)((ts[1] >> 8) & 0xFFFF), 0xBEEFUL);
        }
        // interference variant: same event frame at LINE RATE between two
        // full-rate IPv4 floods + one general gPTP (Follow_Up, must NOT
        // record). Exactly one more record, correct meta.
        uint64_t ts1 = ts.size() == 2 ? ts[0] : 0;
        ts.clear();
        {
            auto flood = vlan_frame(/*pcp=*/1, /*marker=*/0x77);
            std::vector<uint64_t> mix;
            for (int r = 0; r < 3; r++) mix.insert(mix.end(), flood.begin(), flood.end());
            g[14] = 0x18;                          // majorSdoId 1 | Follow_Up(8): general
            g[44] = 0xDE; g[45] = 0xAD;
            for (int bt = 0; bt < 9; bt++) {
                uint64_t v = 0;
                for (int j = 0; j < 8 && bt*8+j < 68; j++)
                    v |= (uint64_t)g[bt*8+j] << (8*j);
                mix.push_back(v);
            }
            g[14] = 0x12;                          // pdelay_req again: event
            g[44] = 0xCA; g[45] = 0xFE;
            for (int bt = 0; bt < 9; bt++) {
                uint64_t v = 0;
                for (int j = 0; j < 8 && bt*8+j < 68; j++)
                    v |= (uint64_t)g[bt*8+j] << (8*j);
                mix.push_back(v);
            }
            for (int r = 0; r < 3; r++) mix.insert(mix.end(), flood.begin(), flood.end());
            // beat boundaries: flood frames are 8 beats, gptp 9 beats
            std::vector<int> lens = {8,8,8, 9, 9, 8,8,8};
            size_t idx = 0; int fi = 0, fb = 0;
            for (int c = 0; c < 1200 && idx < mix.size(); c++) {
                dut->s_axis_mac_rx_tdata = mix[idx];
                dut->s_axis_mac_rx_tkeep = (fi >= 3 && fi <= 4 && fb == 8) ? 0x0F : 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast = (fb == lens[fi] - 1);
                lo();
                bool adv = dut->s_axis_mac_rx_tready;
                bool tsx = dut->m_axis_ts_tvalid && dut->m_axis_ts_tready;
                uint64_t td = dut->m_axis_ts_tdata;
                hi();
                if (adv) { idx++; if (++fb == lens[fi]) { fb = 0; fi++; } }
                if (tsx) ts.push_back(td);
            }
            dut->s_axis_mac_rx_tvalid = 0;
            for (int c = 0; c < 300; c++) {
                lo();
                bool tsx = dut->m_axis_ts_tvalid && dut->m_axis_ts_tready;
                uint64_t td = dut->m_axis_ts_tdata;
                hi();
                if (tsx) ts.push_back(td);
            }
            ck("interference: exactly one record", ts.size(), 2);
            if (ts.size() == 2) {
                ck("interference: ns advanced", ts[0] > ts1 ? 1 : 0, 1);
                ck("interference: mtype=2 seq=0xCAFE",
                   (unsigned long)(((ts[1] >> 4) & 0xF) | (((ts[1] >> 8) & 0xFFFF) << 4)),
                   (unsigned long)(2 | (0xCAFEUL << 4)));
            }
        }
    }

    // --- 8. ADP depart witness + enable-toggle recovery (silicon 2026-07-13) ---
    // The Arty's advertiser went dormant mid-session (available_r cleared with
    // NO software writer of ADP_CMD; link_down structurally impossible) and
    // only an enable-edge poke revived it. This validates the CSR view of that
    // flow: A_ADP_DIAG zero at boot -> ADP_CMD[1] departs (DEPARTING frame on
    // the MAC + depart_cnt/src witness) -> dormant (silent) -> the exact bench
    // recovery (enable 0->1) re-arms and advertises, without a new depart
    // count. The tick-driven dormancy SELF-re-arm is unit-tested in
    // tb/verilator/adp (the 1 s tick is unreachable at datapath scale).
    {
        printf("[ADP-DIAG] depart witness + enable-toggle recovery\n");
        enum { A_ADP_CMD = 0x640, A_ADP_DIAG = 0x668 };
        ck("DIAG zero at boot", axi_read(A_ADP_DIAG), 0);
        uint32_t ai_pre = axi_read(A_ADP_STATUS);
        axi_write(A_ADP_CMD, 0x2);                 // software depart
        Res dep; dut->m_axis_mac_tx_tready = 1;
        for (int c = 0; c < 600; c++) {
            step();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                dep.data.push_back(dut->m_axis_mac_tx_tdata); dep.got = true;
            }
            if (dep.got && dut->m_axis_mac_tx_tlast) { step(); break; }
        }
        ck("DEPARTING frame emerged", dep.got ? 1 : 0, 1);
        // ADPDU byte 15 = {4'b0, message_type} sits in beat1 lane 7
        ck("message_type DEPARTING(1)",
           dep.data.size() < 2 ? 0xFF : (unsigned long)((dep.data[1] >> 56) & 0x0F), 1);
        ck("DIAG: depart_cnt=1, src=shutdown", axi_read(A_ADP_DIAG), (2u << 16) | 1u);
        ck("index bumped on depart", axi_read(A_ADP_STATUS), ai_pre + 1);
        // dormant: nothing else may emerge
        bool stray = false;
        for (int c = 0; c < 400; c++) { step(); if (dut->m_axis_mac_tx_tvalid) stray = true; }
        ck("dormant after depart (MAC silent)", stray ? 1 : 0, 0);
        // recovery = the bench poke: enable 0 -> 1 (wrapper synthesizes the
        // link-up event on the rising edge; same path as enable-after-boot)
        axi_write(A_ADP_CTRL, 0x00001F00);
        axi_write(A_ADP_CTRL, 0x00001F01);
        Res rec;
        for (int c = 0; c < 600; c++) {
            step();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                rec.data.push_back(dut->m_axis_mac_tx_tdata); rec.got = true;
            }
            if (rec.got && dut->m_axis_mac_tx_tlast) { step(); break; }
        }
        ck("AVAILABLE after enable-toggle", rec.got ? 1 : 0, 1);
        ck("message_type AVAILABLE(0)",
           rec.data.size() < 2 ? 0xFF : (unsigned long)((rec.data[1] >> 56) & 0x0F), 0);
        ck("recovery adds no depart count", axi_read(A_ADP_DIAG), (2u << 16) | 1u);
    }

    // --- 9. Milan talker: PROBE_TX-gated AAF streaming end-to-end ---
    // docs/design/MILAN_TALKER_SM.md: with AAF_CTRL bypass=0 (Milan mode)
    // the framer is gated by the ACMP probe SM. Before any probe: enable=1
    // yields NO AAF frames. A PROBE_TX (wire CONNECT_TX) returns SUCCESS
    // with the LIVE stream params AND opens the gate; the AAF frames on the
    // MAC then carry the exact stream_id the probe handed out. CSR
    // A_ACMP_TALKER witnesses {armed, active, gate}.
    {
        printf("[MILAN-TALKER] probe-gated AAF streaming\n");
        enum { A_AAF_CTRL = 0x654, A_ACMP_TALKER = 0x66C };
        // Milan mode: enable=1, bypass=0, VID=2 (reset is bypass=1)
        axi_write(A_AAF_CTRL, 0x00020001);
        ck("gate closed pre-probe (CSR)", axi_read(A_ACMP_TALKER) & 0xB, 0);
        // no AAF frames while gated: watch the MAC for > one full frame
        // accumulation period (6 pairs x 1024 cycles + slack)
        {
            bool aaf_seen = false;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 9000; c++) {
                step();
                if (dut->m_axis_mac_tx_tvalid) aaf_seen = true;
            }
            ck("MAC silent while gated", aaf_seen ? 1 : 0, 0);
        }
        // PROBE_TX for talker :01 uid 0 (70-byte ACMP, little-lane inject)
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x00;      // CONNECT_TX_COMMAND
            f[16]=0x00; f[17]=44;                                // cdl
            for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;     // controller
            const uint8_t tk[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+34, tk, 8);                                 // talker = us
            f[62]=0x3C; f[63]=0x4D;                              // sequence_id
            std::vector<uint64_t> beats;
            for (int bt = 0; bt < 9; bt++) {
                uint64_t v = 0;
                for (int j = 0; j < 8; j++) v |= (uint64_t)f[bt*8+j] << (8*j);
                beats.push_back(v);
            }
            Res pr; size_t idx = 0;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 800; c++) {
                if (idx < beats.size()) {
                    dut->s_axis_mac_rx_tdata  = beats[idx];
                    dut->s_axis_mac_rx_tkeep  = 0xFF;
                    dut->s_axis_mac_rx_tvalid = 1;
                    dut->s_axis_mac_rx_tlast  = (idx == beats.size()-1);
                } else {
                    dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
                }
                step();
                if (dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready) idx++;
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    pr.data.push_back(dut->m_axis_mac_tx_tdata); pr.got = true;
                    if (dut->m_axis_mac_tx_tlast) { step(); break; }
                }
            }
            dut->s_axis_mac_rx_tvalid = 0;
            ck("PROBE response emerged", pr.got ? 1 : 0, 1);
            ck("PROBE response 9 beats", pr.data.size(), 9);
            if (pr.data.size() == 9) {
                // msg CONNECT_TX_RESPONSE(1) + status SUCCESS: frame byte 15
                // = beat1 lane 7; byte 16 = beat2 lane 0
                ck("PROBE msg RESPONSE(1)", (pr.data[1] >> 56) & 0x0F, 1);
                ck("PROBE status SUCCESS", (pr.data[2] >> 3) & 0x1F, 0);
                // stream_id (bytes 18-25 = beat2 lanes 2-7 + beat3 lanes 0-1):
                // {station_mac 02:00:00:00:00:01, uid 0}
                uint64_t sid = 0;
                for (int k = 18; k < 26; k++)
                    sid = (sid << 8) | ((pr.data[k/8] >> (8*(k%8))) & 0xFF);
                ck("PROBE stream_id {mac,0}", (unsigned long long)sid,
                   0x0200000000010000ULL);
            }
        }
        ck("gate open post-probe (CSR armed|active|gate)",
           axi_read(A_ACMP_TALKER) & 0xB, 0xB);
        // AAF frames now flow and carry the SAME stream_id (VLAN-tagged
        // frame: stream_id at bytes 22-29)
        {
            std::vector<uint8_t> fr; bool in_aaf = false; int aaf_frames = 0;
            uint64_t aaf_sid = 0;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 20000 && aaf_frames == 0; c++) {
                step();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            fr.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        if (fr.size() >= 30 && fr[12] == 0x81 && fr[13] == 0x00 &&
                            fr[16] == 0x22 && fr[17] == 0xF0 && fr[18] == 0x02) {
                            in_aaf = true; aaf_frames++;
                            aaf_sid = 0;
                            for (int k = 22; k < 30; k++)
                                aaf_sid = (aaf_sid << 8) | fr[k];
                        }
                        fr.clear();
                    }
                }
            }
            ck("AAF frame flows post-probe", aaf_frames >= 1, 1);
            ck("AAF stream_id == probed id", in_aaf ? (unsigned long long)aaf_sid : 0,
               0x0200000000010000ULL);
        }
        // pilot tone (CSR 0x6DC): AAF payload switches to the exact-period
        // 1 kHz 0 dBFS table - both channels equal, samples advancing
        {
            static const uint32_t TAB[48] = {
                0x000000,0x10B515,0x2120FB,0x30FBC5,0x3FFFFF,0x4DEBE4,
                0x5A8279,0x658C99,0x6ED9EB,0x7641AE,0x7BA374,0x7EE7A9,
                0x7FFFFF,0x7EE7A9,0x7BA374,0x7641AE,0x6ED9EB,0x658C99,
                0x5A8279,0x4DEBE4,0x3FFFFF,0x30FBC5,0x2120FB,0x10B515,
                0x000000,0xEF4AEB,0xDEDF05,0xCF043B,0xC00001,0xB2141C,
                0xA57D87,0x9A7367,0x912615,0x89BE52,0x845C8C,0x811857,
                0x800001,0x811857,0x845C8C,0x89BE52,0x912615,0x9A7367,
                0xA57D87,0xB2141C,0xC00000,0xCF043B,0xDEDF05,0xEF4AEB };
            axi_write(0x6DC, 0x1);          // TONE_CTRL.en
            ck("TONE_CTRL readback", axi_read(0x6DC), 1);
            // skip a few frames so tone samples propagate, then capture one
            std::vector<uint8_t> fr; int skip = 3; bool checked = false;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 60000 && !checked; c++) {
                step();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            fr.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        bool aaf = fr.size() > 60 && fr[12]==0x81 && fr[16]==0x22
                                   && fr[17]==0xF0 && fr[18]==0x02;
                        if (aaf && skip > 0) skip--;
                        else if (aaf) {
                            auto smp = [&](int off){ return (uint32_t)
                                ((fr[off]<<16)|(fr[off+1]<<8)|fr[off+2]); };
                            uint32_t l0=smp(42), r0=smp(46), l1=smp(50);
                            bool in_tab=false; int idx=-1;
                            for (int k=0;k<48;k++) if (TAB[k]==l0){in_tab=true;idx=k;}
                            ck("tone L0 in table", in_tab?1:0, 1);
                            ck("tone L0 == R0 (both channels)", l0==r0, 1);
                            ck("tone advances (L1 = next entry)",
                               idx>=0 && l1==TAB[(idx+1)%48], 1);
                            checked = true;
                        }
                        fr.clear();
                    }
                }
            }
            ck("tone frame captured", checked?1:0, 1);
            axi_write(0x6DC, 0x0);          // tone off
        }

        // restore the reset default (bypass=1) so later sections see legacy
        axi_write(A_AAF_CTRL, 0x00020002);
    }

    {
        printf("[AVTP-RXMON] BIND_RX -> AAF frame -> STREAM_INPUT counters (0x6B8)\n");
        enum { A_ACMPL_STATE = 0x6A4, A_AVTPRX_STAT = 0x6B8,
               A_AVTPRX_FRX = 0x6BC, A_AVTPRX_ERR = 0x6C0 };
        ck("RXMON stat idle", axi_read(A_AVTPRX_STAT), 0);
        ck("RXMON frames_rx idle", axi_read(A_AVTPRX_FRX), 0);

        // helper: inject one little-lane frame on the MAC RX port, draining
        // any TX response and collecting PCM-ring beats the datapath produces
        std::vector<uint8_t> pcm;
        bool pcm_last = false;
        auto inject = [&](const uint8_t* f, size_t len) {
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
            for (int c = 0; c < 1500; c++) {
                if (idx < beats.size()) {
                    dut->s_axis_mac_rx_tdata  = beats[idx];
                    dut->s_axis_mac_rx_tkeep  = 0xFF;
                    dut->s_axis_mac_rx_tvalid = 1;
                    dut->s_axis_mac_rx_tlast  = (idx == beats.size()-1);
                } else {
                    dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
                }
                step();
                if (dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready) idx++;
                if (dut->m_axis_pcm_tvalid) {
                    for (int l = 0; l < 8; l++)
                        pcm.push_back((dut->m_axis_pcm_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_pcm_tlast) pcm_last = true;
                }
            }
            dut->s_axis_mac_rx_tvalid = 0;
        };

        // BIND_RX (CONNECT_RX_COMMAND, msg 6): listener = us, talker = :02
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x06;      // BIND_RX
            f[16]=0x00; f[17]=44;                                // cdl
            for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;     // controller
            const uint8_t tk[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x02};
            memcpy(f+34, tk, 8);                                 // talker :02
            const uint8_t ls[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, ls, 8);                                 // listener = us
            f[62]=0x11; f[63]=0x22;                              // sequence_id
            inject(f, 70);
        }
        ck("listener bound (0x6A4 state != 0)",
           (axi_read(A_ACMPL_STATE) & 0x7) != 0, 1);

        // AAF PDU on the bound stream_id {02:00:00:00:00:02, uid 0} with the
        // default format's fields (48 kHz / INT32 / depth 32 / 8 ch)
        auto mkaaf = [&](uint8_t seq, uint8_t nsr) {
            static uint8_t f[120];
            memset(f, 0, sizeof f);
            const uint8_t dmac[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x02};
            memcpy(f, dmac, 6);
            const uint8_t src[6] = {0x02,0x00,0x00,0x00,0x00,0x02};
            memcpy(f+6, src, 6);
            f[12]=0x22; f[13]=0xF0;
            f[14]=0x02;                                          // AAF
            f[15]=0x81;                                          // sv, tv
            f[16]=seq;
            const uint8_t sid[8] = {0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x00};
            memcpy(f+18, sid, 8);
            f[26]=0xAA; f[27]=0xBB; f[28]=0xCC; f[29]=0xDD;   // avtp_ts
            f[30]=0x02;                                          // format INT32
            f[31]=(uint8_t)(nsr << 4);                           // nsr
            f[32]=2;                                             // channels (talker truth)
            f[33]=32;                                            // bit depth
            f[34]=0x00; f[35]=0x30;                              // data_len 48
            for (int i = 0; i < 48; i++) f[38+i] = (uint8_t)(0x30+i); // payload
            return f;
        };
        inject(mkaaf(5, 0x05), 120);
        ck("FRAMES_RX 1 (0x6BC)", axi_read(A_AVTPRX_FRX), 1);
        ck("locked + MEDIA_LOCKED=1 (0x6B8)",
           axi_read(A_AVTPRX_STAT) & 0xFF01, 0x0101);
        ck("no errors (0x6C0)", axi_read(A_AVTPRX_ERR), 0);

        // PCM ring path: the accepted PDU's 64 payload bytes emerged as
        // 8 full beats, wire byte order, one AXIS frame
        ck("PCM payload 48 bytes", (long)pcm.size(), 48);
        ck("PCM tlast seen", pcm_last ? 1 : 0, 1);
        bool pay_ok = pcm.size() >= 48;
        for (int i = 0; i < 48 && pay_ok; i++)
            if (pcm[i] != (uint8_t)(0x30+i)) pay_ok = false;
        ck("PCM payload byte-exact", pay_ok ? 1 : 0, 1);
        enum { A_PCMRX_CNT = 0x6C4, A_PCMRX_TS = 0x6C8 };
        ck("PCMRX pdus=1 drops=0 (0x6C4)", axi_read(A_PCMRX_CNT), 1);
        ck("PCMRX last avtp_ts (0x6C8)", axi_read(A_PCMRX_TS), 0xAABBCCDD);

        // VLAN-tagged PDU (rotate-6 realignment): same 64 payload bytes
        {
            uint8_t tf[124]; memset(tf, 0, sizeof tf);
            const uint8_t* uf = mkaaf(6, 0x05);
            memcpy(tf, uf, 12);
            tf[12]=0x81; tf[13]=0x00; tf[14]=0x00; tf[15]=0x02;   // C-VLAN, VID 2
            memcpy(tf+16, uf+12, 108);                            // shifted rest
            pcm.clear(); pcm_last = false;
            inject(tf, 124);
        }
        ck("tagged: FRAMES_RX 2", axi_read(A_AVTPRX_FRX), 2);
        ck("tagged: PCM 48 bytes", (long)pcm.size(), 48);
        bool tag_ok = pcm.size() >= 48;
        for (int i = 0; i < 48 && tag_ok; i++)
            if (pcm[i] != (uint8_t)(0x30+i)) tag_ok = false;
        ck("tagged: payload byte-exact", tag_ok ? 1 : 0, 1);
        ck("tagged: PCMRX pdus=2", axi_read(A_PCMRX_CNT), 2);

        // PRE-FILTER TAP (2026-07-19): program a TCAM drop entry for the
        // AVTP multicast range (91:E0:F0::/24) - the KERNEL path must go
        // quiet while the fabric depacketizer keeps consuming the stream.
        {
            enum { A_TCAM_KLO = 0x704, A_TCAM_KHI = 0x708, A_TCAM_MLO = 0x70C,
                   A_TCAM_MHI = 0x710, A_TCAM_ACT = 0x714, A_TCAM_CMD = 0x718 };
            // the shared inject() never drives the DMA-port tready, so passed
            // frames' tails stall at the filter boundary and flush into LATER
            // windows as ghost beats - drain them before arming the drop
            dut->m_axis_rx_tready = 1;
            for (int c = 0; c < 200; c++) step();
            axi_write(A_TCAM_KHI, 0x000091E0);
            axi_write(A_TCAM_KLO, 0xF0000000);
            axi_write(A_TCAM_MHI, 0x0000FFFF);          // care: top 3 bytes
            axi_write(A_TCAM_MLO, 0xFF000000);
            axi_write(A_TCAM_ACT, 0x00000001);          // action[0]=drop
            axi_write(A_TCAM_CMD, 0x00010100);          // commit|valid, entry 0
            long pcm0 = axi_read(A_PCMRX_CNT);
            long kern = 0; long kern_beats = 0; uint64_t kern_dmac = 0;
            auto inject_cnt = [&](const uint8_t* f, size_t len) {
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
                dut->m_axis_rx_tready = 1;
                for (int c = 0; c < 1500; c++) {
                    if (idx < beats.size()) {
                        dut->s_axis_mac_rx_tdata  = beats[idx];
                        dut->s_axis_mac_rx_tkeep  = 0xFF;
                        dut->s_axis_mac_rx_tvalid = 1;
                        dut->s_axis_mac_rx_tlast  = (idx == beats.size()-1);
                    } else {
                        dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
                    }
                    // PRE-edge sampling (correct AXIS observer): settle low,
                    // read what this edge will commit, then clock high.
                    lo();
                    bool in_acc  = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
                    bool pcm_acc = dut->m_axis_pcm_tvalid;
                    uint64_t pcm_d = dut->m_axis_pcm_tdata;
                    bool k_acc   = dut->m_axis_rx_tvalid && dut->m_axis_rx_tready;
                    bool k_last  = dut->m_axis_rx_tlast;
                    uint64_t k_d = dut->m_axis_rx_tdata;
                    hi(); g_step++;
                    if (in_acc) idx++;
                    if (pcm_acc)
                        for (int l = 0; l < 8; l++)
                            pcm.push_back((pcm_d >> (8*l)) & 0xFF);
                    if (k_acc) {
                        if (kern_dmac == 0 && kern_beats == 0) kern_dmac = k_d;
                        kern_beats++;
                        if (k_last) kern++;
                    }
                }
                dut->s_axis_mac_rx_tvalid = 0;
            };
            // isolate: plain (non-AVTP) frame on the filtered dmac range
            {
                uint8_t pf[64]; memset(pf, 0, sizeof pf);
                const uint8_t pdst[6] = {0x91,0xE0,0xF0,0x00,0x77,0x77};
                memcpy(pf, pdst, 6); pf[12]=0x08; pf[13]=0x00;
                kern = 0; kern_beats = 0; kern_dmac = 0;
                inject_cnt(pf, 64);
                ck("prefilter: plain 91E0F0 frame dropped from DMA", kern, 0);
                const uint8_t odst[6] = {0x00,0x11,0x22,0x33,0x44,0x55};
                memcpy(pf, odst, 6);
                kern = 0; inject_cnt(pf, 64);
                ck("prefilter: other dmac still passes", kern, 1);
            }
            // EXACT silicon wire frame (tap capture 2026-07-19): 86 bytes,
            // partial last beat keep=0x3F - the shape mkaaf never covered
            {
                static const uint8_t WF[] = {
                  0x91,0xE0,0xF0,0x00,0xE1,0xE3, 0x02,0x00,0x00,0x00,0x00,0x01,
                  0x22,0xF0,
                  0x02,0x81,0x86,0x00, 0x02,0x00,0x00,0x00,0x00,0x01,0x00,0x00,
                  0x74,0x6A,0xE3,0x96, 0x02,0x50,0x02,0x20, 0x00,0x30,0x00,0x00,
                  0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0
                };
                // stream_id in WF = 02:00:00:00:00:01 (the AX talker) but the
                // TB's bound sid = {02:00:00:ff:fe:00:00:02-derived}: rewrite
                // to the TB's bound stream {02:00:00:00:00:02, uid 0}
                uint8_t wf[86]; memcpy(wf, WF, 86);
                wf[11]=0x02; wf[23]=0x02;         // src mac + stream_id tail
                long f0 = axi_read(A_AVTPRX_FRX);
                long u0 = axi_read(0x6C0);
                inject_cnt(wf, 86);
                inject_cnt(wf, 86);
                printf("  [wire86] FRX delta=%ld UNSUP 0x%lx->0x%lx\n",
                       axi_read(A_AVTPRX_FRX)-f0, u0, (long)axi_read(0x6C0));
                // bisect: same 86-byte content PADDED to 124 (full last beat)
                uint8_t wfp[124]; memset(wfp, 0, sizeof wfp); memcpy(wfp, wf, 86);
                wfp[35]=0x30;  // keep stream_data_len 48 (content identical)
                f0 = axi_read(A_AVTPRX_FRX);
                inject_cnt(wfp, 124);
                printf("  [wire124pad] FRX delta=%ld\n", axi_read(A_AVTPRX_FRX)-f0);
                // bisect: mkaaf content TRUNCATED to 86 (partial last beat)
                f0 = axi_read(A_AVTPRX_FRX);
                inject_cnt(mkaaf(12, 0x05), 86);
                printf("  [mkaaf86] FRX delta=%ld\n", axi_read(A_AVTPRX_FRX)-f0);
            }
            kern = 0;
            pcm0 = axi_read(A_PCMRX_CNT);   // rebase: the 2ch default now
                                            // ACCEPTS the bisect probes above
            inject_cnt(mkaaf(8, 0x05), 124);
            inject_cnt(mkaaf(9, 0x05), 124);
            ck("prefilter: PCM ring advanced past TCAM drop",
               axi_read(A_PCMRX_CNT), pcm0 + 2);
            ck("prefilter: kernel DMA saw NOTHING", kern, 0);
            axi_write(A_TCAM_CMD, 0x00010000);          // commit|remove entry 0
        }

        // I2S playback: the injected pair (payload bytes 0..2 = ch0 S32BE)
        // emerges serialized on the DAC pins - decode the first non-zero
        // LEFT sample (Philips I2S: 1 delay bit after the LRCK fall).
        // LPF off for this check: wire-truth chans (2) would engage it and
        // the samples would arrive FILTERED, not byte-exact.
        {
            axi_write(0x72C, 0x0);
            // the first PDU's pairs can serialize before this decoder starts
            // (they sit ~1 audio frame in the CDC); inject a fresh PDU so
            // the decode window provably contains samples
            inject(mkaaf(6, 0x05), 120);
            // scan for the injected values (the CDC may hold a few stale
            // pairs from earlier sections now that the walker runs at the
            // full wire rate - stop-at-first-nonzero would grab those)
            uint32_t sample = 0; bool got_nz = false;
            int sclk_q = dut->i2s_dac_sclk_o, lrck_q = dut->i2s_dac_lrck_o;
            int bitcnt = -1; uint32_t acc = 0;
            for (int c = 0; c < 60000 && !got_nz; c++) {
                step();
                int sclk = dut->i2s_dac_sclk_o, lrck = dut->i2s_dac_lrck_o;
                if (sclk && !sclk_q) {                    // SCLK rising: sample
                    // textbook I2S chip (CS4344): the rise coincident with the
                    // LRCK transition is the delay slot; the MSB arrives on
                    // the NEXT rise (slots 1..24 here, bitcnt set at slot 0)
                    if (bitcnt >= 0 && bitcnt < 24) {
                        acc = (acc << 1) | (dut->i2s_dac_sdin_o & 1);
                        bitcnt++;
                        if (bitcnt == 24) {
                            if (acc == 0x303132 || acc == 0x505152) {
                                sample = acc; got_nz = true;
                            }
                            bitcnt = -1;
                        }
                    }
                    if (lrck_q && !lrck) { bitcnt = 0; acc = 0; }  // LEFT begins
                    lrck_q = lrck;
                }
                sclk_q = sclk;
            }
            // the FIFO drains continuously, so the decoder catches pair 0
            // (payload bytes 0..2 = 0x303132) or pair 1 (bytes 32..34 =
            // 0x505152) - both prove byte-exact serialization
            ck("I2S left sample from payload",
               sample == 0x303132 || sample == 0x505152, 1);
            axi_write(0x72C, 0x1);
        }

        // wrong-rate PDU: UNSUPPORTED_FORMAT ticks, FRAMES_RX does not,
        // and NOTHING more enters the PCM ring
        // ---- lwSRP TX pair through the FULL egress (MVRP-eater hunt) ----
        // enable the engine (prompt declare pair fires on the rising edge)
        // and count what actually reaches the MAC port per ethertype.
        {
            axi_write(0x684, 0x002);            // SR VID 2
            axi_write(0x688, 0xF0001234); axi_write(0x68C, 0x91E0);
            axi_write(0x680, 0x00F);            // en | talker | queue
            int n22ea = 0, n88f5 = 0, nother = 0;
            std::vector<uint64_t> cur;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 120000; c++) {
                lo();
                bool acc = dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready;
                uint64_t d = dut->m_axis_mac_tx_tdata;
                bool l = dut->m_axis_mac_tx_tlast;
                hi();
                if (acc) {
                    cur.push_back(d);
                    if (l) {
                        if (cur.size() >= 2) {
                            int et = (int)((cur[1] >> 32) & 0xFF) << 8
                                   | (int)((cur[1] >> 40) & 0xFF);
                            if (et == 0x22EA) n22ea++;
                            else if (et == 0x88F5) n88f5++;
                            else nother++;
                        }
                        cur.clear();
                    }
                }
            }
            printf("  [lwsrp-egress] other-ethertype frames=%d\n", nother);
            printf("  [lwsrp-egress] MSRP=%d MVRP=%d at the MAC port\n", n22ea, n88f5);
            ck("lwsrp: MSRP pair half reaches MAC", n22ea >= 1, 1);
            ck("lwsrp: MVRP pair half reaches MAC", n88f5 >= 1, 1);
            axi_write(0x680, 0x00C);            // disable again (LV pair drains)
            for (int c = 0; c < 5000; c++) step();
        }

        // ---- link up/down via LINK_CTRL + reset-epoch canary ----
        {
            enum { A_LINK_CTRL = 0x71C, A_RST_EPOCH = 0x720 };
            long ep = axi_read(A_RST_EPOCH);
            ck("epoch = 1 (one reset release since bitstream)", ep, 1);
            // AVB_IF counters live in the AECP push block; read via GET_COUNTERS
            // is heavy here - instead verify the ADP reacts (depart on down,
            // re-advertise on up) via its diag pulses + the counters through
            // the aecp TB. Here: toggle and confirm no datapath disturbance.
            axi_write(A_LINK_CTRL, 0x0);          // daemon says link DOWN
            for (int c = 0; c < 200; c++) step();
            ck("LINK_CTRL reads back 0 (shadowed)", axi_read(A_LINK_CTRL), 0);
            axi_write(A_LINK_CTRL, 0x1);          // link UP again
            for (int c = 0; c < 200; c++) step();
            ck("LINK_CTRL reads back 1 (shadowed)", axi_read(A_LINK_CTRL), 1);
            ck("epoch unchanged by link toggles", axi_read(A_RST_EPOCH), ep);
            ck("datapath alive after link toggle (ID)", axi_read(A_ID), 0x4D494C4E);
            // board-name overlay CSRs (shadowed RW)
            axi_write(0x724, 0x59545241);   // "ARTY"
            axi_write(0x728, 0x00000000);
            ck("ENT_NAME_LO reads back", axi_read(0x724), 0x59545241);
            // playback biquad LPF: on by default; BYPASS for the legacy
            // byte-exact I2S checks below (the filter alters samples)
            ck("LPF_CTRL default on", axi_read(0x72C), 1);
            axi_write(0x72C, 0x0);
            ck("LPF_CTRL bypass set", axi_read(0x72C), 0);
        }

        pcm.clear(); pcm_last = false;
        long frx_before = axi_read(A_AVTPRX_FRX);
        long uns_before = (long)(axi_read(A_AVTPRX_ERR) >> 8);
        long pcm_before = axi_read(A_PCMRX_CNT);
        inject(mkaaf(7, 0x07), 120);
        ck("UNSUPPORTED_FORMAT +1 (0x6C0)", (long)(axi_read(A_AVTPRX_ERR) >> 8) - uns_before, 1);
        ck("FRAMES_RX unchanged by wrong-rate", axi_read(A_AVTPRX_FRX), frx_before);
        ck("no PCM for rejected PDU", (long)pcm.size(), 0);
        ck("PCMRX unchanged by wrong-rate", axi_read(A_PCMRX_CNT), pcm_before);


    // ---------------------------------------------------------------- //
    // CRF Media Clock Input engine (Milan 7.3.2): parse/validate/lock    //
    // ---------------------------------------------------------------- //
    printf("\n[CRF] Milan CRF media clock input engine\n");
    {
        enum { A_CRF_CTRL = 0x738, A_CRF_SIDLO = 0x73C, A_CRF_SIDHI = 0x740,
               A_CRF_DELTA = 0x744, A_CRF_RATE = 0x748, A_CRF_STATUS = 0x74C };
        // provision the sink: stream_id 02:00:00:00:00:02 uid 1, enable
        axi_write(A_CRF_SIDLO, 0x00020001);
        axi_write(A_CRF_SIDHI, 0x02000000);
        axi_write(A_CRF_CTRL,  0x1);

        uint64_t crf_ts = 1000000000ULL;              // 1 s
        uint8_t  crf_seq = 0;
        auto mkcrf = [&](uint64_t ts, uint8_t seq, uint16_t ival,
                         const uint8_t* sid6ovr) {
            static uint8_t f[64];
            memset(f, 0, sizeof f);
            const uint8_t dmac[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x03};
            memcpy(f, dmac, 6);
            const uint8_t src[6] = {0x02,0x00,0x00,0x00,0x00,0x02};
            memcpy(f+6, src, 6);
            f[12]=0x22; f[13]=0xF0;
            f[14]=0x04;                               // CRF subtype
            f[15]=0x80;                               // sv
            f[16]=seq;
            f[17]=0x01;                               // CRF_AUDIO_SAMPLE
            const uint8_t sid[8] = {0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x01};
            memcpy(f+18, sid, 8);
            if (sid6ovr) memcpy(f+18, sid6ovr, 8);
            f[26]=0x00; f[27]=0x00; f[28]=0xBB; f[29]=0x80;   // pull0|48000
            f[30]=0x00; f[31]=0x08;                   // crf_data_length 8
            f[32]=(uint8_t)(ival>>8); f[33]=(uint8_t)ival;    // interval
            for (int i = 0; i < 8; i++) f[34+i] = (uint8_t)(ts >> (8*(7-i)));
            return f;
        };
        auto send_crf = [&](uint16_t ival = 96, const uint8_t* sid = nullptr) {
            inject(mkcrf(crf_ts, crf_seq, ival, sid), 64);
            crf_seq++;
            crf_ts += 2000000ULL + 1000ULL;           // 2 ms + 1000 ns skew
        };

        send_crf();
        ck("CRF pdu_count 1", axi_read(A_CRF_STATUS) >> 16, 1);
        ck("CRF no fmt/seq errors", axi_read(A_CRF_STATUS) & 0xFFFF, 0);
        ck("CRF not locked yet", axi_read(A_CRF_CTRL) >> 31, 0);
        int32_t d1 = (int32_t)axi_read(A_CRF_DELTA);
        ck("CRF delta captured (nonzero)", d1 != 0, 1);

        for (int k = 0; k < 7; k++) send_crf();
        ck("CRF locked after 8 clean PDUs", axi_read(A_CRF_CTRL) >> 31, 1);
        ck("CRF pdu_count 8", axi_read(A_CRF_STATUS) >> 16, 8);

        // malformed: wrong timestamp_interval -> fmt_err, no count
        send_crf(160);
        ck("CRF fmt_err 1 (wrong interval)", (axi_read(A_CRF_STATUS) >> 8) & 0xFF, 1);
        ck("CRF count unchanged by bad fmt", axi_read(A_CRF_STATUS) >> 16, 8);
        ck("CRF still locked (no timeout)", axi_read(A_CRF_CTRL) >> 31, 1);

        // foreign stream_id -> completely ignored
        const uint8_t alien[8] = {0x02,0x00,0x00,0x00,0x00,0x07,0x00,0x00};
        send_crf(96, alien);
        ck("CRF foreign sid ignored", axi_read(A_CRF_STATUS) >> 16, 8);

        // sequence gap -> seq_err
        crf_seq += 3;
        send_crf();
        ck("CRF seq_err 1", axi_read(A_CRF_STATUS) & 0xFF, 1);

        // rate window: 260 more exact-cadence PDUs; the +1000 ns/PDU skew
        // must read back as 256 * 1000 ns per 512 ms window
        for (int k = 0; k < 260; k++) send_crf();
        ck("CRF rate = +256000 ns/window", (int32_t)axi_read(A_CRF_RATE), 256000);

        // CRF header-rule legs (traceability CRF-5, IEEE 1722-2016
        // 10.4.2-10.4.6 + Milan 7.3.2), through the REAL RX path
        // (MAC AXIS -> avtp_stream_parser -> KL_crf_rx):
        //   sv (10.4.2) gates acceptance entirely; mr (10.4.3) / fs
        //   (10.4.4) / tu (10.4.5) toggles are format-valid and must not
        //   break acceptance, sequence tracking or lock. The engine is the
        //   MEASUREMENT half: it deliberately ignores mr/fs (a re-lock
        //   response is the CRF-8/M-CLK-3 actuator work — matrix stays
        //   open there, not here).
        {
            long cnt5   = axi_read(A_CRF_STATUS) >> 16;
            long errs5  = axi_read(A_CRF_STATUS) & 0xFFFF;
            // mr toggle set
            uint8_t* fr = mkcrf(crf_ts, crf_seq, 96, nullptr);
            fr[15] = 0x80 | 0x08;                 // sv + mr
            inject(fr, 64); crf_seq++; crf_ts += 2000000ULL + 1000ULL;
            // fs + tu set
            fr = mkcrf(crf_ts, crf_seq, 96, nullptr);
            fr[15] = 0x80 | 0x02 | 0x01;          // sv + fs + tu
            inject(fr, 64); crf_seq++; crf_ts += 2000000ULL + 1000ULL;
            ck("CRF-5: mr/fs/tu PDUs accepted (+2)",
               axi_read(A_CRF_STATUS) >> 16, cnt5 + 2);
            ck("CRF-5: no fmt/seq errors from mr/fs/tu",
               axi_read(A_CRF_STATUS) & 0xFFFF, errs5);
            ck("CRF-5: lock survives mr/fs/tu", axi_read(A_CRF_CTRL) >> 31, 1);
            // sv=0 (10.4.2): stream-data invalid -> ignored entirely, and
            // it must not disturb the sequence walk of the next real PDU
            fr = mkcrf(crf_ts, crf_seq, 96, nullptr);
            fr[15] = 0x00;                        // sv=0
            inject(fr, 64);                       // seq NOT consumed
            ck("CRF-5: sv=0 PDU ignored",
               axi_read(A_CRF_STATUS) >> 16, cnt5 + 2);
            send_crf();
            ck("CRF-5: clean seq resumes after sv=0",
               axi_read(A_CRF_STATUS) & 0xFFFF, errs5);
            ck("CRF-5: resumed PDU counted",
               axi_read(A_CRF_STATUS) >> 16, cnt5 + 3);
        }

        // disable -> ignored
        axi_write(A_CRF_CTRL, 0x0);
        long cnt = axi_read(A_CRF_STATUS) >> 16;
        send_crf();
        ck("CRF disabled = inert", axi_read(A_CRF_STATUS) >> 16, cnt);
    }

    // ---------------------------------------------------------------- //
    // [SERVO] media-clock servo INTEGRATION (2026-07-23 bench escape):  //
    // AECP SET_CLOCK_SOURCE(2) through the REAL RX path + CRF lock must //
    // take KL_mmcm_drp_servo out of IDLE (0x8F8). The aecp TB pins      //
    // clk_src_o and the mmcm_servo TB pins the FSM - this pins the      //
    // datapath wiring BETWEEN them, which no TB covered.                //
    // ---------------------------------------------------------------- //
    printf("\n[SERVO] clock_source=2 -> servo leaves IDLE (0x8F8)\n");
    {
        enum { A_CRF_CTRL = 0x738, A_CRF_SIDLO = 0x73C, A_CRF_SIDHI = 0x740,
               A_MCSRV_STAT = 0x8F8 };
        dut->i_mmcm_locked = 1;
        for (int c = 0; c < 8; c++) step();
        ck("SERVO idle before (state 0, trim 0, locked bit follows later)",
           axi_read(A_MCSRV_STAT) & 0x7, 0);

        // re-lock the CRF sink (sid {..:02, uid 1} per the [CRF] section)
        axi_write(A_CRF_SIDLO, 0x00020001);
        axi_write(A_CRF_SIDHI, 0x02000000);
        axi_write(A_CRF_CTRL,  0x1);
        uint64_t ts = 5000000000ULL; uint8_t sq = 0;
        uint8_t f[64];
        for (int k = 0; k < 9; k++) {
            memset(f, 0, sizeof f);
            const uint8_t dmac[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x03};
            memcpy(f, dmac, 6);
            const uint8_t src[6] = {0x02,0x00,0x00,0x00,0x00,0x02};
            memcpy(f+6, src, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0x04; f[15]=0x80; f[16]=sq++;
            f[17]=0x01;
            const uint8_t sid[8] = {0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x01};
            memcpy(f+18, sid, 8);
            f[28]=0xBB; f[29]=0x80; f[31]=0x08; f[32]=0; f[33]=96;
            for (int i = 0; i < 8; i++) f[34+i] = (uint8_t)(ts >> (8*(7-i)));
            inject(f, 64);
            ts += 2000000ULL;
        }
        ck("SERVO precondition: CRF locked", axi_read(A_CRF_CTRL) >> 31, 1);

        // AECP SET_CLOCK_SOURCE(CLOCK_DOMAIN[0], index 2) on the wire
        uint8_t a[64]; memset(a, 0, sizeof a);
        const uint8_t emac[6] = {0x02,0x00,0x00,0x00,0x00,0x01};
        const uint8_t cmac[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
        memcpy(a, emac, 6); memcpy(a+6, cmac, 6);
        a[12]=0x22; a[13]=0xF0; a[14]=0xFB; a[15]=0x00;      // AECP AEM_COMMAND
        a[16]=0x00; a[17]=20;                                 // status0 | cdl 20
        const uint8_t teid[8]={0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
        memcpy(a+18, teid, 8);
        const uint8_t ceid[8]={0x68,0x05,0xCA,0xFF,0xFE,0x95,0xB2,0xD1};
        memcpy(a+26, ceid, 8);
        a[34]=0x30; a[35]=0x01;                               // seq
        a[36]=0x00; a[37]=22;                                 // SET_CLOCK_SOURCE
        a[38]=0x00; a[39]=0x24; a[40]=0; a[41]=0;             // CLOCK_DOMAIN[0]
        a[42]=0x00; a[43]=0x02; a[44]=0; a[45]=0;             // index 2
        inject(a, 64);
        for (int c = 0; c < 40; c++) step();

        uint32_t sv = axi_read(A_MCSRV_STAT);
        ck("SERVO left IDLE after SET_CLOCK_SOURCE(2)", (sv & 0x7) != 0, 1);
        ck("SERVO sees MMCM locked (bit5)", (sv >> 5) & 1, 1);

        // back to internal: SET_CLOCK_SOURCE(0) -> servo returns to IDLE
        a[34]=0x30; a[35]=0x02; a[43]=0x00;
        inject(a, 64);
        for (int c = 0; c < 40; c++) step();
        ck("SERVO back to IDLE at clock_source 0",
           axi_read(A_MCSRV_STAT) & 0x7, 0);
        axi_write(A_CRF_CTRL, 0x0);
        dut->i_mmcm_locked = 0;
    }

    // ---------------------------------------------------------------- //
    // CRF Media Clock Output engine (Milan 7.3.1): KL_crf_tx emits on   //
    // the audio-MMCM 96-sample grid; wire frames byte-checked, then     //
    // looped back into KL_crf_rx for the tx->rx closure.                //
    // ---------------------------------------------------------------- //
    printf("\n[CRFTX] Milan CRF media clock output engine + rx loopback\n");
    {
        enum { A_CRFT_CTRL = 0x750, A_CRFT_SIDLO = 0x754, A_CRFT_SIDHI = 0x758,
               A_CRFT_DMLO = 0x75C, A_CRFT_DMHI = 0x760, A_CRFT_COUNT = 0x764,
               A_CRF_CTRL = 0x738, A_CRF_SIDLO = 0x73C, A_CRF_SIDHI = 0x740,
               A_CRF_DELTA = 0x744, A_CRF_STATUS = 0x74C };

        // silence the AAF talker (preserve VID 2) so the TX side carries
        // control-lane frames only; the subtype filter below guards the rest
        axi_write(0x654, 0x00020000);

        // provision: sid {02:00:00:00:00:01, uid 1}, DMAC 91:E0:F0:00:2A:07
        axi_write(A_CRFT_SIDLO, 0x00010001);
        axi_write(A_CRFT_SIDHI, 0x02000000);
        axi_write(A_CRFT_DMLO,  0xF0002A07);
        axi_write(A_CRFT_DMHI,  0x000091E0);
        ck("CRFT count starts 0", axi_read(A_CRFT_COUNT), 0);

        // station MAC as the wire will carry it (instantiation byte-reverse)
        uint32_t malo = axi_read(0x108), mahi = axi_read(0x10C);
        const uint8_t smac[6] = {
            (uint8_t)malo, (uint8_t)(malo>>8), (uint8_t)(malo>>16),
            (uint8_t)(malo>>24), (uint8_t)mahi, (uint8_t)(mahi>>8) };

        ck("CRFT sid readback (shadow)", axi_read(A_CRFT_SIDLO), 0x00010001);
        ck("CRFT dmac readback (shadow)", axi_read(A_CRFT_DMLO), 0xF0002A07);

        // enable LAST, then capture immediately: no cycles may pass in
        // between or the first PDUs (seq 0..) drain unseen
        axi_write(A_CRFT_CTRL, 0x1);
        ck("CRFT_CTRL readback en=1", axi_read(A_CRFT_CTRL), 1);

        // one CRF PDU per 512*96 = 49152 audio(=axis) cycles
        const int NCAP = 10;
        std::vector<std::array<uint8_t,64>> crf; std::vector<uint8_t> cur;
        uint8_t crf_keep = 0;
        dut->m_axis_mac_tx_tready = 1;
        for (long c = 0; c < 700000 && (int)crf.size() < NCAP; c++) {
            step();
            if (dut->m_axis_mac_tx_tvalid) {
                uint64_t d = dut->m_axis_mac_tx_tdata;
                for (int j = 0; j < 8; j++) cur.push_back((uint8_t)(d >> (8*j)));
                if (dut->m_axis_mac_tx_tlast) {
                    if (cur.size() >= 42 && cur[12]==0x22 && cur[13]==0xF0
                        && cur[14]==0x04) {
                        std::array<uint8_t,64> f{};
                        for (size_t k = 0; k < cur.size() && k < 64; k++) f[k] = cur[k];
                        crf.push_back(f);
                        crf_keep = dut->m_axis_mac_tx_tkeep;
                    }
                    cur.clear();
                }
            }
        }
        ck("CRFTX captured 10 PDUs", (long)crf.size(), NCAP);
        ck("CRFTX 60-byte frame (last keep 0x0F)", crf_keep, 0x0F);
        ck("CRFT count == captured", axi_read(A_CRFT_COUNT), NCAP);

        // byte-exact structural golden on every captured frame + seq chain
        long ok_hdr = 1, ok_seq = 1, ok_pad = 1;
        const uint8_t dmac[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x07};
        const uint8_t sid8[8] = {0x02,0x00,0x00,0x00,0x00,0x01,0x00,0x01};
        for (int k = 0; k < (int)crf.size(); k++) {
            const uint8_t* f = crf[k].data();
            if (memcmp(f, dmac, 6) || memcmp(f+6, smac, 6)) ok_hdr = 0;
            if (f[14]!=0x04 || f[15]!=0x80 || f[17]!=0x01) ok_hdr = 0;
            if (memcmp(f+18, sid8, 8)) ok_hdr = 0;
            if (f[26]!=0x00||f[27]!=0x00||f[28]!=0xBB||f[29]!=0x80) ok_hdr = 0;
            if (f[30]!=0x00||f[31]!=0x08||f[32]!=0x00||f[33]!=0x60) ok_hdr = 0;
            if (f[16] != (uint8_t)k) ok_seq = 0;
            for (int p = 42; p < 60; p++) if (f[p]) ok_pad = 0;
        }
        ck("CRFTX header/sid/base/dlen/ival byte-exact", ok_hdr, 1);
        ck("CRFTX sequence_num 0..9 consecutive", ok_seq, 1);
        ck("CRFTX zero pad to 60B", ok_pad, 1);

        // timestamp grid: strictly monotone, consecutive deltas equal to
        // the 49152-cycle event spacing within 1 ns (fractional-incr slack)
        auto get_ts = [&](int k) {
            uint64_t t = 0;
            for (int j = 0; j < 8; j++) t = (t << 8) | crf[k][34+j];
            return t;
        };
        long ok_mono = crf.size() >= 2 ? 1 : 0,
             ok_grid = crf.size() >= 2 ? 1 : 0;
        uint64_t d0 = crf.size() >= 2 ? get_ts(1) - get_ts(0) : 0;
        for (int k = 1; k < (int)crf.size(); k++) {
            uint64_t dk = get_ts(k) - get_ts(k-1);
            if (get_ts(k) <= get_ts(k-1)) ok_mono = 0;
            if (dk + 1 < d0 || dk > d0 + 1) ok_grid = 0;
        }
        ck("CRFTX ts strictly monotone", ok_mono, 1);
        ck("CRFTX ts grid uniform (event-locked)", ok_grid, 1);
        ck("CRFTX ts spacing nonzero", d0 > 0 ? 1 : 0, 1);

        // ---- loopback closure: our wire PDUs into KL_crf_rx ----
        axi_write(A_CRF_SIDLO, 0x00010001);
        axi_write(A_CRF_SIDHI, 0x02000000);
        axi_write(A_CRF_CTRL,  0x1);
        long pdu0 = axi_read(A_CRF_STATUS) >> 16;
        long seq0 = axi_read(A_CRF_STATUS) & 0xFF;
        long fmt0 = (axi_read(A_CRF_STATUS) >> 8) & 0xFF;
        for (int k = 0; k < (int)crf.size(); k++) inject(crf[k].data(), 64);
        long st = axi_read(A_CRF_STATUS);
        ck("CRFRX counted all looped PDUs", (st >> 16) - pdu0, NCAP);
        ck("CRFRX fmt clean on our wire format", ((st >> 8) & 0xFF) - fmt0, 0);
        ck("CRFRX at most the sid-switch seq gap", ((st & 0xFF) - seq0) <= 1, 1);
        ck("CRFRX locked on our stream", axi_read(A_CRF_CTRL) >> 31, 1);
        // Milan PTO: talker future-dates ts by the presentation offset
        // (reset 2 ms); the LAST looped PDU was captured just before the
        // injects, so its delta ~= +PTO minus the short capture->inject lag
        int32_t dlt = (int32_t)axi_read(A_CRF_DELTA);
        ck("CRFRX delta ~= +PTO (Milan future-dating)",
           (dlt > 1500000) && (dlt <= 2000000), 1);

        // disable -> the event grid keeps running, the wire goes silent
        axi_write(A_CRFT_CTRL, 0x0);
        long cnt_off = axi_read(A_CRFT_COUNT);
        long stray = 0;
        for (long c = 0; c < 120000; c++) {
            step();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tlast) stray++;
        }
        ck("CRFTX disabled = silent wire", stray, 0);
        ck("CRFTX disabled = count frozen", axi_read(A_CRFT_COUNT), cnt_off);
    }

    // ---------------------------------------------------------------- //
    // ACMP sink-1 (CRF) bind chain: CONNECT_RX uid=1 through the whole  //
    // datapath provisions the CRF engine (sid + enable) with the CSR    //
    // pair CLEARED - the Milan bind path, no manual pokes.              //
    // ---------------------------------------------------------------- //
    printf("\n[S1CRF] ACMP sink-1 bind provisions the CRF engine\n");
    {
        enum { A_CRF_CTRL = 0x738, A_CRF_SIDLO = 0x73C, A_CRF_SIDHI = 0x740,
               A_CRF_STATUS = 0x74C, A_ACMPL_STATE = 0x6A4 };
        axi_write(A_CRF_CTRL,  0x0);          // CSR lever OFF
        axi_write(A_CRF_SIDLO, 0x0);
        axi_write(A_CRF_SIDHI, 0x0);
        // (locked bit may linger up to the 100 ms silence timeout from the
        // earlier loopback - the en bit is the provisioning truth here)
        ck("[S1CRF] CSR enable cleared", axi_read(A_CRF_CTRL) & 1, 0);

        const uint64_t S1SID = 0xAABBCCDD00110001ULL;
        auto mkconn = [&](uint8_t msg, uint16_t seq) {
            static uint8_t f[70];
            memset(f, 0, sizeof f);
            const uint8_t dst[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            const uint8_t src[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f, dst, 6); memcpy(f+6, src, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC;   // ACMP
            f[15]=msg;                            // CONNECT_RX=6 / DISC=8
            f[16]=0x00; f[17]=44;                 // status0 | cdl 44
            for (int j = 0; j < 8; j++) f[18+j] = (uint8_t)(S1SID >> (8*(7-j)));
            const uint8_t ctl[8] = {0x68,0x05,0xCA,0xFF,0xFE,0x95,0xB2,0xD1};
            memcpy(f+26, ctl, 8);
            const uint8_t tk[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x09};
            memcpy(f+34, tk, 8);
            const uint8_t ls[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, ls, 8);                  // listener = this entity
            f[50]=0x00; f[51]=0x11;               // talker_unique_id
            f[52]=0x00; f[53]=0x01;               // listener_unique_id = 1
            const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x09};
            memcpy(f+54, dm, 6);
            f[62]=(uint8_t)(seq>>8); f[63]=(uint8_t)seq;
            return f;
        };
        dut->m_axis_mac_tx_tready = 1;
        inject(mkconn(6, 0x300), 70);
        for (int c = 0; c < 4000; c++) step();   // response + settle
        ck("[S1CRF] ACMPL bit31 = sink-1 bound", axi_read(A_ACMPL_STATE) >> 31, 1);

        // CRF PDUs on the ACMP-provisioned sid: engine counts + locks
        long pdu0 = axi_read(A_CRF_STATUS) >> 16;
        uint64_t ts = 5000000000ULL; uint8_t sq = 0;
        for (int k = 0; k < 9; k++) {
            uint8_t f[64]; memset(f, 0, sizeof f);
            const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x09};
            memcpy(f, dm, 6);
            const uint8_t sr[6] = {0x02,0x00,0x00,0x00,0x00,0x09};
            memcpy(f+6, sr, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0x04; f[15]=0x80;
            f[16]=sq++; f[17]=0x01;
            for (int j = 0; j < 8; j++) f[18+j]=(uint8_t)(S1SID >> (8*(7-j)));
            f[26]=0x00; f[27]=0x00; f[28]=0xBB; f[29]=0x80;
            f[30]=0x00; f[31]=0x08; f[32]=0x00; f[33]=0x60;
            for (int j = 0; j < 8; j++) f[34+j]=(uint8_t)(ts >> (8*(7-j)));
            inject(f, 64);
            ts += 2000000ULL;
        }
        ck("[S1CRF] engine counted on bound sid",
           (long)(axi_read(A_CRF_STATUS) >> 16) - pdu0, 9);
        ck("[S1CRF] locked via ACMP provisioning", axi_read(A_CRF_CTRL) >> 31, 1);

        // unbind: engine loses its enable, further PDUs ignored
        inject(mkconn(8, 0x301), 70);
        for (int c = 0; c < 4000; c++) step();
        ck("[S1CRF] unbind clears bit31", axi_read(A_ACMPL_STATE) >> 31, 0);
        long pdu1 = axi_read(A_CRF_STATUS) >> 16;
        {
            uint8_t f[64]; memset(f, 0, sizeof f);
            const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x09};
            memcpy(f, dm, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0x04; f[15]=0x80;
            f[16]=sq; f[17]=0x01;
            for (int j = 0; j < 8; j++) f[18+j]=(uint8_t)(S1SID >> (8*(7-j)));
            f[26]=0x00; f[27]=0x00; f[28]=0xBB; f[29]=0x80;
            f[30]=0x00; f[31]=0x08; f[32]=0x00; f[33]=0x60;
            inject(f, 64);
        }
        ck("[S1CRF] post-unbind PDU ignored",
           (long)(axi_read(A_CRF_STATUS) >> 16), pdu1);
    }

    }

    // ================================================================
    // [LINKG] link-guard integration drill (LAST section: arming is
    // permanent, so the drill ends with the guard disabled to keep the
    // eff_link/reinit state inert for any code after it)
    // ================================================================
    {
        printf("\n[LINKG] link guard integration drill\n");
        // drive the eth toggles alive -> the guard arms (real DEAD=4096)
        auto steps_tgl = [&](int n) {
            for (int i = 0; i < n; i++) {
                if ((g_step & 1) == 0) dut->i_ethrx_tgl ^= 1;
                if ((g_step % 3) == 0) dut->i_ethtx_tgl ^= 1;
                step();
            }
        };
        steps_tgl(64);
        ck("[LINKG] armed alive", (long)(axi_read(0x774) & 0xFF), 0x03);
        ck("[LINKG] reinit pin idle", (long)dut->o_mac_reinit, 0);

        // freeze drill: CSR-faked clock death -> HOLD + reinit pin
        axi_write(0x71C, 0x9);                       // sw_link | freeze
        steps_tgl(4200);                             // > DEAD_CYC_C
        {
            uint32_t st = axi_read(0x774);
            ck("[LINKG] freeze bounce",  (long)(st >> 16), 1);
            ck("[LINKG] freeze state",   (long)((st >> 4) & 3), 1);   // HOLD
            ck("[LINKG] freeze grst",    (long)((st >> 6) & 1), 1);
            ck("[LINKG] freeze alive",   (long)(st & 3), 0);
        }
        ck("[LINKG] reinit pin held", (long)dut->o_mac_reinit, 1);

        // unfreeze while DISABLED: reinit drops immediately (settle
        // short-circuit), clocks re-arm alive under the disable
        axi_write(0x71C, 0x5);                       // sw_link | dis
        steps_tgl(8);
        ck("[LINKG] disable releases pin", (long)dut->o_mac_reinit, 0);
        steps_tgl(4200);                             // alive restores
        // re-enable with clocks alive: RUN, no new episode
        axi_write(0x71C, 0x1);
        steps_tgl(64);
        {
            uint32_t st = axi_read(0x774);
            ck("[LINKG] re-enable RUN", (long)((st >> 4) & 3), 0);
            ck("[LINKG] re-enable alive", (long)(st & 3), 3);
            ck("[LINKG] no extra bounce", (long)(st >> 16), 1);
        }
        ck("[LINKG] reinit pin clear", (long)dut->o_mac_reinit, 0);
        // park disabled so the static toggles stay inert from here on
        axi_write(0x71C, 0x5);
    }

    // --- RMON: MAC-boundary good-frame lanes -> ethernet_events -> snapshot ---
    // Silicon "never worked" root cause (2026-07-22): the LiteX glue ties
    // i_mac_events to 0, so every counter lane was structurally silent. The
    // datapath now derives TX/RX_FIFO_GOOD_FRAME from its own MAC AXIS
    // boundary handshake - this case pushes frames through the REAL boundary
    // ports (the same path the SoC uses) and reads the latched lanes back
    // over AXI. On the pre-fix RTL the good-frame checks read 0 and FAIL.
    printf("[RMON] boundary good-frame lanes + STATS_CTRL snapshot\n");
    {
        enum { A_STATS_CTRL = 0x200, A_STAT_TX_UNDER = 0x210,
               A_STAT_TX_GOOD = 0x21C, A_STAT_RX_GOOD = 0x230 };
        // counter reset, then a clean baseline snapshot: every lane 0
        axi_write(A_STATS_CTRL, 0x2);
        for (int i = 0; i < 8; i++) step();
        axi_write(A_STATS_CTRL, 0x1);
        ck("[RMON] baseline TX_GOOD 0", axi_read(A_STAT_TX_GOOD), 0);
        ck("[RMON] baseline RX_GOOD 0", axi_read(A_STAT_RX_GOOD), 0);
        // traffic through the real MAC boundary: 3 TX out, 2 RX in
        for (int k = 0; k < 3; k++) {
            Res t = run_tx(vlan_frame(/*pcp=*/3, (uint8_t)(0x30 + k)), 400);
            ck("[RMON] TX frame drained to MAC port", t.got ? 1 : 0, 1);
        }
        for (int k = 0; k < 2; k++)
            (void)run_rx(vlan_frame(/*pcp=*/1, (uint8_t)(0x40 + k), 0x0806), 400);
        // the snapshot is a latch: lanes hold until software re-arms
        ck("[RMON] lanes latched (pre-re-arm TX_GOOD still 0)",
           axi_read(A_STAT_TX_GOOD), 0);
        axi_write(A_STATS_CTRL, 0x1);
        ck("[RMON] TX_GOOD == 3 (0x21C)", axi_read(A_STAT_TX_GOOD), 3);
        ck("[RMON] RX_GOOD == 2 (0x230)", axi_read(A_STAT_RX_GOOD), 2);
        ck("[RMON] UNDERFLOW == 0 (0x210)", axi_read(A_STAT_TX_UNDER), 0);
        // i_mac_events: MAC-internal lanes pass through; its good-frame bits
        // are IGNORED (boundary derivation owns them - no double count)
        dut->i_mac_events = (1u << 0) | (1u << 3) | (1u << 8);
        step();
        dut->i_mac_events = 0;
        for (int i = 0; i < 4; i++) step();
        axi_write(A_STATS_CTRL, 0x1);
        ck("[RMON] ext UNDERFLOW pulse == 1", axi_read(A_STAT_TX_UNDER), 1);
        ck("[RMON] ext TX_GOOD bit ignored", axi_read(A_STAT_TX_GOOD), 3);
        ck("[RMON] ext RX_GOOD bit ignored", axi_read(A_STAT_RX_GOOD), 2);
        // MAC-reinit release (LINK_CTRL[1] pulse, guard parked disabled)
        // invalidates the snapshot: all-zero = "no valid snapshot"
        axi_write(0x71C, 0x7);                     // sw_link | reinit | dis
        for (int i = 0; i < 8; i++) step();
        axi_write(0x71C, 0x5);                     // release -> invalidate edge
        for (int i = 0; i < 8; i++) step();
        ck("[RMON] reinit release zeroes TX_GOOD", axi_read(A_STAT_TX_GOOD), 0);
        ck("[RMON] reinit release zeroes RX_GOOD", axi_read(A_STAT_RX_GOOD), 0);
    }

    printf("======================================================================\n");
    printf("milan_datapath: %ld checks, %ld failures\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
