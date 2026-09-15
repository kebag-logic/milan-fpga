// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The gPTP egress timestamp CLOSED LOOP (issue #360).
//
// WHAT IS IN THE LOOP. One live simulation: the real donor engine, the real
// plane and its egress ledger, the real timestamp_counter, the real launch
// observer, the real link guard, the real merge arbiter, and the shipping
// MAC transmit chain converted from the product's own migen source - both
// `mac_tx_cdc` halves, `tx_sf`, the LiteEth core with preamble, FCS,
// padding, width conversion and gap insertion, and the PHY transmit
// register stage. Three clocks run at the product's shape: 125 MHz at the
// wire, 100 MHz at the MAC system side, 50 MHz at the plane. This harness
// drives the datapath boundary, the clocks, the recovery controls and the
// peer, and nothing else: every frame byte, every launch instant, every
// ready and every reset response is produced by the design.
//
// THE TWO SEAMS, AND WHY THE ORACLE IS INDEPENDENT. The observer under test
// reads `phy.sink`, the product connection. This harness's oracle reads the
// PADS, counts octets there itself, and takes the reference launch instant
// from the PHC samples it collected at the plane's own clock edges. It never
// reads the design's computed t1 and never adjusts anything to reach an
// expected answer, so a dropped register stage moves the answer by a whole
// clock period rather than being absorbed.
//
// WHAT THIS BENCH DOES NOT CLAIM. No physical latency, no PHY plane
// correction, no silicon result. Its reference plane is the registered GMII
// launch edge, and the two terms that are not applied anywhere - the gtx
// phase option and pad clock-to-out plus PHY, magnetics and cable - belong
// to the physical qualification issues.

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

#include "Vgptp_txts_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"

namespace {

//! The three clock half-periods, in nanoseconds of simulated time. They are
//! the product's: 125 MHz at the wire, 100 MHz at the MAC system side and
//! 50 MHz at the plane, which is what makes the egress correction this
//! bench grades the product's own 426 ns.
constexpr uint64_t kEthHalfNs = 4;
constexpr uint64_t kSysHalfNs = 5;
constexpr uint64_t kDpHalfNs = 10;

//! The PHC's nominal Q8.24 step at the plane's 20 ns tick.
constexpr uint32_t kPhcIncrNominal = 20u << 24;

//! The published digital bound, and the bench's own tolerance on it. The
//! error a correct reconstruction shows is the crossing's sampling phase
//! minus its mean, plus at most one nanosecond of PHC integer truncation.
constexpr int64_t kBoundNs = 11;
//! Frames the bias oracle needs before its mean means anything.
constexpr int kBiasFrames = 200;

//! THE TWO DOMAINS ARE INDEPENDENT OSCILLATORS, and this bench says so.
//! The transmit domain rides the PHY's recovered clock and the plane rides
//! the board's own PLL: an exactly commensurate 125:50 with a fixed phase
//! is not a conservative model of that, it is a model in which the
//! crossing's sampling phase - the dominant term of the published bound -
//! takes ONE value for the whole run and its mean is whatever that value
//! happens to be. The wire clock therefore carries a relative frequency
//! offset at the declared envelope, so the phase walks through its whole
//! range while every other number stays the product's.
constexpr uint64_t kEthOffsetPpm = 200;
//! the accumulator's unit: parts per million of one nanosecond
constexpr uint64_t kPpmScale = 1'000'000;

//! The peer's clock identity.
constexpr uint64_t kPeerCid = 0x0080E1FFFE112233ull;

//! The middle value of a set of per-frame errors. A median rather than a
//! mean, because the comparison it feeds is between two GROUPS and one
//! outlier must not decide it.
int64_t median_of(std::vector<int64_t> values) {
  if (values.empty()) return 0;
  std::sort(values.begin(), values.end());
  return values[values.size() / 2];
}

//! Loop guards. Every wait is bounded so a broken design reports instead of
//! hanging; each is generous against the interval it covers.
constexpr uint64_t kBringUpNs = 40'000'000;
constexpr uint64_t kExchangeNs = 2'000'000;
//! engine time the donor's initialisation leg needs before its receive
//! path will answer anything
constexpr uint64_t kEngineBootNs = 60'000'000;
constexpr uint64_t kRecoveryNs = 20'000'000;

struct Frame {
  std::vector<uint8_t> b;
  void u8(uint8_t v) { b.push_back(v); }
  void u16(uint16_t v) { u8(static_cast<uint8_t>(v >> 8)); u8(v & 0xFF); }
  void u32(uint32_t v) { u16(static_cast<uint16_t>(v >> 16));
                         u16(static_cast<uint16_t>(v & 0xFFFF)); }
  void u48(uint64_t v) { u16(static_cast<uint16_t>((v >> 32) & 0xFFFF));
                         u32(static_cast<uint32_t>(v & 0xFFFFFFFF)); }
  void u64v(uint64_t v) { u32(static_cast<uint32_t>(v >> 32));
                          u32(static_cast<uint32_t>(v & 0xFFFFFFFF)); }
  void ts(uint64_t ns) { u48(ns / 1000000000ull);
                         u32(static_cast<uint32_t>(ns % 1000000000ull)); }
};

//! One 802.1AS frame in the shape the plane's parser accepts.
Frame ptp_frame(uint8_t mtype, uint16_t seq, uint16_t flags,
                uint16_t body_len, uint64_t src) {
  Frame f;
  f.u48(0x0180C200000Eull);
  f.u48(0x0080E1112233ull);
  f.u16(0x88F7);
  f.u8(static_cast<uint8_t>(0x10 | mtype));
  f.u8(0x02);
  f.u16(static_cast<uint16_t>(34 + body_len));
  f.u8(0);
  f.u8(0);
  f.u16(flags);
  f.u64v(0);
  f.u32(0);
  f.u64v(src);
  f.u16(1);
  f.u16(seq);
  f.u8(0x05);
  f.u8(0x7F);
  return f;
}

//! A frame of `len` octets that is NOT gPTP: the background traffic whose
//! only job is to be in front of a plane frame in the real queue.
std::vector<uint8_t> background_frame(size_t len, uint8_t tag) {
  std::vector<uint8_t> f(len, tag);
  const std::array<uint8_t, 6> da = {0x02, 0x11, 0x22, 0x33, 0x44, 0x55};
  const std::array<uint8_t, 6> sa = {0x02, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE};
  for (size_t i = 0; i < 6; i++) {
    f[i] = da[i];
    f[6 + i] = sa[i];
  }
  f[12] = 0x22;
  f[13] = 0xF0;
  return f;
}

//! One frame the oracle reconstructed from the PADS, with the instant its
//! reference octet was launched.
struct PadFrame {
  uint64_t ref_ns = 0;      //! simulated time of the reference launch edge
  uint8_t type = 0xFF;
  uint16_t seq = 0;
  size_t octets = 0;
  bool gptp = false;
  bool gapped = false;      //! `tx_en` went low inside this frame
  std::vector<uint8_t> body;
};

//! One result the engine accepted.
struct Result {
  uint64_t ns = 0;
  uint16_t seq = 0;
  uint8_t type = 0;
  uint8_t ok = 0;
};

//! One record the observer produced.
struct Record {
  uint16_t oidx = 0;
  uint16_t seq = 0;
  uint8_t type = 0;
  uint8_t delta = 0;
  uint8_t abort = 0;
};

}  // namespace

