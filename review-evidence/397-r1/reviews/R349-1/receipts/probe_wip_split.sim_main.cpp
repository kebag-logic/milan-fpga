// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "Vsim.h"
#include "probe_config.hpp"
#include "verilator_harness.hpp"
#include "flash.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
class Devices {
public:
    Devices(const char* aem, const char* slots, const char* commands, unsigned wait_us, unsigned page_us)
        : flash_(wait_us * (sys_hz / 1000000), page_us * (sys_hz / 1000000)) {
        flash_.load(aem, 0x400000);
        flash_.load(slots, 0xee0000);
        std::ifstream input(commands);
        if (!input) throw std::runtime_error("cannot open command plan");
        std::string line;
        while (std::getline(input, line)) commands_.push_back(line + '\n');
        if (commands_.empty()) throw std::runtime_error("empty command plan");
    }

    void sample(Vsim& dut) {
        ++cycle_;
        flash_sample(dut);
        bus_sample(dut);
        uart_sample(dut);
        if (dut.observe_nvm_request) ++requests_;
        if (dut.observe_nvm_response) {
            ++responses_;
            if (dut.observe_nvm_error) ++errors_;
        }
    }

    void drive(Vsim& dut) const {
        dut.flash_tx_ready = !pending_ && dut.flash_cs;
        dut.flash_rx_valid = pending_ && cycle_ >= response_at_;
        dut.flash_rx_data = response_;
        dut.serial_sink_valid = sending_ && send_offset_ < commands_.at(command_).size();
        dut.serial_sink_data = dut.serial_sink_valid ? commands_.at(command_).at(send_offset_) : 0;
    }

    bool done() const { return finished_; }

private:
    void flash_sample(Vsim& dut) {
        if (last_cs_ && !dut.flash_cs) {
            const auto operation = flash_.deselect(cycle_);
            if (operation) {
                std::printf("\nEVENT cycle=%llu kind=flash opcode=%u wait_cycles=%llu\n",
                            static_cast<unsigned long long>(cycle_), operation,
                            static_cast<unsigned long long>(flash_.busy_until() - cycle_));
            }
        }
        last_cs_ = dut.flash_cs;
        if (dut.flash_rx_valid && dut.flash_rx_ready) pending_ = false;
        if (dut.flash_tx_valid && dut.flash_tx_ready) {
            response_ = flash_.transfer(dut.flash_tx_data, dut.flash_tx_len, dut.flash_tx_width, cycle_);
            // 12.5 MHz SCK, 100 MHz system: eight cycles per serial bit.
            // The device-facing bridge adds one explicit completion cycle.
            response_at_ = cycle_ + dut.flash_tx_len * (sys_hz / 12500000) + 1;
            pending_ = true;
        }
    }

    void bus_sample(Vsim& dut) {
        if (dut.observe_write) {
            if (dut.observe_error) throw std::runtime_error("CSR write failed");
            const auto address = dut.observe_address & 0xffff;
            if (address == 0x920 || address == 0x93c) {
                std::printf("\nEVENT cycle=%llu kind=write address=%u value=%u requests=%u responses=%u errors=%u\n",
                            static_cast<unsigned long long>(cycle_), address, dut.observe_data,
                            requests_, responses_, errors_);
            }
        }
    }

    void uart_sample(Vsim& dut) {
        if (dut.serial_sink_valid && dut.serial_sink_ready) {
            if (send_offset_ == 0)
                std::printf("\nEVENT cycle=%llu kind=command_start index=%zu tx_bytes=%u\n",
                            static_cast<unsigned long long>(cycle_), command_, tx_bytes_);
            ++send_offset_;
            if (send_offset_ == commands_.at(command_).size()) {
                sending_ = false;
                response_text_.clear();
            }
        }
        if (!dut.serial_source_valid || !dut.serial_source_ready) return;
        const char ch = static_cast<char>(dut.serial_source_data);
        ++tx_bytes_;
        std::putchar(ch);
        response_text_ += ch;
        if (response_text_.size() > 32768) throw std::runtime_error("UART response exceeded capture bound");
        // The BIOS prints this suffix only after the handler returns.
        const std::string prompt = "litex\033[0m> ";
        if (response_text_.size() < prompt.size()
            || response_text_.compare(response_text_.size() - prompt.size(), prompt.size(), prompt)) return;
        if (started_) {
            std::printf("\nEVENT cycle=%llu kind=command_end index=%zu erases=%u programs=%u bytes=%u tx_bytes=%u\n",
                        static_cast<unsigned long long>(cycle_), command_,
                        flash_.erases, flash_.programs, flash_.programmed_bytes, tx_bytes_);
            ++command_;
        } else {
            std::printf("\nEVENT cycle=%llu kind=boot_prompt\n", static_cast<unsigned long long>(cycle_));
            started_ = true;
        }
        std::fflush(stdout);
        if (command_ == commands_.size()) {
            finished_ = true;
            return;
        }
        response_text_.clear();
        send_offset_ = 0;
        sending_ = true;
    }

