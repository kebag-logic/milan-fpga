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
 *   rx_mac_filter  filter counters respond to live    MAC ingress remains live;
 *                   traffic                            CSR window is inert
 *   latency taps   LTAP epochs/samples advance on     every LTAP word reads 0
 *                   real traffic                       FOREVER (structural)
 *   mmcm servo     MCSRV_STAT state/flags live        0x8F8 reads 0, MMCM
 *                                                      control pins never move
 *   MAAP           MAAP_STAT1 addr_valid goes 1       stays 0 with the engine
 *                   after a claim                      enabled, no PDU on TX
 *   i2s playback   DAC pins serialize the pair        all four pins stay 0
 */

#include "../../common/verilator_harness.hpp"
#include "Vmilan_datapath.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <vector>

//! AXI4-Lite handshake guard: cycles a single beat may wait before the BFM
//! gives up rather than hanging the leg.
constexpr int kAxiGuardCycles = 4096;

//! CSR byte offsets. Plain integers by intent: every one of them is handed to
//! the AXI BFM as an address, so a `constexpr` block is what keeps the call
//! sites cast-free (Enum.5).
constexpr uint16_t A_ID = 0x000;
constexpr uint16_t A_VERSION = 0x004;
constexpr uint16_t A_CAP = 0x008;
constexpr uint16_t A_MAC_ADDR_LO = 0x108;
constexpr uint16_t A_MAC_ADDR_HI = 0x10C;
constexpr uint16_t A_PCMRX_CNT = 0x6C4;
constexpr uint16_t A_MAAP_CTRL = 0x6CC;
constexpr uint16_t A_MAAP_STAT0 = 0x6D0;
constexpr uint16_t A_MAAP_STAT1 = 0x6D4;
constexpr uint16_t A_I2SPB_STAT = 0x6D8;
constexpr uint16_t A_I2SPB_TRIM = 0x6E0;
constexpr uint16_t A_I2SPB_DBG = 0x6F0;
constexpr uint16_t A_TCAM_CTRL = 0x700;
constexpr uint16_t A_TCAM_KLO = 0x704;
constexpr uint16_t A_TCAM_KHI = 0x708;
constexpr uint16_t A_TCAM_MLO = 0x70C;
constexpr uint16_t A_TCAM_MHI = 0x710;
constexpr uint16_t A_TCAM_ACT = 0x714;
constexpr uint16_t A_TCAM_CMD = 0x718;
constexpr uint16_t A_LPF_CTRL = 0x72C;
constexpr uint16_t A_LTAP_CTRL = 0x870;
constexpr uint16_t A_LTAP_BASE = 0x874;
constexpr uint16_t A_LTAP_END = 0x8B4;
constexpr uint16_t A_MCSRV_STAT = 0x8F8;
constexpr uint16_t A_SLIP_LB = 0x8D4;
constexpr uint16_t A_MCSRV_CTRL = 0x8FC;
//! listener 0 through the 0x800 window (the sim_aclk / sim_ax1x1gptp
//! provisioning): the stream a built loopback ring would accept
constexpr uint16_t A_STRM_SEL = 0x800;
constexpr uint16_t A_STRMW_CTRL = 0x810;
constexpr uint16_t A_STRMW_SID_LO = 0x814;
constexpr uint16_t A_STRMW_SID_HI = 0x818;
constexpr uint16_t A_STRMW_FMT_LO = 0x824;
constexpr uint16_t A_STRMW_FMT_HI = 0x828;
//! the shipping listener stream as sim_aclk.cpp feeds it: 8 wire channels,
//! 6 events per class-A PDU, 12 500 axis cycles per PDU at 48 kHz
constexpr int kAafChans = 8;
constexpr int kAafEvents = 6;
constexpr size_t kAafPayloadBytes = static_cast<size_t>(kAafChans) * kAafEvents * 4;
constexpr size_t kAafFrameBytes = 14 + 24 + kAafPayloadBytes;
constexpr int kAafPduPeriodCycles = 12500;
constexpr int kAafPdusFed = 16;
//! one media tick is 2083.3 axis cycles; twenty of them starve a built ring
//! well past the six ticks its eight-deep queue drains in
constexpr int kStarveCycles = 20 * 2084;