//! The closed loop, its clocks, its peer and its oracles.
class TxtsHarness {
 public:
  int run();

 private:
  // ---- the model and the tally ------------------------------------------
  const milan::tb::Model<Vgptp_txts_wrap> model_;
  Vgptp_txts_wrap *dut = model_.get();
  milan::tb::Checker check{"gptp_txts"};

  // ---- the clock scheduler ----------------------------------------------
  uint64_t now_ = 0;
  uint64_t eth_next_ = 0;
  uint64_t sys_next_ = 0;
  uint64_t dp_next_ = 0;
  //! fractional nanoseconds of the wire clock's relative frequency offset,
  //! carried between half-periods so the offset is exact over a run rather
  //! than rounded away at every edge
  uint64_t eth_acc_ = 0;

  // ---- what the harness drives ------------------------------------------
  std::vector<uint8_t> rx_bytes_;
  size_t rx_pos_ = 0;
  std::vector<uint8_t> bg_bytes_;
  size_t bg_pos_ = 0;
  //! When set, a background frame of this length is kept in flight
  //! continuously, so a plane frame really does wait behind other traffic
  //! in the store-and-forward FIFO rather than finding an empty MAC.
  size_t bg_continuous_ = 0;
  uint8_t bg_tag_ = 0;

  // ---- what the harness observes ----------------------------------------
  std::vector<std::pair<uint64_t, uint64_t>> phc_samples_;
  std::vector<PadFrame> pads_;
  std::vector<Result> results_;
  std::vector<Record> records_;
  std::vector<uint64_t> boundary_ns_;   //! the RETIRED capture, per plane frame
  PadFrame pad_cur_;
  bool pad_open_ = false;
  size_t pad_idx_ = 0;
  uint64_t pad_gap_ = 0;
  bool lane_sof_ = true;
  uint16_t peer_seq_ = 0;
  uint64_t epi_done_count_ = 0;
  uint64_t dbg_rx_beats_ = 0;
  uint64_t dbg_lane_beats_ = 0;
  uint64_t dbg_eng_bytes_ = 0;
  uint64_t dbg_mrg_beats_ = 0;
  uint64_t dbg_busy_cyc_ = 0;
  uint64_t dbg_engrx_ = 0;
  uint64_t dbg_engsof_ = 0;
  uint64_t recov_req_count_ = 0;

