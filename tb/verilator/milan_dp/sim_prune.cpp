/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * PRUNED-SHAPE harness: milan_datapath elaborated with EVERY tier-1
 * optional block dropped (docs/design/AREA_BUDGET.md):
 *
 *   MCSERVO_P=0  LTAP_P=0  MAAP_P=0  I2SPB_P=0  RXFILT_P=0  LPF_P=0
 *
 * WHY THIS FILE EXISTS: a prune that was never elaborated is not a prune.
 * The default suite (sim_main / sim_nxn) proves the PRESENT shape is
 * unchanged; this one proves the PRUNED shape (a) builds at all, (b) leaves
 * every interface at its documented INERT value rather than floating or X,
 * and (c) still does the work that does not depend on the pruned blocks.
 *
 * Each group below is written as the CONTRAST of a check the PRESENT suite
 * already makes, so the two together pin both states:
 *
 *   group          PRESENT (sim_main)                 PRUNED (here)
 *   -------------  ---------------------------------  ----------------------
 *   rx_mac_filter  "prefilter: plain 91E0F0 frame     the same frame REACHES
 *                   dropped from DMA"                  the DMA port, byte-exact
 *   latency taps   LTAP epochs/samples advance on     every LTAP word reads 0
 *                   real traffic                       FOREVER (structural)
 *   mmcm servo     MCSRV_STAT state/flags live        0x8F8 reads 0, MMCM
 *                                                      control pins never move
 *   MAAP           MAAP_STAT1 addr_valid goes 1       stays 0 with the engine
 *                   after a claim                      enabled, no PDU on TX
 *   i2s playback   DAC pins serialize the pair        all four pins stay 0
 */

#include "Vmilan_datapath.h"
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
        printf("  [FAIL] %-50s got=0x%lx exp=0x%lx\n", what, got, exp);
    } else {
        printf("  [ok]   %-50s = 0x%lx\n", what, got);
    }
}

static void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->eval(); }
static void hi() { dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->eval(); }
static void step() { lo(); hi(); }

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
    A_ID = 0x000, A_VERSION = 0x004, A_CAP = 0x008,
    A_MAC_ADDR_LO = 0x108, A_MAC_ADDR_HI = 0x10C,
    A_MAAP_CTRL = 0x6CC, A_MAAP_STAT0 = 0x6D0, A_MAAP_STAT1 = 0x6D4,
    A_I2SPB_STAT = 0x6D8, A_I2SPB_TRIM = 0x6E0, A_I2SPB_DBG = 0x6F0,
    A_TCAM_CTRL = 0x700, A_TCAM_KLO = 0x704, A_TCAM_KHI = 0x708,
    A_TCAM_MLO = 0x70C, A_TCAM_MHI = 0x710, A_TCAM_ACT = 0x714,
    A_TCAM_CMD = 0x718,
    A_LPF_CTRL = 0x72C,
    A_LTAP_CTRL = 0x870, A_LTAP_BASE = 0x874, A_LTAP_END = 0x8B4,
    A_MCSRV_STAT = 0x8F8, A_MCSRV_CTRL = 0x8FC,
};

static void do_reset() {
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
    dut->s_axi_bready = dut->s_axi_rready = 0;
    dut->s_axis_tx_tvalid = 0; dut->s_axis_mac_rx_tvalid = 0;
    dut->m_axis_mac_tx_tready = 0; dut->m_axis_rx_tready = 0; dut->m_axis_ts_tready = 1;
    dut->m_axis_pcm_tready = 1;
    dut->i_mac_speed = 2; dut->i_link_up = 1; dut->i_full_duplex = 1; dut->i_mac_events = 0;
    for (int i = 0; i < 8; i++) step();
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    for (int i = 0; i < 8; i++) step();
}

//! sticky OR of every MMCM control pin + every DAC pin, sampled each cycle.
//! A pruned build must never move any of them - one sample would miss a
//! single-cycle DEN strobe, so accumulate instead.
static unsigned g_mmcm_seen = 0;     //! bit0 drp_en, 1 drp_we, 2 ps_en, 3 rst, 4 addr|di
static unsigned g_dac_seen  = 0;     //! bit0 mclk, 1 sclk, 2 lrck, 3 sdin
static void sample_pins() {
    if (dut->o_mmcm_drp_en)    g_mmcm_seen |= 1u << 0;
    if (dut->o_mmcm_drp_we)    g_mmcm_seen |= 1u << 1;
    if (dut->o_mmcm_ps_en)     g_mmcm_seen |= 1u << 2;
    if (dut->o_mmcm_rst)       g_mmcm_seen |= 1u << 3;
    if (dut->o_mmcm_drp_addr || dut->o_mmcm_drp_di) g_mmcm_seen |= 1u << 4;
    if (dut->i2s_dac_mclk_o)   g_dac_seen |= 1u << 0;
    if (dut->i2s_dac_sclk_o)   g_dac_seen |= 1u << 1;
    if (dut->i2s_dac_lrck_o)   g_dac_seen |= 1u << 2;
    if (dut->i2s_dac_sdin_o)   g_dac_seen |= 1u << 3;
}

