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

// DO NOT re-add `#include "Vmilan_datapath_axi_stream_if__T40.h"`. That name is
// Verilator's mangled per-parameterisation variant of axi_stream_if, and it is
// unused here (nothing below names the type) - but it made this harness the one
// file in the tree that depended on the interface's PARAMETER SET rather than on
// its behaviour. Defaulting TDATA_WIDTH_P 32 -> 64 on 2026-07-27 moved the
// 64-bit instances from variant `__T40` to the base class and broke the build
// with a missing-header error that said nothing about the actual change.
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <vector>
#include <array>
#include <cstdint>
#include <functional>

// ---------------------------------------------------------------------------
// THE ELABORATED SHAPE, stated ONCE per leg by the Makefile.
//
// This file is the harness for EVERY milan_datapath integration leg that runs
// the legacy section list, and since 2026-08-09 that is no longer one entity:
// obj_dir/obj_nolpf elaborate the Arty definition (1 talker source, 2 wire
// channels) and obj_ax1x1 elaborates the shape the AX7101 actually flashes
// (2 talker sources - AAF plus the CRF Media Clock Output - over 8 wire
// channels off a TDM8 master). Every expectation that used to be a literal
// from the Arty side is now DERIVED from these, or read off the DUT.
//
// The defaults below are milan_datapath.sv's OWN parameter defaults, so a leg
// that does not name a value gets the same answer the RTL does. A leg that
// DOES name one states it once in the Makefile and both the -G and the -D come
// out of that single variable: a copied number is a number that drifts.
#ifndef WIRE_CHANS_TB
#define WIRE_CHANS_TB 2         // milan_datapath TALKER_WIRE_CHANS_P default
#endif
#ifndef NSTREAMS_TB
#define NSTREAMS_TB 1           // milan_datapath N_STREAMS default
#endif
#ifndef I2SPB_TB
#define I2SPB_TB 1              // milan_datapath I2SPB_P default (present)
#endif
#ifndef AIF_SLOTS_TB
#define AIF_SLOTS_TB 0          // milan_datapath AUDIO_IF_SLOTS_P default
#endif
#ifndef AIF_I2S_PAIR_TB
#define AIF_I2S_PAIR_TB 0       // milan_datapath AUDIO_IF_I2S_PAIR_P default
#endif

//! Is the TONE_CTRL pilot override wired into the CAPTURE FRONT END on this
//! build? It is an I2S-bench feature and lives in KL_aaf_capture_i2s alone:
//! the two TDM front-ends (KL_tdm_capture, KL_tdm_capture_master) have no
//! tone port at all, so a TDM-only build has no front-end pilot to decode -
//! see the milan_datapath front-end select, "the TONE_CTRL pilot override is
//! an I2S-bench feature and does not reach this front-end". The BLEND shape
//! keeps the I2S capture on pair slot 0, so it does have one.
#define TONE_FRONTEND_TB ((AIF_SLOTS_TB) == 0 || (AIF_I2S_PAIR_TB) != 0)

//! channels_per_frame the framer emits (IEEE 1722-2016 7.3.3)
static const size_t WCH = WIRE_CHANS_TB;
//! first payload octet: 14 Ethernet + 4 C-TAG (the AAF_CTRL VID-2 shim) + 24
//! AVTP/AAF header
static const size_t PAY_O = 14 + 4 + 24;
//! one AAF event = one sample per wire channel, 32 bits each
static const size_t EVT_B = 4 * WCH;
//! 6 events per PDU (48 kHz over the 8 kHz class-A interval), so the whole
//! frame is 42 + 24*C octets: 90 at C=2, 234 at C=8
static const size_t EVENTS_PER_PDU = 6;
static const size_t AAF_BYTES = PAY_O + EVENTS_PER_PDU * EVT_B;

static Vmilan_datapath* dut;
static long checks = 0, fails = 0, skipped = 0;

static void ck(const char* what, unsigned long got, unsigned long exp) {
    bool ok = (got == exp);
    checks++; if (!ok) fails++;
    printf("  [%s] %-34s got=0x%08lx exp=0x%08lx\n", ok ? "PASS" : "FAIL", what, got, exp);
}

//! An expectation this ELABORATION cannot answer, because the block under it
//! was not built. It is NOT a pass: it is counted apart and named in the log,
//! so a shape that quietly stopped testing something says so out loud.
static void ck_skip(const char* what, const char* why) {
    skipped++;
    printf("  [SKIP] %-34s %s\n", what, why);
}

