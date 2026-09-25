// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Issue #387 acceptance 3: a grandmaster change that steps the PHC by more
// than one second, while an AAF stream is bound and locked under CRF
// selection, graded against the #387 decision (comments 5606198212 part b and
// 5794731090): every step is ONE counted media event - tu rises on the commit
// edge and clears after the step's holdover, the talker keeps streaming and
// the listener keeps its lock, the render stage re-centres once, the outgoing
// mr toggles once and the talker's MEDIA_RESET counts once. The counted event
// is the STEP's: the re-base and the toggle land inside a short window after
// the plane's step pulse, and MEDIA_RESET has not moved between the commit and
// the step, so a re-base keyed to the grandmaster identity fails.
//
// What this leg does NOT grade: the grid aligner (the TDM clocks are held),
// the CRF servo (the DRP answers zero; #539), an lwSRP licence (the talker is
// opened by the escape bit), a step that lands inside a pending mr restart
// (ruling 5802264260 item 2: tb/verilator/tkdiag T17 and T18 grade the
// restart engine PDU by PDU), and the physical re-base (#117). Its
// negative controls are gmstep_mutants.py.
//
// Elaboration: the `gptp` leg's (AX7101 1x1 TDM8 entity, fabric gPTP ON, the
// fabric clock compressed to 2 MHz so the plane's real timers fit a runnable
// window, the PHC programmed at 8 ns per cycle, CLKV quarter-tick 131072
// cycles). Everything below is in fabric cycles and PHC nanoseconds of this
// model; nothing is scaled back to wall time.
//
// Peer: one link partner at a 600 ns one-way delay. Its Pdelay answers are
// fabricated against the DUT's own PHC exactly as sim_gptp.cpp does, so the
// published delay stays at the link delay across a PHC step. Its Sync origins
// come from an INDEPENDENT grandmaster timeline, gm(c) = 8 c + epoch: GM A's
// epoch puts it seconds ahead of the reset PHC (the link-up pair steps), and
// the change to GM B moves the epoch by kGmStepNs. Nothing about the new
// timeline is read from the DUT, so a DUT that failed to step would keep
// seeing the whole offset.
//
// Media: the listener is bound through the 0x800 bench window and fed eight
// channel AAF PDUs on the packet grid's own cadence (6 media ticks = 250
// cycles); the CRF sink is provisioned and fed at 2 ms; the media clock source
// is set to the CRF by SET_CLOCK_SOURCE over AECP; the talker is opened by the
// documented AAF_CTRL[1] escape, NOT an lwSRP licence (no SRP peer exists
// here). The peer's media timestamps follow its own PHC, which steps when it
// sends its first GM B Sync, a moment before this DUT steps on consuming it.
// The TDM clocks are held: the grid aligner has no PHC input and stays
// disengaged on a dead feed, which keeps the packet grid exactly nominal.
//
// The render law is graded where KL_render_setpoint states it and judges its
// bands: the fill right after each PDU's push is TARGET_C = setpoint + one
// PDU = 14 events. The harness reads it as the peak of the registered fill
// between two accepts: pops only lower it after the push, and the next PDU
// pushes only after its own accept (the depacketizer commits a frame at its
// tlast, after the monitor's accept at byte 48). The fill AT the accept is not
// graded: it depends on how many media ticks fall between the last push and
// the accept, which moves with the feed's start phase (9 or 10 events here).
// The talker's own cadence in this compressed model is not the product's, so
// its stream is graded against its own baseline: no sequence gap, the same
// rate, no pause beyond four of its intervals, counting the silence from its
// last PDU to the end of the graded window.
//
// Usage: Vmilan_dp_gmstep <aem image> [feed delay]. The optional feed delay
// (fabric cycles, default 0) idles before the peer's media feed starts, which
// moves the accept phase against the media tick; a correct datapath passes at
// every delay. Exit 0 only when every check passes.

#include "../../common/verilator_harness.hpp"
#include "../../common/gptp_launch_observer.hpp"
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include <verilated.h>

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <fstream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#ifndef CLKV_QTICK_CYC_TB
#error "Makefile must couple CLKV_QTICK_CYC_TB to GCLKV_QTICK_CYC_P"
#endif