  // ---- the loop ----------------------------------------------------------
  void step();
  void on_dp_edge();
  void drive_sources();
  void on_eth_edge();
  void pad_octet(uint8_t data);
  void pad_close();
  void run_ns(uint64_t span);
  void reset_all();
  bool wait_unsealed(uint64_t span);

  // ---- the peer ----------------------------------------------------------
  void send_peer(const std::vector<uint8_t> &bytes);
  void send_background(size_t len, uint8_t tag);
  bool exchange(size_t background_len);
  void collect_group(size_t mark, std::vector<int64_t> &old_err,
                     std::vector<int64_t> &new_err);

  // ---- the phases --------------------------------------------------------
  void prove_bring_up();
  void prove_launch_reference();
  void prove_queue_invariance();
  void prove_bias_over_many_frames();
  void prove_pads_are_byte_exact();
  void prove_fragment_aborts();
  void prove_recovery_over_the_production_mac();
  void prove_full_run_laws();

  // ---- the oracles --------------------------------------------------------
  int64_t phc_at(uint64_t when) const;
  size_t gptp_pads() const;
  int64_t error_of(size_t gptp_index) const;
};

// ===========================================================================
//  The clock scheduler
// ===========================================================================

//! Advance to the next clock edge and evaluate. The three clocks are
//! independent: the plane's edge is offset by a swept skew, so the
//! crossing's sampling phase - the dominant term of the published bound -
//! takes every value over a run instead of one.
void TxtsHarness::step() {
  const uint64_t next = std::min({eth_next_, sys_next_, dp_next_});
  now_ = next;
  bool eth_posedge = false;
  bool dp_posedge = false;
  bool dp_negedge = false;
  if (eth_next_ == now_) {
    dut->eth_clk_i = dut->eth_clk_i ? 0 : 1;
    eth_posedge = dut->eth_clk_i != 0;
    eth_next_ += kEthHalfNs;
    eth_acc_ += kEthOffsetPpm * kEthHalfNs;
    if (eth_acc_ >= kPpmScale) {
      eth_acc_ -= kPpmScale;
      eth_next_ += 1;
    }
  }
  if (sys_next_ == now_) {
    dut->sys_clk_i = dut->sys_clk_i ? 0 : 1;
    sys_next_ += kSysHalfNs;
  }
  if (dp_next_ == now_) {
    dut->dp_clk_i = dut->dp_clk_i ? 0 : 1;
    dp_posedge = dut->dp_clk_i != 0;
    dp_negedge = !dp_posedge;
    dp_next_ += kDpHalfNs;
  }
  //! A source presents its beat while the clock is LOW and the design
  //! takes it at the rising edge. Driving at the rising edge instead would
  //! present beat N+1 at the very edge that accepts beat N, and beat N
  //! would never be sampled.
  if (dp_posedge) on_dp_edge();
  if (dp_negedge) drive_sources();
  dut->eval();
  if (eth_posedge) on_eth_edge();
  if (dp_posedge) {
    phc_samples_.emplace_back(now_, dut->phc_ns_o);
    if (dut->eng_txts_v_o) {
      results_.push_back({dut->eng_txts_ns_o,
                          static_cast<uint16_t>(dut->eng_txts_seq_o),
                          static_cast<uint8_t>(dut->eng_txts_type_o),
                          static_cast<uint8_t>(dut->eng_txts_ok_o)});
    }
    if (dut->rec_v_o && !dut->rec_kind_o) {
      records_.push_back({static_cast<uint16_t>(dut->rec_oidx_o),
                          static_cast<uint16_t>(dut->rec_seq_o),
                          static_cast<uint8_t>(dut->rec_type_o),
                          static_cast<uint8_t>(dut->rec_delta_o),
                          static_cast<uint8_t>(dut->rec_abort_o)});
    }
  }
}

void TxtsHarness::run_ns(uint64_t span) {
  const uint64_t until = now_ + span;
  while (now_ < until) step();
}

//! At the rising edge, before the design evaluates it: the handshakes that
//! are completing right now, and the observations that belong to them.
void TxtsHarness::on_dp_edge() {
  if (dut->rx_tvalid_i && dut->rx_tready_i) { rx_pos_ += 8; dbg_rx_beats_++; }
  if (dut->bg_tvalid_i && dut->bg_tready_o) bg_pos_ += 8;
  if (dut->gtx_tvalid_o && dut->gtx_tready_o) dbg_lane_beats_++;
  if (dut->dbg_eng_tx_v_o && dut->dbg_eng_tx_rdy_o) dbg_eng_bytes_++;
  if (dut->dbg_mrg_tvalid_o && dut->dbg_mrg_tready_o) dbg_mrg_beats_++;
  if (dut->dbg_busy_o) dbg_busy_cyc_++;
  if (dut->dbg_eng_rx_v_o) dbg_engrx_++;
  if (dut->dbg_eng_rx_sof_o) dbg_engsof_++;

  //! THE RETIRED CAPTURE POINT, sampled where it used to be: a plane
  //! frame's first accepted beat on its own lane, which the combinational
  //! merge passes straight to the datapath's MAC boundary. Recording it
  //! here is what turns the baseline control into a measurement.
  if (dut->gtx_tvalid_o && dut->gtx_tready_o) {
    if (lane_sof_) boundary_ns_.push_back(now_);
    lane_sof_ = dut->gtx_tlast_o != 0;
  }
  if (dut->dbg_linkg_epi_done_o) epi_done_count_++;
  if (dut->dbg_recov_req_o) recov_req_count_++;
}

