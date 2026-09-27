// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
#pragma once
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <stdexcept>
#include <vector>

// Reviewer probe copy of tb/verilator/fw_service_budget/flash.hpp at 7f997b60,
// adding two read-only accessors. Independent serial-command device model. Time is explicit system cycles.
// The controller, byte pump and CPU remain in the simulated product.
class Flash {
public:
    explicit Flash(std::uint64_t erase_cyc = 0, std::uint64_t program_cyc = 0)
        : bytes_(0x1000000, 0xff), erase_cyc_(erase_cyc), program_cyc_(program_cyc) {}

    void load(const char* path, std::uint32_t offset) {
        std::ifstream input(path, std::ios::binary);
        if (!input) throw std::runtime_error("cannot open flash fixture");
        char ch;
        while (input.get(ch)) bytes_.at(offset++) = static_cast<std::uint8_t>(ch);
        if (!input.eof()) throw std::runtime_error("cannot read flash fixture");
    }

    std::uint32_t transfer(std::uint32_t data, unsigned bits, unsigned width, std::uint64_t cycle) {
        if (width != 1 || bits == 0 || bits > 32 || bits % 8)
            throw std::runtime_error("unsupported flash transfer geometry");
        if (command_ == 0) {
            if (bits != 8) throw std::runtime_error("flash command must be one byte");
            command_ = data & 255;
            if (command_ != 0x0b && command_ != 0x03 && command_ != 0x05
                && command_ != 0x06 && command_ != 0x02 && command_ != 0xd8
                && command_ != 0x9f)
                throw std::runtime_error("unsupported flash opcode");
            return 0;
        }
        if (command_ == 0x05) return (cycle < busy_until_ ? 1u : 0u) | (wel_ ? 2u : 0u);
        if (command_ == 0x9f) return 0x20ba18;
        if (command_ == 0x06) throw std::runtime_error("data after write enable");
        if (address_bytes_ < 3) {
            for (unsigned left = bits; left; left -= 8) {
                address_ = (address_ << 8) | ((data >> (left - 8)) & 255);
                ++address_bytes_;
            }
            if (address_bytes_ > 3) throw std::runtime_error("flash address too long");
            cursor_ = address_;
            return 0;
        }
        if (command_ == 0x0b && !dummy_seen_) {
            if (bits != 8) throw std::runtime_error("fast-read dummy must be eight clocks");
            dummy_seen_ = true;
            return 0;
        }
        if (command_ == 0x02) {
            for (unsigned left = bits; left; left -= 8)
                program_.push_back((data >> (left - 8)) & 255);
            return 0;
        }
        if (command_ != 0x03 && command_ != 0x0b)
            throw std::runtime_error("unexpected flash payload");
        std::uint32_t result = 0;
        for (unsigned i = 0; i < bits / 8; ++i) result = (result << 8) | bytes_.at(cursor_++);
        return result;
    }

    // Return the accepted mutating opcode; reads and WREN return zero.
    unsigned deselect(std::uint64_t cycle) {
        const auto operation = command_;
        unsigned accepted = 0;
        if (operation == 0x06 && cycle >= busy_until_) wel_ = true;
        if (operation == 0xd8 || operation == 0x02) {
            if (!wel_ || cycle < busy_until_ || address_bytes_ != 3)
                throw std::runtime_error("flash write without WEL or while busy");
            // Restrict mutations to the journal, independently of firmware.
            if (address_ < 0xee0000 || address_ >= 0xf00000)
                throw std::runtime_error("flash write escaped the journal");
            if (operation == 0xd8) {
                const auto base = address_ & ~0xffffu;
                std::fill(bytes_.begin() + base, bytes_.begin() + base + 0x10000, 0xff);
                busy_until_ = cycle + erase_cyc_;
                ++erases;
            } else {
                if (program_.empty() || (address_ & 255) + program_.size() > 256)
                    throw std::runtime_error("page program wrapped or was empty");
                for (unsigned i = 0; i < program_.size(); ++i) bytes_.at(address_ + i) &= program_[i];
                busy_until_ = cycle + program_cyc_;
                ++programs;
                programmed_bytes += program_.size();
            }
            wel_ = false;
            accepted = operation;
        }
        command_ = 0;
        address_ = 0;
        address_bytes_ = 0;
        dummy_seen_ = false;
        program_.clear();
        return accepted;
    }

    std::uint64_t busy_until() const { return busy_until_; }
    // Reviewer probe: the open command and address, read before deselect().
    unsigned open_command() const { return command_; }
    std::uint32_t open_address() const { return address_; }
    std::uint8_t byte(std::uint32_t address) const { return bytes_.at(address); }
    unsigned erases = 0;
    unsigned programs = 0;
    unsigned programmed_bytes = 0;

private:
    std::vector<std::uint8_t> bytes_;
    std::vector<std::uint8_t> program_;
    std::uint64_t erase_cyc_;
    std::uint64_t program_cyc_;
    std::uint64_t busy_until_ = 0;
    unsigned command_ = 0;
    unsigned address_bytes_ = 0;
    std::uint32_t address_ = 0;
    std::uint32_t cursor_ = 0;
    bool dummy_seen_ = false;
    bool wel_ = false;
};