namespace {

constexpr uint64_t kPeer = 0x0080E1FFFE112233ULL;
constexpr uint64_t kGmA = 0x00AACCFFFE010203ULL;
constexpr uint64_t kGmB = 0x00BBDDFFFE040506ULL;
constexpr uint8_t kPriorityA = 100;
constexpr uint8_t kPriorityB = 50;             //! better: the change is real
constexpr uint64_t kClkHz = 2000000;
constexpr uint64_t kPhcTickNs = 8;
constexpr uint64_t kEpochANs = 3000000000ULL;  //! GM A ahead of the reset PHC
constexpr uint64_t kGmStepNs = 1500000000ULL;  //! GM B ahead of GM A
constexpr int64_t kLinkNs = 600;               //! one-way link delay
constexpr uint64_t kPresentationNs = 2000000;  //! peer talker's offset
constexpr uint64_t kAafPeriodCyc = kClkHz / 8000;
constexpr uint64_t kCrfPeriodCyc = kClkHz / 500;
constexpr uint64_t kSyncPeriodCyc = kClkHz / 8;
constexpr uint64_t kAnnouncePeriodCyc = kClkHz;
//! the first GM B Sync this long after its Announce: longer than a quarter
//! tick, so a holdover armed by the commit alone ends visibly before a
//! holdover re-armed by the step
constexpr uint64_t kGmSyncDelayCyc = 160000;
constexpr uint64_t kQtickCyc = CLKV_QTICK_CYC_TB;
//! #386 render law under test: one class-A PDU of events plus two is the
//! setpoint, and the fill right after every PDU push is one PDU above it
constexpr unsigned kRenderPduEvt = 6;
constexpr unsigned kRenderSetpointEvt = kRenderPduEvt + 2;
constexpr unsigned kRenderTargetEvt = kRenderSetpointEvt + kRenderPduEvt;
//! a running talker never pauses longer than this many of its own intervals
constexpr uint64_t kTalkerPauseIntervals = 4;
//! the step's counted re-base lands at a PDU end this soon after the plane's
//! step pulse: the next PDU end, with one PDU of slack
constexpr uint64_t kRebaseWindowCyc = 2 * kAafPeriodCyc;
//! the step's mr toggle is first sent this many talker intervals after the
//! plane's step pulse at most: a PDU granted before the pulse keeps the old
//! level, the next one carries the new
constexpr double kToggleWindowIntervals = 2.0;
constexpr uint16_t kCrfClockSource = 1;        //! AX 1x1: INTERNAL 0, CRF 1
//! the Stream Input counters_valid bits this leg reads: MEDIA_UNLOCKED (1)
//! and FRAMES_RX (11), Milan Table 5.6
constexpr uint32_t kSinCountersUsed = (1u << 1) | (1u << 11);
//! frames other than AAF start only this far ahead of the next AAF slot
constexpr uint64_t kSlotGuardCyc = 64;
//! a talker PDU granted before an edge may still carry the old verdict
constexpr uint64_t kWireSettleCyc = 2 * kAafPeriodCyc;

struct Frame {
    std::vector<uint8_t> b;
    void u8(uint8_t v) { b.push_back(v); }
    void u16(uint16_t v) { u8(static_cast<uint8_t>(v >> 8)); u8(static_cast<uint8_t>(v)); }
    void u32(uint32_t v) { u16(static_cast<uint16_t>(v >> 16)); u16(static_cast<uint16_t>(v)); }
    void u48(uint64_t v) { u16(static_cast<uint16_t>(v >> 32)); u32(static_cast<uint32_t>(v)); }
    void u64(uint64_t v) { u32(static_cast<uint32_t>(v >> 32)); u32(static_cast<uint32_t>(v)); }
    void ts(uint64_t ns) { u48(ns / 1000000000ULL); u32(static_cast<uint32_t>(ns % 1000000000ULL)); }
};

uint64_t be(const std::vector<uint8_t>& b, size_t off, size_t n) {
    if (off + n > b.size()) return UINT64_MAX;
    uint64_t v = 0;
    for (size_t i = 0; i < n; ++i) v = (v << 8) | b[off + i];
    return v;
}

Frame ptp(uint8_t type, uint16_t seq, uint16_t flags, uint16_t body) {
    Frame f;
    f.u48(0x0180C200000EULL); f.u48(0x0080E1112233ULL); f.u16(0x88F7);
    f.u8(static_cast<uint8_t>(0x10 | type)); f.u8(2);
    f.u16(static_cast<uint16_t>(34 + body));
    f.u16(0); f.u16(flags); f.u64(0); f.u32(0);
    f.u64(kPeer); f.u16(1); f.u16(seq); f.u8(5); f.u8(0x7F);
    return f;
}

Frame announce(uint16_t seq, uint64_t gm, uint8_t priority1) {
    Frame f = ptp(0xB, seq, 0x0008, 30 + 4 + 16);
    for (int i = 0; i < 10; ++i) f.u8(0);
    f.u16(0xFFC4); f.u8(0);
    f.u8(priority1); f.u32(0xF8FE436A); f.u8(248); f.u64(gm);
    f.u16(1); f.u8(0xA0);
    f.u16(0x0008); f.u16(16); f.u64(gm); f.u64(kPeer);
    return f;
}

Frame follow_up(uint16_t seq, uint64_t origin) {
    Frame f = ptp(0x8, seq, 0x0008, 42);
    f.ts(origin); f.u16(0x0003); f.u16(28);
    f.u48(0x0080C2000001ULL); f.u32(0); f.u16(0);
    f.u64(0); f.u32(0); f.u32(0);
    return f;
}

//! the peer talker's eight-channel PDU; the listener grades none of the
//! samples here, only the accept instant
Frame aaf_pdu(uint8_t seq, uint64_t gm_ns) {
    Frame f;
    f.u48(0x91E0F0002A02ULL); f.u48(0x020000000002ULL); f.u16(0x22F0);
    f.u8(0x02); f.u8(0x81); f.u8(seq); f.u8(0);
    f.u64(0x0200000000020000ULL);
    f.u32(static_cast<uint32_t>(gm_ns + kPresentationNs));
    f.u8(0x02); f.u8(0x50); f.u8(8); f.u8(32); f.u16(192); f.u16(0);
    for (unsigned i = 0; i < 48; ++i) f.u32(0);
    return f;
}

Frame crf_pdu(uint8_t seq, uint64_t gm_ns) {
    Frame f;
    f.u48(0x91E0F0002A03ULL); f.u48(0x020000000002ULL); f.u16(0x22F0);
    f.u8(0x04); f.u8(0x80); f.u8(seq); f.u8(0x01);
    f.u64(0x0200000000020001ULL);
    f.u32(0x0000BB80); f.u16(8); f.u16(96);
    f.u64(gm_ns + kPresentationNs);
    while (f.b.size() < 64) f.u8(0);
    return f;
}

Frame aecp(uint16_t command, uint16_t seq, const std::vector<uint8_t>& payload) {
    Frame f;
    f.u48(0x020000000001ULL); f.u48(0x6805CA95B2D1ULL); f.u16(0x22F0);
    f.u8(0xFB); f.u8(0x00);
    f.u16(static_cast<uint16_t>(12 + payload.size()));
    f.u64(0x020000FFFE000001ULL); f.u64(0x6805CAFFFE95B2D1ULL);
    f.u16(seq); f.u16(command);
    for (uint8_t v : payload) f.u8(v);
    while (f.b.size() < 60) f.u8(0);
    return f;
}

//! One PDU the DUT's AAF talker put on the wire.
struct TxPdu {
    uint64_t cyc = 0;
    uint8_t seq = 0;
    bool tu = false;
    bool mr = false;
};

//! A frame the peer sends, built at the instant its first beat can go, so
//! every time it carries is the time of that instant.
enum class Kind { Aaf, Crf, Announce, Sync, FollowUp, PdelayResp, PdelayRespFu, Aecp };

struct Outgoing {
    Kind kind = Kind::Aaf;
    uint16_t seq = 0;
    uint64_t value = 0;                 //! origin, t1 or t3, per kind
    std::vector<uint8_t> tail;          //! requesting port, or AECP payload
    uint16_t command = 0;
    uint64_t not_before = 0;
};

//! What one run of the GM change looked like, sampled every cycle.
struct Trace {
    uint64_t steps = 0;                 //! PHC discontinuities seen
    uint64_t step_pulses = 0;           //! the plane's phc_step_we_o pulses
    uint64_t step_cyc = 0;              //! the last discontinuity
    uint64_t step_pulse_cyc = 0;        //! the last step pulse
    int64_t step_ns = 0;
    bool tu_prev = true;                //! tu at the previous sample
    uint64_t tu_rise_cyc = 0;
    uint64_t tu_fall_cyc = 0;
    uint64_t identity_cyc = 0;          //! first cycle the bank named GM B
    bool tu_at_identity = false;
    uint64_t render_triggers = 0;       //! render_recentre_p_w pulses
    std::vector<uint64_t> recentre_cycs;  //! cycles the counted tally moved
};

//! The AXI4-Lite handshakes of one cycle, sampled before its edge.
struct AxiFires {
    bool aw = false;
    bool w = false;
    bool b = false;
    bool ar = false;
    bool r = false;
    uint32_t data = 0;
};

class GmStepHarness {
 public:
    GmStepHarness(std::vector<uint8_t> image, uint64_t feed_delay)
        : descriptor_(std::move(image)), feed_delay_(feed_delay) {
        check_.echo_passes();
    }
    int run();

 private:
    milan::tb::Model<Vmilan_datapath> model_;
    Vmilan_datapath* dut_ = model_.get();
    milan::tb::Checker check_{"gmstep"};
    std::vector<uint8_t> descriptor_;
    uint64_t feed_delay_ = 0;                  //! idle before the media feed
    milan::tb::GptpLaunchObserver observer_{kPhcTickNs};
    uint64_t cyc_ = 0;
    uint64_t phc_prev_ = 0;
    uint64_t gm_epoch_ = kEpochANs;
    uint64_t media_epoch_ = kEpochANs;         //! the peer talker's own PHC
    bool slew_probe_ = false;
    bool slew_origin_override_ = false;
    int64_t slew_offset_ns_ = 0;
    std::array<bool, 4> slew_history_{};
    unsigned slew_alignment_errors_ = 0;
    unsigned slew_high_samples_ = 0;
    unsigned slew_falls_ = 0;
    bool slew_previous_ = false;
    bool media_follows_sync_ = false;          //! steps with the next Sync
    double talker_interval_ = 0;               //! baseline cycles per PDU
    uint64_t gm_id_ = kGmA;
    uint8_t gm_priority_ = kPriorityA;
    AxiFires fires_;