//! Present the next beat of each source while the clock is low.
void TxtsHarness::drive_sources() {
  dut->rx_tready_i = 1;
  if (rx_pos_ >= rx_bytes_.size()) {
    rx_bytes_.clear();
    rx_pos_ = 0;
    dut->rx_tvalid_i = 0;
    dut->rx_tlast_i = 0;
  } else {
    uint64_t data = 0;
    uint8_t keep = 0;
    for (size_t i = 0; i < 8 && rx_pos_ + i < rx_bytes_.size(); i++) {
      data |= static_cast<uint64_t>(rx_bytes_[rx_pos_ + i]) << (8 * i);
      keep = static_cast<uint8_t>(keep | (1u << i));
    }
    dut->rx_tdata_i = data;
    dut->rx_tkeep_i = keep;
    dut->rx_tvalid_i = 1;
    dut->rx_tlast_i = (rx_pos_ + 8 >= rx_bytes_.size()) ? 1 : 0;
  }

  if (bg_pos_ >= bg_bytes_.size() && bg_continuous_ != 0) {
    bg_bytes_ = background_frame(bg_continuous_, bg_tag_++);
    bg_pos_ = 0;
  }
  if (bg_pos_ >= bg_bytes_.size()) {
    bg_bytes_.clear();
    bg_pos_ = 0;
    dut->bg_tvalid_i = 0;
    dut->bg_tlast_i = 0;
  } else {
    uint64_t data = 0;
    uint8_t keep = 0;
    for (size_t i = 0; i < 8 && bg_pos_ + i < bg_bytes_.size(); i++) {
      data |= static_cast<uint64_t>(bg_bytes_[bg_pos_ + i]) << (8 * i);
      keep = static_cast<uint8_t>(keep | (1u << i));
    }
    dut->bg_tdata_i = data;
    dut->bg_tkeep_i = keep;
    dut->bg_tvalid_i = 1;
    dut->bg_tlast_i = (bg_pos_ + 8 >= bg_bytes_.size()) ? 1 : 0;
  }
}

// ===========================================================================
//  The independent oracle: the pads, and nothing else
// ===========================================================================

//! Everything this oracle knows it read off `tx_en` and `tx_data`. It never
//! looks at the seam the observer reads, and never at the design's own
//! timestamp.
void TxtsHarness::on_eth_edge() {
  if (dut->gmii_tx_en_o) {
    pad_gap_ = 0;
    pad_octet(static_cast<uint8_t>(dut->gmii_tx_data_o));
  } else if (pad_open_) {
    pad_gap_++;
    //! a frame ends at the inter-frame gap; a shorter low run inside one is
    //! a fragment and is recorded as such
    if (pad_gap_ >= 4) pad_close();
  }
  //! the datapath AXIS boundary sampling has to happen on the plane's clock;
  //! it is done there, in on_dp_edge's caller
}

void TxtsHarness::pad_octet(uint8_t data) {
  if (!pad_open_) {
    pad_open_ = true;
    pad_idx_ = 0;
    pad_cur_ = PadFrame();
  } else {
    pad_idx_++;
    if (pad_gap_ != 0) pad_cur_.gapped = true;
  }
  if (pad_idx_ < 7 && data != 0x55) pad_cur_.gptp = false;
  if (pad_idx_ == 8) {
    //! THE REFERENCE PLANE: the registered GMII launch edge of frame octet
    //! 0, the first symbol after the start-of-frame delimiter.
    pad_cur_.ref_ns = now_;
  }
  if (pad_idx_ >= 8) pad_cur_.body.push_back(data);
  if (pad_idx_ == 21) {
    pad_cur_.gptp = pad_cur_.body.size() >= 14 &&
                    pad_cur_.body[0] == 0x01 && pad_cur_.body[1] == 0x80 &&
                    pad_cur_.body[2] == 0xC2 && pad_cur_.body[3] == 0x00 &&
                    pad_cur_.body[4] == 0x00 && pad_cur_.body[5] == 0x0E &&
                    pad_cur_.body[12] == 0x88 && pad_cur_.body[13] == 0xF7;
  }
  if (pad_idx_ == 22) pad_cur_.type = static_cast<uint8_t>(data & 0xF);
  if (pad_idx_ == 52) pad_cur_.seq = static_cast<uint16_t>(data << 8);
  if (pad_idx_ == 53) {
    pad_cur_.seq = static_cast<uint16_t>(pad_cur_.seq | data);
  }
}