// ---- clocking: axis_clk and gtx_clk driven together (single domain) ----
static void eval() { dut->eval(); }
// clk_tdm_i rides clk_audio_i, which is what the SHIPPING BOARD does: a TDM8
// master needs a 24.576 MHz serial clock, which is the audio MMCM's own
// contract rate, so milan_soc.py:5012 collapses audio_tdm_hz back to None and
// :5224 binds i_clk_tdm_i = ClockSignal("audio"). Leaving it at 0 here - which
// is what this harness did until 2026-08-10 - gives KL_tdm_capture_master a
// CONSTANT-ZERO clock, so the shipping capture front end produces ZERO pairs
// in obj_ax1x1, the only leg that elaborates it. Nothing noticed, because
// A_AAF_PAIRS (0x664) was read by neither milan_dp harness.
static void lo() {
    dut->axis_clk = 0; dut->gtx_clk = 0;
    dut->clk_audio_i = 0; dut->clk_tdm_i = 0; eval();
}
static void hi() {
    dut->axis_clk = 1; dut->gtx_clk = 1;
    dut->clk_audio_i = 1; dut->clk_tdm_i = 1; eval();
}
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
    ck("VERSION",       axi_read(A_VERSION), 0x0002004E);
    // link guard: TB leaves the eth toggles static -> unarmed = inert
    // (alive/alive, RUN, no reinit) exactly like a no-PHY top
    ck("LINKG unarmed", axi_read(0x774), 0x00000003);

    // ---- ETH GUARD (USER 08-06, CSR 0x7D8): guarded from power-on ----
    printf("[CSR] eth guard: refused levers, magic unguard, junk re-arm\n");
    ck("GUARD armed at reset", axi_read(0x7D8), 1);
    axi_write(0x11C, 0x0);                     // PHY_RST drop attempt
    ck("PHY_RST write REFUSED while guarded", axi_read(0x11C), 0x1);
    axi_write(0x71C, 0x3);                     // LINK_CTRL mac_reinit attempt
    ck("LINK_CTRL[1] masked while guarded", axi_read(0x71C), 0x1);
    axi_write(0x7D8, 0x554E4C4B);              // "UNLK"
    ck("magic unguards", axi_read(0x7D8), 0);
    axi_write(0x11C, 0x0);
    ck("PHY_RST write accepted unguarded", axi_read(0x11C), 0x0);
    axi_write(0x11C, 0x1);                     // restore PHY out of reset
    //! LINK_CTRL[1] unguarded acceptance is NOT drilled here: an accepted
    //! mac_reinit pulse starts the REAL reinit sequencer (hold + settle),
    //! which would still be mid-hold when the [LINKG] drill below reads
    //! its state - the masking above is this feature's contract
    axi_write(0x7D8, 0xDEAD);                  // any non-magic word
    ck("junk write re-arms the guard", axi_read(0x7D8), 1);
    axi_write(0x7D8, 0x554E4C4B);              // leave UNGUARDED for the
                                               // rest of the suite (the TB
                                               // predates the guard)
    ck("unguarded for the suite", axi_read(0x7D8), 0);
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

    // --- 5. ADP: THE ADVERTISER IS THE PROCESSOR'S NOW ---------------------
    //
    // WHAT THIS SECTION USED TO BE, AND WHY IT IS NOT THAT ANY MORE.
    // adp_advertiser.sv, KL_adp_parser.sv and adp_pkg.sv are DELETED. ADP is
    // served by KL_pp_shadow -> the processor's KL_adp_engine, which owns
    // ENTITY_AVAILABLE/DEPARTING, the ENTITY_DISCOVER answer, the
    // available_index and the 1 Hz re-advertise cadence.
    //
    // THIS LEG CANNOT OBSERVE AN ADVERTISEMENT, and the reason is arithmetic,
    // not a defect. Milan v1.2 5.6.3.5.2 makes the first advertisement wait
    // T-ADP-DELAY-START, a PRNG draw of 0..2000 ms, and this suite runs the
    // processor's timer service at its SILICON divider (milan_dp passes no
    // -GPP_TIM_DIV_*), so one millisecond is 100,000 axis cycles and the draw
    // is up to 2e8 of them. Measured: no ADPDU in 40,000,000 cycles. The whole
    // cold-boot decode this section used to carry - the multicast DA, the
    // 0x22F0/0xFA pair, the byte-reversed source MAC, the available_index
    // bump, and the ADPDU-vs-0x618/0x61C shape agreement - now lives in
    // tb/verilator/pp_shadow, which compresses the processor's millisecond to
    // 100 cycles and decodes the whole 82-octet ADPDU byte for byte against
    // this same CSR identity group. It is NOT deleted coverage; it MOVED, and
    // it got stronger (a full-frame compare rather than five field probes).
    //
    // What stays here is what this leg can still answer honestly: the CSR
    // identity group is provisioned (the processor reads it), and the two ADP
    // diagnostic words are STRUCTURAL ZEROS - named as such, because the
    // difference between "no engine publishes this" and "the engine is idle"
    // is the whole reason 0x674 was added in the first place.
    printf("[ADP] served by the protocol processor; diag words are structural zeros\n");
    enum { A_ADP_CTRL = 0x600, A_ADP_EIDLO = 0x604, A_ADP_EIDHI = 0x608,
           A_ADP_STATUS = 0x644, A_MAC_ALO = 0x108, A_MAC_AHI = 0x10C };
    // station MAC exactly as kl-eth programs it (platform LSB-first packing:
    // ALO/AHI hold 02:00:00:00:00:01 with [7:0] = first wire byte). This is
    // also the sid root every AAF/CRF framer and the processor's own
    // cfg_stream_id_i derive from, so it is load-bearing well past ADP.
    axi_write(A_MAC_ALO, 0x00000002);
    axi_write(A_MAC_AHI, 0x00000100);
    axi_write(A_ADP_EIDHI, 0x020000FF);
    axi_write(A_ADP_EIDLO, 0xFE000001);
    axi_write(A_ADP_CTRL, 0x00001F01);           // enable=1, valid_time=31
    dut->m_axis_mac_tx_tready = 1;
    for (int c = 0; c < 2000; c++) step();
    {
        enum { A_ADP_DIAG = 0x668, A_ADP_DIAG2 = 0x674 };
        //! STRUCTURAL ZERO, both words. A_ADP_DIAG's depart/rearm counters and
        //! depart source, and A_ADP_DIAG2's egressed-ADPDU count, discover
        //! lanes, last message_type and advertiser state, were all fed by the
        //! deleted advertiser. The processor publishes no equivalent through
        //! the class-D face (available_index alone crosses), so a plausible
        //! count here would be a mirror of nothing. These read 0 FOREVER on
        //! this build, at any cadence, and a reader must not wait on them.
        ck("A_ADP_DIAG 0x668 is a STRUCTURAL ZERO (no advertiser)",
           axi_read(A_ADP_DIAG), 0);
        ck("A_ADP_DIAG2 0x674 is a STRUCTURAL ZERO (no advertiser)",
           axi_read(A_ADP_DIAG2), 0);
        //! ...and A_ADP_STATUS is NOT one of them: adp_available_index is the
        //! processor's class-D adp_next_avail_index_o, a LIVE level. It reads
        //! 0 here only because the cadence above is out of reach, which is a
        //! measurement gap in this leg and not a property of the gateware -
        //! so it is REPORTED, not asserted.
        printf("  [GAP]  ADP advertisement cadence is unreachable at the silicon "
               "millisecond (T-ADP-DELAY-START is a 0..2000 ms PRNG draw = up to "
               "2e8 cycles; measured: no ADPDU in 4e7). A_ADP_STATUS reads 0x%08x. "
               "The ADPDU decode lives in tb/verilator/pp_shadow.\n",
               axi_read(A_ADP_STATUS));
    }

    // --- 6a-bis. THE ADVERTISED SHAPE, read at the CSR (2026-07-27) --------
    // This is the exact field a controller reads to decide how many streams
    // our entity has. Until VERSION 0x0015 it was a plain RW register that
    // reset to ZERO and was filled in by a boot script; on silicon the 8x8
    // board therefore advertised 1 talker source / 2 listener sinks - the
    // numbers that were true when the script was written at 1x1 - and the
    // CRF Media Clock Output at talker_unique_id = N_STREAMS was outside the
    // advertised range, so no controller could see or bind it even though
    // its PDUs were on the wire every 2 ms.
    // NOTHING has been written to 0x618/0x61C here: the words must carry this
    // build's shape straight out of reset.
    //
    // HALF OF THIS LAW MOVED (2026-08-13). It used to be two laws:
    //   1. the WIRE and the CSR must agree - the ADPDU's fields against
    //      0x618/0x61C over a different path. The advertiser is the
    //      processor's now and its cadence is unreachable at this leg's
    //      real-time millisecond (see section 5), so that half is graded in
    //      tb/verilator/pp_shadow, where the whole ADPDU is decoded against
    //      this same CSR group.
    //   2. the COUNT and the CAPABILITY must agree, which is milan_datapath's
    //      own elaboration law ("ADP_TALKER_SRC_C is neither N_STREAMS nor
    //      N_STREAMS+1" is an $error) read back at runtime: an entity claims
    //      MEDIA_CLOCK_SOURCE/SINK if and only if it carries the extra CRF
    //      context to back it. That is precisely the defect shape where the
    //      CRF source sits OUTSIDE the advertised range - advertised as absent
    //      while its PDUs are on the wire every 2 ms, so no controller can
    //      ever be told to ask for it. THAT half is still here, and it is the
    //      half that depends on the elaborated shape rather than on a plane.
    // Everything else - the mandatory IMPLEMENTED|AUDIO_SOURCE / AUDIO_SINK
    // bits, the absence of any other capability bit, the 32-bit packing of the
    // register - stays pinned by construction.
    {
        enum { A_ADP_TALK = 0x618, A_ADP_LIST = 0x61C };
        //! 1722.1-2021 Table 6.4 / 6.5: IMPLEMENTED | AUDIO_SOURCE (Table 6.4)
        //! and IMPLEMENTED | AUDIO_SINK (Table 6.5) are the two this entity
        //! always claims; MEDIA_CLOCK_SOURCE / MEDIA_CLOCK_SINK is the one bit
        //! the end-station config decides.
        const unsigned CAPS_BASE = 0x4001u, CAP_MEDIA_CLOCK = 0x0800u;
        const uint32_t talk_w = axi_read(A_ADP_TALK);
        const uint32_t list_w = axi_read(A_ADP_LIST);
        const unsigned t_mcs = (talk_w >> 16) & CAP_MEDIA_CLOCK ? 1u : 0u;
        const unsigned l_mcs = (list_w >> 16) & CAP_MEDIA_CLOCK ? 1u : 0u;
        printf("[ADP] shape 0x618=0x%08x 0x61C=0x%08x (N_STREAMS=%d, CRF "
               "source %s, CRF sink %s)\n", talk_w, list_w, NSTREAMS_TB,
               t_mcs ? "yes" : "no", l_mcs ? "yes" : "no");

        // ...and the word itself is the shape this build elaborated: the AAF
        // contexts, plus one CRF context exactly when the matching capability
        // bit is claimed. No provisioning, no boot script.
        ck("0x618 RO shape word derives from the config", talk_w,
           ((CAPS_BASE | (t_mcs ? CAP_MEDIA_CLOCK : 0u)) << 16)
               | (unsigned)(NSTREAMS_TB + t_mcs));
        ck("0x61C RO shape word derives from the config", list_w,
           ((CAPS_BASE | (l_mcs ? CAP_MEDIA_CLOCK : 0u)) << 16)
               | (unsigned)(NSTREAMS_TB + l_mcs));
        axi_write(A_ADP_TALK, 0x48010008);   // the retired S50milan poke
        axi_write(A_ADP_LIST, 0x48010008);
        ck("0x618 refuses the poke", axi_read(A_ADP_TALK), talk_w);
        ck("0x61C refuses the poke", axi_read(A_ADP_LIST), list_w);
    }

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
        //! WITNESS REPOINTED (2026-08-13). A_ACMP_STAT 0x650 used to carry the
        //! deleted responder's {responses sent, commands accepted} pair and is
        //! now a STRUCTURAL ZERO: the processor publishes a bind RECORD through
        //! the class-D face, not PDU counters, so those two fields have no
        //! source at all. Asserting the zero is worth exactly one check, named;
        //! the PROPERTY the pair stood for - "the command reached the plane and
        //! an answer left it" - is graded against the processor's own frame
        //! counters at A_PP_DIAG 0x930 ([7:0] rx_frames, [31:16] tx_frames),
        //! which is the live equivalent.
        enum { A_ACMP_STAT = 0x650, A_PP_DIAG = 0x930 };
        ck("0x650 ACMP_STAT is a STRUCTURAL ZERO (no PDU counters)",
           axi_read(A_ACMP_STAT), 0);
        {
            const uint32_t d = axi_read(A_PP_DIAG);
            ck("PP_DIAG: the plane ACCEPTED control frames (rx_frames > 0)",
               (d & 0xFF) > 0 ? 1 : 0, 1);
            ck("PP_DIAG: and it SENT some (tx_frames > 0)",
               ((d >> 16) & 0xFFFF) > 0 ? 1 : 0, 1);
            ck("PP_DIAG: nothing was lost to a full control FIFO",
               (d >> 8) & 0xFF, 0);
        }
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

    // --- 8. DELETED 2026-08-13: the ADP depart witness + enable-toggle
    //     recovery. Every subject in it is gone:
    //       * ADP_CMD 0x640's software depart / advertise-now pulses. The CSR
    //         still decodes the register, but milan_datapath leaves
    //         o_adp_depart_p / o_adp_advertise_p UNCONNECTED - the processor's
    //         KL_adp_engine runs its own timer service off link_up_i as a
    //         LEVEL and takes no per-event pulse from this fabric. A write to
    //         0x640 now reaches nothing, so "software departs, a DEPARTING
    //         frame emerges" cannot be asserted against anything.
    //       * A_ADP_DIAG 0x668's depart_cnt / rearm_cnt / depart_src, which
    //         section 5 above now grades as the structural zeros they are.
    //       * the dormancy-and-recovery flow itself, which was a property of
    //         the deleted advertiser's available_r latch.
    //     The 2026-07-13 silicon question this section answered ("does an
    //     entity that went dormant come back?") belongs to the processor's own
    //     suite now; nothing here can pose it. NOT stubbed and NOT left
    //     asserting zeros: a check that names a register nothing drives is a
    //     check that passes for the wrong reason.

    // --- 9. Milan talker: the admission gate, and what now opens it -------
    // docs/overview/ARCHITECTURE.md: with AAF_CTRL bypass=0 (Milan mode) the
    // framer is gated. Before anything arms it: enable=1 yields NO AAF frames.
    // CSR A_ACMP_TALKER 0x66C witnesses {[0] probe_armed, [1] talker_active,
    // [3] the resolved gate}.
    //
    // WHAT CHANGED, AND WHAT THIS LEG CAN STILL PROVE (2026-08-13).
    // The ACMP talker is the processor's. Its per-source declaring level -
    // acmp_declaring_o, which IS 0x66C[1] - asserts only after a MAAP ALLOC_DA
    // SUCCEEDS through KL_pp_maap_shim, and KL_maap's Annex B claim walk is
    // 3 probes x ~500 ms + announce. milan_dp elaborates KL_maap at the
    // SILICON rate (MAAP_CLK_HZ_P defaults to MILAN_CLK_FREQ_HZ = 100 MHz), so
    // one MAAP millisecond is 100,000 cycles and ANNOUNCE is ~1.5e8 cycles
    // away. Measured: still PROBING after 40,000,000. So on this leg the
    // talker structurally CANNOT hold a destination address, and:
    //   * the probe is still answered - and the answer is the HONEST one,
    //     TALKER_DEST_MAC_FAILED(3), which is a real Milan/1722.1 property and
    //     is graded below instead of the old SUCCESS;
    //   * the gate must therefore STAY SHUT after the probe, which is a
    //     sharper statement than the old "it opens" and is graded;
    //   * the SUCCESS path - status 0, the {station MAC, uid} stream_id in the
    //     response, the granted stream_dest_mac, acmp_declaring_o going high -
    //     is graded in tb/verilator/pp_shadow, which compresses BOTH the
    //     processor's millisecond and KL_maap's onto one grid.
    // The AAF data plane below (tone, ONE-GRID, CLKV's tu byte, the latency
    // taps, CRF) needs frames on the wire, not a particular arming path, so it
    // is armed through AAF_CTRL[1] - the Milan 5.3.7.3 bypass escape hatch,
    // which is a SHIPPING lever with its own CSR bit, not a test backdoor.
    {
        printf("[MILAN-TALKER] the admission gate, and the bypass escape\n");
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
                // msg CONNECT_TX_RESPONSE(1) + status: frame byte 15 = beat1
                // lane 7; byte 16 = beat2 lane 0
                ck("PROBE msg RESPONSE(1)", (pr.data[1] >> 56) & 0x0F, 1);
                //! REPOINTED from SUCCESS. 1722.1-2021 7.4.20 / Milan 5.5.2:
                //! a Talker with no valid destination address answers
                //! TALKER_DEST_MAC_FAILED(3). The processor's talker reaches
                //! a DA only through KL_pp_maap_shim, and this leg's KL_maap
                //! cannot finish its claim walk in simulation time (banner),
                //! so 3 is the CORRECT answer here and asserting SUCCESS would
                //! be asserting that the device hands out an address it does
                //! not own. The SUCCESS path lives in pp_shadow.
                ck("PROBE status TALKER_DEST_MAC_FAILED(3) - no DA held",
                   (pr.data[2] >> 3) & 0x1F, 3);
            }
        }
        //! ...and the gate is STILL SHUT. This is the stronger half of the old
        //! "gate open post-probe": an answered probe that could not allocate a
        //! destination address must not license a stream (Milan 5.3.7.3 needs
        //! a Talker Advertise, and there is nothing to advertise to).
        ck("gate STILL closed after a refused probe", axi_read(A_ACMP_TALKER) & 0xB, 0);
        // The 5.3.7.3 bypass escape (AAF_CTRL[1]) is what arms the framer on
        // this leg. It is the shipping lever - REGISTER_MAP calls it out as a
        // deliberate, watched experiment rather than a boot setting - and it
        // ORs past both qualifying terms, so 0x66C reads gate-only: bit 3 set,
        // bit 1 (the processor's declaring level) still clear.
        axi_write(A_AAF_CTRL, 0x00020003);       // enable | bypass | VID 2
        for (int c = 0; c < 200; c++) step();
        ck("AAF_CTRL[1] bypass opens the gate, and ONLY the gate",
           axi_read(A_ACMP_TALKER) & 0xB, 0x8);
        // AAF frames now flow and carry the stream_id the framer derives from
        // the station MAC, {02:00:00:00:00:01, uid 0} - which is bit-identical
        // to the sid milan_datapath hands the processor as cfg_stream_id_i for
        // source 0, so the wire and the control plane still agree by
        // construction (VLAN-tagged frame: stream_id at bytes 22-29).
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
            ck("AAF frames flow under the bypass escape", aaf_frames >= 1, 1);
            ck("AAF stream_id == {station MAC, uid 0}",
               in_aaf ? (unsigned long long)aaf_sid : 0,
               0x0200000000010000ULL);
        }
        // pilot tone (CSR 0x6DC) through the CAPTURE FRONT END, crossbar in
        // bypass: AAF payload switches to the exact-period 1 kHz 0 dBFS
        // table - both channels equal, samples advancing.
        //
        // FRONT-END FEATURE, NOT A DATAPATH ONE (2026-08-09). The override
        // lives inside KL_aaf_capture_i2s; neither TDM front-end has a tone
        // port, so on a TDM-master build like the AX7101's there is no
        // front-end pilot to decode and the wire carries the (silent) TDM
        // bus instead. That silence is 0x000000, which is table entries 0 and
        // 24 - so "L0 in table" and "L0 == R0" would have reported GREEN on
        // a shape that has no pilot at all, and only "advances" would have
        // failed. Guarded, named, and not counted. The pilot on that shape is
        // proven by the ONE-GRID section below instead, through the capture
        // crossbar - which is the path the board actually routes it through.
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
#if !TONE_FRONTEND_TB
            const char* nofe = "AUDIO_IF_SLOTS_P!=0 without the I2S pair: the "
                               "TDM front-end has no pilot override";
            ck_skip("tone L0 in table", nofe);
            ck_skip("tone L0 == R0 (both channels)", nofe);
            ck_skip("tone advances (L1 = next entry)", nofe);
            ck_skip("tone frame captured", nofe);
