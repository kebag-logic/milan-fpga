// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The testbench of the region-decode simulation (#791): region_soc.py's test
// SoC runs probe.S from reset, and this observes the CPU passively at every
// rising edge of its clock. It drives only the clocks, the reset and the
// idle UART. Every line it prints is an observation, which run.py grades:
//
//   COMMIT <cycle> <pc>                   an instruction committed
//   TRAP <cycle> <interrupt> <cause>      a trap taken
//   FETCH <cycle> <address>               a fetch command on the CPU's bus (an instruction-cache refill)
//   FETCHERR <cycle>                      a fetch response with err
//   LSU <cycle> <R|W> <address> <data>    a data command on the CPU's bus, a store with its data
//   RSP <cycle> <address> <data> <err>    a data response, with its command's address
//   END <cycle> <DONE|HALT>               the probe stored its end word to the report word
#include "Vsim.h"
#include "region_config.hpp"
#include "verilator_harness.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <stdexcept>

namespace {

unsigned long long ull(std::uint64_t value) { return value; }

class Bench {
public:
    // Sample the CPU's outputs just before a rising edge of its clock.
    void sample(const Vsim& dut) {
        ++cycle_;
        if (commit_valid(dut)) std::printf("COMMIT %llu %08x\n", ull(cycle_), commit_pc(dut));
        if (trap_valid(dut))
            std::printf("TRAP %llu %u %u\n", ull(cycle_), unsigned(trap_interrupt(dut)), trap_cause(dut));
        if (fetch_cmd_valid(dut) && fetch_cmd_ready(dut))
            std::printf("FETCH %llu %08x\n", ull(cycle_), fetch_address(dut));
        if (fetch_rsp_valid(dut) && fetch_rsp_error(dut)) std::printf("FETCHERR %llu\n", ull(cycle_));
        if (lsu_cmd_valid(dut) && lsu_cmd_ready(dut)) {
            const bool write = lsu_write(dut);
            const std::uint32_t address = lsu_address(dut), data = lsu_wdata(dut);
            lsu_at_[lsu_cmd_id(dut) % lsu_at_.size()] = address;
            std::printf("LSU %llu %c %08x %08x\n", ull(cycle_), write ? 'W' : 'R', address, write ? data : 0u);
            if (write && address == report_address && (data == done_word || data == halt_word)) {
                std::printf("END %llu %s\n", ull(cycle_), data == done_word ? "DONE" : "HALT");
                done_ = true;
            }
        }
        if (lsu_rsp_valid(dut))
            std::printf("RSP %llu %08x %08x %u\n", ull(cycle_), lsu_at_[lsu_rsp_id(dut) % lsu_at_.size()],
                        lsu_rsp_data(dut), unsigned(lsu_rsp_error(dut)));
    }

    bool done() const { return done_; }

private:
    std::uint64_t cycle_ = 0;
    std::array<std::uint32_t, 4> lsu_at_{};
    bool done_ = false;
};

void initialize(Vsim& dut) {
    dut.sys_reset = 1;
    dut.sys_clk = 0;
    dut.milan_clk = 0;
    dut.audio_clk = 0;
    dut.audio_tdm_clk = 0;
    dut.serial_sink_valid = 0;
    dut.serial_source_ready = 1;
    dut.eval();
}

// The CPU budget harness's clocking: aligned rising edges, the bus at sys_hz and the CPU at cpu_hz.
void simulate(Vsim& dut, Bench& bench) {
    const std::array<std::uint64_t, 2> frequency = {sys_hz, cpu_hz};
    std::array<std::uint64_t, 2> edge = {1, 1};
    std::array<std::uint64_t, 2> next{};
    const std::array<std::uint64_t, 2> offset = {0, (500000000000ULL / cpu_hz - 500000000000ULL / sys_hz)};
    for (unsigned i = 0; i < next.size(); ++i) next[i] = 500000000000ULL / frequency[i] + offset[i];
    while (!Verilated::gotFinish() && !bench.done()) {
        const auto time_ps = *std::min_element(next.begin(), next.end());
        if (time_ps > sim_limit_ps) throw std::runtime_error("simulation exceeded its time limit");
        Verilated::threadContextp()->time(time_ps);
        if (next[1] == time_ps && !dut.milan_clk && !dut.sys_reset) bench.sample(dut);
        for (unsigned i = 0; i < next.size(); ++i) {
            if (next[i] != time_ps) continue;
            if (i == 0) dut.sys_clk = !dut.sys_clk;
            if (i == 1) dut.milan_clk = !dut.milan_clk;
            ++edge[i];
            next[i] = edge[i] * (500000000000ULL / frequency[i])
                + edge[i] * (500000000000ULL % frequency[i]) / frequency[i] + offset[i];
        }
        if (edge[0] > 128) dut.sys_reset = 0;
        dut.eval();
    }
}

}  // namespace

int main(int argc, char** argv) {
    std::setvbuf(stdout, nullptr, _IOFBF, 1 << 20);
    Verilated::commandArgs(argc, argv);
    milan::tb::Checker check{"ctrl_region_decode"};
    try {
        const milan::tb::Model<Vsim> model;
        auto& dut = *model.get();
        initialize(dut);
        Bench bench;
        simulate(dut, bench);
        check.that("the probe stored its end word", bench.done());
    } catch (const std::exception& error) {
        std::fflush(stdout);
        std::fprintf(stderr, "FAIL: %s\n", error.what());
        check.that("simulation completed without boundary failures", false);
    }
    std::fflush(stdout);
    return check.report();
}