void TxtsHarness::pad_close() {
  pad_open_ = false;
  pad_cur_.octets = pad_cur_.body.size();
  pads_.push_back(pad_cur_);
  pad_cur_ = PadFrame();
}

//! The reference clock, interpolated from the samples this harness took at
//! the plane's own edges. The accumulator is linear between them, so this
//! is the true instant `when` in PHC nanoseconds and not a quantised one.
int64_t TxtsHarness::phc_at(uint64_t when) const {
  if (phc_samples_.size() < 2) return 0;
  size_t lo = 0;
  size_t hi = phc_samples_.size() - 1;
  while (lo + 1 < hi) {
    const size_t mid = (lo + hi) / 2;
    if (phc_samples_[mid].first <= when) lo = mid; else hi = mid;
  }
  const auto &a = phc_samples_[lo];
  const auto &b = phc_samples_[lo + 1 < phc_samples_.size() ? lo + 1 : lo];
  if (b.first == a.first) return static_cast<int64_t>(a.second);
  const int64_t span = static_cast<int64_t>(b.first - a.first);
  const int64_t rise = static_cast<int64_t>(b.second) -
                       static_cast<int64_t>(a.second);
  const int64_t into = static_cast<int64_t>(when) -
                       static_cast<int64_t>(a.first);
  return static_cast<int64_t>(a.second) + (rise * into) / span;
}

size_t TxtsHarness::gptp_pads() const {
  size_t n = 0;
  for (const PadFrame &f : pads_) if (f.gptp) n++;
  return n;
}

//! The error of the `n`-th gPTP frame the pads carried, against the
//! reference this harness computed for it.
int64_t TxtsHarness::error_of(size_t gptp_index) const {
  size_t n = 0;
  for (size_t i = 0; i < pads_.size(); i++) {
    if (!pads_[i].gptp) continue;
    if (n == gptp_index) {
      if (n >= results_.size() || !results_[n].ok) return INT64_MAX;
      return static_cast<int64_t>(results_[n].ns) - phc_at(pads_[i].ref_ns);
    }
    n++;
  }
  return INT64_MAX;
}


// ===========================================================================
//  Reset, bring-up and the peer
// ===========================================================================

//! Everything at its idle level, then the three resets released together.
//! The plane starts SEALED and owes its first fence a recovery episode, so
//! bring-up is not "wait a bit": it is "wait for the design to say it is
//! ready", which is what `wait_unsealed` reads.
void TxtsHarness::reset_all() {
  dut->dp_clk_i = 0;
  dut->sys_clk_i = 0;
  dut->eth_clk_i = 0;
  dut->dp_rst_n = 0;
  dut->sys_rst_n = 0;
  dut->eth_rst_n = 0;
  dut->rx_tvalid_i = 0;
  dut->rx_tlast_i = 0;
  dut->rx_tdata_i = 0;
  dut->rx_tkeep_i = 0;
  dut->rx_tready_i = 1;
  dut->bg_tvalid_i = 0;
  dut->bg_tlast_i = 0;
  dut->bg_tdata_i = 0;
  dut->bg_tkeep_i = 0;
  dut->linkg_dis_i = 0;
  dut->linkg_freeze_i = 0;
  dut->cfg_mac_reinit_i = 0;
  dut->eth_alive_i = 1;
  dut->phc_en_i = 1;
  dut->phc_incr_i = kPhcIncrNominal;
  dut->phc_adj_ovr_en_i = 0;
  dut->phc_adj_ovr_i = 0;
  dut->phc_load_i = 0;
  dut->phc_tod_wr_i = 0;
  dut->obs_bubble_i = 0;
  dut->obs_rst_i = 0;
  run_ns(2000);
  dut->dp_rst_n = 1;
  dut->sys_rst_n = 1;
  dut->eth_rst_n = 1;
  run_ns(2000);
}

bool TxtsHarness::wait_unsealed(uint64_t span) {
  const uint64_t until = now_ + span;
  while (now_ < until) {
    if ((dut->dbg_txts_state_o & 0x8000u) == 0) return true;
    step();
  }
  return false;
}

void TxtsHarness::send_peer(const std::vector<uint8_t> &bytes) {
  rx_bytes_ = bytes;
  rx_pos_ = 0;
}

void TxtsHarness::send_background(size_t len, uint8_t tag) {
  bg_bytes_ = background_frame(len, tag);
  bg_pos_ = 0;
}

