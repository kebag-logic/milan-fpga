// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_tdm8_render - the shipping AX7101 TDM8 render lane, from the dynamic
// AUDIO_MAP command to the DECODED SERIAL OUTPUT (issue #447).
//
// WHY THIS IS ITS OWN BINARY. sim_aclk is the #386 render-law instrument and
// carries its own mutation arm; adding the AECP map face, the CSR diagnostic
// window and a serial decoder to it would enlarge the blast radius of every
// future render-law change for no gain. Same reason the tree already keeps
// sim_aclk separate from sim_nxn.
//
// WHAT IT PROVES, and the one rule that makes it worth anything: NOTHING THE
// DUT PRODUCES IS USED AS AN EXPECTED VALUE.
//
//   * The INJECTION RECORD is built before any traffic is sent. inj[e][s] is
//     the 24-bit word {pdu[11:0], event[3:0], channel[7:0]} of media event
//     ordinal e on stream wire channel s. The AAF feeder transmits FROM that
//     table and never writes back to it.
//   * The ROUTE RECORD is built only from the ADD and REMOVE records this leg
//     issued and the SUCCESS status each returned. GET_AUDIO_MAP and the CSR
//     render-RAM readback are GRADED against it; they do not define it.
//   * The PIN DECODER reads exactly three signals - tdm_bclk_o, tdm_fsync_o
//     and tdm_dout_o - sampled after each half step. It reads no DUT internal,
//     and specifically not the exported frame position or bit-clock enables.
//     A frame counter, an FSYNC toggle and an internal crossbar tap are each
//     insufficient by construction, which is what issue #447 acceptance 5
//     asks for.
//   * Internal taps are TIMESTAMP and COUNTER sources only: the crossbar's
//     valid pulse, the adapter's commit strobe, the serial frame start and
//     adoption instants, and the five lane counters. The m-th post-epoch
//     crossbar pulse is correlated with the m-th decoded frame BY COUNT, never
//     by reading its payload.
//
// THE DECODER'S PHASE, and why it is not the slave suite's model. On this
// MASTER-driven bus fsync occupies bit period 0 and data starts in bit period
// 1, so a pin-level receiver sees fsync rise, then samples the last pad bit of
// the previous frame, and only THEN slot 0's MSB: TWO bclk rising edges after
// the observed fsync rise, with the TRIGGER EDGE EXCLUDED FROM THE COUNTDOWN.
// That is the rule the in-tree external codec model of this same bus already
// presents to the capture direction (it arms on a rising edge and counts LATER
// edges). tb/verilator/tdm_render's golden de-serializer models a SLAVE bus
// whose driving master presents fsync with half a bit period of setup and
// takes the MSB one rise earlier; it is deliberately NOT reused here, and both
// it and KL_tdm_render stay untouched and green on their own bench.
//
// WHAT THE FRAMING COUNTER CAN AND CANNOT SEE. The decoder's free-running
// position advances from BCLK alone. A mutation that shifts DOUT by one bit
// while leaving BCLK and FSYNC alone therefore leaves every framing value
// unchanged: it is graded by the full 24-bit word identity and the 8-bit pad
// check, not by the cadence counter. The cadence counter is kept for the
// clock/frame faults it really does observe (a frame that is not 256 bclks,
// or a decoder that resynchronises against its own count).
//
// WHAT IT DOES NOT CLAIM. This is a digital, zero-delay model. It does not
// establish electrical margin at the pins, and the counter-crossing arm below
// does not claim to demonstrate metastability: the CDC discrimination is done
// by the mutation arm's explicitly modelled bit-arrival skew, whose limits are
// stated there. Physical acceptance stays with #386 acceptance 4 and #117.
//
// Modes: no argument runs every phase. --serial-only and --epoch-only are the
// short legs tdm8_render_mutants.py runs, and --defect-stopped-clock and
// --defect-one-sample are its two leg-side defect arms.

#include "../../common/verilator_harness.hpp"
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"

#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

namespace {

//! AXI4-Lite handshake guard: cycles a single beat may wait before the BFM
//! gives up rather than hanging the leg.
constexpr int kAxiGuardCycles = 2048;
//! the shipping listener stream: 8 wire channels, 6 events per class-A PDU
constexpr int kChans = 8;
constexpr int kEvents = 6;
constexpr size_t kPayloadBytes = static_cast<size_t>(kChans) * kEvents * 4;
constexpr size_t kFrameBytes = 14 + 24 + kPayloadBytes;
//! six events per PDU at 48 kHz on the 100 MHz axis clock
constexpr long kPduPeriodCycles = 12500;
//! the exact fractional-N product clock plan: clk_audio_i = clk_tdm_i =
//! axis_clk x 391/1591 = 24,575,738.5292 Hz, BCLK_HALF_P = 1
constexpr long kAudNum = 391;
constexpr long kAudDen = 1591;
//! the serial frame: 8 slots x 32 bit clocks
constexpr int kSlots = 8;
constexpr int kSlotBits = 32;
constexpr int kFrameBclks = kSlots * kSlotBits;
//! the crossbar's TDM key lane (milan_datapath CHMAP_RPHYS_TDM_BASE_C / _N_C).
//! Stated here as the LAW under test, never read back from the DUT.
constexpr int kTdmBase = 2;
constexpr int kI2sBase = 0;
constexpr int kI2sN = 2;
//! the permutation the map programs: no fixed point, so an identity
//! projection cannot pass by accident
constexpr std::array<int, kSlots> kPerm = {3, 5, 0, 7, 2, 6, 1, 4};
//! how far the grading cursor may advance over one decoded frame before the
//! frame is a failure rather than a counted skip
constexpr int kMaxAdvance = 4;

//! One decoded serial frame: the eight 32-bit slot words, exactly as the pins
//! delivered them, and the harness time of slot 0's MSB sampling edge.
struct DecodedFrame {
    std::array<uint32_t, kSlots> slot{};
    long half_step = 0;                 //! of slot 0's MSB sampling edge
    std::array<long, kSlots> msb_half{};//! ...and of every slot's MSB edge
    uint64_t frames_at = 0;             //! lane counters at publication
    uint64_t unders_at = 0;
    uint64_t skips_at = 0;
};

class TdmRenderHarness {
 public:
    int run(int argc, char** argv);

 private:
    Vmilan_datapath* dut = nullptr;
    milan::tb::Checker check{"tdm8_render"};

    bool serial_only = false;
    bool epoch_only = false;
    bool defect_stopped_clock = false;
    bool defect_one_sample = false;

    // ---------------------------------------------------------------- //
    //  The fractional-N product clock, and the freeze this leg needs    //
    // ---------------------------------------------------------------- //
    long acc = 0;
    int  aud = 0;
    long axis_cycle = 0;
    long half_step = 0;
    bool tdm_frozen = false;            //! hold clk_tdm_i static

    void half() {
        if (!tdm_frozen) {
            acc += kAudNum;
            if (acc >= kAudDen) { acc -= kAudDen; aud ^= 1; }
        }
        dut->clk_audio_i = aud;
        dut->clk_tdm_i   = aud;
        ++half_step;
    }

    //! The two memory models are driven and advanced in the LOW phase, the
    //! ordering every other milan_dp leg uses: the model presents its inputs,
    //! the low eval settles, and only then does it read the DUT's registered
    //! valid/ready back. Advancing them on the rising edge instead reads the
    //! outputs the DUT is registering at that very edge, and a valid/ready
    //! handshake graded half a cycle out deadlocks the descriptor burst - the
    //! store then never validates the image and every map command comes back
    //! NO_SUCH_DESCRIPTOR, which looks exactly like a broken responder.
    void lo() {
        dut->axis_clk = 0; dut->gtx_clk = 0;
        desc_drive(); resp_drive();
        half(); dut->eval();
        desc_edge(); resp_edge();
        observe();
    }
    void hi() {
        dut->axis_clk = 1; dut->gtx_clk = 1;
        half(); dut->eval();
        ++axis_cycle;
        observe_axis();
        observe();
        sniff_probe();
    }

    // ---------------------------------------------------------------- //
    //  The two processor memory faces. The AECP uCPU serves the entity  //
    //  model from main memory and lays its responses out in a second    //
    //  region; both are ordered models with no DDR timing claim. The    //
    //  descriptor image is the one the BUILD ships, generated from this //
    //  config by the same two tools sw/litex loads at PP_DESC_BASE_P,   //
    //  so the map face this leg drives is the one a board would serve.  //
    // ---------------------------------------------------------------- //
    static constexpr uint32_t kDescBase = 0x20000000u;
    static constexpr uint32_t kRespBase = 0x20100000u;
    std::vector<uint8_t> desc_img;
    long desc_requests = 0;             //! bursts the AECP store asked for
    bool desc_busy = false;
    uint32_t desc_addr = 0;
    unsigned desc_left = 0;
    unsigned desc_wait = 0;
    std::array<uint8_t, 592> resp_mem{};
    bool mem_busy = false;
    uint32_t mem_addr = 0;
    unsigned mem_left = 0;
    bool mem_done = false;

    void desc_drive() {
        uint64_t data = 0;
        for (unsigned i = 0; i < 8; ++i) {
            const size_t off = static_cast<size_t>(desc_addr - kDescBase) + i;
            data = (data << 8) | (off < desc_img.size() ? desc_img[off] : 0);
        }
        dut->i_desc_mem_req_ready = !desc_busy;
        dut->i_desc_mem_rsp_valid = desc_busy && desc_wait == 0;
        dut->i_desc_mem_rsp_data = data;
        dut->i_desc_mem_rsp_last = desc_busy && desc_left == 1;
        dut->i_desc_mem_rsp_err = 0;
    }
    void desc_edge() {
        if (!desc_busy && dut->o_desc_mem_req_valid) {
            ++desc_requests;
            desc_addr = dut->o_desc_mem_req_addr;
            desc_left = dut->o_desc_mem_req_beats;
            desc_busy = desc_left != 0;
            desc_wait = 12;
        } else if (desc_busy && desc_wait) {
            --desc_wait;
        } else if (desc_busy && dut->o_desc_mem_rsp_ready) {
            desc_addr += 8;
            if (--desc_left == 0) desc_busy = false;
        }
    }
    void resp_drive() {
        uint64_t data = 0;
        for (unsigned i = 0; i < 8; ++i) {
            const size_t off = static_cast<size_t>(mem_addr - kRespBase) + i;
            data = (data << 8) | (off < resp_mem.size() ? resp_mem[off] : 0);
        }
        dut->i_resp_mem_req_ready = !mem_busy;
        dut->i_resp_mem_rsp_valid = mem_busy;
        dut->i_resp_mem_rsp_data = data;
        dut->i_resp_mem_rsp_last = mem_busy && mem_left == 1;
        dut->i_resp_mem_rsp_err = 0;
        dut->i_resp_mem_wr_ready = !mem_done;
        dut->i_resp_mem_wr_done = mem_done;
        dut->i_resp_mem_wr_err = 0;
    }
    void resp_edge() {
        if (mem_busy && dut->o_resp_mem_rsp_ready) {
            mem_addr += 8;
            if (--mem_left == 0) mem_busy = false;
        } else if (!mem_busy && dut->o_resp_mem_req_valid) {
            mem_addr = dut->o_resp_mem_req_addr;
            mem_left = dut->o_resp_mem_req_beats;
            mem_busy = mem_left != 0;
        }
        if (mem_done) {
            mem_done = false;
        } else if (dut->o_resp_mem_wr_valid) {
            for (unsigned i = 0; i < 8; ++i) {
                const size_t off =
                    static_cast<size_t>(dut->o_resp_mem_wr_addr - kRespBase) + i;
                if (off < resp_mem.size() && (dut->o_resp_mem_wr_strb & (1u << i)))
                    resp_mem[off] =
                        static_cast<uint8_t>(dut->o_resp_mem_wr_data >> (56 - 8 * i));
            }
            mem_done = true;
        }
    }
    bool load_descriptor_image(const char* path);
    void step() { lo(); hi(); }
    void steps(long n) { while (n--) step(); }

