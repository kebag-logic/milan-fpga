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
        // any TX response the datapath produces
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
            f[30]=0x02;                                          // format INT32
            f[31]=(uint8_t)(nsr << 4);                           // nsr
            f[32]=8;                                             // channels
            f[33]=32;                                            // bit depth
            f[34]=0x00; f[35]=0x40;                              // data_len
            return f;
        };
        inject(mkaaf(5, 0x05), 120);
        ck("FRAMES_RX 1 (0x6BC)", axi_read(A_AVTPRX_FRX), 1);
        ck("locked + MEDIA_LOCKED=1 (0x6B8)",
           axi_read(A_AVTPRX_STAT) & 0xFF01, 0x0101);
        ck("no errors (0x6C0)", axi_read(A_AVTPRX_ERR), 0);

        // wrong-rate PDU: UNSUPPORTED_FORMAT ticks, FRAMES_RX does not
        inject(mkaaf(6, 0x07), 120);
        ck("UNSUPPORTED_FORMAT=1 (0x6C0)", axi_read(A_AVTPRX_ERR), 0x0100);
        ck("FRAMES_RX still 1", axi_read(A_AVTPRX_FRX), 1);
    }

    printf("======================================================================\n");
    printf("milan_datapath: %ld checks, %ld failures\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
