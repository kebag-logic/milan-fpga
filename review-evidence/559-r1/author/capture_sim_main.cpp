// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "Vsim.h"
#include "verilator_harness.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <string>

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vsim> model;
    auto* dut = model.get();
    milan::tb::Checker check{"capture_cpu_preflight"};
    dut->sys_reset = 1;
    dut->sys_clk = 0;
    dut->milan_clk = 0;
    dut->audio_clk = 0;
    dut->serial_sink_valid = 0;
    dut->serial_sink_data = 0;
    dut->serial_source_ready = 1;
    dut->eval();
    const std::array<std::uint64_t, 3> frequency = {100000000, 100000000, 24576000};
    std::array<std::uint64_t, 3> edge = {1, 1, 1};
    std::array<std::uint64_t, 3> next = {5000, 5000, 20345};
    std::string output;
    constexpr std::uint64_t max_time_ps = 5000000000000ULL;
    while (!Verilated::gotFinish()) {
        const auto time_ps = *std::min_element(next.begin(), next.end());
        if (time_ps > max_time_ps) break;
        Verilated::threadContextp()->time(time_ps);
        if (next[0] == time_ps) {
            if (!dut->sys_clk && dut->serial_source_valid) {
                const auto ch = static_cast<char>(dut->serial_source_data);
                std::putchar(ch);
                std::fflush(stdout);
                output += ch;
            }
            dut->sys_clk = !dut->sys_clk;
            if (edge[0] > 128) dut->sys_reset = 0;
            next[0] = (++edge[0] * 500000000000ULL) / frequency[0];
        }
        if (next[1] == time_ps) {
            dut->milan_clk = !dut->milan_clk;
            next[1] = (++edge[1] * 500000000000ULL) / frequency[1];
        }
        if (next[2] == time_ps) {
            dut->audio_clk = !dut->audio_clk;
            next[2] = (++edge[2] * 500000000000ULL) / frequency[2];
        }
        dut->eval();
        if (output.find("CAPTURE_DONE") != std::string::npos) break;
    }
    check.that("capture completed", output.find("CAPTURE_DONE") != std::string::npos);
    check.that("capture attested", output.find("ok=1") != std::string::npos);
    check.that("stage equals live", output.find("mismatches=0") != std::string::npos);
    return check.report();
}