    // the peer's schedule
    bool peer_on_ = false;
    bool media_on_ = false;
    uint64_t next_aaf_ = 0;
    uint64_t next_crf_ = 0;
    uint64_t next_sync_ = 0;
    uint64_t next_announce_ = 0;
    uint16_t sync_seq_ = 0;
    uint16_t announce_seq_ = 0;
    uint8_t aaf_seq_ = 0;
    uint8_t crf_seq_ = 0;
    std::deque<Outgoing> control_;
    std::vector<uint8_t> rx_;
    Outgoing rx_what_;
    size_t rx_off_ = 0;
    bool rx_busy_ = false;

    // what the DUT sent
    std::vector<uint8_t> tx_cur_;
    std::vector<std::vector<uint8_t>> tx_frames_;
    std::vector<TxPdu> talker_;
    size_t pd_scan_ = 0;

    // what the observers saw
    Trace trace_;
    uint64_t recentres_seen_ = 0;              //! the counted tally, last sample
    //! (accept cycle, fill right after that PDU's push), closed at the next
    //! accept; the open window's accept and running peak
    std::vector<std::pair<uint64_t, unsigned>> pushes_;
    uint64_t window_cyc_ = 0;
    unsigned window_peak_ = 0;
    bool window_open_ = false;
    //! (accept cycle, fill at that accept): the fill is printed, never graded
    std::vector<std::pair<uint64_t, unsigned>> accepts_;
    //! accepts seen before and after each Stream Input GET_COUNTERS
    std::pair<size_t, size_t> sin0_accepts_{0, 0};
    std::pair<size_t, size_t> sin1_accepts_{0, 0};

    // the model's two memory faces and the DRP responder
    std::array<uint8_t, 592> rmem_{};
    bool rm_busy_ = false;
    bool rm_done_ = false;
    uint32_t rm_addr_ = 0;
    unsigned rm_left_ = 0;
    bool dm_busy_ = false;
    uint32_t dm_addr_ = 0;
    unsigned dm_left_ = 0;
    unsigned dm_wait_ = 0;
    unsigned drp_lat_ = 0;

    uint64_t phc_ns() const;
    uint64_t gm_ns(uint64_t cycle) const { return cycle * kPhcTickNs + gm_epoch_; }
    uint64_t media_ns(uint64_t cycle) const { return cycle * kPhcTickNs + media_epoch_; }
    void tick();
    void run_cycles(uint64_t n) { while (n--) tick(); }
    void memory_drive();
    void memory_edge();
    void drp_edge();
    void schedule();
    void start_frame(Outgoing what);
    std::vector<uint8_t> build(const Outgoing& what);
    void rx_drive();
    void rx_accepted();
    void tx_edge();
    void complete_tx();
    void service_pdelay();
    void observe();
    void write(uint16_t addr, uint32_t value);
    uint32_t read(uint16_t addr);
    std::vector<uint8_t> aecp_transaction(uint16_t command, uint16_t seq,
                                          const std::vector<uint8_t>& payload);
    std::vector<uint8_t> counters(uint16_t seq, uint16_t descriptor_type);
    static uint32_t counter_word(const std::vector<uint8_t>& response, unsigned word);

