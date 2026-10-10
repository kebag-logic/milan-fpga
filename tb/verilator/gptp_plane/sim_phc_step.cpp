// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Issue #621: real PHC, independent peer LocalClock and real second cadence.
// A better Announce followed by Sync/Follow_Up drives each signed 10 ms step.
// Peer delay timestamps never derive from the DUT's PHC. The physical link
// is 500 ns each way and the responder turnaround is 800 us.
#include "Vgptp_plane_wrap.h"
#include "../../common/verilator_harness.hpp"
#include <verilated.h>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <vector>
#include <utility>

namespace {
constexpr uint64_t kHz = 8000000;
constexpr uint64_t kTickNs = 125;
constexpr uint64_t kLinkNs = 500;
constexpr uint64_t kTurnNs = 800000;
constexpr uint64_t kOurId = 0x02A1B2FFFEC3D4E5ULL;
constexpr uint64_t kPeerId = 0x0080E1FFFE112233ULL;
constexpr uint64_t kPeerEpochNs = 20000000000ULL;
constexpr uint64_t kGmA = 0x00AACCFFFE010203ULL;
constexpr uint64_t kGmB = 0x00BBDDFFFE040506ULL;

struct Frame {
  std::vector<uint8_t> bytes;
  void put(uint64_t v, unsigned n) {
    for (unsigned i = n; i != 0; --i)
      bytes.push_back(static_cast<uint8_t>(v >> (8 * (i - 1))));
  }
  void timestamp(uint64_t ns) { put(ns / 1000000000, 6); put(ns % 1000000000, 4); }
};

Frame header(unsigned type, uint16_t seq, unsigned body, unsigned flags = 0) {
  Frame f;
  f.put(0x0180C200000EULL, 6); f.put(0x0080E1112233ULL, 6); f.put(0x88F7, 2);
  f.put(0x10 | type, 1); f.put(2, 1); f.put(34 + body, 2);
  f.put(0, 2); f.put(flags, 2); f.put(0, 8); f.put(0, 4);
  f.put(kPeerId, 8); f.put(1, 2); f.put(seq, 2); f.put(5, 1); f.put(0x7F, 1);
  return f;
}

struct Scheduled {
  uint64_t cycle;
  Frame frame;
};

struct Stamp {
  uint64_t cycle;
  uint64_t ns;
  uint16_t seq;
  unsigned type;
};

class Harness {
 public:
  int run() {
    dut_->rst_n = 0;
    dut_->tx_ready_i = 1; dut_->tx_credit_i = 1;
    dut_->txts_ok_i = 1; dut_->txts_gen_i = 1;
    for (int i = 0; i < 8; ++i) tick();
    dut_->rst_n = 1;
    drive(6 * kHz);
    check_.that("setup: asCapable and sync established", (dut_->pub_flags_o & 13) == 13);
    check_.that("setup: independent peer yields physical link delay", valid_delay());
    exercise_step("forward", 10000000, kGmB, 50);
    exercise_step("backward", -10000000, kGmA, 25);
    exercise_crossing("t1 before forward step", 10000000, 200, 500, 0);
    exercise_crossing("t1 before backward step", -10000000, 200, 500, 0);
    exercise_crossing("response before step", 10000000, 6600, 4000, 0);
    exercise_crossing("deferred t1 after step", -10000000, 9000, 500, 20000);
    prove_real_failures();
    exercise_liveness();
    return check_.report();
  }

 private:
  const milan::tb::Model<Vgptp_plane_wrap> model_;
  Vgptp_plane_wrap* dut_ = model_.get();
  milan::tb::Checker check_{"phc_step"};
  uint64_t cycle_ = 0;
  uint64_t gm_epoch_ns_ = 1000000000;
  uint64_t gm_id_ = kGmA;
  unsigned priority_ = 100;
  uint16_t sync_seq_ = 1;
  uint16_t announce_seq_ = 1;
  uint64_t next_sync_ = kHz / 8;
  uint64_t next_announce_ = kHz / 2;
  uint64_t steps_ = 0;
  int64_t last_step_ns_ = 0;
  uint64_t last_step_cycle_ = 0;
  uint64_t last_request_cycle_ = 0;
  uint64_t exchanges_ = 0;
  std::deque<Scheduled> frames_;
  std::deque<Stamp> stamps_;
  uint64_t link_ns_ = kLinkNs;
  uint64_t fu_delay_cycles_ = 500;
  uint64_t stamp_delay_cycles_ = 0;
  bool answer_ = true;
  bool silent_after_probe_ = false;
  uint64_t unanswered_ = 0;
  uint64_t unanswered_at_drop_ = 0;
  Frame receiving_;
  size_t rx_offset_ = 0;
  std::vector<uint8_t> transmitting_;
  uint64_t tx_phc_ns_ = 0;
  uint64_t tx_cycle_ = 0;
  bool monitor_ = false;
  bool capable_prev_ = false;
  uint64_t drops_ = 0;
  uint64_t bad_delays_ = 0;
  uint64_t low_start_ = 0;
  uint64_t low_ticks_ = 0;
  uint64_t probe_request_ = 0;
  uint64_t probe_response_ = 0;
  uint64_t probe_follow_up_ = 0;
  uint64_t probe_stamp_ = 0;
  uint16_t probe_seq_ = 0;