//! One peer request, optionally queued behind a background frame of
//! `background_len` octets. The plane answers with a Pdelay_Resp and, once
//! that frame's own result comes back, its Follow_Up. Returns whether both
//! reached the wire.
bool TxtsHarness::exchange(size_t background_len) {
  const size_t pads_before = pads_.size();
  const uint16_t seq = peer_seq_++;
  bg_continuous_ = background_len;
  if (background_len != 0) run_ns(20000);
  Frame req = ptp_frame(0x2, seq, 0x0000, 20, kPeerCid);
  req.u64v(0);
  req.u64v(0);
  req.u32(0);
  send_peer(req.b);
  const uint64_t until = now_ + kExchangeNs;
  bool saw_resp = false;
  bool saw_fu = false;
  while (now_ < until && !(saw_resp && saw_fu)) {
    step();
    for (size_t i = pads_before; i < pads_.size(); i++) {
      if (!pads_[i].gptp || pads_[i].seq != seq) continue;
      if (pads_[i].type == 0x3) saw_resp = true;
      if (pads_[i].type == 0xA) saw_fu = true;
    }
  }
  //! let the last frame's record cross and its result land
  run_ns(4000);
  //! SWEEP THE MAC SYSTEM CLOCK's phase against the plane's. The two come
  //! from one PLL in the product, so their relative phase is a build-time
  //! fact and not a free variable - which is exactly why a bench must not
  //! assume ONE value of it. The instant a frame is handed from the system
  //! side to the wire side sits on this grid, so this phase and the wire
  //! clock's own drift together are what let the crossing's sampling phase
  //! take its whole range.
  sys_next_ += 1;
  return saw_resp && saw_fu;
}

// ===========================================================================
//  The phases
// ===========================================================================

//! The plane starts SEALED and owes its first fence a recovery episode,
//! because a root reset clears the plane but not the store-and-forward FIFO
//! or the MAC core that still hold whatever it handed over. Bring-up is
//! therefore a proof, not a delay: the plane asks, the guard runs a whole
//! episode, the observer echoes, and only then does the seal lift.
void TxtsHarness::prove_bring_up() {
  reset_all();
  check.that("bring-up: the plane asks for a recovery episode at boot",
             recov_req_count_ != 0 || wait_unsealed(kBringUpNs));
  check.that("bring-up: the plane unseals after its boot episode",
             wait_unsealed(kBringUpNs));
  check.that("bring-up: exactly one episode completed to get there",
             epi_done_count_ == 1);
  check.dec("bring-up: nothing was mis-credited before the seal lifted",
            dut->dbg_txts_disc_o, 0);
  //! The donor runs its own initialisation leg off its millisecond tick,
  //! and its receive parser refuses frames until that leg has published a
  //! local clock identity. Give it the engine time it asks for, in engine
  //! time: this bench's engine image is generated for a faster second, so
  //! this is a small slice of simulated time.
  const uint64_t boot_until = now_ + kEngineBootNs;
  while (now_ < boot_until && dbg_lane_beats_ == 0) step();
  std::printf("  engine cadence reached the lane at %llu us\n",
              static_cast<unsigned long long>(now_ / 1000));
  check.that("bring-up: the engine's own cadence reaches the lane",
             dbg_lane_beats_ != 0);
  run_ns(200000);
}

//! Split one group of frames into the retired capture's error and the new
//! reconstruction's error, both against the same pad reference.
void TxtsHarness::collect_group(size_t mark, std::vector<int64_t> &old_err,
                                std::vector<int64_t> &new_err) {
  size_t n = 0;
  for (const PadFrame &f : pads_) {
    if (!f.gptp) continue;
    if (n >= mark) {
      if (n < boundary_ns_.size()) {
        old_err.push_back(static_cast<int64_t>(boundary_ns_[n]) -
                          static_cast<int64_t>(f.ref_ns));
      }
      const int64_t err = error_of(n);
      if (err != INT64_MAX) new_err.push_back(err);
    }
    n++;
  }
}

//! B1: every reconstructed launch is within the published digital bound of
//! the instant the PADS launched that frame's reference octet.
void TxtsHarness::prove_launch_reference() {
  const size_t before = gptp_pads();
  for (int n = 0; n < 12; n++) {
    check.that("launch: an isolated exchange completes", exchange(0));
  }
  const size_t after = gptp_pads();
  check.that("launch: the wire carried the plane's frames", after > before);
  int64_t worst = 0;
  int graded = 0;
  for (size_t i = before; i < after; i++) {
    const int64_t err = error_of(i);
    if (err == INT64_MAX) continue;
    graded++;
    if (std::abs(err) > std::abs(worst)) worst = err;
  }
  check.that("launch: every isolated frame was graded", graded > 0);
  check.that("launch: every reconstruction is inside the published bound",
             std::abs(worst) <= kBoundNs);
  if (std::abs(worst) > kBoundNs) {
    std::printf("  worst isolated error %lld ns over %d frames\n",
                static_cast<long long>(worst), graded);
  }
}