#else
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
                            auto smp = [&](size_t off){ return (uint32_t)
                                ((fr[off]<<16)|(fr[off+1]<<8)|fr[off+2]); };
                            // event stride is 4 octets PER WIRE CHANNEL, so
                            // "the next event's channel 0" is +EVT_B, not a
                            // hardcoded +8 (which is the stereo answer)
                            uint32_t l0=smp(PAY_O), r0=smp(PAY_O+4),
                                     l1=smp(PAY_O+EVT_B);
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
#endif
            axi_write(0x6DC, 0x0);          // tone off
        }
        // ONE-GRID contract (task #59, bench 2026-08-02): the pilot routed
        // through the CAPTURE CROSSBAR (CHMAP TONE bucket) must advance
        // EXACTLY one table step per media tick - across frame boundaries.
        // The old wiring stepped the tone on clk_audio/512 while the crossbar
        // walk drains on the axis-domain media_tick (MILAN_CLK_FREQ_HZ/48k):
        // two free-running 48 kHz grids, ~4-12 repeats/drops per second on
        // silicon -> audio-loop THD+N capped at -32 dB. In this harness the
        // clocks run in LOCKSTEP, so that wiring steps the tone every 512
        // cycles against a 2083-cycle tick (~4 steps/tick) and THIS CHECK
        // FAILS LOUDLY - which is the bite: it only passes when the tone the
        // crossbar serves is stepped by the SAME media_tick the walk uses.
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
            enum { A_CHMAP_CTRL = 0x900, A_CHMAP_SEL = 0x904,
                   A_CHMAP_WORD = 0x908 };
            axi_write(0x6DC, 0x1);              // TONE_CTRL.en
            axi_write(A_CHMAP_CTRL, 0x1);       // arm the fabric + CSR port
            // per-channel store (0x0027): the window keys CHANNELS, so the
            // tone takes one write per WIRE CHANNEL {en|src=4 TONE} - two on
            // the Arty shape, eight on the AX7101 one. Mapping only the first
            // pair would leave 2..C-1 on their power-on source and the slip
            // count below would be measuring the wrong lane.
            for (size_t ch = 0; ch < WCH; ch++) {
                axi_write(A_CHMAP_SEL, 0x100 | (unsigned)ch);  // side=1 capture
                axi_write(A_CHMAP_WORD, 0xC000);
            }
            // capture 8 CONSECUTIVE AAF frames = 48 media ticks; skip the
            // first two so the arming edge is out of the window
            std::vector<uint8_t> fr; std::vector<uint32_t> ls;
            int skip = 2; long lr_mism = 0;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 400000 && ls.size() < 48; c++) {
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
                            auto smp = [&](size_t off){ return (uint32_t)
                                ((fr[off]<<16)|(fr[off+1]<<8)|fr[off+2]); };
                            for (size_t e = 0; e < EVENTS_PER_PDU; e++) {
                                size_t ev = PAY_O + EVT_B*e;
                                uint32_t s0 = smp(ev);
                                // one pilot, every wire channel: at C=2 this
                                // is the original L-vs-R comparison
                                for (size_t ch = 1; ch < WCH; ch++)
                                    if (smp(ev + 4*ch) != s0) lr_mism++;
                                ls.push_back(s0);
                            }
                        }
                        fr.clear();
                    }
                }
            }
            ck("crossbar tone: 48 ticks captured", (long)ls.size(), 48);
            ck("crossbar tone: all wire channels equal", lr_mism, 0);
            int idx = -1;
            if (!ls.empty())
                for (int k = 0; k < 48; k++)
                    if (TAB[k] == ls[0]) { idx = k; break; }
            ck("crossbar tone: first sample in table", idx >= 0, 1);
            long slips = 0;
            if (idx >= 0)
                for (size_t k = 1; k < ls.size(); k++)
                    if (ls[k] != TAB[(idx + k) % 48]) slips++;
            ck("ONE GRID: N ticks = N table steps (no slip)", slips, 0);
            axi_write(A_CHMAP_CTRL, 0x0);       // crossbar bypass again
            axi_write(0x6DC, 0x0);              // tone off
        }

        // ------------------------------------------------------------------
        // [CLKV] the 2026-07-27 defect, end to end: CSR -> wire byte 21.
        //
        // On 2026-07-27 this datapath streamed at full rate from a PHC 60 h
        // out of the gPTP domain while stamping tu = 0 on every frame, so the
        // receiving Milan device counted 99.4 % of them LATE or EARLY with no
        // way to know why (docs/findings/REF_LISTENER_TIMESTAMP_SWEEP_0727.md).
        //
        // The requirement is NOT to stop: Milan v1.2 5.3.7.3 excludes stopping
        // a Stream Output ("STREAMING_WAIT shall not be implemented"), and
        // IEEE 1722-2016 7.5 makes tv = 1 mandatory for AAF at sp = 0. The
        // lever the standard gives us is the tu bit (Milan 4.3.5.2 -> IEEE
        // 1722-2016 4.4.4.7). So: frames keep flowing, byte 21 bit 0 tells
        // the truth, and NOTHING claims validity until software leases it.
        //
        // Mutation anchor: revert the RTL to a hard fb[21]=8'h00 and the very
        // first check here fails, because a fresh datapath has no lease.
        // ------------------------------------------------------------------
        {
            printf("[CLKV] clock validity -> AVTP tu on the wire (0x778)\n");
            enum { A_CLKV_CTRL = 0x778, A_CLKV_STAT = 0x77C,
                   A_CLKV_TUCNT = 0x780, A_PTP_CMD = 0x520,
                   A_ADP_GMLO = 0x624, A_ADP_GMHI = 0x628 };

            // grab the next AAF frame off the MAC TX port
            auto next_aaf = [&](std::vector<uint8_t>& out) -> bool {
                std::vector<uint8_t> fr;
                dut->m_axis_mac_tx_tready = 1;
                for (int c = 0; c < 60000; c++) {
                    step();
                    if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                        for (int l = 0; l < 8; l++)
                            if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                                fr.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                        if (dut->m_axis_mac_tx_tlast) {
                            if (fr.size() >= 42 && fr[12] == 0x81 && fr[16] == 0x22 &&
                                fr[17] == 0xF0 && fr[18] == 0x02) { out = fr; return true; }
                            fr.clear();
                        }
                    }
                }
                return false;
            };

            // Grab the next AAF frame with a DISCONTINUITY HELD UP over the
            // packetizer's epoch grant.
            //
            // KL_aaf_packetizer latches tu ONCE, at the grant, and says why:
            // "the holdover (0.25 s) dwarfs the 125 us frame period, so no
            // arming edge can slip between the two points". That is true on
            // silicon and it is NOT true here, because this harness builds
            // with -GCLKV_QTICK_CYC_P=4096 so that a lease can expire inside
            // a simulation at all. Two quarter-ticks of holdover is then
            // 8192 cycles, and the AAF frame period is 3069 cycles on the
            // Arty shape (the I2S front end paces the talker) but 12497 on
            // the AX7101 one (the media tick does). So the stereo shape
            // catches the next grant inside the holdover with room to spare
            // and the eight-channel shape misses it by 4000 cycles - a
            // property of the compressed time base, not of the tu path,
            // which still asserts in CLKV_STAT either way. Holding the
            // discontinuity across the wait restores the silicon relation:
            // the frame is provably composed while the clock IS uncertain.
            // Mutation anchor unchanged - tie fb[21] to 0 in the RTL and this
            // runs its full budget and fails.
            auto next_aaf_held = [&](std::vector<uint8_t>& out,
                                     const std::function<void()>& rearm) -> bool {
                std::vector<uint8_t> fr;
                long armed_at = g_step;
                dut->m_axis_mac_tx_tready = 1;
                for (int c = 0; c < 400000; c++) {
                    // re-arm BETWEEN frames only, with the TX port held off,
                    // so the AXI transaction's own clocking cannot eat beats
                    // out of the middle of the frame being collected
                    if (fr.empty() && (g_step - armed_at) > 2048) {
                        dut->m_axis_mac_tx_tready = 0;
                        rearm();
                        dut->m_axis_mac_tx_tready = 1;
                        armed_at = g_step;
                    }
                    step();
                    if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                        for (int l = 0; l < 8; l++)
                            if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                                fr.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                        if (dut->m_axis_mac_tx_tlast) {
                            if (fr.size() >= 42 && fr[12] == 0x81 && fr[16] == 0x22 &&
                                fr[17] == 0xF0 && fr[18] == 0x02) { out = fr; return true; }
                            fr.clear();
                        }
                    }
                }
                return false;
            };

            std::vector<uint8_t> f;
            ck("CLKV: reset CLKV_CTRL = lease 8, SYNC_OK 0",
               axi_read(A_CLKV_CTRL), 0x00000080);
            ck("CLKV: reset STAT[0] tu = 1 (unknown clock is NOT valid)",
               axi_read(A_CLKV_STAT) & 1, 1);
            ck("CLKV: reset STAT[1] sync_ok = 0",
               (axi_read(A_CLKV_STAT) >> 1) & 1, 0);

            ck("CLKV: unsynchronised -> a frame is STILL emitted", next_aaf(f), 1);
            ck("CLKV: unsynchronised -> byte 21 bit 0 = 1", f.size() ? f[21] : 0xEE, 0x01);
            ck("CLKV: unsynchronised -> tv still 1 (1722-2016 7.5)",
               f.size() ? f[19] : 0, 0x81);
            // 14 Ethernet + 4 C-TAG + 24 AVTP + 24 octets per wire channel:
            // 90 on the Arty stereo shape, 234 on the AX7101 eight-channel
            // one. The literal 90 was the whole reason the shipping shape
            // could not run here.
            ck("CLKV: unsynchronised -> frame still the full AAF PDU",
               (long)f.size(), (long)AAF_BYTES);

            // software leases the sync claim -> tu clears
            axi_write(A_CLKV_CTRL, 0x00000FF1);      // SYNC_OK, long lease
            ck("CLKV: leased -> STAT[1] sync_ok", (axi_read(A_CLKV_STAT) >> 1) & 1, 1);
            ck("CLKV: leased -> STAT[0] tu clears", axi_read(A_CLKV_STAT) & 1, 0);
            f.clear();
            ck("CLKV: leased -> frame emitted", next_aaf(f), 1);
            ck("CLKV: leased -> byte 21 = 0", f.size() ? f[21] : 0xEE, 0x00);

            // a PHC settime IS a gPTP discontinuity - no software help needed
            axi_write(A_PTP_CMD, 0x1);
            ck("CLKV: settime -> STAT[3] holdover", (axi_read(A_CLKV_STAT) >> 3) & 1, 1);
            f.clear();
            // ...and every frame composed while the PHC is being stepped
            // carries tu on the wire
            ck("CLKV: settime -> frame emitted",
               next_aaf_held(f, [&]{ axi_write(A_PTP_CMD, 0x1); }), 1);
            ck("CLKV: settime -> byte 21 bit 0 = 1", f.size() ? f[21] : 0xEE, 0x01);

            // ... and it lapses on its own (Milan Annex B.1.1 holdover)
            for (int c = 0; c < 12000 && (axi_read(A_CLKV_STAT) & 1); c++) step();
            ck("CLKV: holdover ends by itself", axi_read(A_CLKV_STAT) & 1, 0);
            f.clear();
            ck("CLKV: post-holdover frame emitted", next_aaf(f), 1);
            ck("CLKV: post-holdover byte 21 = 0", f.size() ? f[21] : 0xEE, 0x00);

            // a grandmaster change (Milan v1.2 Annex B.1.1). The GM id is an
            // ATOMIC pair since 2026-08-02: a lone LO write only STAGES, the
            // HI write commits both halves (gptp2csr.sh's LO-then-HI order)
            // — so publish it the way the daemon does.
            axi_write(A_ADP_GMLO, 0xDEADBEEF);
            ck("CLKV: staged LO alone is NOT a GM change (torn-latch fix)",
               axi_read(A_CLKV_STAT) & 1, 0);
            axi_write(A_ADP_GMHI, 0x00000000);       // commit the pair
            ck("CLKV: GM change -> tu asserts", axi_read(A_CLKV_STAT) & 1, 1);
            f.clear();
            {
                // ...and a grandmaster that KEEPS changing keeps tu on the
                // wire. Each re-arm publishes a genuinely different identity
                // in the daemon's LO-then-HI order - re-writing the same one
                // is not a change and would not re-arm anything.
                uint32_t gm_lo = 0xDEADBEEF;
                ck("CLKV: GM change -> byte 21 bit 0 = 1 on the wire",
                   next_aaf_held(f, [&]{
                       gm_lo ^= 1u;
                       axi_write(A_ADP_GMLO, gm_lo);
                       axi_write(A_ADP_GMHI, 0x00000000);
                   }) ? f[21] : 0xEE, 0x01);
            }
            for (int c = 0; c < 12000 && (axi_read(A_CLKV_STAT) & 1); c++) step();
            axi_write(A_ADP_GMLO, 0x00000000);       // restore (paired)
            axi_write(A_ADP_GMHI, 0x00000000);
            for (int c = 0; c < 12000 && (axi_read(A_CLKV_STAT) & 1); c++) step();

            // the lease EXPIRES: a claim written once and never renewed must
            // lapse. This is what the Arty's 60-hour drift looked like.
            axi_write(A_CLKV_CTRL, 0x00000011);      // SYNC_OK, lease = 1
            ck("CLKV: short lease -> tu clear", axi_read(A_CLKV_STAT) & 1, 0);
            for (int c = 0; c < 12000 && !(axi_read(A_CLKV_STAT) & 1); c++) step();
            ck("CLKV: lease lapses -> tu re-asserts", axi_read(A_CLKV_STAT) & 1, 1);
            ck("CLKV: lapsed -> sync_ok dropped", (axi_read(A_CLKV_STAT) >> 1) & 1, 0);
            f.clear();
            ck("CLKV: lapsed -> byte 21 bit 0 = 1", next_aaf(f) ? f[21] : 0xEE, 0x01);
            ck("CLKV: TUCNT moved (not a decorative counter)",
               axi_read(A_CLKV_TUCNT) > 0, 1);

            // ---- gh #64 J3: asCapable rides the SAME lease, end to end.
            // The path proved here is CSR write -> o_clkv_as_cap ->
            // KL_ptp_clock_validity's leased register -> CLKV_STAT[16], the
            // same bit the AECP builder serves as GET_AVB_INFO's AS_CAPABLE
            // flag. The old consumer read "a nonzero propagation delay was
            // once written" (0x6E4), which no lease can ever retire.
            ck("CLKV: asCapable is 0 while nobody claims it",
               (axi_read(A_CLKV_STAT) >> 16) & 1, 0);
            axi_write(A_CLKV_CTRL, 0x00000FF5);      // SYNC_OK|AS_CAP, lease
            ck("CLKV: CLKV_CTRL[2] readable", (axi_read(A_CLKV_CTRL) >> 2) & 1, 1);
            ck("CLKV: asCapable claimed -> STAT[16]",
               (axi_read(A_CLKV_STAT) >> 16) & 1, 1);
            ck("CLKV: the claim did not disturb tu", axi_read(A_CLKV_STAT) & 1, 0);
            // the deadman: a lease nobody renews takes asCapable with it
            axi_write(A_CLKV_CTRL, 0x00000015);      // SYNC_OK|AS_CAP, lease 1
            for (int c = 0; c < 12000 && ((axi_read(A_CLKV_STAT) >> 16) & 1); c++)
                step();
            ck("CLKV: lease lapses -> asCapable falls",
               (axi_read(A_CLKV_STAT) >> 16) & 1, 0);
            ck("CLKV: ...in the SAME branch as sync_ok",
               (axi_read(A_CLKV_STAT) >> 1) & 1, 0);

            axi_write(A_CLKV_CTRL, 0x00000FF5);      // synchronised + capable
        }

        // ------------------------------------------------------------------
        // [ASPATH] gh #64 J4: local PathTrace staging and readback only.
        // The root leaves the CSR path outputs disconnected, so this test does
        // not prove GET_AS_PATH. The wire response remains the leaf-only
        // grandmaster path. Here the datapath proves only the local ABI.
        // ------------------------------------------------------------------
        {
            printf("[ASPATH] published 802.1AS PathTrace store (0x7DC)\n");
            enum { A_ASP_LO = 0x7DC, A_ASP_HI = 0x7E0, A_ASP_CMD = 0x7E4 };
            ck("ASP: reset {gen,count} = 0 (the LEGACY arm)",
               axi_read(A_ASP_CMD), 0);
            axi_write(A_ASP_LO, 0xFFFE0210);
            axi_write(A_ASP_HI, 0x3CC0C6FF);
            ck("ASP: LO stages and reads back", axi_read(A_ASP_LO), 0xFFFE0210);
            ck("ASP: HI stages and reads back", axi_read(A_ASP_HI), 0x3CC0C6FF);
            axi_write(A_ASP_CMD, 0x80000100);        // commit -> slot 1
            ck("ASP: a commit alone publishes nothing", axi_read(A_ASP_CMD), 0);
            axi_write(A_ASP_LO, 0xFE001122);
            axi_write(A_ASP_HI, 0xAABBCCFF);
            axi_write(A_ASP_CMD, 0x80000200);        // commit -> slot 2
            axi_write(A_ASP_CMD, 0x40000003);        // publish GM + 2 bridges
            ck("ASP: publish latches {gen 1, count 3}",
               axi_read(A_ASP_CMD), 0x00000013);
            axi_write(A_ASP_CMD, 0x40000003);        // bare re-publish
            ck("ASP: a re-publish still bumps the generation",
               axi_read(A_ASP_CMD), 0x00000023);
            axi_write(A_ASP_CMD, 0x4000000F);        // ask for 15 entries
            ck("ASP: length saturates at the store's eight",
               axi_read(A_ASP_CMD) & 0xF, 8);
            axi_write(A_ASP_CMD, 0x40000000);        // withdraw
            ck("ASP: count 0 returns to the legacy derivation",
               axi_read(A_ASP_CMD) & 0xF, 0);
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
        //! THE PROBE SNIFFER (2026-08-13). The bind ladder is the processor's
        //! now, and it is a REAL ladder: KL_pp_acmp_listener answers the
        //! CONNECT_RX_COMMAND, then launches a CONNECT_TX_COMMAND (Milan
        //! PROBE_TX) at the named talker and takes the stream_id and
        //! stream_dest_mac from the ANSWER (Milan v1.2 5.5.3.5.18 step 4).
        //! The deleted listener recorded the derived sid straight out of the
        //! bind command; this one does not, so a bench that never plays the
        //! talker binds the sink to a sid no frame carries and every counter
        //! below reads a silent zero. The probe's own sequence_id is what the
        //! listener matches the response on (5.5.3.5.18 step 1), so it has to
        //! be harvested off the egress rather than guessed.
        //! PER-SINK, not global: sink 0 is re-probed on its own NOTK timer
        //! while sink 1 is being bound, so a single latch would hand sink 1's
        //! answer the OTHER sink's sequence_id and the settle would never
        //! fire. The probe names its sink in listener_unique_id (wire 52..53).
        uint16_t probe_seq_by_luid[16] = {0};
        bool     probe_seen_luid[16]   = {false};
        std::vector<uint8_t> probe_fr_by_luid[16];
        std::vector<uint8_t> sniff_fr;
        auto sniff_probe = [&]() {
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                for (int l = 0; l < 8; l++)
                    if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                        sniff_fr.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                if (dut->m_axis_mac_tx_tlast) {
                    if (sniff_fr.size() >= 64 && sniff_fr[12] == 0x22 &&
                        sniff_fr[13] == 0xF0 && sniff_fr[14] == 0xFC &&
                        (sniff_fr[15] & 0xF) == 0x0) {      // CONNECT_TX_COMMAND
                        const int luid =
                            ((sniff_fr[52] << 8) | sniff_fr[53]) & 0xF;
                        probe_seq_by_luid[luid] =
                            (uint16_t)((sniff_fr[62] << 8) | sniff_fr[63]);
                        probe_seen_luid[luid] = true;
                        probe_fr_by_luid[luid] = sniff_fr;
                    }
                    sniff_fr.clear();
                }
            }
        };
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
            sniff_fr.clear();   // a fragment drained elsewhere is not a frame
            for (int c = 0; c < 1500; c++) {
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
                sniff_probe();
                if (dut->m_axis_pcm_tvalid) {
                    for (int l = 0; l < 8; l++)
                        pcm.push_back((dut->m_axis_pcm_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_pcm_tlast) pcm_last = true;
                }
                hi();
                if (in_acc) idx++;
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
        //! ...and now play the TALKER. The response names the stream_id and
        //! stream_dest_mac of the AAF PDUs below, which is exactly how a real
        //! peer answers, and it echoes the probe's own sequence_id.
        ck("the listener launched a PROBE_TX at the named talker",
           probe_seen_luid[0] ? 1 : 0, 1);
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t tsrc[6] = {0x02,0x00,0x00,0x00,0x00,0x02};
            memcpy(f+6, tsrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x01;   // CONNECT_TX_RESPONSE
            f[16]=0x00; f[17]=44;                             // status SUCCESS, cdl
            const uint8_t sid[8] = {0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x00};
            memcpy(f+18, sid, 8);                             // @4  stream_id
            for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;  // @12 controller
            const uint8_t tk[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x02};
            memcpy(f+34, tk, 8);                              // @20 talker
            const uint8_t ls[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, ls, 8);                              // @28 listener
            f[50]=0x00; f[51]=0x00;                           // @36 talker uid 0
            f[52]=0x00; f[53]=0x00;                           // @38 listener uid 0
            const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x02};
            memcpy(f+54, dm, 6);                              // @40 stream_dest_mac
            f[62]=(uint8_t)(probe_seq_by_luid[0] >> 8);       // @48 echo the probe's
            f[63]=(uint8_t)(probe_seq_by_luid[0] & 0xFF);
            inject(f, 70);
        }
        //! WITNESS REPOINTED (2026-08-13). This used to read ACMPL_STATE[2:0],
        //! the deleted listener SM's UNBOUND/PRB_*/SETTLED_* ladder. The
        //! processor runs that ladder INTERNALLY and publishes only the BOUND
        //! RECORD, so [2:0] is a documented STRUCTURAL ZERO now and a reader
        //! that waits for SETTLED waits forever. [3] bound (acmpl_bound, from
        //! the class-D acmp_bound_o) is the truth, and [4] active follows it -
        //! REGISTER_MAP 0x6A4 states exactly that. The property is unchanged:
        //! the CONNECT_RX_COMMAND bound this sink, which is what arms the
        //! stream table's entry-0 alias for everything below.
        ck("listener bound (0x6A4[3] bound, the class-D record)",
           (axi_read(A_ACMPL_STATE) >> 3) & 1, 1);
        ck("...and 0x6A4[4] stream-active follows it",
           (axi_read(A_ACMPL_STATE) >> 4) & 1, 1);
        ck("0x6A4[2:0] SM state is a STRUCTURAL ZERO (no ladder here)",
           axi_read(A_ACMPL_STATE) & 0x7, 0);

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
        // ================================================================
        // THE ACCEPTANCE GATE ON STREAM_INPUT[0] IS OPEN AGAIN - AND THE
        // DEFECT THAT SHUT IT IS FIXED IN hdl/.
        //
        // KL_avtp_rx_monitor decides fmt_ok by comparing the PDU's
        // {subtype, format, nsr, bit_depth} against the CURRENT
        // STREAM_INPUT[0] format, and for stream 0 that comes from
        // KL_avtp_rx_monitor_ctx's fmt0_i port - NOT from the 0x800 window,
        // which serves streams > 0 only. milan_datapath drives fmt0_i from
        // `aecp_in0_fmt`, and when the AECP/AEM plane was deleted that line
        // briefly read `assign aecp_in0_fmt = 64'd0`. Against a zero format
        // the very first term, subtype == fmt[63:56], is 0x02 != 0x00, so a
        // PERFECTLY CONFORMANT AAF PDU on the bound stream_id was counted
        // UNSUPPORTED_FORMAT and never reached the depacketizer or the PCM
        // ring: stream 0 accepted NOTHING.
        //
        // milan_datapath.sv now reads `assign aecp_in0_fmt =
        // ADP_STRIN0_FMT_C` - the entity model's DECLARED STREAM_INPUT[0]
        // format out of the generated shape header, the same file that
        // feeds 0x618/0x61C - exactly as aecp_pres_offset carries
        // PRES_DFLT_C rather than a zero. Only the SETTER was AECP's; the
        // declaration never was.
        //
        // So the acceptance mechanism is graded here again, end to end:
        // parser -> format compare -> depacketizer -> PCM ring, untagged
        // and tagged, with the ring's own AXIS port decoded rather than
        // counted. The gate is proved DISCRIMINATING and not merely open by
        // the wrong-rate PDU further down (nsr 0x07 -> UNSUPPORTED_FORMAT
        // +1, no ring traffic): a format compare that accepted everything
        // would fail there, and a compare against a zero format fails here.
        // ================================================================
        enum { A_PCMRX_CNT = 0x6C4, A_PCMRX_TS = 0x6C8 };
        pcm.clear(); pcm_last = false;
        inject(mkaaf(5, 0x05), 120);
        printf("  [i] STREAM_INPUT[0] declared-format acceptance: "
               "0x6BC=%u 0x6C0=0x%08x 0x6C4=0x%08x ring=%zu B\n",
               axi_read(A_AVTPRX_FRX), axi_read(A_AVTPRX_ERR),
               axi_read(A_PCMRX_CNT), pcm.size());
        ck("in0 fmt is the DECLARED format: a conformant PDU is ACCEPTED",
           (axi_read(A_AVTPRX_ERR) >> 8) & 0xFF, 0);
        ck("...so FRAMES_RX moved (0x6BC)", axi_read(A_AVTPRX_FRX), 1);
        ck("...and the PCM ring advanced (0x6C4)",
           axi_read(A_PCMRX_CNT), 1);
        //! ...and the ring's AXIS port carried the PDU's OWN payload, byte
        //! for byte. A counter can move on a runt; these are the 48 octets
        //! mkaaf put on the wire (0x30..0x5F), in wire order, and the last
        //! beat closed the packet.
        {
            long ring_bad = 0;
            for (size_t i = 0; i < pcm.size() && i < 48; i++)
                if (pcm[i] != (uint8_t)(0x30 + i)) ring_bad++;
            ck("...carrying the PDU's 48 payload octets", (long)pcm.size(), 48);
            ck("...byte-exact against the injected payload", ring_bad, 0);
            ck("...and the ring packet closed (tlast)", pcm_last ? 1 : 0, 1);
        }
        //! the MEDIA_LOCKED level is a consequence of acceptance
        ck("...and MEDIA_LOCKED asserts (0x6B8)",
           axi_read(A_AVTPRX_STAT) & 0x1, 1);

        // The VLAN-tagged PDU exercises the rotate-6 realignment in the
        // PARSER, which is upstream of the format gate - and it must reach
        // the ring too, or a C-tagged Milan stream is silently deaf.
        {
            uint8_t tf[124]; memset(tf, 0, sizeof tf);
            const uint8_t* uf = mkaaf(6, 0x05);
            memcpy(tf, uf, 12);
            tf[12]=0x81; tf[13]=0x00; tf[14]=0x00; tf[15]=0x02;   // C-VLAN, VID 2
            memcpy(tf+16, uf+12, 108);                            // shifted rest
            pcm.clear(); pcm_last = false;
            inject(tf, 124);
        }
        ck("tagged: the format gate accepts it too (UNSUPPORTED still 0)",
           (axi_read(A_AVTPRX_ERR) >> 8) & 0xFF, 0);
        ck("tagged: FRAMES_RX = 2", axi_read(A_AVTPRX_FRX), 2);
        {
            long ring_bad = 0;
            for (size_t i = 0; i < pcm.size() && i < 48; i++)
                if (pcm[i] != (uint8_t)(0x30 + i)) ring_bad++;
            ck("tagged: the realigned payload reached the ring, byte-exact",
               (long)(pcm.size() == 48 && ring_bad == 0), 1);
        }
        // ---- RX parser probe (APRB 0x8B4-0x8C4) --------------------------
        // The pre-match view: every counter above only exists once a frame
        // MATCHED, so on a listener that accepts nothing they all read 0 and
        // say nothing about why. These words see the parser itself.
        {
            enum { A_APRB_PARSED = 0x8B4, A_APRB_MATCHED = 0x8B8,
                   A_APRB_SIDLO = 0x8BC, A_APRB_SIDHI = 0x8C0,
                   A_APRB_INFO = 0x8C4 };
            ck("APRB parsed = 2 frames",  axi_read(A_APRB_PARSED), 2);
            ck("APRB matched = 2 frames", axi_read(A_APRB_MATCHED), 2);
            ck("APRB last SID_HI (wire)", axi_read(A_APRB_SIDHI), 0x02000000);
            ck("APRB last SID_LO (wire)", axi_read(A_APRB_SIDLO), 0x00020000);
            long info = axi_read(A_APRB_INFO);
            ck("APRB info subtype = AAF",  info & 0xFF, 0x02);
            ck("APRB info matched flag",  (info >> 8) & 1, 1);
            ck("APRB info armed entries", (info >> 16) & 0xFF, 1);

            // The decisive negative: an AAF frame whose stream_id is NOT in
            // the table. parsed++ (the parser saw it), matched stays put, and
            // the latch shows the stream_id LIFTED OFF THE WIRE - which is
            // exactly what a silicon listener that accepts nothing must be
            // able to report.
            uint8_t nf[112]; memcpy(nf, mkaaf(7, 0x05), 112);
            nf[18+5] = 0x09;                      // sid ...0009 0000: unknown
            pcm.clear(); pcm_last = false;
            inject(nf, 112);
            ck("APRB unknown-sid: parsed = 3",  axi_read(A_APRB_PARSED), 3);
            ck("APRB unknown-sid: matched still 2", axi_read(A_APRB_MATCHED), 2);
            ck("APRB unknown-sid: SID_LO is the WIRE value",
               axi_read(A_APRB_SIDLO), 0x00090000);
            ck("APRB unknown-sid: match flag clear",
               (axi_read(A_APRB_INFO) >> 8) & 1, 0);
            ck("APRB unknown-sid: no PCM payload", (long)pcm.size(), 0);
            //! ...and the ACCEPT counter did not move either. This is the
            //! line the in0-format zero used to make vacuous (it read 0
            //! whatever happened). With stream 0 accepting again it has
            //! teeth: FRAMES_RX stands at the TWO frames that matched and
            //! passed the format gate, and a listener that let an unbound
            //! stream_id through would read 3 here.
            ck("APRB unknown-sid: FRAMES_RX still 2 (unbound sid refused)",
               axi_read(A_AVTPRX_FRX), 2);
        }

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
            //! BOTH HALVES ARE GRADED AGAIN. The kernel half (below) is the
            //! one that protects the board; the FABRIC half is the one that
            //! proves the TCAM drop is a KERNEL-path drop and not a global
            //! one, and it was unprovable on stream 0 while aecp_in0_fmt was
            //! tied to zero. With the declared format restored the ring must
            //! advance by exactly the two PDUs injected into this window
            //! while the DMA port stays silent.
            ck("prefilter: the fabric ring KEPT consuming (+2 PDUs)",
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
#if !I2SPB_TB
            // The AX7101 ships --no-i2s-playback: there is no DAC serializer
            // in this gateware, so there are no pins to decode. Not deleted,
            // not silently green - NAMED. The contrast (all four DAC pins
            // structurally inert under live traffic) is sim_prune.cpp's job.
            ck_skip("I2S left sample from payload",
                    "I2SPB_P=0: no DAC serializer in this elaboration");
#elif !defined(I2S_RING_FED)
            //! BLOCKED, NAMED, NOT SILENTLY GREEN. The DAC serializer is fed
            //! from the PCM ring, and the ring is empty because
            //! STREAM_INPUT[0] accepts nothing (aecp_in0_fmt = 0, the finding
            //! above). Decoding the pins would read stale CDC contents or
            //! silence, and either would be a pass that means nothing.
            //!
            //! The decoder is KEPT below, behind I2S_RING_FED: define it the
            //! day aecp_in0_fmt carries the entity's declared STREAM_INPUT[0]
            //! format and this is a live wire-truth check again, unchanged.
            ck_skip("I2S left sample from payload",
                    "blocked: aecp_in0_fmt = 0 keeps the PCM ring empty");
#else
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
#endif
            axi_write(0x72C, 0x1);
        }

        // wrong-rate PDU: UNSUPPORTED_FORMAT ticks, FRAMES_RX does not,
        // and NOTHING more enters the PCM ring
        // ---- DELETED 2026-08-13: the lwSRP TX pair through the full egress.
        // The subject was hdl/ieee8021q/srp/'s applicant: LWSRP_CTRL 0x680's
        // rising edge fired a PROMPT declare pair (MSRP TalkerAdvertise +
        // MVRP JoinIn) and this block counted both halves at the MAC port -
        // the 2026-07-19 "MilanMAC eats the second frame of a back-to-back
        // pair" hunt. hdl/ieee8021q/srp/ is deleted in full. SRP is the
        // processor's KL_srp_top now, and it is NOT edge-driven from this CSR:
        // it declares off its own MRP state machines and their real-time join
        // timers. 0x680 still decodes, but its enable no longer commands a
        // declaration, so "write the register, count the pair" has no subject.
        //
        // MEASURED, so the loss is stated and not guessed: the processor DOES
        // emit one MSRP and one MVRP frame in this build, but not until
        // somewhere past 40,000 and inside 40,000,000 axis cycles - the MRP
        // timers run at the silicon millisecond here, exactly as ADP and MAAP
        // do. A 120,000-cycle window cannot see them, and widening it to tens
        // of millions would add ~10 minutes per leg to a nine-leg suite. The
        // min-IFG gasket that the eater fix installed is still exercised on
        // every control frame this leg DOES emit (the ACMP responses above),
        // and tb/verilator/ifg grades the gasket itself.

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

        // ---- narrow counter views SATURATE, they do not wrap ---------------
        // AVTPRX_ERR packs three 32-bit STREAM_INPUT counters into one word,
        // so it can only ever show a byte or half-word of each. Truncating
        // makes a busy counter count DOWN again past its ceiling - a link
        // getting worse reads as a link getting better (silicon 2026-07-26:
        // SEQ_NUM_MISMATCH 51,523, 79 % of the way to a 16-bit roll). Push
        // UNSUPPORTED_FORMAT well past its 8-bit ceiling with wrong-rate PDUs
        // and require the field to STICK at 0xFF - "at least 255" - while the
        // full-width counter behind it keeps counting in the 0x800 window.
        // On the pre-fix RTL this wraps to a small number and FAILS.
        {
            enum { A_STRM_SEL = 0x800, A_STRM_SNAP = 0x804,
                   A_STRMW_CNT_UF = 0x830 + 6*4 };   // word 6 = UNSUPPORTED_FORMAT
            long uf = (long)(axi_read(A_AVTPRX_ERR) >> 8) & 0xFF;
            int  sent = 0;
            while (uf < 0xFF && sent < 400) {        // climb to the ceiling
                inject(mkaaf(7, 0x07), 120); sent++;
                uf = (long)(axi_read(A_AVTPRX_ERR) >> 8) & 0xFF;
            }
            ck("UNSUPPORTED_FORMAT view reached its 0xFF ceiling", uf, 0xFF);
            for (int k = 0; k < 8; k++) inject(mkaaf(7, 0x07), 120);
            ck("saturated view STAYS 0xFF (no wrap)",
               (long)(axi_read(A_AVTPRX_ERR) >> 8) & 0xFF, 0xFF);
            ck("neighbouring TIMESTAMP_UNCERTAIN byte untouched",
               axi_read(A_AVTPRX_ERR) & 0xFF, 0);
            // the honest full-width value is still there, in the 0x800 window
            axi_write(A_STRM_SEL, 0x000);            // listener context 0
            axi_write(A_STRM_SNAP, 0x1);
            for (int c = 0; c < 64; c++) step();
            ck("full 32-bit UNSUPPORTED_FORMAT > the saturated view",
               axi_read(A_STRMW_CNT_UF) > 0xFF ? 1 : 0, 1);
        }


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
    // [SERVO] THE MEDIA-CLOCK SOURCE SELECTION IS GONE (2026-08-13).    //
    //                                                                  //
    // This section used to drive an AECP SET_CLOCK_SOURCE(2) through    //
    // the real RX path and require KL_mmcm_drp_servo to leave IDLE -    //
    // the datapath wiring between the aecp TB (which pinned clk_src_o)  //
    // and the mmcm_servo TB (which pinned the FSM). SET_CLOCK_SOURCE    //
    // was the ONLY writer of the live CLOCK_DOMAIN clock_source_index   //
    // and the whole AECP plane is deleted, so milan_datapath pins       //
    // aecp_clk_src at 16'd0 - the INTERNAL media clock - for the life   //
    // of the build. There is no command, no index and no selection to   //
    // grade: the checks that drove one are deleted rather than left     //
    // asserting a value nothing can change.                            //
    //                                                                  //
    // What is still assertable is the PIN itself and its one visible    //
    // consequence on the packet grid, plus the CSR boundary of the      //
    // servo's own knob register.                                       //
    // ---------------------------------------------------------------- //
    printf("\n[SERVO] clock_source is pinned INTERNAL (no SET_CLOCK_SOURCE)\n");
    {
        enum { A_CRF_CTRL = 0x738, A_CRF_SIDLO = 0x73C, A_CRF_SIDHI = 0x740,
               A_MCSRV_STAT = 0x8F8 };
        dut->i_mmcm_locked = 1;
        for (int c = 0; c < 8; c++) step();
        //! THE PIN IS A COMPILE-TIME CONSTANT NOW, so there is no net to
        //! read: milan_datapath declares CRF_CLK_SELECTED_C /
        //! MEDIA_CLK_SRC_IDX_C / MEDIA_CLK_SRC_NONE_C and the old pair of
        //! 16-bit nets (aecp_clk_src, aem_crf_clksrc_w) is deleted. That is
        //! the fix for what this block reported as a [DEFECT] on 2026-08-13:
        //! the two nets WERE kept, the CRF-index one had no driver, and every
        //! consumer therefore compared 0 == 0 and read "CRF selected".
        //!
        //! So the assertions moved from the net to its CONSEQUENCES, which is
        //! the stronger place to assert anyway - a constant cannot be observed
        //! wrong, but a servo that engages on it can.
        ck("the NCO grid is structurally free-running (servo_en = 0)",
           dut->rootp->milan_datapath__DOT__mnco_servo_en_w, 0);
        //! ...and the MMCM phase-shift loop stays in IDLE. This is the check
        //! that would have caught the 0 == 0 trap: KL_mmcm_drp_servo selects
        //! on (clk_src_i == crf_src_idx_i), and it is now fed INTERNAL
        //! against MEDIA_CLK_SRC_NONE_C (0xFFFF, an index no CLOCK_SOURCE
        //! descriptor can carry), so that select is structurally false.
        //! Measured on the broken build: MCSRV_STAT = 0x21, servo out of IDLE
        //! at clock_source = INTERNAL.
        {
            const uint32_t sv = axi_read(A_MCSRV_STAT);
            ck("MMCM servo stays IDLE at clock_source = INTERNAL "
               "(MCSRV_STAT[2:0] == 0)", (int)(sv & 0x7), 0);
        }

        // MCSRV_CTRL 0x8FC: the ps_invert bench knob must be RW-readable
        // (it shares the >=0x800 live-read region the 0x8F8 fix opened)
        enum { A_MCSRV_CTRL = 0x8FC };
        ck("MCSRV_CTRL reads 0 at reset", axi_read(A_MCSRV_CTRL), 0);
        axi_write(A_MCSRV_CTRL, 0x1);
        ck("MCSRV_CTRL ps_invert readback", axi_read(A_MCSRV_CTRL), 1);
        axi_write(A_MCSRV_CTRL, 0x0);
        ck("MCSRV_CTRL clears", axi_read(A_MCSRV_CTRL), 0);
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
        // This is a SYNCHRONISED-clock golden: lease the sync claim with the
        // maximum lifetime so CRF byte 15 stays 0x80 (tu = 0) for the whole
        // capture. The tu = 1 shape of the same byte is proved in the
        // KL_crf_tx unit harness and in [CLKV] above.
        axi_write(0x778, 0x0000FFF1);

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
        // en=1 plus stat[7] (emission licensed - lwSRP is off here, so the
        // bring-up escape licenses the free-run; see crft_emit_en_w)
        ck("CRFT_CTRL readback en=1 + stat[7]", axi_read(A_CRFT_CTRL), 0x81);

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
        //
        // BYTE 15 IS SPLIT (2026-08-13). It packs {sv, version[2:0], mr, r,
        // fs, tu} and TWO of those are LEVELS this section does not own: `tu`
        // is the clock-validity verdict the [CLKV] section drives and grades
        // on the wire, and `mr` is the 4.4.4.3 media-clock-restart level the
        // [H2] section owns. Folding them into a byte-exact header compare
        // made this check fail whenever an earlier section left either level
        // set - it is asserting the OTHER sections' subjects, not its own. The
        // structural half (sv = 1, version = 0, reserved = 0, fs = 0) is
        // compared strictly; the two levels are reported, not asserted here.
        long ok_hdr = 1, ok_seq = 1, ok_pad = 1;
        int bad_at = -1; unsigned bad_got = 0, bad_exp = 0;
        auto hdrb = [&](const uint8_t* f, int off, unsigned exp) {
            if (f[off] != exp) {
                ok_hdr = 0;
                if (bad_at < 0) { bad_at = off; bad_got = f[off]; bad_exp = exp; }
            }
        };
        const uint8_t dmac[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x07};
        const uint8_t sid8[8] = {0x02,0x00,0x00,0x00,0x00,0x01,0x00,0x01};
        for (int k = 0; k < (int)crf.size(); k++) {
            const uint8_t* f = crf[k].data();
            for (int j = 0; j < 6; j++) hdrb(f, j, dmac[j]);
            for (int j = 0; j < 6; j++) hdrb(f, 6 + j, smac[j]);
            hdrb(f, 14, 0x04);                       // subtype CRF
            //! sv|version|r|fs strictly; mr (0x08) and tu (0x01) are levels
            if ((f[15] & 0xF6) != 0x80) {
                ok_hdr = 0;
                if (bad_at < 0) { bad_at = 15; bad_got = f[15] & 0xF6; bad_exp = 0x80; }
            }
            hdrb(f, 17, 0x01);                       // type CRF_AUDIO_SAMPLE
            for (int j = 0; j < 8; j++) hdrb(f, 18 + j, sid8[j]);
            hdrb(f, 26, 0x00); hdrb(f, 27, 0x00);
            hdrb(f, 28, 0xBB); hdrb(f, 29, 0x80);    // base_frequency 48000
            hdrb(f, 30, 0x00); hdrb(f, 31, 0x08);    // data_length 8
            hdrb(f, 32, 0x00); hdrb(f, 33, 0x60);    // timestamp_interval 96
            if (f[16] != (uint8_t)k) ok_seq = 0;
            for (int p = 42; p < 60; p++) if (f[p]) ok_pad = 0;
        }
        if (!crf.empty())
            printf("  [i]    CRFTX byte15 = 0x%02x (mr=%d tu=%d, both graded "
                   "elsewhere)\n", crf[0][15], (crf[0][15] >> 3) & 1,
                   crf[0][15] & 1);
        if (bad_at >= 0)
            printf("  [i]    CRFTX first header mismatch at wire byte %d: "
                   "got 0x%02x want 0x%02x\n", bad_at, bad_got, bad_exp);
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
        // ... and that value IS the 10.7 Equation 14 answer at the shipping
        // default: 2 ms is exactly 96 media clock periods, so rounding up to
        // a whole number of them changes nothing. The rounding law itself is
        // swept against an independent oracle in the KL_crf_tx harness; what
        // this pins is that the datapath's default MTT entry stays
        // byte-identical through it (gh #62 H3).

        // ================================================================ //
        // [H2] IEEE 1722-2016 10.4.3 mr on the wire — WHAT SURVIVES.       //
        //                                                                  //
        // Three wirings used to meet here:                                 //
        //   (1) the mr level KL_media_clock_restart grants the CRF Media    //
        //       Clock Output actually reaches the wire byte — KEPT;         //
        //   (2) a media clock SOURCE change drives it (4.4.4.3's primary    //
        //       trigger, PICS Table F.16 CRF-3) — DELETED. The trigger was  //
        //       an AECP SET_CLOCK_SOURCE on the wire and there is no AECP;  //
        //       aecp_clk_src is pinned 0, so no source change can occur at  //
        //       all and the case has no stimulus;                           //
        //   (3) a RECEIVED mr toggle must NOT be echoed while the device is //
        //       on an internal clock (10.4.3: "only the mr bit from the     //
        //       stream being used by the Listener for recovering the media  //
        //       clock is valid") — DELETED, and this one is a FINDING, not  //
        //       a tidy-up. The gate is mcr_restart_p_w's                    //
        //       `aecp_clk_src == aem_crf_clksrc_w`, and with the AECP       //
        //       response builder deleted aem_crf_clksrc_w has NO DRIVER, so //
        //       the comparison is 0 == 0 = TRUE: the fabric behaves as if   //
        //       the CRF source were selected on every build. The check would //
        //       pass here only because the clause's 8-PDU hold outlasts the  //
        //       two-PDU capture window — a pass for the wrong reason — so it //
        //       is removed and reported instead. It comes back the moment    //
        //       milan_datapath reads CRF_CLK_SELECTED_C, the named constant  //
        //       it already declares for exactly this trap.                   //
        // ================================================================ //
        printf("  -- [H2] 10.4.3 mr: the level reaches the wire byte --\n");
        {
            // capture n CRF PDUs off the MAC TX lane
            auto cap_crf = [&](int n, std::vector<std::array<uint8_t,64>>& out,
                               long budget) {
                out.clear();
                std::vector<uint8_t> c2;
                for (long c = 0; c < budget && (int)out.size() < n; c++) {
                    step();
                    if (!dut->m_axis_mac_tx_tvalid) continue;
                    uint64_t d = dut->m_axis_mac_tx_tdata;
                    for (int j = 0; j < 8; j++) c2.push_back((uint8_t)(d >> (8*j)));
                    if (dut->m_axis_mac_tx_tlast) {
                        if (c2.size() >= 42 && c2[12]==0x22 && c2[13]==0xF0
                            && c2[14]==0x04) {
                            std::array<uint8_t,64> f{};
                            for (size_t k = 0; k < c2.size() && k < 64; k++)
                                f[k] = c2[k];
                            out.push_back(f);
                        }
                        c2.clear();
                    }
                }
            };
            //! the send_sink() helper that injected a CRF PDU with a chosen mr
            //! level went with cases (2) and (3): its only consumers were the
            //! two echo cases above, and a builder with no caller is dead code.
            std::vector<std::array<uint8_t,64>> cap;
            auto lvl_of = [&](const std::array<uint8_t,64>& f) {
                return (long)((f[15] >> 3) & 1);
            };

            // CALIBRATE, do not assume. mr is a LEVEL and no clause resets
            // it, so the value the wire is carrying when this case starts is
            // whatever earlier activity left behind. Read it rather than
            // expecting a particular polarity.
            cap_crf(3, cap, 600000);
            ck("H2 baseline: the CRF output is emitting", (long)cap.size(), 3);
            long lvl0 = cap.size() == 3 ? lvl_of(cap[2]) : -1;
            //! sv|version|r|fs strictly; mr is the level under study and tu
            //! is [CLKV]'s, so both are masked out of the shape compare
            ck("H2 baseline: byte 15 is a well-formed sv|mr|fs|tu byte",
               cap.size() == 3 ? (cap[2][15] & 0xF6) : 0xFFu, 0x80);
            //! the LEVEL really is on the wire and stable across PDUs - the
            //! (1) wiring, which is what this case still owns
            {
                long stable = (cap.size() == 3);
                for (auto& f : cap) if (lvl_of(f) != lvl0) stable = 0;
                ck("H2: the granted mr level reaches the wire byte, held", stable, 1);
            }
            printf("  [GAP]  10.4.3 mr TRIGGERS are unreachable on this build: the "
                   "source-change trigger needed AECP SET_CLOCK_SOURCE (deleted, "
                   "aecp_clk_src pinned 0), and the received-toggle GATE is "
                   "`aecp_clk_src == aem_crf_clksrc_w` with aem_crf_clksrc_w "
                   "UNDRIVEN - 0 == 0 reads TRUE, so the gate this case exists to "
                   "prove is stuck open. Fix: read CRF_CLK_SELECTED_C.\n");

        }

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

        // ---- the LICENCE gate (Milan v1.2 5.3.7.3): with lwSRP policing //
        // (engine + talker declarations on) and NO listener-ready         //
        // registered, the CRF talker owes silence - the ax-rv32-e wire    //
        // showed 500 PDU/s with zero listeners through the old bare-CSR   //
        // gate. Dropping lwSRP back off restores the bring-up free-run.   //
        axi_write(A_CRFT_CTRL, 0x1);              // CSR enable back ON
        axi_write(0x680, 0x013);                  // lwSRP en | talker | q4
        long cnt_lic = axi_read(A_CRFT_COUNT);
        long stray_lic = 0;
        std::vector<uint8_t> lcur;
        for (long c = 0; c < 120000; c++) {
            step();
            if (dut->m_axis_mac_tx_tvalid) {
                uint64_t d = dut->m_axis_mac_tx_tdata;
                for (int j = 0; j < 8; j++) lcur.push_back((uint8_t)(d >> (8*j)));
                if (dut->m_axis_mac_tx_tlast) {
                    // CRF = untagged 22F0 subtype 04, or C-tagged variant
                    if (lcur.size() >= 19 &&
                        ((lcur[12]==0x22 && lcur[13]==0xF0 && lcur[14]==0x04) ||
                         (lcur[12]==0x81 && lcur[13]==0x00 &&
                          lcur[16]==0x22 && lcur[17]==0xF0 && lcur[18]==0x04)))
                        stray_lic++;
                    lcur.clear();
                }
            }
        }
        ck("CRFTX unlicensed (lwSRP on, no listener-ready) = silent",
           stray_lic, 0);
        ck("CRFTX unlicensed = count frozen", axi_read(A_CRFT_COUNT), cnt_lic);
        ck("CRFT stat[7] emission-licensed clear",
           (axi_read(A_CRFT_CTRL) >> 7) & 1, 0);
        axi_write(0x680, 0x010);                  // lwSRP back off (bring-up)
        long cnt_byp = axi_read(A_CRFT_COUNT);
        for (long c = 0; c < 120000; c++) step();
        ck("CRFTX free-run restored with lwSRP off",
           axi_read(A_CRFT_COUNT) > cnt_byp ? 1 : 0, 1);
        ck("CRFT stat[7] emission-licensed set",
           (axi_read(A_CRFT_CTRL) >> 7) & 1, 1);
        axi_write(A_CRFT_CTRL, 0x0);              // leave as the block found it
        for (int c = 0; c < 5000; c++) step();
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
            //! talker_unique_id 1, NOT the arbitrary 0x0011 this bench used
            //! to pick. The processor's listener validates a transaction with
            //! `unique_id < N_SINKS_P` (KL_pp_acmp_listener.sv:331) and the
            //! packet validator takes @36 talker_unique_id for message types
            //! 0..5 - so the CONNECT_TX_RESPONSE that answers this sink's
            //! PROBE_TX is steered by @36. A talker_unique_id of 17 against a
            //! 2-sink shape is discarded before it reaches the record, the
            //! probe never settles, and the bind carries a zero stream_id.
            f[50]=0x00; f[51]=0x01;               // talker_unique_id
            f[52]=0x00; f[53]=0x01;               // listener_unique_id = 1
            const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x09};
            memcpy(f+54, dm, 6);
            f[62]=(uint8_t)(seq>>8); f[63]=(uint8_t)seq;
            return f;
        };
        dut->m_axis_mac_tx_tready = 1;
        probe_seen_luid[1] = false;
        inject(mkconn(6, 0x300), 70);
        //! ...and play the talker for sink 1's probe too (5.5.3.5.18 step 4 -
        //! the processor's listener takes the bound sid from the RESPONSE, so
        //! a bench that answers nothing binds the CRF sink to a sid no PDU
        //! carries). The response names S1SID and the CRF PDUs' own DMAC.
        ck("[S1CRF] sink 1 launched its PROBE_TX",
           probe_seen_luid[1] ? 1 : 0, 1);
        if (probe_seen_luid[1]) {
            const std::vector<uint8_t>& q = probe_fr_by_luid[1];
            printf("  [i]    s1 probe: msg=%u len=%zu teid=%02x%02x%02x%02x%02x%02x%02x%02x"
                   " tuid=%02x%02x luid=%02x%02x seq=%02x%02x sid=%02x%02x%02x%02x%02x%02x%02x%02x\n",
                   q[15]&0xF, q.size(), q[34],q[35],q[36],q[37],q[38],q[39],q[40],q[41],
                   q[50],q[51], q[52],q[53], q[62],q[63],
                   q[18],q[19],q[20],q[21],q[22],q[23],q[24],q[25]);
        }
        {
            uint8_t f[70]; memset(f, 0, sizeof f);
            const uint8_t dst[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            const uint8_t src[6] = {0x02,0x00,0x00,0x00,0x00,0x09};
            memcpy(f, dst, 6); memcpy(f+6, src, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x01;  // CONNECT_TX_RESPONSE
            f[16]=0x00; f[17]=44;                            // SUCCESS | cdl 44
            for (int j = 0; j < 8; j++) f[18+j] = (uint8_t)(S1SID >> (8*(7-j)));
            const uint8_t ctl[8] = {0x68,0x05,0xCA,0xFF,0xFE,0x95,0xB2,0xD1};
            memcpy(f+26, ctl, 8);
            const uint8_t tk[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x09};
            memcpy(f+34, tk, 8);
            const uint8_t ls[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, ls, 8);
            f[50]=0x00; f[51]=0x01;                          // talker_unique_id
            f[52]=0x00; f[53]=0x01;                          // listener_unique_id 1
            const uint8_t dm2[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x09};
            memcpy(f+54, dm2, 6);
            f[62]=(uint8_t)(probe_seq_by_luid[1] >> 8);
            f[63]=(uint8_t)(probe_seq_by_luid[1] & 0xFF);
            inject(f, 70);
        }
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

    // --- STATS_CAP 0x204: which STAT lanes are REAL in this build ------------
    // The honesty half of the RMON fix. A zero STAT word used to be ambiguous
    // ("no errors" vs "no counter"), which is exactly why a whole tied-off
    // counter group survived on silicon. 0x204 resolves it structurally: the
    // two good-frame lanes are forced supported because the datapath derives
    // them HERE, and every other lane is claimed only if the integration says
    // it drives it (i_mac_events_cap - the SoC's KL_mac_rmon_events mask).
    printf("[RMON] STATS_CAP lane capability mask (0x204)\n");
    {
        enum { A_STATS_CAP = 0x204, TX_GOOD_L = 3, RX_GOOD_L = 8 };
        const uint32_t GOOD = (1u << TX_GOOD_L) | (1u << RX_GOOD_L);
        dut->i_mac_events_cap = 0;                 // "no MAC attached" stub
        for (int i = 0; i < 4; i++) step();
        ck("[RMON] cap with no MAC = the two derived lanes only",
           axi_read(A_STATS_CAP), GOOD);
        // a MAC that checks FCS + preamble and flags bad frames (lanes 4,5,7)
        dut->i_mac_events_cap = (1u << 4) | (1u << 5) | (1u << 7);
        for (int i = 0; i < 4; i++) step();
        ck("[RMON] cap ORs the integration's lanes over the derived pair",
           axi_read(A_STATS_CAP), GOOD | (1u << 4) | (1u << 5) | (1u << 7));
        // the four MAC-internal lanes are never claimed by this integration
        long cap = axi_read(A_STATS_CAP);
        ck("[RMON] TX_ERROR_UNDERFLOW declared unsupported", (cap >> 0) & 1, 0);
        ck("[RMON] TX_FIFO_OVERFLOW declared unsupported",   (cap >> 1) & 1, 0);
        ck("[RMON] TX_FIFO_BAD_FRAME declared unsupported",  (cap >> 2) & 1, 0);
        ck("[RMON] RX_FIFO_OVERFLOW declared unsupported",   (cap >> 6) & 1, 0);
        ck("[RMON] cap is a live read (bits 31:9 reserved 0)", cap >> 9, 0);
        dut->i_mac_events_cap = 0;
        for (int i = 0; i < 4; i++) step();
    }

    // ------------------------------------------------------------------ //
    //  THE SHIPPING CAPTURE FRONT END IS ALIVE (2026-08-10)
    //
    //  obj_ax1x1 is the ONLY leg that elaborates the shipping solo TDM8
    //  master (AUDIO_IF_SLOTS_P=8, AUDIO_IF_MASTER_P=1 -> g_solo). Until this
    //  round it drove clk_tdm_i at 0, so KL_tdm_capture_master's whole
    //  serializer domain was frozen and the front end produced no pairs at
    //  all - in the one sim that builds it. The suite passed anyway, because
    //  A_AAF_PAIRS was read nowhere and tdm_fsync_o was observed nowhere.
    //
    //  Two rails, deliberately both: fsync toggling proves the MASTER is
    //  generating its bus, and the pair counter proves that bus is actually
    //  clocking samples out of the front end. A master that emits a frame
    //  sync but no pairs is exactly the failure that hid here.
    // ------------------------------------------------------------------ //
#if defined(AIF_SLOTS_TB) && AIF_SLOTS_TB != 0
    {
        const uint32_t pairs0 = axi_read(0x664);          // A_AAF_PAIRS
        int fsync_edges = 0, last = dut->tdm_fsync_o;
        for (int i = 0; i < 200000; i++) {
            step();
            if (dut->tdm_fsync_o != last) { fsync_edges++; last = dut->tdm_fsync_o; }
        }
        const uint32_t pairs1 = axi_read(0x664);
        printf("  [i]    TDM8 master: fsync edges %d, AAF_PAIRS %u -> %u "
               "(+%u) over 200k cycles\n",
               fsync_edges, pairs0, pairs1, pairs1 - pairs0);
        ck("tdm-live: the MASTER generates its frame sync",
           fsync_edges > 0, 1);
        ck("tdm-live: the front end captures pairs (A_AAF_PAIRS advances)",
           pairs1 > pairs0, 1);
    }
#else
    ++skipped;   // no TDM front end in this shape - not a pass
#endif

    printf("======================================================================\n");
    printf("milan_datapath: %ld checks, %ld failures\n", checks, fails);
    // Kept on its OWN line, and deliberately without the word the sweep's
    // tally regexes key on (scripts/suite_tally.py): a guarded expectation is
    // not a check that passed, and it must never be added into the headline.
    if (skipped)
        printf("milan_datapath: guarded and NOT run in this shape: %ld\n",
               skipped);
    delete dut;
    return fails ? 1 : 0;
}