    void reset();
    void acquire();
    void provision_media();
    void baseline();
    void change_grandmaster();
    void check_slew_connection();
    void observe_slew_alignment(bool raw, bool expected);
    void grade_the_event(const std::vector<uint8_t>& sout0, const std::vector<uint8_t>& sout_mid,
                         uint64_t mid_cyc, const std::vector<uint8_t>& sin0,
                         uint64_t recentres0, uint64_t rails0, size_t talker0);
    void grade_uncertainty(size_t talker0);
    void grade_the_licence(size_t talker0, const std::vector<uint8_t>& sin0,
                           const std::vector<uint8_t>& sin1);
    void grade_the_render(uint64_t recentres0, uint64_t rails0, uint64_t event_cyc);
    void grade_the_restart(size_t talker0, const std::vector<uint8_t>& sout0,
                           const std::vector<uint8_t>& sout_mid,
                           const std::vector<uint8_t>& sout1);
};

//! The PHC this cycle, read where the plane reads it: the integer field of
//! the counter's accumulator (`timestamp_counter.sv`).
uint64_t GmStepHarness::phc_ns() const {
    const auto& acc = dut_->rootp->milan_datapath__DOT__ts_counter__DOT__acc;
    return (static_cast<uint64_t>(acc[2]) << 40)
         | (static_cast<uint64_t>(acc[1]) << 8)
         | (acc[0] >> 24);
}

void GmStepHarness::tick() {
    schedule();
    rx_drive();
    dut_->axis_clk = 0; dut_->gtx_clk = 0;
    memory_drive();
    dut_->eval();
    const bool rx_fire = dut_->s_axis_mac_rx_tvalid && dut_->s_axis_mac_rx_tready;
    fires_.aw = dut_->s_axi_awvalid && dut_->s_axi_awready;
    fires_.w = dut_->s_axi_wvalid && dut_->s_axi_wready;
    fires_.b = dut_->s_axi_bvalid && dut_->s_axi_bready;
    fires_.ar = dut_->s_axi_arvalid && dut_->s_axi_arready;
    fires_.r = dut_->s_axi_rvalid && dut_->s_axi_rready;
    fires_.data = dut_->s_axi_rdata;
    const uint64_t phc = phc_ns();
    if (cyc_ != 0 && (phc - phc_prev_ > 64 || phc < phc_prev_)) {
        ++trace_.steps;
        trace_.step_cyc = cyc_;
        trace_.step_ns = static_cast<int64_t>(phc - phc_prev_ - kPhcTickNs);
    }
    phc_prev_ = phc;
    tx_edge();
    observer_.edge(dut_, cyc_, phc);
    drp_edge();
    memory_edge();
    const bool raw_slew = dut_->rootp->milan_datapath__DOT__gptp_slew_active_w;
    const bool expected_slew = raw_slew ||
        std::any_of(slew_history_.begin(), slew_history_.end(), [](bool v) { return v; });
    dut_->axis_clk = 1; dut_->gtx_clk = 1;
    dut_->eval();
    observe_slew_alignment(raw_slew, expected_slew);
    if (rx_fire) rx_accepted();
    ++cyc_;
    observe();
}

//! Observe the servo's staged input, not a parallel harness connection.
//! Four historical source samples cover latch + sync + PHC application.
void GmStepHarness::observe_slew_alignment(bool raw, bool expected) {
    const bool sampled = dut_->rootp->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__phc_slew_q_r;
    if (slew_probe_) {
        slew_alignment_errors_ += sampled != expected;
        slew_high_samples_ += sampled;
        slew_falls_ += slew_previous_ && !raw;
    }
    slew_previous_ = raw;
    for (size_t i = slew_history_.size() - 1; i > 0; --i)
        slew_history_[i] = slew_history_[i - 1];
    slew_history_[0] = raw;
}

void GmStepHarness::observe() {
    auto* root = dut_->rootp;
    const bool tu = root->milan_datapath__DOT__clkv_tu_w;
    if (tu && !trace_.tu_prev) trace_.tu_rise_cyc = cyc_;
    if (!tu && trace_.tu_prev) trace_.tu_fall_cyc = cyc_;
    //! both are read after the same edge: the bank's identity and the tu every
    //! talker stamps during the cycle that follows it
    if (!trace_.identity_cyc && root->milan_datapath__DOT__gptp_pub_gm_w == kGmB) {
        trace_.identity_cyc = cyc_;
        trace_.tu_at_identity = tu;
    }
    trace_.tu_prev = tu;
    if (root->milan_datapath__DOT__gptp_step_we_w) {
        ++trace_.step_pulses;
        trace_.step_pulse_cyc = cyc_;
    }
    if (root->milan_datapath__DOT__render_recentre_p_w) ++trace_.render_triggers;
    const uint64_t recentres = root->milan_datapath__DOT__rsp_recentres_w;
    if (recentres != recentres_seen_) {
        trace_.recentre_cycs.push_back(cyc_);
        recentres_seen_ = recentres;
    }
    //! the fill right after a PDU's push is the peak between its accept and
    //! the next one (the banner has why)
    const unsigned fill = root->milan_datapath__DOT__rsp_fill_w & 0xFF;
    if (root->milan_datapath__DOT__avtprx_accept_p) {
        if (window_open_) pushes_.emplace_back(window_cyc_, window_peak_);
        accepts_.emplace_back(cyc_, fill);
        window_cyc_ = cyc_;
        window_peak_ = fill;
        window_open_ = true;
    }
    window_peak_ = std::max(window_peak_, fill);
}

void GmStepHarness::memory_drive() {
    uint64_t data = 0;
    for (unsigned i = 0; i < 8; ++i) {
        const uint32_t off = rm_addr_ - 0x20100000u + i;
        data = (data << 8) | (off < rmem_.size() ? rmem_[off] : 0);
    }
    dut_->i_resp_mem_req_ready = !rm_busy_;
    dut_->i_resp_mem_rsp_valid = rm_busy_;
    dut_->i_resp_mem_rsp_data = data;
    dut_->i_resp_mem_rsp_last = rm_busy_ && rm_left_ == 1;
    dut_->i_resp_mem_rsp_err = 0;
    dut_->i_resp_mem_wr_ready = !rm_done_;
    dut_->i_resp_mem_wr_done = rm_done_;
    dut_->i_resp_mem_wr_err = 0;
    uint64_t desc = 0;
    for (unsigned i = 0; i < 8; ++i) {
        const uint32_t off = dm_addr_ - 0x20000000u + i;
        desc = (desc << 8) | (off < descriptor_.size() ? descriptor_[off] : 0);
    }
    dut_->i_desc_mem_req_ready = !dm_busy_;
    dut_->i_desc_mem_rsp_valid = dm_busy_ && dm_wait_ == 0;
    dut_->i_desc_mem_rsp_data = desc;
    dut_->i_desc_mem_rsp_last = dm_busy_ && dm_left_ == 1;
    dut_->i_desc_mem_rsp_err = 0;
}

void GmStepHarness::memory_edge() {
    if (rm_busy_ && dut_->o_resp_mem_rsp_ready) {
        rm_addr_ += 8;
        if (--rm_left_ == 0) rm_busy_ = false;
    } else if (!rm_busy_ && dut_->o_resp_mem_req_valid) {
        rm_addr_ = dut_->o_resp_mem_req_addr;
        rm_left_ = dut_->o_resp_mem_req_beats;
        rm_busy_ = rm_left_ != 0;
    }
    if (rm_done_) rm_done_ = false;
    else if (dut_->o_resp_mem_wr_valid) {
        for (unsigned i = 0; i < 8; ++i) {
            const uint32_t off = dut_->o_resp_mem_wr_addr - 0x20100000u + i;
            if (off < rmem_.size() && (dut_->o_resp_mem_wr_strb & (1u << i)))
                rmem_[off] = static_cast<uint8_t>(dut_->o_resp_mem_wr_data >> (56 - 8 * i));
        }
        rm_done_ = true;
    }
    if (!dm_busy_ && dut_->o_desc_mem_req_valid) {
        dm_addr_ = dut_->o_desc_mem_req_addr;
        dm_left_ = dut_->o_desc_mem_req_beats;
        dm_busy_ = dm_left_ != 0;
        dm_wait_ = 12;
    } else if (dm_busy_ && dm_wait_) {
        --dm_wait_;
    } else if (dm_busy_ && dut_->o_desc_mem_rsp_ready) {
        dm_addr_ += 8;
        if (--dm_left_ == 0) dm_busy_ = false;
    }
}

//! The MMCM DRP port answers a few cycles after each request with data 0;
//! the servo's own suite owns the ClkReg contents (tb/verilator/mmcm_servo).
void GmStepHarness::drp_edge() {
    dut_->i_mmcm_drp_rdy = 0;
    if (drp_lat_ && --drp_lat_ == 0) dut_->i_mmcm_drp_rdy = 1;
    if (dut_->o_mmcm_drp_en) drp_lat_ = 3;
    dut_->i_mmcm_drp_do = 0;
}

//! Decide what the peer sends next. AAF owns its slots; everything else
//! starts only with room before the next one, so the listener's accept
//! instant keeps one phase against the media tick.
void GmStepHarness::schedule() {
    if (peer_on_ && cyc_ >= next_sync_) {
        control_.push_back({Kind::Sync, sync_seq_++, 0, {}, 0, cyc_});
        next_sync_ = cyc_ + kSyncPeriodCyc;
    }
    if (peer_on_ && cyc_ >= next_announce_) {
        control_.push_back({Kind::Announce, announce_seq_++, 0, {}, 0, cyc_});
        next_announce_ = cyc_ + kAnnouncePeriodCyc;
    }
    if (rx_busy_) return;
    if (media_on_ && cyc_ >= next_aaf_) {
        start_frame({Kind::Aaf, aaf_seq_++, 0, {}, 0, 0});
        next_aaf_ += kAafPeriodCyc;
        return;
    }
    const bool room = !media_on_ || next_aaf_ >= cyc_ + kSlotGuardCyc;
    if (!room) return;
    if (media_on_ && cyc_ >= next_crf_) {
        start_frame({Kind::Crf, crf_seq_++, 0, {}, 0, 0});
        next_crf_ += kCrfPeriodCyc;
        return;
    }
    for (auto it = control_.begin(); it != control_.end(); ++it) {
        if (it->not_before > cyc_) continue;
        Outgoing what = *it;
        control_.erase(it);
        start_frame(what);
        return;
    }
}

//! A Pdelay response is fabricated here, against the PHC the DUT will stamp
//! its first beat with: t2 = now + 5 ms and a residence that leaves exactly
//! the link delay, so a PHC step between t1 and now cancels (sim_gptp.cpp).
void GmStepHarness::start_frame(Outgoing what) {
    if (what.kind == Kind::PdelayResp) {
        const uint64_t now = phc_ns();
        const uint64_t t2 = now + 5000000;
        const uint64_t t3 = t2 + (now - what.value) - 2 * static_cast<uint64_t>(kLinkNs);
        control_.push_back({Kind::PdelayRespFu, what.seq, t3, what.tail, 0, cyc_ + 16});
        what.value = t2;
    }
    if (what.kind == Kind::Sync && media_follows_sync_) {
        media_epoch_ = gm_epoch_;
        media_follows_sync_ = false;
    }
    rx_ = build(what);
    rx_what_ = std::move(what);
    rx_off_ = 0;
    rx_busy_ = true;
}

std::vector<uint8_t> GmStepHarness::build(const Outgoing& what) {
    switch (what.kind) {
    case Kind::Aaf: return aaf_pdu(static_cast<uint8_t>(what.seq), media_ns(cyc_)).b;
    case Kind::Crf: return crf_pdu(static_cast<uint8_t>(what.seq), media_ns(cyc_)).b;
    case Kind::Announce: return announce(what.seq, gm_id_, gm_priority_).b;
    case Kind::Sync: {
        Frame f = ptp(0x0, what.seq, 0x0208, 10);
        f.ts(0);
        return f.b;
    }
    case Kind::FollowUp: return follow_up(what.seq, what.value).b;
    case Kind::PdelayResp:
    case Kind::PdelayRespFu: {
        const bool resp = what.kind == Kind::PdelayResp;
        Frame f = ptp(resp ? 0x3 : 0xA, what.seq, resp ? 0x0200 : 0x0000, 20);
        f.ts(what.value);
        for (uint8_t v : what.tail) f.u8(v);
        return f.b;
    }
    case Kind::Aecp: return aecp(what.command, what.seq, what.tail).b;
    }
    return {};
}

void GmStepHarness::rx_drive() {
    dut_->s_axis_mac_rx_tvalid = rx_busy_;
    dut_->s_axis_mac_rx_tlast = rx_busy_ && rx_off_ + 8 >= rx_.size();
    uint64_t data = 0;
    uint8_t keep = 0;
    for (size_t i = 0; rx_busy_ && i < 8 && rx_off_ + i < rx_.size(); ++i) {
        data |= static_cast<uint64_t>(rx_[rx_off_ + i]) << (8 * i);
        keep = static_cast<uint8_t>(keep | (1u << i));
    }
    dut_->s_axis_mac_rx_tdata = data;
    dut_->s_axis_mac_rx_tkeep = keep;
}

//! One receive beat went in. The first beat of a Sync is the instant the DUT
//! stamps, so the Follow_Up's origin is the grandmaster's time at that
//! instant less the link; a Pdelay response is answered the same way
//! sim_gptp.cpp does, against the PHC the DUT stamps it with.
void GmStepHarness::rx_accepted() {
    const bool first = rx_off_ == 0;
    rx_off_ += 8;
    if (first && rx_what_.kind == Kind::Sync) {
        const uint64_t origin = slew_origin_override_
            ? static_cast<uint64_t>(static_cast<int64_t>(phc_ns()) - kLinkNs - slew_offset_ns_)
            : gm_ns(cyc_) - static_cast<uint64_t>(kLinkNs);
        control_.push_back({Kind::FollowUp, rx_what_.seq, origin, {}, 0, cyc_ + 200});
    }
    if (rx_off_ < rx_.size()) return;
    rx_busy_ = false;
}

void GmStepHarness::tx_edge() {
    if (!dut_->m_axis_mac_tx_tvalid) return;
    for (unsigned i = 0; i < 8; ++i)
        if (dut_->m_axis_mac_tx_tkeep & (1u << i))
            tx_cur_.push_back(static_cast<uint8_t>(dut_->m_axis_mac_tx_tdata >> (8 * i)));
    if (!dut_->m_axis_mac_tx_tlast) return;
    complete_tx();
    tx_cur_.clear();
}

void GmStepHarness::complete_tx() {
    observer_.offer(tx_cur_, cyc_);
    const auto& f = tx_cur_;
    if (f.size() > 21 && be(f, 12, 2) == 0x8100 && be(f, 16, 2) == 0x22F0 && f[18] == 0x02)
        talker_.push_back({cyc_, f[20], (f[21] & 1) != 0, (f[19] & 0x08) != 0});
    tx_frames_.push_back(f);
    if (peer_on_) service_pdelay();
}

//! Queue an answer to every Pdelay_Req once its launch has been reported
//! (#360); start_frame() fabricates its times.
void GmStepHarness::service_pdelay() {
    while (pd_scan_ < tx_frames_.size()) {
        const std::vector<uint8_t>& req = tx_frames_[pd_scan_];
        if (req.size() < 54 || be(req, 12, 2) != 0x88F7 || (req[14] & 0xF) != 0x2) {
            ++pd_scan_;
            continue;
        }
        uint64_t t1 = 0;
        if (!observer_.t1_of(0x2, static_cast<unsigned>(be(req, 44, 2)), &t1)) return;
        Outgoing resp{Kind::PdelayResp, static_cast<uint16_t>(be(req, 44, 2)), t1,
                      std::vector<uint8_t>(req.begin() + 34, req.begin() + 44), 0, cyc_ + 300};
        control_.push_back(resp);
        ++pd_scan_;
    }
}

void GmStepHarness::write(uint16_t addr, uint32_t value) {
    dut_->s_axi_awaddr = addr; dut_->s_axi_awvalid = 1;
    dut_->s_axi_wdata = value; dut_->s_axi_wstrb = 0xF; dut_->s_axi_wvalid = 1;
    dut_->s_axi_bready = 1;
    for (unsigned g = 0; g < 2048; ++g) {
        tick();
        if (fires_.aw) dut_->s_axi_awvalid = 0;
        if (fires_.w) dut_->s_axi_wvalid = 0;
        if (fires_.b) { dut_->s_axi_bready = 0; return; }
    }
    throw std::runtime_error("AXI write response timeout");
}

uint32_t GmStepHarness::read(uint16_t addr) {
    dut_->s_axi_araddr = addr; dut_->s_axi_arvalid = 1; dut_->s_axi_rready = 1;
    for (unsigned g = 0; g < 2048; ++g) {
        tick();
        if (fires_.ar) dut_->s_axi_arvalid = 0;
        if (fires_.r) { dut_->s_axi_rready = 0; return fires_.data; }
    }
    throw std::runtime_error("AXI read response timeout");
}

std::vector<uint8_t> GmStepHarness::aecp_transaction(uint16_t command, uint16_t seq,
                                                     const std::vector<uint8_t>& payload) {
    const size_t first = tx_frames_.size();
    control_.push_back({Kind::Aecp, seq, 0, payload, command, cyc_});
    for (uint64_t n = 0; n < 400000; ++n) {
        tick();
        for (size_t i = first; i < tx_frames_.size(); ++i) {
            const auto& f = tx_frames_[i];
            if (f.size() > 37 && be(f, 12, 2) == 0x22F0 && f[14] == 0xFB
                    && (f[15] & 0xF) == 1 && be(f, 34, 2) == seq
                    && (be(f, 36, 2) & 0x7FFF) == command)
                return f;
        }
    }
    return {};
}

std::vector<uint8_t> GmStepHarness::counters(uint16_t seq, uint16_t descriptor_type) {
    return aecp_transaction(0x0029, seq, {static_cast<uint8_t>(descriptor_type >> 8),
                                          static_cast<uint8_t>(descriptor_type), 0, 0});
}

//! One GET_COUNTERS quadlet: word 32 is counters_valid, 0..31 the block. A
//! missing answer validates nothing and reads a marker in every counter.
uint32_t GmStepHarness::counter_word(const std::vector<uint8_t>& response, unsigned word) {
    if (response.size() < 174 || word > 32) return word == 32 ? 0u : 0xDEADBEEFu;
    return static_cast<uint32_t>(be(response, word == 32 ? 42u : 46u + 4u * word, 4));
}

void GmStepHarness::reset() {
    dut_->axis_resetn = 0; dut_->gtx_resetn = 0;
    dut_->s_axi_awvalid = 0; dut_->s_axi_wvalid = 0; dut_->s_axi_arvalid = 0;
    dut_->s_axi_bready = 0; dut_->s_axi_rready = 0;
    dut_->m_axis_mac_tx_tready = 1;
    dut_->i_mac_speed = 2; dut_->i_link_up = 1; dut_->i_full_duplex = 1;
    dut_->i_mac_events = 0;
    dut_->i_mmcm_locked = 1;
    dut_->i_mmcm_ps_done = 0; dut_->i_mmcm_drp_rdy = 0; dut_->i_mmcm_drp_do = 0;
    dut_->i2s_sdout_i = 0; dut_->tdm_data_i = 0;
    dut_->tdm_bclk_i = 0; dut_->tdm_fsync_i = 0;
    dut_->clk_audio_i = 0; dut_->clk_tdm_i = 0;
    milan::tb::GptpLaunchObserver::tie_off(dut_);
    run_cycles(16);
    dut_->axis_resetn = 1; dut_->gtx_resetn = 1;
    run_cycles(64);
    write(0x108, 0x00000002); write(0x10C, 0x00000100);
    write(0x608, 0x020000FF); write(0x604, 0xFE000001);
    write(0x504, static_cast<uint32_t>(kPhcTickNs << 24));
    run_cycles(256);
}

//! Pdelay until asCapable, GM A's Announce and Sync until the fabric verdict
//! is healthy. GM A is seconds ahead of the reset PHC, so the first pair
//! after asCapable rises is a link-up pair above 20 us: one step.
void GmStepHarness::acquire() {
    trace_ = Trace{};
    peer_on_ = true;
    next_sync_ = cyc_; next_announce_ = cyc_;
    uint32_t stat = 0;
    for (unsigned poll = 0; poll < 200; ++poll) {
        run_cycles(kClkHz / 20);
        stat = read(0x77C);
        if ((stat & 0x10003) == 0x10002) break;
    }
    check_.hex("acquisition: CLKV healthy (asCapable, sync, tu clear)", stat & 0x10003, 0x10002);
    check_.dec("acquisition: the link-up pair stepped the PHC once", trace_.step_pulses, 1);
    check_.dec("acquisition: the counter saw exactly that step", trace_.steps, 1);
    check_.that("acquisition: that step exceeds the 20 us link-up threshold",
                trace_.step_ns > 20000 || trace_.step_ns < -20000);
    check_.hex("acquisition: the published grandmaster is GM A",
               (uint64_t(read(0x628)) << 32) | read(0x624), kGmA);
}

//! CRF sink, listener, talker and the clock source, then the two feeds.
void GmStepHarness::provision_media() {
    write(0x73C, 0x00020001); write(0x740, 0x02000000); write(0x738, 0x1);
    write(0x800, 0);
    write(0x814, 0x00020000); write(0x818, 0x02000000);
    write(0x824, 0x02006000); write(0x828, 0x02050220);
    write(0x810, 1);
    write(0x900, 1);
    for (unsigned ch = 0; ch < 8; ++ch) {
        write(0x904, 0x100 | ch);
        write(0x908, 0xD000 | ((ch & 1) << 8) | (ch / 2));
    }
    write(0x654, 0x00020003);
    run_cycles(feed_delay_);
    media_on_ = true;
    next_aaf_ = cyc_ + kAafPeriodCyc;
    next_crf_ = cyc_ + kSlotGuardCyc;
    run_cycles(kClkHz / 20);
    const auto set = aecp_transaction(0x0016, 0x7301, {0x00, 0x24, 0x00, 0x00,
                                                        0x00, kCrfClockSource, 0x00, 0x00});
    check_.dec("media: SET_CLOCK_SOURCE to the CRF answers SUCCESS",
               set.size() > 16 ? set[16] >> 3 : 255, 0);
    run_cycles(kClkHz / 10);
    check_.dec("media: the root resolves the CRF selection",
               dut_->rootp->milan_datapath__DOT__crf_clk_selected_r, 1);
    check_.dec("media: the CRF sink is locked", read(0x738) >> 31, 1);
    check_.hex("media: the talker gate is open", read(0x66C) & 8, 8);
}

void GmStepHarness::baseline() {
    const size_t pushes0 = pushes_.size();
    const size_t accepts0 = accepts_.size();
    const size_t talker0 = talker_.size();
    const uint64_t recentres0 = dut_->rootp->milan_datapath__DOT__rsp_recentres_w;
    run_cycles(kClkHz / 5);
    check_.that("baseline: the listener accepted PDUs", pushes_.size() - pushes0 > 100);
    size_t off_target = 0;
    unsigned lo = 255;
    unsigned hi = 0;
    for (size_t i = pushes0; i < pushes_.size(); ++i) {
        if (pushes_[i].second != kRenderTargetEvt) ++off_target;
        lo = std::min(lo, pushes_[i].second);
        hi = std::max(hi, pushes_[i].second);
    }
    unsigned at_lo = 255;
    unsigned at_hi = 0;
    for (size_t i = accepts0; i < accepts_.size(); ++i) {
        at_lo = std::min(at_lo, accepts_[i].second);
        at_hi = std::max(at_hi, accepts_[i].second);
    }
    printf("RENDER: fill after each push %u..%u events (target %u = setpoint %u + %u); "
           "fill at accept %u..%u (the accept phase, not graded)\n",
           lo, hi, kRenderTargetEvt, kRenderSetpointEvt, kRenderPduEvt, at_lo, at_hi);
    check_.dec("baseline: every PDU push leaves the #386 target fill", off_target, 0);
    size_t uncertain = 0;
    for (size_t i = talker0; i < talker_.size(); ++i) uncertain += talker_[i].tu;
    check_.that("baseline: the talker streams", talker_.size() - talker0 > 100);
    if (talker_.size() > talker0 + 1)
        talker_interval_ = double(talker_.back().cyc - talker_[talker0].cyc)
                         / double(talker_.size() - talker0 - 1);
    printf("TALKER: baseline interval %.1f cycles\n", talker_interval_);
    check_.dec("baseline: no talker PDU carries tu", uncertain, 0);
    check_.dec("baseline: no render recentre",
               dut_->rootp->milan_datapath__DOT__rsp_recentres_w - recentres0, 0);
}

//! GM B, 1.5 s ahead of GM A, is announced through the same parent and its
//! first Sync follows kGmSyncDelayCyc later. The peer's media timestamps
//! follow its grandmaster from the Announce on. Between the commit and the
//! step the talker's counters are read once more, so MEDIA_RESET is seen to
//! belong to the step rather than to the identity change.
void GmStepHarness::change_grandmaster() {
    const auto sout0 = counters(0x7310, 0x0006);
    sin0_accepts_.first = accepts_.size();
    const auto sin0 = counters(0x7311, 0x0005);
    sin0_accepts_.second = accepts_.size();
    const uint64_t recentres0 = dut_->rootp->milan_datapath__DOT__rsp_recentres_w;
    const uint64_t rails0 = dut_->rootp->milan_datapath__DOT__rsp_rails_w;
    const size_t talker0 = talker_.size();
    trace_ = Trace{};
    trace_.tu_prev = dut_->rootp->milan_datapath__DOT__clkv_tu_w;
    check_.dec("event: tu is clear before the change", trace_.tu_prev, 0);
    gm_id_ = kGmB; gm_priority_ = kPriorityB; gm_epoch_ += kGmStepNs;
    media_follows_sync_ = true;
    next_announce_ = cyc_;
    next_sync_ = cyc_ + kGmSyncDelayCyc;
    const uint64_t announced = cyc_;
    printf("EVENT: GM B announced at cycle %llu\n", static_cast<unsigned long long>(cyc_));
    while (!trace_.identity_cyc && cyc_ < announced + kGmSyncDelayCyc / 2) tick();
    const auto sout_mid = counters(0x7314, 0x0006);
    const uint64_t mid_cyc = cyc_;
    const uint64_t end = announced + kGmSyncDelayCyc + 5 * kQtickCyc;
    if (cyc_ < end) run_cycles(end - cyc_);
    grade_the_event(sout0, sout_mid, mid_cyc, sin0, recentres0, rails0, talker0);
}

void GmStepHarness::grade_the_event(const std::vector<uint8_t>& sout0,
                                    const std::vector<uint8_t>& sout_mid, uint64_t mid_cyc,
                                    const std::vector<uint8_t>& sin0, uint64_t recentres0,
                                    uint64_t rails0, size_t talker0) {
    printf("EVENT: identity %llu, counters read %llu, step pulse %llu, step %llu (%lld ns), "
           "tu rise %llu fall %llu\n",
           static_cast<unsigned long long>(trace_.identity_cyc),
           static_cast<unsigned long long>(mid_cyc),
           static_cast<unsigned long long>(trace_.step_pulse_cyc),
           static_cast<unsigned long long>(trace_.step_cyc),
           static_cast<long long>(trace_.step_ns),
           static_cast<unsigned long long>(trace_.tu_rise_cyc),
           static_cast<unsigned long long>(trace_.tu_fall_cyc));
    check_.that("event: the published grandmaster became GM B", trace_.identity_cyc != 0);
    check_.dec("event: the plane stepped the PHC exactly once", trace_.step_pulses, 1);
    check_.dec("event: the counter saw exactly that step", trace_.steps, 1);
    check_.that("event: the step is the 1.5 s between the grandmasters, within 1 us",
                trace_.step_ns > int64_t(kGmStepNs) - 1000
                && trace_.step_ns < int64_t(kGmStepNs) + 1000);
    check_.that("event: the step follows the commit", trace_.step_cyc > trace_.identity_cyc);
    check_.that("event: the counters were read between the commit and the step",
                mid_cyc > trace_.identity_cyc && mid_cyc < trace_.step_pulse_cyc);
    grade_uncertainty(talker0);
    const auto sout1 = counters(0x7312, 0x0006);
    sin1_accepts_.first = accepts_.size();
    const auto sin1 = counters(0x7313, 0x0005);
    sin1_accepts_.second = accepts_.size();
    grade_the_licence(talker0, sin0, sin1);
    grade_the_render(recentres0, rails0, trace_.identity_cyc);
    grade_the_restart(talker0, sout0, sout_mid, sout1);
}

//! REQ-PTP-08 and Milan Annex B.1.1: tu is already set in the first cycle
//! the bank names GM B, and clears only a holdover after the step.
void GmStepHarness::grade_uncertainty(size_t talker0) {
    check_.dec("tu: set in the first cycle the bank names GM B", trace_.tu_at_identity, 1);
    check_.that("tu: cleared after the step", trace_.tu_fall_cyc > trace_.step_cyc);
    const uint64_t held = trace_.tu_fall_cyc - trace_.step_cyc;
    printf("TU: held %llu cycles after the step (quarter tick %llu)\n",
           static_cast<unsigned long long>(held), static_cast<unsigned long long>(kQtickCyc));
    check_.that("tu: held at least the 0.25 s holdover after the step", held >= kQtickCyc);
    check_.that("tu: cleared within the holdover's bound", held <= 3 * kQtickCyc);
    check_.dec("tu: clear at the end of the window", dut_->rootp->milan_datapath__DOT__clkv_tu_w, 0);
    size_t wrong = 0;
    size_t graded_hold = 0;
    size_t graded_after = 0;
    for (size_t i = talker0; i < talker_.size(); ++i) {
        const TxPdu& p = talker_[i];
        const bool in_hold = p.cyc > trace_.identity_cyc + kWireSettleCyc
                          && p.cyc + kWireSettleCyc < trace_.tu_fall_cyc;
        const bool after = p.cyc > trace_.tu_fall_cyc + kWireSettleCyc;
        if (!in_hold && !after) continue;
        graded_hold += in_hold;
        graded_after += after;
        if (p.tu != in_hold) ++wrong;
    }
    check_.that("tu: talker PDUs graded inside the hold", graded_hold > 100);
    check_.that("tu: talker PDUs graded after tu clears", graded_after > 100);
    check_.dec("tu: every talker PDU carries the verdict of its instant", wrong, 0);
}

//! REQ-PTP-08: uncertainty never stops a stream. The talker keeps its gate
//! and its cadence to the end of the graded window, which ends here: the
//! silence after its last PDU counts as a pause. The listener keeps its lock.
void GmStepHarness::grade_the_licence(size_t talker0, const std::vector<uint8_t>& sin0,
                                      const std::vector<uint8_t>& sin1) {
    check_.hex("licence: the talker gate is open after the event", read(0x66C) & 8, 8);
    if (talker_.size() <= talker0) {
        check_.fail("licence: the talker sent PDUs across the event");
        return;
    }
    const uint64_t window_end = cyc_;
    size_t gaps = 0;
    uint64_t longest = window_end - talker_.back().cyc;
    for (size_t i = talker0 + 1; i < talker_.size(); ++i) {
        if (talker_[i].seq != uint8_t(talker_[i - 1].seq + 1)) ++gaps;
        longest = std::max(longest, talker_[i].cyc - talker_[i - 1].cyc);
    }
    check_.dec("licence: no talker sequence gap across the event", gaps, 0);
    const uint64_t span = window_end - talker_[talker0].cyc;
    const uint64_t sent = talker_.size() - talker0 - 1;
    const double expected = double(span) / talker_interval_;
    printf("TALKER: %llu PDUs over %llu cycles to the window end (baseline rate: %.0f), "
           "longest pause %llu, last PDU %llu cycles before the end\n",
           static_cast<unsigned long long>(sent), static_cast<unsigned long long>(span),
           expected, static_cast<unsigned long long>(longest),
           static_cast<unsigned long long>(window_end - talker_.back().cyc));
    check_.that("licence: the talker never pauses beyond four of its intervals",
                double(longest) <= kTalkerPauseIntervals * talker_interval_);
    check_.that("licence: the talker keeps its baseline rate within 1%",
                double(sent) > 0.99 * expected && double(sent) < 1.01 * expected);
    //! FRAMES_RX moved by the accepts between the two snapshots, each taken
    //! somewhere inside its own transaction
    const uint64_t frames = counter_word(sin1, 11) - counter_word(sin0, 11);
    const size_t fewest = sin1_accepts_.first - sin0_accepts_.second;
    const size_t most = sin1_accepts_.second - sin0_accepts_.first;
    printf("LISTENER: counters valid 0x%x / 0x%x, EARLY_TIMESTAMP +%u, LATE_TIMESTAMP +%u, "
           "FRAMES_RX +%llu (accepts seen %zu..%zu)\n", counter_word(sin0, 32),
           counter_word(sin1, 32), counter_word(sin1, 10) - counter_word(sin0, 10),
           counter_word(sin1, 9) - counter_word(sin0, 9),
           static_cast<unsigned long long>(frames), fewest, most);
    check_.hex("licence: both Stream Input answers carry MEDIA_UNLOCKED and FRAMES_RX",
               counter_word(sin0, 32) & counter_word(sin1, 32) & kSinCountersUsed,
               kSinCountersUsed);
    check_.that("licence: FRAMES_RX advances by the PDUs the listener accepted",
                frames >= fewest && frames <= most && fewest > 100);
    check_.dec("licence: the listener stays locked (MEDIA_UNLOCKED unchanged)",
               counter_word(sin1, 1) - counter_word(sin0, 1), 0);
}

//! The #386 stage re-centres once, for the step, and holds its law throughout.
void GmStepHarness::grade_the_render(uint64_t recentres0, uint64_t rails0, uint64_t event_cyc) {
    const uint64_t recentres = dut_->rootp->milan_datapath__DOT__rsp_recentres_w - recentres0;
    size_t outside = 0;
    for (uint64_t at : trace_.recentre_cycs) {
        printf("RENDER: counted recentre at cycle %llu (step pulse %+lld)\n",
               static_cast<unsigned long long>(at),
               static_cast<long long>(at) - static_cast<long long>(trace_.step_pulse_cyc));
        if (at <= trace_.step_pulse_cyc || at > trace_.step_pulse_cyc + kRebaseWindowCyc)
            ++outside;
    }
    printf("RENDER: %llu counted recentres from %llu trigger pulses\n",
           static_cast<unsigned long long>(recentres),
           static_cast<unsigned long long>(trace_.render_triggers));
    check_.dec("render: the GM change is one counted re-base event", recentres, 1);
    check_.dec("render: every counted re-base lands at a PDU end right after the step",
               outside, 0);
    check_.dec("render: no reset rail across the event",
               dut_->rootp->milan_datapath__DOT__rsp_rails_w - rails0, 0);
    size_t off_target = 0;
    size_t graded = 0;
    for (const auto& [at, fill] : pushes_) {
        if (at < event_cyc) continue;
        ++graded;
        if (fill != kRenderTargetEvt) ++off_target;
    }
    check_.that("render: PDUs accepted across the event", graded > 100);
    check_.dec("render: every PDU push leaves the target fill across the event", off_target, 0);
}

//! IEEE 1722-2016 4.4.4.3 and Milan Table 5.4: the step restarts the media
//! clock once on the wire, and MEDIA_RESET counts that one toggle. Both are
//! the step's: the toggle is first sent right after the step pulse, and the
//! count has not moved at the reading taken between the commit and the step.
void GmStepHarness::grade_the_restart(size_t talker0, const std::vector<uint8_t>& sout0,
                                      const std::vector<uint8_t>& sout_mid,
                                      const std::vector<uint8_t>& sout1) {
    const double window = kToggleWindowIntervals * talker_interval_;
    size_t toggles = 0;
    size_t outside = 0;
    for (size_t i = talker0 + 1; i < talker_.size(); ++i) {
        if (talker_[i].mr == talker_[i - 1].mr) continue;
        ++toggles;
        const uint64_t at = talker_[i].cyc;
        printf("RESTART: mr toggle first sent at cycle %llu (step pulse %+lld)\n",
               static_cast<unsigned long long>(at),
               static_cast<long long>(at) - static_cast<long long>(trace_.step_pulse_cyc));
        if (at <= trace_.step_pulse_cyc || double(at - trace_.step_pulse_cyc) > window)
            ++outside;
    }
    check_.dec("restart: the outgoing mr toggles exactly once", toggles, 1);
    check_.dec("restart: every mr toggle is first sent right after the step", outside, 0);
    check_.hex("restart: the Stream Output counters are valid before the change",
               counter_word(sout0, 32), 0x1F);
    check_.hex("restart: the Stream Output counters are valid between commit and step",
               counter_word(sout_mid, 32), 0x1F);
    check_.hex("restart: the Stream Output counters are valid after the event",
               counter_word(sout1, 32), 0x1F);
    check_.dec("restart: MEDIA_RESET does not move between the commit and the step",
               counter_word(sout_mid, 2) - counter_word(sout0, 2), 0);
    check_.dec("restart: the talker's MEDIA_RESET counts exactly one",
               counter_word(sout1, 2) - counter_word(sout0, 2), 1);
}

//! Wire-driven policy verdict from the real engine through the actual
//! shadow/datapath/servo port. Unit tests grade lock and rate integration;
//! this compressed-clock leg grades transport and every release-tail edge.
void GmStepHarness::check_slew_connection() {
    slew_origin_override_ = true;
    slew_offset_ns_ = 0;
    run_cycles(3 * kSyncPeriodCyc);
    check_.dec("slew path: in-band pairs clear the plane level",
               dut_->rootp->milan_datapath__DOT__gptp_slew_active_w, 0);
    const unsigned steps0 = trace_.steps;
    slew_probe_ = true;
    slew_offset_ns_ = 90000;
    run_cycles(kSyncPeriodCyc + 10000);
    const int32_t offset = static_cast<int32_t>(dut_->rootp->milan_datapath__DOT__gptp_pub_offset_w);
    check_.that("slew path: consumed offset is between 80 and 100 us",
                offset > 80000 && offset < 100000);
    check_.dec("slew path: the plane raises its level",
               dut_->rootp->milan_datapath__DOT__gptp_slew_active_w, 1);
    check_.that("slew path: the actual servo receives the level", slew_high_samples_ > 100);
    slew_offset_ns_ = 0;
    run_cycles(3 * kSyncPeriodCyc);
    check_.dec("slew path: measured completion lowers the level",
               dut_->rootp->milan_datapath__DOT__gptp_slew_active_w, 0);
    check_.dec("slew path: completion happened once", slew_falls_, 1);
    check_.dec("slew path: every staged sample covers the PHC tail", slew_alignment_errors_, 0);
    check_.dec("slew path: a policy slew never steps the PHC", trace_.steps - steps0, 0);
    slew_probe_ = false;
}

int GmStepHarness::run() {
    printf("gmstep: 2 MHz fabric, 8 ns PHC, quarter tick %llu cycles\n",
           static_cast<unsigned long long>(kQtickCyc));
    try {
        reset();
        acquire();
        provision_media();
        baseline();
        change_grandmaster();
        check_slew_connection();
    } catch (const std::exception& e) {
        check_.fail(e.what());
        printf("NOT RUN: the remaining phases after a bounded transport failure\n");
    }
    printf("simulated_cycles=%llu\n", static_cast<unsigned long long>(cyc_));
    return check_.report();
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2 && argc != 3) {
        fprintf(stderr, "usage: %s <aem image> [feed delay cycles]\n", argv[0]);
        return 2;
    }
    uint64_t feed_delay = 0;
    if (argc == 3) {
        const std::string text = argv[2];
        if (text.empty() || text.find_first_not_of("0123456789") != std::string::npos
                || text.size() > 6) {
            fprintf(stderr, "gmstep: the feed delay %s is not a cycle count below 10^6\n", argv[2]);
            return 2;
        }
        feed_delay = std::stoull(text);
    }
    std::ifstream file(argv[1], std::ios::binary);
    std::vector<uint8_t> image{std::istreambuf_iterator<char>(file),
                               std::istreambuf_iterator<char>()};
    if (image.empty()) {
        fprintf(stderr, "gmstep: the AEM image %s is missing or empty\n", argv[1]);
        return 2;
    }
    printf("gmstep: feed delay %llu cycles\n", static_cast<unsigned long long>(feed_delay));
    GmStepHarness harness(std::move(image), feed_delay);
    return harness.run();
}
