// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_aclk - the media-grid ALIGNMENT proof, at the TRUE clock ratio.
//
// WHY THIS IS ITS OWN BINARY. Every other milan_dp leg toggles clk_audio_i
// (and, since 2026-08-10, clk_tdm_i) 1:1 with axis_clk. That is fine for the
// 380-odd functional checks those legs run - none of them care about the audio
// clock's RATE - but it means the one property the media clock actually has to
// hold cannot be observed anywhere else in the tree:
//
//     the TDM word clock and the AAF packet grid must stay ALIGNED
//
// On the shipping board's divider plan the two grids differ by a compile-time
// constant, not a tolerance:
//
//   clk_audio = 100 MHz * 23/2 /37 * 34/43 = 100e6 * 391/1591
//             = 24,575,738.5292 Hz            (PLAN A, milan_soc.py:363)
//   clk_tdm   = clk_audio                     (milan_soc.py nulls audio_tdm_hz
//                                              at 24.576 MHz and binds
//                                              ClockSignal("audio"))
//   fsync     = clk_tdm / (2*8*32) = /512     = 47,999.4893 Hz
//   media_tick_p                              = 48,000.0000 Hz exactly
//                                              (KL_media_nco off axis_clk)
//   => -10.6393 ppm, one whole sample of slip every 1.9582 s
//
// 391/1591 is exact and reduced (23*34 / (2*37*43)), and BOTH clocks come off
// the same 100 MHz oscillator, so this is a pure divider-plan constant with no
// oscillator noise in it. That is exactly why an integer-ratio model is
// faithful rather than an approximation - there is nothing stochastic to miss.
//
// TWO PHASES since #74, one instrument:
//
//   [INTERNAL] clock_source INTERNAL free-runs by USER rule ("internal media
//   clock = free-run, slips accepted"), so the -10.64 ppm drift is PRESENT,
//   measured, and matches the divider plan - the accepted state, kept honest
//   rather than hidden (the junction counters in KL_chan_map_capture count
//   its slips).
//
//   [CRF] the STORED clock-source selection is poked to this shape's CRF
//   index (a documented public_flat_rw tap on the processor's dyn-state row;
//   the AECP command path INTO that row - SET_CLOCK_SOURCE -> store ->
//   clk_src_index_o -> the root resolve - is pinned end-to-end by sim_nxn's
//   AECP-FACE arms, so the poke sits one hop upstream of a proven chain), a
//   CRF stream locks the sink, and the SAME period instrument that proved
//   the drift now proves the grids ALIGNED: KL_media_grid_align holds the
//   packet grid on the physical one. The MMCM servo's status slice goes
//   non-zero under the CRF stimulus (the exact live slice, A_MCSRV_STAT
//   [31:16]), and the 1722-2016 4.4.4.3 mr machinery becomes reachable: a
//   received mr toggle on the followed stream flips OUR outgoing mr, and
//   stops doing so the moment the selection returns to INTERNAL (10.4.3's
//   own scoping).
//
// WHAT IT DOES NOT DO. It does not wait for a whole sample of slip
// (195,815,385 axis cycles); it measures RATES, which needs ~1e7 cycles for
// 0.1 ppm resolution. The silicon counterpart is AX7101 J11.8 (tdm_fsync_o)
// against J11.9 (media_lrclk_o) on a two-channel probe.
//
// THE RENDER LAW (#386), three more phases on the same instrumented clock:
//
//   [RENDER-INT] listener 0 is bound over ACMP (the sim_main ladder: BIND_RX,
//   the harvested PROBE_TX, a played CONNECT_TX_RESPONSE) and fed 8-channel
//   class-A AAF PDUs at EXACTLY the packet grid's cadence (12500 axis cycles
//   at 100 MHz) with every sample naming its {pdu, event, channel}. The
//   accept-to-render delay of each PDU is timed from the monitor's accept
//   pulse to the setpoint stage's pop of that PDU's event 0 (the render
//   crossbar's input grid), and the law is asserted PER PDU: the fill at
//   accept is the setpoint, the delay is inside (SETPOINT, SETPOINT + 1]
//   media ticks, and with the cadence locked the spread is a few cycles.
//
//   [RENDER-CRF] the same, under CRF selection with the grids aligned, the
//   cadence now locked to the PHYSICAL grid (12500 + 52/391 cycles: the
//   fsync period times six). Same setpoint, same band: the constant does
//   not depend on the selected clock source, only the sub-tick phase does.
//
//   [RENDER-RC] at INTERNAL and again under CRF: the cadence is shifted three
//   ticks later, which the instrument sees as a displaced fill (the negative
//   control of the measurement itself), then a PHC adjtime through CLKV
//   software (the plane is off in this leg, so PTP_CMD[1] IS the step) fires
//   the recentre: the next PDU end restores the law, the recentre is counted
//   ONCE, and a hundred more PDUs show neither a second recentre nor a drift
//   back. Then the same three ticks EARLY, which reaches the recentre's other
//   branch (a long queue snaps instead of re-entering prefill).
//
//   [RENDER-LIVE] the clock source is changed UNDER THE RUNNING STREAM, the
//   case a restarted feed never sees. The feed is first moved past a tick
//   (the grid-moved-0.6-tick equivalent: the fill sits one event off the
//   setpoint, the delay outside the band, no rail, converged) and the stream
//   keeps running through the INTERNAL measurement and the CRF selection.
//   The datapath's settled-grid trigger then fires ONE recentre once the
//   aligner's error has rested inside its band, and every PDU of the aligned
//   window is back at the setpoint. The deselect (back to INTERNAL) is the
//   same arm the other way: the feed is moved past a tick the other way
//   (fill one short), the source change fires one recentre after its dwell,
//   and the law holds again.
//
//   render_mutants.py rebuilds this leg against mutated copies of the stage
//   (a wrong prefill target; the recentre pulse ignored; the recentre counted
//   but not snapped) and of the datapath (the clock-source trigger dropped
//   from the recentre set) and requires the named checks to FAIL by their own
//   verdict. --render-only and --live-only are the short legs it runs.

#include "../../common/verilator_harness.hpp"
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"

#include <array>
#include <cstdio>
#include <cstdint>
#include <cmath>
#include <cstring>
#include <string>
#include <vector>

//! AXI4-Lite handshake guard: cycles a single beat may wait before the BFM
//! gives up rather than hanging the leg.
constexpr int kAxiGuardCycles = 2048;
//! The CRF cadence this leg feeds: 96 samples per PDU at 48 kHz is 2 ms, and
//! 2 ms of the 100 MHz axis clock is 200 000 cycles.
constexpr long kCrfPduPeriodCycles = 200000;
//! The AAF cadence: six events per class-A PDU at 48 kHz on the 100 MHz axis
//! clock is 12 500 cycles on the packet grid; on the physical grid the fsync
//! period is 512 x 1591/391 cycles, so six of them are 12 500 + 52/391.
constexpr long kAafPduPeriodCycles = 12500;
constexpr long kAafPhysFracNum = 52;
constexpr long kAafPhysFracDen = 391;
//! one media tick on the packet grid, in axis cycles (100 MHz / 48 kHz)
constexpr double kTickCycles = 100e6 / 48000.0;
//! the shipping listener stream: 8 wire channels, 6 events per PDU
constexpr int kAafChans = 8;
constexpr int kAafEvents = 6;
constexpr size_t kAafPayloadBytes = static_cast<size_t>(kAafChans) * kAafEvents * 4;
constexpr size_t kAafFrameBytes = 14 + 24 + kAafPayloadBytes;
//! the render setpoint as milan_datapath derives it: one class-A PDU of
//! events plus the two-tick allowance (RENDER_SETPOINT_EVT_C). Stated here
//! as the LAW under test, not read back from the DUT.
constexpr int kRenderSetpointEvt = kAafEvents + 2;
//! registration slack on the band's upper edge: the accept pulse and the pop
//! pulse are each one register behind their events
constexpr long kBandSlackCycles = 64;
//! PDUs skipped at the start of a window (prefill and lock) and at its end
//! (the last PDUs have not rendered yet)
constexpr int kLawSkipHead = 40;
constexpr int kLawSkipTail = 4;
//! a PHC adjtime of 65 536 ns: any nonzero step is the recentre trigger
constexpr uint32_t kPhcStepNs = 0x00010000;
//! The loopback-ring aim (#390, the banner inside the class): land the restart
//! burst this far after a media tick, and accept it inside the band.
constexpr double kRingAimPhase = 0.93;
constexpr long kRingAimCycles = static_cast<long>(kRingAimPhase * kTickCycles + 0.5);
constexpr long kRingAimBandLo = static_cast<long>(0.90 * kTickCycles);
constexpr long kRingAimBandHi = static_cast<long>(0.96 * kTickCycles);
//! one physical frame of the audio clock in half() calls: 512 audio cycles x
//! 2 edges x 1591/391 = 4166.7 half-steps
constexpr long kFrameHalfSteps = 4167;

// ---------------------------------------------------------------------- //
//  The fractional-N audio clock (exact 391/1591 - see the banner).        //
// ---------------------------------------------------------------------- //
constexpr long AUD_NUM = 391;
constexpr long AUD_DEN = 1591;

namespace {

//! The whole media-grid alignment leg: the model, the fractional-N audio
//! clock, the one period instrument, the CRF feeder and the counted verdicts
//! in one scope rather than at file scope (I.2).
class MediaGridAlignmentHarness {
 public:
    int run();
    bool render_only = false;   //! --render-only: the mutation arm's short leg (the stage)
    bool live_only = false;     //! --live-only: the mutation arm's short leg (the datapath trigger)

 private:
    Vmilan_datapath* dut = nullptr;
    long checks = 0;
    long fails = 0;

    void ck(const char* what, unsigned long got, unsigned long exp) {
        checks++;
        if (got != exp) { fails++; printf("  [FAIL] %-58s got=%lu exp=%lu\n", what, got, exp); }
        else            { printf("  [ok]   %-58s = %lu\n", what, got); }
    }

    // the fractional-N accumulator state for the audio clock above
    long acc = 0;
    int  aud = 0;
    long axis_cycle = 0;