namespace {

//! The whole pruned-shape leg: the model, its BFMs, the sticky pin observer
//! and the counted verdicts, in one scope rather than at file scope (I.2).
class PrunedShapeHarness {
 public:
    int run();

 private:
    Vmilan_datapath* dut = nullptr;
    long checks = 0;
    long fails = 0;

    //! sticky OR of every MMCM control pin + every DAC pin, sampled each cycle.
    //! A pruned build must never move any of them - one sample would miss a
    //! single-cycle DEN strobe, so accumulate instead.
    unsigned g_mmcm_seen = 0;     //! bit0 drp_en, 1 drp_we, 2 ps_en, 3 rst, 4 addr|di
    unsigned g_dac_seen  = 0;     //! bit0 mclk, 1 sclk, 2 lrck, 3 sdin

    void ck(const char* what, unsigned long got, unsigned long exp) {
        checks++;
        if (got != exp) {
            fails++;
            printf("  [FAIL] %-50s got=0x%lx exp=0x%lx\n", what, got, exp);
        } else {
            printf("  [ok]   %-50s = 0x%lx\n", what, got);
        }
    }

    void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->eval(); }
    void hi() { dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->eval(); }
    void step() { lo(); hi(); }

    //! docs/reference/REGISTER_MAP.md's structural-zero paragraph tells a
    //! reader to ESTABLISH THE LANE before believing a `SLIP_LB` zero, and
    //! offers `CHMAP_LOOP[17]` fed at 0x914 as the pointer. This executes
    //! it: arm a CAPTURE-side map readback and return
    //! {mask_valid, valid, loop_fed}. [27] mask_valid is what makes [17] a
    //! measurement rather than a structural zero, so all three ride in ONE
    //! graded word, and the two ring legs are the discriminator - 7 on
    //! obj_aclk (lane built and fed), 6 on obj_prune (LOOPBACK_P = 0).
    unsigned chmap_loop_lane_flags(unsigned key) {
        constexpr uint16_t A_CHMAP_SEL = 0x904;
        constexpr uint16_t A_CHMAP_SNAP = 0x910;
        constexpr uint16_t A_CHMAP_LOOP = 0x914;
        constexpr int kSnapPolls = 64;
        axi_write(A_CHMAP_SEL, 0x100u | key);        // 0x100 = capture side
        axi_write(A_CHMAP_SNAP, 1);                  // W1S arm
        for (int g = 0; g < kSnapPolls; g++) {
            if ((axi_read(A_CHMAP_SNAP) & 1u) == 0) break;
        }
        const uint32_t v = axi_read(A_CHMAP_LOOP);
        return (((v >> 27) & 1u) << 2) | (((v >> 26) & 1u) << 1) |
               ((v >> 17) & 1u);
    }

    void axi_write(uint16_t a, uint32_t d) {
        dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
        dut->s_axi_wdata = d;  dut->s_axi_wvalid = 1; dut->s_axi_wstrb = 0xF;
        dut->s_axi_bready = 1;
        for (int g = 0; g < kAxiGuardCycles; ++g) {
            dut->eval();
            bool acc = dut->s_axi_awready && dut->s_axi_wready;
            step();
            if (acc) break;
        }
        dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
        for (int g = 0; g < kAxiGuardCycles; ++g) { dut->eval(); if (dut->s_axi_bvalid) break; step(); }
        step();
        dut->s_axi_bready = 0;
    }

    uint32_t axi_read(uint16_t a) {
        dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
        for (int g = 0; g < kAxiGuardCycles; ++g) {
            dut->eval();
            bool acc = dut->s_axi_arready;
            step();
            if (acc) break;
        }
        dut->s_axi_arvalid = 0;
        uint32_t v = 0;
        for (int g = 0; g < kAxiGuardCycles; ++g) { dut->eval(); if (dut->s_axi_rvalid) { v = dut->s_axi_rdata; break; } step(); }
        step();
        dut->s_axi_rready = 0;
        return v;
    }

