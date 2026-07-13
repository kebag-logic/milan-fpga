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
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <vector>
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
static void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; eval(); }
static void hi() { dut->axis_clk = 1; dut->gtx_clk = 1; eval(); }
static void step() { lo(); hi(); }

// ---- AXI4-Lite BFM (same protocol/timing as the milan_csr harness): sample the
//      *ready when the clock is low (combinational), then pulse the rising edge to
//      commit the transfer. AW and W are held valid together until both readys
//      assert (milan_csr is a single-outstanding slave that accepts them jointly). ----
static void axi_write(uint16_t a, uint32_t d) {
    dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
    dut->s_axi_wdata = d;  dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
    dut->s_axi_bready = 1;
    for (int g = 0; g < 64; g++) {
        lo(); bool acc = dut->s_axi_awready && dut->s_axi_wready; hi();
        if (acc) break;
    }
    dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
    for (int g = 0; g < 64; g++) { lo(); bool bv = dut->s_axi_bvalid; hi(); if (bv) break; }
    dut->s_axi_bready = 0;
}

static uint32_t axi_read(uint16_t a) {
    dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
    for (int g = 0; g < 64; g++) { lo(); bool acc = dut->s_axi_arready; hi(); if (acc) break; }
    dut->s_axi_arvalid = 0;
    uint32_t d = 0;
    for (int g = 0; g < 64; g++) {
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
        step();
        if (dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready) idx++;
        if (dut->m_axis_rx_tvalid && dut->m_axis_rx_tready) {
            r.data.push_back(dut->m_axis_rx_tdata); r.got = true;
        }
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
    ck("VERSION",       axi_read(A_VERSION), 0x00010003);
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
                v |= (uint64_t)g[bt*8+j] << (8*(7-j));
            gb.push_back(v);
        }
        std::vector<uint64_t> ts;
        size_t idx = 0;
        dut->m_axis_ts_tready = 1;
        for (int c = 0; c < 600; c++) {
            if (idx < gb.size()) {
                dut->s_axis_mac_rx_tdata = gb[idx];
                dut->s_axis_mac_rx_tkeep = (idx == gb.size()-1) ? 0xF0 : 0xFF;
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
            ck("ts word1 seq=0xBEEF",   (unsigned long)((ts[1] >> 8) & 0xFFFF), 0xBEEFUL);
        }
    }

    printf("======================================================================\n");
    printf("milan_datapath: %ld checks, %ld failures\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