    // ---------------------------------------------------------------- //
    //  THE PIN DECODER. Three pins, nothing else.                      //
    // ---------------------------------------------------------------- //
    int  p_bclk = 0;
    int  p_fsync = 0;
    bool armed = false;
    int  pend = 0;
    bool framed = false;
    int  q = 0;                          //! free-running bit position
    long rises = 0;                      //! bclk rises since reset release
    long rises_at_last_fsync = -1;
    long fsync_rises = 0;
    std::array<uint32_t, kSlots> word{};
    std::array<long, kSlots> msb_half{};
    long frame_msb_half = 0;
    std::vector<DecodedFrame> decoded;
    long framing_faults = 0;             //! q != 0 at a two-rise expiry
    long gap_faults = 0;                 //! fsync-to-fsync != 256 bclk rises
    bool collect = false;                //! publish frames into `decoded`

    void observe() {
        const int b = dut->tdm_bclk_o;
        const int f = dut->tdm_fsync_o;
        const int d = dut->tdm_dout_o;
        if (!(b && !p_bclk)) { p_bclk = b; return; }
        p_bclk = b;
        ++rises;
        // THE COUNTDOWN EXCLUDES ITS OWN TRIGGER EDGE. Setting the delay on
        // the fsync rise and decrementing on that same edge would put the
        // first decoded MSB one rise early, which this bus does not deliver.
        if (f && !p_fsync && armed) {
            if (rises_at_last_fsync >= 0 && rises - rises_at_last_fsync != kFrameBclks)
                ++gap_faults;
            rises_at_last_fsync = rises;
            ++fsync_rises;
            pend = 2;
        } else if (pend > 0 && --pend == 0) {
            if (framed && q != 0) ++framing_faults;
            q = 0;
            framed = true;
        }
        if (!f) armed = true;
        p_fsync = f;
        if (!framed) return;
        const int slot = q / kSlotBits;
        const int bit = q % kSlotBits;
        if (bit == 0) msb_half[static_cast<size_t>(slot)] = half_step;
        if (slot == 0 && bit == 0) frame_msb_half = half_step;
        word[static_cast<size_t>(slot)] =
            (word[static_cast<size_t>(slot)] << 1) | static_cast<uint32_t>(d);
        if (slot == kSlots - 1 && bit == kSlotBits - 1 && collect) {
            DecodedFrame fr;
            fr.slot = word;
            fr.msb_half = msb_half;
            fr.half_step = frame_msb_half;
            fr.frames_at = lane_frames();
            fr.unders_at = lane_unders();
            fr.skips_at = lane_skips();
            decoded.push_back(fr);
        }
        if (++q == kFrameBclks) q = 0;
    }

    void decoder_reset() {
        armed = false; pend = 0; framed = false; q = 0;
        rises = 0; rises_at_last_fsync = -1; fsync_rises = 0;
        framing_faults = 0; gap_faults = 0;
        word.fill(0); msb_half.fill(0);
        decoded.clear();
        p_bclk = dut->tdm_bclk_o;
        p_fsync = dut->tdm_fsync_o;
    }

    // ---------------------------------------------------------------- //
    //  Internal taps: timestamps and counters ONLY                     //
    // ---------------------------------------------------------------- //
    uint64_t lane_frames() const { return dut->rootp->milan_datapath__DOT__tdmr_frames_w; }
    uint64_t lane_unders() const { return dut->rootp->milan_datapath__DOT__tdmr_underruns_w; }
    uint64_t lane_skips()  const { return dut->rootp->milan_datapath__DOT__tdmr_skips_w; }
    uint64_t lane_over()   const { return dut->rootp->milan_datapath__DOT__tdmr_overruns_w; }
    uint64_t lane_epochs() const { return dut->rootp->milan_datapath__DOT__tdmr_epochs_w; }

    std::vector<long> phys_valid_cycle;  //! axis cycle of each crossbar pulse
    std::vector<long> commit_cycle;      //! axis cycle of each frame commit
    long adopt_events = 0;
    int  adopt_prev = 0;
    //! T28's counter-sanity record: every sampled frames_o, against the pin
    //! decoder's own count of observed frame boundaries. The baseline is taken
    //! when the decoder re-arms, so the two are counting the same interval.
    uint64_t frames_seen_max = 0;
    uint64_t frames_base = 0;
    long counter_regressions = 0;
    long counter_impossible = 0;
    long counter_worst_lead = 0;

    void observe_axis() {
        if (dut->rootp->milan_datapath__DOT__chmap_phys_v_w)
            phys_valid_cycle.push_back(axis_cycle);
        if (dut->rootp->milan_datapath__DOT__tdmr_commit_p_w)
            commit_cycle.push_back(axis_cycle);
        const int a = dut->rootp->milan_datapath__DOT__tdmr_adopt_p_w;
        if (a && !adopt_prev) ++adopt_events;
        adopt_prev = a;
        const uint64_t fr = lane_frames();
        if (fr < frames_seen_max) ++counter_regressions;
        else frames_seen_max = fr;
        // The counter increments at frame starts; the decoder counts fsync
        // rises, one bit period apart, so over the SAME interval the two can
        // differ only by a frame plus the crossing's own registration. A
        // sampled value ahead of what the pins can justify is a value the
        // counter never held - the discrimination the gray crossing exists
        // for, read without trusting the counter to grade itself.
        const long lead = static_cast<long>(fr - frames_base) - fsync_rises;
        if (lead > counter_worst_lead) counter_worst_lead = lead;
        if (lead > 3) ++counter_impossible;
    }

    void taps_reset() {
        phys_valid_cycle.clear();
        commit_cycle.clear();
        adopt_events = 0;
        frames_seen_max = lane_frames();
        frames_base = lane_frames();
        counter_regressions = 0;
        counter_impossible = 0;
        counter_worst_lead = 0;
    }

