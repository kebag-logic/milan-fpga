// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_ship8_render - the 8x8/1if render lane as it ships (#584): AUDIO_MAP
// commands on the eight STREAM_PORT_INPUTs, eight bound listeners carrying
// identifiable audio, and the DECODED TDM32 pins, on milan_datapath elaborated
// at the generated 8x8 shape with the shipping render parameters.
//
// WHAT SHIPS. configs/endstation_ax7101_8x8.yaml gives STREAM_PORT_INPUT 0 one
// cluster backed by the first TDM render channel (Milan v1.2 5.3.3.8): input
// key 0 projects onto render key 2, the first key of the crossbar's TDM lane,
// and KL_tdm_render_master serializes that one slot as slot 0 of the 32-slot
// bus the capture master owns, with zero in slots 1-31. Ports 1-7 own one
// unrouted cluster each, which projects onto no render key. The elaboration's
// -G flags are not restated here: ship8_params.py derives them from the
// soc_params.json the builder emits for that config (loopback lane off, TDM32
// bus master, one render slot, eight listeners of eight wire channels, no DAC
// lane, no render filter), and ship8_geometry.hpp, written beside them, pins
// this file's stated geometry to the same values. The argv's observability
// levers (latency taps, datapath probes) prune nothing on this path and stay
// at their defaults.
//
// THE CONTROL FACE. The product is the split placement: the control CPU's
// AECP owner drives ADD/REMOVE_AUDIO_MAPPINGS into milan_datapath's edit
// window (i_ctl_edit_*). This leg elaborates the all-fabric face, where the
// protocol processor drives the same beats. milan_datapath joins the two at
// ppo_amap_edit_* (its CTRL_SPLIT_P = 1 arm assigns them from i_ctl_edit_*),
// and from there the transaction server, its validation, the map store, the
// projection, the crossbar, the render stage, the adapter and the serializer
// are one path in both placements.
//
// THE RULE THIS LEG KEEPS: nothing the DUT produces is an expected value.
//  * The injection word of stream s, wire channel c, media event e is
//    {1, s[2:0], c[2:0], e[16:0]}: fixed before any traffic, only read after,
//    and never zero, so a rendered word cannot pass for silence.
//  * The route record is set from the commands this leg issued and the
//    SUCCESS each returned, starting from D7's power-on map (stream p channel
//    0 on port p's one cluster) once that map has been read back.
//  * The pin decoder reads tdm_bclk_o, tdm_fsync_o and tdm_dout_o only: the
//    dsp_a receiver sim_tdm8_render.cpp states (fsync centred on the rise it
//    marks, slot 0's MSB on the following rise), over a 1024-bclk frame.
//  * Internal taps are timestamp and counter sources only: the PHC, the media
//    domain's event instants, and the lane's skip, underrun, epoch and stream
//    mask taps.
//
// THE CLOCKS ARE MODEL RATES, as in sim_tdm8_render: axis_clk at 100 MHz and
// clk_tdm_i at axis x 1564/1591 = 98.303 MHz, the shipping TDM32 clock
// (2 x 32 x 32 x 48 kHz) on that leg's divider plan, so the frame is the
// shipping 20.834 us. The shipping image clocks axis_clk at 50 MHz.
//
// Every PDU is stamped as a talker on the domain's clock would stamp it (#632):
// one timeline per stream, a lead of 92 frames, so each event reaches the pins
// at its presentation time and the leg grades that too.

#include "../../common/verilator_harness.hpp"
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "ship8_geometry.hpp"
#include "verilated.h"

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

namespace {

//! THE GEOMETRY UNDER TEST, stated here and pinned to the config's
constexpr int kStreams = 8;
constexpr int kChans = 8;
constexpr int kBusSlots = 32;
constexpr int kRenderSlots = 1;
static_assert(kCfgStreams == kStreams, "the 8x8 config's listener count moved");
static_assert(kCfgWireChans == kChans, "the 8x8 config's wire channel count moved");
static_assert(kCfgBusSlots == kBusSlots, "the 8x8 config's TDM bus width moved");
static_assert(kCfgRenderSlots == kRenderSlots, "the 8x8 config's render lane width moved");
static_assert(kCfgLoopback == 0, "the 8x8 config now builds the loopback lane");
static_assert(kCfgDacLane == 0, "the 8x8 config now builds the DAC lane");

constexpr int kAxiGuardCycles = 2048;
constexpr int kEvents = 6;
constexpr size_t kPayloadBytes = static_cast<size_t>(kChans) * kEvents * 4;
constexpr size_t kFrameBytes = 14 + 24 + kPayloadBytes;
//! six events per class-A PDU at 48 kHz on the 100 MHz model axis clock
constexpr long kPduPeriodCycles = 12500;
constexpr double kModelNsPerAxis = 10.0;
//! clk_tdm_i = axis_clk x 1564/1591: four times sim_tdm8_render's TDM8 plan
constexpr long kAudNum = 1564;
constexpr long kAudDen = 1591;
constexpr int kSlotBits = 32;
constexpr int kFrameBclks = kBusSlots * kSlotBits;
//! the crossbar's TDM lane, its first key, and the whole physical vector:
//! the DAC lane (keys 0, 1) and the TDM lane (keys 2..9). Stated as the law
//! under test, never read back from the DUT.
constexpr int kTdmBase = 2;
constexpr int kPhysKeys = 10;
//! #632: a feed's first event is stamped this many frames past the domain's
//! latest event, and every event must reach its pins inside IEEE 1722-2016
//! 10.8's +/-5 % of Ps of its presentation time
constexpr long kLeadFrames = 92;
constexpr double kPresBandFrac = 0.05;
//! PDUs from a feed's start, or from a rebind, to its first rendered event,
//! with margin; and the PDUs a map change takes to reach the pins
constexpr long kLeadPdus = kLeadFrames / kEvents + 4;
constexpr long kSettlePdus = 4;
//! a graded window: 20 PDUs, 120 media events
constexpr long kWindowPdus = 20;
constexpr long kMinFrames = 100;
constexpr const char* kAemImage = "ship8_aemi.bin";

constexpr uint32_t kMarker = 0x800000u;
constexpr uint32_t kEventMask = 0x1FFFFu;
//! the injection word: {1, stream, channel, event}
constexpr uint32_t sample_word(int s, int c, long e) {
    return kMarker | (static_cast<uint32_t>(s & 7) << 20) |
           (static_cast<uint32_t>(c & 7) << 17) |
           (static_cast<uint32_t>(e) & kEventMask);
}
//! the render RAM's live entry for an AVB listener channel (CHANNEL_MAP_64
//! section 3): {EN, SRC = 0, STREAM, CHANNEL}
constexpr uint32_t render_entry(int s, int c) {
    return 0x80u | (static_cast<uint32_t>(s & 7) << 3) | static_cast<uint32_t>(c & 7);
}

//! one decoded serial frame: the 32 slot words as the pins delivered them,
//! and the PHC at slot 0's MSB sampling edge
struct DecodedFrame {
    std::array<uint32_t, kBusSlots> slot{};
    double msb0_phc = 0.0;
};

//! one graded window
struct Window {
    long frames = 0;
    long tail_nonzero = 0;   //! frames with a nonzero bit in slots 1..31
    long pad_nonzero = 0;    //! frames whose slot-0 pad byte is not zero
    long silent = 0;         //! frames whose slot 0 is zero
    long rendered = 0;       //! frames whose slot 0 is the routed source's word
    long wrong_source = 0;   //! frames whose slot 0 is anything else
    long reordered = 0;      //! an event at or before its predecessor, uncounted
    long skipped = 0;        //! events between two rendered ones
    long repeats = 0;
    long first_event = -1;
    long last_event = -1;
    double pres_max = 0.0;   //! the largest presentation error, ns
    long pres_n = 0;
    long gap_faults = 0;
    long framing_faults = 0;
    long fsync_rises = 0;
    uint64_t skips = 0;      //! the lane's counted skips over the window
    uint64_t unders = 0;     //! ...and counted underruns
};

class Ship8Harness {
 public:
    int run();