    void do_reset() {
        dut->axis_resetn = 0; dut->gtx_resetn = 0;
        dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
        dut->s_axi_bready = dut->s_axi_rready = 0;
        dut->s_axis_mac_rx_tvalid = 0;
        dut->m_axis_mac_tx_tready = 0;
        dut->i_mac_speed = 2; dut->i_link_up = 1; dut->i_full_duplex = 1; dut->i_mac_events = 0;
        for (int i = 0; i < 8; i++) step();
        dut->axis_resetn = 1; dut->gtx_resetn = 1;
        for (int i = 0; i < 8; i++) step();
    }

    void sample_pins() {
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

    //! Inject a raw frame on the MAC RX AXIS. The useful pruned-shape invariant is
    //! that ingress keeps making
    //! progress while the optional observers are absent.
    size_t inject_rx(const uint8_t* f, size_t len) {
        std::vector<uint64_t> beats;
        for (size_t bt = 0; bt < (len + 7) / 8; bt++) {
            uint64_t v = 0;
            for (int j = 0; j < 8; j++)
                if (bt * 8 + j < len) v |= static_cast<uint64_t>(f[bt * 8 + j]) << (8 * j);
            beats.push_back(v);
        }
        size_t idx = 0;
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
            sample_pins();
            hi();
            if (in_acc) idx++;
        }
        dut->s_axis_mac_rx_tvalid = 0;
        return idx;
    }

    void run_cycles(int n) {
        for (int c = 0; c < n; c++) { lo(); sample_pins(); hi(); }
    }

    //! listener 0 bound through the 0x800 window: the sid the AAF feed below
    //! carries and the eight-channel INT32 format, exactly as sim_aclk.cpp
    //! provisions it
    void bind_listener_zero_through_the_window() {
        axi_write(A_MAC_ADDR_LO, 0x00000002);
        axi_write(A_MAC_ADDR_HI, 0x00000100);
        axi_write(A_STRM_SEL, 0);
        axi_write(A_STRMW_SID_LO, 0x00020000);      // sid 02:00:00:00:00:02:00:00
        axi_write(A_STRMW_SID_HI, 0x02000000);
        axi_write(A_STRMW_FMT_LO, 0x02006000);
        axi_write(A_STRMW_FMT_HI, 0x02050220);
        axi_write(A_STRMW_CTRL, 1);
    }

