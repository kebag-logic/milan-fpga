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
// It is the PHY too (#919): an IEEE 802.3 clause 22 peer on the MDIO pins at
// address kPhyAddress, 1000BASE-T full duplex negotiated, which launches bit
// k + 1 on MDC's rising edge k (22.3.4) and fails the run on a frame that is
// not a read driven then released or a write driven whole (22.2.4.5). A write
// at its address sets the register (#840's advertisement), register 0's
// restart and reset bits clearing themselves; it renegotiates at once, so its
// link is the script's alone. After the commands it holds the link for
// two polls, latches a loss that has already recovered (BMSR's latched-low
// link status, 22.2.4.2.13), then drops the link until a poll publishes it
// down and one more, and brings it back, latched, until a poll publishes it
// up.
//
// Output lines, which run.py grades:
//   CSRR <cycle> <offset> <value>   a window read
//   CSRW <cycle> <offset> <value>   a window write
//   UART <cycle> <hex byte>         a byte the firmware sent
//   READY <cycle>                   the ready line's last byte
//   STOPPED <cycle>                 a stop line's last byte (the boot refused a stage)
//   IN <cycle> <command>            a command's first byte taken by the UART
//   PHYF <first> <last> <addr> <reg> an MDIO frame: the cycles its pins left and returned to 0
//   PHYW <cycle> <addr> <reg> <value> a write frame's register and value, as the frame ends
//   PHYP <cycle> <word>             a write to milan_mac_link_status
//   PHYS <cycle> <event>            the script's link: latched, down, back
//   PHYT <high> <low> <period>      MDC's shortest high and low times and period within a frame, in bus cycles
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

//! The PHY's address: one past the first, so the boot's probe misses once.
constexpr unsigned kPhyAddress = 1u;

// The clause 22 peer on the MDIO pins (fw_service_budget/phy.hpp's, at kPhyAddress, with BMSR's latch).
class Phy {
public:
    void sample(Vsim& dut, std::uint64_t cycle) {
        const unsigned pins = dut.phy_pins;
        if (pins != 0u && previous_ == 0u && bit_ == 0u) start_ = cycle;
        if ((pins & 1u) && !(previous_ & 1u)) {
            if (bit_ > 0u) {
                low_ = std::min(low_, cycle - fall_);
                period_ = std::min(period_, cycle - rose_);
            }
            rose_ = cycle;
            rise(pins, cycle);
        }
        if (!(pins & 1u) && (previous_ & 1u)) {
            high_ = std::min(high_, cycle - rose_);
            fall_ = cycle;
        }
        if (!(pins & 1u) && bit_ == 64u && pins == 0u) {
            std::printf("PHYF %llu %llu %u %u\n", ull(start_), ull(cycle), (command_ >> 5) & 31u, command_ & 31u);
            if ((command_ >> 10) == 5u) written(cycle);
            bit_ = 0;
            command_ = 0;
            data_ = 0;
            reply_ = 1;
        }
        previous_ = pins;
        if (dut.phy_publish) {
            word_ = dut.phy_status;
            std::printf("PHYP %llu %u\n", ull(cycle), word_);
            ++publications_;
        }
    }
    void report() const { std::printf("PHYT %llu %llu %llu\n", ull(high_), ull(low_), ull(period_)); }
    unsigned reply() const { return reply_; }
    unsigned word() const { return word_; }
    unsigned publications() const { return publications_; }
    void latch() { latched_ = true; }
    void link(bool up) { up_ = up; }

private:
    void rise(unsigned pins, std::uint64_t cycle) {
        if (bit_ >= 64u) throw std::runtime_error("MDIO frame longer than 64 bit periods");
        if (bit_ < 46u) {
            if (!(pins & 2u)) throw std::runtime_error("MDIO preamble or command not driven");
            if (bit_ < 32u && !(pins & 4u)) throw std::runtime_error("MDIO preamble bit not one");
            if (bit_ >= 32u) command_ = (command_ << 1) | ((pins >> 2) & 1u);
            reply_ = 1;
        } else if ((command_ >> 10) == 5u) {
            if (!(pins & 2u)) throw std::runtime_error("MDIO write's turnaround or data not driven");
            data_ = ((data_ << 1) | ((pins >> 2) & 1u)) & 0x3ffffu;
            reply_ = 1;
        } else {
            if (pins & 2u) throw std::runtime_error("MDIO turnaround or data driven by the STA");
            if ((command_ >> 10) != 6u) throw std::runtime_error("MDIO frame not a clause 22 read or write");
            const bool addressed = ((command_ >> 5) & 31u) == kPhyAddress;
            if (bit_ == 46u) value_ = reg(command_ & 31u, addressed);
            reply_ = bit_ == 46u ? 0u : bit_ == 63u ? 1u : ((value_ >> (62u - bit_)) & 1u);
            if (!addressed) reply_ = 1;
        }
        (void)cycle;
        ++bit_;
    }
    unsigned reg(unsigned r, bool addressed) {
        if (r != 1u) return regs_[r];
        const bool latched = latched_ && addressed;
        if (latched) latched_ = false;
        return ((up_ && !latched) ? 0x0024u : 0x0020u) | (mii_100_only ? 0u : 0x0100u);
    }
    // A whole write: its turnaround 10, then the register set at the PHY's address.
    void written(std::uint64_t cycle) {
        if ((data_ >> 16) != 2u) throw std::runtime_error("MDIO write's turnaround not 10");
        const unsigned address = (command_ >> 5) & 31u, r = command_ & 31u, value = data_ & 0xffffu;
        std::printf("PHYW %llu %u %u %u\n", ull(cycle), address, r, value);
        if (address == kPhyAddress) regs_[r] = r == 0u ? value & ~0x8200u : value;
    }
    // 1000BASE-T full duplex negotiated: BMCR, PHYID1, the advertisement and the partner's, the 1000BASE-T pair and
    // the extended status, as the release's host test's PHY holds them
    std::array<unsigned, 32> regs_ = [] {
        std::array<unsigned, 32> r{};
        r[0] = 0x1000u;
        r[2] = 0x001cu;
        r[4] = 0x01e1u;
        r[5] = 0x01e1u;
        r[9] = mii_100_only ? 0u : 0x0300u;
        r[10] = mii_100_only ? 0u : 0x0c00u;
        r[15] = mii_100_only ? 0u : 0x3000u;
        return r;
    }();
    unsigned previous_ = 0, bit_ = 0, command_ = 0, reply_ = 1, value_ = 0, word_ = phy_up_word, publications_ = 0, data_ = 0;
    std::uint64_t start_ = 0, rose_ = 0, fall_ = 0;
    std::uint64_t high_ = ~0ull, low_ = ~0ull, period_ = ~0ull;
    bool latched_ = false;
    bool up_ = true;
};