    //! the TDM-junction slip inducers (#390): hold_steps freezes the audio
    //! clock for that many half-steps (one frame = one missing marker = one
    //! dup), boost_steps doubles its rate (two frames per tick = skips)
    long aud_hold_steps = 0;
    long aud_boost_steps = 0;
    void half() {
        if (aud_hold_steps > 0) {
            aud_hold_steps--;
        } else {
            acc += (aud_boost_steps > 0) ? 2 * AUD_NUM : AUD_NUM;
            if (aud_boost_steps > 0) aud_boost_steps--;
            if (acc >= AUD_DEN) { acc -= AUD_DEN; aud ^= 1; }
        }
        dut->clk_audio_i = aud;
        dut->clk_tdm_i   = aud;
    }

    // ---- the ONE period instrument, observing inside step() so that CSR    //
    //      traffic and frame injection (which step the clock themselves)     //
    //      can never lose an edge of either grid                             //
    long m_first = 0;
    long m_last = 0;
    long m_n = 0;
    long f_first = 0;
    long f_last = 0;
    long f_n = 0;
    int  f_prev = 0;

    void obs_reset() {
        m_first = m_last = f_first = f_last = -1; m_n = f_n = 0;
        f_prev = dut->tdm_fsync_o;
    }

    // ---- the render instrument: accept pulses, popped events, pulses ----
    //! accept i belongs to the i-th AAF PDU injected since the feed started
    //! (the depacketizer keeps order and this leg drops nothing). Records are
    //! kept by injection SEQUENCE, not by the 12-bit wire id: the live feed
    //! now runs through phases long enough for the id to wrap, and at most a
    //! dozen PDUs are ever in flight, so the id of a popped event names the
    //! latest sequence injected with it.
    std::vector<long> aaf_injected;        //! sequence numbers, in injection order
    size_t            accepts_seen = 0;
    std::vector<long> accept_cycle;        //! by sequence
    std::vector<int>  fill_at_accept;      //! the stage's fill at that instant
    std::vector<long> render_cycle;        //! by sequence: event 0 popped
    std::array<long, 4096> id_seq{};       //! wire id -> the latest sequence carrying it
    long recentre_pulses = 0;              //! render_recentre_p_w edges
    long src_recentre_pulses = 0;          //! the datapath's clock-source trigger pulses

    void ensure_slot(long seq) {
        while (static_cast<long>(accept_cycle.size()) <= seq) {
            accept_cycle.push_back(-1); fill_at_accept.push_back(-1); render_cycle.push_back(-1);
        }
    }

    void observe_render() {
        if (dut->rootp->milan_datapath__DOT__avtprx_accept_p && accepts_seen < aaf_injected.size()) {
            const long seq = aaf_injected[accepts_seen++];
            ensure_slot(seq);
            accept_cycle[seq]   = axis_cycle;
            fill_at_accept[seq] = dut->rootp->milan_datapath__DOT__rsp_fill_w & 0xFF;
        }
        if (dut->rootp->milan_datapath__DOT__rsp_pop_p_w & 1) {
            const uint64_t d = dut->rootp->milan_datapath__DOT__rsp_tdata_w;
            const uint32_t s0 = (static_cast<uint32_t>(d & 0xFF) << 16) |
                                (static_cast<uint32_t>((d >> 8) & 0xFF) << 8) |
                                static_cast<uint32_t>((d >> 16) & 0xFF);
            const int pdu = static_cast<int>((s0 >> 12) & 0xFFF);
            const int event = static_cast<int>((s0 >> 8) & 0xF);
            const long seq = id_seq[static_cast<size_t>(pdu)];
            if (event == 0 && seq >= 0) { ensure_slot(seq); if (render_cycle[seq] < 0) render_cycle[seq] = axis_cycle; }
        }
        if (dut->rootp->milan_datapath__DOT__render_recentre_p_w) recentre_pulses++;
        if (dut->rootp->milan_datapath__DOT__src_recentre_p_r) src_recentre_pulses++;
    }

    //! THE PROBE SNIFFER (the sim_main ladder): the processor's listener
    //! launches a CONNECT_TX_COMMAND at the named talker and takes the
    //! stream_id from the ANSWER, so the probe's sequence_id is harvested
    //! off the egress and echoed back by the played talker.
    std::vector<uint8_t> sniff_fr;
    uint16_t probe_seq = 0;
    bool     probe_seen = false;

    void sniff_probe() {
        if (!(dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready)) return;
        for (int l = 0; l < 8; l++)
            if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                sniff_fr.push_back(static_cast<uint8_t>((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF));
        if (!dut->m_axis_mac_tx_tlast) return;
        if (sniff_fr.size() >= 64 && sniff_fr[12] == 0x22 && sniff_fr[13] == 0xF0 &&
            sniff_fr[14] == 0xFC && (sniff_fr[15] & 0xF) == 0x0) {
            probe_seq  = static_cast<uint16_t>((sniff_fr[62] << 8) | sniff_fr[63]);
            probe_seen = true;
        }
        sniff_fr.clear();
    }

    void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; half(); dut->eval(); }
    int drp_lat = 0;
    void hi() {
        dut->axis_clk = 1; dut->gtx_clk = 1; half(); dut->eval();
        axis_cycle++;
        observe_render();
        sniff_probe();
        // minimal DRP responder: DRDY a few cycles after DEN, data 0. With
        // auto_repair off a VERIFY mismatch is informative-only and the servo
        // proceeds to ACQUIRE - the state this leg grades. The true ClkReg
        // contents live in tb/verilator/mmcm_servo's full MMCM model.
        dut->i_mmcm_drp_rdy = 0;
        if (drp_lat > 0 && --drp_lat == 0) dut->i_mmcm_drp_rdy = 1;
        if (dut->o_mmcm_drp_en) drp_lat = 3;
        dut->i_mmcm_drp_do = 0;
        if (dut->rootp->milan_datapath__DOT__media_tick_p) {
            if (m_first < 0) m_first = axis_cycle;
            m_last = axis_cycle; m_n++;
        }
        const int f = dut->tdm_fsync_o;
        if (f && !f_prev) {
            if (f_first < 0) f_first = axis_cycle;
            f_last = axis_cycle; f_n++;
        }
        f_prev = f;
        observe_the_loop_ring();
    }
    void step() { lo(); hi(); }

    // measured fsync-vs-media rate difference in ppm over the current window.
    // NEGATIVE = fsync slower. NAN-free by construction: callers gate on counts.
    double window_ppm() {
        const double t_media = double(m_last - m_first) / double(m_n - 1);
        const double t_fsync = double(f_last - f_first) / double(f_n - 1);
        return (t_media / t_fsync - 1.0) * 1e6;
    }

