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
//   LSU <cycle> <R|W> <address> <data>    a completed cached load or committed store
//   RSP <cycle> <address> <data> <err>    a completed load, with its address and actual data
//   BUS <cycle> <C|I> <address>         a cache refill or I/O command
//   DATAERR <cycle>                     a data-cache refill returned an error
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
        if (refill_valid(dut) && refill_ready(dut))
            std::printf("BUS %llu C %08x\n", ull(cycle_), refill_address(dut));
        if (io_valid(dut) && io_ready(dut))
            std::printf("BUS %llu I %08x\n", ull(cycle_), io_address(dut));
        if (refill_error_valid(dut) && refill_error(dut)) std::printf("DATAERR %llu\n", ull(cycle_));
        // The Whiteboxer store signal also marks cache-miss retries. Only
        // architectural commits report the probe once. Both are stage 4.
        if (store_valid(dut) && commit_valid(dut)) {
            const std::uint32_t address = store_address(dut), data = store_data(dut);
            std::printf("LSU %llu W %08x %08x\n", ull(cycle_), address, data);
            if (address == report_address && (data == done_word || data == halt_word)) {
                std::printf("END %llu %s\n", ull(cycle_), data == done_word ? "DONE" : "HALT");
                done_ = true;
            }
        }
        if (load_valid(dut) && commit_valid(dut)) {
            std::printf("LSU %llu R %08x 00000000\n", ull(cycle_), load_address(dut));
            std::printf("RSP %llu %08x %08x 0\n", ull(cycle_), load_address(dut), load_data(dut));
        }
    }

    bool done() const { return done_; }

private:
    std::uint64_t cycle_ = 0;
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

// The CPU budget harness's clocking: CPU and bus on sys_hz; the independent datapath clock is milan_hz.
void simulate(Vsim& dut, Bench& bench) {
    const std::array<std::uint64_t, 2> frequency = {sys_hz, milan_hz};
    std::array<std::uint64_t, 2> edge = {1, 1};
    std::array<std::uint64_t, 2> next{};
    const std::array<std::uint64_t, 2> offset = {0, (500000000000ULL / milan_hz - 500000000000ULL / sys_hz)};
    for (unsigned i = 0; i < next.size(); ++i) next[i] = 500000000000ULL / frequency[i] + offset[i];
    while (!Verilated::gotFinish() && !bench.done()) {
        const auto time_ps = *std::min_element(next.begin(), next.end());
        if (time_ps > sim_limit_ps) throw std::runtime_error("simulation exceeded its time limit");
        Verilated::threadContextp()->time(time_ps);
        if (next[0] == time_ps && !dut.sys_clk && !dut.sys_reset) bench.sample(dut);
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