  bool valid_delay() const {
    return dut_->pub_pdelay_ns_o >= kLinkNs - kTickNs &&
           dut_->pub_pdelay_ns_o <= kLinkNs + kTickNs;
  }

  void schedule(Frame frame, uint64_t at) {
    auto it = frames_.begin();
    while (it != frames_.end() && it->cycle <= at) ++it;
    frames_.insert(it, Scheduled{at, std::move(frame)});
  }

  void announce() {
    auto f = header(0xB, announce_seq_++, 30, 8);
    f.timestamp(0); f.put(0xFFC4, 2); f.put(0, 1);
    f.put(priority_, 1); f.put(0xF8FE436A, 4); f.put(248, 1);
    f.put(gm_id_, 8); f.put(0, 2); f.put(0xA0, 1);
    schedule(std::move(f), cycle_);
  }

  void sync() {
    const auto seq = sync_seq_++;
    auto f = header(0, seq, 10, 0x0208);
    f.timestamp(0);
    // Its origin is finalized at actual SOF, after any queued response.
    schedule(std::move(f), cycle_);
  }

  void start_receive() {
    if (!receiving_.bytes.empty() || frames_.empty() || frames_.front().cycle > cycle_)
      return;
    receiving_ = std::move(frames_.front().frame);
    frames_.pop_front(); rx_offset_ = 0;
    dut_->rx_ts_i = dut_->phc_ns_o;
    const unsigned type = receiving_.bytes[14] & 15;
    const uint16_t seq = (receiving_.bytes[44] << 8) | receiving_.bytes[45];
    if (monitor_ && probe_request_ && seq == probe_seq_) {
      if (type == 3) probe_response_ = cycle_;
      if (type == 10) probe_follow_up_ = cycle_;
    }
    if ((receiving_.bytes[14] & 15) == 0) {
      const uint16_t seq = (receiving_.bytes[44] << 8) | receiving_.bytes[45];
      auto fu = header(8, seq, 42);
      fu.timestamp(cycle_ * kTickNs + gm_epoch_ns_ - link_ns_);
      fu.put(3, 2); fu.put(28, 2); fu.put(0x0080C2, 3); fu.put(1, 3);
      fu.put(0, 4); fu.put(0, 2); fu.put(0, 8); fu.put(0, 4); fu.put(0, 4);
      schedule(std::move(fu), cycle_ + 500);
    }
  }

  void transmit_complete() {
    if (transmitting_.size() < 46) return;
    const unsigned type = transmitting_[14] & 15;
    const uint16_t seq = (transmitting_[44] << 8) | transmitting_[45];
    if (type == 0 || type == 2 || type == 3) {
      stamps_.push_back({cycle_ + (type == 2 ? stamp_delay_cycles_ : 0), tx_phc_ns_, seq, type});
    }
    if (type != 2) return;
    last_request_cycle_ = tx_cycle_;
    if (monitor_ && !probe_request_) {
      probe_request_ = tx_cycle_; probe_seq_ = seq;
    }
    if (silent_after_probe_ && seq != probe_seq_) { ++unanswered_; return; }
    if (!answer_) return;
    const uint64_t t2 = tx_cycle_ * kTickNs + kPeerEpochNs + link_ns_;
    const uint64_t t3 = t2 + kTurnNs;
    const uint64_t response_cycle = tx_cycle_ + (2 * link_ns_ + kTurnNs) / kTickNs;
    auto response = header(3, seq, 20, 0x0200);
    response.timestamp(t2); response.put(kOurId, 8); response.put(1, 2);
    schedule(std::move(response), response_cycle);
    auto fu = header(0xA, seq, 20);
    fu.timestamp(t3); fu.put(kOurId, 8); fu.put(1, 2);
    schedule(std::move(fu), response_cycle + fu_delay_cycles_);
    ++exchanges_;
  }