//! A1 and B3: the retired capture is queue dependent by microseconds and
//! the new one is not. Both are measured in the same run, against the same
//! pads, so this is a comparison and not an argument.
void TxtsHarness::prove_queue_invariance() {
  std::vector<int64_t> isolated_old;
  std::vector<int64_t> queued_old;
  std::vector<int64_t> isolated_new;
  std::vector<int64_t> queued_new;
  for (int n = 0; n < 6; n++) {
    const size_t mark = gptp_pads();
    check.that("invariance: an isolated exchange completes", exchange(0));
    collect_group(mark, isolated_old, isolated_new);
  }
  for (int n = 0; n < 6; n++) {
    const size_t mark = gptp_pads();
    check.that("invariance: a queued exchange completes", exchange(1518));
    collect_group(mark, queued_old, queued_new);
  }
  check.that("invariance: both groups produced frames",
             !isolated_old.empty() && !queued_old.empty());
  const int64_t old_iso = median_of(isolated_old);
  const int64_t old_q = median_of(queued_old);
  //! THE DEFECT, as a number: the first-accepted-beat capture precedes the
  //! launch by an amount that depends on what was queued in front of it.
  std::printf("  retired capture precedes the launch by %lld ns isolated, "
              "%lld ns queued\n", static_cast<long long>(-old_iso),
              static_cast<long long>(-old_q));
  check.that("baseline control: the retired capture FAILS queue invariance "
             "by more than four microseconds",
             std::abs(old_q - old_iso) > 4000);
  const int64_t new_iso = median_of(isolated_new);
  const int64_t new_q = median_of(queued_new);
  check.that("invariance: the reconstruction does not move with the queue",
             std::abs(new_q - new_iso) <= kBoundNs);
  for (int64_t e : isolated_new) {
    check.that("invariance: isolated frames stay inside the bound",
               std::abs(e) <= kBoundNs);
  }
  for (int64_t e : queued_new) {
    check.that("invariance: queued frames stay inside the bound",
               std::abs(e) <= kBoundNs);
  }
}

//! B2: a dropped one-octet or one-cycle term hides inside the bound but not
//! inside the MEAN, once the crossing phase has been swept.
void TxtsHarness::prove_bias_over_many_frames() {
  const size_t before = gptp_pads();
  const uint64_t bias_t0_ = now_;
  while (static_cast<int>(gptp_pads() - before) < kBiasFrames) {
    if (!exchange(0)) break;
  }
  int64_t total = 0;
  int graded = 0;
  for (size_t i = before; i < gptp_pads(); i++) {
    const int64_t err = error_of(i);
    if (err == INT64_MAX) continue;
    total += err;
    graded++;
  }
  check.that("bias: at least two hundred phase-varied frames were graded",
             graded >= kBiasFrames);
  const int64_t mean_milli = graded != 0 ? (total * 1000) / graded : 9999;
  std::printf("  mean reconstruction error %lld.%03lld ns over %d frames\n",
              static_cast<long long>(mean_milli / 1000),
              static_cast<long long>(std::abs(mean_milli % 1000)), graded);
  //! The distribution itself, printed: a run whose errors sit on one value
  //! has not swept the crossing phase, and a reader can see that here
  //! rather than infer it from a mean that happens to be small.
  int64_t lo = INT64_MAX;
  int64_t hi = INT64_MIN;
  int distinct = 0;
  std::vector<int64_t> seen;
  for (size_t i = before; i < gptp_pads(); i++) {
    const int64_t e = error_of(i);
    if (e == INT64_MAX) continue;
    lo = std::min(lo, e);
    hi = std::max(hi, e);
    if (std::find(seen.begin(), seen.end(), e) == seen.end()) {
      seen.push_back(e);
      distinct++;
    }
  }
  std::printf("  error spread %+lld..%+lld ns over %d distinct values, "
              "%llu us of run\n", static_cast<long long>(lo),
              static_cast<long long>(hi), distinct,
              static_cast<unsigned long long>((now_ - bias_t0_) / 1000));
  check.that("bias: the crossing phase really was swept", distinct >= 8);
  check.that("bias: the mean error is within one nanosecond of zero",
             std::abs(mean_milli) <= 1000);
}

//! A2: the wire carries whole frames. Every gPTP frame the pads showed has
//! its preamble, its start-of-frame delimiter, the plane's own octets, a
//! frame check sequence and no gap inside it.
void TxtsHarness::prove_pads_are_byte_exact() {
  int gapped = 0;
  int short_frames = 0;
  int wrong_tag = 0;
  size_t n = 0;
  for (const PadFrame &f : pads_) {
    if (!f.gptp) continue;
    if (f.gapped) gapped++;
    //! 64 octets is the minimum Ethernet frame the padding inserter
    //! guarantees, FCS included
    if (f.octets < 64) short_frames++;
    if (n < records_.size() && records_[n].abort == 0 &&
        (records_[n].type != f.type || records_[n].seq != f.seq)) {
      wrong_tag++;
    }
    n++;
  }
  check.dec("pads: no gPTP frame had a gap inside it", gapped, 0);
  check.dec("pads: every gPTP frame reached the minimum frame length",
            short_frames, 0);
  check.dec("pads: the observer's tag is the tag on the wire", wrong_tag, 0);
  check.that("pads: the run carried frames to grade", n > 0);
}