//! Inject a raw frame on the MAC RX AXIS and collect what reaches the DMA
//! port (m_axis_rx_*). Pre-edge sampling, exactly as sim_main does.
static std::vector<uint64_t> inject_rx(const uint8_t* f, size_t len, long* frames) {
    std::vector<uint64_t> beats;
    for (size_t bt = 0; bt < (len + 7) / 8; bt++) {
        uint64_t v = 0;
        for (int j = 0; j < 8; j++)
            if (bt * 8 + j < len) v |= (uint64_t)f[bt * 8 + j] << (8 * j);
        beats.push_back(v);
    }
    std::vector<uint64_t> out;
    size_t idx = 0;
    dut->m_axis_rx_tready = 1;
    dut->m_axis_mac_tx_tready = 1;
    for (int c = 0; c < 400; c++) {
        if (idx < beats.size()) {
            dut->s_axis_mac_rx_tdata  = beats[idx];
            dut->s_axis_mac_rx_tkeep  = 0xFF;
            dut->s_axis_mac_rx_tvalid = 1;
            dut->s_axis_mac_rx_tlast  = (idx == beats.size() - 1);
        } else {
            dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
        }
        lo();
        bool in_acc  = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
        bool out_acc = dut->m_axis_rx_tvalid && dut->m_axis_rx_tready;
        bool out_last = dut->m_axis_rx_tlast;
        uint64_t out_d = dut->m_axis_rx_tdata;
        sample_pins();
        hi();
        if (in_acc) idx++;
        if (out_acc) { out.push_back(out_d); if (out_last && frames) (*frames)++; }
    }
    dut->s_axis_mac_rx_tvalid = 0;
    return out;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vmilan_datapath;

    printf("=== milan_datapath PRUNED shape "
           "(MCSERVO_P=LTAP_P=MAAP_P=I2SPB_P=RXFILT_P=LPF_P=0) ===\n");
    do_reset();

    // ---------------------------------------------------------------- 0 ----
    // The prune is NOT CSR-observable at the identity level: same ID, same
    // VERSION, same CAP. This is the check that says "no VERSION bump was
    // owed" - the register contract did not move, only which logic backs it.
    printf("[identity] the CSR contract is unchanged by pruning\n");
    ck("ID == 'MILN'", axi_read(A_ID), 0x4D494C4E);
    ck("VERSION unchanged by the prunes", axi_read(A_VERSION), 0x00010027);
    {
        uint32_t cap = axi_read(A_CAP);
        ck("CAP.ADP bit12 still set",  (cap >> 12) & 1, 1);
        //! CAP.TCAM advertises the CSR WINDOW, which still exists and still
        //! accepts writes - what changed is that nothing consumes it. The
        //! honest declaration of "this build does not filter in hardware"
        //! belongs to the build config, not to a runtime bit (there is no
        //! STATS_CAP-style capability lane for the filter today).
        ck("CAP.TCAM bit13 still set", (cap >> 13) & 1, 1);
    }

    // ---------------------------------------------------------------- 1 ----
    printf("[MCSERVO_P=0] servo pruned: status 0, MMCM pins parked\n");
    ck("MCSRV_STAT 0x8F8 reads 0 (structural)", axi_read(A_MCSRV_STAT), 0);
    //! the CSR half is untouched: the knob register still stores and reads
    //! back, it just has nothing to steer. Pruning RTL must not silently
    //! delete a register.
    ck("MCSRV_CTRL reads 0 at reset", axi_read(A_MCSRV_CTRL), 0);
    axi_write(A_MCSRV_CTRL, 0x3);
    ck("MCSRV_CTRL still RW (ps_invert|auto_repair)", axi_read(A_MCSRV_CTRL), 0x3);
    axi_write(A_MCSRV_CTRL, 0x0);

    // ---------------------------------------------------------------- 2 ----
    printf("[LTAP_P=0] taps pruned: the whole 0x870 window is a hard zero\n");
    //! LTAP_CTRL reads i_ltap_status | {ltap_en_r,1'b0}. With the taps gone
    //! the status half is 0 and only the reset-1 enable bit shows: 0x2.
    ck("LTAP_CTRL = enable bit only, no status", axi_read(A_LTAP_CTRL), 0x2);
    {
        unsigned long acc = 0;
        for (uint16_t a = A_LTAP_BASE; a < A_LTAP_END; a += 4) acc |= axi_read(a);
        ck("all 16 LTAP RO words read 0", acc, 0);
    }

    // ---------------------------------------------------------------- 3 ----
    printf("[MAAP_P=0] engine pruned: claim never completes, no PDU\n");
    ck("MAAP_STAT0 reads 0", axi_read(A_MAAP_STAT0), 0);
    ck("MAAP_STAT1 reads 0 (state INITIAL, addr_valid 0)", axi_read(A_MAAP_STAT1), 0);

    // ---------------------------------------------------------------- 4 ----
    printf("[I2SPB_P=0] DAC serializer pruned: counters 0\n");
    ck("I2SPB_STAT reads 0", axi_read(A_I2SPB_STAT), 0);
    ck("I2SPB_TRIM reads 0", axi_read(A_I2SPB_TRIM), 0);
    ck("I2SPB_DBG  reads 0", axi_read(A_I2SPB_DBG),  0);

    // ---------------------------------------------------------------- 5 ----
    printf("[LPF_P=0] filter pruned: LPF_CTRL survives as a plain register\n");
    ck("LPF_CTRL reset = 1 (enable, default)", axi_read(A_LPF_CTRL) & 1, 1);
    axi_write(A_LPF_CTRL, 0x0);
    ck("LPF_CTRL still RW with no filter behind it", axi_read(A_LPF_CTRL) & 1, 0);
    axi_write(A_LPF_CTRL, 0x1);

    // ---------------------------------------------------------------- 6 ----
    // The headline contrast. sim_main programs EXACTLY this TCAM drop entry
    // and checks "prefilter: plain 91E0F0 frame dropped from DMA". With the
    // filter pruned the same frame must arrive, byte-for-byte, because the
    // tie-off is a straight wire = promiscuous.
    printf("[RXFILT_P=0] filter pruned: RX is a wire (promiscuous)\n");
    axi_write(A_MAC_ADDR_LO, 0x33221100);      // station 00:11:22:33:44:55
    axi_write(A_MAC_ADDR_HI, 0x00005544);
    axi_write(A_TCAM_KHI, 0x000091E0);
    axi_write(A_TCAM_KLO, 0xF0000000);
    axi_write(A_TCAM_MHI, 0x0000FFFF);
    axi_write(A_TCAM_MLO, 0xFF000000);
    axi_write(A_TCAM_ACT, 0x00000001);          // action[0] = drop
    axi_write(A_TCAM_CMD, 0x00010100);          // commit | valid, entry 0
    //! arm the station filter too, with default_pass = 0: on the PRESENT
    //! build this is the harshest configuration there is (drop the TCAM
    //! range AND drop anything not addressed to us).
    axi_write(A_TCAM_CTRL, 0x2);
    ck("TCAM_CTRL still stores (window intact)", axi_read(A_TCAM_CTRL), 0x2);
    {
        uint8_t pf[64]; memset(pf, 0, sizeof pf);
        const uint8_t pdst[6] = {0x91, 0xE0, 0xF0, 0x00, 0x77, 0x77};
        memcpy(pf, pdst, 6);
        pf[6] = 0x66; pf[7] = 0x77; pf[8] = 0x88;
        pf[12] = 0x08; pf[13] = 0x00;
        for (int i = 18; i < 64; i++) pf[i] = (uint8_t)(0x5A ^ i);
        long frames = 0;
        std::vector<uint64_t> got = inject_rx(pf, 64, &frames);
        ck("TCAM-drop dmac REACHES the DMA port", frames, 1);
        ck("...as 8 beats", (unsigned long)got.size(), 8);
        bool exact = got.size() == 8;
        for (size_t bt = 0; bt < got.size() && exact; bt++) {
            uint64_t want = 0;
            for (int j = 0; j < 8; j++) want |= (uint64_t)pf[bt * 8 + j] << (8 * j);
            if (got[bt] != want) exact = false;
        }
        ck("...byte-exact (a wire, not a rewrite)", exact ? 1 : 0, 1);

        //! second contrast: a foreign UNICAST with default_pass=0 and the
        //! station filter armed. The PRESENT build drops this one on the
        //! station-address test alone.
        const uint8_t fdst[6] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xF0};
        memcpy(pf, fdst, 6);
        frames = 0;
        got = inject_rx(pf, 64, &frames);
        ck("foreign unicast REACHES the DMA port", frames, 1);
    }

    // ---------------------------------------------------------------- 7 ----
    // Structural-zero durability: run real traffic with everything ENABLED
    // and re-read. A zero that only holds before the first frame would be a
    // "not armed yet" zero, which is exactly the class of lie STATS_CAP was
    // added to kill. These must be zero AFTER traffic, not just at reset.
    printf("[durability] the inert values hold under live traffic\n");
    axi_write(A_LTAP_CTRL, 0x2);                       // taps enabled
    axi_write(A_MAAP_CTRL, 0x00000801);                // MAAP en, block of 8
    {
        uint8_t af[124]; memset(af, 0, sizeof af);
        const uint8_t adst[6] = {0x91, 0xE0, 0xF0, 0x00, 0xE1, 0xE3};
        memcpy(af, adst, 6);
        af[6] = 0x02; af[11] = 0x02;
        af[12] = 0x22; af[13] = 0xF0;                  // AVTP ethertype
        af[14] = 0x02;                                  // subtype AAF
        long frames = 0;
        for (int r = 0; r < 4; r++) (void)inject_rx(af, 124, &frames);
        for (int c = 0; c < 4000; c++) { lo(); sample_pins(); hi(); }
    }
    ck("LTAP words STILL 0 after traffic", axi_read(A_LTAP_BASE) |
       axi_read(A_LTAP_BASE + 4) | axi_read(A_LTAP_BASE + 32), 0);
    ck("LTAP_CTRL STILL 0x2 after traffic", axi_read(A_LTAP_CTRL), 0x2);
    ck("MCSRV_STAT STILL 0 after traffic", axi_read(A_MCSRV_STAT), 0);
    ck("MAAP_STAT1 STILL 0 with MAAP_CTRL.en=1", axi_read(A_MAAP_STAT1), 0);
    ck("MAAP_STAT0 STILL 0 with MAAP_CTRL.en=1", axi_read(A_MAAP_STAT0), 0);
    ck("I2SPB_STAT STILL 0 after traffic", axi_read(A_I2SPB_STAT), 0);
    ck("no MMCM pin ever moved", g_mmcm_seen, 0);
    ck("no DAC pin ever moved",  g_dac_seen,  0);

    // ---------------------------------------------------------------- 8 ----
    // What must STILL work: the prunes touch none of the mandatory path.
    printf("[unaffected] the mandatory datapath still runs\n");
    {
        //! a tagged best-effort frame still traverses classify -> queue ->
        //! shaper -> PTP stamp -> MAC TX
        uint8_t b[64]; memset(b, 0, sizeof b);
        const uint8_t dst[6] = {0x00, 0x11, 0x22, 0x33, 0x44, 0x55};
        memcpy(b, dst, 6);
        b[12] = 0x81; b[13] = 0x00; b[16] = 0x08; b[17] = 0x00;
        for (int i = 18; i < 64; i++) b[i] = (uint8_t)(0xA5 ^ i);
        std::vector<uint64_t> beats;
        for (int bt = 0; bt < 8; bt++) {
            uint64_t v = 0;
            for (int j = 0; j < 8; j++) v |= (uint64_t)b[bt * 8 + j] << (8 * (7 - j));
            beats.push_back(v);
        }
        size_t idx = 0; long out_beats = 0;
        dut->m_axis_mac_tx_tready = 1;
        for (int c = 0; c < 600; c++) {
            if (idx < beats.size()) {
                dut->s_axis_tx_tdata = beats[idx];
                dut->s_axis_tx_tkeep = 0xFF;
                dut->s_axis_tx_tvalid = 1;
                dut->s_axis_tx_tlast = (idx == beats.size() - 1);
            } else {
                dut->s_axis_tx_tvalid = 0; dut->s_axis_tx_tlast = 0;
            }
            step(); sample_pins();
            if (dut->s_axis_tx_tvalid && dut->s_axis_tx_tready) idx++;
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) out_beats++;
        }
        dut->s_axis_tx_tvalid = 0;
        ck("TX shaper path still egresses the frame", out_beats >= 8 ? 1 : 0, 1);
    }
    ck("RST_EPOCH live (no shadow lie)", axi_read(0x720) >= 1 ? 1 : 0, 1);

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    delete dut;
    return fails ? 1 : 0;
}