 private:
    Vmilan_datapath* dut = nullptr;
    milan::tb::Checker check{"ship8_render"};

    // ---------------------------------------------------------------- //
    //  Clocks                                                           //
    // ---------------------------------------------------------------- //
    long acc = 0;
    int aud = 0;
    long axis_cycle = 0;

    void half() {
        acc += kAudNum;
        if (acc >= kAudDen) { acc -= kAudDen; aud ^= 1; }
        dut->clk_audio_i = aud;
        dut->clk_tdm_i = aud;
    }
    //! the memory models advance in the low phase, as every milan_dp leg's do
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
        observe_domain();
        observe_streams();
        observe();
        sniff_probe();
        drp_respond();
    }
    int drp_lat = 0;
    void drp_respond() {
        dut->i_mmcm_drp_rdy = 0;
        if (drp_lat > 0 && --drp_lat == 0) dut->i_mmcm_drp_rdy = 1;
        if (dut->o_mmcm_drp_en) drp_lat = 3;
        dut->i_mmcm_drp_do = 0;
    }

    // ---------------------------------------------------------------- //
    //  The processor's two memory faces: the entity image the build     //
    //  ships, and its response region                                   //
    // ---------------------------------------------------------------- //
    static constexpr uint32_t kDescBase = 0x20000000u;
    static constexpr uint32_t kRespBase = 0x20100000u;
    std::vector<uint8_t> desc_img;
    long desc_requests = 0;
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

    // ---------------------------------------------------------------- //
    //  THE PIN DECODER: three pins, nothing else                        //
    // ---------------------------------------------------------------- //
    int p_bclk = 0;
    int p_fsync = 0;
    bool armed = false;
    int pend = 0;
    bool framed = false;
    int q = 0;
    long rises = 0;
    long last_fsync_rise = -1;
    long fsync_rises = 0;
    long gap_faults = 0;
    long framing_faults = 0;
    std::array<uint32_t, kBusSlots> word{};
    double msb0_phc = 0.0;
    bool collect = false;
    std::vector<DecodedFrame> decoded;