    // ---- AXI4-Lite BFM (the sim_main helper, on this leg's instrumented    //
    //      clock) ----
    void axi_write(uint16_t a, uint32_t d) {
        dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
        dut->s_axi_wdata = d;  dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
        dut->s_axi_bready = 1;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); bool acc_w = dut->s_axi_awready && dut->s_axi_wready; hi();
            if (acc_w) break;
        }
        dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
        for (int g = 0; g < kAxiGuardCycles; g++) { lo(); bool bv = dut->s_axi_bvalid; hi(); if (bv) break; }
        dut->s_axi_bready = 0;
    }
    uint32_t axi_read(uint16_t a) {
        dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
        for (int g = 0; g < kAxiGuardCycles; g++) { lo(); bool ar = dut->s_axi_arready; hi(); if (ar) break; }
        dut->s_axi_arvalid = 0;
        uint32_t d = 0;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); bool rv = dut->s_axi_rvalid; if (rv) d = dut->s_axi_rdata; hi();
            if (rv) break;
        }
        dut->s_axi_rready = 0;
        return d;
    }

    // ---- one frame into the MAC ingress (little byte lane, as everywhere) --
    void inject(const uint8_t* f, size_t len) {
        std::vector<uint64_t> beats;
        for (size_t bt = 0; bt < (len + 7) / 8; bt++) {
            uint64_t v = 0;
            for (int j = 0; j < 8; j++)
                if (bt*8 + j < len) v |= static_cast<uint64_t>(f[bt*8+j]) << (8*j);
            beats.push_back(v);
        }
        size_t idx = 0;
        for (int c = 0; c < 1500 && idx < beats.size() + 8; c++) {
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
            hi();
            if (in_acc || idx >= beats.size()) idx++;
        }
        dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
    }

    // ---- the CRF stream into the provisioned sink (sim_main's [CRF] frame,  //
    //      500 PDU/s: 96 samples = 2 ms per PDU, timestamps at the NOMINAL    //
    //      rate so the servo reads clk_audio's honest deviation) ----
    uint64_t crf_ts  = 1000000000ULL;
    uint8_t  crf_seq = 0;
    long     next_pdu_at = 0;
    int      crf_mr = 0;

    void send_crf() {
        uint8_t f[64]; memset(f, 0, sizeof f);
        const uint8_t dmac[6] = {
            0x91,0xE0,0xF0,0x00,0x2A,0x03};
        memcpy(f, dmac, 6);
        const uint8_t src[6] = {
            0x02,0x00,0x00,0x00,0x00,0x02};
        memcpy(f+6, src, 6);
        f[12]=0x22; f[13]=0xF0;
        f[14]=0x04;                               // CRF subtype
        f[15]=static_cast<uint8_t>(0x80 | (crf_mr ? 0x08 : 0x00));
        f[16]=crf_seq++;
        f[17]=0x01;                               // CRF_AUDIO_SAMPLE
        const uint8_t sid[8] = {
            0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x01};
        memcpy(f+18, sid, 8);
        f[26]=0x00; f[27]=0x00; f[28]=0xBB; f[29]=0x80;   // pull0|48000
        f[30]=0x00; f[31]=0x08;                   // crf_data_length 8
        f[32]=0x00; f[33]=96;                     // timestamp_interval
        for (int i = 0; i < 8; i++) f[34+i] = static_cast<uint8_t>(crf_ts >> (8*(7-i)));
        crf_ts += 2000000ULL;
        inject(f, 64);
    }

    // ---- the AAF stream into the bound listener: 8 channels x 6 events, --
    //      every sample = {pdu[11:0], event[3:0], channel[7:0]} in S32BE --
    bool    aaf_on = false;
    long    aaf_next_at = 0;
    long    aaf_frac_acc = 0;
    long    aaf_frac_num = 0;           //! 0 on the packet grid, 52 on the physical one
    uint8_t aaf_wire_seq = 0;           //! the AVTP sequence_num byte
    long    aaf_seq = 0;                //! the next injection sequence (its wire id is the low 12 bits)

    void send_aaf() {
        const int aaf_pdu = static_cast<int>(aaf_seq & 0xFFF);
        uint8_t f[kAafFrameBytes]; memset(f, 0, sizeof f);
        const uint8_t dmac[6] = {
            0x91,0xE0,0xF0,0x00,0x2A,0x02};
        memcpy(f, dmac, 6);
        const uint8_t src[6] = {
            0x02,0x00,0x00,0x00,0x00,0x02};
        memcpy(f+6, src, 6);
        f[12]=0x22; f[13]=0xF0;
        f[14]=0x02;                               // AAF
        f[15]=0x81;                               // sv, tv
        f[16]=aaf_wire_seq++;
        const uint8_t sid[8] = {
            0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x00};
        memcpy(f+18, sid, 8);
        f[26]=0x00; f[27]=0x00; f[28]=0x10; f[29]=0x00;   // avtp_ts (not late/early)
        f[30]=0x02;                               // format INT32
        f[31]=static_cast<uint8_t>(0x05 << 4);    // nsr = 48 kHz
        f[32]=static_cast<uint8_t>(kAafChans);
        f[33]=32;                                 // bit depth
        f[34]=static_cast<uint8_t>(kAafPayloadBytes >> 8);
        f[35]=static_cast<uint8_t>(kAafPayloadBytes & 0xFF);
        for (int k = 0; k < kAafEvents; k++)
            for (int c = 0; c < kAafChans; c++) {
                const uint32_t v = (static_cast<uint32_t>(aaf_pdu & 0xFFF) << 12) |
                                   (static_cast<uint32_t>(k & 0xF) << 8) |
                                   static_cast<uint32_t>(c & 0xFF);
                const size_t o = 38 + 4 * (static_cast<size_t>(k) * kAafChans + c);
                f[o]   = static_cast<uint8_t>(v >> 16);
                f[o+1] = static_cast<uint8_t>(v >> 8);
                f[o+2] = static_cast<uint8_t>(v);
                f[o+3] = 0;
            }
        aaf_injected.push_back(aaf_seq);
        id_seq[static_cast<size_t>(aaf_pdu)] = aaf_seq;
        aaf_seq++;
        inject(f, kAafFrameBytes);
    }

    //! the next AAF slot: an integer period plus a fraction on the physical grid
    void advance_aaf_slot() {
        aaf_next_at += kAafPduPeriodCycles;
        aaf_frac_acc += aaf_frac_num;
        if (aaf_frac_acc >= kAafPhysFracDen) { aaf_frac_acc -= kAafPhysFracDen; aaf_next_at += 1; }
    }

    //! start the feed, or - under a running one - restart its RECORDS only:
    //! the stream keeps its cadence, and the PDU in flight lands (is
    //! accepted) before the books are cleared so no accept is misattributed
    void start_aaf_feed(long frac_num) {
        if (aaf_on) {
            run_to_a_fresh_slot();
            for (int g = 0; g < 4000 && accepts_seen < aaf_injected.size(); g++) step();
        }
        aaf_injected.clear(); accepts_seen = 0;
        accept_cycle.clear(); fill_at_accept.clear(); render_cycle.clear();
        id_seq.fill(-1);
        aaf_seq = 0;                         //! sequences restart with the records
        aaf_frac_num = frac_num; aaf_frac_acc = 0;
        if (!aaf_on) aaf_next_at = axis_cycle + 64;
        aaf_on = true;
    }

    //! step until a PDU has just gone out, so a cadence shift applied next
    //! lands on a slot a whole period away (never on one already due)
    void run_to_a_fresh_slot() {
        while (aaf_next_at - axis_cycle < kAafPduPeriodCycles - 64) run_fed(1);
    }

    //! move the running feed's cadence by `ticks` media ticks (negative =
    //! earlier); the stream never stops, so the stage sees exactly the
    //! sub-tick phase step a moved grid would show it
    void shift_the_running_feed(double ticks) {
        run_to_a_fresh_slot();
        aaf_next_at += static_cast<long>(ticks * kTickCycles);
    }


    // step n cycles with the CRF stream kept alive at its 2 ms cadence (once
    // the sink is provisioned) and the AAF stream at its own (once bound)
    bool crf_on = false;
    //! the live selection's records (set by the CRF phase, judged after it)
    uint32_t live_rc0 = 0;
    long     live_pulses0 = 0;
    long     live_src0 = 0;
    long     live_first_seq = 0;
    long     live_last_seq = 0;
    void run_fed(long n) {
        const long stop = axis_cycle + n;
        while (axis_cycle < stop) {
            if (crf_on && axis_cycle >= next_pdu_at) { send_crf(); next_pdu_at += kCrfPduPeriodCycles; }
            else if (aaf_on && axis_cycle >= aaf_next_at) { send_aaf(); advance_aaf_slot(); }
            else step();
        }
    }

    // capture n outgoing CRF PDUs (subtype 0x04) off the MAC egress
    long cap_crf(int n, std::vector<std::array<uint8_t,64>>& out, long budget) {
        out.clear();
        std::vector<uint8_t> c2;
        const long stop = axis_cycle + budget;
        while (axis_cycle < stop && static_cast<int>(out.size()) < n) {
            if (axis_cycle >= next_pdu_at) { send_crf(); next_pdu_at += kCrfPduPeriodCycles; continue; }
            if (aaf_on && axis_cycle >= aaf_next_at) { send_aaf(); advance_aaf_slot(); continue; }
            step();
            if (!dut->m_axis_mac_tx_tvalid) continue;
            uint64_t d = dut->m_axis_mac_tx_tdata;
            for (int j = 0; j < 8; j++) c2.push_back(static_cast<uint8_t>(d >> (8*j)));
            if (dut->m_axis_mac_tx_tlast) {
                if (c2.size() >= 42 && c2[12]==0x22 && c2[13]==0xF0 && c2[14]==0x04) {
                    std::array<uint8_t,64> f{};
                    for (size_t k = 0; k < c2.size() && k < 64; k++) f[k] = c2[k];
                    out.push_back(f);
                }
                c2.clear();
            }
        }
        return static_cast<long>(out.size());
    }

    //! the documented tap (see the pp-side banner on clksrc_r): the STORE is
    //! poked, one hop upstream of the command chain sim_nxn's AECP-FACE arms
    //! prove end-to-end. AX 1x1 shape: internal 0, Stream Clock 1, CRF 2.
    void poke_clksrc(uint16_t v) {
        dut->rootp
            ->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r[0]
            = v;
        for (int i = 0; i < 8; i++) step();
    }

    void bring_out_of_reset() {
        dut->axis_resetn = 0; dut->gtx_resetn = 0;
        dut->m_axis_mac_tx_tready = 1;
        obs_reset();
        for (int i = 0; i < 64; i++) step();
        dut->axis_resetn = 1; dut->gtx_resetn = 1;
        for (int i = 0; i < 512; i++) step();
    }

    // =================================================================== //
    //  PHASE 1 - INTERNAL: free-run by USER rule, the drift present,      //
    //  measured, and equal to the divider plan.                           //
    // =================================================================== //
    //! Returns false when neither grid ticked: the leg has already printed
    //! its own tally and the caller must exit 1 without measuring.
    bool measure_the_internal_free_run_drift(double& ppm_int) {
        printf("\n[INTERNAL] clock_source INTERNAL: free-run, slips accepted\n");
        const long RUN = 10000000;          // ~0.1 s of board time, ~4800 ticks
        obs_reset();
        run_fed(RUN);                       //! the AAF feed, when live, keeps running

        printf("  media_tick_p : %ld ticks, first %ld last %ld\n", m_n, m_first, m_last);
        printf("  tdm_fsync_o  : %ld frames, first %ld last %ld\n", f_n, f_first, f_last);
        ck("media grid ticked", m_n > 2, 1);
        ck("TDM master framed", f_n > 2, 1);
        if (m_n <= 2 || f_n <= 2) {
            printf("\n  [FAIL] nothing to measure - the ratio test needs both grids live\n");
            printf("media_aclk: %ld checks, %ld failures\n", checks, fails + 1);
            return false;
        }

        ppm_int = window_ppm();
        const double t_media_exp = 100e6 / 48000.0;
        const double t_fsync_exp = 512.0 * double(AUD_DEN) / double(AUD_NUM);
        const double ppm_exp = (t_media_exp / t_fsync_exp - 1.0) * 1e6;  // -10.6393

        printf("  MEASURED     : %+9.4f ppm   (closed form %+9.4f ppm)\n",
               ppm_int, ppm_exp);
        printf("  one sample of slip every %.4f s\n",
               1.0 / (48000.0 * std::fabs(ppm_int) * 1e-6));

        // Resolution: one axis cycle of quantisation on each period over ~4800
        // ticks is about 0.10 ppm, so a 0.5 ppm gate is four sigma.
        ck("INTERNAL: fsync SLOWER than the media grid (the known drift)",
           ppm_int < 0.0, 1);
        ck("INTERNAL: drift matches the divider plan within 0.5 ppm",
           std::fabs(ppm_int - ppm_exp) < 0.5, 1);
        ck("INTERNAL: the grids free-run apart (USER rule: slips accepted)",
           std::fabs(ppm_int) > 1.0, 1);
        ck("INTERNAL: align loop disengaged",
           dut->rootp->milan_datapath__DOT__mga_engaged_w, 0);
        ck("INTERNAL: NCO servo gate low",
           dut->rootp->milan_datapath__DOT__mnco_servo_en_w, 0);
        return true;
    }

    // =================================================================== //
    //  PHASE 2 - CRF selected: the SAME instrument proves alignment.      //
    // =================================================================== //
    void select_crf_and_prove_the_grids_align(double ppm_int) {
        printf("\n[CRF] the stored selection goes to this shape's CRF index (2)\n");
        //! CSR byte offsets, plain integers by intent: each is handed straight to
        //! the AXI BFM as an address, so `constexpr` keeps the call sites
        //! cast-free (Enum.5).
        constexpr uint16_t A_MAC_ALO = 0x108;
        constexpr uint16_t A_MAC_AHI = 0x10C;
        constexpr uint16_t A_CRF_CTRL = 0x738;
        constexpr uint16_t A_CRF_SIDLO = 0x73C;
        constexpr uint16_t A_CRF_SIDHI = 0x740;
        constexpr uint16_t A_CRFT_CTRL = 0x750;
        constexpr uint16_t A_MCSRV_STAT = 0x8F8;
        dut->i_mmcm_locked = 1;
        axi_write(A_MAC_ALO, 0x00000002);
        axi_write(A_MAC_AHI, 0x00000100);
        // provision the CRF sink exactly as [CRF] in sim_main does
        axi_write(A_CRF_SIDLO, 0x00020001);
        axi_write(A_CRF_SIDHI, 0x02000000);
        axi_write(A_CRF_CTRL,  0x1);
        // the CRF Media Clock Output, for the mr half below
        axi_write(A_CRFT_CTRL, 0x1);

        //! the live stream's records around the selection: the trigger's
        //! one pulse must land inside the pull-in wait, and the aligned
        //! window's PDUs are the law's witnesses ([RENDER-LIVE-CRF])
        live_rc0     = dut->rootp->milan_datapath__DOT__rsp_recentres_w;
        live_pulses0 = recentre_pulses;
        live_src0    = src_recentre_pulses;
        poke_clksrc(2);
        //! a talker on the CRF grid: from here the feed's cadence is the
        //! physical grid's, the one the packet grid is about to follow
        if (aaf_on) aaf_frac_num = kAafPhysFracNum;
        ck("CRF: the root resolve sees the selection",
           dut->rootp->milan_datapath__DOT__crf_clk_selected_r, 1);
        ck("CRF: the NCO servo gate is live",
           dut->rootp->milan_datapath__DOT__mnco_servo_en_w, 1);

        // lock the sink: 8 clean PDUs at the 2 ms cadence
        next_pdu_at = axis_cycle;
        crf_on = true;
        run_fed(2000000);
        ck("CRF: sink locked (8 clean PDUs)", axi_read(A_CRF_CTRL) >> 31, 1);

        // let the align loop engage and walk its integral in (the unit suite
        // measures ~0.35 s to settle; the proportional bound holds phase from
        // the first frames, so nothing slips while we wait)
        run_fed(45000000);
        ck("CRF: align loop engaged on the physical frame marker",
           dut->rootp->milan_datapath__DOT__mga_engaged_w, 1);

        long dup0  = dut->rootp->milan_datapath__DOT__tdm_dup_cnt_w;
        long skip0 = dut->rootp->milan_datapath__DOT__tdm_skip_cnt_w;
        obs_reset();
        live_first_seq = aaf_seq;
        run_fed(15000000);                  // ~0.15 s aligned window
        live_last_seq = aaf_seq;
        const double ppm_crf = window_ppm();
        printf("  MEASURED     : %+9.4f ppm with CRF selected (was %+9.4f)\n",
               ppm_crf, ppm_int);
        ck("CRF: the grids are ALIGNED (|ppm| < 0.5 - the #74 close)",
           std::fabs(ppm_crf) < 0.5, 1);
        ck("CRF: zero junction dups over the aligned window",
           static_cast<long>(dut->rootp->milan_datapath__DOT__tdm_dup_cnt_w) - dup0, 0);
        ck("CRF: zero junction skips over the aligned window",
           static_cast<long>(dut->rootp->milan_datapath__DOT__tdm_skip_cnt_w) - skip0, 0);
        {
            long e = static_cast<int16_t>(dut->rootp->milan_datapath__DOT__mga_err_w);
            if (e < 0) e = -e;
            ck("CRF: phase error bounded well inside a sample (<300 cycles)",
               e < 300, 1);
        }
        {
            const uint32_t sv = axi_read(A_MCSRV_STAT);
            printf("  A_MCSRV_STAT : 0x%08X\n", sv);
            //! ACQUIRE(3): the live selection carried the servo out of IDLE,
            //! through VERIFY (the harness DRP responder answers with data 0;
            //! a mismatch is informative-only with auto_repair off) and into
            //! the tracking state. The non-zero COMMAND on this slice needs the
            //! 256-PDU / 512 ms crf_rate ring plus a full servo window - tens
            //! of seconds of board time, sweep-hostile here - and is proven
            //! where the window physics is affordable: tb/verilator/mmcm_servo
            //! [U2] converges the same slice against the same -10.64 ppm plan
            //! under the same clk_src selection, and the CSR mapping of
            //! status_o to 0x8F8 is pinned by the csr suite. What the root owns
            //! is that the SELECTION reaches this servo - and it now does.
            ck("CRF: the MMCM servo tracks through the live select (ACQUIRE)",
               sv & 0x7, 3);
        }
    }

    // =================================================================== //
    //  THE LOOPBACK RING ON THE ONE GRID (#390).                            //
    //                                                                      //
    //  The LOOP bucket of KL_chan_map_capture is the last elastic queue at  //
    //  the media boundary: PUSHED by the depacketizer clone at the UPSTREAM //
    //  talker's rate, POPPED once per media tick. Nothing in this leg fed   //
    //  it before, so its dup/skip evidence read zero for want of a feed,    //
    //  not for want of a slip. The upstream talker is modelled here on the  //
    //  PHYSICAL grid - the AAF feed at 12500 + 52/391 cycles per PDU, the   //
    //  cadence a peer disciplined to the same CRF produces - so at INTERNAL //
    //  the ring sees the -10.64 ppm plan (pop faster than push: one dup per //
    //  beat period, 1.958 s), and under CRF, the packet grid held on fsync  //
    //  by KL_media_grid_align, it sees ONE grid.                             //
    //                                                                      //
    //  MAKING THE BEAT DETERMINISTIC. The dup fires when a six-event burst  //
    //  lands AFTER the tick that would have popped its first event. Bursts  //
    //  repeat every six ticks + 52/391 cycles, so the burst-vs-tick phase   //
    //  walks 0.133 cycle per PDU and the first dup comes after              //
    //  (P - phi) / 0.133 PDUs, phi = the burst's landing offset after the   //
    //  preceding tick (P = 2083.33). The harness AIMS phi: it empties the   //
    //  queue, waits for a tick and lands the restart PDU 0.93 P after one   //
    //  (the landing latency is measured on the priming PDU), which puts the //
    //  first dup ~1100 PDUs = 13.7 M cycles out; the graded window is 1.5x  //
    //  that. The same aim and window under CRF must show ZERO: a pop grid   //
    //  drifting by the INTERNAL plan would dup inside it, so the window     //
    //  exposes any ring drift above (P - phi) / window = 7 ppm.             //
    //                                                                      //
    //  The evidence is read TWICE: the tap, and the SLIP_LB / SLIP_TDM CSR  //
    //  words (0x8D4 / 0x8D8) that make it visible on silicon.               //
    // =================================================================== //
    long tick_cycle_last = -1;    //! the last media tick (never reset)
    long lb_land_cycle   = -1;    //! last accepted tlast at the loop tap
    long lb_land_tick    = -1;    //! the tick that preceded that landing

    void observe_the_loop_ring() {
        if (dut->rootp->milan_datapath__DOT__media_tick_p) tick_cycle_last = axis_cycle;
        if (dut->rootp->milan_datapath__DOT__lb_tap_tvalid_w &&
            dut->rootp->milan_datapath__DOT__lb_tap_tlast_w) {
            lb_land_cycle = axis_cycle;
            lb_land_tick  = tick_cycle_last;
        }
    }

    uint32_t slip_lb_tap() const {
        return (static_cast<uint32_t>(dut->rootp->milan_datapath__DOT__lb_skip_cnt_w) << 16) |
               static_cast<uint32_t>(dut->rootp->milan_datapath__DOT__lb_dup_cnt_w);
    }
    uint32_t slip_tdm_tap() const {
        return (static_cast<uint32_t>(dut->rootp->milan_datapath__DOT__tdm_skip_cnt_w) << 16) |
               static_cast<uint32_t>(dut->rootp->milan_datapath__DOT__tdm_dup_cnt_w);
    }

    //! listener 0 through the 0x800 window (the sim_ax1x1gptp provisioning):
    //! the sid the AAF feed carries and the eight-channel INT32 format
    void bind_listener_zero_through_the_window() {
        constexpr uint16_t A_MAC_ALO = 0x108;
        constexpr uint16_t A_MAC_AHI = 0x10C;
        constexpr uint16_t A_STRM_SEL = 0x800;
        constexpr uint16_t A_STRMW_CTRL = 0x810;
        constexpr uint16_t A_STRMW_SID_LO = 0x814;
        constexpr uint16_t A_STRMW_SID_HI = 0x818;
        constexpr uint16_t A_STRMW_FMT_LO = 0x824;
        constexpr uint16_t A_STRMW_FMT_HI = 0x828;
        axi_write(A_MAC_ALO, 0x00000002);
        axi_write(A_MAC_AHI, 0x00000100);
        axi_write(A_STRM_SEL, 0);
        axi_write(A_STRMW_SID_LO, 0x00020000);      // sid 02:00:00:00:00:02:00:00
        axi_write(A_STRMW_SID_HI, 0x02000000);
        axi_write(A_STRMW_FMT_LO, 0x02006000);
        axi_write(A_STRMW_FMT_HI, 0x02050220);
        axi_write(A_STRMW_CTRL, 1);
    }

    //! talker 0's eight channels onto the LOOP bucket of stream 0, pair ch/2
    //! half ch&1 - the shipping AX7101 loopback lane, programmed through the
    //! 0x900 window exactly as sim_ax1x1gptp does
    void map_talker_zero_onto_the_loop_lane() {
        constexpr uint16_t A_CHMAP_CTRL = 0x900;
        constexpr uint16_t A_CHMAP_SEL = 0x904;
        constexpr uint16_t A_CHMAP_WORD = 0x908;
        axi_write(A_CHMAP_CTRL, 1);
        for (unsigned ch = 0; ch < static_cast<unsigned>(kAafChans); ch++) {
            axi_write(A_CHMAP_SEL, 0x100u | ch);
            axi_write(A_CHMAP_WORD, 0xD000u | ((ch & 1u) << 8) | (ch / 2));
        }
    }

    //! feed until the next AAF PDU lands at the loop tap; false = the budget
    //! ran out first
    bool run_fed_until_a_pdu_lands(long budget) {
        const long seen = lb_land_cycle;
        const long stop = axis_cycle + budget;
        while (axis_cycle < stop && lb_land_cycle == seen) {
            if (crf_on && axis_cycle >= next_pdu_at) { send_crf(); next_pdu_at += kCrfPduPeriodCycles; }
            else if (aaf_on && axis_cycle >= aaf_next_at) { send_aaf(); advance_aaf_slot(); }
            else step();
        }
        return lb_land_cycle != seen;
    }

    //! feed for `cycles`; returns the cycle at which the ring's dup count
    //! first left `dup0`, or -1
    long run_fed_watching_the_ring(long cycles, uint16_t dup0) {
        long first = -1;
        const long stop = axis_cycle + cycles;
        while (axis_cycle < stop) {
            if (crf_on && axis_cycle >= next_pdu_at) { send_crf(); next_pdu_at += kCrfPduPeriodCycles; }
            else if (aaf_on && axis_cycle >= aaf_next_at) { send_aaf(); advance_aaf_slot(); }
            else step();
            if (first < 0 && dut->rootp->milan_datapath__DOT__lb_dup_cnt_w != dup0) first = axis_cycle;
        }
        return first;
    }

    //! With the feed off and the queue empty: wait for a media tick, then land
    //! the restart PDU kRingAimCycles after a tick two ticks on (the latency
    //! fits inside), and keep the physical cadence from there. Every burst
    //! then leaves six events in the queue and the aimed phase alone decides
    //! when a slow drift produces the first dup. Returns the landing offset
    //! after the tick that preceded it, in cycles.
    long restart_the_feed_at_the_aimed_phase(long landing_latency) {
        const long seen = tick_cycle_last;
        while (tick_cycle_last == seen) {
            if (crf_on && axis_cycle >= next_pdu_at) { send_crf(); next_pdu_at += kCrfPduPeriodCycles; }
            else step();
        }
        aaf_next_at = tick_cycle_last + static_cast<long>(2 * kTickCycles)
                    + kRingAimCycles - landing_latency;
        aaf_on = true;
        if (!run_fed_until_a_pdu_lands(4 * kAafPduPeriodCycles)) return -1;
        return lb_land_cycle - lb_land_tick;
    }

    long ring_landing_latency = 0;      //! inject slot -> loop-tap tlast
    long ring_window_cycles = 0;        //! the window BOTH ring phases grade

    // =================================================================== //
    //  [RING-INT] the ring slips at INTERNAL, on the beat the plan predicts //
    // =================================================================== //
    void prove_the_loop_ring_slips_at_internal() {
        printf("\n[RING-INT] the loopback ring at INTERNAL: pushed on the physical grid, popped on the packet grid\n");
        bind_listener_zero_through_the_window();
        map_talker_zero_onto_the_loop_lane();
        //! the render-law phases leave a LIVE feed running into here, and
        //! start_aaf_feed() keeps a running feed's cadence: the first
        //! landing seen would then be a PDU already in flight and the
        //! latency would be a whole period out. Drain first, so the feed
        //! restarts from this phase's own slot.
        if (aaf_on) { aaf_on = false; run_fed(2 * kAafPduPeriodCycles); }
        // prime the ring with one PDU at whatever phase; its landing is the
        // latency the aim below needs
        start_aaf_feed(kAafPhysFracNum);
        const long sent_at = aaf_next_at;
        ck("RING-INT: the priming PDU reached the loop tap",
           run_fed_until_a_pdu_lands(kAafPduPeriodCycles) ? 1 : 0, 1);
        ring_landing_latency = lb_land_cycle - sent_at;
        printf("  loop-tap landing latency: %ld cycles after the inject slot\n",
               ring_landing_latency);
        // feed off: the queue drains in six ticks and the primed pair then
        // counts every empty tick, honestly - that starved run is not graded
        aaf_on = false;
        run_fed(2 * kAafPduPeriodCycles);
        const long phase = restart_the_feed_at_the_aimed_phase(ring_landing_latency);
        printf("  restart PDU landed %ld cycles after a tick (aim %ld, band %ld..%ld)\n",
               phase, kRingAimCycles, kRingAimBandLo, kRingAimBandHi);
        ck("RING-INT: the restart PDU landed inside the aimed band",
           (phase >= kRingAimBandLo && phase <= kRingAimBandHi) ? 1 : 0, 1);
        // the prediction: the physical cadence walks each burst 52/391 cycle
        // later against the packet grid; the first dup is the burst crossing
        // the next tick
        const double walk_per_pdu = static_cast<double>(kAafPhysFracNum)
                                  / static_cast<double>(kAafPhysFracDen);
        const double pdus_to_dup = (kTickCycles - static_cast<double>(phase)) / walk_per_pdu;
        const long predicted = static_cast<long>(pdus_to_dup * kAafPduPeriodCycles);
        ring_window_cycles = predicted + predicted / 2;
        printf("  predicted first dup: %.0f PDUs = %ld cycles (%.3f s); window %ld cycles\n",
               pdus_to_dup, predicted, static_cast<double>(predicted) / 100e6, ring_window_cycles);
        run_fed(64);                          // the burst is queued
        const uint16_t dup0  = dut->rootp->milan_datapath__DOT__lb_dup_cnt_w;
        const uint16_t skip0 = dut->rootp->milan_datapath__DOT__lb_skip_cnt_w;
        const long t0 = axis_cycle;
        const long first = run_fed_watching_the_ring(ring_window_cycles, dup0);
        const long dups  = static_cast<long>(dut->rootp->milan_datapath__DOT__lb_dup_cnt_w) - dup0;
        const long skips = static_cast<long>(dut->rootp->milan_datapath__DOT__lb_skip_cnt_w) - skip0;
        const long at = first < 0 ? -1 : first - t0;
        printf("  ring over the window: %ld dup, %ld skip; first dup at +%ld cycles (%+.1f%% of the prediction)\n",
               dups, skips, at,
               at < 0 ? 0.0 : 100.0 * static_cast<double>(at - predicted) / static_cast<double>(predicted));
        //! one beat = one starved tick, and the ring counts it ONCE PER FED
        //! PAIR (KL_chan_map_capture: "dups are one per starved fed pair per
        //! tick"): four pairs of the eight-channel lane repeat one event each
        ck("RING-INT: one beat period = one repeated event on each of the four fed pairs",
           dups, kAafChans / 2);
        ck("RING-INT: no skip - the push side is the slower grid", skips, 0);
        const long err = at - predicted;
        ck("RING-INT: the first dup landed within 25% of the -10.64 ppm prediction",
           (at >= 0 && (err < 0 ? -err : err) * 4 <= predicted) ? 1 : 0, 1);
        ck("RING-INT: SLIP_LB 0x8D4 carries the ring's {skip, dup}",
           axi_read(0x8D4), slip_lb_tap());
    }

    // =================================================================== //
    //  [SLIP-CSR] the two words read their taps, after induced slips       //
    // =================================================================== //
    void prove_the_slip_words_follow_their_taps() {
        printf("\n[SLIP-CSR] SLIP_LB 0x8D4 / SLIP_TDM 0x8D8 carry the junction counters\n");
        constexpr uint16_t A_SLIP_LB = 0x8D4;
        constexpr uint16_t A_SLIP_TDM = 0x8D8;
        // the TDM junction: hold the audio clock for one frame (one marker
        // missing at one tick = one dup), then double it for two frames
        // (markers over unread markers = skips). Harness clock stimuli, at
        // INTERNAL, before any loop is engaged on this clock.
        const uint16_t tdup0  = dut->rootp->milan_datapath__DOT__tdm_dup_cnt_w;
        const uint16_t tskip0 = dut->rootp->milan_datapath__DOT__tdm_skip_cnt_w;
        aud_hold_steps = kFrameHalfSteps;
        run_fed(4 * static_cast<long>(kTickCycles));
        const long tdups = static_cast<long>(dut->rootp->milan_datapath__DOT__tdm_dup_cnt_w) - tdup0;
        ck("SLIP-CSR: one held frame = one TDM junction dup", tdups, 1);
        aud_boost_steps = 2 * kFrameHalfSteps;
        run_fed(4 * static_cast<long>(kTickCycles));
        const long tskips = static_cast<long>(dut->rootp->milan_datapath__DOT__tdm_skip_cnt_w) - tskip0;
        printf("  TDM junction: +%ld dup after the held frame, +%ld skip after the doubled frames\n",
               tdups, tskips);
        ck("SLIP-CSR: doubled frames = TDM junction skips", tskips >= 1 ? 1 : 0, 1);
        uint32_t tap  = slip_tdm_tap();
        uint32_t word = axi_read(A_SLIP_TDM);
        printf("  SLIP_TDM 0x%08X (tap 0x%08X)\n", word, tap);
        ck("SLIP-CSR: SLIP_TDM carries the junction's {skip, dup}", word, tap);
        tap  = slip_lb_tap();
        word = axi_read(A_SLIP_LB);
        printf("  SLIP_LB  0x%08X (tap 0x%08X)\n", word, tap);
        ck("SLIP-CSR: SLIP_LB carries the ring's {skip, dup}", word, tap);
        ck("SLIP-CSR: both words are non-zero after the induced slips",
           ((word & 0xFFFF) != 0 && (slip_tdm_tap() & 0xFFFF) != 0) ? 1 : 0, 1);
        // read-only: a write lands nowhere
        axi_write(A_SLIP_LB, 0xFFFFFFFFu);
        axi_write(A_SLIP_TDM, 0xFFFFFFFFu);
        ck("SLIP-CSR: SLIP_LB ignores writes",  axi_read(A_SLIP_LB),  slip_lb_tap());
        ck("SLIP-CSR: SLIP_TDM ignores writes", axi_read(A_SLIP_TDM), slip_tdm_tap());
    }

    // =================================================================== //
    //  [RING-CRF] the same instrument with the grids aligned: ONE grid     //
    // =================================================================== //
    void prove_the_loop_ring_rides_one_grid_under_crf() {
        printf("\n[RING-CRF] under CRF the ring's push (the physical grid) and pop (the aligned packet grid) are one grid\n");
        constexpr uint16_t A_SLIP_LB = 0x8D4;
        constexpr uint16_t A_SLIP_TDM = 0x8D8;
        ck("RING-CRF: the align loop is engaged",
           dut->rootp->milan_datapath__DOT__mga_engaged_w, 1);
        // the same aim and the same window as [RING-INT]: a pop grid that
        // drifted by the INTERNAL plan would dup inside it
        aaf_on = false;
        run_fed(2 * kAafPduPeriodCycles);
        const long phase = restart_the_feed_at_the_aimed_phase(ring_landing_latency);
        printf("  restart PDU landed %ld cycles after a tick (aim %ld, band %ld..%ld)\n",
               phase, kRingAimCycles, kRingAimBandLo, kRingAimBandHi);
        ck("RING-CRF: the restart PDU landed inside the aimed band",
           (phase >= kRingAimBandLo && phase <= kRingAimBandHi) ? 1 : 0, 1);
        run_fed(64);
        const uint16_t dup0   = dut->rootp->milan_datapath__DOT__lb_dup_cnt_w;
        const uint16_t skip0  = dut->rootp->milan_datapath__DOT__lb_skip_cnt_w;
        const uint16_t tdup0  = dut->rootp->milan_datapath__DOT__tdm_dup_cnt_w;
        const uint16_t tskip0 = dut->rootp->milan_datapath__DOT__tdm_skip_cnt_w;
        const long t0 = axis_cycle;
        const long first = run_fed_watching_the_ring(ring_window_cycles, dup0);
        const long dups   = static_cast<long>(dut->rootp->milan_datapath__DOT__lb_dup_cnt_w) - dup0;
        const long skips  = static_cast<long>(dut->rootp->milan_datapath__DOT__lb_skip_cnt_w) - skip0;
        const long tdups  = static_cast<long>(dut->rootp->milan_datapath__DOT__tdm_dup_cnt_w) - tdup0;
        const long tskips = static_cast<long>(dut->rootp->milan_datapath__DOT__tdm_skip_cnt_w) - tskip0;
        printf("  ring over the same %ld-cycle window: %ld dup, %ld skip (first dup at %ld); TDM junction %ld dup, %ld skip\n",
               ring_window_cycles, dups, skips, first < 0 ? -1L : first - t0, tdups, tskips);
        {
            long e = static_cast<int16_t>(dut->rootp->milan_datapath__DOT__mga_err_w);
            if (e < 0) e = -e;
            printf("  align-loop phase error at the window's end: %ld cycles\n", e);
        }
        ck("RING-CRF: zero ring dups over the window that exposed -10.64 ppm at INTERNAL", dups, 0);
        ck("RING-CRF: zero ring skips", skips, 0);
        ck("RING-CRF: zero TDM junction slips over the same window", tdups + tskips, 0);
        ck("RING-CRF: the align loop stayed engaged",
           dut->rootp->milan_datapath__DOT__mga_engaged_w, 1);
        ck("RING-CRF: SLIP_LB still reads its tap under lock",  axi_read(A_SLIP_LB),  slip_lb_tap());
        ck("RING-CRF: SLIP_TDM still reads its tap under lock", axi_read(A_SLIP_TDM), slip_tdm_tap());
    }

    // ---- 4.4.4.3 mr reachability: the received toggle echoes while CRF  //
    //      is the followed source, and stops when it is not (10.4.3) ----
    void prove_the_mr_toggle_echoes_only_under_crf() {
        printf("\n[MR] the received mr toggle reaches our streams - only under CRF\n");
        std::vector<std::array<uint8_t,64>> cap;
        auto lvl_of = [&](const std::array<uint8_t,64>& f) {
            return static_cast<long>((f[15] >> 3) & 1);
        };
        ck("MR baseline: our CRF output is emitting", cap_crf(2, cap, 3000000), 2);
        const long lvl0 = cap.empty() ? -1 : lvl_of(cap.back());
        crf_mr = 1;                          // toggle the RECEIVED level
        run_fed(1200000);                    // a few PDUs at the new level
        ck("MR: our outgoing mr FLIPPED on the received toggle (CRF selected)",
           cap_crf(2, cap, 3000000) == 2 ? lvl_of(cap.back()) : -1, lvl0 ^ 1);

        const long lvl1 = cap.empty() ? -1 : lvl_of(cap.back());
        //! the live stream's records around the deselect ([RENDER-LIVE-INT])
        const uint32_t rc0 = dut->rootp->milan_datapath__DOT__rsp_recentres_w;
        const long pulses0 = recentre_pulses;
        const long src0 = src_recentre_pulses;
        const uint32_t rails0 = dut->rootp->milan_datapath__DOT__rsp_rails_w;
        poke_clksrc(0);                      // back to INTERNAL
        ck("MR: deselect resolves back",
           dut->rootp->milan_datapath__DOT__crf_clk_selected_r, 0);
        //! the deselect IS a media-clock SOURCE CHANGE - 4.4.4.3's other
        //! mandatory trigger, detected inside KL_media_clock_restart from the
        //! live clk_src_i this round wired. It must toggle mr once more.
        run_fed(1200000);
        ck("MR: the source change itself toggles mr (4.4.4.3)",
           cap_crf(2, cap, 3000000) == 2 ? lvl_of(cap.back()) : -1, lvl1 ^ 1);
        const long lvl2 = cap.empty() ? -1 : lvl_of(cap.back());
        crf_mr = 0;                          // received toggle - must NOT echo now
        run_fed(1200000);
        ck("MR: the received toggle does NOT echo at INTERNAL (10.4.3)",
           cap_crf(2, cap, 3000000) == 2 ? lvl_of(cap.back()) : -1, lvl2);
        ck("MR: align loop disengaged again at INTERNAL",
           dut->rootp->milan_datapath__DOT__mga_engaged_w, 0);
        if (!aaf_on) return;
        //! [RENDER-LIVE-INT] the deselect under the running stream: the
        //! source change arms the settled-grid recentre, which at INTERNAL
        //! fires after its tick dwell (2048 ticks, 43 ms) and restores the
        //! law the [RENDER-LIVE] displacement broke the other way
        printf("\n[RENDER-LIVE-INT] the deselect under the running stream: one recentre after the dwell\n");
        run_fed(6000000);
        ck("RENDER-LIVE-INT: the source change fired the settled-grid trigger once",
           src_recentre_pulses - src0, 1);
        ck("RENDER-LIVE-INT: ...as one recentre pulse", recentre_pulses - pulses0, 1);
        ck("RENDER-LIVE-INT: the recentre executed once",
           dut->rootp->milan_datapath__DOT__rsp_recentres_w - rc0, 1);
        const int first = static_cast<int>(aaf_seq);
        run_fed(100 * kAafPduPeriodCycles);
        const LawStats st = law_over(first, static_cast<int>(aaf_seq) - kLawSkipTail, kRenderSetpointEvt);
        report_law("RENDER-LIVE-INT", st, 90, static_cast<long>(kTickCycles) + kBandSlackCycles);
        ck("RENDER-LIVE-INT: no rail", dut->rootp->milan_datapath__DOT__rsp_rails_w - rails0, 0);
        ck("RENDER-LIVE-INT: counted once, never again",
           dut->rootp->milan_datapath__DOT__rsp_recentres_w - rc0, 1);
    }

    // =================================================================== //
    //  [RENDER-BIND] listener 0 over ACMP, the sim_main ladder             //
    // =================================================================== //
    void bind_listener_zero_over_acmp() {
        printf("\n[RENDER-BIND] listener 0 bound over ACMP for the render-law phases\n");
        constexpr uint16_t A_ADP_CTRL = 0x600;
        constexpr uint16_t A_ADP_EIDLO = 0x604;
        constexpr uint16_t A_ADP_EIDHI = 0x608;
        constexpr uint16_t A_MAC_ALO = 0x108;
        constexpr uint16_t A_MAC_AHI = 0x10C;
        constexpr uint16_t A_ACMPL_STATE = 0x6A4;
        // the identity group, exactly as sim_main provisions it
        axi_write(A_MAC_ALO, 0x00000002);
        axi_write(A_MAC_AHI, 0x00000100);
        axi_write(A_ADP_EIDHI, 0x020000FF);
        axi_write(A_ADP_EIDLO, 0xFE000001);
        axi_write(A_ADP_CTRL, 0x00001F01);
        for (int c = 0; c < 2000; c++) step();
        {   // BIND_RX (CONNECT_RX_COMMAND, msg 6): listener = us, talker = :02
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {
                0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {
                0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x06;
            f[16]=0x00; f[17]=44;
            for (int i = 26; i < 34; i++) f[i] = static_cast<uint8_t>(i);
            const uint8_t tk[8] = {
                0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x02};
            memcpy(f+34, tk, 8);
            const uint8_t ls[8] = {
                0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, ls, 8);
            f[62]=0x11; f[63]=0x22;
            inject(f, 70);
        }
        for (int c = 0; c < 3000 && !probe_seen; c++) step();
        ck("RENDER-BIND: the listener launched a PROBE_TX at the named talker",
           probe_seen ? 1 : 0, 1);
        {   // play the talker: CONNECT_TX_RESPONSE naming the sid and dest MAC
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {
                0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t tsrc[6] = {
                0x02,0x00,0x00,0x00,0x00,0x02};
            memcpy(f+6, tsrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x01;
            f[16]=0x00; f[17]=44;
            const uint8_t sid[8] = {
                0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x00};
            memcpy(f+18, sid, 8);
            for (int i = 26; i < 34; i++) f[i] = static_cast<uint8_t>(i);
            const uint8_t tk[8] = {
                0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x02};
            memcpy(f+34, tk, 8);
            const uint8_t ls[8] = {
                0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, ls, 8);
            f[50]=0x00; f[51]=0x00;
            f[52]=0x00; f[53]=0x00;
            const uint8_t dm[6] = {
                0x91,0xE0,0xF0,0x00,0x2A,0x02};
            memcpy(f+54, dm, 6);
            f[62]=static_cast<uint8_t>(probe_seq >> 8);
            f[63]=static_cast<uint8_t>(probe_seq & 0xFF);
            inject(f, 70);
        }
        for (int c = 0; c < 2000; c++) step();
        ck("RENDER-BIND: listener bound (0x6A4[3], the class-D record)",
           (axi_read(A_ACMPL_STATE) >> 3) & 1, 1);
    }

    // =================================================================== //
    //  The render law over one window of PDUs                             //
    // =================================================================== //
    struct LawStats {
        long n = 0;
        long in_band = 0;
        long fill_ok = 0;
        long fill_is = 0;      //! PDUs whose fill at accept equals `fill_expect`
        long dmin = 0;
        long dmax = 0;
        double dmean = 0.0;
    };

    //! the law over PDU ids [first, last): delay = pop of event 0 - accept
    LawStats law_over(int first, int last, int fill_expect) const {
        LawStats st;
        const double lo = kRenderSetpointEvt * kTickCycles;
        const double hi = (kRenderSetpointEvt + 1) * kTickCycles + kBandSlackCycles;
        double sum = 0.0;
        for (int pdu = first; pdu < last; pdu++) {
            if (pdu >= static_cast<int>(accept_cycle.size())) break;
            if (accept_cycle[pdu] < 0 || render_cycle[pdu] < 0) continue;
            const long d = render_cycle[pdu] - accept_cycle[pdu];
            if (st.n == 0 || d < st.dmin) st.dmin = d;
            if (st.n == 0 || d > st.dmax) st.dmax = d;
            if (static_cast<double>(d) > lo && static_cast<double>(d) <= hi) st.in_band++;
            if (fill_at_accept[pdu] == kRenderSetpointEvt) st.fill_ok++;
            if (fill_at_accept[pdu] == fill_expect) st.fill_is++;
            sum += static_cast<double>(d);
            st.n++;
        }
        st.dmean = st.n ? sum / static_cast<double>(st.n) : 0.0;
        return st;
    }

    //! the accept phase against the grid, in ticks, from a window's mean
    //! first-event delay: what d / T carries above the setpoint
    static double accept_phase_ticks(const LawStats& st) {
        return st.dmean / kTickCycles - static_cast<double>(kRenderSetpointEvt);
    }

    void report_law(const char* tag, const LawStats& st, long expect_n, long max_spread) {
        printf("  %s: %ld PDUs, first-event delay min %ld max %ld mean %.1f cycles = %.3f..%.3f media ticks\n",
               tag, st.n, st.dmin, st.dmax, st.dmean,
               static_cast<double>(st.dmin) / kTickCycles, static_cast<double>(st.dmax) / kTickCycles);
        printf("  %s: the law: %d < d/T <= %d (+%ld cycles of registration slack); setpoint %d events = %.2f us\n",
               tag, kRenderSetpointEvt, kRenderSetpointEvt + 1, kBandSlackCycles,
               kRenderSetpointEvt, kRenderSetpointEvt * 1e6 / 48000.0);
        char w[128];
        snprintf(w, sizeof w, "%s: PDUs measured in the window", tag);
        ck(w, st.n >= expect_n, 1);
        snprintf(w, sizeof w, "%s: every PDU's first event inside the law band", tag);
        ck(w, st.in_band, st.n);
        snprintf(w, sizeof w, "%s: the fill at accept is the setpoint for every PDU", tag);
        ck(w, st.fill_ok, st.n);
        snprintf(w, sizeof w, "%s: one constant: spread within %ld cycles", tag, max_spread);
        ck(w, (st.dmax - st.dmin) <= max_spread, 1);
    }

    // =================================================================== //
    //  [RENDER-INT] the law at INTERNAL: the cadence IS the packet grid    //
    // =================================================================== //
    void measure_the_render_law_at_internal() {
        printf("\n[RENDER-INT] the render law at INTERNAL (cadence = the packet grid)\n");
        const uint32_t rails0 = dut->rootp->milan_datapath__DOT__rsp_rails_w;
        const uint32_t under0 = dut->rootp->milan_datapath__DOT__rsp_underruns_w;
        start_aaf_feed(0);
        //! ~0.12 s: 960 PDUs, and past the observer's 100-period dwell (100 ms
        //! of the 100 MHz axis clock) once the prefill's three PDUs are out
        const long RUN = 12000000;
        run_fed(RUN);
        const long n = aaf_seq;              //! the next sequence = PDUs injected
        ck("RENDER-INT: every injected PDU was accepted",
           static_cast<unsigned long>(accepts_seen), static_cast<unsigned long>(n));
        const LawStats st = law_over(kLawSkipHead, static_cast<int>(n) - kLawSkipTail, kRenderSetpointEvt);
        report_law("RENDER-INT", st, 850, kBandSlackCycles);
        ck("RENDER-INT: no rail inside the window",
           dut->rootp->milan_datapath__DOT__rsp_rails_w - rails0, 0);
        ck("RENDER-INT: no underrun inside the window",
           dut->rootp->milan_datapath__DOT__rsp_underruns_w - under0, 0);
        ck("RENDER-INT: converged", dut->rootp->milan_datapath__DOT__rsp_converged_w & 1, 1);
    }

    // =================================================================== //
    //  [RENDER-CRF] the law under CRF: cadence = the PHYSICAL grid         //
    // =================================================================== //
    void measure_the_render_law_under_crf() {
        printf("\n[RENDER-CRF] the render law under CRF (cadence = the physical grid, 12500 + 52/391)\n");
        //! the same stream, still running since the bind; only the records
        //! restart here
        start_aaf_feed(kAafPhysFracNum);
        run_fed(2000000);                   // the observer's dwell
        const uint32_t rails0 = dut->rootp->milan_datapath__DOT__rsp_rails_w;
        const uint32_t under0 = dut->rootp->milan_datapath__DOT__rsp_underruns_w;
        const int first = static_cast<int>(aaf_seq);   //! the first sequence of the window
        run_fed(15000000);                  // ~0.15 s: 1200 PDUs
        const int n = static_cast<int>(aaf_seq);
        ck("RENDER-CRF: every injected PDU was accepted",
           static_cast<unsigned long>(accepts_seen), static_cast<unsigned long>(n));
        const LawStats st = law_over(first, n - kLawSkipTail, kRenderSetpointEvt);
        //! the sub-tick phase may wander with the aligner's residual; the
        //! integer fill and the band are the constant, so the spread bound
        //! here is the band width itself
        report_law("RENDER-CRF", st, 1100, static_cast<long>(kTickCycles) + kBandSlackCycles);
        ck("RENDER-CRF: no rail inside the window",
           dut->rootp->milan_datapath__DOT__rsp_rails_w - rails0, 0);
        ck("RENDER-CRF: no underrun inside the window",
           dut->rootp->milan_datapath__DOT__rsp_underruns_w - under0, 0);
        ck("RENDER-CRF: the aligner stayed engaged",
           dut->rootp->milan_datapath__DOT__mga_engaged_w, 1);
        ck("RENDER-CRF: converged", dut->rootp->milan_datapath__DOT__rsp_converged_w & 1, 1);
    }

    // =================================================================== //
    //  [RENDER-RC] a displaced fill, then ONE recentre on a PHC step       //
    // =================================================================== //
    //! one PHC adjtime through CLKV software (the plane-off step)
    void step_the_phc() {
        constexpr uint16_t A_PTP_OFLO = 0x518;
        constexpr uint16_t A_PTP_OFHI = 0x51C;
        constexpr uint16_t A_PTP_CMD = 0x520;
        axi_write(A_PTP_OFLO, kPhcStepNs);
        axi_write(A_PTP_OFHI, 0);
        axi_write(A_PTP_CMD, 0x2);
    }

    //! one displacement of `ticks` (late = positive: the fill falls short and
    //! the recentre re-enters prefill; early = negative: the fill runs long
    //! and the recentre SNAPS), then one PHC step, then the law again
    void displace_then_step(const char* tag, int ticks, uint32_t rc0, long pulses0,
                            uint32_t rails0, int recentres_so_far) {
        char w[128];
        const char* side = ticks > 0 ? "late" : "early";
        // the displacement: every PDU from here on arrives `ticks` ticks later
        shift_the_running_feed(static_cast<double>(ticks));
        int first = static_cast<int>(aaf_seq);          //! windows are named by sequence
        run_fed(25 * kAafPduPeriodCycles);
        int n = static_cast<int>(aaf_seq);
        LawStats st = law_over(first + 8, n - kLawSkipTail, kRenderSetpointEvt - ticks);
        printf("  %s: displaced %d ticks %s: %ld PDUs, delay min %ld max %ld cycles = %.3f..%.3f ticks\n",
               tag, ticks > 0 ? ticks : -ticks, side, st.n, st.dmin, st.dmax,
               static_cast<double>(st.dmin) / kTickCycles, static_cast<double>(st.dmax) / kTickCycles);
        snprintf(w, sizeof w, "%s: the instrument sees the %s displacement (fill at accept = setpoint %+d)",
                 tag, side, -ticks);
        ck(w, st.fill_is, st.n);
        snprintf(w, sizeof w, "%s: ...and the delay left the law band (%s)", tag, side);
        ck(w, st.in_band, 0);
        snprintf(w, sizeof w, "%s: a three-tick displacement trips no rail (%s)", tag, side);
        ck(w, dut->rootp->milan_datapath__DOT__rsp_rails_w - rails0, 0);
        step_the_phc();
        first = static_cast<int>(aaf_seq);
        run_fed(25 * kAafPduPeriodCycles);
        n = static_cast<int>(aaf_seq);
        snprintf(w, sizeof w, "%s: the step reached the render stage as one pulse (%s)", tag, side);
        ck(w, recentre_pulses - pulses0, recentres_so_far + 1);
        snprintf(w, sizeof w, "%s: the recentre executed once (%s)", tag, side);
        ck(w, dut->rootp->milan_datapath__DOT__rsp_recentres_w - rc0, recentres_so_far + 1);
        st = law_over(first + 8, n - kLawSkipTail, kRenderSetpointEvt);
        snprintf(w, sizeof w, "%s: the recentre restored the law (fill at accept = setpoint) (%s)", tag, side);
        ck(w, st.fill_ok, st.n);
        snprintf(w, sizeof w, "%s: ...and the delay is back inside the band (%s)", tag, side);
        ck(w, st.in_band, st.n);
        // a hundred more PDUs: nothing drifts back, nothing recentres again
        first = static_cast<int>(aaf_seq);
        run_fed(100 * kAafPduPeriodCycles);
        n = static_cast<int>(aaf_seq);
        st = law_over(first, n - kLawSkipTail, kRenderSetpointEvt);
        snprintf(w, sizeof w, "%s: counted once, never again (%s)", tag, side);
        ck(w, dut->rootp->milan_datapath__DOT__rsp_recentres_w - rc0, recentres_so_far + 1);
        snprintf(w, sizeof w, "%s: no drift back: every later PDU at the setpoint (%s)", tag, side);
        ck(w, st.fill_ok, st.n);
        snprintf(w, sizeof w, "%s: no drift back: every later PDU inside the band (%s)", tag, side);
        ck(w, st.in_band, st.n);
        snprintf(w, sizeof w, "%s: the recentre is not a rail (%s)", tag, side);
        ck(w, dut->rootp->milan_datapath__DOT__rsp_rails_w - rails0, 0);
    }

    void prove_the_recentre_is_one_shot(const char* tag) {
        printf("\n[%s] shift the cadence three ticks late, then early; a PHC adjtime recentres ONCE each\n", tag);
        const uint32_t rails0 = dut->rootp->milan_datapath__DOT__rsp_rails_w;
        const uint32_t rc0 = dut->rootp->milan_datapath__DOT__rsp_recentres_w;
        const long pulses0 = recentre_pulses;
        //! late: the queue at the PDU end is short, the recentre re-enters
        //! prefill and the release snaps; early: the queue is long, the
        //! recentre itself snaps (the branch a late shift never reaches)
        displace_then_step(tag, +3, rc0, pulses0, rails0, 0);
        displace_then_step(tag, -3, rc0, pulses0, rails0, 1);
    }

    // =================================================================== //
    //  [RENDER-LIVE] the running feed is moved past a tick: the grid-moved  //
    //  equivalent the review probed. `later` = the grid later (fill one     //
    //  long, delay above the band); otherwise the grid earlier (fill one    //
    //  short, delay below the band). No rail, converged, nothing recentres. //
    // =================================================================== //
    void move_the_running_feed_past_a_tick(const char* tag, bool later) {
        printf("\n[%s] the running feed moved past a tick (the grid moved %s): one event off, no recovery\n",
               tag, later ? "later" : "earlier");
        char w[128];
        const uint32_t rails0 = dut->rootp->milan_datapath__DOT__rsp_rails_w;
        const uint32_t rc0 = dut->rootp->milan_datapath__DOT__rsp_recentres_w;
        const uint32_t conv0 = dut->rootp->milan_datapath__DOT__rsp_converged_w & 1;
        // the phase the stream sits at now, from a short settled window
        int first = static_cast<int>(aaf_seq);
        run_fed(25 * kAafPduPeriodCycles);
        LawStats st = law_over(first + 4, static_cast<int>(aaf_seq) - kLawSkipTail, kRenderSetpointEvt);
        const double phase = accept_phase_ticks(st);
        //! a grid moved later by d is the feed moved earlier by d: the delay
        //! grows by d, and it leaves the band exactly when a tick crosses the
        //! accept instant. Aim 0.3 tick past the boundary either way.
        const double shift = later ? -(1.3 - phase) : (phase + 0.3);
        printf("  %s: accept phase %.3f tick; the feed moves %.3f ticks %s\n",
               tag, phase, shift < 0 ? -shift : shift, shift < 0 ? "earlier" : "later");
        snprintf(w, sizeof w, "%s: the stream sat at the setpoint before the move", tag);
        ck(w, st.fill_ok, st.n);
        shift_the_running_feed(shift);
        first = static_cast<int>(aaf_seq);
        run_fed(25 * kAafPduPeriodCycles);
        const int expect = later ? kRenderSetpointEvt + 1 : kRenderSetpointEvt - 1;
        st = law_over(first + 8, static_cast<int>(aaf_seq) - kLawSkipTail, expect);
        printf("  %s: moved: %ld PDUs, delay min %ld max %ld cycles = %.3f..%.3f ticks\n",
               tag, st.n, st.dmin, st.dmax,
               static_cast<double>(st.dmin) / kTickCycles, static_cast<double>(st.dmax) / kTickCycles);
        snprintf(w, sizeof w, "%s: the fill at accept is one event %s for every PDU", tag,
                 later ? "long" : "short");
        ck(w, st.fill_is, st.n);
        snprintf(w, sizeof w, "%s: ...and the delay left the law band", tag);
        ck(w, st.in_band, 0);
        snprintf(w, sizeof w, "%s: one event off trips no rail", tag);
        ck(w, dut->rootp->milan_datapath__DOT__rsp_rails_w - rails0, 0);
        snprintf(w, sizeof w, "%s: nothing recentred it", tag);
        ck(w, dut->rootp->milan_datapath__DOT__rsp_recentres_w - rc0, 0);
        //! one event off is inside the convergence band: the observer keeps
        //! whatever it reported (a recentre just before this phase may have
        //! restarted its dwell; the move itself clears nothing)
        snprintf(w, sizeof w, "%s: the move left the convergence verdict as it was", tag);
        ck(w, dut->rootp->milan_datapath__DOT__rsp_converged_w & 1, conv0);
    }

    // =================================================================== //
    //  [RENDER-LIVE-CRF] judged after the CRF phase: the selection under    //
    //  the running stream fired ONE settled-grid recentre during the        //
    //  pull-in, and every PDU of the aligned window is at the setpoint.     //
    // =================================================================== //
    void prove_the_live_selection_recentred_once(long expect_n) {
        printf("\n[RENDER-LIVE-CRF] the CRF selection under the running stream: one recentre once the grid settled\n");
        ck("RENDER-LIVE-CRF: the selection fired the settled-grid trigger once",
           src_recentre_pulses - live_src0, 1);
        ck("RENDER-LIVE-CRF: ...as one recentre pulse", recentre_pulses - live_pulses0, 1);
        ck("RENDER-LIVE-CRF: the recentre executed once",
           dut->rootp->milan_datapath__DOT__rsp_recentres_w - live_rc0, 1);
        const LawStats st = law_over(static_cast<int>(live_first_seq),
                                     static_cast<int>(live_last_seq) - kLawSkipTail, kRenderSetpointEvt);
        report_law("RENDER-LIVE-CRF", st, expect_n, static_cast<long>(kTickCycles) + kBandSlackCycles);
        ck("RENDER-LIVE-CRF: converged", dut->rootp->milan_datapath__DOT__rsp_converged_w & 1, 1);
    }

    // =================================================================== //
    //  --live-only: the mutation arm's short leg for the datapath trigger.  //
    //  Bind, lock, move the feed past a tick, select CRF under the stream,  //
    //  wait out the settle, judge one window.                               //
    // =================================================================== //
    int run_live_only() {
        bring_out_of_reset();
        bind_listener_zero_over_acmp();
        printf("\n[RENDER-INT] a short lock (the --live-only leg)\n");
        start_aaf_feed(0);
        run_fed(3000000);
        move_the_running_feed_past_a_tick("RENDER-LIVE", true);
        printf("\n[CRF] the stored selection goes to this shape's CRF index (2), the feed running\n");
        constexpr uint16_t A_MAC_ALO = 0x108;
        constexpr uint16_t A_MAC_AHI = 0x10C;
        constexpr uint16_t A_CRF_CTRL = 0x738;
        constexpr uint16_t A_CRF_SIDLO = 0x73C;
        constexpr uint16_t A_CRF_SIDHI = 0x740;
        dut->i_mmcm_locked = 1;
        axi_write(A_MAC_ALO, 0x00000002);
        axi_write(A_MAC_AHI, 0x00000100);
        axi_write(A_CRF_SIDLO, 0x00020001);
        axi_write(A_CRF_SIDHI, 0x02000000);
        axi_write(A_CRF_CTRL,  0x1);
        live_rc0     = dut->rootp->milan_datapath__DOT__rsp_recentres_w;
        live_pulses0 = recentre_pulses;
        live_src0    = src_recentre_pulses;
        poke_clksrc(2);
        aaf_frac_num = kAafPhysFracNum;
        next_pdu_at = axis_cycle;
        crf_on = true;
        run_fed(2000000);
        ck("CRF: sink locked (8 clean PDUs)", axi_read(A_CRF_CTRL) >> 31, 1);
        //! the aligner engages within a frame and its error rests inside the
        //! trigger's band once the proportional peak has passed; the dwell
        //! is 2048 ticks (43 ms), so 12 M cycles cover the pull-in
        run_fed(12000000);
        ck("CRF: align loop engaged on the physical frame marker",
           dut->rootp->milan_datapath__DOT__mga_engaged_w, 1);
        live_first_seq = aaf_seq;
        run_fed(3000000);
        live_last_seq = aaf_seq;
        prove_the_live_selection_recentred_once(200);
        aaf_on = false;
        return report();
    }

    int report() const {
        printf("\n----------------------------------------------------------------------\n");
        printf("media_aclk: %ld checks, %ld failures\n", checks, fails);
        printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
        return fails ? 1 : 0;
    }
};

int MediaGridAlignmentHarness::run() {
    const milan::tb::Model<Vmilan_datapath> model;
    dut = model.get();

    printf("======================================================================\n");
    printf("media-grid alignment at the TRUE ratio: clk_audio = axis * %ld/%ld\n",
           AUD_NUM, AUD_DEN);
    printf("======================================================================\n");

    if (live_only) return run_live_only();

    bring_out_of_reset();
    bind_listener_zero_over_acmp();
    measure_the_render_law_at_internal();
    prove_the_recentre_is_one_shot("RENDER-RC-INT");
    //! --render-only: the mutation arm's leg - the law and the recentre at
    //! INTERNAL are what the stage's mutants must break, and the grid phases
    //! below are the expensive half of this binary
    if (render_only) { aaf_on = false; return report(); }

    //! the stream now stays LIVE through the grid phases: moved one event
    //! off here, carried through the INTERNAL measurement, and judged after
    //! the CRF selection re-centred it. #390's ring phases run AFTER the
    //! move: they re-aim the feed and stimulate the audio clock, so the
    //! move's own "sat at the setpoint before the move" window has to be
    //! measured before they touch it, and the selection's recentre is what
    //! restores the law afterwards (RENDER-LIVE-CRF grades that).
    move_the_running_feed_past_a_tick("RENDER-LIVE", true);
    double ppm_int = 0.0;
    if (!measure_the_internal_free_run_drift(ppm_int)) return 1;
    prove_the_loop_ring_slips_at_internal();
    prove_the_slip_words_follow_their_taps();
    select_crf_and_prove_the_grids_align(ppm_int);
    prove_the_live_selection_recentred_once(1100);
    measure_the_render_law_under_crf();
    prove_the_recentre_is_one_shot("RENDER-RC-CRF");
    //! #390's CRF ring window: the grids are aligned and the render law has
    //! just been measured on them, so the ring is graded before the feed is
    //! moved off the setpoint again for the deselect below
    prove_the_loop_ring_rides_one_grid_under_crf();
    //! ...and the other way for the deselect inside the mr phase
    move_the_running_feed_past_a_tick("RENDER-LIVE", false);
    prove_the_mr_toggle_echoes_only_under_crf();
    aaf_on = false;

    return report();
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    MediaGridAlignmentHarness harness;
    for (int i = 1; i < argc; i++) {
        if (std::string(argv[i]) == "--render-only") harness.render_only = true;
        if (std::string(argv[i]) == "--live-only") harness.live_only = true;
    }
    return harness.run();
}