    // ---------------------------------------------------------------- //
    //  AXI4-Lite BFM                                                   //
    // ---------------------------------------------------------------- //
    void axi_write(uint16_t a, uint32_t d) {
        dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
        dut->s_axi_wdata = d;  dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
        dut->s_axi_bready = 1;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); const bool acc_w = dut->s_axi_awready && dut->s_axi_wready; hi();
            if (acc_w) break;
        }
        dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); const bool bv = dut->s_axi_bvalid; hi(); if (bv) break;
        }
        dut->s_axi_bready = 0;
    }
    uint32_t axi_read(uint16_t a) {
        dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); const bool ar = dut->s_axi_arready; hi(); if (ar) break;
        }
        dut->s_axi_arvalid = 0;
        uint32_t d = 0;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); const bool rv = dut->s_axi_rvalid; if (rv) d = dut->s_axi_rdata; hi();
            if (rv) break;
        }
        dut->s_axi_rready = 0;
        return d;
    }

    // ---------------------------------------------------------------- //
    //  MAC ingress                                                     //
    // ---------------------------------------------------------------- //
    void inject(const uint8_t* f, size_t len) {
        std::vector<uint64_t> beats;
        for (size_t bt = 0; bt < (len + 7) / 8; bt++) {
            uint64_t v = 0;
            for (int j = 0; j < 8; j++)
                if (bt * 8 + j < len)
                    v |= static_cast<uint64_t>(f[bt * 8 + j]) << (8 * j);
            beats.push_back(v);
        }
        size_t idx = 0;
        for (int c = 0; c < 1500 && idx < beats.size() + 8; c++) {
            if (idx < beats.size()) {
                dut->s_axis_mac_rx_tdata  = beats[idx];
                dut->s_axis_mac_rx_tkeep  = 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast  = (idx == beats.size() - 1);
            } else {
                dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
            }
            lo();
            const bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
            hi();
            if (in_acc || idx >= beats.size()) idx++;
        }
        dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
    }

    // ---------------------------------------------------------------- //
    //  THE IMMUTABLE INJECTION RECORD                                  //
    // ---------------------------------------------------------------- //
    //! inj[e][s]: the 24-bit word of media event ordinal e on wire channel s.
    //! Built before any traffic and never written again.
    std::vector<std::array<uint32_t, kChans>> inj;
    long injected_events = 0;            //! how many ordinals have been sent

    void build_injection_record(long pdus) {
        inj.clear();
        inj.reserve(static_cast<size_t>(pdus) * kEvents);
        for (long p = 0; p < pdus; p++)
            for (int k = 0; k < kEvents; k++) {
                std::array<uint32_t, kChans> ev{};
                for (int c = 0; c < kChans; c++)
                    ev[static_cast<size_t>(c)] =
                        (static_cast<uint32_t>(p & 0xFFF) << 12) |
                        (static_cast<uint32_t>(k & 0xF) << 8) |
                        static_cast<uint32_t>(c & 0xFF);
                inj.push_back(ev);
            }
        injected_events = 0;
    }

    bool feed_on = false;
    long next_pdu_at = 0;
    uint8_t wire_seq = 0;
    long pdu_cursor = 0;

    void send_pdu() {
        uint8_t f[kFrameBytes]; memset(f, 0, sizeof f);
        const uint8_t dmac[6] = {
            0x91, 0xE0, 0xF0, 0x00, 0x2A, 0x02};
        memcpy(f, dmac, 6);
        const uint8_t src[6] = {
            0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
        memcpy(f + 6, src, 6);
        f[12] = 0x22; f[13] = 0xF0;
        f[14] = 0x02;                               // AAF
        f[15] = 0x81;                               // sv, tv
        f[16] = wire_seq++;
        const uint8_t sid[8] = {
            0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00};
        memcpy(f + 18, sid, 8);
        f[26] = 0x00; f[27] = 0x00; f[28] = 0x10; f[29] = 0x00;
        f[30] = 0x02;                               // INT32
        f[31] = static_cast<uint8_t>(0x05 << 4);    // 48 kHz
        f[32] = static_cast<uint8_t>(kChans);
        f[33] = 32;
        f[34] = static_cast<uint8_t>(kPayloadBytes >> 8);
        f[35] = static_cast<uint8_t>(kPayloadBytes & 0xFF);
        for (int k = 0; k < kEvents; k++) {
            const size_t e = static_cast<size_t>(injected_events) + static_cast<size_t>(k);
            if (e >= inj.size()) break;
            for (int c = 0; c < kChans; c++) {
                uint32_t v = inj[e][static_cast<size_t>(c)];
                // the ONE arm that deliberately puts a different word on the
                // wire than the record holds (N4): the record keeps the
                // intended value, so the identity check is the thing that has
                // to notice
                if (defect_one_sample && c == 3 && e == corrupt_at)
                    v ^= 0x000010u;
                const size_t o = 38 + 4 * (static_cast<size_t>(k) * kChans + c);
                f[o]     = static_cast<uint8_t>(v >> 16);
                f[o + 1] = static_cast<uint8_t>(v >> 8);
                f[o + 2] = static_cast<uint8_t>(v);
                f[o + 3] = 0;
            }
        }
        injected_events += kEvents;
        ++pdu_cursor;
        inject(f, kFrameBytes);
    }
    long corrupt_at = 1 << 30;

    void run_fed(long n) {
        const long stop = axis_cycle + n;
        while (axis_cycle < stop) {
            if (feed_on && axis_cycle >= next_pdu_at &&
                static_cast<size_t>(injected_events) + kEvents <= inj.size()) {
                send_pdu();
                next_pdu_at += kPduPeriodCycles;
            } else {
                step();
            }
        }
    }

    // ---------------------------------------------------------------- //
    //  THE ROUTE RECORD - issued commands only                         //
    // ---------------------------------------------------------------- //
    //! route[co] = the stream wire channel feeding global cluster key co, or
    //! -1 for a cluster with no mapping. Written only from an ADD/REMOVE this
    //! leg issued that returned SUCCESS.
    std::array<int, kSlots> route{};

    void route_reset() { route.fill(-1); }
    //! serial slot k is fed by the cluster whose key is k (PBASE 0), so its
    //! source channel is route[k]
    int src_of_slot(int k) const { return route[static_cast<size_t>(k)]; }

    // ---------------------------------------------------------------- //
    //  AECP command face                                               //
    // ---------------------------------------------------------------- //
    static constexpr uint16_t kCmdGetAudioMap = 43;
    static constexpr uint16_t kCmdAddMappings = 44;
    static constexpr uint16_t kCmdRemoveMappings = 45;
    static constexpr uint16_t kDescStreamPortIn = 0x000E;
    uint16_t aecp_seq = 0x4470;
    //! print the raw answer of a map command that neither succeeded nor
    //! earned the documented BAD_ARGUMENTS refusal, so an unexpected status
    //! is diagnosable from the log alone
    bool trace_map_cmd = true;

    std::vector<uint8_t> aecp_request(uint16_t cmd, uint16_t sq,
                                      const std::vector<uint8_t>& pl) {
        const size_t flen = (38 + pl.size() < 60) ? 60 : 38 + pl.size();
        std::vector<uint8_t> f(flen, 0);
        const uint8_t cmac[6] = {
            0x68, 0x05, 0xCA, 0x95, 0xB2, 0xD1};
        memcpy(f.data() + 6, cmac, 6);
        f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFB; f[15] = 0x00;
        const uint16_t cdl = static_cast<uint16_t>(12 + pl.size());
        f[16] = static_cast<uint8_t>((cdl >> 8) & 0x7);
        f[17] = static_cast<uint8_t>(cdl);
        const uint8_t teid[8] = {
            0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x01};
        memcpy(f.data() + 18, teid, 8);
        const uint8_t ceid[8] = {
            0x68, 0x05, 0xCA, 0xFF, 0xFE, 0x95, 0xB2, 0xD1};
        memcpy(f.data() + 26, ceid, 8);
        f[34] = static_cast<uint8_t>(sq >> 8); f[35] = static_cast<uint8_t>(sq);
        f[36] = static_cast<uint8_t>((cmd >> 8) & 0x7F);
        f[37] = static_cast<uint8_t>(cmd);
        for (size_t i = 0; i < pl.size(); i++) f[38 + i] = pl[i];
        return f;
    }

    std::vector<uint8_t> await_aecp(int cyc = 200000) {
        std::vector<uint8_t> cur, resp;
        dut->m_axis_mac_tx_tready = 1;
        for (int c = 0; c < cyc && resp.empty(); c++) {
            lo();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                for (int l = 0; l < 8; l++)
                    if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                        cur.push_back(static_cast<uint8_t>(dut->m_axis_mac_tx_tdata >> (8 * l)));
                if (dut->m_axis_mac_tx_tlast) {
                    const bool is_aecp = cur.size() > 37 && cur[12] == 0x22 &&
                                         cur[13] == 0xF0 && cur[14] == 0xFB;
                    const bool solicited = is_aecp && (cur[15] & 0xF) == 1 &&
                                           (cur[36] & 0x80) == 0;
                    if (solicited) resp = cur;
                    cur.clear();
                }
            }
            hi();
        }
        return resp;
    }

    std::vector<uint8_t> aecp_xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
        const std::vector<uint8_t> f = aecp_request(cmd, aecp_seq++, pl);
        inject(f.data(), f.size());
        return await_aecp();
    }

    static long aecp_status(const std::vector<uint8_t>& b) {
        return b.size() > 16 ? (b[16] >> 3) & 0x1F : -1;
    }

    //! One ADD or REMOVE of n {stream_channel, cluster_offset} rows on
    //! STREAM_PORT_INPUT 0. Returns the AEM status.
    long map_cmd(uint16_t cmd, const std::vector<std::pair<int, int>>& rows,
                 int port = 0) {
        std::vector<uint8_t> pl = {
            static_cast<uint8_t>(kDescStreamPortIn >> 8),
            static_cast<uint8_t>(kDescStreamPortIn),
            static_cast<uint8_t>(port >> 8), static_cast<uint8_t>(port),
            0x00, static_cast<uint8_t>(rows.size()), 0x00, 0x00};
        for (const auto& r : rows) {
            const uint8_t row[8] = {
                0, 0, 0, static_cast<uint8_t>(r.first),
                                    0, static_cast<uint8_t>(r.second), 0, 0};
            pl.insert(pl.end(), row, row + 8);
        }
        const auto resp = aecp_xact(cmd, pl);
        const long st = aecp_status(resp);
        if (st != 0 && st != 7 && trace_map_cmd) {
            std::printf("  [i]    map command %u returned status %ld, %zu "
                        "bytes:", cmd, st, resp.size());
            for (size_t i = 0; i < resp.size() && i < 56; i++)
                std::printf(" %02X", resp[i]);
            std::printf("\n");
        }
        if (st == 0) {
            for (const auto& r : rows) {
                if (r.second < 0 || r.second >= kSlots) continue;
                route[static_cast<size_t>(r.second)] =
                    (cmd == kCmdAddMappings) ? r.first : -1;
            }
        }
        return st;
    }

    //! The GET_AUDIO_MAP page, as {stream_index, stream_channel,
    //! cluster_offset} rows.
    std::vector<std::array<int, 3>> get_audio_map(int port = 0, int page = 0,
                                                  long* number_of_maps = nullptr) {
        const std::vector<uint8_t> pl = {
            static_cast<uint8_t>(kDescStreamPortIn >> 8),
            static_cast<uint8_t>(kDescStreamPortIn),
            static_cast<uint8_t>(port >> 8), static_cast<uint8_t>(port),
            static_cast<uint8_t>(page >> 8), static_cast<uint8_t>(page),
            0x00, 0x00};
        const auto r = aecp_xact(kCmdGetAudioMap, pl);
        std::vector<std::array<int, 3>> rows;
        if (aecp_status(r) != 0 || r.size() < 50) return rows;
        if (number_of_maps != nullptr)
            *number_of_maps = (static_cast<long>(r[44]) << 8) | r[45];
        const unsigned n = (static_cast<unsigned>(r[46]) << 8) | r[47];
        if (r.size() < 50 + 8 * n) return rows;
        for (unsigned i = 0; i < n; i++) {
            const size_t o = 50 + 8 * i;
            rows.push_back({static_cast<int>((r[o] << 8) | r[o + 1]),
                            static_cast<int>((r[o + 2] << 8) | r[o + 3]),
                            static_cast<int>((r[o + 4] << 8) | r[o + 5])});
        }
        return rows;
    }

    // ---------------------------------------------------------------- //
    //  CSR crossbar window                                             //
    // ---------------------------------------------------------------- //
    static constexpr uint16_t kChmapCtrl = 0x900;
    static constexpr uint16_t kChmapSel  = 0x904;
    static constexpr uint16_t kChmapWord = 0x908;
    static constexpr uint16_t kChmapSnap = 0x910;
    static constexpr uint16_t kChmapLoop = 0x914;

    //! the render RAM word at a PHYSICAL render key. The 0x904 selector is a
    //! PHYSICAL key on the readback side and a GLOBAL CLUSTER key on the
    //! 0x908 write side; on every shape shipped so far the two coincided, and
    //! on this one they differ by the lane base. That asymmetry is preserved
    //! from source, documented in the register map, and pinned by T10.
    uint32_t render_ram(int phys_key) {
        axi_write(kChmapSel, static_cast<uint32_t>(phys_key));
        axi_write(kChmapSnap, 1);
        for (int g = 0; g < 64; g++) {
            const uint32_t sv = axi_read(kChmapSnap);
            if ((sv & 1) == 0) break;
        }
        const uint32_t v = axi_read(kChmapLoop);
        if (((v >> 26) & 1) == 0) return 0xFFFFFFFFu;
        return v & 0xFF;
    }

    //! one CSR 0x908 write, addressed by GLOBAL CLUSTER key
    void csr_map_write(int cluster_key, uint32_t word16) {
        const uint32_t ctrl = axi_read(kChmapCtrl);
        axi_write(kChmapCtrl, ctrl | 1u);
        axi_write(kChmapSel, static_cast<uint32_t>(cluster_key));
        axi_write(kChmapWord, word16);
        axi_write(kChmapCtrl, ctrl);
        steps(16);
    }

    // ---------------------------------------------------------------- //
    //  ACMP: the bind ladder and the unbind                            //
    // ---------------------------------------------------------------- //
    std::vector<uint8_t> sniff_fr;
    uint16_t probe_seq = 0;
    bool probe_seen = false;

    void sniff_probe() {
        if (!(dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready)) return;
        for (int l = 0; l < 8; l++)
            if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                sniff_fr.push_back(static_cast<uint8_t>(dut->m_axis_mac_tx_tdata >> (8 * l)));
        if (!dut->m_axis_mac_tx_tlast) return;
        if (sniff_fr.size() >= 64 && sniff_fr[12] == 0x22 && sniff_fr[13] == 0xF0 &&
            sniff_fr[14] == 0xFC && (sniff_fr[15] & 0xF) == 0x0) {
            probe_seq = static_cast<uint16_t>((sniff_fr[62] << 8) | sniff_fr[63]);
            probe_seen = true;
        }
        sniff_fr.clear();
    }

    void acmp_connect_rx(uint16_t seq) {
        uint8_t f[72]; memset(f, 0, sizeof f);
        const uint8_t mc[6] = {
            0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
        memcpy(f, mc, 6);
        const uint8_t csrc[6] = {
            0x68, 0x05, 0xCA, 0x95, 0xB2, 0xD1};
        memcpy(f + 6, csrc, 6);
        f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFC; f[15] = 0x06;
        f[16] = 0x00; f[17] = 44;
        for (int i = 26; i < 34; i++) f[i] = static_cast<uint8_t>(i);
        const uint8_t tk[8] = {
            0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x02};
        memcpy(f + 34, tk, 8);
        const uint8_t ls[8] = {
            0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x01};
        memcpy(f + 42, ls, 8);
        f[62] = static_cast<uint8_t>(seq >> 8); f[63] = static_cast<uint8_t>(seq);
        inject(f, 70);
    }

    void acmp_play_talker_response() {
        uint8_t f[72]; memset(f, 0, sizeof f);
        const uint8_t mc[6] = {
            0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
        memcpy(f, mc, 6);
        const uint8_t tsrc[6] = {
            0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
        memcpy(f + 6, tsrc, 6);
        f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFC; f[15] = 0x01;
        f[16] = 0x00; f[17] = 44;
        const uint8_t sid[8] = {
            0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00};
        memcpy(f + 18, sid, 8);
        for (int i = 26; i < 34; i++) f[i] = static_cast<uint8_t>(i);
        const uint8_t tk[8] = {
            0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x02};
        memcpy(f + 34, tk, 8);
        const uint8_t ls[8] = {
            0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x01};
        memcpy(f + 42, ls, 8);
        const uint8_t dm[6] = {
            0x91, 0xE0, 0xF0, 0x00, 0x2A, 0x02};
        memcpy(f + 54, dm, 6);
        f[62] = static_cast<uint8_t>(probe_seq >> 8);
        f[63] = static_cast<uint8_t>(probe_seq & 0xFF);
        inject(f, 70);
    }

    //! DISCONNECT_RX alone drops the bind: the record's enable falls without
    //! a talker answer, which is exactly the qualified bind fall the render
    //! epoch watches for.
    void acmp_disconnect_rx(uint16_t seq) {
        uint8_t f[72]; memset(f, 0, sizeof f);
        const uint8_t mc[6] = {
            0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
        memcpy(f, mc, 6);
        const uint8_t csrc[6] = {
            0x68, 0x05, 0xCA, 0x95, 0xB2, 0xD1};
        memcpy(f + 6, csrc, 6);
        f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFC; f[15] = 0x08;
        f[16] = 0x00; f[17] = 44;
        const uint8_t sid[8] = {
            0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00};
        memcpy(f + 18, sid, 8);
        for (int i = 26; i < 34; i++) f[i] = static_cast<uint8_t>(i);
        const uint8_t tk[8] = {
            0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x02};
        memcpy(f + 34, tk, 8);
        const uint8_t ls[8] = {
            0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x01};
        memcpy(f + 42, ls, 8);
        f[62] = static_cast<uint8_t>(seq >> 8); f[63] = static_cast<uint8_t>(seq);
        inject(f, 70);
    }

    void bring_out_of_reset();
    void bind_listener_zero();
    void phase_map();
    void phase_serial();
    void phase_csr();
    void phase_reset();
    void phase_bind_loss();

    //! THE GRADING RULE. Every published frame is matched against the
    //! injection record at some advance a in 0..kMaxAdvance; the smallest a
    //! that matches wins. a == 0 on a later frame is a REPEAT and needs a
    //! counted underrun; a > 1 is a SKIP of a-1 events and needs a-1 COUNTED
    //! skips - which may already be PENDING, because the counter increments
    //! when a prefetched frame is overwritten and that is BEFORE the decoded
    //! frame whose ordinal jump exposes it.
    struct Grade {
        long frames = 0;
        long repeats = 0;
        long skipped = 0;
        long identity_failures = 0;
        long pad_failures = 0;
        long channel_field_failures = 0;
        long coherence_failures = 0;
        long distinct_failures = 0;
        long uncounted_repeats = 0;
        long uncounted_skips = 0;
        long pending_skips = 0;
        long cursor = 0;
        //! the advance each decoded frame took, so a later measurement can
        //! walk the COMMIT cursor beside the event cursor
        std::vector<long> advances;
    };
    Grade grade_frames(long first_event, const char* tag);

    //! The arms phase_serial and the two epoch phases run, each named for what
    //! it proves rather than for the order it happens to sit in.
    void grade_the_decoded_window(long first_event, uint64_t skips_before,
                                  uint64_t unders_before);
    void measure_the_bank_term(long* walk_min, long* walk_max);
    void measure_the_commit_to_pin_terms(const Grade& g);
    void prove_each_slot_sits_at_its_own_position(double bit_axis);
    void prove_the_lane_counters_are_coherent(uint64_t skips_before,
                                              uint64_t unders_before);
    void prove_the_surplus_is_drop_oldest();
    void prove_a_removal_silences_only_its_own_slots();
    void prove_a_stopped_clock_reset_reopens_one_epoch(
            const std::array<uint32_t, kSlots>& pre_epoch,
            uint64_t epochs_before);
    void prove_the_lane_recovers_after_a_reset();
    void prove_a_rebind_carries_only_post_rebind_audio(uint64_t epochs_before,
                                                       long events_at_loss);

    //! how many serial slots the route record currently feeds. An oracle over
    //! an empty route would match every ordinal trivially, so every arm that
    //! grades identity states this first.
    int routed_slots() const {
        int n = 0;
        for (int k = 0; k < kSlots; k++) if (route[static_cast<size_t>(k)] >= 0) ++n;
        return n;
    }
};

// ====================================================================== //

bool TdmRenderHarness::load_descriptor_image(const char* path) {
    std::FILE* f = std::fopen(path, "rb");
    if (f == nullptr) return false;
    uint8_t buf[4096];
    size_t n = 0;
    while ((n = std::fread(buf, 1, sizeof buf, f)) > 0)
        desc_img.insert(desc_img.end(), buf, buf + n);
    std::fclose(f);
    return !desc_img.empty();
}

void TdmRenderHarness::bring_out_of_reset() {
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->m_axis_mac_tx_tready = 1;
    dut->i_mac_speed = 0b10; dut->i_link_up = 1; dut->i_full_duplex = 1;
    steps(64);
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    steps(256);
}

void TdmRenderHarness::bind_listener_zero() {
    constexpr uint16_t kAdpCtrl = 0x600;
    constexpr uint16_t kAdpEidLo = 0x604;
    constexpr uint16_t kAdpEidHi = 0x608;
    constexpr uint16_t kAcmplState = 0x6A4;
    // THE STATION MAC IS LEFT AT ITS RESET ZERO, on purpose. This leg
    // addresses AECP commands to the station's own unicast address, and the
    // RX address filter answers "is this the station" against exactly that
    // register; a bench that programmed a group address there and then sent a
    // unicast command to it would be filtered out, and silence from a filter
    // looks the same as silence from a broken responder. Every other frame
    // this leg sends is multicast.
    axi_write(kAdpEidHi, 0x020000FF);
    axi_write(kAdpEidLo, 0xFE000001);
    axi_write(kAdpCtrl, 0x00001F01);
    steps(2000);
    probe_seen = false;
    acmp_connect_rx(0x1122);
    for (int c = 0; c < 4000 && !probe_seen; c++) step();
    check.dec("T1 BIND: the listener launched a PROBE_TX at the named talker",
              probe_seen ? 1 : 0, 1);
    acmp_play_talker_response();
    steps(3000);
    check.dec("T1 BIND: listener 0 bound (0x6A4[3], the class-D record)",
              (axi_read(kAcmplState) >> 3) & 1, 1);
}

TdmRenderHarness::Grade TdmRenderHarness::grade_frames(long first_event,
                                                       const char* tag) {
    Grade g;
    g.cursor = first_event;
    long skips_accounted = 0;
    const uint64_t skips0 = decoded.empty() ? 0 : decoded.front().skips_at;
    uint64_t unders_prev = decoded.empty() ? 0 : decoded.front().unders_at;
    bool first = true;
    for (const DecodedFrame& fr : decoded) {
        // THE STRUCTURAL CHECKS COME FIRST, and they are counted before the
        // ordinal search rather than after it: they must be INDEPENDENT of
        // the identity oracle, or a frame the oracle cannot place would
        // silently take its padding and its per-slot structure with it. A
        // data line shifted by one bit is exactly that case - it moves no
        // clock, so the framing counter cannot see it, and what does see it
        // is the padding and the full-word grading.
        bool pad_ok = true;
        bool chan_ok = true;
        bool coherent = true;
        std::array<uint32_t, kSlots> data{};
        for (int k = 0; k < kSlots; k++) {
            const uint32_t raw = fr.slot[static_cast<size_t>(k)];
            data[static_cast<size_t>(k)] = raw >> 8;          // 24 data bits
            if ((raw & 0xFFu) != 0) pad_ok = false;           // 8 pad bits
        }
        {
            uint32_t sid = 0;
            bool have_sid = false;
            std::array<uint32_t, kSlots> seen0{};
            int n0 = 0;
            for (int k = 0; k < kSlots; k++) {
                const int s = src_of_slot(k);
                if (s < 0) continue;
                const uint32_t v = data[static_cast<size_t>(k)];
                if ((v & 0xFFu) != static_cast<uint32_t>(s)) chan_ok = false;
                if (!have_sid) { sid = v >> 8; have_sid = true; }
                else if ((v >> 8) != sid) coherent = false;
                for (int j = 0; j < n0; j++)
                    if (seen0[static_cast<size_t>(j)] == v) ++g.distinct_failures;
                seen0[static_cast<size_t>(n0++)] = v;
            }
            if (!pad_ok) ++g.pad_failures;
            if (!chan_ok) ++g.channel_field_failures;
            if (!coherent) ++g.coherence_failures;
        }
        long advance = -1;
        for (int a = 0; a <= kMaxAdvance; a++) {
            const size_t e = static_cast<size_t>(g.cursor + a);
            if (e >= inj.size()) break;
            bool all = true;
            for (int k = 0; k < kSlots && all; k++) {
                const int s = src_of_slot(k);
                const uint32_t want = (s < 0) ? 0u
                                    : inj[e][static_cast<size_t>(s)];
                if (data[static_cast<size_t>(k)] != want) all = false;
            }
            if (all) { advance = a; break; }
        }
        if (advance < 0) {
            ++g.identity_failures;
            if (g.identity_failures <= 4) {
                std::printf("  [i]    %s frame %ld: no injection ordinal in "
                            "[%ld, %ld] matches", tag, g.frames, g.cursor,
                            g.cursor + kMaxAdvance);
                for (int k = 0; k < kSlots; k++)
                    std::printf(" s%d=%06X(src %d)", k,
                                data[static_cast<size_t>(k)], src_of_slot(k));
                std::printf("\n");
            }
            g.advances.push_back(1);        // assume the nominal advance
            ++g.frames;
            continue;
        }
        g.advances.push_back(first ? 0 : advance);

        const long pending = static_cast<long>(fr.skips_at - skips0) - skips_accounted;
        if (advance == 0 && !first) {
            ++g.repeats;
            if (fr.unders_at != unders_prev + 1) ++g.uncounted_repeats;
        } else if (advance > 1) {
            const long lost = advance - 1;
            g.skipped += lost;
            if (pending < lost) ++g.uncounted_skips;
            else skips_accounted += lost;
        }
        g.pending_skips = static_cast<long>(fr.skips_at - skips0) - skips_accounted;
        unders_prev = fr.unders_at;
        g.cursor += advance;
        ++g.frames;
        first = false;
    }
    return g;
}

// ====================================================================== //
//  Phases                                                                //
// ====================================================================== //

void TdmRenderHarness::phase_map() {
    std::printf("\n[MAP] the dynamic AUDIO_MAP command path and its projection\n");
    bind_listener_zero();
    route_reset();
    // The AECP store must actually have READ the entity image, or a refusal
    // below would be a stalled model rather than a verdict.
    check.that("the AECP descriptor store fetched the entity image",
               desc_requests > 0);
    std::printf("  [i]    %ld descriptor burst(s) served from the %zu-byte "
                "generated image\n", desc_requests, desc_img.size());

    // T2 ADD: eight records, a permutation with no fixed point
    std::vector<std::pair<int, int>> rows;
    for (int co = 0; co < kSlots; co++)
        rows.emplace_back(kPerm[static_cast<size_t>(co)], co);
    check.dec("T2 ADD: eight permuted mappings accepted",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, rows)), 0);

    // T3 GET: the requested semantic mapping comes back
    long nmaps = -1;
    const auto page = get_audio_map(0, 0, &nmaps);
    check.dec("T3 GET: the page carries all eight mappings", page.size(), kSlots);
    check.dec("T3 GET: number_of_maps is 1", static_cast<uint64_t>(nmaps), 1);
    long agree = 0;
    for (const auto& r : page)
        if (r[0] == 0 && r[2] >= 0 && r[2] < kSlots &&
            r[1] == src_of_slot(r[2]))
            ++agree;
    check.dec("T3 GET: every row agrees with the issued route record",
              static_cast<uint64_t>(agree), page.size());

    // T4 PROJECTION: the render RAM, read at PHYSICAL keys
    long projected = 0;
    for (int k = 0; k < kSlots; k++) {
        const uint32_t w = render_ram(kTdmBase + k);
        const uint32_t want = 0x80u | static_cast<uint32_t>(src_of_slot(k) & 0x3F);
        if (w == want) ++projected;
        else std::printf("  [i]    T4 physical key %d holds %02X, expected %02X\n",
                         kTdmBase + k, w, want);
    }
    check.dec("T4 PROJECTION: physical keys 2..9 hold the routed sources",
              static_cast<uint64_t>(projected), kSlots);
    long dac_clear = 0;
    for (int k = 0; k < kI2sN; k++)
        if (render_ram(kI2sBase + k) == 0) ++dac_clear;
    check.dec("T4 PROJECTION: nothing reached the pruned DAC lane keys",
              static_cast<uint64_t>(dac_clear), kI2sN);

    // T9 the two refusals, each named for its own defect class
    check.dec("T9 CLUSTER-BOUND: cluster_offset 8 past this port's 8 clusters "
              "is BAD_ARGUMENTS",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, {{0, kSlots}})), 7);
    check.dec("T9 STREAM-CHANNEL: stream_channel 8 outside the format is "
              "BAD_ARGUMENTS",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, {{kChans, 0}})), 7);
    long unchanged = 0;
    for (int k = 0; k < kSlots; k++)
        if (render_ram(kTdmBase + k) ==
            (0x80u | static_cast<uint32_t>(src_of_slot(k) & 0x3F))) ++unchanged;
    check.dec("T9: the render RAM is bit-identical after both refusals",
              static_cast<uint64_t>(unchanged), kSlots);
}