    void observe() {
        const int b = dut->tdm_bclk_o;
        const int f = dut->tdm_fsync_o;
        const int d = dut->tdm_dout_o;
        if (!(b && !p_bclk)) { p_bclk = b; return; }
        p_bclk = b;
        ++rises;
        if (f && !p_fsync && armed) {
            if (last_fsync_rise >= 0 && rises - last_fsync_rise != kFrameBclks) ++gap_faults;
            last_fsync_rise = rises;
            ++fsync_rises;
            pend = 1;
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
        if (slot == 0 && bit == 0) msb0_phc = phc();
        word[static_cast<size_t>(slot)] =
            (word[static_cast<size_t>(slot)] << 1) | static_cast<uint32_t>(d);
        if (slot == kBusSlots - 1 && bit == kSlotBits - 1 && collect) {
            DecodedFrame fr;
            fr.slot = word;
            fr.msb0_phc = msb0_phc;
            decoded.push_back(fr);
        }
        if (++q == kFrameBclks) q = 0;
    }
    void decoder_reset() {
        armed = false; pend = 0; framed = false; q = 0;
        rises = 0; last_fsync_rise = -1; fsync_rises = 0;
        gap_faults = 0; framing_faults = 0;
        word.fill(0);
        decoded.clear();
        p_bclk = dut->tdm_bclk_o;
        p_fsync = dut->tdm_fsync_o;
    }

    // ---------------------------------------------------------------- //
    //  Taps: timestamps and counters only                               //
    // ---------------------------------------------------------------- //
    double phc() const {
        return static_cast<double>(dut->rootp->milan_datapath__DOT__ptp_now_w);
    }
    uint64_t lane_unders() const { return dut->rootp->milan_datapath__DOT__tdmr_underruns_w; }
    uint64_t lane_skips() const { return dut->rootp->milan_datapath__DOT__tdmr_skips_w; }
    uint64_t lane_epochs() const { return dut->rootp->milan_datapath__DOT__tdmr_epochs_w; }
    uint64_t lane_streams() const {
        return dut->rootp->milan_datapath__DOT__tdmr_lane_streams_w;
    }
    uint64_t bound_streams() const { return dut->rootp->milan_datapath__DOT__strtbl_en_w; }
    //! the classification table's stream id for entry s
    uint64_t table_sid(int s) const {
        const auto& flat = dut->rootp->milan_datapath__DOT__strtbl_sid_w;
        return (static_cast<uint64_t>(flat[static_cast<size_t>(2 * s + 1)]) << 32) |
               flat[static_cast<size_t>(2 * s)];
    }
    //! PDUs the receive monitor accepted, and events the render stage
    //! presented, per stream: counters, reported beside each window
    std::array<long, kStreams> accepts{};
    std::array<long, kStreams> pops{};
    void observe_streams() {
        if (dut->rootp->milan_datapath__DOT__avtprx_accept_p) {
            const size_t i = static_cast<size_t>(dut->rootp->milan_datapath__DOT__avtprx_idx);
            if (i < accepts.size()) ++accepts[i];
        }
        const uint32_t popped = dut->rootp->milan_datapath__DOT__rq_pop_p_w;
        for (int k = 0; k < kStreams; k++)
            if ((popped >> k) & 1u) ++pops[static_cast<size_t>(k)];
    }

    // ---------------------------------------------------------------- //
    //  THE PRESENTATION INSTRUMENT (#632): the domain's media events off  //
    //  its public instant tap, one timeline per stream                    //
    // ---------------------------------------------------------------- //
    uint64_t dom_ns_last = 0;
    //! the frame period in PHC ns on this model's clock plan
    const double ps_phc = 2.0 * kFrameBclks * static_cast<double>(kAudDen) /
                          static_cast<double>(kAudNum) * kModelNsPerAxis;
    std::array<bool, kStreams> anchored{};
    std::array<double, kStreams> anchor_ns{};
    std::array<long, kStreams> anchor_ord{};
    std::array<std::vector<double>, kStreams> pt_ns;

    void observe_domain() {
        dom_ns_last = dut->rootp->milan_datapath__DOT__dom_ns_w;
    }
    double stamp_the_event(int s, long ord) {
        const size_t i = static_cast<size_t>(s);
        double pt = anchor_ns[i] + static_cast<double>(ord - anchor_ord[i]) * ps_phc;
        const double floor_ns = static_cast<double>(dom_ns_last) + 0.5 * kLeadFrames * ps_phc;
        if (!anchored[i] || pt < floor_ns) {
            anchored[i] = true;
            anchor_ord[i] = ord;
            anchor_ns[i] = static_cast<double>(dom_ns_last) + kLeadFrames * ps_phc;
            pt = anchor_ns[i];
        }
        return pt;
    }
    void record_pt(int s, long ord, double pt) {
        auto& v = pt_ns[static_cast<size_t>(s)];
        if (static_cast<long>(v.size()) <= ord) v.resize(static_cast<size_t>(ord) + 1, -1.0);
        v[static_cast<size_t>(ord)] = pt;
    }
    double pt_of(int s, long ord) const {
        const auto& v = pt_ns[static_cast<size_t>(s)];
        return (ord >= 0 && ord < static_cast<long>(v.size())) ? v[static_cast<size_t>(ord)] : -1.0;
    }
    //! slot 0's MSB is one bit period after its frame's instant
    double slot0_offset() const { return ps_phc / static_cast<double>(kFrameBclks); }

    // ---------------------------------------------------------------- //
    //  AXI4-Lite and MAC ingress                                        //
    // ---------------------------------------------------------------- //
    void axi_write(uint16_t a, uint32_t d) {
        dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
        dut->s_axi_wdata = d; dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
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
    void inject(const uint8_t* f, size_t len) {
        std::vector<uint64_t> beats;
        for (size_t bt = 0; bt < (len + 7) / 8; bt++) {
            uint64_t v = 0;
            for (size_t j = 0; j < 8; j++)
                if (bt * 8 + j < len) v |= static_cast<uint64_t>(f[bt * 8 + j]) << (8 * j);
            beats.push_back(v);
        }
        size_t idx = 0;
        for (int c = 0; c < 1500 && idx < beats.size() + 8; c++) {
            if (idx < beats.size()) {
                dut->s_axis_mac_rx_tdata = beats[idx];
                dut->s_axis_mac_rx_tkeep = 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast = (idx == beats.size() - 1);
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
    //  THE EIGHT TALKER STREAMS. Stream s is listener s's, each with its  //
    //  own destination address, stream id, sequence and event cursor.    //
    // ---------------------------------------------------------------- //
    static std::array<uint8_t, 8> sid_of(int s) {
        return {0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, static_cast<uint8_t>(2 * s)};
    }
    static std::array<uint8_t, 6> dmac_of(int s) {
        return {0x91, 0xE0, 0xF0, 0x00, 0x2A, static_cast<uint8_t>(0x02 + 2 * s)};
    }
    unsigned feed_mask = 0;
    long next_pdu_at = 0;
    std::array<uint8_t, kStreams> wire_seq{};
    std::array<long, kStreams> injected{};

    void send_pdu(int s) {
        uint8_t f[kFrameBytes];
        memset(f, 0, sizeof f);
        const auto dmac = dmac_of(s);
        memcpy(f, dmac.data(), 6);
        const uint8_t src[6] = {0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
        memcpy(f + 6, src, 6);
        f[12] = 0x22; f[13] = 0xF0;
        f[14] = 0x02;                                // AAF
        f[15] = 0x81;                                // sv, tv
        f[16] = wire_seq[static_cast<size_t>(s)]++;
        const auto sid = sid_of(s);
        memcpy(f + 18, sid.data(), 8);
        const long base = injected[static_cast<size_t>(s)];
        const double ts = stamp_the_event(s, base);
        const uint32_t ts32 = static_cast<uint32_t>(static_cast<uint64_t>(std::llround(ts)));
        f[26] = static_cast<uint8_t>(ts32 >> 24); f[27] = static_cast<uint8_t>(ts32 >> 16);
        f[28] = static_cast<uint8_t>(ts32 >> 8);  f[29] = static_cast<uint8_t>(ts32);
        for (int k = 0; k < kEvents; k++) record_pt(s, base + k, ts + k * ps_phc);
        f[30] = 0x02;                                // INT32
        f[31] = static_cast<uint8_t>(0x05 << 4);     // 48 kHz
        f[32] = static_cast<uint8_t>(kChans);
        f[33] = 32;
        f[34] = static_cast<uint8_t>(kPayloadBytes >> 8);
        f[35] = static_cast<uint8_t>(kPayloadBytes & 0xFF);
        for (int k = 0; k < kEvents; k++)
            for (int c = 0; c < kChans; c++) {
                const uint32_t v = sample_word(s, c, base + k);
                const size_t o = 38 + 4 * (static_cast<size_t>(k) * kChans + static_cast<size_t>(c));
                f[o] = static_cast<uint8_t>(v >> 16);
                f[o + 1] = static_cast<uint8_t>(v >> 8);
                f[o + 2] = static_cast<uint8_t>(v);
                f[o + 3] = 0;
            }
        injected[static_cast<size_t>(s)] += kEvents;
        inject(f, kFrameBytes);
    }
    //! one axis cycle, the running streams served first: a talker does not
    //! pause while this leg issues commands
    void step() {
        if (feed_mask != 0 && axis_cycle >= next_pdu_at) {
            for (int s = 0; s < kStreams; s++)
                if ((feed_mask >> s) & 1u) send_pdu(s);
            next_pdu_at += kPduPeriodCycles;
            return;
        }
        lo();
        hi();
    }
    void steps(long n) { while (n--) step(); }
    void run_pdus(long n) {
        const long stop = axis_cycle + n * kPduPeriodCycles;
        while (axis_cycle < stop) step();
    }
    void start_the_feeds() {
        anchored.fill(false);
        feed_mask = (1u << kStreams) - 1u;
        next_pdu_at = axis_cycle + 64;
    }

    // ---------------------------------------------------------------- //
    //  THE ROUTE RECORD: issued commands only                           //
    // ---------------------------------------------------------------- //
    //! the mapping each port's one cluster holds, {stream, channel}, or
    //! {-1, -1}; port 0's is the one the lane renders
    std::array<std::array<int, 2>, kStreams> held{};
    void hold_power_on() {
        for (int p = 0; p < kStreams; p++) held[static_cast<size_t>(p)] = {p, 0};
    }

    // ---------------------------------------------------------------- //
    //  AECP command face                                                //
    // ---------------------------------------------------------------- //
    static constexpr uint16_t kCmdGetAudioMap = 43;
    static constexpr uint16_t kCmdAddMappings = 44;
    static constexpr uint16_t kCmdRemoveMappings = 45;
    static constexpr uint16_t kDescStreamPortIn = 0x000E;
    static constexpr long kSuccess = 0;
    static constexpr long kBadArguments = 7;
    uint16_t aecp_seq = 0x5840;

    std::vector<uint8_t> aecp_request(uint16_t cmd, uint16_t sq, const std::vector<uint8_t>& pl) {
        const size_t flen = (38 + pl.size() < 60) ? 60 : 38 + pl.size();
        std::vector<uint8_t> f(flen, 0);
        const uint8_t cmac[6] = {0x68, 0x05, 0xCA, 0x95, 0xB2, 0xD1};
        memcpy(f.data() + 6, cmac, 6);
        f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFB; f[15] = 0x00;
        const uint16_t cdl = static_cast<uint16_t>(12 + pl.size());
        f[16] = static_cast<uint8_t>((cdl >> 8) & 0x7);
        f[17] = static_cast<uint8_t>(cdl);
        const uint8_t teid[8] = {0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x01};
        memcpy(f.data() + 18, teid, 8);
        const uint8_t ceid[8] = {0x68, 0x05, 0xCA, 0xFF, 0xFE, 0x95, 0xB2, 0xD1};
        memcpy(f.data() + 26, ceid, 8);
        f[34] = static_cast<uint8_t>(sq >> 8); f[35] = static_cast<uint8_t>(sq);
        f[36] = static_cast<uint8_t>((cmd >> 8) & 0x7F);
        f[37] = static_cast<uint8_t>(cmd);
        for (size_t i = 0; i < pl.size(); i++) f[38 + i] = pl[i];
        return f;
    }
    std::vector<uint8_t> await_aecp(int cyc = 200000) {
        std::vector<uint8_t> cur;
        std::vector<uint8_t> resp;
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
                    const bool solicited = is_aecp && (cur[15] & 0xF) == 1 && (cur[36] & 0x80) == 0;
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
    //! One ADD or REMOVE of one {stream, stream_channel, cluster_offset} row
    //! on STREAM_PORT_INPUT `port`. The route record follows a SUCCESS only.
    long map_cmd(uint16_t cmd, int port, int stream, int chan, int cluster = 0) {
        std::vector<uint8_t> pl = {
            static_cast<uint8_t>(kDescStreamPortIn >> 8), static_cast<uint8_t>(kDescStreamPortIn),
            static_cast<uint8_t>(port >> 8), static_cast<uint8_t>(port),
            0x00, 0x01, 0x00, 0x00,
            0x00, static_cast<uint8_t>(stream), 0x00, static_cast<uint8_t>(chan),
            0x00, static_cast<uint8_t>(cluster), 0x00, 0x00};
        const long st = aecp_status(aecp_xact(cmd, pl));
        if (st == kSuccess && cluster == 0)
            held[static_cast<size_t>(port)] =
                (cmd == kCmdAddMappings) ? std::array<int, 2>{stream, chan} : std::array<int, 2>{-1, -1};
        return st;
    }
    //! GET_AUDIO_MAP page 0, as {stream, stream_channel, cluster_offset} rows
    std::vector<std::array<int, 3>> get_audio_map(int port, long* number_of_maps) {
        const std::vector<uint8_t> pl = {
            static_cast<uint8_t>(kDescStreamPortIn >> 8), static_cast<uint8_t>(kDescStreamPortIn),
            static_cast<uint8_t>(port >> 8), static_cast<uint8_t>(port),
            0x00, 0x00, 0x00, 0x00};
        const auto r = aecp_xact(kCmdGetAudioMap, pl);
        std::vector<std::array<int, 3>> rows;
        *number_of_maps = -1;
        if (aecp_status(r) != kSuccess || r.size() < 50) return rows;
        *number_of_maps = (static_cast<long>(r[44]) << 8) | r[45];
        const unsigned n = (static_cast<unsigned>(r[46]) << 8) | r[47];
        if (r.size() < 50 + 8 * static_cast<size_t>(n)) return rows;
        for (unsigned i = 0; i < n; i++) {
            const size_t o = 50 + 8 * static_cast<size_t>(i);
            rows.push_back({(r[o] << 8) | r[o + 1], (r[o + 2] << 8) | r[o + 3],
                            (r[o + 4] << 8) | r[o + 5]});
        }
        return rows;
    }

    //! the render RAM word at a PHYSICAL render key, through the CSR
    //! crossbar window: 0xFFFFFFFF when the snapshot is not valid
    uint32_t render_ram(int phys_key) {
        constexpr uint16_t kChmapSel = 0x904;
        constexpr uint16_t kChmapSnap = 0x910;
        constexpr uint16_t kChmapLoop = 0x914;
        axi_write(kChmapSel, static_cast<uint32_t>(phys_key));
        axi_write(kChmapSnap, 1);
        for (int g = 0; g < 64; g++)
            if ((axi_read(kChmapSnap) & 1) == 0) break;
        const uint32_t v = axi_read(kChmapLoop);
        if (((v >> 26) & 1) == 0) return 0xFFFFFFFFu;
        return v & 0xFF;
    }
    std::array<uint32_t, kPhysKeys> render_vector() {
        std::array<uint32_t, kPhysKeys> v{};
        for (int k = 0; k < kPhysKeys; k++) v[static_cast<size_t>(k)] = render_ram(k);
        return v;
    }
    //! the physical vector the route record implies: port 0's one cluster on
    //! render key 2, every other key empty
    std::array<uint32_t, kPhysKeys> expected_vector() const {
        std::array<uint32_t, kPhysKeys> v{};
        const auto& r = held[0];
        if (r[0] >= 0) v[kTdmBase] = render_entry(r[0], r[1]);
        return v;
    }

    // ---------------------------------------------------------------- //
    //  ACMP: the bind ladder and the unbind                             //
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
    static void acmp_head(uint8_t* f, uint8_t msg_type, int listener) {
        const uint8_t mc[6] = {0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
        memcpy(f, mc, 6);
        f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFC; f[15] = msg_type;
        f[16] = 0x00; f[17] = 44;
        for (int i = 26; i < 34; i++) f[i] = static_cast<uint8_t>(i);
        const uint8_t tk[8] = {0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x02};
        memcpy(f + 34, tk, 8);
        const uint8_t ls[8] = {0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x01};
        memcpy(f + 42, ls, 8);
        f[51] = static_cast<uint8_t>(listener);      // talker_unique_id: stream s is talker s's
        f[53] = static_cast<uint8_t>(listener);      // listener_unique_id
    }
    void acmp_send(uint8_t msg_type, int listener, uint16_t seq, bool from_talker) {
        uint8_t f[72];
        memset(f, 0, sizeof f);
        acmp_head(f, msg_type, listener);
        const uint8_t csrc[6] = {0x68, 0x05, 0xCA, 0x95, 0xB2, 0xD1};
        const uint8_t tsrc[6] = {0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
        memcpy(f + 6, from_talker ? tsrc : csrc, 6);
        if (msg_type != 0x06) {
            const auto sid = sid_of(listener);
            memcpy(f + 18, sid.data(), 8);
        }
        if (from_talker) {
            const auto dmac = dmac_of(listener);
            memcpy(f + 54, dmac.data(), 6);
        }
        f[62] = static_cast<uint8_t>(seq >> 8); f[63] = static_cast<uint8_t>(seq);
        inject(f, 70);
    }
    //! every controller command carries its own sequence id
    uint16_t acmp_seq = 0x6600;
    //! BIND_RX, the harvested PROBE_TX, a played CONNECT_TX_RESPONSE
    void bind(int listener, const char* tag) {
        char what[160];
        probe_seen = false;
        acmp_send(0x06, listener, acmp_seq++, false);
        for (int c = 0; c < 4000 && !probe_seen; c++) step();
        std::snprintf(what, sizeof what, "%s: listener %d launched a PROBE_TX at its talker",
                      tag, listener);
        check.dec(what, probe_seen ? 1 : 0, 1);
        acmp_send(0x01, listener, probe_seq, true);
        steps(3000);
    }
    //! DISCONNECT_RX alone drops the bind: the bind fall the render epoch watches
    void unbind(int listener) {
        acmp_send(0x08, listener, acmp_seq++, false);
        steps(3000);
    }

    // ---------------------------------------------------------------- //
    //  Windows                                                          //
    // ---------------------------------------------------------------- //
    Window decode_a_window(long pdus, int want_stream, int want_chan);
    void prove_a_rendering_window(const Window& w, const char* tag, int s, int c);
    void prove_a_silent_window(const Window& w, const char* tag);
    void report(const Window& w, const char* tag) const;

    void bring_out_of_reset();
    void boot_the_entity();
    void provision_the_listener_contexts(const char* tag);
    void prove_the_power_on_map(const char* tag);
    void prove_the_store_and_the_projection(const char* tag);
    void phase_power_on();
    void phase_routes();
    void phase_unrouted_ports();
    void phase_remove();
    void phase_bind_freshness();
    void phase_reset();
};

// ====================================================================== //

bool Ship8Harness::load_descriptor_image(const char* path) {
    std::FILE* f = std::fopen(path, "rb");
    if (f == nullptr) return false;
    uint8_t buf[4096];
    size_t n = 0;
    while ((n = std::fread(buf, 1, sizeof buf, f)) > 0) desc_img.insert(desc_img.end(), buf, buf + n);
    std::fclose(f);
    return !desc_img.empty();
}

void Ship8Harness::bring_out_of_reset() {
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->m_axis_mac_tx_tready = 1;
    dut->i_mac_speed = 0b10; dut->i_link_up = 1; dut->i_full_duplex = 1;
    steps(64);
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    steps(256);
    //! #839: the station MAC pair written, as configure_fabric() writes it
    axi_write(0x108, 0x0); axi_write(0x10C, 0x0);
}

//! the entity identity, the boot restore walk and the enable, in the
//! firmware's order (sim_tdm8_render.cpp boot_the_entity)
void Ship8Harness::boot_the_entity() {
    constexpr uint16_t kAdpCtrl = 0x600;
    constexpr uint16_t kAdpEidLo = 0x604;
    constexpr uint16_t kAdpEidHi = 0x608;
    constexpr uint16_t kPpCtrl = 0x920;
    constexpr uint16_t kPpStat = 0x924;
    axi_write(kAdpEidHi, 0x020000FF);
    axi_write(kAdpEidLo, 0xFE000001);
    axi_write(kPpCtrl, axi_read(kPpCtrl) | 0x2u);
    uint32_t done = 0;
    for (int r = 0; r < 400 && done == 0; r++) {
        steps(64);
        done = (axi_read(kPpStat) >> 2) & 1u;
    }
    check.dec("BOOT: PP_STAT[2] the restore walk sequenced", done, 1);
    axi_write(kAdpCtrl, 0x00001F01);
    steps(2000);
}

//! THE LISTENER CONTEXTS. Stream 0's current format reaches the receive
//! monitor through the legacy fmt0 path; streams 1-7 are served from the
//! per-stream LCTX, which the firmware provisions through the 0x800 window,
//! as sim_tdm8_render.cpp's [MULTI] phase and the NxN legs do. The words are
//! the format the builder's entity overlay declares for every AAF
//! STREAM_INPUT (kCfgListenerFormat, read by ship8_params.py), and a CTRL
//! commit with no staged stream id provisions that format and nothing else.
void Ship8Harness::provision_the_listener_contexts(const char* tag) {
    constexpr uint16_t kStrmSel = 0x800;
    constexpr uint16_t kSwCtrl = 0x810;
    constexpr uint16_t kSwFmtLo = 0x824;
    constexpr uint16_t kSwFmtHi = 0x828;
    const uint32_t lo_word = static_cast<uint32_t>(kCfgListenerFormat);
    const uint32_t hi_word = static_cast<uint32_t>(kCfgListenerFormat >> 32);
    long read_back = 0;
    for (int s = 1; s < kStreams; s++) {
        axi_write(kStrmSel, static_cast<uint32_t>(s));
        axi_write(kSwFmtLo, lo_word);
        axi_write(kSwFmtHi, hi_word);
        axi_write(kSwCtrl, 0x1);
        if (axi_read(kSwFmtHi) == hi_word) ++read_back;
    }
    char what[160];
    std::snprintf(what, sizeof what, "%s: streams 1-7's listener format reads back out of the LCTX", tag);
    check.dec(what, static_cast<uint64_t>(read_back), kStreams - 1);
}

Window Ship8Harness::decode_a_window(long pdus, int want_stream, int want_chan) {
    Window w;
    const uint64_t skips0 = lane_skips();
    const uint64_t unders0 = lane_unders();
    decoder_reset();
    collect = true;
    run_pdus(pdus);
    collect = false;
    w.skips = lane_skips() - skips0;
    w.unders = lane_unders() - unders0;
    w.gap_faults = gap_faults;
    w.framing_faults = framing_faults;
    w.fsync_rises = fsync_rises;
    long prev = -1;
    for (const DecodedFrame& fr : decoded) {
        ++w.frames;
        bool tail = false;
        for (int k = 1; k < kBusSlots; k++)
            if (fr.slot[static_cast<size_t>(k)] != 0) tail = true;
        if (tail) ++w.tail_nonzero;
        const uint32_t raw = fr.slot[0];
        if ((raw & 0xFFu) != 0) ++w.pad_nonzero;
        const uint32_t v = raw >> 8;
        if (v == 0) { ++w.silent; continue; }
        const bool ours = want_stream >= 0 && (v & kMarker) != 0 &&
                          static_cast<int>((v >> 20) & 7u) == want_stream &&
                          static_cast<int>((v >> 17) & 7u) == want_chan;
        if (!ours) {
            if (++w.wrong_source <= 4)
                std::printf("  [i]    frame %ld slot 0 carries %06X (route stream %d channel %d)\n",
                            w.frames - 1, v, want_stream, want_chan);
            continue;
        }
        ++w.rendered;
        const long ev = static_cast<long>(v & kEventMask);
        if (w.first_event < 0) w.first_event = ev;
        w.last_event = ev;
        if (prev >= 0) {
            if (ev == prev) ++w.repeats;
            else if (ev < prev) ++w.reordered;
            else w.skipped += ev - prev - 1;
        }
        prev = ev;
        const double pt = pt_of(want_stream, ev);
        if (pt >= 0.0) {
            w.pres_max = std::max(w.pres_max, std::fabs(fr.msb0_phc - slot0_offset() - pt));
            ++w.pres_n;
        }
    }
    return w;
}

void Ship8Harness::report(const Window& w, const char* tag) const {
    std::printf("  [i]    %s: bound %02llX, lane streams %02llX; accepted PDUs / presented events per "
                "stream:", tag, static_cast<unsigned long long>(bound_streams()),
                static_cast<unsigned long long>(lane_streams()));
    for (int k = 0; k < kStreams; k++)
        std::printf(" %ld/%ld", accepts[static_cast<size_t>(k)], pops[static_cast<size_t>(k)]);
    std::printf("\n");
    std::printf("  [i]    %s: %ld frames, slot 0 rendered %ld silent %ld other %ld, events %ld..%ld, "
                "%ld skipped (%llu counted) %ld repeated (%llu counted), presentation max %.1f ns "
                "over %ld events (band %.1f)\n",
                tag, w.frames, w.rendered, w.silent, w.wrong_source, w.first_event, w.last_event,
                w.skipped, static_cast<unsigned long long>(w.skips), w.repeats,
                static_cast<unsigned long long>(w.unders), w.pres_max, w.pres_n,
                kPresBandFrac * ps_phc);
}

void Ship8Harness::prove_a_rendering_window(const Window& w, const char* tag, int s, int c) {
    char what[220];
    report(w, tag);
    std::snprintf(what, sizeof what, "%s FRAMING: fsync every 1024 bclk rises and at position 0, "
                  "over at least %ld frames", tag, kMinFrames);
    check.that(what, w.gap_faults == 0 && w.framing_faults == 0 && w.frames >= kMinFrames);
    std::snprintf(what, sizeof what, "%s: slot 0 carries stream %d channel %d in every frame", tag, s, c);
    check.dec(what, static_cast<uint64_t>(w.rendered), static_cast<uint64_t>(w.frames));
    std::snprintf(what, sizeof what, "%s: no other source and no silence in slot 0", tag);
    check.dec(what, static_cast<uint64_t>(w.wrong_source + w.silent), 0);
    std::snprintf(what, sizeof what, "%s: slots 1-31 carry zero in every frame", tag);
    check.dec(what, static_cast<uint64_t>(w.tail_nonzero), 0);
    std::snprintf(what, sizeof what, "%s: slot 0 is 24-in-32, its pad byte zero", tag);
    check.dec(what, static_cast<uint64_t>(w.pad_nonzero), 0);
    std::snprintf(what, sizeof what, "%s: events in order, each skip and repeat counted by the lane", tag);
    check.that(what, w.reordered == 0 && static_cast<uint64_t>(w.skipped) <= w.skips &&
                     static_cast<uint64_t>(w.repeats) <= w.unders);
    std::snprintf(what, sizeof what, "%s: every rendered event at its presentation time (+/-5%% Ps, #632)",
                  tag);
    check.that(what, w.pres_n == w.rendered && w.pres_max <= kPresBandFrac * ps_phc);
}

void Ship8Harness::prove_a_silent_window(const Window& w, const char* tag) {
    char what[200];
    report(w, tag);
    std::snprintf(what, sizeof what, "%s FRAMING: the bus keeps framing, over at least %ld frames",
                  tag, kMinFrames);
    check.that(what, w.gap_faults == 0 && w.framing_faults == 0 && w.frames >= kMinFrames);
    std::snprintf(what, sizeof what, "%s: all 32 slots are digital silence in every frame", tag);
    check.that(what, w.silent == w.frames && w.tail_nonzero == 0 && w.pad_nonzero == 0);
}

//! the AECP store (GET_AUDIO_MAP on every port) and the render RAM's
//! physical vector, each against the route record
void Ship8Harness::prove_the_store_and_the_projection(const char* tag) {
    char what[200];
    long agree = 0;
    for (int p = 0; p < kStreams; p++) {
        long nmaps = -1;
        const auto page = get_audio_map(p, &nmaps);
        const auto& r = held[static_cast<size_t>(p)];
        const bool want_row = r[0] >= 0;
        const bool ok = nmaps == 1 &&
                        (want_row ? (page.size() == 1 && page[0][0] == r[0] && page[0][1] == r[1] &&
                                     page[0][2] == 0)
                                  : page.empty());
        if (ok) ++agree;
        else std::printf("  [i]    %s: port %d reads %zu rows (want %s stream %d channel %d)\n",
                         tag, p, page.size(), want_row ? "" : "none,", r[0], r[1]);
    }
    std::snprintf(what, sizeof what, "%s: GET_AUDIO_MAP on all eight ports reads the issued route record",
                  tag);
    check.dec(what, static_cast<uint64_t>(agree), kStreams);
    const auto got = render_vector();
    const auto want = expected_vector();
    long same = 0;
    for (int k = 0; k < kPhysKeys; k++) {
        if (got[static_cast<size_t>(k)] == want[static_cast<size_t>(k)]) ++same;
        else std::printf("  [i]    %s: render key %d holds %02X, expected %02X\n", tag, k,
                         got[static_cast<size_t>(k)], want[static_cast<size_t>(k)]);
    }
    std::snprintf(what, sizeof what, "%s: render keys 0-9 hold port 0's mapping on key 2 and nothing else",
                  tag);
    check.dec(what, static_cast<uint64_t>(same), kPhysKeys);
    const auto& r0 = held[0];
    std::snprintf(what, sizeof what, "%s: the lane's stream mask names port 0's stream alone", tag);
    check.hex(what, lane_streams(), r0[0] >= 0 ? (1ull << r0[0]) : 0ull);
}

//! D7: every port powers up holding stream p channel 0 on its one cluster,
//! and only port 0's projects (onto render key 2)
void Ship8Harness::prove_the_power_on_map(const char* tag) {
    hold_power_on();
    prove_the_store_and_the_projection(tag);
}

void Ship8Harness::phase_power_on() {
    std::printf("\n[POWER-ON] the 8x8 shape's input ports, read back\n");
    check.that("the AECP descriptor store fetched the generated 8x8 entity image", desc_requests > 0);
    std::printf("  [i]    %ld descriptor burst(s) served from the %zu-byte image\n", desc_requests,
                desc_img.size());
    prove_the_power_on_map("P1 POWER-ON");
    for (int l = 0; l < kStreams; l++) bind(l, "P2 BIND");
    check.hex("P2 BIND: all eight listener streams are bound", bound_streams(), (1u << kStreams) - 1u);
    long ids = 0;
    for (int k = 0; k < kStreams; k++) {
        uint64_t want = 0;
        for (const uint8_t b : sid_of(k)) want = (want << 8) | b;
        if (table_sid(k) == want) ++ids;
    }
    check.dec("P2 BIND: entry s of the stream table holds the stream id stream s's answer carried",
              static_cast<uint64_t>(ids), kStreams);
    start_the_feeds();
    run_pdus(kLeadPdus);
    const Window w = decode_a_window(kWindowPdus, 0, 0);
    prove_a_rendering_window(w, "P3 POWER-ON RENDER", 0, 0);
}

void Ship8Harness::phase_routes() {
    std::printf("\n[ROUTES] port 0's one cluster, remapped through ADD and REMOVE\n");
    check.dec("R1: REMOVE of port 0's power-on mapping succeeds",
              static_cast<uint64_t>(map_cmd(kCmdRemoveMappings, 0, 0, 0)), kSuccess);
    check.dec("R1: ADD stream 0 channel 5 on port 0 succeeds",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, 0, 0, 5)), kSuccess);
    prove_the_store_and_the_projection("R1");
    run_pdus(kSettlePdus);
    prove_a_rendering_window(decode_a_window(kWindowPdus, 0, 5), "R1 RENDER", 0, 5);
    check.dec("R2: REMOVE stream 0 channel 5 from port 0 succeeds",
              static_cast<uint64_t>(map_cmd(kCmdRemoveMappings, 0, 0, 5)), kSuccess);
    check.dec("R2: ADD stream 3 channel 2 on port 0 succeeds",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, 0, 3, 2)), kSuccess);
    prove_the_store_and_the_projection("R2");
    run_pdus(kSettlePdus);
    prove_a_rendering_window(decode_a_window(kWindowPdus, 3, 2), "R2 RENDER", 3, 2);
}

//! Ports 1-7: every mapping is stored, returned and refused exactly as on
//! port 0, and none reaches a render key or a pin
void Ship8Harness::phase_unrouted_ports() {
    std::printf("\n[UNROUTED] ports 1-7, mapped, against the pins\n");
    long removed = 0;
    long added = 0;
    for (int p = 1; p < kStreams; p++) {
        if (map_cmd(kCmdRemoveMappings, p, p, 0) == kSuccess) ++removed;
        if (map_cmd(kCmdAddMappings, p, p, 7) == kSuccess) ++added;
    }
    check.dec("U1: REMOVE of each unrouted port's power-on mapping succeeds",
              static_cast<uint64_t>(removed), kStreams - 1);
    check.dec("U1: ADD stream p channel 7 on each unrouted port p succeeds",
              static_cast<uint64_t>(added), kStreams - 1);
    check.dec("U2: cluster_offset 1 past port 7's one cluster is BAD_ARGUMENTS",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, 7, 7, 6, 1)), kBadArguments);
    prove_the_store_and_the_projection("U3");
    run_pdus(kSettlePdus);
    const auto pops0 = pops;
    prove_a_rendering_window(decode_a_window(kWindowPdus, 3, 2), "U4 RENDER", 3, 2);
    //! the unrouted ports' streams are live, so their absence from every
    //! slot is the projection's doing and not a silent feed
    long live = 0;
    for (int k = 0; k < kStreams; k++)
        if (k != 3 && pops[static_cast<size_t>(k)] - pops0[static_cast<size_t>(k)] >= kMinFrames) ++live;
    check.dec("U4: the seven other streams each presented a window of events, none at the pins",
              static_cast<uint64_t>(live), kStreams - 1);
}

void Ship8Harness::phase_remove() {
    std::printf("\n[REMOVE] port 0's mapping removed: silence\n");
    check.dec("X1: REMOVE stream 3 channel 2 from port 0 succeeds",
              static_cast<uint64_t>(map_cmd(kCmdRemoveMappings, 0, 3, 2)), kSuccess);
    prove_the_store_and_the_projection("X1");
    run_pdus(kSettlePdus);
    prove_a_silent_window(decode_a_window(kWindowPdus, -1, -1), "X2 SILENCE");
    check.dec("X3: ADD stream 0 channel 1 on port 0 succeeds",
              static_cast<uint64_t>(map_cmd(kCmdAddMappings, 0, 0, 1)), kSuccess);
    prove_the_store_and_the_projection("X3");
    run_pdus(kSettlePdus);
    prove_a_rendering_window(decode_a_window(kWindowPdus, 0, 1), "X3 RENDER", 0, 1);
}

//! The render epoch is stream qualified: a bind fall on a stream the lane
//! does not render changes nothing; one on the rendered stream silences the
//! slot until a post-loss event is presented, and no pre-loss sample renders
void Ship8Harness::phase_bind_freshness() {
    std::printf("\n[BIND] bind falls and the rebind's freshness\n");
    const uint64_t epochs0 = lane_epochs();
    unbind(5);
    check.dec("B1: a bind fall on stream 5, which the lane does not render, opens no epoch",
              lane_epochs(), epochs0);
    prove_a_rendering_window(decode_a_window(kWindowPdus, 0, 1), "B1 RENDER", 0, 1);
    const long events_at_loss = injected[0];
    unbind(0);
    check.dec("B2: the bind fall on stream 0, which the lane renders, opens one epoch",
              lane_epochs(), epochs0 + 1);
    //! the frame in flight at the fall ends whole (sim_tdm8_render T22), so
    //! the window opens one PDU later
    run_pdus(1);
    prove_a_silent_window(decode_a_window(kWindowPdus, -1, -1), "B2 UNBOUND");
    bind(0, "B3 REBIND");
    run_pdus(kLeadPdus);
    const Window w = decode_a_window(kWindowPdus, 0, 1);
    prove_a_rendering_window(w, "B3 RENDER", 0, 1);
    char what[200];
    std::snprintf(what, sizeof what, "B3 FRESHNESS: the first event after the rebind is past the %ld "
                  "sent before the loss", events_at_loss);
    check.that(what, w.first_event >= events_at_loss);
    check.dec("B3: the rebind opened no further epoch", lane_epochs(), epochs0 + 1);
    bind(5, "B4 REBIND");
}

//! A reset during activity: every port returns to D7's power-on map, the
//! lane stays silent until a listener is bound again, and then renders only
//! post-reset audio
void Ship8Harness::phase_reset() {
    std::printf("\n[RESET] a datapath reset while the lane renders\n");
    const long events_at_reset = injected[0];
    const unsigned mask = feed_mask;
    feed_mask = 0;
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    steps(64);
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    steps(256);
    axi_write(0x108, 0x0); axi_write(0x10C, 0x0);
    boot_the_entity();
    provision_the_listener_contexts("Z1");
    prove_the_power_on_map("Z1 POWER-ON AGAIN");
    feed_mask = mask;
    anchored.fill(false);
    next_pdu_at = axis_cycle + 64;
    run_pdus(kLeadPdus);
    prove_a_silent_window(decode_a_window(kWindowPdus, -1, -1), "Z2 UNBOUND AFTER RESET");
    for (int l = 0; l < kStreams; l++) bind(l, "Z3 BIND");
    run_pdus(kLeadPdus);
    const Window w = decode_a_window(kWindowPdus, 0, 0);
    prove_a_rendering_window(w, "Z3 RENDER", 0, 0);
    char what[200];
    std::snprintf(what, sizeof what, "Z3 FRESHNESS: the first event after the reset is past the %ld "
                  "sent before it", events_at_reset);
    check.that(what, w.first_event >= events_at_reset);
}

int Ship8Harness::run() {
    const milan::tb::Model<Vmilan_datapath> model;
    dut = model.get();
    char image_check[96];
    std::snprintf(image_check, sizeof image_check,
                  "the generated 8x8 entity image is on disk (make %s)", kAemImage);
    if (!check.that(image_check, load_descriptor_image(kAemImage))) return check.report();
    bring_out_of_reset();
    boot_the_entity();
    provision_the_listener_contexts("BOOT");
    phase_power_on();
    phase_routes();
    phase_unrouted_ports();
    phase_remove();
    phase_bind_freshness();
    phase_reset();
    return check.report();
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Ship8Harness harness;
    return harness.run();
}
