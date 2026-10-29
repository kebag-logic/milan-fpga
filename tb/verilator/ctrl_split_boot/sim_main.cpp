// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The testbench of the split boot simulation (#665): the split SoC of
// boot_soc.py, booting the platform image from reset to its ready line, then
// answering the release grader's commands on its UART.
//
// It drives the clocks as the CPU budget harness does (aligned rising edges,
// the CPU at cpu_hz), the flash as that harness's native model, the mailbox's
// datapath idle with interface 0's link up and its transmit always ready, and
// it answers the Milan CSR window from a register file: gate 35's seeded words
// (sw/builder/test_builder.py, _fabric_seed), ID and VERSION as the
// datapath's, and TOD_RD_LO/HI holding the simulated time of the last
// PTP_CMD snapshot. Every figure it prints is an observed bus-cycle count.
//
// Output lines, which run.py grades:
//   CSRR <cycle> <offset> <value>   a window read
//   CSRW <cycle> <offset> <value>   a window write
//   UART <cycle> <hex byte>         a byte the firmware sent
//   READY <cycle>                   the ready line's last byte
//   STOPPED <cycle>                 a stop line's last byte (the boot refused a stage)
//   IN <cycle> <command>            a command's first byte taken by the UART
//   SUMMARY sys=<cycles> cpu=<cycles> ...
#include "Vsim.h"
#include "boot_config.hpp"
#include "flash.hpp"
#include "verilator_harness.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <fstream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

unsigned long long ull(std::uint64_t value) { return value; }

class Bench {
public:
    explicit Bench(const char* transcript) : flash_(0, 0), out_(transcript) {
        if (!out_) throw std::runtime_error("cannot open the transcript");
        words_[0x000u] = 0x4d494c4eu;   // ID, 'MILN'
        words_[0x004u] = 0x00020060u;   // VERSION, as every image before the flip (D2)
    }

    std::uint32_t word(std::uint32_t offset) const {
        auto it = words_.find(offset);
        return it == words_.end() ? (0x5a000001u | (offset << 8)) : it->second;
    }

    // Sample the outputs just before a rising bus edge.
    void sample(Vsim& dut, std::uint64_t time_ps) {
        ++sys_;
        csr_sample(dut, time_ps);
        uart_sample(dut);
        flash_sample(dut);
        script();
    }

    // Drive the inputs for the next rising edge.
    void drive(Vsim& dut) {
        dut.milan_csr_ack = csr_ack_;
        dut.milan_csr_dat_r = csr_rdata_;
        dut.serial_source_ready = 1;
        dut.serial_sink_valid = !typed_.empty();
        dut.serial_sink_data = typed_.empty() ? 0 : typed_.front();
        dut.mbx_tx_ready = 1;
        dut.mbx_link_up = 1;
        dut.flash_tx_ready = !flash_pending_ && dut.flash_cs;
        dut.flash_rx_valid = flash_pending_ && sys_ >= flash_at_;
        dut.flash_rx_data = flash_response_;
    }

    bool done() const { return done_; }

    void report() const {
        std::printf("SUMMARY sys=%llu cpu=%llu csr_reads=%u csr_writes=%u uart_bytes=%zu\n", ull(sys_),
                    ull(sys_ * cpu_hz / sys_hz), csr_reads_, csr_writes_, transcript_.size());
    }

private:
    void csr_sample(Vsim& dut, std::uint64_t time_ps) {
        if (!(dut.milan_csr_cyc && dut.milan_csr_stb) || csr_ack_) {
            csr_ack_ = false;
            return;
        }
        const std::uint32_t offset = (std::uint32_t(dut.milan_csr_adr) << 2) & (csr_size - 1u);
        if (dut.milan_csr_we) {
            const std::uint32_t value = dut.milan_csr_dat_w;
            words_[offset] = value;
            ++csr_writes_;
            std::printf("CSRW %llu %03x %08x\n", ull(sys_), offset, value);
            if (offset == 0x520u && (value & 0x4u)) {   // PTP_CMD's snapshot strobe
                const std::uint64_t ns = time_ps / 1000u;
                words_[0x530u] = std::uint32_t(ns);
                words_[0x534u] = std::uint32_t(ns >> 32);
            }
        } else {
            csr_rdata_ = word(offset);
            ++csr_reads_;
            std::printf("CSRR %llu %03x %08x\n", ull(sys_), offset, csr_rdata_);
        }
        csr_ack_ = true;
    }