void TdmRenderHarness::phase_serial() {
    std::printf("\n[SERIAL] the pins, decoded, against the injection record\n");
    build_injection_record(400);
    feed_on = true;
    next_pdu_at = axis_cycle + 64;
    pdu_cursor = 0;
    if (defect_stopped_clock) {
        std::printf("  [i]    DEFECT ARM: clk_tdm_i held static through the "
                    "serial window\n");
        tdm_frozen = true;
    }
    // prefill and lock: the setpoint's own 18-to-14 snap happens here, and
    // the first EEGIBLE event is decided by it, not by the first injection
    run_fed(60 * kPduPeriodCycles);
    decoder_reset();
    taps_reset();
    collect = true;
    const long first_event = injected_events;
    const uint64_t skips_before = lane_skips();
    const uint64_t unders_before = lane_unders();
    run_fed(140 * kPduPeriodCycles);
    collect = false;

    check.that("T5 FRAMING: consecutive fsync rises are exactly 256 bclk rises "
               "apart", gap_faults == 0 && fsync_rises > 4);
    check.that("T5 FRAMING: the free-running position is 0 at every two-rise "
               "expiry", framing_faults == 0);
    check.that("T5 FRAMING: the window decoded whole frames", !decoded.empty());
    // An oracle over an EMPTY route matches every ordinal trivially, so the
    // route the grading stands on is stated before anything is graded.
    check.dec("T6 PRECONDITION: every serial slot is routed, so no frame can "
              "match trivially", static_cast<uint64_t>(routed_slots()), kSlots);
    if (decoded.empty()) {
        std::printf("  [i]    T5: no frame decoded - fsync rises %ld, bclk "
                    "rises %ld\n", fsync_rises, rises);
        return;
    }

    grade_the_decoded_window(first_event, skips_before, unders_before);
}