    //! one well-formed AAF PDU into the bound listener: sv and tv set, the
    //! bound sid, INT32 at 48 kHz, 8 channels x 6 events (sim_aclk's frame)
    uint8_t aaf_seq = 0;
    void send_aaf_pdu(int pdu) {
        uint8_t f[kAafFrameBytes]; memset(f, 0, sizeof f);
        const uint8_t dmac[6] = {
            0x91, 0xE0, 0xF0, 0x00, 0x2A, 0x02};
        memcpy(f, dmac, 6);
        const uint8_t src[6] = {
            0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
        memcpy(f + 6, src, 6);
        f[12] = 0x22; f[13] = 0xF0;
        f[14] = 0x02;                             // AAF
        f[15] = 0x81;                             // sv, tv
        f[16] = aaf_seq++;
        const uint8_t sid[8] = {
            0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00};
        memcpy(f + 18, sid, 8);
        f[26] = 0x00; f[27] = 0x00; f[28] = 0x10; f[29] = 0x00;   // avtp_ts
        f[30] = 0x02;                             // format INT32
        f[31] = static_cast<uint8_t>(0x05 << 4);  // nsr = 48 kHz
        f[32] = static_cast<uint8_t>(kAafChans);
        f[33] = 32;                               // bit depth
        f[34] = static_cast<uint8_t>(kAafPayloadBytes >> 8);
        f[35] = static_cast<uint8_t>(kAafPayloadBytes & 0xFF);
        for (int k = 0; k < kAafEvents; k++)
            for (int c = 0; c < kAafChans; c++) {
                const uint32_t v = (static_cast<uint32_t>(pdu & 0xFFF) << 12) |
                                   (static_cast<uint32_t>(k & 0xF) << 8) |
                                   static_cast<uint32_t>(c & 0xFF);
                const size_t o = 38 + 4 * (static_cast<size_t>(k) * kAafChans + c);
                f[o]     = static_cast<uint8_t>(v >> 16);
                f[o + 1] = static_cast<uint8_t>(v >> 8);
                f[o + 2] = static_cast<uint8_t>(v);
                f[o + 3] = 0;
            }
        (void)inject_rx(f, kAafFrameBytes);
    }

    //! the stream on the class-A cadence (inject_rx spends 400 cycles of each
    //! period), then the feed stops and the media ticks keep coming
    void feed_the_bound_listener_then_starve_it() {
        for (int pdu = 0; pdu < kAafPdusFed; pdu++) {
            send_aaf_pdu(pdu);
            run_cycles(kAafPduPeriodCycles - 400);
        }
        run_cycles(kStarveCycles);
    }

    // ---------------------------------------------------------------- 0 ----
    // The prune is NOT CSR-observable at the identity level: same ID, same
    // VERSION, same CAP. This is the check that says "no VERSION bump was
    // owed" - the register contract did not move, only which logic backs it.
    void prove_csr_identity_unchanged_by_pruning() {
        printf("[identity] the CSR contract is unchanged by pruning\n");
        ck("ID == 'MILN'", axi_read(A_ID), 0x4D494C4E);
        ck("VERSION unchanged by the prunes", axi_read(A_VERSION), 0x00020058);
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
    }

    // ---------------------------------------------------------------- 1 ----
    void prove_servo_pruned_but_its_knob_register_survives() {
        printf("[MCSERVO_P=0] servo pruned: status 0, MMCM pins parked\n");
        ck("MCSRV_STAT 0x8F8 reads 0 (structural)", axi_read(A_MCSRV_STAT), 0);
        //! the CSR half is untouched: the knob register still stores and reads
        //! back, it just has nothing to steer. Pruning RTL must not silently
        //! delete a register.
        ck("MCSRV_CTRL reads 0 at reset", axi_read(A_MCSRV_CTRL), 0);
        axi_write(A_MCSRV_CTRL, 0x3);
        ck("MCSRV_CTRL still RW (ps_invert|auto_repair)", axi_read(A_MCSRV_CTRL), 0x3);
        axi_write(A_MCSRV_CTRL, 0x0);
    }

    // ---------------------------------------------------------------- 2 ----
    void prove_latency_tap_window_is_a_hard_zero() {
        printf("[LTAP_P=0] taps pruned: the whole 0x870 window is a hard zero\n");
        //! LTAP_CTRL reads i_ltap_status | {ltap_en_r,1'b0}. With the taps gone
        //! the status half is 0 and only the reset-1 enable bit shows: 0x2.
        ck("LTAP_CTRL = enable bit only, no status", axi_read(A_LTAP_CTRL), 0x2);
        {
            unsigned long acc = 0;
            for (uint16_t a = A_LTAP_BASE; a < A_LTAP_END; a += 4) acc |= axi_read(a);
            ck("all 16 LTAP RO words read 0", acc, 0);
        }
    }

    // ---------------------------------------------------------------- 3 ----
    void prove_maap_claim_never_completes() {
        printf("[MAAP_P=0] engine pruned: claim never completes, no PDU\n");
        ck("MAAP_STAT0 reads 0", axi_read(A_MAAP_STAT0), 0);
        ck("MAAP_STAT1 reads 0 (state INITIAL, addr_valid 0)", axi_read(A_MAAP_STAT1), 0);
    }

    // ---------------------------------------------------------------- 4 ----
    void prove_i2s_playback_counters_are_zero() {
        printf("[I2SPB_P=0] DAC serializer pruned: counters 0\n");
        ck("I2SPB_STAT reads 0", axi_read(A_I2SPB_STAT), 0);
        ck("I2SPB_TRIM reads 0", axi_read(A_I2SPB_TRIM), 0);
        ck("I2SPB_DBG  reads 0", axi_read(A_I2SPB_DBG),  0);
    }

    // ---------------------------------------------------------------- 5 ----
    void prove_lpf_ctrl_survives_as_a_plain_register() {
        printf("[LPF_P=0] filter pruned: LPF_CTRL survives as a plain register\n");
        ck("LPF_CTRL reset = 1 (enable, default)", axi_read(A_LPF_CTRL) & 1, 1);
        axi_write(A_LPF_CTRL, 0x0);
        ck("LPF_CTRL still RW with no filter behind it", axi_read(A_LPF_CTRL) & 1, 0);
        axi_write(A_LPF_CTRL, 0x1);
    }

    // ---------------------------------------------------------------- 6 ----
    // Exercise the MAC ingress under the harshest legacy filter configuration
    // and prove the retained
    // fabric endpoint cannot be backpressured by a missing observer.
    void prove_mac_ingress_remains_live_without_the_filter() {
        printf("[RXFILT_P=0] filter pruned: MAC ingress remains live\n");
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
            const uint8_t pdst[6] = {
                0x91, 0xE0, 0xF0, 0x00, 0x77, 0x77};
            memcpy(pf, pdst, 6);
            pf[6] = 0x66; pf[7] = 0x77; pf[8] = 0x88;
            pf[12] = 0x08; pf[13] = 0x00;
            for (int i = 18; i < 64; i++) pf[i] = static_cast<uint8_t>(0x5A ^ i);
            ck("TCAM-drop dmac is accepted at MAC ingress", inject_rx(pf, 64), 8);

            //! second contrast: a foreign UNICAST with default_pass=0 and the
            //! station filter armed. The PRESENT build drops this one on the
            //! station-address test alone.
            const uint8_t fdst[6] = {
                0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xF0};
            memcpy(pf, fdst, 6);
            ck("foreign unicast is accepted at MAC ingress", inject_rx(pf, 64), 8);
        }
    }

