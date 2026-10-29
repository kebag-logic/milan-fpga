// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// plat_bus.hpp - the split platform's bus on the host (#665 S3): the datapath
// CSR window as a register file and LiteX's UART as two queues, behind
// ctrl_plat_io.h. Every access is logged in order, so a test reads the boot's
// writes as the bus would carry them.
//
// The CSR window's words start as builder gate 35's host register file holds
// them (sw/builder/test_builder.py, _fabric_seed): bit 0 set and bit 3 clear,
// the offset in the middle, so a cleared enable or a set bit changes the word
// and names it. ID and VERSION start as the datapath's.

#ifndef PLAT_BUS_HPP
#define PLAT_BUS_HPP

#include <cstdint>
#include <deque>
#include <map>
#include <string>
#include <vector>

#include "ctrl_plat_console.h"
#include "ctrl_plat_csr.h"
#include "ctrl_plat_io.h"

namespace plat_bus {

constexpr std::uintptr_t kCsr = 0x90000000u;
constexpr std::uintptr_t kUart = 0xf0001000u;
constexpr ctrl_plat_uart kUartRegs = {kUart + 0x0u, kUart + 0x4u, kUart + 0x8u, kUart + 0x10u};
constexpr std::uint32_t kVersion = 0x00020060u;

struct Access {
    bool write;
    std::uintptr_t address;
    std::uint32_t value;
};

inline std::uint32_t seed(std::uint32_t offset) { return 0x5A000001u | (offset << 8); }

struct Bus {
    std::map<std::uint32_t, std::uint32_t> csr;   // by offset
    std::vector<Access> log;
    std::deque<std::uint8_t> rx;                  // bytes the UART has received
    std::string tx;                               // bytes the UART sent
    unsigned tx_room = ~0u;                       // bytes the transmit FIFO takes before TXFULL
    unsigned overruns = 0;                        // RXTX written while TXFULL was set
    std::deque<std::uint32_t> tod_hi;             // TOD_RD_HI's answers, in order (then the register)
    std::vector<std::uint64_t> stamps;            // a caller-maintained clock per access (optional)

    void reset() {
        csr.clear();
        log.clear();
        rx.clear();
        tx.clear();
        tx_room = ~0u;
        overruns = 0;
        tod_hi.clear();
        csr[CTRL_PLAT_CSR_ID] = CTRL_PLAT_MILAN_ID;
        csr[CTRL_PLAT_CSR_VERSION] = kVersion;
    }
    std::uint32_t word(std::uint32_t offset) const {
        auto it = csr.find(offset);
        return it == csr.end() ? seed(offset) : it->second;
    }
    void type(const std::string& text) { rx.insert(rx.end(), text.begin(), text.end()); }
    // The CSR window's writes, as (offset, value), in order.
    std::vector<std::pair<std::uint32_t, std::uint32_t>> writes() const {
        std::vector<std::pair<std::uint32_t, std::uint32_t>> out;
        for (const auto& a : log) {
            if (a.write && a.address >= kCsr && a.address < kCsr + 0x10000u) {
                out.emplace_back(static_cast<std::uint32_t>(a.address - kCsr), a.value);
            }
        }
        return out;
    }
    std::uint32_t read(std::uintptr_t address) {
        std::uint32_t value = 0;
        if (address == kUartRegs.rxempty) {
            value = rx.empty() ? 1u : 0u;
        } else if (address == kUartRegs.rxtx) {
            value = rx.empty() ? 0u : rx.front();
        } else if (address == kUartRegs.txfull) {
            value = tx_room == 0u ? 1u : 0u;
        } else if (address >= kCsr && address < kCsr + 0x10000u) {
            auto offset = static_cast<std::uint32_t>(address - kCsr);
            if (offset == CTRL_PLAT_CSR_TOD_RD_HI && !tod_hi.empty()) {
                value = tod_hi.front();
                tod_hi.pop_front();
            } else {
                value = word(offset);
            }
        }
        log.push_back({false, address, value});
        return value;
    }
    void write(std::uintptr_t address, std::uint32_t value) {
        log.push_back({true, address, value});
        if (address == kUartRegs.ev_pending && (value & CTRL_PLAT_UART_EV_RX) != 0u && !rx.empty()) {
            rx.pop_front();
        } else if (address == kUartRegs.rxtx) {
            tx.push_back(static_cast<char>(value));
            overruns += tx_room == 0u;
            if (tx_room != ~0u && tx_room != 0u) --tx_room;
        } else if (address >= kCsr && address < kCsr + 0x10000u) {
            csr[static_cast<std::uint32_t>(address - kCsr)] = value;
        }
    }
    // Accesses from log position `from` on, at `address`.
    unsigned count(std::size_t from, std::uintptr_t address, bool write) const {
        unsigned n = 0;
        for (std::size_t k = from; k < log.size(); ++k) n += log[k].address == address && log[k].write == write;
        return n;
    }
};

// The bus the test's ctrl_plat_io.h answers from (defined in plat_bus.cpp).
Bus& bus();

}  // namespace plat_bus

#endif  // PLAT_BUS_HPP