//! The decoded window, graded against the immutable injection record: the
//! first eligible ordinal, the per-frame identity, padding and structure, the
//! order rules, and the arms that follow from them.
void TdmRenderHarness::grade_the_decoded_window(long first_event,
                                                uint64_t skips_before,
                                                uint64_t unders_before) {
    // THE FIRST ELIGIBLE EVENT. It is NOT the first injected event: the
    // preserved setpoint snaps the queue to TARGET_C = 14 events at a PDU
    // end, discarding the oldest excess, and a closed render epoch suppresses
    // events while its handshake is outstanding. The cursor is therefore
    // SEARCHED for in the injection record around the first decoded frame
    // rather than assumed, and what is graded is that every later frame
    // follows from it by a permitted advance.
    long start = -1;
    const DecodedFrame& f0 = decoded.front();
    for (size_t e = 0; e + 1 < inj.size() && start < 0; e++) {
        bool all = true;
        for (int k = 0; k < kSlots && all; k++) {
            const int s = src_of_slot(k);
            const uint32_t want = (s < 0) ? 0u : inj[e][static_cast<size_t>(s)];
            if ((f0.slot[static_cast<size_t>(k)] >> 8) != want) all = false;
        }
        if (all) start = static_cast<long>(e);
    }
    check.that("T6 IDENTITY: the first decoded frame is an injected media "
               "event", start >= 0);
    if (start < 0) {
        std::printf("  [i]    T6: first decoded frame slots:");
        for (int k = 0; k < kSlots; k++)
            std::printf(" %08X", f0.slot[static_cast<size_t>(k)]);
        std::printf("\n");
    } else {
        check.that("T6 PREFILL: the first eligible event follows the preserved "
                   "prefill snap and epoch admission, not the first injection",
                   start <= first_event);
    }
    std::printf("  [i]    first decoded ordinal %ld; %ld events had been "
                "injected when collection opened\n", start, first_event);

    // The window is graded even when the first frame did not resolve to an
    // ordinal: falling back to the injection cursor keeps the per-frame
    // identity, padding and structural counts reportable, so a defect says
    // WHICH property it broke instead of stopping the phase at the door.
    const Grade g = grade_frames(start >= 0 ? start : first_event, "T6");
    check.dec("T6 IDENTITY: every decoded frame is a complete 24-bit match "
              "against the injection record",
              static_cast<uint64_t>(g.identity_failures), 0);
    check.dec("T6 PADDING: the eight pad bits of every slot are zero",
              static_cast<uint64_t>(g.pad_failures), 0);
    check.dec("T6 STRUCTURAL: each slot's channel field is its routed source",
              static_cast<uint64_t>(g.channel_field_failures), 0);
    check.dec("T6 STRUCTURAL: the eight slots carry one media event's identity",
              static_cast<uint64_t>(g.coherence_failures), 0);
    check.dec("T6 STRUCTURAL: the eight slots are distinct samples",
              static_cast<uint64_t>(g.distinct_failures), 0);
    check.dec("T6 ORDER: every repeat is a counted underrun",
              static_cast<uint64_t>(g.uncounted_repeats), 0);
    check.dec("T6 ORDER: every skipped event is covered by a counted skip",
              static_cast<uint64_t>(g.uncounted_skips), 0);
    std::printf("  [i]    %ld frames graded, %ld repeat(s), %ld skipped "
                "event(s), %ld counted skip(s) still pending adoption\n",
                g.frames, g.repeats, g.skipped, g.pending_skips);

    prove_the_lane_counters_are_coherent(skips_before, unders_before);
    measure_the_commit_to_pin_terms(g);
    prove_the_surplus_is_drop_oldest();
    prove_a_removal_silences_only_its_own_slots();
    feed_on = false;
    tdm_frozen = false;
}

//! T28 COUNTER SANITY: the gray counter crossing, read from the PINS' own
//! view of how many frames were delivered rather than from the counter
//! grading itself. `skips_before` and `unders_before` are the lane's values
//! when the window opened, printed so a later reader can place the deltas.
void TdmRenderHarness::prove_the_lane_counters_are_coherent(
        uint64_t skips_before, uint64_t unders_before) {
    check.dec("T28 COUNTERS: no sampled frame count went backwards",
              static_cast<uint64_t>(counter_regressions), 0);
    check.dec("T28 COUNTERS: no sampled frame count ran ahead of the frames "
              "the pins delivered",
              static_cast<uint64_t>(counter_impossible), 0);
    std::printf("  [i]    worst observed frames_o lead over decoded frame "
                "boundaries: %ld\n", counter_worst_lead);
    check.that("T28 COUNTERS: overruns did not move (drop-oldest keeps the "
               "CDC near empty)", lane_over() == 0);
    check.that("T28 COUNTERS: the lane counted at least as many frames as the "
               "pins delivered", lane_frames() >= static_cast<uint64_t>(fsync_rises) - 2);
    std::printf("  [i]    lane counters: frames %llu underruns %llu skips %llu "
                "overruns %llu epochs %llu (skips before the window %llu, "
                "underruns before %llu)\n",
                static_cast<unsigned long long>(lane_frames()),
                static_cast<unsigned long long>(lane_unders()),
                static_cast<unsigned long long>(lane_skips()),
                static_cast<unsigned long long>(lane_over()),
                static_cast<unsigned long long>(lane_epochs()),
                static_cast<unsigned long long>(skips_before),
                static_cast<unsigned long long>(unders_before));
}