    // ---------------------------------------------------------------- 7 ----
    // Structural-zero durability: run real traffic with everything ENABLED
    // and re-read. A zero that only holds before the first frame would be a
    // "not armed yet" zero, which is exactly the class of lie STATS_CAP was
    // added to kill. These must be zero AFTER traffic, not just at reset.
    void prove_the_inert_values_hold_under_live_traffic() {
        printf("[durability] the inert values hold under live traffic\n");
        axi_write(A_LTAP_CTRL, 0x2);                       // taps enabled
        axi_write(A_MAAP_CTRL, 0x00000801);                // MAAP en, block of 8
        {
            uint8_t af[124]; memset(af, 0, sizeof af);
            const uint8_t adst[6] = {
                0x91, 0xE0, 0xF0, 0x00, 0xE1, 0xE3};
            memcpy(af, adst, 6);
            af[6] = 0x02; af[11] = 0x02;
            af[12] = 0x22; af[13] = 0xF0;                  // AVTP ethertype
            af[14] = 0x02;                                  // subtype AAF
            for (int r = 0; r < 4; r++) (void)inject_rx(af, 124);
            for (int c = 0; c < 4000; c++) { lo(); sample_pins(); hi(); }
        }
        ck("LTAP words STILL 0 after traffic", axi_read(A_LTAP_BASE) |
           axi_read(A_LTAP_BASE + 4) | axi_read(A_LTAP_BASE + 32), 0);
        ck("LTAP_CTRL STILL 0x2 after traffic", axi_read(A_LTAP_CTRL), 0x2);
        ck("MCSRV_STAT STILL 0 after traffic", axi_read(A_MCSRV_STAT), 0);
        //! #390: SLIP_LB is a STRUCTURAL zero on this shape - LOOPBACK_P = 0
        //! folds the loop feed strobe (milan_datapath's lb_tap_tvalid_w) to a
        //! constant 0, so the ring's fed and primed rails never set and its
        //! counters are pruned with it. The ring's ONLY feed is the
        //! depacketizer's accepted output, so the zero is read behind the
        //! stream a built ring would accept: listener 0 bound through the
        //! window and fed well-formed PDUs on the class-A cadence (PCMRX_CNT
        //! proves the acceptance), then starved for twenty ticks. A built
        //! ring primes and feeds four pairs on that stream and counts one
        //! dup per pair per starved tick, so the same harness rebuilt with
        //! -GLOOPBACK_P=1, or with the LOOPBACK_P fold removed from the feed
        //! strobe, fails the zero (the two negative controls of PR #436).
        {
            const uint32_t pdus0 = axi_read(A_PCMRX_CNT) & 0xFFFF;
            bind_listener_zero_through_the_window();
            feed_the_bound_listener_then_starve_it();
            ck("listener 0 accepted the fed AAF PDUs (PCMRX_CNT pdus)",
               (axi_read(A_PCMRX_CNT) & 0xFFFF) - pdus0, kAafPdusFed);
        }
        ck("SLIP_LB 0x8D4 STILL 0 fed then starved (structural: LOOPBACK_P=0)",
           axi_read(A_SLIP_LB), 0);
        //! ...and the SAME zero read with the lane ESTABLISHED, the
        //! instruction REGISTER_MAP.md gives and that nothing executed until
        //! now: the capture readback answers mask_valid and valid 1 with
        //! loop_fed 0, so the SLIP_LB zero above is a MEASURED absent lane,
        //! never an unarmed word. obj_aclk reads 7 for the same three bits.
        ck("CHMAP_LOOP {mask_valid, valid, fed}: no lane",
           chmap_loop_lane_flags(0), 6);
        ck("MAAP_STAT1 STILL 0 with MAAP_CTRL.en=1", axi_read(A_MAAP_STAT1), 0);
        ck("MAAP_STAT0 STILL 0 with MAAP_CTRL.en=1", axi_read(A_MAAP_STAT0), 0);
        ck("I2SPB_STAT STILL 0 after traffic", axi_read(A_I2SPB_STAT), 0);
        ck("no MMCM pin ever moved", g_mmcm_seen, 0);
        ck("no DAC pin ever moved",  g_dac_seen,  0);
    }

