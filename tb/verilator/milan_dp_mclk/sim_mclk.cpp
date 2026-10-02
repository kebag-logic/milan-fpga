// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_mclk - media-clock following of one selected AAF or CRF source at the
// root (#629, docs/design/MEDIA_CLOCK_FOLLOWING.md, the milan_datapath rows
// of its test plan).
//
// THE PLANT. The servo's fine phase shift is closed through the behavioral
// MMCM of tb/verilator/mmcm_servo/mmcm_model.h: each completed PSDONE moves
// the modelled audio clock's next edge by one step, so a sustained step rate
// IS a frequency offset. The step is 1/59 ns, the servo's own GAIN_NUM_P
// (KL_mmcm_drp_servo: 59 steps per ns per 1 ms tick, one ppm), so the plant
// gain is the one the servo is designed for. Two things are scaled, neither
// of them loop arithmetic: PSCLK is the 4 MHz fabric clock, and the model
// answers PSDONE 2 PSCLK cycles after PSEN rather than UG472's 12 (the servo
// waits for PSDONE and never counts the cycles), so the actuator carries the
// trims this leg plants at a fabric rate the simulator can run.
//
// THE CLOCKS (one femtosecond wheel):
//   axis   MCLK_HZ_TB = 4 MHz, which is also gtx_clk and PSCLK; the PHC
//          advances PTP_INCR = 250 ns a cycle, so gPTP time IS wheel time;
//   audio  the shipping plan, 100 MHz x 391/1591 (-10.64 ppm against
//          24.576 MHz), plus the modelled phase steps; clk_tdm_i rides it,
//          so the TDM8 frame is the physical 48 kHz grid the aligner reads.
//
// THE TALKERS. Two AAF talkers (listeners 0 and 1, the 48 kHz Base format,
// 8 channels) and one CRF talker (the CRF sink), each on its own media clock
// at a planted offset. A talker's PDU i is sent when its media clock reaches
// it, and carries that instant plus a 2 ms presentation offset: ideal
// timestamps, the meter's own suite owns their error shapes. Offsets follow
// the servo suites' convention: a -6 ppm talker's 125 us of samples span
// 125,000 / (1 - 6e-6) ns of gPTP time.
//
// THE TAPS. The clock-source selection is poked into the processor's stored
// row (the documented clksrc_r tap obj_aclk uses; the AECP chain into that
// row is tb/verilator/milan_dp's [CLKSRC-WALK]). tu is the test double's
// register (clkv_double.sv). Everything graded is a public net, a CSR read or
// a frame on the wire.

#include "../../common/verilator_harness.hpp"
#include "../mmcm_servo/mmcm_model.h"
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"

#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <deque>
#include <functional>
#include <string>
#include <vector>

namespace {

constexpr int64_t kMclkHz = MCLK_HZ_TB;
constexpr int64_t kFsPerS = 1'000'000'000'000'000;
constexpr int64_t kFsPerNs = 1'000'000;
constexpr int64_t kAxisHalfFs = kFsPerS / 2 / kMclkHz;
//! half an audio period on the plan, 100 MHz x 391/1591: 1591e7 / 782 fs
constexpr int64_t kAudHalfNum = 15'910'000'000;
constexpr int64_t kAudHalfDen = 782;
constexpr double kAudioNomHz = 24.576e6;
constexpr double kPlanPpm = (1e8 * 391.0 / 1591.0 / kAudioNomHz - 1.0) * 1e6;
//! the servo's GAIN_NUM_P: 59 fine steps per ns
constexpr double kPsStepFs = 1e6 / 59.0;
constexpr int kPsLatCycles = 2;
constexpr int64_t kAafPduNs = 125'000;           //! 6 samples at 48 kHz
constexpr int64_t kCrfPduNs = 2'000'000;         //! 96 samples at 48 kHz
constexpr int64_t kPresentNs = 2'000'000;        //! Milan's default offset
constexpr int kAafChans = 8;
constexpr int kAafPayload = kAafChans * 6 * 4;   //! 192 = 24 x 8 octets
constexpr int kIfgCycles = 2;
constexpr int kAxiGuard = 4096;

// clock-source indexes of the two-stream shape (gen_mclk_shape.py asserts
// them on the generated header before anything is elaborated)
constexpr uint16_t kSrcInternal = 0;
constexpr uint16_t kSrcCrf = 1;
constexpr uint16_t kSrcAaf0 = 2;
constexpr uint16_t kSrcAaf1 = 3;

// servo states (KL_mmcm_drp_servo, MCSRV_STAT[2:0])
constexpr int kStIdle = 0;
constexpr int kStAcquire = 3;
constexpr int kStLocked = 4;
constexpr int kStHoldover = 5;

//! One talker on its own media clock. PDU i is due when that clock reaches
//! it; `muted` keeps the clock and the sequence running with nothing sent
//! (a cable pull), `lost` drops single PDUs (a lossy network).
struct Talker {
    bool crf = false;
    uint8_t uid = 0;                     //! SID byte 7 and the DA's low byte
    bool on = false;
    bool muted = false;
    double ppm = 0.0;
    int mr = 0;
    uint8_t seq = 0;
    uint64_t n = 0;                      //! the next PDU's index
    long double anchor_ns = 0.0L;        //! media time of PDU anchor_n
    uint64_t anchor_n = 0;
    std::function<bool(uint64_t)> lost;
    uint64_t sent = 0;

    int64_t period_ns() const { return crf ? kCrfPduNs : kAafPduNs; }
    long double media_ns(uint64_t i) const {
        const long double sp = static_cast<long double>(period_ns()) / (1.0L + ppm * 1e-6L);
        return anchor_ns + static_cast<long double>(i - anchor_n) * sp;
    }
    //! a step of the offset that keeps the talker's phase
    void set_ppm(double p) {
        anchor_ns = media_ns(n);
        anchor_n = n;
        ppm = p;
    }
};

class MclkHarness {
 public:
    explicit MclkHarness(milan::tb::Checker& check) : check_(check) {}
    int run(const std::string& mode);

    Vmilan_datapath* dut = nullptr;

 private:
    milan::tb::Checker& check_;
    MmcmModel mm_{};

    // ---- the wheel -----------------------------------------------------
    int64_t t_fs_ = 0;
    int64_t next_axis_ = kAxisHalfFs;
    int64_t aud_base_ = 0;
    int64_t aud_acc_ = 0;
    int64_t next_audio_ = 0;
    uint64_t axis_cycle_ = 0;
    uint64_t audio_cycles_ = 0;          //! clk_audio rising edges

    // ---- the MAC RX driver ---------------------------------------------
    std::deque<std::vector<uint64_t>> rxq_;
    std::vector<uint64_t> rx_cur_;
    size_t rx_idx_ = 0;
    int rx_gap_ = 0;
    bool rx_acc_ = false;

    // ---- the MAC TX sniffer --------------------------------------------
    std::vector<uint8_t> tx_fr_;

 public:
    //! per output: the wire's mr level, its toggles, PDUs since a toggle,
    //! and the shortest hold seen after one
    struct OutWatch {
        long pdus = 0;
        int mr = -1;
        long toggles = 0;
        long since = 0;
        long min_hold = 1L << 30;
    };
    OutWatch aaf_out{};
    OutWatch crf_out{};

    Talker aaf0{};
    Talker aaf1{};
    Talker crfk{};