//! T7 BANK TERM: how long the adapter takes to walk the crossbar's TDM key
//! window into the serializer's bank and commit it, measured between two
//! registered events in `axis_clk` - the crossbar's valid pulse and the frame
//! commit strobe - and never modelled.
void TdmRenderHarness::measure_the_bank_term(long* walk_min, long* walk_max) {
    *walk_min = 1 << 30;
    *walk_max = 0;
    const size_t n = (commit_cycle.size() < phys_valid_cycle.size())
                   ? commit_cycle.size() : phys_valid_cycle.size();
    for (size_t i = 0; i < n; i++) {
        const long d = commit_cycle[i] - phys_valid_cycle[i];
        if (d < 0 || d > 64) continue;              // an unpaired edge
        if (d < *walk_min) *walk_min = d;
        if (d > *walk_max) *walk_max = d;
    }
    check.that("T7 BANK TERM: the adapter's commit follows its crossbar pulse "
               "by a fixed number of cycles",
               *walk_max >= *walk_min && *walk_min >= 1 && *walk_max <= 32);
    std::printf("  [i]    T7 bank walk and commit: %ld..%ld axis cycles "
                "(%.1f..%.1f ns at 100 MHz) over %zu pairs\n",
                *walk_min, *walk_max, 10.0 * static_cast<double>(*walk_min),
                10.0 * static_cast<double>(*walk_max), n);
}

void TdmRenderHarness::measure_the_commit_to_pin_terms(const Grade& g) {
    // T7 LATENCY - measured from REGISTERED events, never from a model.
    // The m-th crossbar valid pulse is correlated with the m-th decoded
    // frame BY COUNT; its payload is never read.
    if (!commit_cycle.empty() && !phys_valid_cycle.empty()) {
        long walk_min = 0;
        long walk_max = 0;
        measure_the_bank_term(&walk_min, &walk_max);
        // ...and the whole commit-to-pin interval, measured between two
        // REGISTERED events: the adapter's frame commit and the receiver's
        // sampling edge of that frame's slot 0 MSB. The commit that produced
        // a frame is the newest one that landed before its adoption, which is
        // drop-oldest's own rule, so the cursor is SEATED once that way and
        // then walked by the grading's own advances - counted events, never a
        // guessed alignment.
        const double kAxisPerHalf = 0.5;
        const double bit_axis0 = 2.0 * static_cast<double>(kAudDen)
                               / static_cast<double>(kAudNum);
        // WHICH COMMIT PRODUCED THIS FRAME is not a guess. The frame CDC
        // cannot deliver a committed frame to the serial side faster than its
        // own registered depth: the write pointer's gray value crosses two
        // flops and sets the empty flag (3 read edges), the prefetch read
        // enable is one more, the FIFO's registered read data and the
        // fetch-valid flag one more, and the load of the double buffer one
        // more. Six clk_tdm periods, plus slot 0's own one bit period of
        // serial position, is therefore a floor no commit closer than that can
        // have met - which seats the cursor unambiguously. After that it walks
        // by the grading's own advances, because drop-oldest consumes exactly
        // one commit per adoption plus one per counted skip.
        const double kCdcFloorAxis = 6.0 * static_cast<double>(kAudDen)
                                   / static_cast<double>(kAudNum);
        long cursor = -1;
        const double pin0 = static_cast<double>(decoded.front().half_step) * kAxisPerHalf;
        for (size_t j = 0; j < commit_cycle.size(); j++)
            if (static_cast<double>(commit_cycle[j]) <= pin0 - kCdcFloorAxis - bit_axis0)
                cursor = static_cast<long>(j);
        long tmin = 1 << 30;
    long tmax = -(1 << 30);
    long span_n = 0;
        long tail_unpaired = 0;
        long bad_interval = 0;
        for (size_t i = 0; i < decoded.size() && i < g.advances.size(); i++) {
            cursor += g.advances[i];
            if (cursor < 0 || cursor >= static_cast<long>(commit_cycle.size())) {
                ++tail_unpaired;            // the window ended, not a defect
                continue;
            }
            const double pin_axis = static_cast<double>(decoded[i].half_step) * kAxisPerHalf;
            const long d = static_cast<long>(pin_axis)
                         - commit_cycle[static_cast<size_t>(cursor)];
            if (d < 0 || d > 8000) { ++bad_interval; continue; }
            if (d < tmin) tmin = d;
            if (d > tmax) tmax = d;
            ++span_n;
        }
        if (span_n > 16) {
            // one serial frame is 256 bit periods = 512 clk_tdm cycles =
            // 512 x 1591/391 axis cycles
            const double frame_axis = 512.0 * static_cast<double>(kAudDen)
                                    / static_cast<double>(kAudNum);
            const double bit_axis = 2.0 * static_cast<double>(kAudDen)
                                  / static_cast<double>(kAudNum);
            check.that("T7 LATENCY: the commit-to-pin interval spreads by at "
                       "most one serial frame, so the delay does not ratchet",
                       static_cast<double>(tmax - tmin) <= frame_axis * 1.05);
            check.dec("T7 LATENCY: every decoded frame inside the window "
                      "paired with the commit that produced it",
                      static_cast<uint64_t>(bad_interval), 0);
            check.that("T7 LATENCY: the commit that produced a frame is at "
                       "least the CDC's own registered depth before its pin "
                       "edge", static_cast<double>(tmin) >= kCdcFloorAxis);
            std::printf("  [i]    T7 frame commit to slot 0 MSB sampling edge: "
                        "%ld..%ld axis cycles (%.3f..%.3f us) over %ld frames, "
                        "%ld past the window's end; one frame = %.3f us, one "
                        "bit period = %.4f us, CDC floor = %.1f cycles\n",
                        tmin, tmax, static_cast<double>(tmin) / 100.0,
                        static_cast<double>(tmax) / 100.0, span_n,
                        tail_unpaired, frame_axis / 100.0, bit_axis / 100.0,
                        kCdcFloorAxis);
            // THE PUBLISHED TERMS, derived from those measurements: the bank
            // walk is walk_min..walk_max, and the CDC-plus-adopt wait phi is
            // what is left after the slot's own serial position is removed.
            std::printf("  [i]    T7 published terms, measured: bank walk and "
                        "commit %.1f..%.1f ns; adopt wait phi %.3f..%.3f us "
                        "(the measured interval less slot 0's one bit period "
                        "of serial position); slot k adds %.4f us\n",
                        10.0 * static_cast<double>(walk_min),
                        10.0 * static_cast<double>(walk_max),
                        (static_cast<double>(tmin) - bit_axis) / 100.0,
                        (static_cast<double>(tmax) - bit_axis) / 100.0,
                        32.0 * bit_axis / 100.0);
            prove_each_slot_sits_at_its_own_position(bit_axis);
        } else {
            check.fail("T7 LATENCY: too few correlated frames to measure the "
                       "commit-to-pin interval");
        }
    } else {
        check.fail("T7 LATENCY: no commit or crossbar pulse was observed");
    }
}

//! T7 SLOT POSITION: slot k's MSB must sit exactly 32k bit periods after
//! slot 0's, on every decoded frame. That is what makes "slot k" a
//! POSITION on the wire rather than a label in the bank.
void TdmRenderHarness::prove_each_slot_sits_at_its_own_position(
        double bit_axis) {
    const double kAxisPerHalf = 0.5;
    long slot_pos_faults = 0;
    for (const DecodedFrame& fr : decoded) {
        for (int k = 1; k < kSlots; k++) {
            const double got =
                static_cast<double>(fr.msb_half[static_cast<size_t>(k)]
                                    - fr.msb_half[0]) * kAxisPerHalf;
            const double want = 32.0 * static_cast<double>(k) * bit_axis;
            if (got < want - 2.0 || got > want + 2.0) ++slot_pos_faults;
        }
    }
    check.dec("T7 SLOT POSITION: slot k's MSB sits exactly 32k bit periods "
              "after slot 0's, on every decoded frame",
              static_cast<uint64_t>(slot_pos_faults), 0);
}

void TdmRenderHarness::prove_the_surplus_is_drop_oldest() {
    // T14 SKIP LAW: hold the serial clock for several frame intervals while
    // the producer keeps committing, so the surplus is forced in bounded time
    // instead of waiting out the 1.96 s free-run beat. Drop-OLDEST keeps
    // prefetching the freshest committed frame, counts each overwritten one
    // and leaves the CDC near empty; drop-NEWEST would fill it, drop commits
    // as overruns and let the commit-to-pin delay ratchet upward.
    {
        const uint64_t skips0 = lane_skips();
        const uint64_t over0 = lane_over();
        feed_on = true;
        next_pdu_at = axis_cycle + 64;
        run_fed(10 * kPduPeriodCycles);
        tdm_frozen = true;
        // Two and a half frame intervals: enough that two producer commits
        // land inside one frame interval, and inside the CDC's four entries
        // so nothing is lost as an OVERRUN. A hold longer than the CDC is
        // depth-limited whatever the surplus policy is - the consumer cannot
        // drain a clock that is not running - so it would discriminate
        // nothing; that limit is recorded in docs/CHANNEL_MAP_64.md.
        run_fed(5200);
        tdm_frozen = false;
        run_fed(10 * kPduPeriodCycles);
        check.that("T14 SKIP LAW: the forced surplus was COUNTED as skips",
                   lane_skips() >= skips0 + 1);
        check.dec("T14 SKIP LAW: the CDC never filled, so no commit was "
                  "dropped as an overrun",
                  static_cast<uint64_t>(lane_over() - over0), 0);
        std::printf("  [i]    T14: skips %llu -> %llu, overruns %llu -> %llu "
                    "across a two-and-a-half-frame serial-clock hold\n",
                    static_cast<unsigned long long>(skips0),
                    static_cast<unsigned long long>(lane_skips()),
                    static_cast<unsigned long long>(over0),
                    static_cast<unsigned long long>(lane_over()));
        // ...and the delay is back inside the band it held before the hold,
        // which is what "does not ratchet" means at the pins
        decoder_reset();
        taps_reset();
        collect = true;
        run_fed(30 * kPduPeriodCycles);
        collect = false;
        if (!decoded.empty() && !commit_cycle.empty()) {
            const double kAxisPerHalf = 0.5;
            const double bit_axis = 2.0 * static_cast<double>(kAudDen)
                                  / static_cast<double>(kAudNum);
            const double cdc_floor = 6.0 * static_cast<double>(kAudDen)
                                   / static_cast<double>(kAudNum);
            const double frame_axis = 512.0 * static_cast<double>(kAudDen)
                                    / static_cast<double>(kAudNum);
            long cur = -1;
            const double pin0 =
                static_cast<double>(decoded.front().half_step) * kAxisPerHalf;
            for (size_t j = 0; j < commit_cycle.size(); j++)
                if (static_cast<double>(commit_cycle[j]) <= pin0 - cdc_floor - bit_axis)
                    cur = static_cast<long>(j);
            long worst = 0;
            if (cur >= 0) {
                const double pin_axis =
                    static_cast<double>(decoded.front().half_step) * kAxisPerHalf;
                worst = static_cast<long>(pin_axis)
                      - commit_cycle[static_cast<size_t>(cur)];
            }
            check.that("T14 SKIP LAW: the commit-to-pin delay after the hold "
                       "is still inside one frame, so it did not ratchet",
                       cur >= 0 && static_cast<double>(worst)
                                   <= frame_axis + cdc_floor + bit_axis);
            std::printf("  [i]    T14: commit-to-pin after the hold = %ld axis "
                        "cycles (%.3f us)\n", worst,
                        static_cast<double>(worst) / 100.0);
        } else {
            check.fail("T14 SKIP LAW: nothing decoded after the serial-clock "
                       "hold");
        }
        feed_on = false;
    }

}