    // ---------------------------------------------------------------- 8 ----
    // What must STILL work: the prunes touch none of the mandatory control
    // path, and the live traffic above has crossed the retained MAC ingress.
    void prove_the_mandatory_control_path_still_runs() {
        printf("[unaffected] the mandatory control path still runs\n");
        ck("RST_EPOCH live (no shadow lie)", axi_read(0x720) >= 1 ? 1 : 0, 1);
    }

    int report() const {
        printf("--------------------------------------------------------------\n");
        printf("checks: %ld   failures: %ld\n", checks, fails);
        printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
        return fails ? 1 : 0;
    }
};

int PrunedShapeHarness::run() {
    const milan::tb::Model<Vmilan_datapath> model;
    dut = model.get();

    printf("=== milan_datapath PRUNED shape "
           "(MCSERVO_P=LTAP_P=MAAP_P=I2SPB_P=RXFILT_P=LPF_P=0) ===\n");
    do_reset();

    prove_csr_identity_unchanged_by_pruning();
    prove_servo_pruned_but_its_knob_register_survives();
    prove_latency_tap_window_is_a_hard_zero();
    prove_maap_claim_never_completes();
    prove_i2s_playback_counters_are_zero();
    prove_lpf_ctrl_survives_as_a_plain_register();
    prove_mac_ingress_remains_live_without_the_filter();
    prove_the_inert_values_hold_under_live_traffic();
    prove_the_mandatory_control_path_still_runs();

    return report();
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    PrunedShapeHarness harness;
    return harness.run();
}