    // what the run observed, sampled every fabric cycle
    long restart_pulses = 0;             //! mcr_restart_p_w
    long src_recentres = 0;              //! the #386 clock-source trigger
    long holdover_entries = 0;
    int last_state = 0;

    // ---- stepping -----------------------------------------------------------
    void step();
    void axis_fall();
    void axis_rise();
    void audio_edge();
    void run_for_ns(int64_t ns) { const int64_t stop = t_fs_ + ns * kFsPerNs; while (t_fs_ < stop) step(); }
    void cycles(long n) { const uint64_t stop = axis_cycle_ + static_cast<uint64_t>(n); while (axis_cycle_ < stop) step(); }
    double now_s() const { return static_cast<double>(t_fs_) * 1e-15; }

    // ---- stimulus -------------------------------------------------------------
    void talker_due(Talker& t);
    void send_aaf(Talker& t);
    void send_crf(Talker& t);
    void enqueue(const std::vector<uint8_t>& f);
    void sniff_tx();
    void observe();

    // ---- the CSR bus ----------------------------------------------------------
    void axi_write(uint16_t a, uint32_t d);
    uint32_t axi_read(uint16_t a);

    // ---- taps -------------------------------------------------------------------
    int servo_state() const { return static_cast<int>(dut->rootp->milan_datapath__DOT__mcsrv_stat_w & 7u); }
    double trim_ppm() const { return static_cast<int16_t>(dut->rootp->milan_datapath__DOT__mcsrv_stat_w >> 16) / 16.0; }
    uint32_t meter_stat() const { return dut->rootp->milan_datapath__DOT__aafm_stat_w; }
    uint32_t ctr_locked() const { return dut->rootp->milan_datapath__DOT__ctr_mlock_r; }
    uint32_t ctr_unlocked() const { return dut->rootp->milan_datapath__DOT__ctr_munlock_r; }
    void select(uint16_t ix);
    void set_tu(bool tu) { dut->rootp->milan_datapath__DOT__ptp_clock_validity__DOT__tu_tap_r = tu ? 1 : 0; }

    // ---- set-up and measurement --------------------------------------------------
    void reset_and_provision();
    void bind_listener(unsigned ix, uint8_t uid);
    double media_clock_ppm_over(int64_t ns);
    bool run_until_state(int want, int64_t budget_ns);
    void ck(const char* what, bool ok) { check_.that(what, ok); }
    void ckv(const char* what, uint64_t got, uint64_t exp) { check_.dec(what, got, exp); }

    // ---- the two grids (the INTERNAL row): media_tick_p on the fabric
    //      clock, the TDM frame sync on the audio clock, timed on the wheel
    bool grid_on_ = false;
    long tick_n_ = 0;
    int64_t tick_first_ = 0;
    int64_t tick_last_ = 0;
    long fsync_n_ = 0;
    int64_t fsync_first_ = 0;
    int64_t fsync_last_ = 0;
    int fsync_prev_ = 0;
    void grid_window(int64_t ns);
    double grid_ppm() const;

    // ---- the C1 counters, sampled every millisecond of the run
    uint64_t next_ctr_sample_ = 0;
    long ctr_bad_ = 0;
    void sample_counters();