void TdmRenderHarness::prove_a_removal_silences_only_its_own_slots() {
    // T8 REMOVE: two of the eight, and nothing else moves
    const int drop_a = 2;
    const int drop_b = 5;
    check.dec("T8 REMOVE: two mappings removed",
              static_cast<uint64_t>(map_cmd(kCmdRemoveMappings,
                                            {{kPerm[drop_a], drop_a},
                                             {kPerm[drop_b], drop_b}})), 0);
    check.dec("T8 REMOVE: their physical keys read disabled",
              render_ram(kTdmBase + drop_a) | render_ram(kTdmBase + drop_b), 0);
    const auto page2 = get_audio_map(0, 0);
    long still = 0;
    for (const auto& r : page2)
        if (r[2] == drop_a || r[2] == drop_b) ++still;
    check.dec("T8 REMOVE: GET no longer reports them",
              static_cast<uint64_t>(still), 0);
    long dac_after = 0;
    for (int k = 0; k < kI2sN; k++)
        if (render_ram(kI2sBase + k) == 0) ++dac_after;
    check.dec("T8 REMOVE: no removal aliased the pruned DAC lane",
              static_cast<uint64_t>(dac_after), kI2sN);
    // the removed slots must now render digital silence while the rest are
    // still graded against the record
    decoder_reset();
    taps_reset();
    collect = true;
    run_fed(40 * kPduPeriodCycles);
    collect = false;
    long silent = 0;
    for (const DecodedFrame& fr : decoded) {
        if ((fr.slot[static_cast<size_t>(drop_a)] == 0) &&
            (fr.slot[static_cast<size_t>(drop_b)] == 0)) ++silent;
    }
    check.that("T8 REMOVE: the two removed slots carry 24'h000000 in every "
               "decoded frame",
               !decoded.empty() && silent == static_cast<long>(decoded.size()));
    if (!decoded.empty()) {
        long start2 = -1;
        const DecodedFrame& h = decoded.front();
        for (size_t e = 0; e + 1 < inj.size() && start2 < 0; e++) {
            bool all = true;
            for (int k = 0; k < kSlots && all; k++) {
                const int s = src_of_slot(k);
                const uint32_t want = (s < 0) ? 0u : inj[e][static_cast<size_t>(s)];
                if ((h.slot[static_cast<size_t>(k)] >> 8) != want) all = false;
            }
            if (all) start2 = static_cast<long>(e);
        }
        check.that("T8 REMOVE: the six surviving slots still grade against the "
                   "injection record", start2 >= 0);
        if (start2 >= 0) {
            const Grade g2 = grade_frames(start2, "T8");
            check.dec("T8 REMOVE: identity holds for the surviving slots",
                      static_cast<uint64_t>(g2.identity_failures), 0);
        }
    }
    // put the two mappings back for the later phases
    map_cmd(kCmdAddMappings, {{kPerm[drop_a], drop_a}, {kPerm[drop_b], drop_b}});
}

void TdmRenderHarness::phase_csr() {
    std::printf("\n[CSR] the diagnostic write window, by CLUSTER key\n");
    // T10: the 0x908 write arm addresses by GLOBAL CLUSTER key and projects
    // through the generated table; the 0x910/0x914 readback addresses by
    // PHYSICAL key with no projection. On this shape the two differ by the
    // lane base, which is the asymmetry the register map documents.
    const int cluster = 4;
    const int phys = kTdmBase + cluster;
    const uint32_t before = render_ram(phys);
    csr_map_write(cluster, 0x8006u);      // en, src 0, stream 0, channel 6
    const uint32_t after = render_ram(phys);
    check.hex("T10 CSR: a write by CLUSTER key lands at the PROJECTED "
              "physical key", after, 0x86u);
    check.that("T10 CSR: the readback selector is the PHYSICAL key, so the "
               "two sides differ by the lane base",
               before != after || kTdmBase == 0);
    // restore the AECP-owned route
    csr_map_write(cluster,
                  0x8000u | static_cast<uint32_t>(src_of_slot(cluster) & 0x7));
    check.hex("T10 CSR: the route is restored", render_ram(phys),
              0x80u | static_cast<uint32_t>(src_of_slot(cluster) & 0x3F));

    // T11: an in-range cluster key whose RPHYS is INVALID. On this shape
    // every declared key is projected, so the unprojected key is one past the
    // declared block: it is out of the generated table's range, the crossbar
    // write is suppressed, and - the correction this arm exists for - the
    // AECP protocol store STILL MIRRORS an in-range CSR write, subject to the
    // existing lock and transaction gates. The store is read back through
    // GET_AUDIO_MAP, which is the authority for it.
    const int unprojected = kSlots;       // key 8: declared block is 0..7
    std::array<uint32_t, 16> ram_before{};
    for (int k = 0; k < kI2sN + kSlots; k++)
        ram_before[static_cast<size_t>(k)] = render_ram(k);
    csr_map_write(unprojected, 0x8001u);
    long ram_same = 0;
    for (int k = 0; k < kI2sN + kSlots; k++)
        if (render_ram(k) == ram_before[static_cast<size_t>(k)]) ++ram_same;
    check.dec("T11 CSR SUPPRESSION: a cluster key with no valid projection "
              "changes no render RAM word",
              static_cast<uint64_t>(ram_same), kI2sN + kSlots);
    const auto page = get_audio_map(0, 0);
    long rows_out_of_block = 0;
    for (const auto& r : page)
        if (r[2] >= kSlots) ++rows_out_of_block;
    check.dec("T11 CSR SUPPRESSION: no mapping outside this port's declared "
              "cluster block appears in the GET page",
              static_cast<uint64_t>(rows_out_of_block), 0);
    std::printf("  [i]    T11: CSR suppression is a CSR behaviour; no AECP "
                "status is asserted for it. The in-range protocol-store "
                "mirror is exercised by T11b below.\n");

    // T11b: the PRESERVED behaviour the suppression must not have changed.
    // An unlocked CSR write at an IN-RANGE cluster key writes the AECP
    // protocol store whatever its physical projection says; only the crossbar
    // write is gated by the projection. Here the key IS projected, so both
    // effects are visible and are checked independently.
    const int mirror_key = 6;
    csr_map_write(mirror_key, 0x8007u);   // stream 0, channel 7
    check.hex("T11b MIRROR: the in-range CSR write reached the render RAM",
              render_ram(kTdmBase + mirror_key), 0x87u);
    const auto page_b = get_audio_map(0, 0);
    long mirrored = 0;
    for (const auto& r : page_b)
        if (r[2] == mirror_key && r[1] == 7 && r[0] == 0) ++mirrored;
    check.dec("T11b MIRROR: the same write is visible in the AECP protocol "
              "store through GET_AUDIO_MAP",
              static_cast<uint64_t>(mirrored), 1);
    // restore
    csr_map_write(mirror_key,
                  0x8000u | static_cast<uint32_t>(src_of_slot(mirror_key) & 0x7));
    map_cmd(kCmdAddMappings, {{src_of_slot(mirror_key), mirror_key}});
}

void TdmRenderHarness::phase_reset() {
    std::printf("\n[RESET] the four-phase render epoch over reset and a "
                "stopped serial clock\n");
    // Warm the lane: pointers away from zero, a recognisable pre-reset epoch
    // in the active and prefetched banks.
    build_injection_record(400);
    feed_on = true;
    next_pdu_at = axis_cycle + 64;
    run_fed(60 * kPduPeriodCycles);
    decoder_reset();
    collect = true;
    run_fed(20 * kPduPeriodCycles);
    collect = false;
    check.that("T18 WARM: the lane was serializing real audio before the reset",
               !decoded.empty());
    std::array<uint32_t, kSlots> pre_epoch{};
    if (!decoded.empty()) pre_epoch = decoded.back().slot;
    const uint64_t epochs_before = lane_epochs();

    prove_a_stopped_clock_reset_reopens_one_epoch(pre_epoch, epochs_before);
    prove_the_lane_recovers_after_a_reset();
}

//! T18 and T21/T22: the four-phase epoch over a reset the SERIAL SIDE NEVER
//! SEES AS AN EDGE. The clock is stopped first, the datapath reset is asserted
//! and released entirely while it is stopped, and what reopens the lane when
//! the clock returns is the producer's RETAINED request, not a pulse.
void TdmRenderHarness::prove_a_stopped_clock_reset_reopens_one_epoch(
        const std::array<uint32_t, kSlots>& pre_epoch, uint64_t epochs_before) {
    feed_on = false;
    tdm_frozen = true;
    steps(200);
    const int dout_frozen = dut->tdm_dout_o;
    const uint64_t frames_frozen = lane_frames();
    // A STOPPED CLOCK DELIVERS NOTHING, and that is the property to state -
    // not that the pin is low. The serial reset is SYNCHRONOUS, so with
    // clk_tdm_i stopped it cannot take effect at all: nothing shifts, the pin
    // holds whatever level it was last launched at, and no frame is counted,
    // which is what makes a stopped clock unreadable as delivered audio. The
    // statement is made BEFORE the reset, because a reset zeroes the
    // destination side of the counter export and would answer it trivially.
    steps(4000);
    check.dec("T18 STOPPED CLOCK: nothing shifts while clk_tdm_i is stopped, "
              "so the serial pin holds its last launched level",
              static_cast<uint64_t>(dut->tdm_dout_o),
              static_cast<uint64_t>(dout_frozen));
    check.that("T18 STOPPED CLOCK: no serial frame is counted while the clock "
               "is stopped", lane_frames() == frames_frozen);
    dut->axis_resetn = 0;
    steps(400);
    // The reset is RELEASED while the clock is still stopped, so the serial
    // domain never observes it as an edge at all. What it does observe, when
    // its clock returns, is the producer's RETAINED epoch request - the whole
    // reason the handshake is a level and not a pulse.
    dut->axis_resetn = 1;
    steps(400);
    tdm_frozen = false;
    steps(4000);
    check.dec("T18 RESET: once the serial clock returns, the retained request "
              "flushes the lane and the pin is driven low",
              static_cast<uint64_t>(dut->tdm_dout_o), 0);
    decoder_reset();
    collect = true;
    steps(6000);
    collect = false;
    long nonzero = 0;
    for (const DecodedFrame& fr : decoded)
        for (int k = 0; k < kSlots; k++)
            if (fr.slot[static_cast<size_t>(k)] != 0) ++nonzero;
    check.dec("T18 RESET: every frame decoded after the clock returns is all "
              "zero until the epoch reopens",
              static_cast<uint64_t>(nonzero), 0);
    long pre_epoch_seen = 0;
    for (const DecodedFrame& fr : decoded)
        for (int k = 0; k < kSlots; k++)
            if (fr.slot[static_cast<size_t>(k)] != 0 &&
                fr.slot[static_cast<size_t>(k)] == pre_epoch[static_cast<size_t>(k)])
                ++pre_epoch_seen;
    check.dec("T18 RESET: no pre-reset sample survives the stopped-clock reset",
              static_cast<uint64_t>(pre_epoch_seen), 0);
    check.that("T18 RESET: the epoch reopened and was counted",
               lane_epochs() > epochs_before);
    std::printf("  [i]    epochs %llu -> %llu across the stopped-clock reset\n",
                static_cast<unsigned long long>(epochs_before),
                static_cast<unsigned long long>(lane_epochs()));
    check.dec("T18 RESET: the FIFO write side admitted nothing before the "
              "round trip completed", static_cast<uint64_t>(lane_over()), 0);

    // T22: a reset asserted MID-FRAME interrupts the frame in flight and that
    // serial interval is INVALID. The distinction from a graceful epoch flush
    // - which completes the frame whole - is the correction this arm carries.
    dut->axis_resetn = 0;
    steps(8);
    const long rises_at_reset = rises;
    steps(600);
    dut->axis_resetn = 1;
    decoder_reset();
    steps(8000);
    check.that("T22 HARD RESET: the interrupted interval is bounded - a fresh "
               "frame boundary is observed after the release",
               fsync_rises >= 1);
    std::printf("  [i]    T22: the reset landed %ld bclk rises into the "
                "frame; the decoder re-armed and saw %ld fsync rise(s) after "
                "release\n", rises_at_reset % kFrameBclks, fsync_rises);

    // T21: commits placed immediately before, during and after the release
    // may not reach the pins from a closed epoch.
    check.dec("T21 COMMIT AROUND RELEASE: no commit made before the epoch "
              "reopened reached the pins", static_cast<uint64_t>(nonzero), 0);

}