    Flash flash_;
    std::vector<std::string> commands_;
    std::string response_text_;
    std::uint64_t cycle_ = 0;
    std::uint64_t response_at_ = 0;
    std::uint32_t response_ = 0;
    std::size_t command_ = 0;
    std::size_t send_offset_ = 0;
    unsigned requests_ = 0;
    unsigned responses_ = 0;
    unsigned errors_ = 0;
    unsigned tx_bytes_ = 0;
    bool pending_ = false;
    bool last_cs_ = false;
    bool sending_ = false;
    bool started_ = false;
    bool finished_ = false;
};

void initialize(Vsim& dut) {
    dut.sys_reset = 1;
    dut.sys_clk = 0;
    dut.milan_clk = 0;
    dut.audio_clk = 0;
    dut.audio_tdm_clk = 0;
    dut.serial_sink_valid = 0;
    dut.serial_source_ready = 1;
    dut.traffic_rx_valid = 0;
    dut.traffic_rx_data = 0;
    dut.traffic_rx_keep = 0;
    dut.traffic_rx_last = 0;
    dut.traffic_tx_ready = 1;
    dut.probe_requests = 0;
    dut.probe_responses = 0;
    dut.probe_reads = 0;
    dut.flash_tx_ready = 0;
    dut.flash_rx_valid = 0;
    dut.flash_rx_data = 0;
    dut.eval();
}

void simulate(Vsim& dut, Devices& devices) {
    const std::array<std::uint64_t, 4> frequency = {sys_hz, cpu_hz, 24576000, tdm_hz};
    std::array<std::uint64_t, 4> edge = {1, 1, 1, 1};
    std::array<std::uint64_t, 4> next{};
    const std::array<std::uint64_t, 4> offset = {
        0, (500000000000ULL / cpu_hz - 500000000000ULL / sys_hz), 0, 0};
    for (unsigned i = 0; i < next.size(); ++i)
        next[i] = 500000000000ULL / frequency[i] + offset[i];
    while (!Verilated::gotFinish() && !devices.done()) {
        const auto time_ps = *std::min_element(next.begin(), next.end());
        if (time_ps > 30000000000000ULL) throw std::runtime_error("simulation exceeded 30 seconds");
        if (time_ps <= Verilated::threadContextp()->time()) throw std::runtime_error("nonmonotonic clock");
        Verilated::threadContextp()->time(time_ps);
        if (next[0] == time_ps && !dut.sys_clk) devices.sample(dut);
        for (unsigned i = 0; i < next.size(); ++i) {
            if (next[i] != time_ps) continue;
            if (i == 0) dut.sys_clk = !dut.sys_clk;
            if (i == 1) dut.milan_clk = !dut.milan_clk;
            if (i == 2) dut.audio_clk = !dut.audio_clk;
            if (i == 3) dut.audio_tdm_clk = !dut.audio_tdm_clk;
            ++edge[i];
            next[i] = edge[i] * (500000000000ULL / frequency[i])
                + edge[i] * (500000000000ULL % frequency[i]) / frequency[i] + offset[i];
        }
        if (edge[0] > 128) dut.sys_reset = 0;
        dut.eval();
        if (!dut.sys_clk) { devices.drive(dut); dut.eval(); }
    }
}
} // namespace

int main(int argc, char** argv) {
    std::setvbuf(stdout, nullptr, _IOLBF, 0);
    Verilated::commandArgs(argc, argv);
    milan::tb::Checker check{"fw_service_budget"};
    try {
        if (argc != 6) throw std::runtime_error("expected AEM, slots, commands, device-wait-us");
        const milan::tb::Model<Vsim> model;
        auto& dut = *model.get();
        initialize(dut);
        Devices devices(argv[1], argv[2], argv[3], std::stoul(argv[4]), std::stoul(argv[5]));
        simulate(dut, devices);
        check.that("all UART intervals completed", devices.done());
    } catch (const std::exception& error) {
        std::fprintf(stderr, "FAIL: %s\n", error.what());
        check.that("simulation completed without boundary failures", false);
    }
    return check.report();
}
