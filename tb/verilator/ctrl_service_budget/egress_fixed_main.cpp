// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The fixed path of the 100 Mb/s egress row (egress_mii.py, MII_FIXED_NS): one frame at a time through the CONVERTED
// MII transmit chain (tb/verilator/gptp_txts/generated/mac_tx_chain_mii.v, sw/litex/gen_mac_tx_model.py), from the
// last beat its datapath boundary accepts to the last nibble at its pads, less that frame's wire time. The chain is
// otherwise idle, so nothing queues: what is left is its crossing, the store-and-forward FIFO's release, the MAC
// core's pipeline and crossing, and the PHY stage. The clocks are the Arty point's, 80 MHz sys, 50 MHz datapath and
// the 25 MHz MII transmit clock, each phase of the datapath and wire clocks against sys swept.
//
// Usage: Vmac_tx_chain_mii <length>...   One line per length and phase: `FIXED <length> <dp> <eth> <ps>`.
#include "Vmac_tx_chain_mii.h"
#include "verilated.h"

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <vector>

namespace {

// The sys period, ps: the Arty 1x1's 80 MHz unless the build names another (the 4x4 runs sys at 100 MHz).
#ifndef EGRESS_FIXED_SYS_PS
#define EGRESS_FIXED_SYS_PS 12500
#endif
constexpr std::uint64_t kSysPs = EGRESS_FIXED_SYS_PS;
constexpr std::uint64_t kDpPs = 20000;
constexpr std::uint64_t kEthPs = 40000;
constexpr std::uint64_t kOctetPs = 80000;
constexpr unsigned kPhases = 8;

// One run: reset, settle, one frame of `len` bytes at the boundary, and the chain's own latency.
class Run {
 public:
    Run(std::uint64_t dp_offset, std::uint64_t eth_offset)
        : dut_(std::make_unique<Vmac_tx_chain_mii>()), dp_next_(dp_offset + kDpPs / 2),
          eth_next_(eth_offset + kEthPs / 2) {}

    std::uint64_t fixed(std::size_t len);

 private:
    std::unique_ptr<Vmac_tx_chain_mii> dut_;
    std::uint64_t now_ = 0;
    std::uint64_t sys_next_ = kSysPs / 2;
    std::uint64_t dp_next_;
    std::uint64_t eth_next_;
    std::size_t pos_ = 0;
    std::size_t len_ = 0;
    bool armed_ = false;
    std::uint64_t last_beat_ = 0;
    std::uint64_t last_nibble_ = 0;

    void step();
    void drive();
};

void Run::step() {
    now_ = std::min({sys_next_, dp_next_, eth_next_});
    const bool dp_rise = dp_next_ == now_ && dut_->dp_clk == 0;
    const bool dp_fall = dp_next_ == now_ && dut_->dp_clk != 0;
    const bool eth_rise = eth_next_ == now_ && dut_->eth_tx_clk == 0;
    const bool accepted = dp_rise && dut_->dp_tvalid != 0 && dut_->dp_tready != 0;
    const bool last = accepted && dut_->dp_tlast != 0;
    if (sys_next_ == now_) {
        dut_->sys_clk = !dut_->sys_clk;
        sys_next_ += kSysPs / 2;
    }
    if (dp_next_ == now_) {
        dut_->dp_clk = !dut_->dp_clk;
        dp_next_ += kDpPs / 2;
    }
    if (eth_next_ == now_) {
        dut_->eth_tx_clk = !dut_->eth_tx_clk;
        dut_->eth_rx_clk = dut_->eth_tx_clk;
        eth_next_ += kEthPs / 2;
    }
    dut_->eval();
    if (accepted) pos_ += 8;
    if (last) last_beat_ = now_;
    if (dp_fall) drive();
    dut_->eval();
    if (eth_rise && dut_->gmii_tx_en != 0) last_nibble_ = now_;
}

void Run::drive() {
    const bool on = armed_ && pos_ < len_;
    dut_->dp_tvalid = on;
    dut_->dp_tlast = on && pos_ + 8 >= len_;
    dut_->dp_tkeep = 0;
    dut_->dp_tdata = 0;
    if (!on) return;
    for (std::size_t i = 0; i < 8 && pos_ + i < len_; ++i) dut_->dp_tkeep |= 1u << i;
    dut_->dp_tdata = pos_ == 0 ? 0x0000554433221102ULL : 0xa5a5a5a5a5a5a5a5ULL;
}

std::uint64_t Run::fixed(std::size_t len) {
    dut_->sys_rst = 1;
    dut_->dp_rst = 1;
    dut_->eth_phy_rst = 1;
    dut_->reinit = 0;
    dut_->eth_rst = 0;
    dut_->loopback = 0;
    while (now_ < 400000) step();
    dut_->sys_rst = 0;
    dut_->dp_rst = 0;
    dut_->eth_phy_rst = 0;
    while (now_ < 800000) step();
    len_ = len;
    armed_ = true;
    const std::uint64_t wire = (8 + std::max<std::size_t>(len, 60) + 4) * kOctetPs;
    while (now_ < 800000 + 4 * wire + 20000000) step();
    if (last_beat_ == 0 || last_nibble_ <= last_beat_) {
        std::fprintf(stderr, "length %zu: no frame on the pads\n", len);
        std::exit(1);
    }
    return last_nibble_ + kEthPs - last_beat_ - wire;
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    std::vector<std::size_t> lengths;
    for (int i = 1; i < argc; ++i) {
        if (argv[i][0] != '+') lengths.push_back(std::strtoul(argv[i], nullptr, 10));
    }
    if (lengths.empty()) {
        std::fprintf(stderr, "usage: %s <length>...\n", argv[0]);
        return 2;
    }
    for (const std::size_t len : lengths) {
        for (unsigned d = 0; d < kPhases; ++d) {
            for (unsigned e = 0; e < kPhases; ++e) {
                Run run(d * kDpPs / kPhases, e * kEthPs / kPhases);
                std::printf("FIXED %zu %u %u %llu\n", len, d, e,
                            static_cast<unsigned long long>(run.fixed(len)));
            }
        }
    }
    return 0;
}
