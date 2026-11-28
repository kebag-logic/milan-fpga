// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Injection handshake on the production tap and converted MII MAC chain.
// A fully checked frame waits with injection disabled. Once granted, a
// datapath frame arrives behind it. Measure grant to datapath acceptance,
// subtracting only the injected wire frame (not its inter-frame gap).
#include "Vusbnet_egress_chain.h"
#include "verilated.h"
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <vector>

namespace {
constexpr std::uint64_t kSysPs = 12500;
constexpr std::uint64_t kDpPs = 20000;
constexpr std::uint64_t kEthPs = 40000;
constexpr std::uint64_t kOctetPs = 80000;
constexpr unsigned kPhases = 8;

void require(bool yes, const char* why) {
    if (!yes) { std::fprintf(stderr, "FAIL: %s\n", why); std::exit(1); }
}

class Run {
 public:
    Run(unsigned dp, unsigned eth) : dut_(std::make_unique<Vusbnet_egress_chain>()),
        dp_next_(dp * kDpPs / kPhases + kDpPs / 2), eth_next_(eth * kEthPs / kPhases + kEthPs / 2) {}
    std::uint64_t measure(unsigned len);
 private:
    std::unique_ptr<Vusbnet_egress_chain> dut_;
    std::uint64_t now_ = 0;
    std::uint64_t sys_next_ = kSysPs / 2;
    std::uint64_t dp_next_;
    std::uint64_t eth_next_;
    std::uint64_t grant_ = 0;
    std::uint64_t hi_take_ = 0;
    std::uint64_t low_end_ = 0;
    std::vector<std::uint16_t> input_;
    std::size_t word_ = 0;
    unsigned high_pos_ = 0;
    unsigned frames_ = 0;
    unsigned nibbles_ = 0;
    unsigned low_nibbles_ = 0;
    bool enabled_ = false;
    bool previous_en_ = false;
    bool blocked_ = false;
    void step();
    void packet(unsigned kind, const std::vector<std::uint8_t>& bytes);
};

void Run::packet(unsigned kind, const std::vector<std::uint8_t>& bytes) {
    input_.push_back(bytes.size()); input_.push_back(kind);
    for (std::size_t i = 0; i < bytes.size(); i += 2)
        input_.push_back(bytes[i] | (i + 1 < bytes.size() ? unsigned(bytes[i + 1]) << 8 : 0));
}

void Run::step() {
    now_ = std::min({sys_next_, dp_next_, eth_next_});
    const bool sr = sys_next_ == now_ && !dut_->sys_clk;
    const bool sf = sys_next_ == now_ && dut_->sys_clk;
    const bool dr = dp_next_ == now_ && !dut_->dp_clk;
    const bool df = dp_next_ == now_ && dut_->dp_clk;
    const bool er = eth_next_ == now_ && !dut_->eth_tx_clk;
    const bool dn = sr && dut_->dn_valid && dut_->dn_ready;
    const bool dp = dr && dut_->dp_tvalid && dut_->dp_tready;
    if (sr && grant_ && dut_->hi_valid && !dut_->hi_ready) blocked_ = true;
    if (sr && dut_->hi_valid && dut_->hi_ready && !hi_take_) hi_take_ = now_;
    if (sys_next_ == now_) { dut_->sys_clk = !dut_->sys_clk; sys_next_ += kSysPs / 2; }
    if (dp_next_ == now_) { dut_->dp_clk = !dut_->dp_clk; dp_next_ += kDpPs / 2; }
    if (eth_next_ == now_) {
        dut_->eth_tx_clk = !dut_->eth_tx_clk; dut_->eth_rx_clk = dut_->eth_tx_clk;
        eth_next_ += kEthPs / 2;
    }
    dut_->eval();
    if (dn) ++word_;
    if (dp) high_pos_ += 8;
    if (dut_->active && !grant_) grant_ = now_;
    if (sf) {
        dut_->dn_valid = word_ < input_.size();
        dut_->dn_data = word_ < input_.size() ? input_[word_] : 0;
        dut_->inject_enable = enabled_;
    }
    if (df) {
        dut_->dp_tvalid = grant_ && high_pos_ < 64;
        dut_->dp_tlast = high_pos_ == 56;
        dut_->dp_tkeep = 255;
        dut_->dp_tdata = 0x5555555555555555ULL;
    }
    dut_->eval();
    if (er) {
        if (dut_->gmii_tx_en) ++nibbles_;
        if (!dut_->gmii_tx_en && previous_en_) {
            ++frames_;
            if (frames_ == 1) { low_end_ = now_; low_nibbles_ = nibbles_; }
            else require(nibbles_ == 2 * (8 + 64 + 4), "datapath frame length on MII pads");
            nibbles_ = 0;
        }
        previous_en_ = dut_->gmii_tx_en;
    }
}

std::uint64_t Run::measure(unsigned len) {
    dut_->sys_rst = dut_->dp_rst = dut_->eth_phy_rst = 1;
    while (now_ < 400000) step();
    dut_->sys_rst = dut_->dp_rst = dut_->eth_phy_rst = 0;
    while (now_ < 2000000) step();
    const std::vector<std::uint8_t> host = {2, 0x78, 0x56, 0x34, 0x12, 0x90};
    std::vector<std::uint8_t> station = host;
    station.insert(station.end(), {15, 0, 0, 0, 1, 0, 100, 0, 0, 0});
    packet(0x4e02, station);
    std::vector<std::uint8_t> frame(len, 0x55);
    std::fill_n(frame.begin(), 6, 0xff);
    std::copy(host.begin(), host.end(), frame.begin() + 6);
    frame[12] = 8; frame[13] = 0;
    packet(0x4e01, frame);
    while (word_ < input_.size() && now_ < 100000000) step();
    require(word_ == input_.size(), "checked network frame accepted");
    const auto settle = now_ + 1000000;
    while (now_ < settle) step();
    require(!grant_ && !frames_, "disabled injection remains pending");
    enabled_ = true;
    const auto limit = now_ + 500000000;
    while (now_ < limit && frames_ < 2) step();
    require(frames_ == 2 && grant_ && hi_take_, "both injected and datapath frames depart");
    require(blocked_, "datapath is held behind injection");
    require(low_nibbles_ == 2 * (8 + std::max(len, 60u) + 4), "injected length on MII pads");
    require(hi_take_ >= low_end_ - kEthPs, "datapath waits for injected PHY completion");
    const auto wire = (8 + std::max(len, 60u) + 4) * kOctetPs;
    const auto elapsed = hi_take_ - grant_;
    return elapsed > wire ? elapsed - wire : 0;
}
}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    for (const unsigned len : {14u, 60u, 64u, 90u, 127u, 512u, 1514u, 1515u})
        for (unsigned d = 0; d < kPhases; ++d)
            for (unsigned e = 0; e < kPhases; ++e) {
                Run run(d, e);
                std::printf("HANDSHAKE %u %u %u %llu\n", len, d, e,
                            static_cast<unsigned long long>(run.measure(len)));
            }
    return 0;
}