  void tick() {
    if (!dut_->txts_valid_i && !stamps_.empty() && stamps_.front().cycle <= cycle_) {
      const auto stamp = stamps_.front(); stamps_.pop_front();
      dut_->txts_ns_i = stamp.ns; dut_->txts_seq_i = stamp.seq;
      dut_->txts_type_i = stamp.type; dut_->txts_valid_i = 1;
    }
    start_receive();
    dut_->rx_valid_i = !receiving_.bytes.empty();
    dut_->rx_sof_i = dut_->rx_valid_i && rx_offset_ == 0;
    dut_->rx_eof_i = dut_->rx_valid_i && rx_offset_ + 1 == receiving_.bytes.size();
    if (dut_->rx_valid_i) dut_->rx_data_i = receiving_.bytes[rx_offset_];
    dut_->clk_i = 0; dut_->eval();
    const bool stamp_taken = dut_->txts_valid_i && dut_->txts_ready_o;
    if (dut_->tx_valid_o && dut_->tx_ready_i) {
      if (dut_->tx_sof_o) {
        transmitting_.clear(); tx_phc_ns_ = dut_->phc_ns_o; tx_cycle_ = cycle_;
      }
      transmitting_.push_back(dut_->tx_data_o);
    }
    const bool tx_end = dut_->tx_valid_o && dut_->tx_ready_i && dut_->tx_eof_o;
    dut_->clk_i = 1; dut_->eval();
    if (stamp_taken) {
      if (monitor_ && dut_->txts_type_i == 2 && dut_->txts_seq_i == probe_seq_)
        probe_stamp_ = cycle_;
      dut_->txts_valid_i = 0;
    }
    if (tx_end) transmit_complete();
    if (dut_->rx_valid_i && ++rx_offset_ == receiving_.bytes.size()) receiving_.bytes.clear();
    if (dut_->tap_step_we_o) {
      ++steps_; last_step_ns_ = static_cast<int64_t>(dut_->tap_step_o);
      last_step_cycle_ = cycle_;
      printf("STEP cycle=%llu ns=%lld\n", static_cast<unsigned long long>(cycle_),
             static_cast<long long>(last_step_ns_));
    }
    const bool capable = (dut_->pub_flags_o & 4) != 0;
    if (monitor_) {
      if (!capable && capable_prev_) {
        ++drops_; low_start_ = cycle_; unanswered_at_drop_ = unanswered_;
        printf("LOSS cycle=%llu delay=%d since_step_ns=%llu unanswered=%llu\n",
               static_cast<unsigned long long>(cycle_), static_cast<int32_t>(dut_->pub_pdelay_ns_o),
               static_cast<unsigned long long>((cycle_ - last_step_cycle_) * kTickNs),
               static_cast<unsigned long long>(unanswered_));
      }
      if (capable && !capable_prev_) {
        low_ticks_ += cycle_ - low_start_;
        printf("RETURN outage_ns=%llu\n", static_cast<unsigned long long>((cycle_ - low_start_) * kTickNs));
      }
      if (dut_->pub_commit_o && !valid_delay()) ++bad_delays_;
    }
    capable_prev_ = capable;
    ++cycle_;
  }

  void drive(uint64_t cycles) {
    const uint64_t end = cycle_ + cycles;
    while (cycle_ < end) {
      if (cycle_ >= next_announce_) { announce(); next_announce_ = cycle_ + kHz; }
      if (cycle_ >= next_sync_) { sync(); next_sync_ = cycle_ + kHz / 8; }
      tick();
    }
  }

  void exercise_step(const char* name, int64_t delta, uint64_t identity, unsigned priority) {
    gm_id_ = identity; priority_ = priority;
    exercise(name, delta, kHz / 10);
  }

  void exercise_crossing(const char* name, int64_t delta, uint64_t phase,
                         uint64_t fu_delay, uint64_t stamp_delay) {
    // Reach 1 ms before the next scheduled request. Its cadence is fixed
    // by the timer, and every observed request checks that assumption below.
    const uint64_t target = last_request_cycle_ + kHz;
    if (target > cycle_ + 8000) drive(target - cycle_ - 8000);
    fu_delay_cycles_ = fu_delay; stamp_delay_cycles_ = stamp_delay;
    gm_id_ = gm_id_ == kGmA ? kGmB : kGmA;
    --priority_;
    exercise(name, delta, target + phase - cycle_);
    check_.that("crossing: request precedes the actual step", probe_request_ < last_step_cycle_);
    if (stamp_delay) {
      check_.that("crossing: complete response precedes step and delayed t1 follows",
                  probe_response_ < probe_follow_up_ && probe_follow_up_ < last_step_cycle_ &&
                  last_step_cycle_ < probe_stamp_);
    } else if (fu_delay > 500) {
      check_.that("crossing: step falls between response and follow-up",
                  probe_response_ < last_step_cycle_ && last_step_cycle_ < probe_follow_up_);
    } else {
      check_.that("crossing: step falls between returned t1 and response",
                  probe_stamp_ < last_step_cycle_ && last_step_cycle_ < probe_response_);
    }
    fu_delay_cycles_ = 500; stamp_delay_cycles_ = 0;
  }