//! B11: a frame fragmented on the wire is an abort and a counted loss,
//! not a successful measurement with a different correction. The arm names
//! the ONE frame it fragmented and grades that frame's own outcome, so a
//! loss somewhere else in the window cannot stand in for it.
void TxtsHarness::prove_fragment_aborts() {
  const uint16_t lost0 = dut->dbg_txts_lost_o;
  const uint16_t seq = peer_seq_++;
  Frame req = ptp_frame(0x2, seq, 0x0000, 20, kPeerCid);
  req.u64v(0);
  req.u64v(0);
  req.u32(0);
  send_peer(req.b);
  size_t target = 0;
  bool injected = false;
  const uint64_t until = now_ + kExchangeNs;
  while (now_ < until) {
    step();
    if (!injected && pad_open_ && pad_cur_.gptp && pad_idx_ == 30) {
      //! the frame now on the wire is the one this arm fragments
      target = gptp_pads();
      dut->obs_bubble_i = 1;
      run_ns(2 * kEthHalfNs);
      dut->obs_bubble_i = 0;
      injected = true;
    }
  }
  check.that("fragment: the bubble was injected inside a gPTP frame",
             injected);
  check.that("fragment: that frame reached the wire whole",
             target < gptp_pads());
  const bool have_record = target < records_.size();
  check.that("fragment: the observer produced a record for it", have_record);
  if (have_record) {
    //! the measured cycle distance is the refusal: it is not the expected
    //! one, and the record says so
    check.that("fragment: the observer refused it, by measurement",
               records_[target].abort != 0 || records_[target].delta != 45);
  }
  const bool have_result = target < results_.size();
  check.that("fragment: the plane delivered its result", have_result);
  if (have_result) {
    check.dec("fragment: that frame's own result is an explicit loss",
              results_[target].ok, 0);
  }
  check.that("fragment: the loss was counted",
             dut->dbg_txts_lost_o != lost0);
}

//! B7 and B13 over the PRODUCTION MAC: a recovery episode really destroys
//! the frames the fence separated, and an abort does not.
void TxtsHarness::prove_recovery_over_the_production_mac() {
  const uint16_t barr0 = dut->dbg_txts_barr_o;
  const uint64_t done0 = epi_done_count_;
  //! disable the guard, then break the observer: the barrier is raised with
  //! no reset level involved, and the guard cannot answer it
  dut->linkg_dis_i = 1;
  run_ns(4000);
  dut->obs_rst_i = 1;
  run_ns(2000);
  dut->obs_rst_i = 0;
  const uint64_t until = now_ + kRecoveryNs;
  while (now_ < until && dut->dbg_txts_barr_o == barr0) {
    exchange(0);
  }
  check.that("recovery: a broken observer raises a barrier",
             dut->dbg_txts_barr_o != barr0);
  check.that("recovery: the barrier seals the plane",
             (dut->dbg_txts_state_o & 0x8000u) != 0);
  const uint64_t req0 = recov_req_count_;
  run_ns(200000);
  check.that("recovery: a disabled guard is not asked",
             recov_req_count_ == req0);
  check.that("recovery: the seal holds while the demand is unmet",
             (dut->dbg_txts_state_o & 0x8000u) != 0);
  dut->linkg_dis_i = 0;
  const uint64_t until2 = now_ + kRecoveryNs;
  while (now_ < until2 && epi_done_count_ == done0) step();
  check.that("recovery: re-enabling the guard obtains an accepted episode",
             epi_done_count_ > done0);
  check.that("recovery: the completed episode unseals the plane",
             wait_unsealed(kRecoveryNs));
  check.that("recovery: stamping resumes over the production MAC",
             exchange(0));
}

//! The full-run laws.
void TxtsHarness::prove_full_run_laws() {
  check.that("laws: the wire carried gPTP frames", gptp_pads() > 0);
  check.that("laws: the plane delivered results", !results_.empty());
  //! every result named its own frame, in the order the wire carried them
  size_t n = 0;
  int wrong = 0;
  for (const PadFrame &f : pads_) {
    if (!f.gptp) continue;
    if (n < results_.size()) {
      if (results_[n].type != f.type || results_[n].seq != f.seq) wrong++;
    }
    n++;
  }
  check.dec("laws: every result carries its own frame's tag", wrong, 0);
  check.that("laws: no result was published for a frame the wire never "
             "carried", results_.size() <= n + 8);
  check.dec("laws: the observer never overran its crossing",
            dut->dbg_rec_ovr_o, 0);
}

int TxtsHarness::run() {
  prove_bring_up();
  prove_launch_reference();
  prove_queue_invariance();
  prove_bias_over_many_frames();
  prove_pads_are_byte_exact();
  prove_fragment_aborts();
  prove_recovery_over_the_production_mac();
  prove_full_run_laws();
  return check.report();
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  TxtsHarness harness;
  return harness.run();
}
