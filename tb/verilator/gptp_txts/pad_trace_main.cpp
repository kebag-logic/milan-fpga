// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// One deterministic stimulus through the CONVERTED MAC transmit chain, and
// the octet trace its pads produced.
//
// WHY THIS IS SEPARATE FROM THE CLOSED LOOP. This binary grades nothing. It
// exists so `sw/litex/test_gptp_tx_timestamp.py` can drive the identical
// stimulus through the migen objects the chain was converted FROM and
// require the two pad traces to agree; that comparison is what turns "this
// Verilog is the product's transmit chain" from a property of the converter
// into a checked claim. The chain is instantiated ALONE here - no plane, no
// arbiter, no engine - because the comparable object on the migen side is
// the chain alone.
//
// The stimulus is fixed and has no protocol in it: five frames that are not
// gPTP, pushed back to back at the datapath boundary as fast as the chain
// accepts them, which is faster than the wire carries them, so the chain
// runs with a full queue and the pads run without a gap of their own.
//
// Usage: Vmac_tx_chain_pads <trace file>
// Each line is `<tx_en> <tx_data as two hex digits>`, one per wire cycle.

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <utility>
#include <vector>

#include "Vmac_tx_chain.h"

#include "../../common/verilator_harness.hpp"

namespace {

//! The product's clock periods, in nanoseconds: 125 MHz at the wire, 100 MHz
//! at the MAC system side, 50 MHz at the datapath. The migen run drives the
//! same three numbers into its own simulator.
constexpr uint64_t kEthPeriodNs = 8;
constexpr uint64_t kSysPeriodNs = 10;
constexpr uint64_t kDpPeriodNs = 20;

//! how long the chain is held in reset, and how long it is left alone
//! afterwards before the first beat is offered
constexpr uint64_t kResetNs = 400;
constexpr uint64_t kSettleNs = 400;
//! the run is over when the pads have been idle this long with nothing left
//! to push, which ends it on the chain's own behaviour rather than on a
//! wall-clock guess
constexpr uint64_t kDrainNs = 2000;

//! The same lengths, in the same order, as `FRAME_LENGTHS` on the migen
//! side. 46 is below the minimum frame length so the padding stage is in
//! the comparison, 67 is not a whole number of 64-bit beats so the
//! `last_be` conversion is, and 1518 is the largest frame the product
//! carries. The gate reconciles the two lists rather than trusting them.
//!
//! THE LARGEST FRAME IS FIRST on purpose. It occupies the wire for twelve
//! microseconds while the remaining three hundred octets arrive in one, so
//! the source is never what the wire is waiting for and every later gap is
//! the chain's own inter-frame gap. Starved of data the gap instead
//! measures the phase between this harness's source and the wire, and that
//! phase differs from the migen run's by the one cycle their two reset
//! models differ by - a property of the two simulators, not of the chain.
const std::vector<size_t> kLengths = {1518, 46, 64, 67, 128};

//! A frame of `len` octets that is not gPTP. Byte for byte the frame
//! `background_frame()` builds in the closed loop and `background_frame()`
//! builds in the migen gate.
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

//! The chain, its three clocks and the one source that feeds it.
class PadTrace {
 public:
  int write(const char *path);

 private:
  const milan::tb::Model<Vmac_tx_chain> model_;
  Vmac_tx_chain *dut = model_.get();

  //! The three clocks start LOW and first rise at their own half period,
  //! which is where migen's simulator puts the first rising edge of a clock
  //! it is given a period for. The equivalence gate drives this harness and
  //! that simulator with one stimulus and compares the pads, so the two
  //! have to agree about the phases as well as the periods; with these
  //! three no two rising edges ever coincide, so neither run has an
  //! ordering to decide.
  uint64_t now_ = 0;
  uint64_t eth_next_ = kEthPeriodNs / 2;
  uint64_t sys_next_ = kSysPeriodNs / 2;
  uint64_t dp_next_ = kDpPeriodNs / 2;

  std::vector<uint8_t> src_;     //! the frame being pushed, if any
  size_t src_pos_ = 0;
  size_t sent_ = 0;              //! how many of kLengths have been started
  //! Nothing is offered until the trace is recording, so the FIRST frame in
  //! the trace is a whole frame. A run that started pushing during reset
  //! put the tail of one frame at the top of the file, which is not a
  //! comparable object.
  bool armed_ = false;
  std::vector<std::pair<uint8_t, uint8_t>> trace_;