  void exercise(const char* name, int64_t delta, uint64_t sync_delay) {
    const uint64_t initial_steps = steps_;
    const uint64_t initial_exchanges = exchanges_;
    drops_ = bad_delays_ = low_ticks_ = 0;
    probe_request_ = probe_response_ = probe_follow_up_ = probe_stamp_ = 0;
    monitor_ = true;
    gm_epoch_ns_ += delta;
    announce(); next_announce_ = cycle_ + kHz;
    // Place the new Sync at the selected phase of the peer exchange.
    next_sync_ = cycle_ + sync_delay;
    drive(4 * kHz);
    monitor_ = false;
    printf("ARM %s drops=%llu outage_ns=%llu exchanges=%llu last_req=%llu\n", name,
           static_cast<unsigned long long>(drops_), static_cast<unsigned long long>(low_ticks_ * kTickNs),
           static_cast<unsigned long long>(exchanges_ - initial_exchanges),
           static_cast<unsigned long long>(last_request_cycle_));
    check_.dec("one grandmaster-driven step", steps_ - initial_steps, 1);
    check_.that("step has intended sign and magnitude", last_step_ns_ >= delta - 1000 && last_step_ns_ <= delta + 1000);
    check_.dec("asCapable never falls after step", drops_, 0);
    check_.dec("no invalid link-delay publication", bad_delays_, 0);
    check_.that("four peer exchanges actually occurred", exchanges_ - initial_exchanges >= 4);
    check_.that("settled link delay remains physical", valid_delay());
  }

  void prove_real_failures() {
    link_ns_ = 1500;
    drive(2 * kHz);
    check_.dec("real excessive delay still clears asCapable", dut_->pub_flags_o & 4, 0);
    link_ns_ = kLinkNs;
    drive(3 * kHz);
    check_.dec("good exchanges requalify after real fault", dut_->pub_flags_o & 4, 4);
    answer_ = false;
    drive(5 * kHz);
    check_.dec("missing peer still clears asCapable", dut_->pub_flags_o & 4, 0);
  }

  void exercise_liveness() {
    // A received response resets lostResponses (IEEE 802.1AS-2020 11.2.19).
    // allowedLostResponses is 3 (11.2.13.4), so after a crossing exchange
    // that is answered, the fourth unanswered request, not the third,
    // clears asCapable when the next interval judges it lost.
    answer_ = true;
    drive(4 * kHz);
    check_.dec("liveness: answered exchanges requalify after silence", dut_->pub_flags_o & 4, 4);
    const uint64_t target = last_request_cycle_ + kHz;
    if (target > cycle_ + 8000) drive(target - cycle_ - 8000);
    gm_id_ = gm_id_ == kGmA ? kGmB : kGmA;
    --priority_;
    const uint64_t initial_steps = steps_;
    drops_ = bad_delays_ = low_ticks_ = unanswered_ = unanswered_at_drop_ = 0;
    probe_request_ = probe_response_ = probe_follow_up_ = probe_stamp_ = 0;
    monitor_ = silent_after_probe_ = true;
    gm_epoch_ns_ += 10000000;
    announce(); next_announce_ = cycle_ + kHz;
    // The step lands between the crossing request's returned t1 and its response.
    next_sync_ = target + 200;
    drive(6 * kHz);
    monitor_ = silent_after_probe_ = false;
    printf("ARM liveness drops=%llu unanswered=%llu unanswered_at_drop=%llu\n",
           static_cast<unsigned long long>(drops_), static_cast<unsigned long long>(unanswered_),
           static_cast<unsigned long long>(unanswered_at_drop_));
    check_.dec("liveness: one grandmaster-driven step", steps_ - initial_steps, 1);
    check_.that("liveness: step falls between returned t1 and response",
                probe_stamp_ < last_step_cycle_ && last_step_cycle_ < probe_response_);
    check_.dec("liveness: no invalid link-delay publication", bad_delays_, 0);
    check_.dec("liveness: asCapable falls once while the peer is silent", drops_, 1);
    check_.dec("asCapable falls at the fourth unanswered request after a crossing exchange",
               unanswered_at_drop_, 4);
  }
};
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Harness harness;
  return harness.run();
}