class Bench {
public:
    explicit Bench(const char* transcript) : flash_(0, 0), out_(transcript) {
        if (!out_) throw std::runtime_error("cannot open the transcript");
        words_[0x000u] = 0x4d494c4eu;   // ID, 'MILN'
        words_[0x004u] = 0x00030060u;   // VERSION, as a split image reads it since the flip (#665)
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
        phy_.sample(dut, sys_);
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
        dut.phy_reply = phy_.reply();
    }

    bool done() const { return done_; }

    void report() const {
        phy_.report();
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
            next();
        } else if (step_ == 5 && sys_ >= wait_until_) {
            next();
        } else if (step_ >= 8) {
            phy_script();
        }
    }

    // The PHY's link after the commands: two polls up, a loss latched that has already recovered, then the link
    // down until a poll publishes it down and one more, then back, latched, until a poll publishes it up. A step
    // that waits past phy_step_limit_ms says so and moves on, so a run whose firmware never publishes still
    // completes and is graded: what it waited for is then missing from its log.
    void phy_script() {
        const unsigned n = phy_.publications();
        if (step_ != phy_step_) {
            phy_step_ = step_;
            phy_since_ = sys_;
            phy_mark_ = n;
        }
        const bool late = sys_ - phy_since_ > phy_step_limit_ms * (sys_hz / 1000u);
        const bool met = (step_ == 8 && phy_.word() == phy_up_word) || (step_ == 9 && n >= phy_mark_ + 2u) ||
                         (step_ == 10 && n >= phy_mark_ + 2u && phy_.word() == phy_up_word) ||
                         (step_ == 11 && n >= phy_mark_ + 3u && phy_.word() == 0u) ||
                         (step_ == 12 && n > phy_mark_ && phy_.word() == phy_up_word);
        if (!met && !late) return;
        if (!met) event("timeout");
        if (step_ == 9) {
            phy_.latch();
            event("latched");
        } else if (step_ == 10) {
            phy_.link(false);
            event("down");
        } else if (step_ == 11) {
            phy_.link(true);
            phy_.latch();
            event("back");
        } else if (step_ == 12) {
            done_ = true;
        }
        next();
    }

    void event(const char* what) const { std::printf("PHYS %llu %s\n", ull(sys_), what); }

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
    Phy phy_;
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
    unsigned phy_mark_ = 0;   // the PHY's publications as the script's last step began
    unsigned phy_step_ = 0;   // the script's step phy_since_ is of
    std::uint64_t phy_since_ = 0;
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
    dut.phy_reply = 1;
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