  void step();
  void drive_source();
  void run_ns(uint64_t span);
};

//! One scheduler step: advance to the next clock edge and evaluate it.
//!
//! The source is presented on the DATAPATH FALLING edge, after the rising
//! edge that consumed the previous beat, so a beat is never replaced at the
//! same instant it is being accepted.
void PadTrace::step() {
  now_ = std::min({eth_next_, sys_next_, dp_next_});
  const bool eth_rise = (eth_next_ == now_) && (dut->eth_tx_clk == 0);
  const bool dp_rise = (dp_next_ == now_) && (dut->dp_clk == 0);
  const bool dp_fall = (dp_next_ == now_) && (dut->dp_clk != 0);
  //! read BEFORE the edge: this is the handshake the chain itself sees
  const bool accepted = dp_rise && (dut->dp_tvalid != 0) &&
                        (dut->dp_tready != 0);
  if (eth_next_ == now_) {
    dut->eth_tx_clk = !dut->eth_tx_clk;
    dut->eth_rx_clk = dut->eth_tx_clk;
    eth_next_ += kEthPeriodNs / 2;
  }
  if (sys_next_ == now_) {
    dut->sys_clk = !dut->sys_clk;
    sys_next_ += kSysPeriodNs / 2;
  }
  if (dp_next_ == now_) {
    dut->dp_clk = !dut->dp_clk;
    dp_next_ += kDpPeriodNs / 2;
  }
  dut->eval();
  if (accepted) src_pos_ += 8;
  if (dp_fall) drive_source();
  dut->eval();
  //! the pads are sampled where a receiver samples them: on the rising edge
  //! of the wire clock, after that edge has been evaluated
  if (eth_rise) {
    trace_.emplace_back(static_cast<uint8_t>(dut->gmii_tx_en),
                        static_cast<uint8_t>(dut->gmii_tx_data));
  }
}

//! Present the next beat, or start the next frame, or go idle.
void PadTrace::drive_source() {
  if (!armed_) return;
  if (src_pos_ >= src_.size()) {
    src_.clear();
    src_pos_ = 0;
    if (sent_ < kLengths.size()) {
      src_ = background_frame(kLengths[sent_],
                              static_cast<uint8_t>(0xA0 + sent_));
      sent_++;
    }
  }
  if (src_.empty()) {
    dut->dp_tvalid = 0;
    dut->dp_tlast = 0;
    return;
  }
  uint64_t data = 0;
  uint8_t keep = 0;
  for (size_t i = 0; i < 8 && src_pos_ + i < src_.size(); i++) {
    data |= static_cast<uint64_t>(src_[src_pos_ + i]) << (8 * i);
    keep = static_cast<uint8_t>(keep | (1u << i));
  }
  dut->dp_tdata = data;
  dut->dp_tkeep = keep;
  dut->dp_tvalid = 1;
  dut->dp_tlast = (src_pos_ + 8 >= src_.size()) ? 1 : 0;
}

void PadTrace::run_ns(uint64_t span) {
  const uint64_t until = now_ + span;
  while (now_ < until) step();
}

//! Reset, push the frames, drain, and write what the pads carried.
int PadTrace::write(const char *path) {
  dut->sys_clk = 0;
  dut->dp_clk = 0;
  dut->eth_tx_clk = 0;
  dut->eth_rx_clk = 0;
  dut->sys_rst = 1;
  dut->dp_rst = 1;
  dut->eth_phy_rst = 1;
  dut->reinit = 0;
  dut->eth_rst = 0;
  dut->loopback = 0;
  dut->dp_tdata = 0;
  dut->dp_tkeep = 0;
  dut->dp_tvalid = 0;
  dut->dp_tlast = 0;
  run_ns(kResetNs);
  dut->sys_rst = 0;
  dut->dp_rst = 0;
  dut->eth_phy_rst = 0;
  run_ns(kSettleNs);

  //! from here the trace is the answer, so it starts empty and the source
  //! starts offering
  trace_.clear();
  armed_ = true;
  uint64_t idle_since = now_;
  while (true) {
    step();
    if (dut->gmii_tx_en != 0 || sent_ < kLengths.size() || !src_.empty()) {
      idle_since = now_;
    } else if (now_ - idle_since >= kDrainNs) {
      break;
    }
  }

  std::FILE *out = std::fopen(path, "w");
  if (out == nullptr) {
    std::fprintf(stderr, "cannot write %s\n", path);
    return 1;
  }
  for (const auto &sample : trace_) {
    std::fprintf(out, "%u %02x\n", sample.first, sample.second);
  }
  std::fclose(out);
  std::printf("converted chain: %zu wire cycles, %zu frames pushed\n",
              trace_.size(), sent_);
  return 0;
}

}  // namespace

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  if (argc < 2) {
    std::fprintf(stderr, "usage: %s <trace file>\n", argv[0]);
    return 2;
  }
  PadTrace trace;
  return trace.write(argv[1]);
}
