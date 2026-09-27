// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "flash.hpp"
#include "verilator_harness.hpp"
#include <functional>

namespace {
constexpr std::uint32_t journal = 0xee0000;

void write_enable(Flash& flash, std::uint64_t cycle) {
    flash.transfer(0x06, 8, 1, cycle);
    flash.deselect(cycle);
}

void program(Flash& flash, std::uint32_t address, unsigned bytes, std::uint64_t cycle) {
    flash.transfer(0x02, 8, 1, cycle);
    flash.transfer(address, 24, 1, cycle);
    for (unsigned i = 0; i < bytes; ++i) flash.transfer(0xa5, 8, 1, cycle);
    flash.deselect(cycle);
}

unsigned status(Flash& flash, std::uint64_t cycle) {
    flash.transfer(0x05, 8, 1, cycle);
    const auto value = flash.transfer(0, 8, 1, cycle);
    flash.deselect(cycle);
    return value;
}

bool refused(const std::function<void()>& action) {
    try { action(); } catch (const std::runtime_error&) { return true; }
    return false;
}
} // namespace

int main() {
    milan::tb::Checker check{"fw_service_budget_flash"};
    Flash flash(1000, 20);
    check.hex("erased medium", flash.byte(journal), 255);
    write_enable(flash, 1);
    check.hex("WEL before program", status(flash, 1), 2);
    program(flash, journal, 256, 1);
    check.hex("last byte of full page programmed", flash.byte(journal + 255), 0xa5);
    check.hex("next page unchanged", flash.byte(journal + 256), 255);
    check.hex("busy before boundary, WEL consumed", status(flash, 20), 1);
    check.hex("ready exactly at boundary", status(flash, 21), 0);
    write_enable(flash, 22);
    flash.transfer(0xd8, 8, 1, 22);
    flash.transfer(journal, 24, 1, 22);
    flash.deselect(22);
    check.hex("erase changed programmed byte", flash.byte(journal + 255), 255);
    check.hex("erase WIP duration", status(flash, 1021), 1);
    check.hex("erase completion", status(flash, 1022), 0);
    check.that("missing write enable refused", refused([] {
        Flash device;
        program(device, journal, 1, 0);
    }));
    check.that("page wrap refused", refused([] {
        Flash device;
        write_enable(device, 0);
        program(device, journal + 255, 2, 0);
    }));
    check.that("outside journal refused", refused([] {
        Flash device;
        write_enable(device, 0);
        program(device, journal - 1, 1, 0);
    }));
    check.that("program while busy refused", refused([] {
        Flash device(0, 20);
        write_enable(device, 0);
        program(device, journal, 1, 0);
        // Prepare WEL after completion, then exercise the earlier busy time.
        // This isolates the WIP predicate; it is not a physical sequence.
        write_enable(device, 20);
        program(device, journal + 1, 1, 1);
    }));
    check.that("unknown opcode refused", refused([] {
        Flash device;
        device.transfer(0xff, 8, 1, 0);
    }));
    return check.report();
}