    // ---- the rows ------------------------------------------------------------
    void boot();
    void row_internal(int64_t settle_ns);
    void row_select_aaf0();
    void row_trim_holds_until_the_meter_rate();
    void follow_to_locked(const char* tag, uint32_t locked0);
    void row_follows(const char* tag, const Talker& t);
    void row_csr_words(bool full);
    void row_echo();
    void row_loss_leg(int64_t ns);
    void row_aaf_loss(bool full);
    void row_w2_switch_to_crf(bool full);
    void row_select_crf();
    void row_crf_loss();
    //! what one source switch moved, over the gap after it
    struct SwitchDelta {
        long pulses = 0;
        long aaf_toggles = 0;
        long crf_toggles = 0;
        uint32_t aaf_mreset = 0;
        uint32_t crf_mreset = 0;
        long recentres = 0;
    };
    SwitchDelta switch_once(uint16_t to, int64_t gap_ns);
    uint32_t mreset(unsigned ctx) const { return dut->rootp->milan_datapath__DOT__talker_diag__DOT__mreset_r[ctx]; }
    void row_switch_sweep(int phases, bool grade_slips);
    void row_switch_recentres();
    void row_switch_onto_a_silent_talker();
    void row_internal_dwell();
    void leg_a();
    void leg_b();
    void leg_c();
    void report_counters();
};

// =============================================================================
//  the wheel
// =============================================================================

void MclkHarness::step() {
    if (next_axis_ <= next_audio_) {
        t_fs_ = next_axis_;
        next_axis_ += kAxisHalfFs;
        if (dut->axis_clk) axis_fall(); else axis_rise();
    } else {
        t_fs_ = next_audio_;
        audio_edge();
    }
}

void MclkHarness::axis_fall() {
    dut->axis_clk = 0;
    dut->gtx_clk = 0;
    dut->i_ps_clk = 0;
    dut->eval();
    //! the beat on the bus now is the one the coming rising edge takes
    rx_acc_ = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
}

void MclkHarness::axis_rise() {
    dut->axis_clk = 1;
    dut->gtx_clk = 1;
    dut->i_ps_clk = 1;
    dut->eval();
    axis_cycle_++;
    // the MMCM: DRP and PS on this same edge, outputs for the next one
    mm_.dclk_edge(dut->o_mmcm_drp_addr, dut->o_mmcm_drp_en, dut->o_mmcm_drp_we,
                  dut->o_mmcm_drp_di, dut->o_mmcm_rst);
    dut->i_mmcm_drp_rdy = mm_.drdy;
    dut->i_mmcm_drp_do = mm_.dout;
    mm_.psclk_edge(dut->o_mmcm_ps_en, dut->o_mmcm_ps_incdec, dut->o_mmcm_rst);
    dut->i_mmcm_ps_done = mm_.psdone;
    dut->i_mmcm_locked = mm_.locked;
    sniff_tx();
    observe();
    // the RX driver: advance on an accepted beat, then present the next
    if (rx_acc_) rx_idx_++;
    if (!rx_cur_.empty() && rx_idx_ >= rx_cur_.size()) { rx_cur_.clear(); rx_idx_ = 0; rx_gap_ = kIfgCycles; }
    if (rx_cur_.empty() && rx_gap_ > 0) rx_gap_--;
    else if (rx_cur_.empty() && !rxq_.empty()) { rx_cur_ = std::move(rxq_.front()); rxq_.pop_front(); rx_idx_ = 0; }
    const bool v = !rx_cur_.empty();
    dut->s_axis_mac_rx_tvalid = v;
    dut->s_axis_mac_rx_tdata = v ? rx_cur_[rx_idx_] : 0;
    dut->s_axis_mac_rx_tkeep = 0xFF;
    dut->s_axis_mac_rx_tlast = v && (rx_idx_ + 1 == rx_cur_.size());
    talker_due(aaf0);
    talker_due(aaf1);
    talker_due(crfk);
}

void MclkHarness::audio_edge() {
    aud_acc_ += kAudHalfNum;
    aud_base_ += aud_acc_ / kAudHalfDen;
    aud_acc_ %= kAudHalfDen;
    next_audio_ = aud_base_ + static_cast<int64_t>(std::llround(mm_.audio_adj_fs));
    if (next_audio_ <= t_fs_) next_audio_ = t_fs_ + 1000;
    const uint8_t a = dut->clk_audio_i ? 0 : 1;
    dut->clk_audio_i = a;
    dut->clk_tdm_i = a;
    dut->eval();
    if (a) audio_cycles_++;
    if (grid_on_) {
        const int f = dut->tdm_fsync_o;
        if (f && !fsync_prev_) {
            if (fsync_n_ == 0) fsync_first_ = t_fs_;
            fsync_last_ = t_fs_;
            fsync_n_++;
        }
        fsync_prev_ = f;
    }
}

// =============================================================================
//  stimulus and observation
// =============================================================================

void MclkHarness::talker_due(Talker& t) {
    if (!t.on) return;
    const long double due_fs = t.media_ns(t.n) * static_cast<long double>(kFsPerNs);
    if (static_cast<long double>(t_fs_) < due_fs) return;
    const bool drop = t.muted || (t.lost && t.lost(t.n));
    if (!drop) {
        if (t.crf) send_crf(t); else send_aaf(t);
        t.sent++;
    }
    t.seq++;
    t.n++;
}

void MclkHarness::send_aaf(Talker& t) {
    std::vector<uint8_t> f(38 + kAafPayload, 0);
    const std::array<uint8_t, 6> dmac = {0x91, 0xE0, 0xF0, 0x00, 0x2A, static_cast<uint8_t>(0x02 + 2 * t.uid)};
    const std::array<uint8_t, 6> src = {0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
    std::memcpy(f.data(), dmac.data(), dmac.size());
    std::memcpy(f.data() + 6, src.data(), src.size());
    f[12] = 0x22; f[13] = 0xF0;
    f[14] = 0x02;                                         // AAF
    f[15] = static_cast<uint8_t>(0x81 | (t.mr ? 0x08 : 0x00));   // sv, mr, tv
    f[16] = t.seq;
    f[17] = 0x00;                                         // tu clear
    const std::array<uint8_t, 8> sid = {0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, t.uid};
    std::memcpy(f.data() + 18, sid.data(), sid.size());
    const uint32_t ts = static_cast<uint32_t>(
        static_cast<uint64_t>(std::floor(t.media_ns(t.n))) + kPresentNs);
    f[26] = static_cast<uint8_t>(ts >> 24); f[27] = static_cast<uint8_t>(ts >> 16);
    f[28] = static_cast<uint8_t>(ts >> 8);  f[29] = static_cast<uint8_t>(ts);
    f[30] = 0x02;                                         // INT_32BIT
    f[31] = static_cast<uint8_t>(0x05 << 4);              // nsr 48 kHz
    f[32] = static_cast<uint8_t>(kAafChans);
    f[33] = 32;
    f[34] = static_cast<uint8_t>(kAafPayload >> 8);
    f[35] = static_cast<uint8_t>(kAafPayload & 0xFF);
    enqueue(f);
}

void MclkHarness::send_crf(Talker& t) {
    std::vector<uint8_t> f(64, 0);
    const std::array<uint8_t, 6> dmac = {0x91, 0xE0, 0xF0, 0x00, 0x2A, 0x03};
    const std::array<uint8_t, 6> src = {0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
    std::memcpy(f.data(), dmac.data(), dmac.size());
    std::memcpy(f.data() + 6, src.data(), src.size());
    f[12] = 0x22; f[13] = 0xF0;
    f[14] = 0x04;                                         // CRF
    f[15] = static_cast<uint8_t>(0x80 | (t.mr ? 0x08 : 0x00));
    f[16] = t.seq;
    f[17] = 0x01;                                         // CRF_AUDIO_SAMPLE
    const std::array<uint8_t, 8> sid = {0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, t.uid};
    std::memcpy(f.data() + 18, sid.data(), sid.size());
    f[28] = 0xBB; f[29] = 0x80;                           // pull 0, 48000
    f[31] = 0x08;                                         // crf_data_length
    f[33] = 96;                                           // timestamp_interval
    const uint64_t ts = static_cast<uint64_t>(std::floor(t.media_ns(t.n))) + kPresentNs;
    for (int i = 0; i < 8; i++) f[34 + i] = static_cast<uint8_t>(ts >> (8 * (7 - i)));
    enqueue(f);
}

void MclkHarness::enqueue(const std::vector<uint8_t>& f) {
    std::vector<uint64_t> beats;
    for (size_t b = 0; b < (f.size() + 7) / 8; b++) {
        uint64_t v = 0;
        for (size_t j = 0; j < 8; j++)
            if (b * 8 + j < f.size()) v |= static_cast<uint64_t>(f[b * 8 + j]) << (8 * j);
        beats.push_back(v);
    }
    rxq_.push_back(std::move(beats));
}

void MclkHarness::sniff_tx() {
    if (!dut->m_axis_mac_tx_tvalid) return;
    for (int l = 0; l < 8; l++)
        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
            tx_fr_.push_back(static_cast<uint8_t>((dut->m_axis_mac_tx_tdata >> (8 * l)) & 0xFF));
    if (!dut->m_axis_mac_tx_tlast) return;
    const size_t off = (tx_fr_.size() > 17 && tx_fr_[12] == 0x81 && tx_fr_[13] == 0x00) ? 4 : 0;
    if (tx_fr_.size() >= 30 + off && tx_fr_[12 + off] == 0x22 && tx_fr_[13 + off] == 0xF0) {
        const uint8_t st = tx_fr_[14 + off];
        //! talker 0's AAF output (stream_id uid 0) and the CRF output
        OutWatch* w = (st == 0x04) ? &crf_out : ((st == 0x02 && tx_fr_[25 + off] == 0) ? &aaf_out : nullptr);
        if (w != nullptr) {
            const int mr = (tx_fr_[15 + off] >> 3) & 1;
            w->pdus++;
            if (w->mr >= 0 && mr != w->mr) {
                if (w->toggles > 0 && w->since < w->min_hold) w->min_hold = w->since;
                w->toggles++;
                w->since = 0;
            }
            w->since++;
            w->mr = mr;
        }
    }
    tx_fr_.clear();
}

void MclkHarness::observe() {
    auto* rp = dut->rootp;
    if (rp->milan_datapath__DOT__mcr_restart_p_w) restart_pulses++;
    if (rp->milan_datapath__DOT__src_recentre_p_r) src_recentres++;
    const int st = static_cast<int>(rp->milan_datapath__DOT__mcsrv_stat_w & 7u);
    if (st == kStHoldover && last_state != kStHoldover) holdover_entries++;
    last_state = st;
    if (grid_on_ && rp->milan_datapath__DOT__media_tick_p) {
        if (tick_n_ == 0) tick_first_ = t_fs_;
        tick_last_ = t_fs_;
        tick_n_++;
    }
    if (axis_cycle_ >= next_ctr_sample_) {
        sample_counters();
        next_ctr_sample_ = axis_cycle_ + static_cast<uint64_t>(kMclkHz / 1000);
    }
}

// =============================================================================
//  the CSR bus (AXI4-Lite, one access at a time, on the wheel)
// =============================================================================

void MclkHarness::axi_write(uint16_t a, uint32_t d) {
    dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
    dut->s_axi_wdata = d;  dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
    dut->s_axi_bready = 1;
    for (int g = 0; g < kAxiGuard; g++) {
        const bool aw = dut->s_axi_awready;
        const bool w = dut->s_axi_wready;
        cycles(1);
        if (aw) dut->s_axi_awvalid = 0;
        if (w) dut->s_axi_wvalid = 0;
        if (!dut->s_axi_awvalid && !dut->s_axi_wvalid && dut->s_axi_bvalid) break;
    }
    cycles(1);
    dut->s_axi_bready = 0;
}

uint32_t MclkHarness::axi_read(uint16_t a) {
    dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
    uint32_t r = 0;
    for (int g = 0; g < kAxiGuard; g++) {
        const bool ar = dut->s_axi_arready;
        cycles(1);
        if (ar) dut->s_axi_arvalid = 0;
        if (!dut->s_axi_arvalid && dut->s_axi_rvalid) { r = dut->s_axi_rdata; break; }
    }
    cycles(1);
    dut->s_axi_rready = 0;
    return r;
}

// =============================================================================
//  set-up and measurement
// =============================================================================

void MclkHarness::select(uint16_t ix) {
    dut->rootp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r[0] = ix;
}

void MclkHarness::bind_listener(unsigned ix, uint8_t uid) {
    constexpr uint16_t kStrmSel = 0x800;
    constexpr uint16_t kStrmwCtrl = 0x810;
    constexpr uint16_t kStrmwSidLo = 0x814;
    constexpr uint16_t kStrmwSidHi = 0x818;
    constexpr uint16_t kStrmwFmtLo = 0x824;
    constexpr uint16_t kStrmwFmtHi = 0x828;
    axi_write(kStrmSel, ix);
    axi_write(kStrmwSidLo, 0x00020000u | uid);            // 02:00:00:00:00:02:00:uid
    axi_write(kStrmwSidHi, 0x02000000u);
    axi_write(kStrmwFmtLo, 0x02006000u);
    axi_write(kStrmwFmtHi, 0x02050220u);
    axi_write(kStrmwCtrl, 1);
}

void MclkHarness::reset_and_provision() {
    mm_.regs[0x08] = 0x0595;
    mm_.regs[0x09] = 0x0080;
    mm_.step_fs = kPsStepFs;
    mm_.ps_lat = kPsLatCycles;
    dut->axis_resetn = 0;
    dut->gtx_resetn = 0;
    dut->m_axis_mac_tx_tready = 1;
    dut->i_mmcm_locked = 1;
    next_audio_ = kAudHalfNum / kAudHalfDen;
    aud_base_ = next_audio_;
    cycles(64);
    dut->axis_resetn = 1;
    dut->gtx_resetn = 1;
    cycles(256);
    constexpr uint16_t kMacAlo = 0x108;
    constexpr uint16_t kMacAhi = 0x10C;
    constexpr uint16_t kAafCtrl = 0x654;
    constexpr uint16_t kCrfCtrl = 0x738;
    constexpr uint16_t kCrfSidLo = 0x73C;
    constexpr uint16_t kCrfSidHi = 0x740;
    constexpr uint16_t kCrftCtrl = 0x750;
    axi_write(kMacAlo, 0x00000002);
    axi_write(kMacAhi, 0x00000100);
    bind_listener(0, 0);
    bind_listener(1, 2);
    axi_write(kCrfSidLo, 0x00020001);
    axi_write(kCrfSidHi, 0x02000000);
    axi_write(kCrfCtrl, 0x1);
    axi_write(kAafCtrl, 0x3);                             // talker 0: enable, bypass
    axi_write(kCrftCtrl, 0x1);                            // the CRF output
}

//! The media clock's offset from 48 kHz nominal over the next `ns` of gPTP
//! time, read off the modelled audio clock's own edges.
double MclkHarness::media_clock_ppm_over(int64_t ns) {
    const uint64_t c0 = audio_cycles_;
    const int64_t t0 = t_fs_;
    run_for_ns(ns);
    const double secs = static_cast<double>(t_fs_ - t0) * 1e-15;
    return (static_cast<double>(audio_cycles_ - c0) / (secs * kAudioNomHz) - 1.0) * 1e6;
}

bool MclkHarness::run_until_state(int want, int64_t budget_ns) {
    const int64_t stop = t_fs_ + budget_ns * kFsPerNs;
    while (t_fs_ < stop) {
        if (servo_state() == want) return true;
        cycles(64);
    }
    return servo_state() == want;
}


void MclkHarness::sample_counters() {
    const uint32_t l = ctr_locked();
    const uint32_t u = ctr_unlocked();
    if (!(l == u || l == u + 1)) ctr_bad_++;
}

void MclkHarness::grid_window(int64_t ns) {
    tick_n_ = 0;
    fsync_n_ = 0;
    fsync_prev_ = dut->tdm_fsync_o;
    grid_on_ = true;
    run_for_ns(ns);
    grid_on_ = false;
}

//! The packet grid's rate against the TDM frame's, in ppm: NEGATIVE = the
//! frame is slower. Both periods are wheel time, so the fabric clock's
//! 250 ns cycle quantises only the tick side.
double MclkHarness::grid_ppm() const {
    if (tick_n_ < 2 || fsync_n_ < 2) return 1e9;
    const double t_media = static_cast<double>(tick_last_ - tick_first_) / static_cast<double>(tick_n_ - 1);
    const double t_fsync = static_cast<double>(fsync_last_ - fsync_first_) / static_cast<double>(fsync_n_ - 1);
    return (t_media / t_fsync - 1.0) * 1e6;
}

// =============================================================================
//  the rows
// =============================================================================

void MclkHarness::boot() {
    reset_and_provision();
    aaf0.uid = 0;
    aaf0.ppm = -6.0;
    aaf1.uid = 2;
    aaf1.ppm = -8.0;
    aaf1.mr = 1;                                          //! opposite levels
    crfk.crf = true;
    crfk.uid = 1;
    crfk.ppm = -14.0;
    for (Talker* t : {&aaf0, &aaf1, &crfk}) {
        t->anchor_ns = static_cast<long double>(t_fs_ / kFsPerNs) + 1000.0L;
        t->on = true;
    }
    set_tu(false);
    run_for_ns(50'000'000);
    auto* rp = dut->rootp;
    ck("boot: the CRF sink is locked (8 clean PDUs)", (axi_read(0x738) >> 31) == 1);
    ck("boot: INTERNAL decodes and nothing is followed",
       rp->milan_datapath__DOT__int_clk_selected_r == 1 && rp->milan_datapath__DOT__follow_sel_r == 0);
    ckv("boot: C1 LOCKED counted the valid clock once", ctr_locked(), 1);
    ckv("boot: C1 UNLOCKED has not moved", ctr_unlocked(), 0);
    ck("boot: both outputs are emitting", aaf_out.pdus > 0 && crf_out.pdus > 0);
}

//! The INTERNAL half of the true-ratio row. `settle_ns` covers the aligner's
//! pull-in after boot: on this 4 MHz elaboration its keep-off is a quarter
//! sample (20 cycles) rather than 256, and the junction counts skips until
//! the lock walks clear of the walk's crossing, about 2.5 s after boot. The
//! leg grades INTERNAL after a dwell instead, with the aligner long engaged.
void MclkHarness::row_internal(int64_t settle_ns) {
    std::printf("\n[INTERNAL] the aligner engaged at INTERNAL (#629 D4 = A2-a)\n");
    auto* rp = dut->rootp;
    run_for_ns(settle_ns);
    const long d0 = rp->milan_datapath__DOT__tdm_dup_cnt_w + rp->milan_datapath__DOT__tdm_skip_cnt_w;
    grid_window(500'000'000);
    const long d1 = rp->milan_datapath__DOT__tdm_dup_cnt_w + rp->milan_datapath__DOT__tdm_skip_cnt_w;
    const double p = grid_ppm();
    std::printf("  packet grid against the TDM frame over 0.5 s: %+.3f ppm (the plan alone: %+.4f)\n",
                p, kPlanPpm);
    ck("INTERNAL: the packet grid holds the physical grid's rate (the plan's drift gone, |ppm| < 5)",
       std::fabs(p) < 5.0);
    ckv("INTERNAL: the aligner is engaged", rp->milan_datapath__DOT__mga_engaged_w, 1);
    ckv("INTERNAL: SLIP_TDM static over the window", static_cast<uint64_t>(d1 - d0), 0);
    ckv("INTERNAL: the servo idles", static_cast<uint64_t>(servo_state()), kStIdle);
    ckv("INTERNAL: the meter is disabled (AAFM_STAT[2:0])", meter_stat() & 7u, 0);
}

void MclkHarness::row_select_aaf0() {
    std::printf("\n[AAF0] INTERNAL -> AAF input 0 (talker %+.1f ppm)\n", aaf0.ppm);
    auto* rp = dut->rootp;
    const uint32_t lk0 = ctr_locked();
    const uint32_t un0 = ctr_unlocked();
    const long rq0 = restart_pulses;
    const long at0 = aaf_out.toggles;
    const long ct0 = crf_out.toggles;
    select(kSrcAaf0);
    cycles(8);
    ck("AAF0: decodes as AAF listener 0 (and the servo's select)",
       rp->milan_datapath__DOT__aaf_clk_selected_r == 1 && rp->milan_datapath__DOT__aaf_follow_idx_r == 0 &&
       rp->milan_datapath__DOT__follow_sel_r == 1 && rp->milan_datapath__DOT__crf_clk_selected_r == 0 &&
       rp->milan_datapath__DOT__int_clk_selected_r == 0);
    ckv("C1: UNLOCKED moves at the switch onto AAF0", ctr_unlocked() - un0, 1);
    run_for_ns(10'000'000);
    ckv("AAF0: the meter locked on listener 0 (AAFM_STAT {idx, en, locked})", meter_stat() & 0xF5u, 0x05);
    ck("AAF0: the servo leaves IDLE once the meter locks", servo_state() != kStIdle);
    run_for_ns(40'000'000);
    ckv("C1: LOCKED holds until the servo reads LOCKED", ctr_locked() - lk0, 0);
    ckv("AAF0: no restart request at the switch (the source change is the restart)",
        static_cast<uint64_t>(restart_pulses - rq0), 0);
    ckv("AAF0: one mr toggle on the AAF output", static_cast<uint64_t>(aaf_out.toggles - at0), 1);
    ckv("AAF0: one mr toggle on the CRF output", static_cast<uint64_t>(crf_out.toggles - ct0), 1);
}

//! Under E8 the meter's rate validates 2,048 group intervals after its
//! history starts (4.096 s); until then the servo has no reference and
//! skips every window, so its trim holds at the INTERNAL value. A reference
//! taken from anywhere else moves it.
void MclkHarness::row_trim_holds_until_the_meter_rate() {
    run_for_ns(3'000'000'000);
    std::printf("  at 3 s on AAF0: state %d, trim %+.3f ppm, AAFM_STAT 0x%08x\n",
                servo_state(), trim_ppm(), meter_stat());
    ckv("AAF0: the meter's rate is not valid yet at 3 s", meter_stat() & 2u, 0);
    ck("AAF0: the trim holds until the meter's rate validates", trim_ppm() == 0.0);
}

void MclkHarness::follow_to_locked(const char* tag, uint32_t locked0) {
    char w[160];
    const bool ok = run_until_state(kStLocked, 15'000'000'000);
    std::printf("  %s: LOCKED at %.3f s, trim %+.3f ppm\n", tag, now_s(), trim_ppm());
    std::snprintf(w, sizeof w, "%s: the servo reaches LOCKED", tag);
    ck(w, ok);
    cycles(4);
    std::snprintf(w, sizeof w, "C1: LOCKED moves when the servo reads LOCKED (%s)", tag);
    ckv(w, ctr_locked() - locked0, 1);
}

//! The design's true-ratio row: the media clock lands on the selected
//! talker's offset, with the aligner engaged and no junction slip.
void MclkHarness::row_follows(const char* tag, const Talker& t) {
    char w[160];
    auto* rp = dut->rootp;
    run_for_ns(2'000'000'000);
    const long d0 = rp->milan_datapath__DOT__tdm_dup_cnt_w + rp->milan_datapath__DOT__tdm_skip_cnt_w;
    const double p = media_clock_ppm_over(2'000'000'000);
    const long d1 = rp->milan_datapath__DOT__tdm_dup_cnt_w + rp->milan_datapath__DOT__tdm_skip_cnt_w;
    std::printf("  %s: media clock %+.4f ppm over 2 s (talker %+.1f, plan %+.4f), trim %+.3f\n",
                tag, p, t.ppm, kPlanPpm, trim_ppm());
    std::snprintf(w, sizeof w, "%s: the media clock follows the talker within 0.5 ppm", tag);
    ck(w, std::fabs(p - t.ppm) < 0.5);
    std::snprintf(w, sizeof w, "%s: the servo stays LOCKED", tag);
    ckv(w, static_cast<uint64_t>(servo_state()), kStLocked);
    std::snprintf(w, sizeof w, "%s: the aligner stays engaged", tag);
    ckv(w, rp->milan_datapath__DOT__mga_engaged_w, 1);
    std::snprintf(w, sizeof w, "%s: zero junction slips while following", tag);
    ckv(w, static_cast<uint64_t>(d1 - d0), 0);
}

void MclkHarness::row_csr_words(bool full) {
    std::printf("\n[CSR] AAFM_STAT 0x8E0 / AAFM_RATE 0x8E4 against the meter\n");
    const uint32_t st = axi_read(0x8E0);
    const uint32_t tap = meter_stat();
    std::printf("  AAFM_STAT 0x%08x (meter 0x%08x)\n", st, tap);
    ckv("CSR: AAFM_STAT reads the meter's status word", st, tap);
    if (!full) return;
    ckv("CSR: AAFM_STAT {listener 0, en, rate valid, locked}", st & 0xF7u, 0x07);
    ckv("CSR: AAFM_STAT data-caused restarts 0 (ideal timestamps)", (st >> 8) & 0xFFu, 0);
    //! ideal timestamps deviate from the nominal 125 us spacing only by the
    //! talker's offset, accumulated over a group's 15 spacings
    const double dev = 15.0 * kAafPduNs * std::fabs(1.0 / (1.0 + aaf0.ppm * 1e-6) - 1.0);
    std::printf("  largest deviation %u ns (the offset over 15 spacings: %.2f ns)\n", st >> 16, dev);
    ck("CSR: AAFM_STAT largest deviation is the talker's offset over a group (+/-1.5 ns)",
       std::fabs(static_cast<double>(st >> 16) - dev) <= 1.5);
    const int32_t rate = static_cast<int32_t>(axi_read(0x8E4));
    const double want = 512e6 * (1.0 / (1.0 + aaf0.ppm * 1e-6) - 1.0);
    std::printf("  AAFM_RATE %d ns per 512 ms (the talker: %.1f)\n", rate, want);
    ck("CSR: AAFM_RATE reads the talker's planted rate within 2 ns per 512 ms",
       std::fabs(static_cast<double>(rate) - want) <= 2.0);
}

void MclkHarness::row_echo() {
    std::printf("\n[ECHO] the followed talker's mr toggle echoes; an unfollowed one's does not\n");
    long rq0 = restart_pulses;
    long at0 = aaf_out.toggles;
    long ct0 = crf_out.toggles;
    aaf0.mr ^= 1;
    run_for_ns(30'000'000);
    ckv("echo: the followed AAF0's toggle raises one request", static_cast<uint64_t>(restart_pulses - rq0), 1);
    ckv("echo: ...one mr toggle on the AAF output", static_cast<uint64_t>(aaf_out.toggles - at0), 1);
    ckv("echo: ...one mr toggle on the CRF output", static_cast<uint64_t>(crf_out.toggles - ct0), 1);
    rq0 = restart_pulses;
    at0 = aaf_out.toggles;
    ct0 = crf_out.toggles;
    aaf1.mr ^= 1;                                         //! still opposite to AAF0
    run_for_ns(30'000'000);
    ckv("echo: the unfollowed AAF1's toggle raises no request", static_cast<uint64_t>(restart_pulses - rq0), 0);
    ckv("echo: ...and toggles no output",
        static_cast<uint64_t>(aaf_out.toggles - at0 + crf_out.toggles - ct0), 0);
}

void MclkHarness::row_loss_leg(int64_t ns) {
    std::printf("\n[LOSS] one AAF0 PDU lost in every 0.3 s for %.1f s\n", static_cast<double>(ns) * 1e-9);
    const uint64_t n0 = aaf0.n;
    constexpr uint64_t kEvery = 2400;                     //! 0.3 s of 125 us PDUs
    aaf0.lost = [n0](uint64_t i) { return i > n0 && (i - n0) % kEvery == 0; };
    const uint32_t lk0 = ctr_locked();
    const uint32_t un0 = ctr_unlocked();
    const long rq0 = restart_pulses;
    const uint32_t rs0 = (meter_stat() >> 8) & 0xFFu;
    const uint64_t sent0 = aaf0.sent;
    long left = 0;
    const int64_t stop = t_fs_ + ns * kFsPerNs;
    while (t_fs_ < stop) {
        cycles(kMclkHz / 1000);
        if (servo_state() != kStLocked) left++;
    }
    aaf0.lost = nullptr;
    const uint64_t lost = (aaf0.n - n0) - (aaf0.sent - sent0);
    std::printf("  %llu PDUs lost; servo left LOCKED in %ld of the 1 ms samples\n",
                static_cast<unsigned long long>(lost), left);
    ck("loss leg: PDUs were actually lost", lost + 1 >= static_cast<uint64_t>(ns / 300'000'000));
    ckv("loss leg: the servo stays LOCKED through single lost PDUs", static_cast<uint64_t>(left), 0);
    ckv("C1: neither counter moves in the loss leg (LOCKED)", ctr_locked() - lk0, 0);
    ckv("C1: neither counter moves in the loss leg (UNLOCKED)", ctr_unlocked() - un0, 0);
    ckv("loss leg: no restart request", static_cast<uint64_t>(restart_pulses - rq0), 0);
    ckv("loss leg: no history restart in the meter", ((meter_stat() >> 8) & 0xFFu) - rs0, 0);
    ckv("loss leg: the meter's rate stays valid", (meter_stat() >> 1) & 1u, 1);
}

void MclkHarness::row_aaf_loss(bool full) {
    std::printf("\n[AAF-LOSS] the followed AAF0 falls silent for 150 ms, then returns\n");
    auto* rp = dut->rootp;
    const uint32_t lk0 = ctr_locked();
    const uint32_t un0 = ctr_unlocked();
    long rq0 = restart_pulses;
    long at0 = aaf_out.toggles;
    long ct0 = crf_out.toggles;
    aaf0.muted = true;
    run_for_ns(150'000'000);
    ckv("AAF loss: one request at the meter's timeout", static_cast<uint64_t>(restart_pulses - rq0), 1);
    ckv("AAF loss: the servo holds over", static_cast<uint64_t>(servo_state()), kStHoldover);
    ckv("AAF loss: one mr toggle on the AAF output", static_cast<uint64_t>(aaf_out.toggles - at0), 1);
    ckv("AAF loss: one mr toggle on the CRF output", static_cast<uint64_t>(crf_out.toggles - ct0), 1);
    ck("AAF loss: the selection is unchanged (index 2, AAF listener 0)",
       rp->milan_datapath__DOT__pp_aecp_clk_src_index_w == kSrcAaf0 &&
       rp->milan_datapath__DOT__aaf_clk_selected_r == 1 && rp->milan_datapath__DOT__aaf_follow_idx_r == 0);
    if (full) ckv("C1: UNLOCKED moves at the loss", ctr_unlocked() - un0, 1);
    aaf0.muted = false;
    rq0 = restart_pulses;
    at0 = aaf_out.toggles;
    ct0 = crf_out.toggles;
    run_for_ns(100'000'000);
    ckv("AAF return: no request on return", static_cast<uint64_t>(restart_pulses - rq0), 0);
    ckv("AAF return: no further mr toggle",
        static_cast<uint64_t>(aaf_out.toggles - at0 + crf_out.toggles - ct0), 0);
    ckv("AAF return: the meter locked again", meter_stat() & 1u, 1);
    if (full) follow_to_locked("AAF return", lk0);
}

void MclkHarness::row_w2_switch_to_crf(bool full) {
    std::printf("\n[W2] the followed source moves from AAF input 0 to the locked CRF input\n");
    auto* rp = dut->rootp;
    ck("W2: the CRF input is locked before the switch", (axi_read(0x738) >> 31) == 1);
    const double trim0 = trim_ppm();
    const int st0 = servo_state();
    const uint32_t lk0 = ctr_locked();
    const uint32_t un0 = ctr_unlocked();
    const long rq0 = restart_pulses;
    const long at0 = aaf_out.toggles;
    const long ct0 = crf_out.toggles;
    select(kSrcCrf);
    bool held = false;
    for (int c = 0; c < 4000 && !(held && servo_state() == kStAcquire); c++) {
        cycles(1);
        if (servo_state() == kStHoldover) held = true;
    }
    std::printf("  from state %d, trim %+.3f: HOLDOVER %s, now state %d, trim %+.3f\n",
                st0, trim0, held ? "seen" : "NOT seen", servo_state(), trim_ppm());
    ck("W2: the switch onto a locked CRF passes HOLDOVER", held);
    ckv("W2: ...then ACQUIRE", static_cast<uint64_t>(servo_state()), kStAcquire);
    ck("W2: the trim is kept (no reset through IDLE)", std::fabs(trim_ppm() - trim0) < 0.1);
    ck("W2: decodes as CRF",
       rp->milan_datapath__DOT__crf_clk_selected_r == 1 && rp->milan_datapath__DOT__aaf_clk_selected_r == 0 &&
       rp->milan_datapath__DOT__follow_sel_r == 1);
    if (!full) return;
    run_for_ns(1'000'000'000);
    ckv("W2: LOCKED is re-earned, not kept (still ACQUIRE 1 s on)", static_cast<uint64_t>(servo_state()), kStAcquire);
    ckv("C1: UNLOCKED moves at the switch to CRF", ctr_unlocked() - un0, 1);
    ckv("W2: no restart request at the switch", static_cast<uint64_t>(restart_pulses - rq0), 0);
    ckv("W2: one mr toggle on the AAF output", static_cast<uint64_t>(aaf_out.toggles - at0), 1);
    ckv("W2: one mr toggle on the CRF output", static_cast<uint64_t>(crf_out.toggles - ct0), 1);
    follow_to_locked("CRF", lk0);
    row_follows("CRF", crfk);
}

void MclkHarness::row_select_crf() {
    std::printf("\n[CRF] INTERNAL -> the CRF input (talker %+.1f ppm)\n", crfk.ppm);
    auto* rp = dut->rootp;
    const uint32_t lk0 = ctr_locked();
    const uint32_t un0 = ctr_unlocked();
    select(kSrcCrf);
    cycles(8);
    ck("CRF: decodes as CRF",
       rp->milan_datapath__DOT__crf_clk_selected_r == 1 && rp->milan_datapath__DOT__follow_sel_r == 1);
    ckv("C1: UNLOCKED moves at the switch onto CRF", ctr_unlocked() - un0, 1);
    ckv("CRF: the AAF meter stays disabled", meter_stat() & 7u, 0);
    follow_to_locked("CRF", lk0);
}

void MclkHarness::row_crf_loss() {
    std::printf("\n[CRF-LOSS] the followed CRF falls silent for 150 ms, then returns\n");
    auto* rp = dut->rootp;
    const uint32_t lk0 = ctr_locked();
    const uint32_t un0 = ctr_unlocked();
    long rq0 = restart_pulses;
    long at0 = aaf_out.toggles;
    long ct0 = crf_out.toggles;
    crfk.muted = true;
    run_for_ns(150'000'000);
    ckv("CRF loss: one request at the sink's timeout", static_cast<uint64_t>(restart_pulses - rq0), 1);
    ckv("CRF loss: the servo holds over", static_cast<uint64_t>(servo_state()), kStHoldover);
    ckv("CRF loss: one mr toggle on the AAF output", static_cast<uint64_t>(aaf_out.toggles - at0), 1);
    ckv("CRF loss: one mr toggle on the CRF output", static_cast<uint64_t>(crf_out.toggles - ct0), 1);
    ck("CRF loss: the selection is unchanged (index 1)",
       rp->milan_datapath__DOT__pp_aecp_clk_src_index_w == kSrcCrf &&
       rp->milan_datapath__DOT__crf_clk_selected_r == 1);
    ckv("C1: UNLOCKED moves at the CRF loss", ctr_unlocked() - un0, 1);
    crfk.muted = false;
    rq0 = restart_pulses;
    at0 = aaf_out.toggles;
    ct0 = crf_out.toggles;
    run_for_ns(100'000'000);
    ckv("CRF return: no request on return", static_cast<uint64_t>(restart_pulses - rq0), 0);
    ckv("CRF return: no further mr toggle",
        static_cast<uint64_t>(aaf_out.toggles - at0 + crf_out.toggles - ct0), 0);
    follow_to_locked("CRF return", lk0);
}

//! the CRF Media Clock Output's talker-diag context: after the AAF talkers
constexpr unsigned kCrfCtx = 2;
//! the gap after a switch: 30 CRF output PDUs, past the 8-PDU hold, and
//! past the #386 settle's 2048-tick dwell (43 ms)
constexpr int64_t kSwitchGapNs = 60'000'000;

MclkHarness::SwitchDelta MclkHarness::switch_once(uint16_t to, int64_t gap_ns) {
    SwitchDelta d{};
    const long rq0 = restart_pulses;
    const long at0 = aaf_out.toggles;
    const long ct0 = crf_out.toggles;
    const uint32_t ma0 = mreset(0);
    const uint32_t mc0 = mreset(kCrfCtx);
    const long rc0 = src_recentres;
    select(to);
    run_for_ns(gap_ns);
    d.pulses = restart_pulses - rq0;
    d.aaf_toggles = aaf_out.toggles - at0;
    d.crf_toggles = crf_out.toggles - ct0;
    d.aaf_mreset = mreset(0) - ma0;
    d.crf_mreset = mreset(kCrfCtx) - mc0;
    d.recentres = src_recentres - rc0;
    return d;
}

//! Row (i): AAF0 -> CRF -> AAF0 -> AAF1 -> AAF0, the two AAF talkers at
//! opposite mr levels, each round started `p` sixteenths of a CRF output
//! period after one of that output's PDUs.
void MclkHarness::row_switch_sweep(int phases, bool grade_slips) {
    std::printf("\n[SWITCH] AAF0 -> CRF -> AAF0 -> AAF1 -> AAF0 at %d phases of the CRF output\n", phases);
    auto* rp = dut->rootp;
    const std::array<uint16_t, 4> order = {kSrcCrf, kSrcAaf0, kSrcAaf1, kSrcAaf0};
    long n = 0;
    long bad_pulse = 0;
    long bad_toggle = 0;
    long bad_mreset = 0;
    long bad_recentre = 0;
    long bad_aaf1 = 0;
    long bad_engaged = 0;
    const long d0 = rp->milan_datapath__DOT__tdm_dup_cnt_w + rp->milan_datapath__DOT__tdm_skip_cnt_w;
    for (int p = 0; p < phases; p++) {
        const long pdus = crf_out.pdus;
        while (crf_out.pdus == pdus) cycles(1);
        run_for_ns(static_cast<int64_t>(p) * kCrfPduNs / 16);
        for (uint16_t to : order) {
            const SwitchDelta d = switch_once(to, kSwitchGapNs);
            n++;
            if (d.pulses != 0) bad_pulse++;
            if (d.aaf_toggles != 1 || d.crf_toggles != 1) bad_toggle++;
            if (d.aaf_mreset != 1 || d.crf_mreset != 1) bad_mreset++;
            if (d.recentres > 1) bad_recentre++;
            if (rp->milan_datapath__DOT__mga_engaged_w != 1) bad_engaged++;
            if (to == kSrcAaf1 && !(rp->milan_datapath__DOT__aaf_clk_selected_r == 1 &&
                                    rp->milan_datapath__DOT__aaf_follow_idx_r == 1 &&
                                    ((meter_stat() >> 4) & 0xFu) == 1)) bad_aaf1++;
        }
    }
    const long d1 = rp->milan_datapath__DOT__tdm_dup_cnt_w + rp->milan_datapath__DOT__tdm_skip_cnt_w;
    std::printf("  %ld switches: %ld with a request pulse, %ld without one toggle per output, "
                "%ld without one MEDIA_RESET per output, %ld with more than one recentre\n",
                n, bad_pulse, bad_toggle, bad_mreset, bad_recentre);
    ckv("switch: no request pulse at any switch", static_cast<uint64_t>(bad_pulse), 0);
    ckv("switch: exactly one mr toggle per output per switch", static_cast<uint64_t>(bad_toggle), 0);
    ckv("switch: each output's MEDIA_RESET moves once per switch", static_cast<uint64_t>(bad_mreset), 0);
    ckv("switch: never more than one #386 recentre per switch (re-armed, never queued)",
        static_cast<uint64_t>(bad_recentre), 0);
    ckv("switch: AAF1 decodes as listener 1 and the meter follows it", static_cast<uint64_t>(bad_aaf1), 0);
    ckv("switch: the aligner stays engaged", static_cast<uint64_t>(bad_engaged), 0);
    if (grade_slips) ckv("switch: SLIP_TDM static across the sweep", static_cast<uint64_t>(d1 - d0), 0);
    ck("switch: every toggle held at least 8 PDUs on the AAF output", aaf_out.min_hold >= 8);
    ck("switch: every toggle held at least 8 PDUs on the CRF output", crf_out.min_hold >= 8);
}

//! The #386 recentre of each switch kind, given the settle's own time. On
//! this 4 MHz elaboration the settle band, 1/64 sample, is one fabric cycle,
//! so while the servo re-acquires the band can miss and the settle takes its
//! 32768-tick ceiling (683 ms): one recentre per switch is graded over a gap
//! past that ceiling, and the sweep above grades that none is ever queued.
void MclkHarness::row_switch_recentres() {
    std::printf("\n[SWITCH-RECENTRE] one #386 recentre per switch, over 0.8 s gaps\n");
    const std::array<uint16_t, 4> order = {kSrcCrf, kSrcAaf0, kSrcAaf1, kSrcAaf0};
    long bad = 0;
    long bad_other = 0;
    for (uint16_t to : order) {
        const SwitchDelta d = switch_once(to, 800'000'000);
        std::printf("  -> source %u: %ld recentre(s), %ld request(s), toggles %ld/%ld\n",
                    to, d.recentres, d.pulses, d.aaf_toggles, d.crf_toggles);
        if (d.recentres != 1) bad++;
        if (d.pulses != 0 || d.aaf_toggles != 1 || d.crf_toggles != 1) bad_other++;
    }
    ckv("switch: one #386 recentre per switch", static_cast<uint64_t>(bad), 0);
    ckv("switch: ...with no request pulse and one toggle per output", static_cast<uint64_t>(bad_other), 0);
}

//! Row (ii): onto AAF input 1 while its talker is silent; it starts 5 ms on.
void MclkHarness::row_switch_onto_a_silent_talker() {
    std::printf("\n[SWITCH-SILENT] AAF0 -> AAF1 with AAF1 silent at the switch, starting 5 ms on\n");
    aaf1.muted = true;
    run_for_ns(2'000'000);
    const long rq0 = restart_pulses;
    const long at0 = aaf_out.toggles;
    const long ct0 = crf_out.toggles;
    select(kSrcAaf1);
    run_for_ns(5'000'000);
    aaf1.muted = false;
    run_for_ns(kSwitchGapNs);
    ckv("switch (ii): no request pulse", static_cast<uint64_t>(restart_pulses - rq0), 0);
    ckv("switch (ii): exactly one mr toggle on the AAF output", static_cast<uint64_t>(aaf_out.toggles - at0), 1);
    ckv("switch (ii): exactly one mr toggle on the CRF output", static_cast<uint64_t>(crf_out.toggles - ct0), 1);
    ckv("switch (ii): the meter locked on listener 1 once it started", meter_stat() & 0xF5u, 0x15);
}

//! Row (iii): an INTERNAL dwell with AAF0 toggling its mr.
void MclkHarness::row_internal_dwell() {
    std::printf("\n[DWELL] INTERNAL with AAF0 toggling its mr\n");
    select(kSrcInternal);
    run_for_ns(kSwitchGapNs);
    const long rq0 = restart_pulses;
    const long at0 = aaf_out.toggles;
    const long ct0 = crf_out.toggles;
    aaf0.mr ^= 1;
    run_for_ns(30'000'000);
    aaf0.mr ^= 1;
    run_for_ns(30'000'000);
    ckv("(iii) INTERNAL dwell: AAF0's mr toggle raises no request", static_cast<uint64_t>(restart_pulses - rq0), 0);
    ckv("(iii) INTERNAL dwell: ...and toggles no output",
        static_cast<uint64_t>(aaf_out.toggles - at0 + crf_out.toggles - ct0), 0);
    ckv("(iii) INTERNAL dwell: the meter is disabled", meter_stat() & 7u, 0);
}

void MclkHarness::report_counters() {
    std::printf("\n  C1 counters at the end: LOCKED %u, UNLOCKED %u; %ld bad samples\n",
                ctr_locked(), ctr_unlocked(), ctr_bad_);
    ckv("C1: LOCKED equals UNLOCKED or UNLOCKED + 1 at every sample", static_cast<uint64_t>(ctr_bad_), 0);
}

//! Leg A: INTERNAL -> AAF input 0: lock, follow, CSR words, echo, the loss
//! leg, a lock loss and return.
void MclkHarness::leg_a() {
    const uint32_t lk0 = ctr_locked();
    row_select_aaf0();
    row_trim_holds_until_the_meter_rate();
    follow_to_locked("AAF0", lk0);
    row_follows("AAF0", aaf0);
    row_csr_words(true);
    row_echo();
    row_loss_leg(3'000'000'000);
    row_aaf_loss(true);
    report_counters();
}

//! Leg C: AAF input 0 LOCKED, then W2 onto the locked CRF input and its
//! follow. Its own leg so the pool runs it beside A: the AAF lock it repeats
//! costs less wall time than the two in series.
void MclkHarness::leg_c() {
    const uint32_t lk0 = ctr_locked();
    row_select_aaf0();
    follow_to_locked("AAF0", lk0);
    row_w2_switch_to_crf(true);
    report_counters();
}

//! Leg B: the CRF input locked, its loss and return, the switch rows, then
//! INTERNAL graded after its dwell.
void MclkHarness::leg_b() {
    row_select_crf();
    row_crf_loss();
    select(kSrcAaf0);
    run_for_ns(kSwitchGapNs);
    row_switch_sweep(16, true);
    row_switch_recentres();
    row_switch_onto_a_silent_talker();
    row_internal_dwell();
    row_internal(0);
    report_counters();
}

int MclkHarness::run(const std::string& mode) {
    boot();
    std::printf("plan %+.4f ppm; mode %s\n", kPlanPpm, mode.c_str());
    if (mode == "a") leg_a();
    else if (mode == "b") leg_b();
    else if (mode == "c") leg_c();
    else if (mode == "internal") row_internal(3'500'000'000);
    else if (mode == "select") row_select_aaf0();
    else if (mode == "refmux") { row_select_aaf0(); row_trim_holds_until_the_meter_rate(); }
    else if (mode == "csr") { row_select_aaf0(); row_csr_words(false); }
    else if (mode == "echo") { row_select_aaf0(); row_echo(); }
    else if (mode == "aafloss") { row_select_aaf0(); row_aaf_loss(false); }
    else if (mode == "w2") { row_select_aaf0(); row_w2_switch_to_crf(false); }
    else if (mode == "loss") {
        const uint32_t lk0 = ctr_locked();
        row_select_aaf0();
        follow_to_locked("AAF0", lk0);
        row_loss_leg(1'000'000'000);
    } else if (mode == "switch") {
        select(kSrcAaf0);
        run_for_ns(kSwitchGapNs);
        row_switch_sweep(1, false);
    } else if (mode == "dwell") row_internal_dwell();
    else check_.fail("unknown mode");
    std::printf("simulated %.3f s\n", now_s());
    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    std::setvbuf(stdout, nullptr, _IOLBF, 0);     //! a killed run still shows its last row
    const milan::tb::Model<Vmilan_datapath> model;
    milan::tb::Checker check{"milan_dp_mclk"};
    MclkHarness h(check);
    h.dut = model.get();
    std::string mode = "a";
    for (int i = 1; i < argc; i++) {
        const std::string a = argv[i];
        if (a.rfind("--", 0) == 0) mode = a.substr(2);
    }
    h.run(mode);
    return check.report();
}