    void uart_sample(Vsim& dut) {
        if (dut.serial_source_valid) {
            const char ch = char(dut.serial_source_data);
            transcript_.push_back(ch);
            out_.put(ch);
            std::printf("UART %llu %02x\n", ull(sys_), unsigned(std::uint8_t(ch)));
        }
        if (dut.serial_sink_valid && dut.serial_sink_ready && !typed_.empty()) typed_.pop_front();
    }

    void flash_sample(Vsim& dut) {
        if (flash_cs_ && !dut.flash_cs) (void)flash_.deselect(sys_);
        flash_cs_ = dut.flash_cs;
        if (dut.flash_rx_valid && dut.flash_rx_ready) flash_pending_ = false;
        if (dut.flash_tx_valid && dut.flash_tx_ready) {
            flash_response_ = flash_.transfer(dut.flash_tx_data, dut.flash_tx_len, dut.flash_tx_width, sys_);
            flash_at_ = sys_ + dut.flash_tx_len * (sys_hz / 12500000) + 1;   // a 12.5 MHz SCK
            flash_pending_ = true;
        }
    }

    bool seen(const std::string& text, std::size_t from) const {
        return transcript_.find(text, from) != std::string::npos;
    }

    // Boot to the ready line, then milan_status, milan_gettime, a millisecond, milan_gettime.
    void script() {
        if (step_ == 0 && seen(ready_line, 0)) {
            std::printf("READY %llu\n", ull(sys_));
            next();
        } else if (step_ == 0 && seen(stop_prefix, 0) && transcript_.back() == '\n') {
            std::printf("STOPPED %llu\n", ull(sys_));
            done_ = true;
        } else if (step_ == 1 || step_ == 3 || step_ == 6) {
            type(step_ == 1 ? "milan_status" : "milan_gettime");
        } else if ((step_ == 2 || step_ == 4 || step_ == 7) && seen("TAI_NS=", mark_) && transcript_.back() == '\n') {
            if (step_ == 7) done_ = true;
            next();
        } else if (step_ == 5 && sys_ >= wait_until_) {
            next();
        }
    }

    void type(const char* command) {
        std::printf("IN %llu %s\n", ull(sys_), command);
        for (const char* c = command; *c; ++c) typed_.push_back(std::uint8_t(*c));
        typed_.push_back('\r');
        mark_ = transcript_.size();
        next();
    }

    void next() {
        ++step_;
        if (step_ == 5) wait_until_ = sys_ + sys_hz / 1000u;
    }

    Flash flash_;
    std::ofstream out_;
    std::map<std::uint32_t, std::uint32_t> words_;
    std::string transcript_;
    std::deque<std::uint8_t> typed_;
    std::uint64_t sys_ = 0;
    std::uint64_t flash_at_ = 0;
    std::uint64_t wait_until_ = 0;
    std::uint32_t csr_rdata_ = 0;
    std::uint32_t flash_response_ = 0;
    unsigned csr_reads_ = 0;
    unsigned csr_writes_ = 0;
    unsigned step_ = 0;
    std::size_t mark_ = 0;
    bool csr_ack_ = false;
    bool flash_cs_ = false;
    bool flash_pending_ = false;
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
    dut.mbx_rx_valid = 0;
    dut.mbx_tx_ready = 1;
    dut.mbx_link_up = 0;
    dut.mbx_gm_change = 0;
    dut.flash_tx_ready = 0;
    dut.flash_rx_valid = 0;
    dut.milan_csr_ack = 0;
    dut.eval();
}

// The CPU budget harness's clocking: aligned rising edges, the CPU at cpu_hz.
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
        if (next[0] == time_ps && !dut.sys_clk) bench.sample(dut, time_ps);
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
        if (!dut.sys_clk) {
            bench.drive(dut);
            dut.eval();
        }
    }
}

}  // namespace

int main(int argc, char** argv) {
    std::setvbuf(stdout, nullptr, _IOFBF, 1 << 20);
    Verilated::commandArgs(argc, argv);
    milan::tb::Checker check{"ctrl_split_boot"};
    try {
        if (argc != 2) throw std::runtime_error("expected the transcript path");
        const milan::tb::Model<Vsim> model;
        auto& dut = *model.get();
        initialize(dut);
        Bench bench(argv[1]);
        simulate(dut, bench);
        check.that("the boot reached its ready line and every command answered, or a stop line", bench.done());
        bench.report();
    } catch (const std::exception& error) {
        std::fflush(stdout);
        std::fprintf(stderr, "FAIL: %s\n", error.what());
        check.that("simulation completed without boundary failures", false);
    }
    std::fflush(stdout);
    return check.report();
}
