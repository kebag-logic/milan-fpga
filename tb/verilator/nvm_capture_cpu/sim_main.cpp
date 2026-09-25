// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "Vsim.h"
#include "probe_config.hpp"
#include "verilator_harness.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>

namespace {
// Minimum Ethernet frame excluding FCS. AECP AEM READ_DESCRIPTOR ENTITY 0.
std::array<std::uint8_t, 60> request(std::uint16_t sequence) {
    std::array<std::uint8_t, 60> frame{};
    frame[0] = 2;
    frame[5] = 1;
    frame[6] = 2;
    frame[11] = 2;
    frame[12] = 0x22;
    frame[13] = 0xf0;
    frame[14] = 0xfb;
    frame[17] = 20;
    frame[18] = 2;
    frame[21] = 0xff;
    frame[22] = 0xfe;
    frame[25] = 1;
    frame[26] = 2;
    frame[29] = 0xff;
    frame[30] = 0xfe;
    frame[33] = 2;
    frame[34] = sequence >> 8;
    frame[35] = sequence & 0xff;
    frame[37] = 4;
    return frame;
}

class Controller {
public:
    void sample(Vsim& dut) {
        // Firmware keeps active high only over the record walk and byte copy.
        if (dut.probe_active && !active_) {
            dut.probe_requests = 0;
            dut.probe_responses = 0;
            dut.probe_reads = 0;
        }
        active_ = dut.probe_active;
        if (dut.traffic_rx_valid && dut.traffic_rx_ready) {
            offset_ += 8;
            if (offset_ >= frame_.size()) {
                if (active_) ++dut.probe_requests;
                offset_ = 0;
                frame_ = request(++sequence_);
            }
        }
        if (dut.traffic_tx_valid && dut.traffic_tx_ready) {
            for (unsigned i = 0; i < 8; ++i) {
                if (dut.traffic_tx_keep & (1u << i))
                    response_.push_back((dut.traffic_tx_data >> (8 * i)) & 0xff);
            }
            if (dut.traffic_tx_last) {
                if (traced_ < 5) {
                    std::printf("\nTX_FRAME bytes=%zu header=", response_.size());
                    for (unsigned i = 0; i < std::min<std::size_t>(46, response_.size()); ++i)
                        std::printf("%02x", response_[i]);
                    std::printf("\n");
                    std::fflush(stdout);
                    ++traced_;
                }
                if (active_ && good_response()) ++dut.probe_responses;
                response_.clear();
            }
        }
    }

    void drive(Vsim& dut) const {
        dut.traffic_rx_valid = dut.probe_enable;
        dut.traffic_rx_data = 0;
        dut.traffic_rx_keep = 0;
        for (unsigned i = 0; i < 8 && offset_ + i < frame_.size(); ++i) {
            dut.traffic_rx_data |= static_cast<std::uint64_t>(frame_[offset_ + i]) << (8 * i);
            dut.traffic_rx_keep |= 1u << i;
        }
        dut.traffic_rx_last = offset_ + 8 >= frame_.size();
    }

private:
    bool good_response() const {
        return response_.size() >= 46 && response_[12] == 0x22 && response_[13] == 0xf0
            && response_[14] == 0xfb && response_[15] == 1 && (response_[16] >> 3) == 0
            && response_[36] == 0 && response_[37] == 4;
    }
    std::array<std::uint8_t, 60> frame_ = request(0);
    std::vector<std::uint8_t> response_;
    unsigned offset_ = 0;
    std::uint16_t sequence_ = 0;
    bool active_ = false;
    unsigned traced_ = 0;
};

void initialize(Vsim& dut) {
    dut.sys_reset = 1;
    dut.sys_clk = 0;
    dut.milan_clk = 0;
    dut.audio_clk = 0;
    dut.audio_tdm_clk = 0;
    dut.serial_sink_valid = 0;
    dut.serial_sink_data = 0;
    dut.serial_source_ready = 1;
    dut.traffic_rx_valid = 0;
    dut.traffic_rx_data = 0;
    dut.traffic_rx_keep = 0;
    dut.traffic_rx_last = 0;
    dut.traffic_tx_ready = 1;
    dut.probe_requests = 0;
    dut.probe_responses = 0;
    dut.probe_reads = 0;
    dut.eval();
}

std::string simulate(Vsim& dut) {
    // Integer picoseconds, scheduled at edges. No 5 ps idle evaluations.
    const std::array<std::uint64_t, 4> frequency = {sys_hz, cpu_hz, 24576000, tdm_hz};
    std::array<std::uint64_t, 4> edge = {1, 1, 1, 1};
    std::array<std::uint64_t, 4> next{};
    // Match the board PLL: every CPU rising edge meets a sys rising edge.
    // At 50/100 MHz this delays the CPU by 5 ns, as the review probe did.
    const std::array<std::uint64_t, 4> offset = {
        0, (500000000000ULL / cpu_hz - 500000000000ULL / sys_hz), 0, 0};
    for (unsigned i = 0; i < next.size(); ++i)
        next[i] = 500000000000ULL / frequency[i] + offset[i];
    std::string output;
    Controller controller;
    bool complete = false;
    constexpr std::uint64_t max_time_ps = 30000000000000ULL;
    while (!Verilated::gotFinish()) {
        const auto time_ps = *std::min_element(next.begin(), next.end());
        if (time_ps > max_time_ps) break;
        if (time_ps <= Verilated::threadContextp()->time()) {
            output += "CAPTURE_FAILED clock order";
            break;
        }
        Verilated::threadContextp()->time(time_ps);
        if (next[1] == time_ps && !dut.milan_clk) controller.sample(dut);
        if (next[0] == time_ps && !dut.sys_clk) {
            if (dut.probe_active && dut.probe_desc_ack) ++dut.probe_reads;
            if (dut.serial_source_valid) {
                const auto ch = static_cast<char>(dut.serial_source_data);
                std::putchar(ch);
                std::fflush(stdout);
                output += ch;
                complete = output.find("CAPTURE_DONE") != std::string::npos
                    || output.find("CAPTURE_FAILED") != std::string::npos;
            }
        }
        for (unsigned i = 0; i < next.size(); ++i) {
            if (next[i] != time_ps) continue;
            if (i == 0) dut.sys_clk = !dut.sys_clk;
            if (i == 1) dut.milan_clk = !dut.milan_clk;
            if (i == 2) dut.audio_clk = !dut.audio_clk;
            if (i == 3) dut.audio_tdm_clk = !dut.audio_tdm_clk;
            ++edge[i];
            // Split the quotient before multiplying: edge * 5e11 wraps
            // after 36 million edges, well inside a repeated capture run.
            next[i] = edge[i] * (500000000000ULL / frequency[i])
                + edge[i] * (500000000000ULL % frequency[i]) / frequency[i] + offset[i];
        }
        if (edge[0] > 128) dut.sys_reset = 0;
        dut.eval();
        if (!dut.milan_clk) { controller.drive(dut); dut.eval(); }
        if (complete) break;
    }
    return output;
}
} // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vsim> model;
    auto& dut = *model.get();
    milan::tb::Checker check{"nvm_capture_cpu"};
    initialize(dut);
    const auto output = simulate(dut);
    check.that("capture completed", output.find("CAPTURE_DONE") != std::string::npos);
    check.that("capture attested", output.find("ok=1") != std::string::npos);
    check.that("stage equals live", output.find("mismatches=0") != std::string::npos);
    return check.report();
}