//! ...and the lane comes back: rebind, remap, and the first nonzero frame is a
//! POST-reset injected event.
void TdmRenderHarness::prove_the_lane_recovers_after_a_reset() {
    // ...and the lane comes back: rebind, remap, and the first nonzero frame
    // is a post-reset injected event.
    bind_listener_zero();
    route_reset();
    std::vector<std::pair<int, int>> rows;
    for (int co = 0; co < kSlots; co++)
        rows.emplace_back(kPerm[static_cast<size_t>(co)], co);
    check.dec("T18 RECOVERY: the map is programmable again after the reset",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, rows)), 0);
    build_injection_record(200);
    feed_on = true;
    next_pdu_at = axis_cycle + 64;
    run_fed(60 * kPduPeriodCycles);
    decoder_reset();
    collect = true;
    run_fed(40 * kPduPeriodCycles);
    collect = false;
    long recovered = -1;
    if (!decoded.empty()) {
        const DecodedFrame& h = decoded.front();
        for (size_t e = 0; e + 1 < inj.size() && recovered < 0; e++) {
            bool all = true;
            for (int k = 0; k < kSlots && all; k++) {
                const int s = src_of_slot(k);
                const uint32_t want = (s < 0) ? 0u : inj[e][static_cast<size_t>(s)];
                if ((h.slot[static_cast<size_t>(k)] >> 8) != want) all = false;
            }
            if (all) recovered = static_cast<long>(e);
        }
    }
    check.that("T18 RECOVERY: complete fresh frames decode after the epoch "
               "reopens", recovered >= 0);
    feed_on = false;
}

void TdmRenderHarness::phase_bind_loss() {
    std::printf("\n[BIND] the render epoch over a bind loss and a rebind\n");
    // A distinct sample epoch before the loss, so a surviving sample is
    // recognisable rather than merely plausible.
    build_injection_record(400);
    feed_on = true;
    next_pdu_at = axis_cycle + 64;
    run_fed(60 * kPduPeriodCycles);
    decoder_reset();
    collect = true;
    run_fed(20 * kPduPeriodCycles);
    collect = false;
    check.that("T23 WARM: the lane carried pre-loss audio", !decoded.empty());
    std::vector<std::array<uint32_t, kSlots>> pre_loss;
    for (const DecodedFrame& fr : decoded) pre_loss.push_back(fr.slot);
    const uint64_t epochs_before = lane_epochs();
    const long events_at_loss = injected_events;

    // Drop the bind with every mapping in place, and WITHOUT resetting.
    acmp_disconnect_rx(0x2233);
    decoder_reset();
    collect = true;
    steps(40000);
    collect = false;
    feed_on = false;
    long carried = 0;
    long frames_after_boundary = 0;
    bool boundary_passed = false;
    for (const DecodedFrame& fr : decoded) {
        bool all_zero = true;
        for (int k = 0; k < kSlots; k++)
            if (fr.slot[static_cast<size_t>(k)] != 0) all_zero = false;
        if (all_zero) { boundary_passed = true; }
        if (!boundary_passed) continue;
        ++frames_after_boundary;
        if (all_zero) continue;
        for (const auto& old : pre_loss)
            for (int k = 0; k < kSlots; k++)
                if (fr.slot[static_cast<size_t>(k)] != 0 &&
                    fr.slot[static_cast<size_t>(k)] == old[static_cast<size_t>(k)])
                    ++carried;
    }
    check.that("T23 BIND LOSS: the lane reached digital silence after the "
               "boundary", boundary_passed);
    check.dec("T23 BIND LOSS: no frame after the boundary carries a pre-loss "
              "sample in any slot", static_cast<uint64_t>(carried), 0);
    check.that("T23 BIND LOSS: the epoch closed and was counted on reopening "
               "or is still closed",
               lane_epochs() >= epochs_before);
    check.dec("T23 BIND LOSS: the adapter commit gate is closed while the "
              "epoch is",
              static_cast<uint64_t>(dut->rootp->milan_datapath__DOT__tdmr_commit_en_w),
              0);

    prove_a_rebind_carries_only_post_rebind_audio(epochs_before, events_at_loss);
}

//! T26 and T23: a map write inside the CLOSED epoch may not reach a slot, and
//! the first nonzero frame after the rebind must be a POST-rebind event routed
//! by the NEW map.
void TdmRenderHarness::prove_a_rebind_carries_only_post_rebind_audio(
        uint64_t epochs_before, long events_at_loss) {
    // T26: rewrite the map while the bind is down. The re-seeded crossbar
    // value must not reach a slot, and the first nonzero frame after the
    // rebind must be a POST-rebind event routed by the NEW map.
    std::vector<std::pair<int, int>> newrows;
    for (int co = 0; co < kSlots; co++)
        newrows.emplace_back((kPerm[static_cast<size_t>(co)] + 1) % kChans, co);
    map_cmd(kCmdAddMappings, newrows);
    decoder_reset();
    collect = true;
    steps(20000);
    collect = false;
    long leaked = 0;
    for (const DecodedFrame& fr : decoded)
        for (int k = 0; k < kSlots; k++)
            if (fr.slot[static_cast<size_t>(k)] != 0) ++leaked;
    check.dec("T26 MAP WRITE IN A CLOSED EPOCH: the re-seeded crossbar value "
              "never reaches a slot", static_cast<uint64_t>(leaked), 0);

    // Restore the bind and a disjoint injection epoch.
    probe_seen = false;
    acmp_connect_rx(0x3344);
    for (int c = 0; c < 4000 && !probe_seen; c++) step();
    acmp_play_talker_response();
    steps(3000);
    build_injection_record(200);
    injected_events = 0;
    feed_on = true;
    next_pdu_at = axis_cycle + 64;
    run_fed(60 * kPduPeriodCycles);
    decoder_reset();
    collect = true;
    run_fed(40 * kPduPeriodCycles);
    collect = false;
    check.that("T23 REBIND: the lane serializes again after the rebind",
               !decoded.empty());
    long post = -1;
    if (!decoded.empty()) {
        const DecodedFrame& h = decoded.front();
        for (size_t e = 0; e + 1 < inj.size() && post < 0; e++) {
            bool all = true;
            for (int k = 0; k < kSlots && all; k++) {
                const int s = src_of_slot(k);
                const uint32_t want = (s < 0) ? 0u : inj[e][static_cast<size_t>(s)];
                if ((h.slot[static_cast<size_t>(k)] >> 8) != want) all = false;
            }
            if (all) post = static_cast<long>(e);
        }
    }
    check.that("T23 REBIND: the first nonzero frame after the rebind is a "
               "post-rebind injected event routed by the NEW map", post >= 0);
    if (post >= 0) {
        const Grade g = grade_frames(post, "T23");
        check.dec("T23 REBIND: identity and order hold after the rebind",
                  static_cast<uint64_t>(g.identity_failures), 0);
        check.dec("T23 REBIND: every repeat is still a counted underrun",
                  static_cast<uint64_t>(g.uncounted_repeats), 0);
        check.dec("T23 REBIND: every skipped event is still covered by a "
                  "counted skip", static_cast<uint64_t>(g.uncounted_skips), 0);
    }
    check.that("T28 EPOCHS: the epoch counter advanced across the loss and "
               "recovery", lane_epochs() > epochs_before);
    std::printf("  [i]    events injected before the loss: %ld; epochs %llu -> "
                "%llu\n", events_at_loss,
                static_cast<unsigned long long>(epochs_before),
                static_cast<unsigned long long>(lane_epochs()));
    feed_on = false;
}

int TdmRenderHarness::run(int argc, char** argv) {
    for (int i = 1; i < argc; i++) {
        const std::string a = argv[i];
        if (a == "--serial-only") serial_only = true;
        else if (a == "--epoch-only") epoch_only = true;
        else if (a == "--defect-stopped-clock") { defect_stopped_clock = true; serial_only = true; }
        else if (a == "--defect-one-sample") { defect_one_sample = true; serial_only = true; corrupt_at = 400; }
    }
    const milan::tb::Model<Vmilan_datapath> model;
    dut = model.get();
    // THE ENTITY MODEL IS THE ONE THE BUILD SHIPS. The AECP uCPU serves
    // READ_DESCRIPTOR from main memory and validates the image header before
    // it enables the entity, so a leg that leaves this face unanswered gets
    // no AECP response at all - which is a stalled harness, not a verdict.
    if (!check.that("the generated entity image is on disk "
                    "(make tdm8r_aemi.bin)",
                    load_descriptor_image("tdm8r_aemi.bin")))
        return check.report();
    route_reset();
    bring_out_of_reset();

    phase_map();
    if (!epoch_only) phase_serial();
    if (!serial_only) {
        phase_csr();
        phase_reset();
        phase_bind_loss();
    }
    return check.report();
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    TdmRenderHarness harness;
    return harness.run(argc, argv);
}
